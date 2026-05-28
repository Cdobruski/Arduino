from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class MainWindow(QMainWindow):
    # Sinal puro: emite True para SIM e False para NÃO
    choice_made = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dilemas Éticos - Interação Arduino/IA")
        self.resize(900, 700)
        # Fonte base aumentada para 20px
        self.setStyleSheet("background-color: #0F0F0F; color: #E0E0E0; font-size: 20px; font-family: 'Segoe UI', Arial;")
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)

        # Tela de texto com fonte de 24px
        self.display = QTextBrowser()
        self.display.setStyleSheet("background-color: #1A1A1A; border-radius: 12px; padding: 20px; font-size: 24px; line-height: 1.5;")
        layout.addWidget(self.display)

        # Botões maiores
        btn_layout = QHBoxLayout()
        
        self.btn_yes = QPushButton("SIM")
        self.btn_yes.setStyleSheet("background-color: #03DAC6; color: #000; padding: 20px; border-radius: 8px; font-weight: bold;")
        self.btn_yes.setCursor(Qt.PointingHandCursor)
        self.btn_yes.clicked.connect(lambda: self.choice_made.emit(True))
        
        self.btn_no = QPushButton("NÃO")
        self.btn_no.setStyleSheet("background-color: #CF6679; color: #FFF; padding: 20px; border-radius: 8px; font-weight: bold;")
        self.btn_no.setCursor(Qt.PointingHandCursor)
        self.btn_no.clicked.connect(lambda: self.choice_made.emit(False))

        btn_layout.addWidget(self.btn_no)
        btn_layout.addWidget(self.btn_yes)
        layout.addLayout(btn_layout)

    def update_text(self, text: str):
        """Método público para o controlador injetar texto na tela."""
        self.display.append(f'<div style="margin-top: 15px;">{text}</div>')

    def end_session(self):
        """Desativa e escurece os botões ao final das 5 perguntas."""
        self.btn_yes.setEnabled(False)
        self.btn_no.setEnabled(False)
        self.btn_yes.setStyleSheet("background-color: #333; color: #666; padding: 20px; border-radius: 8px;")
        self.btn_no.setStyleSheet("background-color: #333; color: #666; padding: 20px; border-radius: 8px;")