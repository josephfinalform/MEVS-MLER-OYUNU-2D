"""Character rendering: animated armored character from char.png + wizard fallback."""

from __future__ import annotations

import math
import random
from typing import Optional
from pathlib import Path

import pygame

import assets
import game
import particles

# ── Physics constants ────────────────────────────────────────────
AYAK_K = 0.35
AYAK_D = 0.55

_onceki_oy: float = 0.0
_onceki_yr: bool = True

# ── Character sprite parts (extracted from char.png) ─────────────
_body_surf: Optional[pygame.Surface] = None
_body_surf_f: Optional[pygame.Surface] = None
_left_leg_surf: Optional[pygame.Surface] = None
_left_leg_surf_f: Optional[pygame.Surface] = None
_right_leg_surf: Optional[pygame.Surface] = None
_right_leg_surf_f: Optional[pygame.Surface] = None
_leg_composite: Optional[pygame.Surface] = None
_shadow_surf: Optional[pygame.Surface] = None
_leg_h: int = 18

# ── Animation state ──────────────────────────────────────────────
_anim_time: float = 0.0
_walk_frame: int = 0
_gesture_timer: int = 0
_gesture_type: int = 0  # 0=none, 1=wave, 2=point, 3=both_up
_blink_timer: int = 0


class AyakFizik:
    """Spring-mass-damper physics for foot jiggle and landing impact."""

    def __init__(self) -> None:
        self.sol_y: float = 0.0
        self.sol_vy: float = 0.0
        self.sag_y: float = 0.0
        self.sag_vy: float = 0.0
        self.sol_x: float = 0.0
        self.sol_vx: float = 0.0
        self.sag_x: float = 0.0
        self.sag_vx: float = 0.0
        self.yer: bool = True
        self.dusme_hizi: float = 0.0
        self.basma_mesafesi: float = 0.0

    def guncelle(self, ivme: float, ziplama: bool, yr: bool) -> None:
        self.yer = yr
        hedef_y = 0.0 if yr else 4.0

        if not yr:
            self.sol_vy += (hedef_y - self.sol_y) * 0.08
            self.sol_vy += abs(ivme) * 0.01
            self.sol_y += self.sol_vy
            self.sag_vy += (hedef_y - self.sag_y) * 0.08
            self.sag_vy += abs(ivme) * 0.01
            self.sag_y += self.sag_vy
        else:
            self.sol_vy += (-self.sol_y * AYAK_K - self.sol_vy * AYAK_D) * 0.15
            self.sol_vy += abs(ivme) * 0.04
            self.sol_y += self.sol_vy
            self.sag_vy += (-self.sag_y * AYAK_K - self.sag_vy * AYAK_D) * 0.15
            self.sag_vy += abs(ivme) * 0.04
            self.sag_y += self.sag_vy

        self.sol_vx += (-self.sol_x * 0.3 - self.sol_vx * 0.6) * 0.1
        self.sol_vx += ivme * 0.02
        self.sol_x += self.sol_vx
        self.sag_vx += (-self.sag_x * 0.3 - self.sag_vx * 0.6) * 0.1
        self.sag_vx += ivme * 0.02
        self.sag_x += self.sag_vx

        self.sol_x *= 0.92
        self.sag_x *= 0.92

        self.basma_mesafesi = max(0.0, self.basma_mesafesi - 0.08)

        if self.dusme_hizi > 0:
            self.basma_mesafesi = min(6.0, self.dusme_hizi * 0.8)
            self.dusme_hizi = 0.0


ayak_fizik = AyakFizik()


# ═══════════════════════════════════════════════════════════════════
# CHARACTER SPRITE LOADING (char.png → body parts)
# ═══════════════════════════════════════════════════════════════════
def karakter_yukle() -> bool:
    """Load char.png and extract body/leg surfaces. Returns True on success."""
    global _body_surf, _body_surf_f, _left_leg_surf, _left_leg_surf_f
    global _right_leg_surf, _right_leg_surf_f, _leg_composite, _leg_h
    global _shadow_surf

    path = Path(__file__).parent / "char.png"
    if not path.exists():
        print("char.png bulunamadi - wizard fallback kullanilacak")
        return False

    try:
        sprite = pygame.image.load(str(path)).convert_alpha()
    except Exception:
        return False

    w, h = sprite.get_size()  # 42 x 75
    _leg_h = h - 57  # rows 57-74

    # Surface for upper body (rows 0-56)
    _body_surf = pygame.Surface((w, 57), pygame.SRCALPHA)
    _body_surf.blit(sprite, (0, 0), (0, 0, w, 57))

    # Surfaces for left / right leg (rows 57-74)
    _left_leg_surf = pygame.Surface((w, _leg_h), pygame.SRCALPHA)
    _right_leg_surf = pygame.Surface((w, _leg_h), pygame.SRCALPHA)

    for y in range(57, h):
        for x in range(w):
            c = sprite.get_at((x, y))
            if c.a > 20:
                ly = y - 57
                if x < w // 2:
                    _left_leg_surf.set_at((x, ly), c)
                else:
                    _right_leg_surf.set_at((x, ly), c)

    # Pre-create flipped versions and composite surface
    _body_surf_f = pygame.transform.flip(_body_surf, True, False)
    _left_leg_surf_f = pygame.transform.flip(_left_leg_surf, True, False)
    _right_leg_surf_f = pygame.transform.flip(_right_leg_surf, True, False)
    _leg_composite = pygame.Surface((w, _leg_h), pygame.SRCALPHA)
    _shadow_surf = pygame.Surface((20, 6), pygame.SRCALPHA)

    print(f"Karakter yuklendi: {w}x{h}")
    return True


# ═══════════════════════════════════════════════════════════════════
# ANIMATED CHARACTER RENDERER (char.png based)
# ═══════════════════════════════════════════════════════════════════
def _ciz_karakter(sx: float, sy: float, yon: int) -> None:
    """Draw the animated armored character at (sx,sy) facing yon."""
    if _body_surf is None:
        return

    ek = game.ekran
    w = _body_surf.get_width()
    body_h = 57

    # ── Animation parameters ──
    hiz = game.hx
    yerde = game.yr
    anim = game.sz

    # Foot physics offsets
    ayak_fizik.guncelle(hiz, not yerde, yerde)
    foot_bounce = (ayak_fizik.sol_y + ayak_fizik.sag_y) * 0.3
    foot_lean = (ayak_fizik.sol_x + ayak_fizik.sag_x) * 0.2

    # Idle bob
    idle_bob = math.sin(anim * 2) * 1.5 if abs(hiz) < 0.5 else 0

    # Walk cycle (6-frame)
    walk_speed = 8 if abs(hiz) > 4 else 6
    phase = anim * walk_speed
    left_leg_off = int(round(5 * math.sin(phase))) if abs(hiz) > 0.8 else 0
    right_leg_off = int(round(5 * math.sin(phase + math.pi))) if abs(hiz) > 0.8 else 0
    walk_bob = abs(int(round(2 * math.sin(phase)))) if abs(hiz) > 0.8 else 0

    # Jump squash/stretch
    if not yerde:
        jump_squash = max(-4, min(4, int(game.hy * 0.3)))
        body_h_adj = jump_squash
        leg_tuck = game.hy * 0.2 if game.hy < 0 else 0
    else:
        body_h_adj = 0
        leg_tuck = 0

    # Landing impact
    landing_squash = int(ayak_fizik.basma_mesafesi * 0.5)

    total_squash = body_h_adj - landing_squash

    # ── Base position ──
    base_x = int(sx - w // 2 + foot_lean)
    base_y = int(sy - 45 + idle_bob + foot_bounce + total_squash * 0.5)

    # Flip for direction
    flip_x = yon < 0

    # ── Draw body (upper torso, rows 0-56) ──
    body = _body_surf_f if flip_x else _body_surf

    body_draw_y = base_y - total_squash
    ek.blit(body, (base_x, body_draw_y))

    # ── Draw legs ──
    _leg_composite.fill((0, 0, 0, 0))
    _leg_composite.blit(_left_leg_surf, (left_leg_off + foot_lean, 0), None)
    _leg_composite.blit(_right_leg_surf, (right_leg_off + foot_lean, 0), None)
    out_legs = pygame.transform.flip(_leg_composite, True, False) if flip_x else _leg_composite

    leg_draw_y = base_y + body_h - total_squash
    if not yerde and game.hy < 0:
        leg_draw_y += int(leg_tuck)
    ek.blit(out_legs, (base_x, leg_draw_y))

    # ── Hand gestures ──
    global _gesture_timer, _gesture_type
    if _gesture_timer > 0:
        _gesture_timer -= 1
        _ciz_el_animasyonu(ek, sx, sy, yon, _gesture_type)
    else:
        _gesture_type = 0
        # Random gesture trigger when idle
        if yerde and abs(hiz) < 0.5 and random.random() < 0.002:
            _gesture_type = random.randint(1, 3)
            _gesture_timer = 30

    # ── Shadow ──
    _shadow_surf.fill((0, 0, 0, 0))
    alpha = max(30, 60 - abs(game.hy) * 2)
    pygame.draw.ellipse(_shadow_surf, (0, 0, 0, alpha),
                        (0, 0, 20, 6))
    ek.blit(_shadow_surf, (int(sx - 10), int(sy + 40)))

    # ── Weapon ──
    if game.weapon:
        _ciz_silah(sx, sy, yon)

    # ── Costume overlay ──
    _ciz_kostum(sx, sy)

    # ── Magic effect ──
    _ciz_magic_effect(sx, sy)


def _ciz_el_animasyonu(ek: pygame.Surface, sx: float, sy: float,
                       yon: int, gtype: int) -> None:
    """Draw hand gesture overlays (wave, point, both up)."""
    base_y = int(sy - 10)
    hand_color = (210, 180, 180)
    skin_d = (130, 70, 70)

    if yon < 0:
        dir_mul = -1
    else:
        dir_mul = 1

    if gtype == 1:
        # Wave - right hand up
        hx = int(sx + 18 * dir_mul)
        hy = base_y - 12
        for dy in range(5):
            for dx in range(3):
                ek.set_at((hx + dx, hy + dy), hand_color)
        # Fingers spread
        for f in range(3):
            fx = hx + f * 1
            fy = hy - 2
            ek.set_at((fx + 1, fy), skin_d)
            ek.set_at((fx, fy), hand_color)

    elif gtype == 2:
        # Point - arm extended, index finger pointing
        hx = int(sx + 24 * dir_mul)
        hy = base_y
        for dy in range(4):
            for dx in range(3):
                ek.set_at((hx + dx, hy + dy), hand_color)
        # Index finger
        for fx in range(4):
            ek.set_at((hx + 3 + fx * dir_mul, hy + 1), hand_color)

    elif gtype == 3:
        # Both arms up
        for side, x_off in [(-1, -18), (1, 18)]:
            hx = int(sx + x_off)
            hy = base_y - 14
            for dy in range(4):
                for dx in range(3):
                    ek.set_at((hx + dx, hy + dy), hand_color)


# ═══════════════════════════════════════════════════════════════════
# WEAPON DRAWING (unchanged from original, slightly adapted)
# ═══════════════════════════════════════════════════════════════════
def _ciz_silah(sx: float, sy: float, yon: int) -> None:
    """Draw biome-themed weapon sprite."""
    ek = game.ekran
    m = game.mv
    w_yon = 1 if yon >= 0 else -1
    w_x = sx + (22 if yon >= 0 else -22)
    w_y = sy - 2
    c = assets.WP_DATA[m].color

    if m == "ilkbahar":
        pygame.draw.rect(ek, (60, 80, 60), (w_x, w_y - 3, 30 * w_yon, 6))
        pygame.draw.rect(ek, (80, 110, 80), (w_x, w_y - 3, 30 * w_yon, 6), 1)
        pygame.draw.rect(ek, (100, 140, 100), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
        pygame.draw.circle(ek, (255, 220, 180), (w_x + 31 * w_yon, w_y), 4)
        pygame.draw.circle(ek, (255, 200, 50), (w_x + 31 * w_yon, w_y), 2)
        pygame.draw.rect(ek, (50, 70, 50), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
        pygame.draw.rect(ek, (70, 90, 70), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
        mag_x = w_x + 2 * w_yon
        pygame.draw.polygon(ek, (70, 50, 30), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
        pygame.draw.polygon(ek, (90, 70, 50), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
        pygame.draw.polygon(ek, (50, 80, 50), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
        pygame.draw.rect(ek, (50, 70, 40), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
        pygame.draw.rect(ek, (70, 90, 60), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
        for ci in range(3):
            cx = int(w_x + (ci * 10 - 5) * w_yon)
            cy = int(w_y - 6 + ci * 6)
            pygame.draw.circle(ek, (255, 220, 200), (cx, cy), 3)
            pygame.draw.circle(ek, (255, 200, 50), (cx, cy), 1)
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


# ═══════════════════════════════════════════════════════════════════
# COSTUME OVERLAY (unchanged)
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════
# MAGIC EFFECT (unchanged)
# ═══════════════════════════════════════════════════════════════════
def _ciz_magic_effect(sx: float, sy: float) -> None:
    """Wizard magic aura particles."""
    ek = game.ekran
    for i in range(3):
        a = game.sz * 0.5 + i * 2.1
        r = 30 + math.sin(game.sz * 0.3 + i) * 5
        px = sx + math.cos(a) * r
        py = sy - 20 + math.sin(a) * r * 0.5
        s = pygame.Surface((6, 6), pygame.SRCALPHA)
        c = (100, 200, 255, 100 - i * 30)
        pygame.draw.circle(s, c, (3, 3), 3)
        ek.blit(s, (int(px), int(py)))
        if i == 0:
            for _ in range(2):
                sx2 = sx + math.cos(game.sz * 2 + _ * 3) * r
                sy2 = sy - 20 + math.sin(game.sz * 2 + _ * 3) * r * 0.4
                pygame.draw.circle(ek, (255, 215, 0), (int(sx2), int(sy2)), 1)
                pygame.draw.circle(ek, (255, 255, 200), (int(sx2), int(sy2)), 1, 1)


# ═══════════════════════════════════════════════════════════════════
# WIZARD SPRITE RENDERER (original, kept as fallback)
# ═══════════════════════════════════════════════════════════════════
def _ciz_sapka(sx: float, sy: float, yon: int) -> None:
    ek = game.ekran
    cone_pts = [(sx - 16, sy - 54), (sx + 16, sy - 54), (sx, sy - 100)]
    pygame.draw.polygon(ek, (45, 35, 85), cone_pts)
    pygame.draw.polygon(ek, (65, 55, 110), cone_pts, 1)
    for i in range(4):
        yy = sy - 60 - i * 9
        lx = sx - 14 + i * 2
        rx = sx + 14 - i * 2
        pygame.draw.arc(ek, (55, 45, 95), (sx - lx, yy - 3, lx * 2, 6), 0, math.pi, 1)
    for i in range(3):
        yy = sy - 65 - i * 11
        random.seed(int(yy))
        r2 = random.randint(0, 255)
        pygame.draw.circle(ek, (255, 215, r2), (int(sx + random.randint(-8, 8)), int(yy)), 2)
        pygame.draw.circle(ek, (255, 255, r2), (int(sx + random.randint(-8, 8)), int(yy)), 1)
    random.seed()
    pygame.draw.ellipse(ek, (50, 40, 90), (sx - 24, sy - 56, 48, 12))
    pygame.draw.ellipse(ek, (70, 60, 115), (sx - 24, sy - 56, 48, 12), 1)
    pygame.draw.ellipse(ek, (35, 25, 70), (sx - 22, sy - 54, 44, 6))
    pygame.draw.rect(ek, (120, 90, 50), (sx - 16, sy - 56, 32, 6))
    pygame.draw.rect(ek, (150, 120, 70), (sx - 16, sy - 56, 32, 6), 1)
    pygame.draw.rect(ek, (200, 180, 100), (sx - 4, sy - 55, 8, 6))
    pygame.draw.rect(ek, (255, 220, 50), (sx - 4, sy - 55, 8, 6), 1)
    pygame.draw.circle(ek, (255, 220, 50), (sx, sy - 52), 2)
    px = sx + math.sin(game.sz * 0.5) * 2
    pygame.draw.line(ek, (120, 90, 50), (sx, sy - 100), (px, sy - 112), 2)
    for i in range(4):
        a3 = game.sz * 0.3 + i * 1.57
        pygame.draw.circle(ek, (255, 215, 0), (int(px + math.cos(a3) * 3), int(sy - 112 + math.sin(a3) * 2)), 2)
        pygame.draw.circle(ek, (255, 255, 200), (int(px + math.cos(a3) * 3), int(sy - 112 + math.sin(a3) * 2)), 1)


def _ciz_sac_ve_sakal(sx: float, sy: float) -> None:
    ek = game.ekran
    for side in [-1, 1]:
        for i in range(4):
            yy = sy - 38 + i * 4
            xx = sx + side * (13 + i * 1.5)
            pygame.draw.ellipse(ek, (220, 220, 230), (xx - 2, yy, 5, 12))
            pygame.draw.ellipse(ek, (190, 190, 200), (xx - 2, yy, 5, 12), 1)
    for i in range(8):
        bx = sx - 5 + i * 1.5
        by = sy - 16 + i * 2
        bw = 4 + i * 0.5
        bh = 10 + i * 2
        pygame.draw.ellipse(ek, (220, 220, 230), (bx, by, bw, bh))
        pygame.draw.ellipse(ek, (190, 190, 200), (bx, by, bw, bh), 1)
    pygame.draw.polygon(ek, (220, 220, 230), [(sx - 4, sy + 2), (sx + 4, sy + 2), (sx, sy + 14)])
    pygame.draw.polygon(ek, (190, 190, 200), [(sx - 4, sy + 2), (sx + 4, sy + 2), (sx, sy + 14)], 1)
    pygame.draw.arc(ek, (220, 220, 230), (sx - 10, sy - 26, 20, 10), 0.2, 2.9, 2)
    pygame.draw.arc(ek, (220, 220, 230), (sx - 8, sy - 28, 16, 8), 0.3, 2.8, 2)


def _ciz_kafa(sx: float, sy: float) -> None:
    ek = game.ekran
    pygame.draw.ellipse(ek, (245, 210, 190), (sx - 14, sy - 46, 28, 38))
    pygame.draw.ellipse(ek, (235, 200, 180), (sx - 13, sy - 40, 12, 16))
    pygame.draw.ellipse(ek, (235, 200, 180), (sx + 1, sy - 40, 12, 16))
    for i in range(3):
        yy = sy - 30 + i * 6
        pygame.draw.arc(ek, (220, 185, 165), (sx - 12, yy, 24, 4), 0, 3.14, 1)
    pygame.draw.line(ek, (220, 185, 165), (sx - 12, sy - 38), (sx - 6, sy - 36), 1)
    pygame.draw.line(ek, (220, 185, 165), (sx + 6, sy - 36), (sx + 12, sy - 38), 1)
    pygame.draw.line(ek, (225, 190, 170), (sx, sy - 24), (sx, sy - 18), 2)
    pygame.draw.circle(ek, (220, 185, 165), (sx, sy - 18), 2)
    pygame.draw.line(ek, (230, 195, 175), (sx - 1, sy - 22), (sx - 4, sy - 20), 1)
    pygame.draw.line(ek, (230, 195, 175), (sx + 1, sy - 22), (sx + 4, sy - 20), 1)
    for off in [-1, 1]:
        pygame.draw.line(ek, (220, 220, 230), (sx + off * 3 - 8, sy - 44), (sx + off * 3 - 1, sy - 45), 2)
        pygame.draw.line(ek, (190, 190, 200), (sx + off * 3 - 8, sy - 44), (sx + off * 3 - 1, sy - 45), 1)
    if game.yr and abs(game.hx) < 0.5:
        pygame.draw.arc(ek, (210, 160, 150), (sx - 5, sy - 24, 10, 7), 0.1, 3.0, 2)
    else:
        pygame.draw.arc(ek, (200, 150, 140), (sx - 4, sy - 22, 8, 5), 0, 3.14, 2)
        pygame.draw.line(ek, (180, 130, 120), (sx - 5, sy - 23), (sx + 5, sy - 23), 2)


def _ciz_gozler(sx: float, sy: float) -> None:
    ek = game.ekran
    ga = game.gk % 180 > 5
    if not ga:
        pygame.draw.line(ek, (40, 40, 40), (sx - 10, sy - 35), (sx - 1, sy - 35), 2)
        pygame.draw.line(ek, (40, 40, 40), (sx + 1, sy - 35), (sx + 10, sy - 35), 2)
        return
    pygame.draw.ellipse(ek, (255, 255, 240), (sx - 11, sy - 39, 11, 9))
    pygame.draw.ellipse(ek, (255, 255, 240), (sx + 1, sy - 39, 11, 9))
    for off in [-5, 5]:
        cx = sx + off
        cy = sy - 35
        pygame.draw.circle(ek, (100, 200, 255), (cx, cy), 5)
        pygame.draw.circle(ek, (50, 150, 255), (cx, cy), 5, 1)
        for i in range(4):
            a_s = i * 1.57 + game.sz * 0.3
            pygame.draw.line(ek, (150, 220, 255),
                             (cx + int(math.cos(a_s) * 3), cy + int(math.sin(a_s) * 3)),
                             (cx + int(math.cos(a_s) * 4), cy + int(math.sin(a_s) * 4)), 1)
        pygame.draw.circle(ek, (0, 50, 100), (cx, cy), 2)
        pygame.draw.circle(ek, (255, 255, 255), (cx - 2, cy - 2), 1)
    for i, kx in enumerate([-11, -9, 9, 11]):
        kys = -39
        ky2 = -42 + i * 0.5
        pygame.draw.line(ek, (30, 30, 30), (sx + kx, sy + kys), (sx + kx - 1 + i * 0.5, sy + ky2), 1)


def _ciz_govde(sx: float, sy: float) -> None:
    ek = game.ekran
    robe = (60, 50, 100)
    robe_d = (45, 35, 80)
    robe_l = (80, 70, 120)
    pygame.draw.rect(ek, (245, 210, 190), (sx - 4, sy - 14, 8, 6))
    pygame.draw.line(ek, (220, 185, 170), (sx - 3, sy - 14), (sx - 3, sy - 9), 1)
    pygame.draw.line(ek, (220, 185, 170), (sx + 3, sy - 14), (sx + 3, sy - 9), 1)
    pygame.draw.rect(ek, robe, (sx - 18, sy - 10, 36, 34), border_radius=4)
    pygame.draw.rect(ek, robe_d, (sx - 18, sy - 10, 36, 34), 1, border_radius=4)
    for i in range(4):
        yy = sy - 6 + i * 8
        pygame.draw.line(ek, robe_l, (sx - 12, yy), (sx + 12, yy), 1)
        pygame.draw.line(ek, robe_d, (sx - 14, yy + 1), (sx + 14, yy + 1), 1)
    pygame.draw.polygon(ek, robe_d, [(sx - 7, sy - 10), (sx + 7, sy - 10), (sx, sy - 1)])
    pygame.draw.polygon(ek, (120, 100, 160), [(sx - 7, sy - 10), (sx - 12, sy - 2), (sx, sy - 3)])
    pygame.draw.polygon(ek, (120, 100, 160), [(sx + 7, sy - 10), (sx + 12, sy - 2), (sx, sy - 3)])
    pygame.draw.polygon(ek, (50, 40, 30), [(sx - 4, sy - 2), (sx + 4, sy - 2), (sx + 3, sy + 8), (sx, sy + 12), (sx - 3, sy + 8)])
    pygame.draw.polygon(ek, (70, 60, 50), [(sx - 4, sy - 2), (sx + 4, sy - 2), (sx + 3, sy + 8), (sx, sy + 12), (sx - 3, sy + 8)], 1)
    pygame.draw.circle(ek, (200, 180, 100), (sx, sy + 3), 3)
    pygame.draw.circle(ek, (255, 220, 50), (sx, sy + 3), 2)
    for _ in range(4):
        rsx = sx + random.randint(-12, 12)
        rsy = sy + random.randint(-2, 14)
        rsize = random.randint(1, 2)
        pygame.draw.circle(ek, (255, 215, 0), (rsx, rsy), rsize)
        pygame.draw.circle(ek, (255, 255, 200), (rsx, rsy), rsize, 1)
    pygame.draw.line(ek, robe_d, (sx - 17, sy + 6), (sx - 20, sy + 16), 1)
    pygame.draw.line(ek, robe_d, (sx + 17, sy + 6), (sx + 20, sy + 16), 1)


def _ciz_etek(sx: float, sy: float, yon: int, iv: pygame.Vector2) -> None:
    ek = game.ekran
    robe = (60, 50, 100)
    robe_d = (45, 35, 80)
    robe_l = (80, 70, 120)
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
    sol_x = sx - 10 + ba * 0.08
    sag_x = sx + 1 - ba * 0.08
    pygame.draw.rect(ek, robe, (sol_x - 3, sy + 22 + syk, 15, 20), border_radius=3)
    pygame.draw.rect(ek, robe_d, (sol_x - 3, sy + 22 + syk, 15, 20), 1, border_radius=3)
    pygame.draw.rect(ek, robe, (sag_x - 3, sy + 22 + sagk, 15, 20), border_radius=3)
    pygame.draw.rect(ek, robe_d, (sag_x - 3, sy + 22 + sagk, 15, 20), 1, border_radius=3)
    for x_off, y_off in [(sol_x, syk), (sag_x, sagk)]:
        pygame.draw.line(ek, robe_l, (x_off + 4, sy + 24 + y_off), (x_off + 4, sy + 40 + y_off), 1)
        pygame.draw.line(ek, robe_d, (x_off + 1, sy + 26 + y_off), (x_off + 8, sy + 28 + y_off), 1)
    for _ in range(2):
        rsx = sol_x + random.randint(-1, 8)
        rsy = sy + 24 + syk + random.randint(0, 14)
        pygame.draw.circle(ek, (255, 215, 0), (rsx, rsy), 1)
        rsx = sag_x + random.randint(-1, 8)
        rsy = sy + 24 + sagk + random.randint(0, 14)
        pygame.draw.circle(ek, (255, 215, 0), (rsx, rsy), 1)
    ayak_fizik.guncelle(game.hx, not game.yr, game.yr)
    for i, (x_off, y_off) in enumerate([(sol_x, syk), (sag_x, sagk)]):
        if i == 0:
            fy = ayak_fizik.sol_y
            fx = ayak_fizik.sol_x
        else:
            fy = ayak_fizik.sag_y
            fx = ayak_fizik.sag_x
        bot_y = sy + 38 + y_off + fy
        bot_x = x_off + fx
        squash = max(0, ayak_fizik.basma_mesafesi - abs(fy) * 0.5)
        bot_w = 16 + squash * 1.5
        bot_h = 8 - squash * 0.8
        pygame.draw.ellipse(ek, (50, 40, 80), (bot_x - bot_w // 2, bot_y, bot_w, max(3, bot_h)))
        pygame.draw.ellipse(ek, (70, 60, 110), (bot_x - (bot_w - 2) // 2, bot_y + 1, bot_w - 2, max(2, bot_h - 2)))
        pygame.draw.rect(ek, (40, 30, 70), (bot_x - bot_w // 2, bot_y + bot_h - 3, bot_w, 3), border_radius=1)
        for si in range(4):
            taban_x = bot_x - 5 + si * 3 + fx * 0.3
            pygame.draw.circle(ek, (60, 50, 90), (int(taban_x), int(bot_y + bot_h - 1)), 1)
        pygame.draw.line(ek, (80, 60, 100), (int(bot_x - 2), int(bot_y + 1)),
                         (int(bot_x + 2), int(bot_y + 1)), 1)
        pygame.draw.line(ek, (80, 60, 100), (int(bot_x - 1), int(bot_y + 3)),
                         (int(bot_x + 1), int(bot_y + 3)), 1)


def _ciz_kollar(sx: float, sy: float, yon: int) -> None:
    """Wizard arms (kept for fallback)."""
    ek = game.ekran
    wd_cd = assets.WP_DATA[game.mv].cooldown if game.weapon else 10
    geri_tepme = (wd_cd - game.shoot_cd) / wd_cd if game.shoot_cd > 0 else 0
    geri_tepme = max(0.0, min(1.0, geri_tepme))
    yuruyus = math.sin(game.sz * 8) if abs(game.hx) > 1 else 0
    kol_yukari = math.sin(game.sz * 6) * 4 if abs(game.hx) > 1 else 0
    kol_yukari += geri_tepme * 10
    kol_diz = 0.4 + abs(math.sin(game.sz * 6)) * 0.3 if abs(game.hx) > 1 else 0.2
    kol_diz += geri_tepme * 0.5
    robe_l = (80, 70, 120)
    robe_d = (45, 35, 80)
    kol_renk = (55, 45, 90)
    for side in [-1, 1]:
        shoulder_x = sx + side * 16
        shoulder_y = sy - 8
        upper_len = 16
        forearm_len = 14
        if game.weapon:
            raise_a = kol_yukari * side
            walk_swing = yuruyus * side * 3
            elbow_a = -0.3 + raise_a * 0.05 + walk_swing * 0.02
            hand_a = elbow_a + kol_diz
            elbow_x = shoulder_x + math.cos(elbow_a) * upper_len
            elbow_y = shoulder_y + math.sin(elbow_a) * upper_len + walk_swing
            hand_x = elbow_x + math.cos(hand_a) * forearm_len
            hand_y = elbow_y + math.sin(hand_a) * forearm_len + walk_swing * 0.5
            pygame.draw.line(ek, robe_d, (int(shoulder_x), int(shoulder_y)),
                             (int(elbow_x), int(elbow_y)), 7)
            pygame.draw.line(ek, robe_l, (int(shoulder_x), int(shoulder_y)),
                             (int(elbow_x), int(elbow_y)), 2)
            pygame.draw.line(ek, robe_d, (int(elbow_x), int(elbow_y)),
                             (int(hand_x), int(hand_y)), 6)
            pygame.draw.line(ek, robe_l, (int(elbow_x), int(elbow_y)),
                             (int(hand_x), int(hand_y)), 2)
            pygame.draw.ellipse(ek, kol_renk, (int(elbow_x) - 4, int(elbow_y) - 3, 8, 6))
            pygame.draw.ellipse(ek, robe_d, (int(hand_x) - 4, int(hand_y) - 3, 8, 6))
        else:
            idle_sway = math.sin(game.sz * 1.5 + side * 0.5) * 2
            walk_swing = yuruyus * side * 4
            elbow_a = 0.5 + idle_sway * 0.05 + walk_swing * 0.03
            hand_a = elbow_a + 0.8
            elbow_x = shoulder_x + math.cos(elbow_a) * upper_len
            elbow_y = shoulder_y + math.sin(elbow_a) * upper_len + walk_swing
            hand_x = elbow_x + math.cos(hand_a) * forearm_len
            hand_y = elbow_y + math.sin(hand_a) * forearm_len + walk_swing * 0.3
            pygame.draw.line(ek, robe_d, (int(shoulder_x), int(shoulder_y)),
                             (int(elbow_x), int(elbow_y)), 7)
            pygame.draw.line(ek, robe_l, (int(shoulder_x), int(shoulder_y)),
                             (int(elbow_x), int(elbow_y)), 2)
            pygame.draw.line(ek, robe_d, (int(elbow_x), int(elbow_y)),
                             (int(hand_x), int(hand_y)), 6)
            pygame.draw.line(ek, robe_l, (int(elbow_x), int(elbow_y)),
                             (int(hand_x), int(hand_y)), 2)
            pygame.draw.ellipse(ek, kol_renk, (int(elbow_x) - 4, int(elbow_y) - 3, 8, 6))
            pygame.draw.ellipse(ek, robe_d, (int(hand_x) - 4, int(hand_y) - 3, 8, 6))
    if game.weapon:
        _ciz_silah(sx, sy, yon)


# ═══════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════
def ciz_krk(x: float, y: float, yn: int, yy: float = 0.0) -> None:
    """Draw the full character at (x, y) facing yn.
    
    Uses the animated char.png renderer if available,
    falls back to the wizard procedural drawing.
    """
    global _onceki_oy, _onceki_yr

    game.sz += 0.05
    game.gk += 1
    y += yy
    game.sh += (game.hx * 0.3 - game.sh) * 0.15

    yon = 1 if yn >= 0 else -1
    sx = x
    sy = y

    # Landing detection
    if not _onceki_yr and game.yr:
        ayak_fizik.dusme_hizi = abs(game.hx) * 2 + 3

    # ── Render path: char.png based OR wizard fallback ──
    if _body_surf is not None:
        _ciz_karakter(sx, sy, yon)
    elif game.wizard_sprite is not None:
        _ciz_krk_sprite(sx, sy, yon)
    else:
        _ciz_krk_procedural(sx, sy, yon)

    # ── Particles ──
    if abs(game.hx) < 0.5 and game.yr and random.random() < 0.04:
        px2 = sx + random.randint(-18, 18)
        py2 = sy + 10 + random.randint(-20, 5)
        renk = random.choice([(100, 150, 255), (150, 200, 255), (200, 230, 255)])
        particles.ptk_ekle(px2, py2, renk, 1)

    if game.yr and abs(game.hx) > 1.5 and random.random() < 0.12:
        particles.ptk_ekle(sx + random.randint(-6, 6), sy + 22, (180, 180, 200), 2)

    if not _onceki_yr and game.yr:
        for _ in range(5):
            particles.ptk_ekle(sx + random.randint(-10, 10), sy + 22, (180, 200, 255), 2)
        particles.ptk_patlatma(sx, sy + 22, (180, 200, 255), 6, 3)

    if not game.yr and random.random() < 0.06:
        particles.ptk_ekle(sx + random.randint(-8, 8), sy + random.randint(-5, 15), (150, 200, 255), 1)

    _onceki_oy = game.oy
    _onceki_yr = game.yr


def _ciz_krk_sprite(sx: float, sy: float, yon: int) -> None:
    """Draw wizard from WİZARD.gif + arms/effects (original)."""
    ek = game.ekran
    sprite = game.wizard_sprite
    if sprite is None:
        return
    if yon < 0:
        sprite = pygame.transform.flip(sprite, True, False)
    ayak_fizik.guncelle(game.hx, not game.yr, game.yr)
    idle_bob = math.sin(game.sz * 2) * 2 if abs(game.hx) < 0.5 else 0
    foot_bounce_l = ayak_fizik.sol_y * 0.5
    foot_bounce_r = ayak_fizik.sag_y * 0.5
    foot_shift_l = ayak_fizik.sol_x * 0.3
    foot_shift_r = ayak_fizik.sag_x * 0.3
    draw_x = int(sx - sprite.get_width() // 2)
    draw_y = int(sy - sprite.get_height() + 25 + idle_bob + (foot_bounce_l + foot_bounce_r) * 0.3)
    ek.blit(sprite, (draw_x, draw_y))
    _ciz_kollar(sx, sy, yon)
    _ciz_magic_effect(sx, sy)
    _ciz_kostum(sx, sy)


def _ciz_krk_procedural(sx: float, sy: float, yon: int) -> None:
    """Draw wizard from primitives (original fallback)."""
    ek = game.ekran
    iv = pygame.Vector2(math.sin(game.sz) * 2, math.sin(game.sz * 0.6) * 0.8)
    hizlanma = game.hx * 0.1
    _ciz_sapka(sx, sy, yon)
    _ciz_sac_ve_sakal(sx, sy)
    _ciz_kafa(sx, sy)
    _ciz_gozler(sx, sy)
    _ciz_govde(sx, sy)
    _ciz_etek(sx, sy, yon, iv)
    _ciz_kollar(sx, sy, yon)
    _ciz_magic_effect(sx, sy)
    _ciz_kostum(sx, sy)
