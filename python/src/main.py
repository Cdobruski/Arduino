import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from ui.main_window import MainWindow
from core.ai_client import EthicalAIClient

class AIWorker(QThread):
    finished = pyqtSignal(str)

    # Adicionamos o is_final aqui no worker
    def __init__(self, ai_client, scenario=None, choice=None, is_final=False):
        super().__init__()
        self.ai_client = ai_client
        self.scenario = scenario
        self.choice = choice
        self.is_final = is_final

    def run(self):
        try:
            if self.scenario is None:
                res = self.ai_client.generate_initial_scenario()
            else:
                # Passa a flag para a IA saber se é a última rodada
                res = self.ai_client.generate_consequence(self.scenario, self.choice, self.is_final)
            self.finished.emit(res)
        except Exception as e:
            self.finished.emit(f"Erro na IA: {str(e)}")


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.ai = EthicalAIClient()
        self.current_scenario = ""
        
        # Variáveis de controle de limite
        self.interaction_count = 0
        self.MAX_INTERACTIONS = 5 
        
        self.window.choice_made.connect(self.process_choice)
        self.fetch_ai_response()

    def process_choice(self, choice: bool):
        self.interaction_count += 1
        is_final = (self.interaction_count >= self.MAX_INTERACTIONS)
        
        self.window.btn_yes.setEnabled(False)
        self.window.btn_no.setEnabled(False)
        
        self.window.update_text(f'<div style="text-align: right; color: #BB86FC; margin: 15px 0;"><b>ESCOLHA: {"SIM" if choice else "NÃO"}</b></div>')
        self.window.update_text('<i style="color: #888;">Analisando desdobramentos...</i>')
        
        self.fetch_ai_response(self.current_scenario, choice, is_final)

    def fetch_ai_response(self, scenario=None, choice=None, is_final=False):
        self.worker = AIWorker(self.ai, scenario, choice, is_final)
        self.worker.finished.connect(self.on_ai_done)
        self.worker.start()

    def on_ai_done(self, result: str):
        self.current_scenario = result
        
        # 1. Converte quebras de linha do texto (Enter) para quebras de linha HTML (<br>)
        texto_formatado = self.current_scenario.replace('\n', '<br>')
        
        # 2. Muda a cor da fonte para branco (#FFFFFF)
        self.window.update_text(f'<div style="color: #FFFFFF;">{texto_formatado}</div>')
        
        # Se chegou no limite, finaliza a sessão. Se não, libera os botões.
        if self.interaction_count >= self.MAX_INTERACTIONS:
            self.window.end_session()
            self.window.update_text('<div style="text-align: center; color: #CF6679; margin-top: 20px;"><b>[ FIM DA SIMULAÇÃO ]</b></div>')
        else:
            self.window.btn_yes.setEnabled(True)
            self.window.btn_no.setEnabled(True)

    def run(self):
        """Exibe a janela e inicia o loop da aplicação."""
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()