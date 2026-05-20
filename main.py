import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from ui.main_window import MainWindow
from core.ai_client import EthicalAIClient

class AIWorker(QThread):
    """
    Thread separada para evitar que a interface gráfica (UI) congele 
    enquanto aguardamos a resposta da API (que pode levar segundos).
    """
    finished = pyqtSignal(str)

    def __init__(self, ai_client: EthicalAIClient, scenario: str = None, choice: bool = None):
        super().__init__()
        self.ai_client = ai_client
        self.scenario = scenario
        self.choice = choice

    def run(self):
        if self.scenario is None:
            # É a primeira inicialização
            result = self.ai_client.generate_initial_scenario()
        else:
            # É uma resposta a uma escolha
            result = self.ai_client.generate_consequence(self.scenario, self.choice)
        
        self.finished.emit(result)


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.ai_client = EthicalAIClient(api_key="SUA_CHAVE_AQUI")
        
        self.current_scenario = ""
        self.is_processing = False
        
        # Conecta os botões da UI ao processamento
        self.window.choice_made.connect(self.handle_user_choice)

        # Dispara a geração do primeiro dilema ao abrir
        self.request_ai_generation()

    def handle_user_choice(self, choice: bool):
        """Recebe o clique do botão (True=Sim, False=Não)."""
        if self.is_processing:
            return # Evita cliques duplos enquanto a API responde
            
        texto_escolha = "SIM" if choice else "NÃO"
        
        # Registra a escolha na tela
        self.window.chat_display.append(
            f'<div style="text-align: right; color: #BB86FC; margin: 10px 0;"><b>ESCOLHA: {texto_escolha}</b></div>'
        )
        
        # Solicita a nova consequência à API
        self.request_ai_generation(self.current_scenario, choice)

    def request_ai_generation(self, scenario: str = None, choice: bool = None):
        """Inicia a Thread que fará a chamada de rede para a API."""
        self.is_processing = True
        self.window.display_scenario("<i>Processando desdobramentos éticos com IA...</i>")
        
        # Desabilita botões temporariamente
        self.window.btn_yes.setEnabled(False)
        self.window.btn_no.setEnabled(False)

        # Inicia a Thread
        self.worker = AIWorker(self.ai_client, scenario, choice)
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    def on_ai_response(self, response_text: str):
        """Recebe o texto da API quando a Thread terminar."""
        self.current_scenario = response_text
        self.window.display_scenario(self.current_scenario)
        
        # Reabilita interface
        self.is_processing = False
        self.window.btn_yes.setEnabled(True)
        self.window.btn_no.setEnabled(True)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()