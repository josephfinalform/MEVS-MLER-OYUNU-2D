"""Character rendering: body, physics, weapons, costumes."""

from __future__ import annotations

import math
import random
from typing import Optional

import pygame

import assets
import game
import particles

# ── Constants ────────────────────────────────────────────────────
MEME_K = 0.3
MEME_D = 0.6
GOT_K = 0.4
GOT_D = 0.7

CHAR: Optional[pygame.Surface] = None
_onceki_oy: float = 0.0
_onceki_yr: bool = True


def _yukle_char() -> None:
    """Lazy-load wizard overlay sprite."""
    global CHAR
    if CHAR is not None:
        return
    try:
        CHAR = pygame.image.load(str(assets.config.KAYNAK / "char.png")).convert_alpha()
    except Exception:
        CHAR = None


class KrkFizik:
    """Spring-mass-damper physics for breast/buttock jiggle."""

    def __init__(self) -> None:
        self.msx: float = 0.0
        self.msy: float = 0.0
        self.mxv: float = 0.0
        self.myv: float = 0.0
        self.gsx: float = 0.0
        self.gsy: float = 0.0
        self.gv: float = 0.0
        self.sf: float = 0.0
        self.kb: float = 0.0

    def guncelle(self, hizlanma: float) -> None:
        """Step physics simulation for one frame."""
        self.mxv += (hizlanma * 0.3 - self.msx) * 0.05
        self.msx += self.mxv
        self.msx *= 0.9
        self.myv += (-self.msy * MEME_K - self.myv * MEME_D) * 0.1
        self.myv += abs(hizlanma) * 0.02
        self.msy += self.myv

        self.gv += (-self.gsy * GOT_K - self.gv * GOT_D) * 0.1
        self.gv += abs(hizlanma) * 0.03
        self.gsy += self.gv

        self.sf += 0.08
        self.kb = max(0.0, self.kb - 0.05)


fizik = KrkFizik()


def _ciz_kafa(sx: float, sy: float) -> None:
    """Draw character head: face, nose, eyebrows, mouth."""
    ek = game.ekran
    # Head shape
    pygame.draw.ellipse(ek, assets.TEN, (sx - 13, sy - 46, 26, 36))
    pygame.draw.ellipse(ek, (245, 210, 195), (sx - 12, sy - 40, 12, 16))
    pygame.draw.ellipse(ek, (245, 210, 195), (sx + 1, sy - 40, 12, 16))
    # Eyelashes
    pygame.draw.line(ek, (240, 195, 180), (sx - 9, sy - 28), (sx - 4, sy - 30), 1)
    pygame.draw.line(ek, (240, 195, 180), (sx + 4, sy - 30), (sx + 9, sy - 28), 1)
    pygame.draw.arc(ek, (230, 190, 175), (sx - 11, sy - 18, 22, 12), 0.1, 3.0, 1)

    # Nose
    pygame.draw.line(ek, (225, 185, 165), (sx, sy - 24), (sx, sy - 19), 1)
    pygame.draw.circle(ek, (220, 180, 160), (sx, sy - 19), 1)
    pygame.draw.line(ek, (230, 190, 170), (sx - 1, sy - 22), (sx - 3, sy - 21), 1)
    pygame.draw.line(ek, (230, 190, 170), (sx + 1, sy - 22), (sx + 3, sy - 21), 1)

    # Eyebrows
    pygame.draw.line(ek, (180, 120, 140), (sx - 10, sy - 43), (sx - 2, sy - 44), 2)
    pygame.draw.line(ek, (180, 120, 140), (sx + 2, sy - 44), (sx + 10, sy - 43), 2)

    # Mouth
    if game.yr and abs(game.hx) < 0.5:
        pygame.draw.arc(ek, (220, 170, 160), (sx - 5, sy - 24, 10, 7), 0.1, 3.0, 2)
    else:
        pygame.draw.arc(ek, (210, 160, 150), (sx - 4, sy - 22, 8, 5), 0, 3.14, 2)
        pygame.draw.line(ek, (190, 140, 130), (sx - 5, sy - 23), (sx + 5, sy - 23), 2)
        pygame.draw.line(ek, (180, 130, 120), (sx, sy - 22), (sx, sy - 21), 1)
    pygame.draw.line(ek, (230, 190, 180), (sx - 2, sy - 20), (sx + 2, sy - 20), 1)


def _ciz_gozler(sx: float, sy: float) -> None:
    """Draw eyes with iris, blink animation, and highlights."""
    ek = game.ekran
    ga = game.gk % 180 > 5
    if not ga:
        pygame.draw.line(ek, (40, 40, 40), (sx - 10, sy - 35), (sx - 1, sy - 35), 2)
        pygame.draw.line(ek, (40, 40, 40), (sx + 1, sy - 35), (sx + 10, sy - 35), 2)
        return

    pygame.draw.ellipse(ek, assets.B, (sx - 11, sy - 39, 11, 9))
    pygame.draw.ellipse(ek, assets.B, (sx + 1, sy - 39, 11, 9))
    pygame.draw.ellipse(ek, (250, 250, 255), (sx - 10, sy - 38, 9, 7))
    pygame.draw.ellipse(ek, (250, 250, 255), (sx + 2, sy - 38, 9, 7))

    # Iris
    for off in [-5, 5]:
        cx = sx + off
        cy = sy - 35
        pygame.draw.circle(ek, (255, 220, 50), (cx, cy), 5)
        pygame.draw.circle(ek, (255, 160, 30), (cx, cy), 5, 1)
        for i in range(4):
            a_s = i * 1.57
            pygame.draw.line(ek, (255, 180, 40),
                             (cx + int(math.cos(a_s) * 3), cy + int(math.sin(a_s) * 3)),
                             (cx + int(math.cos(a_s) * 4), cy + int(math.sin(a_s) * 4)), 1)
        pygame.draw.circle(ek, assets.S, (cx, cy), 2)
        pygame.draw.circle(ek, (255, 255, 255), (cx - 2, cy - 2), 1)

    # Lashes
    for i, kx in enumerate([-11, -9, 9, 11]):
        kys = -39 if i < 2 else -39
        ky2 = -42 + i * 0.5 if i < 2 else -42 + (i - 2) * 0.5
        pygame.draw.line(ek, (30, 30, 30), (sx + kx, sy + kys), (sx + kx - 1 + i * 0.5, sy + ky2), 1)
    for kx in [-8, -4, 4, 8]:
        pygame.draw.line(ek, (60, 60, 60), (sx + kx, sy - 31), (sx + kx - 0.5, sy - 29), 1)


def _ciz_govde(sx: float, sy: float) -> None:
    """Draw torso, neck, belt, and shirt details."""
    ek = game.ekran
    # Neck
    pygame.draw.rect(ek, assets.TEN, (sx - 4, sy - 14, 8, 6))
    pygame.draw.line(ek, (220, 180, 165), (sx - 3, sy - 14), (sx - 3, sy - 9), 1)
    pygame.draw.line(ek, (220, 180, 165), (sx + 3, sy - 14), (sx + 3, sy - 9), 1)
    pygame.draw.line(ek, (215, 175, 160), (sx - 6, sy - 8), (sx + 6, sy - 8), 1)

    # Torso
    pygame.draw.rect(ek, (240, 235, 225), (sx - 13, sy - 10, 26, 28), border_radius=2)
    for i in range(3):
        yy = sy - 6 + i * 8
        pygame.draw.line(ek, (235, 230, 220), (sx - 10, yy), (sx + 10, yy), 1)
    pygame.draw.rect(ek, (215, 210, 200), (sx - 13, sy - 10, 26, 28), 1, border_radius=2)

    # Collar
    pygame.draw.polygon(ek, (230, 225, 215), [(sx - 5, sy - 10), (sx - 9, sy - 3), (sx, sy - 4)])
    pygame.draw.polygon(ek, (230, 225, 215), [(sx + 5, sy - 10), (sx + 9, sy - 3), (sx, sy - 4)])
    pygame.draw.polygon(ek, (220, 215, 205), [(sx - 5, sy - 10), (sx - 9, sy - 3), (sx, sy - 4)], 1)
    pygame.draw.polygon(ek, (220, 215, 205), [(sx + 5, sy - 10), (sx + 9, sy - 3), (sx, sy - 4)], 1)

    # Belt
    pygame.draw.polygon(ek, (15, 15, 15), [(sx - 2, sy - 4), (sx + 2, sy - 4), (sx + 1, sy + 6), (sx, sy + 10), (sx - 1, sy + 6)])
    pygame.draw.polygon(ek, (30, 30, 30), [(sx - 2, sy - 4), (sx + 2, sy - 4), (sx + 1, sy + 6), (sx, sy + 10), (sx - 1, sy + 6)], 1)
    pygame.draw.line(ek, (40, 40, 40), (sx, sy - 3), (sx, sy + 4), 1)
    pygame.draw.circle(ek, (200, 200, 200), (sx, sy + 2), 1)

    # Buttons
    for i in range(4):
        yy = sy - 4 + i * 6
        pygame.draw.circle(ek, (210, 205, 195), (sx, yy), 1)
        pygame.draw.circle(ek, (225, 220, 210), (sx - 1, yy - 1), 1)

    # Sides
    pygame.draw.line(ek, (230, 225, 215), (sx - 12, sy + 6), (sx - 16, sy + 12), 1)
    pygame.draw.line(ek, (230, 225, 215), (sx + 12, sy + 6), (sx + 16, sy + 12), 1)


def _ciz_memeler(sx: float, sy: float) -> None:
    """Draw breast physics."""
    ek = game.ekran
    mx_l = sx - 9 + fizik.msx
    my_l = sy - 4 + abs(fizik.msy) * 2
    mx_r = sx + 9 + fizik.msx
    my_r = sy - 4 + abs(fizik.msy) * 2
    renk = (240, 235, 225)
    for cx, cy in [(mx_l, my_l), (mx_r, my_r)]:
        pygame.draw.ellipse(ek, renk, (cx - 5, cy - 4, 10, 12))
        pygame.draw.ellipse(ek, (250, 245, 235), (cx - 4, cy - 3, 8, 10))
        pygame.draw.ellipse(ek, (230, 225, 215), (cx - 3, cy - 1, 6, 8))


def _ciz_pacalar(sx: float, sy: float, yon: int, iv: pygame.Vector2) -> None:
    """Draw legs with walking animation."""
    ek = game.ekran

    if not game.yr:
        ba = 0.0
        syk = -6.0
        sagk = -6.0
    elif abs(game.hx) > 1:
        ba = math.sin(game.sz * 8) * 30 * yon
        syk = abs(math.sin(game.sz * 8)) * 6
        sagk = abs(math.cos(game.sz * 8)) * 6
    else:
        ba = iv.x * 3
        syk = iv.x * 0.5
        sagk = -iv.x * 0.5

    sol_x = sx - 9 + ba * 0.08
    sag_x = sx + 2 - ba * 0.08

    # Legs
    pygame.draw.rect(ek, (15, 15, 22), (sol_x, sy + 22 + syk, 9, 16))
    pygame.draw.rect(ek, (15, 15, 22), (sag_x, sy + 22 + sagk, 9, 16))
    for x_off, y_off in [(sol_x, syk), (sag_x, sagk)]:
        pygame.draw.line(ek, (25, 25, 32), (x_off + 4, sy + 24 + y_off), (x_off + 4, sy + 36 + y_off), 1)
        pygame.draw.line(ek, (20, 20, 28), (x_off + 1, sy + 26 + y_off), (x_off + 7, sy + 28 + y_off), 1)
        pygame.draw.line(ek, (30, 30, 38), (x_off, sy + 22 + y_off), (x_off, sy + 38 + y_off), 1)

    # Buttocks
    got_y = sy + 20 + abs(fizik.gsy) * 3
    for x_off in [sol_x, sag_x]:
        pygame.draw.ellipse(ek, (20, 20, 30), (x_off - 2, got_y - 3, 12, 10))
        pygame.draw.ellipse(ek, (30, 30, 40), (x_off - 1, got_y - 2, 10, 8))

    # Shoes
    for x_off, y_off in [(sol_x, syk), (sag_x, sagk)]:
        pygame.draw.ellipse(ek, (100, 60, 35), (x_off - 4, sy + 36 + y_off, 14, 8))
        pygame.draw.ellipse(ek, (120, 75, 45), (x_off - 3, sy + 37 + y_off, 12, 6))
        pygame.draw.rect(ek, (60, 35, 20), (x_off - 4, sy + 42 + y_off, 14, 3))
        pygame.draw.line(ek, (50, 25, 15), (x_off - 2, sy + 43 + y_off), (x_off + 8, sy + 43 + y_off), 1)
        for si in range(3):
            pygame.draw.circle(ek, (50, 30, 15), (x_off + si * 3 - 1, sy + 38 + y_off), 1)
        pygame.draw.line(ek, (50, 30, 15), (x_off + 1, sy + 37 + y_off), (x_off + 4, sy + 40 + y_off), 1)
        pygame.draw.line(ek, (140, 90, 55), (x_off - 1, sy + 38 + y_off), (x_off + 5, sy + 38 + y_off), 1)


def _ciz_kollar(sx: float, sy: float, yon: int) -> None:
    """Draw arms and weapon."""
    ek = game.ekran
    wd_cd = assets.WP_DATA[game.mv].cooldown if game.weapon else 10
    geri_tepme = (wd_cd - game.shoot_cd) / wd_cd if game.shoot_cd > 0 else 0
    geri_tepme = max(0.0, min(1.0, geri_tepme))
    kol_sag = math.sin(game.sz * 6) * 3 if abs(game.hx) > 1 else 0
    kol_sag += geri_tepme * 8 * yon

    if game.weapon:
        # Upper arms
        pygame.draw.line(ek, (240, 235, 225), (sx - 15, sy - 8), (sx - 28 + kol_sag, sy + 2), 5)
        pygame.draw.line(ek, (240, 235, 225), (sx + 15, sy - 8), (sx + 26 - kol_sag, sy + 2), 5)
        pygame.draw.line(ek, (225, 220, 210), (sx - 15, sy - 7), (sx - 27 + kol_sag, sy + 3), 1)
        pygame.draw.line(ek, (225, 220, 210), (sx + 15, sy - 7), (sx + 25 - kol_sag, sy + 3), 1)
        pygame.draw.line(ek, (220, 215, 205), (sx - 27 + kol_sag, sy), (sx - 27 + kol_sag, sy + 4), 2)
        pygame.draw.line(ek, (220, 215, 205), (sx + 25 - kol_sag, sy), (sx + 25 - kol_sag, sy + 4), 2)

        _ciz_silah(sx, sy, yon)
    else:
        pygame.draw.line(ek, (240, 235, 225), (sx - 15, sy - 8), (sx - 22 + kol_sag, sy + 6), 5)
        pygame.draw.line(ek, (240, 235, 225), (sx + 15, sy - 8), (sx + 22 - kol_sag, sy + 6), 5)
        pygame.draw.line(ek, (225, 220, 210), (sx - 15, sy - 7), (sx - 21 + kol_sag, sy + 7), 1)
        pygame.draw.line(ek, (225, 220, 210), (sx + 15, sy - 7), (sx + 21 - kol_sag, sy + 7), 1)
        pygame.draw.line(ek, (220, 215, 205), (sx - 21 + kol_sag, sy + 4), (sx - 21 + kol_sag, sy + 8), 2)
        pygame.draw.line(ek, (220, 215, 205), (sx + 21 - kol_sag, sy + 4), (sx + 21 - kol_sag, sy + 8), 2)


def _ciz_silah(sx: float, sy: float, yon: int) -> None:
    """Draw biome-themed weapon sprite."""
    ek = game.ekran
    m = game.mv
    w_yon = 1 if yon >= 0 else -1
    w_x = sx + (22 if yon >= 0 else -22)
    w_y = sy - 2
    c = assets.WP_DATA[m].color

    if m == "ilkbahar":
        # Body
        pygame.draw.rect(ek, (60, 80, 60), (w_x, w_y - 3, 30 * w_yon, 6))
        pygame.draw.rect(ek, (80, 110, 80), (w_x, w_y - 3, 30 * w_yon, 6), 1)
        pygame.draw.rect(ek, (100, 140, 100), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
        # Muzzle
        pygame.draw.circle(ek, (255, 220, 180), (w_x + 31 * w_yon, w_y), 4)
        pygame.draw.circle(ek, (255, 200, 50), (w_x + 31 * w_yon, w_y), 2)
        # Grip
        pygame.draw.rect(ek, (50, 70, 50), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
        pygame.draw.rect(ek, (70, 90, 70), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
        mag_x = w_x + 2 * w_yon
        pygame.draw.polygon(ek, (70, 50, 30), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
        pygame.draw.polygon(ek, (90, 70, 50), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
        pygame.draw.polygon(ek, (50, 80, 50), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
        pygame.draw.rect(ek, (50, 70, 40), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
        pygame.draw.rect(ek, (70, 90, 60), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
        # Flowers
        for ci in range(3):
            cx = int(w_x + (ci * 10 - 5) * w_yon)
            cy = int(w_y - 6 + ci * 6)
            pygame.draw.circle(ek, (255, 220, 200), (cx, cy), 3)
            pygame.draw.circle(ek, (255, 200, 50), (cx, cy), 1)
        # Vines
        for vi in range(4):
            vx = int(w_x + vi * 7 * w_yon)
            pygame.draw.line(ek, (60, 140, 60), (vx, w_y - 4), (vx - 2 * w_yon, w_y + 6 + vi * 2), 1)

    elif m == "yaz":
        pygame.draw.rect(ek, (200, 140, 20), (w_x, w_y - 4, 30 * w_yon, 8))
        pygame.draw.rect(ek, (255, 200, 50), (w_x, w_y - 4, 30 * w_yon, 8), 1)
        pygame.draw.line(ek, (255, 255, 100), (w_x, w_y), (w_x + 28 * w_yon, w_y), 2)
        pygame.draw.rect(ek, (255, 180, 50), (w_x + 26 * w_yon, w_y - 5, 8 * w_yon, 10))
        pygame.draw.circle(ek, (255, 255, 200), (w_x + 32 * w_yon, w_y), 5)
        pygame.draw.circle(ek, (255, 255, 255), (w_x + 32 * w_yon, w_y), 2)
        pygame.draw.rect(ek, (180, 120, 30), (w_x - 4 * w_yon, w_y - 6, 14 * w_yon, 12))
        pygame.draw.rect(ek, (220, 160, 40), (w_x - 4 * w_yon, w_y - 6, 14 * w_yon, 12), 1)
        mag_x = w_x + 3 * w_yon
        pygame.draw.polygon(ek, (160, 100, 20), [(mag_x, w_y + 6), (mag_x + 6 * w_yon, w_y + 6), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
        pygame.draw.polygon(ek, (200, 140, 40), [(mag_x, w_y + 6), (mag_x + 6 * w_yon, w_y + 6), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
        pygame.draw.polygon(ek, (140, 80, 20), [(w_x + 6 * w_yon, w_y + 6), (w_x + 10 * w_yon, w_y + 6), (w_x + 8 * w_yon, w_y + 16)])
        pygame.draw.rect(ek, (130, 80, 20), (w_x - 10 * w_yon, w_y - 6, 8 * w_yon, 12))
        pygame.draw.rect(ek, (170, 110, 30), (w_x - 10 * w_yon, w_y - 6, 8 * w_yon, 12), 1)
        for ri in range(5):
            rx = int(w_x + ri * 6 * w_yon)
            pygame.draw.line(ek, (255, 220, 50), (rx, w_y - 8), (rx, w_y - 12 - ri % 2 * 3), 1)
            pygame.draw.line(ek, (255, 220, 50), (rx, w_y + 8), (rx, w_y + 12 + ri % 2 * 3), 1)

    elif m == "sonbahar":
        pygame.draw.rect(ek, (100, 60, 30), (w_x, w_y - 3, 30 * w_yon, 6))
        pygame.draw.rect(ek, (130, 80, 40), (w_x, w_y - 3, 30 * w_yon, 6), 1)
        pygame.draw.rect(ek, (80, 50, 20), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
        pygame.draw.polygon(ek, (200, 80, 30), [(w_x + 30 * w_yon, w_y), (w_x + 28 * w_yon, w_y - 5), (w_x + 28 * w_yon, w_y + 5)])
        pygame.draw.rect(ek, (80, 50, 30), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
        pygame.draw.rect(ek, (110, 70, 40), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
        mag_x = w_x + 2 * w_yon
        pygame.draw.polygon(ek, (120, 60, 20), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
        pygame.draw.polygon(ek, (150, 80, 30), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
        pygame.draw.polygon(ek, (80, 40, 20), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
        pygame.draw.rect(ek, (70, 40, 20), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
        pygame.draw.rect(ek, (100, 60, 30), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
        for li in range(4):
            lx = int(w_x + li * 7 * w_yon)
            ly = int(w_y - 5 + li * 3)
            pygame.draw.ellipse(ek, (200, 100, 30), (lx, ly, 5 * w_yon, 3))
            pygame.draw.ellipse(ek, (255, 150, 50), (lx + 1, ly + 1, 3 * w_yon, 1))
        for bi in range(3):
            bx = int(w_x + bi * 8 * w_yon)
            pygame.draw.line(ek, (60, 40, 20), (bx, w_y - 4), (bx + 2 * w_yon, w_y - 10 + bi * 2), 1)

    elif m == "kis":
        pygame.draw.rect(ek, (150, 200, 230), (w_x, w_y - 3, 30 * w_yon, 6))
        pygame.draw.rect(ek, (200, 230, 255), (w_x, w_y - 3, 30 * w_yon, 6), 1)
        pygame.draw.rect(ek, (180, 220, 240), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
        pygame.draw.circle(ek, (200, 240, 255), (w_x + 31 * w_yon, w_y), 4)
        pygame.draw.circle(ek, (255, 255, 255), (w_x + 31 * w_yon, w_y), 2)
        pygame.draw.rect(ek, (130, 180, 210), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
        pygame.draw.rect(ek, (170, 210, 235), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
        mag_x = w_x + 2 * w_yon
        pygame.draw.polygon(ek, (140, 190, 220), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
        pygame.draw.polygon(ek, (180, 220, 245), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
        pygame.draw.polygon(ek, (120, 170, 200), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
        pygame.draw.rect(ek, (110, 160, 190), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
        pygame.draw.rect(ek, (150, 200, 230), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
        for si in range(4):
            sx2 = int(w_x + (si * 7 + 2) * w_yon)
            sy2 = int(w_y - 6 + si * 4)
            pygame.draw.line(ek, (220, 240, 255), (sx2 - 3, sy2), (sx2 + 3, sy2), 1)
            pygame.draw.line(ek, (220, 240, 255), (sx2, sy2 - 3), (sx2, sy2 + 3), 1)
        for bi in range(3):
            bxi = int(w_x + bi * 9 * w_yon)
            byi = int(w_y + 10 + bi * 3)
            pygame.draw.circle(ek, (200, 235, 255), (bxi, byi), 2)
            pygame.draw.circle(ek, (255, 255, 255), (bxi, byi), 1)

    # Muzzle flash
    wd_cd = assets.WP_DATA[m].cooldown
    if game.shoot_cd > wd_cd - 3:
        flash_r = c if m != "kis" else (200, 230, 255)
        pygame.draw.circle(ek, flash_r, (int(w_x + 32 * w_yon), int(w_y)), 6)
        pygame.draw.circle(ek, (255, 255, 255), (int(w_x + 32 * w_yon), int(w_y)), 3)


def _ciz_kostum(sx: float, sy: float) -> None:
    """Draw equipped costume overlay."""
    ek = game.ekran
    ak = game.aktif_k
    if ak == "sonbahar":
        pygame.draw.polygon(ek, assets.YP, [(sx - 16, sy - 6), (sx - 22, sy + 20), (sx - 8, sy + 18)])
        pygame.draw.polygon(ek, assets.YP, [(sx + 16, sy - 6), (sx + 22, sy + 20), (sx + 8, sy + 18)])
        pygame.draw.line(ek, (150, 80, 20), (sx - 15, sy - 4), (sx - 15, sy + 14), 1)
        pygame.draw.line(ek, (150, 80, 20), (sx + 15, sy - 4), (sx + 15, sy + 14), 1)
    elif ak == "ilkbahar":
        for i in range(5):
            a = sx - 12 + i * 6
            pygame.draw.circle(ek, assets.C1, (a, sy - 54), 5)
            pygame.draw.circle(ek, assets.C2, (a, sy - 54), 3)
            pygame.draw.circle(ek, (255, 200, 50), (a, sy - 54), 1)
    elif ak == "kis":
        for i in range(5):
            a = sx - 12 + i * 6
            pygame.draw.circle(ek, assets.KR, (a, sy - 56), 6)
            pygame.draw.circle(ek, assets.B, (a, sy - 56), 4)
            pygame.draw.circle(ek, (200, 230, 255), (a - 1, sy - 57), 2)
    elif ak == "yaz":
        pygame.draw.circle(ek, assets.ALTIN, (sx - 9, sy - 36), 8, 2)
        pygame.draw.circle(ek, assets.ALTIN, (sx + 9, sy - 36), 8, 2)
        pygame.draw.line(ek, assets.ALTIN, (sx - 1, sy - 36), (sx + 1, sy - 36), 2)
        for i in range(6):
            a = math.radians(i * 60)
            dx = int(math.cos(a) * 9)
            dy = int(math.sin(a) * 9)
            dx2 = int(math.cos(a) * 14)
            dy2 = int(math.sin(a) * 14)
            pygame.draw.line(ek, assets.ALTIN, (sx + dx, sy - 36 + dy), (sx + dx2, sy - 36 + dy2), 1)


def ciz_krk(x: float, y: float, yn: int, yy: float = 0.0) -> None:
    """Draw the full player character at (x, y) facing yn.

    Args:
        x: World X position.
        y: World Y position.
        yn: Facing direction (positive = right).
        yy: Vertical offset (for bounce/damage shake).
    """
    global _onceki_oy, _onceki_yr

    game.sz += 0.05
    game.gk += 1
    y += yy
    game.sh += (game.hx * 0.3 - game.sh) * 0.15
    iv = pygame.Vector2(math.sin(game.sz) * 2, math.sin(game.sz * 0.6) * 0.8)

    hizlanma = game.hx * 0.1
    fizik.guncelle(hizlanma)

    yon = 1 if yn >= 0 else -1
    sx = x
    sy = y

    # Draw character layers back-to-front
    _ciz_kafa(sx, sy)
    _ciz_gozler(sx, sy)
    _ciz_govde(sx, sy)

    # Belt / waist
    pygame.draw.rect(game.ekran, (240, 235, 225), (sx - 13, sy + 14, 26, 6))
    pygame.draw.rect(game.ekran, (15, 15, 20), (sx - 11, sy + 18, 22, 5))
    pygame.draw.rect(game.ekran, (25, 25, 30), (sx - 11, sy + 18, 22, 5), 1)
    pygame.draw.rect(game.ekran, (180, 180, 180), (sx - 2, sy + 19, 4, 3))
    pygame.draw.rect(game.ekran, (200, 200, 200), (sx - 1, sy + 20, 2, 1))

    _ciz_memeler(sx, sy)
    _ciz_pacalar(sx, sy, yon, iv)
    _ciz_kollar(sx, sy, yon)

    # Wizard sprite overlay
    _yukle_char()
    if CHAR:
        sprite = CHAR
        if yon < 0:
            sprite = pygame.transform.flip(CHAR, True, False)
        game.ekran.blit(sprite, (sx - sprite.get_width() // 2, sy + 25 - sprite.get_height()))

    # Breathing particles
    if abs(game.hx) < 0.5 and game.yr and random.random() < 0.04:
        px = sx + random.randint(-18, 18)
        py = sy + 10 + random.randint(-20, 5)
        renk = random.choice([(100, 150, 255), (150, 200, 255), (200, 230, 255)])
        particles.ptk_ekle(px, py, renk, 1)

    # Running dust
    if game.yr and abs(game.hx) > 1.5 and random.random() < 0.12:
        particles.ptk_ekle(sx + random.randint(-6, 6), sy + 22, (180, 180, 200), 2)

    # Landing dust
    if not _onceki_yr and game.yr:
        for _ in range(5):
            particles.ptk_ekle(sx + random.randint(-10, 10), sy + 22, (180, 200, 255), 2)
        particles.ptk_patlatma(sx, sy + 22, (180, 200, 255), 6, 3)

    # Air trail
    if not game.yr and random.random() < 0.06:
        particles.ptk_ekle(sx + random.randint(-8, 8), sy + random.randint(-5, 15), (150, 200, 255), 1)

    _onceki_oy = game.oy
    _onceki_yr = game.yr

    _ciz_kostum(sx, sy)
