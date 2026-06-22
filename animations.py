"""Background animation layers: waves, leaves, sunlight, snow."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

import assets
import game

# ── Background animation state ───────────────────────────────────
_cizgiler: list[dict[str, Any]] = []
_leaf_olay: list[dict[str, Any]] = []
_gunes_glow: list[pygame.Surface] = []
_gunes_glow_r: list[int] = []
_kar_buf: pygame.Surface | None = None


def animasyon_baslat() -> None:
    """Initialize background animation data for the current season."""
    global _cizgiler, _leaf_olay, _gunes_glow, _gunes_glow_r, _kar_buf
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    m = game.mv

    _cizgiler = [
        {"faz": i * 0.7, "gen": 2 + i * 0.5, "hiz": 0.025 + i * 0.005}
        for i in range(3)
    ]

    renk = {
        "ilkbahar": (50, 170, 50), "yaz": (130, 160, 40),
        "sonbahar": (190, 110, 30), "kis": (170, 180, 190),
    }.get(m, (50, 170, 50))

    _leaf_olay = [
        {
            "x": random.uniform(0, z), "y": random.uniform(50, h // 3),
            "s": random.uniform(0.03, 0.06), "faz": random.uniform(0, 6.28),
            "r": renk, "b": random.randint(4, 8),
        }
        for _ in range(5)
    ]

    sr = 18
    _gunes_glow.clear()
    _gunes_glow_r.clear()
    for gi in range(3):
        gr = sr + gi * 10 + 4
        s = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
        _gunes_glow.append(s)
        _gunes_glow_r.append(gr)

    _kar_buf = pygame.Surface((z, h), pygame.SRCALPHA)


def deniz_wave_ciz() -> None:
    """Draw animated water/heat-wave lines at the bottom of the screen."""
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    sz = game.sz
    alt = h - h // 6

    for cizgi in _cizgiler:
        nok: list[tuple[int, int]] = []
        for x in range(0, z + 10, 8):
            y = alt + 8 + math.sin(x * 0.025 + sz * cizgi["hiz"] + cizgi["faz"]) * (
                cizgi["gen"] + math.sin(sz * cizgi["hiz"] * 0.5) * 1
            )
            nok.append((int(x), int(y)))
        a2 = max(0, min(120, 60 + int(math.sin(sz * cizgi["hiz"] + cizgi["faz"]) * 30)))
        for i in range(len(nok) - 1):
            pygame.draw.line(game.ekran, (255, 255, 255, a2), nok[i], nok[i + 1], 1)


def yaprak_hisirtisi_ciz() -> None:
    """Draw floating leaf-like particles that drift across the background."""
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    sz = game.sz
    m = game.mv

    renk = {
        "ilkbahar": (50, 170, 50), "yaz": (130, 160, 40),
        "sonbahar": (190, 110, 30), "kis": (170, 180, 190),
    }.get(m, (50, 170, 50))

    for yp in _leaf_olay:
        yp["r"] = renk
        yp["x"] += math.sin(sz * yp["s"] + yp["faz"]) * 0.3
        yp["y"] += math.sin(sz * yp["s"] * 1.5 + yp["faz"] * 1.3) * 0.15
        if yp["x"] < -30: yp["x"] = z + 30
        if yp["x"] > z + 30: yp["x"] = -30
        if yp["y"] < 20: yp["y"] = h // 3
        if yp["y"] > h // 3: yp["y"] = 50

        for li in range(3):
            xy = yp["x"] + li * yp["b"] * 0.8 + math.sin(sz * 0.025 + yp["faz"] + li) * 2
            yy = yp["y"] + math.sin(sz * 0.02 + yp["faz"] + li * 0.7) * 3
            boy = yp["b"] * 1.2 + math.sin(sz * 0.03 + yp["faz"] + li) * 2
            pygame.draw.ellipse(game.ekran, renk, (xy, yy, boy, yp["b"] * 0.5), 1)


def gunes_isini_ciz() -> None:
    """Draw a pulsing sun with radial glow and light rays."""
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    sz = game.sz
    m = game.mv

    renk = {
        "ilkbahar": (255, 255, 200), "yaz": (255, 230, 100),
        "sonbahar": (255, 200, 150), "kis": (220, 220, 240),
    }.get(m, (255, 255, 200))

    gunes_x = int(z * 0.75 + math.sin(sz * 0.003) * 150)
    gunes_y = int(60 + math.sin(sz * 0.002) * 20)

    # Light rays
    for ri in range(6):
        a = sz * 0.008 + ri * 1.047
        son_x = gunes_x + int(math.cos(a) * (80 + math.sin(sz * 0.01 + ri) * 15))
        son_y = gunes_y + int(math.sin(a) * (50 + math.sin(sz * 0.01 + ri) * 10))
        a2 = max(0, min(60, 30 + int(math.sin(sz * 0.015 + ri) * 20)))
        pygame.draw.line(game.ekran, (*renk, a2), (gunes_x, gunes_y), (son_x, son_y), 2)

    # Glow layers
    for gi in range(3):
        gr = 18 + gi * 10 + int(math.sin(sz * 0.025 + gi) * 3)
        s = _gunes_glow[gi]
        sr = _gunes_glow_r[gi]
        s.fill((0, 0, 0, 0))
        a2 = max(0, 60 - gi * 20)
        pygame.draw.circle(s, (*renk, a2), (sr, sr), gr)
        game.ekran.blit(s, (gunes_x - sr, gunes_y - sr))

    pygame.draw.circle(game.ekran, renk, (gunes_x, gunes_y), 18)
    pygame.draw.circle(game.ekran, (255, 255, 255), (gunes_x - 1, gunes_y - 1), 14)


def kar_ciz() -> None:
    """Draw falling snow overlay via deterministic pseudo-random positions."""
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    sz = game.sz

    global _kar_buf
    if _kar_buf is None:
        return
    _kar_buf.fill((0, 0, 0, 0))
    for ki in range(10):
        kx = int((sz * 17.3 + ki * 137.5) % z)
        ky = int((sz * 23.7 + ki * 89.3 + 50) % h)
        ks = 1 + ki % 2
        kayma = int(math.sin(sz * 0.015 + kx) * ks)
        pygame.draw.circle(_kar_buf, (255, 255, 255, 160), (kx + kayma, ky), ks)
    game.ekran.blit(_kar_buf, (0, 0))


def tum_animasyonlari_ciz() -> None:
    """Draw all background animation layers for the current season."""
    deniz_wave_ciz()
    gunes_isini_ciz()
    yaprak_hisirtisi_ciz()
    if game.mv == "kis":
        kar_ciz()
