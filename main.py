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
    # Quando frozen (exe), config.json fica ao lado do executável
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base, "config.json")
    config = {
        "serial_port": "COM3",
        "baud_rate": 9600,
        "timeout": 1.0,
        "gemini_api_key": "",
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                config.update(json.load(config_file))
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

        self.current_scenario = ""
        self.is_processing = False

        self.config = load_config()
        self.ai_client = EthicalAIClient(api_key=self.config.get("gemini_api_key", ""))
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
        line = raw_line.strip()

        if line == "ARDUINO_READY":
            self.window.chat_display.append(
                '<div style="text-align:center; color:#4FC3A1; margin:12px 0;">'
                '<b>— Arduino conectado e pronto —</b></div>'
            )
            return

        parsed = parse_serial_line(line)
        if parsed is None:
            return

        user_choice = parsed.get("choice")
        if user_choice is None:
            return

        if self.is_processing:
            self.window.chat_display.append(
                '<div style="text-align:center; color:#888; margin:6px 0; font-size:14px;">'
                '<i>Aguarde a IA responder antes de pressionar novamente.</i></div>'
            )
            return

        label = "SIM" if user_choice else "NÃO"
        self.window.chat_display.append(
            f'<div style="text-align:left; color:#82DAFF; margin:10px 0;"><b>Arduino: {label}</b></div>'
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

        self.worker = AIWorker(self.ai_client, scenario, choice)
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    def on_ai_response(self, response_text: str):
        self.current_scenario = response_text
        self.window.display_scenario(self.current_scenario)

        self.is_processing = False

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()