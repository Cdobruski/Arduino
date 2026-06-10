from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextBrowser, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QColor
import math
import random

# ── Constantes do canvas ──────────────────────────────────────────────────────
_BG_W    = 900
_BG_H    = 700
_HORIZON = int(_BG_H * 0.60)   # 420
_MOON_R  = 68
_CX      = _BG_W // 2          # 450
_CY      = _HORIZON - _MOON_R  # 352


# ── Geração do fundo estático (céu, lua, água) ────────────────────────────────

def _make_background() -> QPixmap:
    pm = QPixmap(_BG_W, _BG_H)
    pm.fill(QColor(8, 10, 22))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, False)
    PX = 3

    # Céu degradê
    for y in range(0, _HORIZON, PX):
        t = y / _HORIZON
        p.fillRect(0, y, _BG_W, PX, QColor(int(8+t*8), int(10+t*12), int(22+t*26)))

    # Lua
    L = dict(hi=QColor(255,252,235), b=QColor(245,238,210),
             sh=QColor(205,197,165), dsh=QColor(175,167,135), rim=QColor(155,148,118))
    for py in range(_CY-_MOON_R-PX, _HORIZON+PX, PX):
        for px in range(_CX-_MOON_R-PX, _CX+_MOON_R+PX, PX):
            dx, dy = px-_CX, py-_CY
            d = math.hypot(dx, dy)
            if d > _MOON_R:
                continue
            light = (-0.6*dx - 0.8*dy) / _MOON_R
            if   d > _MOON_R-PX*2: col = L['rim']
            elif light > 0.35:     col = L['hi']
            elif light > -0.1:     col = L['b']
            elif light > -0.4:     col = L['sh']
            else:                  col = L['dsh']
            p.fillRect(px, py, PX, PX, col)

    # Crateras
    for ox, oy, cr in [(-28,-18,11),(18,-12,8),(-12,22,10),
                        (32,12,7),(-38,12,6),(6,-38,9),(20,30,5)]:
        cx, cy = _CX+ox, _CY+oy
        for py in range(cy-cr-PX, cy+cr+PX, PX):
            for px in range(cx-cr-PX, cx+cr+PX, PX):
                ddx, ddy = px-cx, py-cy
                if ddx*ddx+ddy*ddy > cr*cr: continue
                if (px-_CX)**2+(py-_CY)**2 > _MOON_R*_MOON_R: continue
                inner = ddx*ddx+ddy*ddy <= (cr-PX)*(cr-PX)
                p.fillRect(px, py, PX, PX, QColor(172,165,133) if inner else QColor(208,200,168))

    # Halo lunar
    for extra, alpha in [(4,55),(10,28),(20,12)]:
        gr = _MOON_R + extra
        for py in range(_CY-gr-PX, _HORIZON+PX, PX):
            for px in range(_CX-gr-PX, _CX+gr+PX, PX):
                d = math.hypot(px-_CX, py-_CY)
                if _MOON_R < d <= gr:
                    p.fillRect(px, py, PX, PX, QColor(200,188,148,alpha))

    # Água base
    for y in range(_HORIZON, _BG_H, PX):
        t = (y-_HORIZON) / max(1, _BG_H-_HORIZON)
        p.fillRect(0, y, _BG_W, PX, QColor(int(10+t*4), int(14+t*6), int(28+t*14)))
    p.fillRect(0, _HORIZON-PX, _BG_W, PX*2, QColor(35, 55, 100, 130))

    # Reflexo estático da lua
    rng2 = random.Random(77)
    for y in range(_HORIZON, _BG_H, PX):
        t  = (y-_HORIZON) / max(1, _BG_H-_HORIZON)
        ww = int(_MOON_R*2*(1+t*1.8))
        wo = int(rng2.uniform(-3, 3)*PX*t*2)
        intensity = max(0.0, 1.0-t*1.1)
        for px in range(_CX-ww//2+wo, _CX+ww//2+wo, PX):
            if not 0 <= px < _BG_W: continue
            fade = max(0.0, 1.0 - abs(px-(_CX+wo)) / max(1, ww//2))
            rv = int(215*intensity*fade)
            gv = int(200*intensity*fade)
            bv = int(148*intensity*fade)
            if rv > 6 or gv > 6:
                p.fillRect(px, y, PX, PX, QColor(rv, gv, bv))

    # Brilho difuso no horizonte
    for y in range(_HORIZON, min(_HORIZON+90, _BG_H), PX):
        t2 = (y-_HORIZON) / 90
        gw = int(_MOON_R*3.5*(1-t2*0.5))
        a  = int(45*(1-t2))
        if a > 0:
            p.fillRect(_CX-gw//2, y, gw, PX, QColor(205, 190, 140, a))

    p.end()
    return pm


# ── Dados para camada animada ─────────────────────────────────────────────────

def _make_star_data() -> list:
    """(x, y, size, phase, speed) — size=-1 indica estrela em cruz."""
    rng = random.Random(42)
    stars = []
    for _ in range(130):
        x     = rng.randint(0, _BG_W-3)
        y     = rng.randint(0, _HORIZON-15)
        sz    = rng.choice([3, 3, 3, 3, 6])
        phase = rng.uniform(0, math.pi * 2)
        speed = rng.uniform(0.6, 2.8)
        stars.append((x, y, sz, phase, speed))
    for _ in range(12):
        x     = rng.randint(6, _BG_W-9)
        y     = rng.randint(6, _HORIZON-24)
        phase = rng.uniform(0, math.pi * 2)
        speed = rng.uniform(0.4, 1.5)
        stars.append((x, y, -1, phase, speed))
    return stars


def _make_sparkle_data() -> list:
    """(x, y, speed, phase) — reflexos cintilantes na água."""
    rng = random.Random(55)
    sparkles = []
    water_h = _BG_H - _HORIZON
    for _ in range(35):
        x     = _CX + rng.randint(-int(_MOON_R*2.5), int(_MOON_R*2.5))
        y     = _HORIZON + rng.randint(int(water_h*0.03), int(water_h*0.97))
        speed = rng.uniform(1.2, 3.5)
        phase = rng.uniform(0, math.pi * 2)
        sparkles.append((x, y, speed, phase))
    return sparkles


# ── Canvas com animação ───────────────────────────────────────────────────────

class _Canvas(QWidget):
    FPS = 24

    def __init__(self, bg: QPixmap, stars: list, sparkles: list, parent=None):
        super().__init__(parent)
        self._bg       = bg
        self._stars    = stars
        self._sparkles = sparkles
        self._tick     = 0.0
        self.setAttribute(Qt.WA_OpaquePaintEvent)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._step)
        self._timer.start(1000 // self.FPS)

    def _step(self):
        self._tick += 1.0 / self.FPS
        self.update()

    def paintEvent(self, _event):
        W, H = self.width(), self.height()
        sx, sy = W / _BG_W, H / _BG_H
        t = self._tick

        p = QPainter(self)

        # Fundo estático escalado
        p.drawPixmap(
            self.rect(),
            self._bg.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation),
        )

        hz = int(_HORIZON * sy)
        cx = int(_CX * sx)
        mr = int(_MOON_R * sx)

        # ── Estrelas piscando ─────────────────────────────────────────
        for (bx, by, bsz, phase, speed) in self._stars:
            bright = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * speed + phase))
            scx = int(bx * sx)
            scy = int(by * sy)

            if bsz == -1:
                a   = max(0, int(240 * bright))
                c   = QColor(255, 252, 210, a)
                psz = max(1, int(3 * sx))
                p.fillRect(scx,       scy - psz, psz,    psz*3, c)
                p.fillRect(scx - psz, scy,       psz*3,  psz,   c)
            else:
                ssz = max(1, round(bsz * sx))
                p.fillRect(scx, scy, ssz, ssz, QColor(255, 252, 220, int(255 * bright)))

        # ── Ondulações da água (linhas subindo) ───────────────────────
        NUM_RIPPLES = 8
        for i in range(NUM_RIPPLES):
            phase    = ((t * 0.22 + i / NUM_RIPPLES) % 1.0)
            ry       = hz + int((H - hz) * phase)
            dist     = phase
            half_w   = int(mr * (1.0 + dist * 2.2))
            wobble   = int(math.sin(t * 0.85 + i * 1.9) * 7 * sx)
            a        = int(55 * math.sin(phase * math.pi))
            if a > 4:
                p.fillRect(cx - half_w + wobble, ry, half_w * 2,
                           max(1, round(2 * sy)), QColor(100, 150, 215, a))

        # ── Brilho animado no reflexo central ─────────────────────────
        for i in range(14):
            phase_r   = ((t * 0.38 + i * 0.072) % 1.0)
            ry        = hz + int((H - hz) * phase_r)
            intensity = max(0.0, 1.0 - phase_r * 1.15)
            shimmer   = 0.45 + 0.55 * math.sin(t * 2.8 + i * 0.65)
            half_w    = int(mr * 0.55 * (1 + phase_r * 0.6))
            wobble    = int(math.sin(t * 0.75 + i * 0.55) * 5 * sx)
            a         = int(50 * intensity * shimmer)
            if a > 4:
                p.fillRect(cx - half_w + wobble, ry, half_w * 2,
                           max(1, round(3 * sy)), QColor(245, 225, 160, a))

        # ── Reflexos cintilantes (glitter) ────────────────────────────
        for (bx, by, spd, phase) in self._sparkles:
            val = math.sin(t * spd + phase)
            if val > 0.25:
                a   = int(130 * (val - 0.25) / 0.75)
                scx = int(bx * sx)
                scy = int(by * sy)
                ssz = max(1, round(2.5 * sx))
                p.fillRect(scx, scy, ssz, ssz, QColor(210, 228, 255, a))

        p.end()


# ── Janela principal ──────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    choice_made = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dilemas Éticos — Arduino & IA")
        self.resize(900, 700)
        self.setMinimumSize(700, 500)
        self._setup_ui()

    def _setup_ui(self):
        bg       = _make_background()
        stars    = _make_star_data()
        sparkles = _make_sparkle_data()

        canvas = _Canvas(bg, stars, sparkles)
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
