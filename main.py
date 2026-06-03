import json
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from ui.main_window import MainWindow
from core.ai_client import EthicalAIClient
from core.data_parser import parse_serial_line
from hardware.serial_client import SerialReadThread


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    config = {
        "serial_port": "COM3",
        "baud_rate": 9600,
        "timeout": 1.0
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                user_config = json.load(config_file)
                config.update(user_config)
        except Exception as error:
            print(f"Aviso: falha ao carregar config.json: {error}")

    return config

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

        self.config = load_config()
        self.serial_thread = SerialReadThread(
            port=self.config["serial_port"],
            baudrate=self.config["baud_rate"],
            timeout=self.config["timeout"]
        )
        self.serial_thread.line_received.connect(self.on_serial_line)
        self.serial_thread.error.connect(self.on_serial_error)
        self.serial_thread.start()

        self.window.choice_made.connect(self.handle_user_choice)
        self.app.aboutToQuit.connect(self.stop_serial)

        self.request_ai_generation()

    def on_serial_line(self, raw_line: str):
        parsed = parse_serial_line(raw_line)
        if parsed is None or self.is_processing:
            return

        user_choice = parsed.get("choice")
        if user_choice is None:
            return

        label = "SIM" if user_choice else "NÃO"
        self.window.chat_display.append(
            f'<div style="text-align: left; color: #82DAFF; margin: 10px 0;"><b>Arduino: {label}</b></div>'
        )

        self.handle_user_choice(user_choice)

    def on_serial_error(self, message: str):
        self.window.chat_display.append(
            f'<div style="text-align: center; color: #CF6679; margin: 10px 0;"><b>Erro Serial:</b> {message}</div>'
        )

    def stop_serial(self):
        if hasattr(self, "serial_thread") and self.serial_thread is not None:
            self.serial_thread.stop()

    def handle_user_choice(self, choice: bool):
        if self.is_processing:
            return

        texto_escolha = "SIM" if choice else "NÃO"
        self.window.chat_display.append(
            f'<div style="text-align: right; color: #BB86FC; margin: 10px 0;"><b>ESCOLHA: {texto_escolha}</b></div>'
        )

        self.request_ai_generation(self.current_scenario, choice)

    def request_ai_generation(self, scenario: str = None, choice: bool = None):
        self.is_processing = True
        self.window.display_scenario("<i>Processando desdobramentos éticos com IA...</i>")

        self.window.btn_yes.setEnabled(False)
        self.window.btn_no.setEnabled(False)

        self.worker = AIWorker(self.ai_client, scenario, choice)
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    def on_ai_response(self, response_text: str):
        self.current_scenario = response_text
        self.window.display_scenario(self.current_scenario)

        self.is_processing = False
        self.window.btn_yes.setEnabled(True)
        self.window.btn_no.setEnabled(True)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()