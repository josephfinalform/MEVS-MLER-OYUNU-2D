import math
import random
import pygame
import assets
import game

yldzlar = [{"x": random.randint(0, assets.GENISLIK), "y": random.randint(0, assets.YUKSEKLIK), "h": random.uniform(0.1, 0.3), "b": random.randint(1, 2)} for _ in range(25)]

def ptk_ekle(x, y, r, s=8):
    for _ in range(s):
        a = random.uniform(0, math.pi*2)
        h = random.uniform(1, 3)
        game.ptk.append({"x":x,"y":y,"vx":math.cos(a)*h,"vy":math.sin(a)*h-2,"r":r,"o":random.randint(15,25),"b":random.randint(2,4)})

def ptk_guncelle():
    for p in game.ptk[:]:
        p["x"] += p["vx"]; p["y"] += p["vy"]
        p["vy"] += 0.1; p["o"] -= 1
        if p["o"] <= 0: game.ptk.remove(p)

def ptk_ciz():
    for p in game.ptk:
        a = max(0, min(255, p["o"]*12))
        s2 = pygame.Surface((p["b"]*2, p["b"]*2), pygame.SRCALPHA)
        pygame.draw.circle(s2, (*p["r"], a), (p["b"], p["b"]), p["b"])
        game.ekran.blit(s2, (p["x"]-p["b"], p["y"]-p["b"]))

def ark_ciz():
    game.ekran.fill(game.rnk["a"])
    for y in yldzlar:
        y["y"] += y["h"]
        if y["y"] > assets.YUKSEKLIK: y["y"] = 0; y["x"] = random.randint(0, assets.GENISLIK)
        pygame.draw.circle(game.ekran, game.rnk["ac"], (int(y["x"]), int(y["y"])), y["b"])
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(game.ekran, game.rnk["ac"], (i, 0), (i, assets.YUKSEKLIK), 1)
    d = game.lvl.get("d", "")
    if d == "cicek":
        for _ in range(10):
            cx = random.randint(0, assets.GENISLIK); cy = random.randint(0, assets.YUKSEKLIK-100)
            pygame.draw.circle(game.ekran, assets.C1, (cx, cy), 3)
            pygame.draw.circle(game.ekran, assets.C2, (cx-1, cy-1), 1)
    if d == "kar":
        for _ in range(15):
            kx = random.randint(0, assets.GENISLIK); ky = random.randint(0, assets.YUKSEKLIK)
            pygame.draw.circle(game.ekran, assets.KR, (kx, ky), 2)
