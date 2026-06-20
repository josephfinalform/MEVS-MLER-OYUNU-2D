import math
import pygame
import assets
import game

gs = pygame.Surface((60, 80), pygame.SRCALPHA)
pygame.draw.ellipse(gs, (255, 20, 147, 25), (5, 5, 50, 65))
pygame.draw.ellipse(gs, (255, 50, 180, 40), (10, 10, 40, 55))

def ciz_krk(x, y, yn, yy=0):
    game.sz += 0.05; game.gk += 1; y += yy
    game.sh += (game.hx*0.3 - game.sh)*0.15
    iv = pygame.Vector2(math.sin(game.sz)*2, math.sin(game.sz*0.6)*0.8)
    sy2 = game.sh*0.6 + game.hy*0.3 + iv.x
    game.ekran.blit(gs, (x-30, y-15))
    for o in range(-16, 18, 4):
        u = 20 + abs(o)*0.5; e = sy2*(1-abs(o)/20)
        pygame.draw.rect(game.ekran, assets.SG, (x+o+e-2, y-50, 4, 18+u))
    sk2 = max(-8, min(8, sy2))
    pygame.draw.ellipse(game.ekran, assets.SAC, (x-18+sk2, y-58, 36, 28))
    pygame.draw.ellipse(game.ekran, assets.SAC, (x-20+sk2*1.5, y-52, 15, 22))
    pygame.draw.ellipse(game.ekran, assets.SAC, (x+5+sk2*1.5, y-52, 15, 22))
    pygame.draw.ellipse(game.ekran, assets.TEN, (x-13, y-44, 26, 30))
    pygame.draw.ellipse(game.ekran, assets.TEN, (x-15, y-40, 12, 18))
    pygame.draw.ellipse(game.ekran, assets.TEN, (x+3, y-40, 12, 18))
    ga = game.gk % 180 > 5
    if ga:
        pygame.draw.ellipse(game.ekran, assets.GB, (x-11, y-38, 12, 14))
        pygame.draw.ellipse(game.ekran, assets.GB, (x-1, y-38, 12, 14))
        pygame.draw.ellipse(game.ekran, assets.GM, (x-9, y-36, 8, 10))
        pygame.draw.ellipse(game.ekran, assets.GM, (x+1, y-36, 8, 10))
        pygame.draw.circle(game.ekran, assets.GI, (x-5, y-33), 3)
        pygame.draw.circle(game.ekran, assets.GI, (x+5, y-33), 3)
        pygame.draw.circle(game.ekran, assets.S, (x-6, y-33), 2)
        pygame.draw.circle(game.ekran, assets.S, (x+4, y-33), 2)
    else:
        pygame.draw.line(game.ekran, assets.S, (x-10, y-31), (x-3, y-31), 2)
        pygame.draw.line(game.ekran, assets.S, (x+3, y-31), (x+10, y-31), 2)
    if game.yr and abs(game.hx)<0.5: pygame.draw.arc(game.ekran, assets.AG, (x-5, y-28, 10, 8), 0.2, 2.9, 2)
    else: pygame.draw.arc(game.ekran, assets.AG, (x-4, y-26, 8, 6), 0, 3.14, 2)
    pygame.draw.rect(game.ekran, assets.TEN, (x-4, y-14, 8, 6))
    nf = math.sin(game.sz*0.8)*1.5
    pygame.draw.ellipse(game.ekran, assets.PEMBE, (x-16, y-10+nf, 32, 22))
    pygame.draw.line(game.ekran, assets.NP, (x, y-8), (x, y+8), 2)
    pygame.draw.line(game.ekran, assets.NM, (x-8, y-4), (x-8, y+4), 1)
    pygame.draw.line(game.ekran, assets.NM, (x+8, y-4), (x+8, y+4), 1)
    if game.aktif_k == "sonbahar":
        pygame.draw.polygon(game.ekran, assets.YP, [(x-16,y-6),(x-22,y+20),(x-8,y+18)])
        pygame.draw.polygon(game.ekran, assets.YP, [(x+16,y-6),(x+22,y+20),(x+8,y+18)])
    pygame.draw.rect(game.ekran, assets.S, (x-16, y+6, 32, 28))
    pygame.draw.rect(game.ekran, (30,30,40), (x-16, y+6, 32, 28), 1)
    pygame.draw.line(game.ekran, assets.NM, (x-8, y+8), (x-8, y+32), 2)
    pygame.draw.line(game.ekran, assets.NP, (x-6, y+10), (x-6, y+30), 1)
    pygame.draw.line(game.ekran, assets.NM, (x+8, y+8), (x+8, y+32), 2)
    pygame.draw.line(game.ekran, assets.NP, (x+6, y+10), (x+6, y+30), 1)
    pygame.draw.rect(game.ekran, assets.PEMBE, (x-17, y+4, 34, 5))
    pygame.draw.rect(game.ekran, assets.NP, (x-17, y+4, 34, 5), 1)
    if game.aktif_k == "yaz":
        pygame.draw.circle(game.ekran, assets.ALTIN, (x-8, y-35), 7, 2)
        pygame.draw.circle(game.ekran, assets.ALTIN, (x+8, y-35), 7, 2)
        pygame.draw.line(game.ekran, assets.ALTIN, (x-1, y-35), (x+1, y-35), 2)
    if not game.yr: ba=0; syk=-6; sagk=-6
    elif abs(game.hx)>1:
        ba=math.sin(game.sz*8)*30*(1 if game.hx>0 else -1)
        syk=abs(math.sin(game.sz*8))*6; sagk=abs(math.cos(game.sz*8))*6
    else: ba=iv.x*3; syk=iv.x*0.5; sagk=-iv.x*0.5
    sx=x-9+ba*0.08; gx=x+2-ba*0.08
    pygame.draw.rect(game.ekran, assets.S, (sx, y+28+syk, 7, 10))
    pygame.draw.rect(game.ekran, assets.S, (gx, y+28+sagk, 7, 10))
    pygame.draw.rect(game.ekran, assets.MB, (sx-3, y+36+syk, 14, 10))
    pygame.draw.rect(game.ekran, assets.MB, (gx-3, y+36+sagk, 14, 10))
    pygame.draw.line(game.ekran, assets.NM, (sx-1, y+38+syk), (sx+9, y+38+syk), 2)
    pygame.draw.line(game.ekran, assets.NM, (gx-1, y+38+sagk), (gx+9, y+38+sagk), 2)
    pygame.draw.rect(game.ekran, assets.NM, (sx-4, y+44+syk, 16, 3))
    pygame.draw.rect(game.ekran, assets.NM, (gx-4, y+44+sagk, 16, 3))
    if game.aktif_k == "ilkbahar":
        for i in range(5):
            a=x-12+i*6; pygame.draw.circle(game.ekran, assets.C1, (a, y-52), 4)
            pygame.draw.circle(game.ekran, assets.C2, (a, y-52), 2)
    if game.aktif_k == "kis":
        for i in range(5):
            a=x-12+i*6; pygame.draw.circle(game.ekran, assets.KR, (a, y-54), 5)
            pygame.draw.circle(game.ekran, assets.B, (a, y-54), 3)
