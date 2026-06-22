"""Weather effects, background particles, and dust/explosion particle system."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

import assets
import game

# ── Stars (menu background) ───────────────────────────────────────
_yildizlar: list[dict[str, Any]] = [
    {
        "x": random.randint(0, assets.GENISLIK),
        "y": random.randint(0, assets.YUKSEKLIK),
        "h": random.uniform(0.1, 0.3),
        "b": random.randint(1, 2),
    }
    for _ in range(25)
]

# ── Background weather particles ─────────────────────────────────
_bg_par: list[dict[str, Any]] = []

# ── SRCALPHA buffer for all transparent weather effects ──────────
_hava_buf: pygame.Surface | None = None


def bg_par_baslat() -> None:
    """Initialize background weather particles for the current season."""
    global _bg_par, _hava_buf
    _bg_par.clear()
    m = game.mv
    z, h = assets.GENISLIK, assets.YUKSEKLIK

    for _ in range(40):
        x = random.randint(0, z)
        y = random.randint(-50, h)
        if m == "kis":
            _bg_par.append({"x": x, "y": y, "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(0.5, 2), "b": random.randint(1, 3)})
        elif m == "sonbahar":
            _bg_par.append({"x": x, "y": y, "vx": random.uniform(-1, -0.2), "vy": random.uniform(0.3, 1.5), "b": random.randint(2, 4)})
        elif m == "yaz":
            _bg_par.append({"x": x, "y": y, "vx": random.uniform(-2, 2), "vy": random.uniform(0.2, 0.8), "b": random.randint(1, 2)})
        else:
            _bg_par.append({"x": x, "y": y, "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(0.1, 0.5), "b": random.randint(2, 4)})

    _hava_buf = pygame.Surface((z, h), pygame.SRCALPHA)


def ptk_ekle(x: float, y: float, r: tuple[int, int, int], s: int = 8) -> None:
    """Spawn s dust/spark particles at (x, y) with color r, random scatter."""
    for _ in range(s):
        a = random.uniform(0, math.pi * 2)
        h = random.uniform(1, 3)
        game.ptk.append({"x": x, "y": y, "vx": math.cos(a) * h, "vy": math.sin(a) * h - 2, "r": r, "o": random.randint(15, 25), "b": random.randint(2, 4)})


def ptk_patlatma(x: float, y: float, r: tuple[int, int, int], s: int = 20, g: int = 5) -> None:
    """Spawn s explosive particles at (x, y) with color r, speed up to g."""
    for _ in range(s):
        a = random.uniform(0, math.pi * 2)
        h = random.uniform(1, g)
        game.ptk.append({"x": x, "y": y, "vx": math.cos(a) * h, "vy": math.sin(a) * h, "r": r, "o": random.randint(20, 35), "b": random.randint(2, 6)})


def ptk_birim(x: float, y: float, r: tuple[int, int, int]) -> None:
    """Spawn a single rising particle at (x, y)."""
    game.ptk.append({"x": x, "y": y, "vx": random.uniform(-0.5, 0.5), "vy": -1, "r": r, "o": 20, "b": 3})


def ptk_guncelle() -> None:
    """Advance all particles: move, apply gravity, remove expired."""
    for p in game.ptk[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.1
        p["o"] -= 1
        if p["o"] <= 0:
            game.ptk.remove(p)


def ptk_ciz() -> None:
    """Draw all active particles."""
    for p in game.ptk:
        pygame.draw.circle(game.ekran, p["r"], (int(p["x"]), int(p["y"])), p["b"])


def hava_ciz() -> None:
    """Draw season weather effects (rain/snow/leaves/dust) on a SRCALPHA buffer."""
    global _hava_buf
    m = game.mv
    rnk = game.rnk
    z, h = assets.GENISLIK, assets.YUKSEKLIK
    sz = game.sz

    # Remove expired effects, spawn new ones up to 30
    game.hava_efektleri = [he for he in game.hava_efektleri if he["o"] > 0]
    while len(game.hava_efektleri) < 30:
        x2 = random.randint(0, z)
        y2 = random.randint(-20, -5)
        if m == "kis":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(0.5, 2), "b": random.randint(1, 3), "o": random.randint(60, 120), "r": assets.KR})
        elif m == "sonbahar":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-1.5, -0.3), "vy": random.uniform(0.3, 1.2), "b": random.randint(2, 4), "o": random.randint(80, 150), "r": assets.YP})
        elif m == "yaz":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-3, 3), "vy": random.uniform(0.2, 0.8), "b": random.randint(1, 2), "o": random.randint(40, 80), "r": assets.ALTIN})
        else:
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(0.3, 1), "b": random.randint(2, 4), "o": random.randint(80, 150), "r": (150, 200, 255)})

    # Clear buffer
    if _hava_buf is None:
        return
    _hava_buf.fill((0, 0, 0, 0))

    # Draw weather effects onto buffer
    for he in game.hava_efektleri:
        he["x"] += he["vx"]
        he["y"] += he["vy"]
        he["o"] -= 1
        a2 = min(200, he["o"] * 3)
        if m == "kis":
            pygame.draw.circle(_hava_buf, (255, 255, 255, a2), (int(he["x"]), int(he["y"])), he["b"])
        elif m == "sonbahar":
            d2 = he["x"] * 0.5 + he["y"] * 0.3
            lx = int(he["x"] - 4 + math.sin(d2) * 2)
            ly = int(he["y"] - 2)
            pygame.draw.ellipse(_hava_buf, (200, 150, 50, a2), (lx, ly, 8, 5))
            pygame.draw.line(_hava_buf, (150, 80, 20, a2), (lx + 1, ly + 2), (lx + 7, ly + 2), 1)
        elif m == "yaz":
            pygame.draw.circle(_hava_buf, (255, 215, 0, a2), (int(he["x"]), int(he["y"])), he["b"])
        else:
            pygame.draw.circle(_hava_buf, (100, 200, 255, a2), (int(he["x"]), int(he["y"])), he["b"])

    # Season-specific extras (fireflies, mist)
    if m == "yaz":
        for fi in range(3):
            fix = int((sz * 5.7 + fi * 311.7) % z)
            fiy = int(200 + (sz * 3.1 + fi * 179.3) % (h - 300) + math.sin(sz * 0.03 + fi) * 8)
            fb_i = 80 + int(math.sin(sz * 0.05 + fi) * 60)
            a2 = max(0, min(255, fb_i))
            pygame.draw.circle(_hava_buf, (200, 255, 100, a2), (fix, fiy), 4)
            pygame.draw.circle(_hava_buf, (255, 255, 200, a2 // 2), (fix, fiy), 5)

    if m == "sonbahar" and int(sz * 10 + 50) % 40 < 2:
        sis_x = int((sz * 0.3 + 100) % z)
        sis_y = int(h - 60 + math.sin(sz * 0.01) * 20)
        pygame.draw.ellipse(_hava_buf, (180, 160, 140, 15), (sis_x, sis_y, 40, 20))

    # Blit weather buffer
    game.ekran.blit(_hava_buf, (0, 0))

    # Vertical gradient lines
    for i in range(0, z, 100):
        pygame.draw.line(game.ekran, rnk["ac"], (i, 0), (i, h), 1)

    # Seasonal ambient effects
    if m == "ilkbahar":
        for bi in range(2):
            kx = int((sz * 0.5 + bi * 400) % z)
            ky = int(100 + bi * 150 + math.sin(sz * 0.02 + bi * 2) * 30)
            kanat_c = int(math.sin(sz * 0.1 + bi * 3) * 3)
            pygame.draw.ellipse(game.ekran, (255, 150, 200), (kx - 6 - kanat_c, ky - 2, 6, 4))
            pygame.draw.ellipse(game.ekran, (255, 200, 220), (kx + kanat_c, ky - 2, 6, 4))
            pygame.draw.line(game.ekran, (50, 50, 50), (kx, ky), (kx, ky + 4), 1)

    # Legacy decoration (from level data)
    d = game.lvl.get("d", "")
    if d == "cicek":
        for ci in range(15):
            cx = int((ci * 73 + 50) % z)
            cy = int((ci * 97 + 30) % (h - 100))
            pygame.draw.circle(game.ekran, assets.C1, (cx, cy), 3)
            pygame.draw.circle(game.ekran, assets.C2, (cx - 1, cy - 1), 1)
    if d == "kar":
        for ki in range(20):
            kx = int((ki * 53 + 20) % z)
            ky = int((ki * 67 + 40) % h)
            pygame.draw.circle(game.ekran, assets.KR, (kx, ky), 2)
