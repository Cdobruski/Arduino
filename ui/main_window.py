from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

DARK_THEME = """
QMainWindow { background-color: #0F0F0F; }
QWidget { background-color: #0F0F0F; color: #E0E0E0; font-family: 'Urbanist', sans-serif; }
QTextBrowser { 
    background-color: #1A1A1A; border: 1px solid #333; 
    border-radius: 12px; padding: 15px; font-size: 16px; 
}
QPushButton {
    border-radius: 8px; padding: 15px; font-weight: bold; font-size: 16px; min-width: 120px;
}
/* Estilo para botão SIM/Positivo */
QPushButton#btn_yes { background-color: #03DAC6; color: #000; }
QPushButton#btn_yes:hover { background-color: #01B3A1; }

/* Estilo para botão NÃO/Negativo */
QPushButton#btn_no { background-color: #CF6679; color: #FFF; }
QPushButton#btn_no:hover { background-color: #B05566; }
"""

class MainWindow(QMainWindow):
    # Emitimos um booleano: True para SIM, False para NÃO
    choice_made = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dilemas Éticos - Escolha sua Consequência")
        self.resize(800, 600)
        self.setStyleSheet(DARK_THEME)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        self.chat_display = QTextBrowser()
        main_layout.addWidget(self.chat_display)

        # Botões de Escolha
        choice_layout = QHBoxLayout()
        choice_layout.setSpacing(20)
        
        self.btn_yes = QPushButton("SIM")
        self.btn_yes.setObjectName("btn_yes")
        self.btn_yes.setCursor(Qt.PointingHandCursor)
        self.btn_yes.clicked.connect(lambda: self.choice_made.emit(True))
        
        self.btn_no = QPushButton("NÃO")
        self.btn_no.setObjectName("btn_no")
        self.btn_no.setCursor(Qt.PointingHandCursor)
        self.btn_no.clicked.connect(lambda: self.choice_made.emit(False))

        choice_layout.addWidget(self.btn_no)
        choice_layout.addWidget(self.btn_yes)
        
        main_layout.addLayout(choice_layout)

    def display_scenario(self, text: str):
        """Injeta o novo cenário ou consequência na tela."""
        msg = f'<div style="margin-top:20px; border-left: 4px solid #BB86FC; padding-left: 15px;">{text}</div>'
        self.chat_display.append(msg)