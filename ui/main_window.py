from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextBrowser, QFrame
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPixmap, QColor
import math
import random


def _make_background(width: int, height: int) -> QPixmap:
    pm = QPixmap(width, height)
    pm.fill(QColor(8, 10, 22))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, False)

    PX      = 3
    HORIZON = int(height * 0.60)
    MOON_R  = 68
    CX      = width // 2
    CY      = HORIZON - MOON_R

    # Céu degradê
    for y in range(0, HORIZON, PX):
        t = y / HORIZON
        p.fillRect(0, y, width, PX,
                   QColor(int(8+t*8), int(10+t*12), int(22+t*26)))

    # Estrelas
    rng = random.Random(42)
    star_pal = [QColor(255,255,255), QColor(220,235,255),
                QColor(255,250,200), QColor(200,215,255), QColor(255,235,180)]
    for _ in range(130):
        sx = rng.randint(0, width-PX)
        sy = rng.randint(0, HORIZON-PX*5)
        sz = rng.choice([PX, PX, PX, PX, PX*2])
        p.fillRect(sx, sy, sz, sz, rng.choice(star_pal))
    for _ in range(12):
        sx = rng.randint(PX*2, width-PX*3)
        sy = rng.randint(PX*2, HORIZON-PX*8)
        c  = QColor(255, 252, 210, 220)
        p.fillRect(sx,     sy-PX, PX,   PX*3, c)
        p.fillRect(sx-PX,  sy,    PX*3, PX,   c)

    # Lua
    L = dict(hi=QColor(255,252,235), b=QColor(245,238,210),
             sh=QColor(205,197,165), dsh=QColor(175,167,135), rim=QColor(155,148,118))
    for py in range(CY-MOON_R-PX, HORIZON+PX, PX):
        for px in range(CX-MOON_R-PX, CX+MOON_R+PX, PX):
            dx, dy = px-CX, py-CY
            d = math.hypot(dx, dy)
            if d > MOON_R:
                continue
            light = (-0.6*dx - 0.8*dy) / MOON_R
            if   d > MOON_R-PX*2: col = L['rim']
            elif light > 0.35:    col = L['hi']
            elif light > -0.1:    col = L['b']
            elif light > -0.4:    col = L['sh']
            else:                 col = L['dsh']
            p.fillRect(px, py, PX, PX, col)

    # Crateras
    for ox, oy, cr in [(-28,-18,11),(18,-12,8),(-12,22,10),
                        (32,12,7),(-38,12,6),(6,-38,9),(20,30,5)]:
        cx, cy = CX+ox, CY+oy
        for py in range(cy-cr-PX, cy+cr+PX, PX):
            for px in range(cx-cr-PX, cx+cr+PX, PX):
                ddx, ddy = px-cx, py-cy
                if ddx*ddx+ddy*ddy > cr*cr: continue
                if (px-CX)**2+(py-CY)**2 > MOON_R*MOON_R: continue
                inner = ddx*ddx+ddy*ddy <= (cr-PX)*(cr-PX)
                p.fillRect(px, py, PX, PX,
                           QColor(172,165,133) if inner else QColor(208,200,168))

    # Halo lunar
    for extra, alpha in [(4,55),(10,28),(20,12)]:
        gr = MOON_R + extra
        for py in range(CY-gr-PX, HORIZON+PX, PX):
            for px in range(CX-gr-PX, CX+gr+PX, PX):
                d = math.hypot(px-CX, py-CY)
                if MOON_R < d <= gr:
                    p.fillRect(px, py, PX, PX, QColor(200,188,148,alpha))

    # Água
    for y in range(HORIZON, height, PX):
        t = (y-HORIZON) / max(1, height-HORIZON)
        p.fillRect(0, y, width, PX,
                   QColor(int(10+t*4), int(14+t*6), int(28+t*14)))
    p.fillRect(0, HORIZON-PX, width, PX*2, QColor(35, 55, 100, 130))

    # Reflexo da lua na água
    rng2 = random.Random(77)
    for y in range(HORIZON, height, PX):
        t  = (y-HORIZON) / max(1, height-HORIZON)
        ww = int(MOON_R*2*(1+t*1.8))
        wo = int(rng2.uniform(-3, 3)*PX*t*2)
        intensity = max(0.0, 1.0-t*1.1)
        for px in range(CX-ww//2+wo, CX+ww//2+wo, PX):
            if not 0 <= px < width: continue
            fade = max(0.0, 1.0 - abs(px-(CX+wo)) / max(1, ww//2))
            rv = int(215*intensity*fade)
            gv = int(200*intensity*fade)
            bv = int(148*intensity*fade)
            if rv > 6 or gv > 6:
                p.fillRect(px, y, PX, PX, QColor(rv, gv, bv))

    # Cintilações na água
    rng3 = random.Random(55)
    for _ in range(45):
        ry = rng3.randint(HORIZON+PX*2, height-PX*2)
        p.fillRect(rng3.randint(0, width-PX*5), ry,
                   rng3.randint(PX*2, PX*10), PX,
                   QColor(80, 130, 200, rng3.randint(25, 70)))

    # Brilho difuso no horizonte
    for y in range(HORIZON, min(HORIZON+90, height), PX):
        t2 = (y-HORIZON) / 90
        gw = int(MOON_R*3.5*(1-t2*0.5))
        a  = int(45*(1-t2))
        if a > 0:
            p.fillRect(CX-gw//2, y, gw, PX, QColor(205, 190, 140, a))

    p.end()
    return pm


class _Canvas(QWidget):
    """Widget central que pinta o fundo pixel-art."""
    def __init__(self, bg: QPixmap, parent=None):
        super().__init__(parent)
        self._bg = bg
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(
            self.rect(),
            self._bg.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation),
        )


class MainWindow(QMainWindow):
    choice_made = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dilemas Éticos — Arduino & IA")
        self.resize(900, 700)
        self.setMinimumSize(700, 500)
        self._setup_ui()

    def _setup_ui(self):
        bg     = _make_background(900, 700)
        canvas = _Canvas(bg)
        self.setCentralWidget(canvas)

        outer = QVBoxLayout(canvas)
        outer.setContentsMargins(50, 40, 50, 40)

        panel = QFrame()
        panel.setObjectName("glassPanel")
        panel.setAutoFillBackground(False)
        panel.setStyleSheet("""
            QFrame#glassPanel {
                background-color: rgba(4, 7, 18, 188);
                border: 1px solid rgba(158, 146, 106, 48);
                border-radius: 16px;
            }
        """)

        inner = QVBoxLayout(panel)
        inner.setContentsMargins(28, 24, 28, 24)

        self.chat_display = QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        self.chat_display.viewport().setAutoFillBackground(False)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                border: none;
                color: #F0EAD6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 17px;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 7px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(155, 142, 105, 120);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical  { height: 0; }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical  { background: transparent; }
        """)
        inner.addWidget(self.chat_display)
        outer.addWidget(panel)

    def display_scenario(self, text: str):
        formatted = text.replace('\n', '<br>')
        self.chat_display.append(
            '<div style="margin-top:16px; padding:10px 14px; '
            'border-left:3px solid rgba(200,185,130,200); '
            'color:#F2EDD5; font-size:17px; line-height:1.65;">'
            f'{formatted}</div>'
        )

    def end_session(self):
        pass
