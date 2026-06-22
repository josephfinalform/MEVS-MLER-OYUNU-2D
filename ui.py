"""Reusable UI components: buttons, icons, save disk."""

from __future__ import annotations

import math

import pygame

import assets
import game


def btn(
    metin: str,
    x: int,
    y: int,
    w: int,
    h: int,
    normal_renk: tuple[int, int, int],
    uzeri_renk: tuple[int, int, int],
    yazi_renk: tuple[int, int, int] = assets.B,
) -> bool:
    """Draw a rounded button with shadow, return True when clicked."""
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, w, h)
    hover = r.collidepoint(mx, my)

    pygame.draw.rect(game.ekran, (10, 10, 20), (x + 3, y + 3, w, h), border_radius=8)
    pygame.draw.rect(game.ekran, uzeri_renk if hover else normal_renk, r, border_radius=8)
    pygame.draw.rect(game.ekran, yazi_renk, r, 2, border_radius=8)

    t = game.fm.render(metin, True, yazi_renk)
    game.ekran.blit(t, (x + w // 2 - t.get_width() // 2, y + h // 2 - t.get_height() // 2))
    return hover and game.ft


def ikon(x: int, y: int, sekil: str, renk: tuple[int, int, int] = assets.B) -> bool:
    """Draw an icon button, return True when clicked.

    Supported shapes: A (arrow), R (refresh), M (home), S (speaker).
    """
    mx, my = pygame.mouse.get_pos()
    cx, cy = x + 18, y + 18
    r = pygame.Rect(x, y, 36, 36)
    hover = r.collidepoint(mx, my)

    pygame.draw.circle(game.ekran, assets.AGT if hover else (30, 30, 50), (cx, cy), 18)
    pygame.draw.circle(game.ekran, renk, (cx, cy), 18, 2)

    if sekil == "A":
        for a in range(6):
            a2 = a * 1.047
            dx = int(math.cos(a2) * 9)
            dy = int(math.sin(a2) * 9)
            dx2 = int(math.cos(a2) * 14)
            dy2 = int(math.sin(a2) * 14)
            pygame.draw.line(game.ekran, renk, (cx + dx, cy + dy), (cx + dx2, cy + dy2), 4)
        pygame.draw.circle(game.ekran, (30, 30, 50), (cx, cy), 7)
    elif sekil == "R":
        pygame.draw.arc(game.ekran, renk, (cx - 7, cy - 7, 14, 14), 0.5, 5.5, 3)
        ex = cx + int(7 * math.cos(5.5))
        ey = cy + int(7 * math.sin(5.5))
        tx, ty = -math.sin(5.5), math.cos(5.5)
        pygame.draw.line(game.ekran, renk, (ex, ey), (ex + int(tx * 3 + ty * 2), ey + int(ty * 3 - tx * 2)), 2)
        pygame.draw.line(game.ekran, renk, (ex, ey), (ex + int(tx * 3 - ty * 2), ey + int(ty * 3 + tx * 2)), 2)
    elif sekil == "M":
        pygame.draw.polygon(game.ekran, renk, [(cx, cy - 10), (cx - 10, cy), (cx + 10, cy)])
        pygame.draw.rect(game.ekran, renk, (cx - 8, cy, 16, 14))
        pygame.draw.rect(game.ekran, renk, (cx - 3, cy + 6, 6, 8))
    elif sekil == "S":
        pygame.draw.polygon(game.ekran, renk, [(cx - 3, cy - 6), (cx + 6, cy - 10), (cx + 6, cy + 10), (cx - 3, cy + 6)])
        for li in range(2):
            lx = cx + 7 + li * 4
            pygame.draw.line(game.ekran, renk, (lx, cy - 5), (lx, cy + 5), 2)

    return hover and game.ft


def disket(x: int, y: int) -> bool:
    """Draw a save-disk icon button, return True when clicked."""
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, 32, 32)
    hover = r.collidepoint(mx, my)
    renk = assets.AGT if hover else (50, 60, 80)

    pygame.draw.rect(game.ekran, renk, r, border_radius=4)
    pygame.draw.rect(game.ekran, assets.B, r, 2, border_radius=4)
    pygame.draw.rect(game.ekran, (30, 30, 50), (x + 4, y + 18, 24, 10))
    pygame.draw.rect(game.ekran, (60, 70, 90), (x + 6, y + 6, 20, 14))

    return hover and game.ft
