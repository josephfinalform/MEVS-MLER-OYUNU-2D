import pygame
import assets
import game

def btn(m, x, y, w, h, n, u, yr=assets.B):
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, w, h)
    u2 = r.collidepoint(mx, my)
    pygame.draw.rect(game.ekran, (0, 0, 0, 60), (x+3, y+3, w, h), border_radius=8)
    pygame.draw.rect(game.ekran, u if u2 else n, r, border_radius=8)
    pygame.draw.rect(game.ekran, yr, r, 2, border_radius=8)
    t = game.fm.render(m, True, yr)
    game.ekran.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return u2 and game.ft

def ikon(x, y, s, rn=assets.B):
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, 36, 36)
    u = r.collidepoint(mx, my)
    pygame.draw.circle(game.ekran, assets.AGT if u else assets.GT, (x+18, y+18), 20)
    pygame.draw.circle(game.ekran, rn, (x+18, y+18), 20, 2)
    if s == "A":
        pygame.draw.circle(game.ekran, rn, (x+18, y+18), 8, 2)
        pygame.draw.line(game.ekran, rn, (x+18, y+8), (x+18, y+10), 2)
        pygame.draw.line(game.ekran, rn, (x+8, y+18), (x+10, y+18), 2)
        pygame.draw.line(game.ekran, rn, (x+26, y+18), (x+28, y+18), 2)
    elif s == "R":
        pygame.draw.line(game.ekran, rn, (x+12, y+12), (x+22, y+12), 3)
        pygame.draw.line(game.ekran, rn, (x+12, y+12), (x+12, y+22), 3)
        pygame.draw.line(game.ekran, rn, (x+22, y+12), (x+22, y+22), 3)
        pygame.draw.line(game.ekran, rn, (x+12, y+22), (x+22, y+22), 3)
        pygame.draw.polygon(game.ekran, rn, [(x+24, y+14), (x+28, y+18), (x+24, y+22)])
    elif s == "M":
        pygame.draw.rect(game.ekran, rn, (x+10, y+16, 16, 12), 2)
        pygame.draw.polygon(game.ekran, rn, [(x+9, y+18), (x+18, y+10), (x+27, y+18)])
        pygame.draw.rect(game.ekran, rn, (x+16, y+22, 4, 6))
    return u and game.ft
