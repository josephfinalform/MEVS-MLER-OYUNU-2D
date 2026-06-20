import math, random, pygame
import assets, game

yldzlar = [{"x": random.randint(0, assets.GENISLIK), "y": random.randint(0, assets.YUKSEKLIK), "h": random.uniform(0.1, 0.3), "b": random.randint(1, 2)} for _ in range(25)]

bg_par = []

def bg_par_baslat():
    global bg_par
    bg_par = []
    m = game.mv
    for _ in range(40):
        if m == "kis":
            bg_par.append({"x": random.randint(0, assets.GENISLIK), "y": random.randint(-50, assets.YUKSEKLIK), "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(0.5, 2), "b": random.randint(1, 3)})
        elif m == "sonbahar":
            bg_par.append({"x": random.randint(0, assets.GENISLIK), "y": random.randint(-50, assets.YUKSEKLIK), "vx": random.uniform(-1, -0.2), "vy": random.uniform(0.3, 1.5), "b": random.randint(2, 4)})
        elif m == "yaz":
            bg_par.append({"x": random.randint(0, assets.GENISLIK), "y": random.randint(-50, assets.YUKSEKLIK), "vx": random.uniform(-2, 2), "vy": random.uniform(0.2, 0.8), "b": random.randint(1, 2)})
        else:
            bg_par.append({"x": random.randint(0, assets.GENISLIK), "y": random.randint(-50, assets.YUKSEKLIK), "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(0.1, 0.5), "b": random.randint(2, 4)})

def ptk_ekle(x, y, r, s=8):
    for _ in range(s):
        a = random.uniform(0, math.pi*2)
        h = random.uniform(1, 3)
        game.ptk.append({"x":x,"y":y,"vx":math.cos(a)*h,"vy":math.sin(a)*h-2,"r":r,"o":random.randint(15,25),"b":random.randint(2,4)})

def ptk_patlatma(x, y, r, s=20, g=5):
    for _ in range(s):
        a = random.uniform(0, math.pi*2)
        h = random.uniform(1, g)
        game.ptk.append({"x":x,"y":y,"vx":math.cos(a)*h,"vy":math.sin(a)*h,"r":r,"o":random.randint(20,35),"b":random.randint(2,6)})

def ptk_birim(x, y, r):
    game.ptk.append({"x":x,"y":y,"vx":random.uniform(-0.5,0.5),"vy":-1,"r":r,"o":20,"b":3})

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
    m = game.mv
    rnk = game.rnk

    game.ekran.fill(rnk["a"])

    # Parallax katmanlari
    if m == "ilkbahar":
        for i in range(0, assets.GENISLIK, 200):
            y2 = 200 + math.sin(i*0.01 + game.sz*0.2) * 30
            pygame.draw.ellipse(game.ekran, (50, 100, 70), (i, y2, 180, 60))
            pygame.draw.ellipse(game.ekran, (60, 120, 80), (i, y2+5, 180, 60), 1)
        for i in range(0, assets.GENISLIK, 150):
            y2 = 350 + math.sin(i*0.02 + game.sz*0.15) * 20
            pygame.draw.ellipse(game.ekran, (70, 150, 80), (i+30, y2, 140, 50))
            pygame.draw.ellipse(game.ekran, (80, 170, 100), (i+30, y2+3, 140, 50), 1)
    elif m == "yaz":
        for i in range(0, assets.GENISLIK, 100):
            h2 = 100 + math.sin(i*0.03 + game.sz*0.1) * 40
            pygame.draw.polygon(game.ekran, (180, 150, 80), [(i, 400+h2), (i+80, 300+h2), (i+160, 400+h2)])
            pygame.draw.polygon(game.ekran, (200, 170, 100), [(i, 400+h2), (i+80, 300+h2), (i+160, 400+h2)], 1)
    elif m == "sonbahar":
        for i in range(0, assets.GENISLIK, 180):
            y2 = 250 + math.sin(i*0.015 + game.sz*0.12) * 25
            pygame.draw.polygon(game.ekran, (100, 60, 30), [(i, 350), (i+90, y2), (i+180, 350)])
            pygame.draw.polygon(game.ekran, (130, 80, 40), [(i, 350), (i+90, y2), (i+180, 350)], 1)
    elif m == "kis":
        for i in range(0, assets.GENISLIK, 250):
            y2 = 300 + math.sin(i*0.02 + game.sz*0.08) * 20
            pygame.draw.polygon(game.ekran, (150, 180, 200), [(i, 400), (i+125, y2), (i+250, 400)])
            pygame.draw.polygon(game.ekran, (180, 200, 220), [(i, 400), (i+125, y2), (i+250, 400)], 1)
    # Hava efektleri (yagmur, kar, yaprak, kum)
    game.hava_efektleri = [h for h in game.hava_efektleri if h["o"] > 0]
    while len(game.hava_efektleri) < 30:
        x2 = random.randint(0, assets.GENISLIK)
        y2 = random.randint(-20, -5)
        if m == "kis":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(0.5, 2), "b": random.randint(1, 3), "o": random.randint(60, 120), "r": assets.KR})
        elif m == "sonbahar":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-1.5, -0.3), "vy": random.uniform(0.3, 1.2), "b": random.randint(2, 4), "o": random.randint(80, 150), "r": assets.YP})
        elif m == "yaz":
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-3, 3), "vy": random.uniform(0.2, 0.8), "b": random.randint(1, 2), "o": random.randint(40, 80), "r": assets.ALTIN})
        else:
            game.hava_efektleri.append({"x": x2, "y": y2, "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(0.3, 1), "b": random.randint(2, 4), "o": random.randint(80, 150), "r": (150, 200, 255)})

    for h in game.hava_efektleri:
        h["x"] += h["vx"]; h["y"] += h["vy"]
        h["o"] -= 1
        if m == "kis":
            s2 = pygame.Surface((h["b"]*2, h["b"]*2), pygame.SRCALPHA)
            pygame.draw.circle(s2, (255, 255, 255, min(200, h["o"]*3)), (h["b"], h["b"]), h["b"])
            game.ekran.blit(s2, (h["x"]-h["b"], h["y"]-h["b"]))
        elif m == "sonbahar":
            d2 = h["x"] * 0.5 + h["y"] * 0.3
            s2 = pygame.Surface((8, 5), pygame.SRCALPHA)
            a2 = min(200, h["o"]*3)
            pygame.draw.ellipse(s2, (200, 150, 50, a2), (0, 0, 8, 5))
            pygame.draw.line(s2, (150, 80, 20, a2), (1, 2), (7, 2), 1)
            game.ekran.blit(s2, (h["x"]-4 + math.sin(d2)*2, h["y"]-2))
        elif m == "yaz":
            pygame.draw.circle(game.ekran, assets.ALTIN, (int(h["x"]), int(h["y"])), h["b"])
        else:
            a2 = min(180, h["o"]*3)
            s2 = pygame.Surface((h["b"]*2+2, h["b"]*2+2), pygame.SRCALPHA)
            for di in range(h["b"]):
                pygame.draw.circle(s2, (100, 200, 255, a2//(di+1)), (h["b"]+1, h["b"]+1), h["b"]-di)
            game.ekran.blit(s2, (h["x"]-h["b"]-1, h["y"]-h["b"]-1))

    # Izgara
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(game.ekran, rnk["ac"], (i, 0), (i, assets.YUKSEKLIK), 1)

    # Dekor
    d = game.lvl.get("d", "")
    if d == "cicek":
        for _ in range(15):
            cx = random.randint(0, assets.GENISLIK)
            cy = random.randint(0, assets.YUKSEKLIK-100)
            pygame.draw.circle(game.ekran, assets.C1, (cx, cy), 3)
            pygame.draw.circle(game.ekran, assets.C2, (cx-1, cy-1), 1)
    if d == "kar":
        for _ in range(20):
            kx = random.randint(0, assets.GENISLIK)
            ky = random.randint(0, assets.YUKSEKLIK)
            pygame.draw.circle(game.ekran, assets.KR, (kx, ky), 2)
