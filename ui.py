import math
import pygame
import assets
import game

def btn(m, x, y, w, h, n, u, yr=assets.B):
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, w, h)
    u2 = r.collidepoint(mx, my)
    pygame.draw.rect(game.ekran, (10, 10, 20), (x+3, y+3, w, h), border_radius=8)
    pygame.draw.rect(game.ekran, u if u2 else n, r, border_radius=8)
    pygame.draw.rect(game.ekran, yr, r, 2, border_radius=8)
    t = game.fm.render(m, True, yr)
    game.ekran.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return u2 and game.ft

def ikon(x, y, s, rn=assets.B):
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, 36, 36)
    u = r.collidepoint(mx, my)
    pygame.draw.circle(game.ekran, assets.AGT if u else (30, 30, 50), (x+18, y+18), 18)
    pygame.draw.circle(game.ekran, rn, (x+18, y+18), 18, 2)
    cx, cy = x+18, y+18
    if s == "A":
        for a in range(6):
            a2 = a * 1.047
            pygame.draw.line(game.ekran, rn, (cx+int(math.cos(a2)*9), cy+int(math.sin(a2)*9)), (cx+int(math.cos(a2)*14), cy+int(math.sin(a2)*14)), 4)
        pygame.draw.circle(game.ekran, (30, 30, 50), (cx, cy), 7)
    elif s == "R":
        pygame.draw.arc(game.ekran, rn, (cx-7, cy-7, 14, 14), 0.5, 5.5, 3)
        ex = cx + int(7 * math.cos(5.5))
        ey = cy + int(7 * math.sin(5.5))
        tx, ty = -math.sin(5.5), math.cos(5.5)
        pygame.draw.line(game.ekran, rn, (ex, ey), (ex+int(tx*3+ty*2), ey+int(ty*3-tx*2)), 2)
        pygame.draw.line(game.ekran, rn, (ex, ey), (ex+int(tx*3-ty*2), ey+int(ty*3+tx*2)), 2)
    elif s == "M":
        pygame.draw.polygon(game.ekran, rn, [(cx, cy-10), (cx-10, cy), (cx+10, cy)])
        pygame.draw.rect(game.ekran, rn, (cx-8, cy, 16, 14))
        pygame.draw.rect(game.ekran, rn, (cx-3, cy+6, 6, 8))
    elif s == "S":
        pygame.draw.polygon(game.ekran, rn, [(cx-3, cy-6), (cx+6, cy-10), (cx+6, cy+10), (cx-3, cy+6)])
        for li in range(2):
            lx = cx + 7 + li*4
            pygame.draw.line(game.ekran, rn, (lx, cy-5), (lx, cy+5), 2)
    return u and game.ft

def disket(x, y):
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, 32, 32)
    u = r.collidepoint(mx, my)
    renk = assets.AGT if u else (50, 60, 80)
    pygame.draw.rect(game.ekran, renk, r, border_radius=4)
    pygame.draw.rect(game.ekran, assets.B, r, 2, border_radius=4)
    # disket govde cizgisi
    pygame.draw.rect(game.ekran, (30, 30, 50), (x+4, y+18, 24, 10))
    pygame.draw.rect(game.ekran, (60, 70, 90), (x+6, y+6, 20, 14))
    return u and game.ft
