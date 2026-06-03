import serial
from PyQt5.QtCore import QThread, pyqtSignal


class SerialReadThread(QThread):
    line_received = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, port="COM3", baudrate=9600, timeout=1.0):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._running = True
        self.serial_port = None

    def run(self):
        try:
            self.serial_port = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
        except Exception as error:
            self.error.emit(f"Falha ao abrir porta serial {self.port}: {error}")
            return

        while self._running:
            try:
                raw_line = self.serial_port.readline()
                if not raw_line:
                    continue

                line = raw_line.decode("utf-8", errors="replace").strip()
                if line:
                    self.line_received.emit(line)
            except Exception as error:
                self.error.emit(f"Erro na leitura serial: {error}")
                break

        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def stop(self):
        self._running = False
        self.wait(1000)
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def write(self, message: str):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write((message.strip() + "\n").encode("utf-8"))
            except Exception as error:
                self.error.emit(f"Falha ao enviar comando ao Arduino: {error}")
