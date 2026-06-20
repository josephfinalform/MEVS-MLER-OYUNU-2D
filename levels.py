import pygame
import assets
import game
import particles

LVL = {}

def level_hazirla():
    z = assets.GENISLIK; h = assets.YUKSEKLIK

    for sezon in assets.MS:
        LVL[sezon] = {"z": assets.MS.index(sezon)+1, "d": sezon, "rounds": {}}

    LVL["ilkbahar"]["d"] = "cicek"
    LVL["yaz"]["d"] = "cizgi"
    LVL["sonbahar"]["d"] = "yaprak"
    LVL["kis"]["d"] = "kar"

    # ---- ILKBAHAR ----
    LVL["ilkbahar"]["rounds"][1] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(80, h-120, 220, 20), pygame.Rect(380, h-220, 200, 20),
              pygame.Rect(680, h-320, 200, 20), pygame.Rect(250, h-400, 180, 20)],
        "pr": [(170, h-140), (470, h-240), (770, h-340), (330, h-420)],
        "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [(700, h-350, "cift_zipla")],
        "wp": [(400, h-250)],
        "cp": (190, h-145),
    }
    LVL["ilkbahar"]["rounds"][2] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(50, h-120, 200, 20), pygame.Rect(320, h-220, 200, 20),
              pygame.Rect(620, h-300, 200, 20), pygame.Rect(350, h-380, 180, 20), pygame.Rect(700, h-460, 180, 20)],
        "pr": [(140, h-140), (410, h-240), (710, h-320), (440, h-400), (780, h-480)],
        "t": [pygame.Rect(500, h-40, 40, 20)], "dk": [(340, h-240)], "ds": [(320, 480)],
        "mp": [{"x": 700, "y": h-160, "w": 120, "h": 16, "dx": 100, "dy": 0, "spd": 1.5}],
        "pu": [(450, h-410, "kalkan")],
        "wp": [(600, h-330)],
        "cp": (150, h-145),
    }
    LVL["ilkbahar"]["rounds"][3] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(80, h-120, 180, 20), pygame.Rect(340, h-210, 180, 20),
              pygame.Rect(560, h-300, 180, 20), pygame.Rect(200, h-380, 180, 20), pygame.Rect(500, h-450, 160, 20),
              pygame.Rect(800, h-520, 180, 20)],
        "pr": [(160, h-140), (420, h-230), (640, h-320), (280, h-400), (570, h-470), (880, h-540)],
        "t": [pygame.Rect(400, h-40, 40, 20), pygame.Rect(650, h-60, 40, 20)],
        "dk": [(320, h-230), (520, h-470)], "ds": [(300, 460), (500, 660)],
        "mp": [{"x": 400, "y": h-300, "w": 120, "h": 16, "dx": 0, "dy": 80, "spd": 1.0},
               {"x": 250, "y": h-100, "w": 100, "h": 16, "dx": 120, "dy": 0, "spd": 2.0}],
        "pu": [(700, h-540, "miknatis")],
        "wp": [(350, h-240)],
        "cp": (170, h-145),
    }
    LVL["ilkbahar"]["rounds"][4] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(0, h-160, 300, 20), pygame.Rect(z-300, h-160, 300, 20),
              pygame.Rect(z//2-100, h-260, 200, 20), pygame.Rect(100, h-350, 180, 20),
              pygame.Rect(z-280, h-350, 180, 20), pygame.Rect(z//2-60, h-440, 120, 20)],
        "pr": [], "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [], "wp": [], "cp": (150, h-155),
        "boss": {"hp": 10, "atk": 60},
    }

    # ---- YAZ ----
    LVL["yaz"]["rounds"][1] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(100, h-130, 200, 20), pygame.Rect(400, h-230, 200, 20),
              pygame.Rect(700, h-330, 180, 20), pygame.Rect(300, h-420, 160, 20)],
        "pr": [(190, h-150), (490, h-250), (780, h-350), (370, h-440)],
        "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [(600, h-360, "cift_zipla")],
        "wp": [(800, h-380)],
        "cp": (200, h-145),
    }
    LVL["yaz"]["rounds"][2] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(50, h-120, 180, 20), pygame.Rect(300, h-220, 180, 20),
              pygame.Rect(550, h-310, 180, 20), pygame.Rect(250, h-400, 160, 20), pygame.Rect(600, h-480, 180, 20)],
        "pr": [(130, h-140), (380, h-240), (630, h-330), (320, h-420), (680, h-500)],
        "t": [pygame.Rect(700, h-40, 40, 20)], "dk": [(350, h-240)], "ds": [(320, 500)],
        "mp": [{"x": 500, "y": h-160, "w": 100, "h": 16, "dx": 120, "dy": 0, "spd": 2.0}],
        "pu": [(400, h-430, "hiz")],
        "wp": [(550, h-340)],
        "cp": (140, h-145),
    }
    LVL["yaz"]["rounds"][3] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(60, h-110, 160, 20), pygame.Rect(280, h-200, 160, 20),
              pygame.Rect(520, h-290, 160, 20), pygame.Rect(180, h-370, 160, 20), pygame.Rect(450, h-450, 160, 20),
              pygame.Rect(750, h-520, 180, 20)],
        "pr": [(140, h-130), (350, h-220), (590, h-310), (250, h-390), (520, h-470), (830, h-540)],
        "t": [pygame.Rect(300, h-40, 40, 20), pygame.Rect(550, h-50, 40, 20)],
        "dk": [(300, h-220), (500, h-470)], "ds": [(280, 440), (450, 640)],
        "mp": [{"x": 350, "y": h-300, "w": 120, "h": 16, "dx": 0, "dy": 70, "spd": 1.2},
               {"x": 650, "y": h-150, "w": 100, "h": 16, "dx": 100, "dy": 0, "spd": 1.8}],
        "pu": [(550, h-500, "kalkan")],
        "wp": [(400, h-240)],
        "cp": (140, h-145),
    }
    LVL["yaz"]["rounds"][4] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(0, h-160, 280, 20), pygame.Rect(z-280, h-160, 280, 20),
              pygame.Rect(z//2-100, h-260, 200, 20), pygame.Rect(80, h-350, 160, 20),
              pygame.Rect(z-240, h-350, 160, 20), pygame.Rect(z//2-50, h-440, 100, 20)],
        "pr": [], "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [], "wp": [], "cp": (140, h-155),
        "boss": {"hp": 12, "atk": 50},
    }

    # ---- SONBAHAR ----
    LVL["sonbahar"]["rounds"][1] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(120, h-140, 180, 20), pygame.Rect(400, h-240, 180, 20),
              pygame.Rect(700, h-340, 180, 20), pygame.Rect(300, h-430, 160, 20)],
        "pr": [(200, h-160), (480, h-260), (780, h-360), (370, h-450)],
        "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [(550, h-370, "miknatis")],
        "wp": [(800, h-390)],
        "cp": (210, h-145),
    }
    LVL["sonbahar"]["rounds"][2] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(80, h-120, 160, 20), pygame.Rect(300, h-220, 160, 20),
              pygame.Rect(540, h-310, 160, 20), pygame.Rect(200, h-390, 160, 20), pygame.Rect(500, h-470, 160, 20)],
        "pr": [(150, h-140), (370, h-240), (610, h-330), (270, h-410), (570, h-490)],
        "t": [pygame.Rect(450, h-40, 40, 20)], "dk": [(340, h-240)], "ds": [(300, 480)],
        "mp": [{"x": 600, "y": h-170, "w": 100, "h": 16, "dx": 80, "dy": 0, "spd": 1.5}],
        "pu": [(350, h-420, "kalkan")],
        "wp": [(550, h-340)],
        "cp": (160, h-145),
    }
    LVL["sonbahar"]["rounds"][3] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(40, h-110, 140, 20), pygame.Rect(240, h-200, 140, 20),
              pygame.Rect(460, h-290, 140, 20), pygame.Rect(140, h-370, 140, 20), pygame.Rect(380, h-450, 140, 20),
              pygame.Rect(640, h-520, 160, 20)],
        "pr": [(110, h-130), (300, h-220), (520, h-310), (200, h-390), (440, h-470), (710, h-540)],
        "t": [pygame.Rect(250, h-40, 40, 20), pygame.Rect(500, h-50, 40, 20)],
        "dk": [(280, h-220), (420, h-470)], "ds": [(240, 420), (380, 580)],
        "mp": [{"x": 300, "y": h-300, "w": 100, "h": 16, "dx": 0, "dy": 60, "spd": 1.5},
               {"x": 500, "y": h-150, "w": 100, "h": 16, "dx": 90, "dy": 0, "spd": 2.0}],
        "pu": [(600, h-540, "hiz")],
        "wp": [(350, h-240)],
        "cp": (110, h-145),
    }
    LVL["sonbahar"]["rounds"][4] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(0, h-160, 260, 20), pygame.Rect(z-260, h-160, 260, 20),
              pygame.Rect(z//2-100, h-260, 200, 20), pygame.Rect(60, h-350, 160, 20),
              pygame.Rect(z-220, h-350, 160, 20), pygame.Rect(z//2-50, h-440, 100, 20)],
        "pr": [], "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [], "wp": [], "cp": (130, h-155),
        "boss": {"hp": 15, "atk": 45},
    }

    # ---- KIS ----
    LVL["kis"]["rounds"][1] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(80, h-130, 180, 20), pygame.Rect(360, h-230, 180, 20),
              pygame.Rect(640, h-330, 180, 20), pygame.Rect(260, h-420, 160, 20)],
        "pr": [(160, h-150), (440, h-250), (720, h-350), (330, h-440)],
        "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [(500, h-360, "cift_zipla")],
        "wp": [(750, h-380)],
        "cp": (170, h-145),
    }
    LVL["kis"]["rounds"][2] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(60, h-120, 160, 20), pygame.Rect(280, h-210, 160, 20),
              pygame.Rect(520, h-300, 160, 20), pygame.Rect(220, h-380, 160, 20), pygame.Rect(560, h-460, 160, 20)],
        "pr": [(130, h-140), (350, h-230), (590, h-320), (290, h-400), (630, h-480)],
        "t": [pygame.Rect(400, h-40, 40, 20)], "dk": [(320, h-230)], "ds": [(280, 460)],
        "mp": [{"x": 500, "y": h-160, "w": 100, "h": 16, "dx": 90, "dy": 0, "spd": 1.8}],
        "pu": [(400, h-410, "hiz")],
        "wp": [(600, h-330)],
        "cp": (140, h-145),
    }
    LVL["kis"]["rounds"][3] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(40, h-110, 140, 20), pygame.Rect(220, h-200, 140, 20),
              pygame.Rect(440, h-290, 140, 20), pygame.Rect(120, h-370, 140, 20), pygame.Rect(360, h-450, 140, 20),
              pygame.Rect(620, h-520, 160, 20)],
        "pr": [(100, h-130), (280, h-220), (500, h-310), (180, h-390), (420, h-470), (690, h-540)],
        "t": [pygame.Rect(200, h-40, 40, 20), pygame.Rect(600, h-50, 40, 20)],
        "dk": [(260, h-220), (400, h-470)], "ds": [(220, 400), (360, 560)],
        "mp": [{"x": 300, "y": h-300, "w": 100, "h": 16, "dx": 0, "dy": 60, "spd": 1.8},
               {"x": 450, "y": h-120, "w": 100, "h": 16, "dx": 80, "dy": 0, "spd": 2.2}],
        "pu": [(500, h-540, "kalkan")],
        "wp": [(280, h-230)],
        "cp": (110, h-145),
    }
    LVL["kis"]["rounds"][4] = {
        "p": [pygame.Rect(0, h-20, z, 20), pygame.Rect(0, h-160, 240, 20), pygame.Rect(z-240, h-160, 240, 20),
              pygame.Rect(z//2-100, h-260, 200, 20), pygame.Rect(50, h-350, 150, 20),
              pygame.Rect(z-200, h-350, 150, 20), pygame.Rect(z//2-50, h-440, 100, 20)],
        "pr": [], "t": [], "dk": [], "ds": [], "mp": [],
        "pu": [], "wp": [], "cp": (120, h-155),
        "boss": {"hp": 18, "atk": 40},
    }

level_hazirla()

def lv_yukle(m, rnd=1):
    game.mv = m; game.rnk = assets.MEV[m]
    game.rnd = rnd
    rd = LVL[m]["rounds"][rnd].copy()
    rd["d"] = LVL[m].get("d", "")
    rd["z"] = LVL[m].get("z", 1)
    game.lvl = rd
    game.plt = [r.copy() for r in rd["p"]]
    game.prl = rd["pr"][:]
    game.tzl = [r.copy() for r in rd["t"]]
    game.dsm = []
    game.mpl = []
    game.bullets = []
    game.boss_btl = []

    for i in range(len(rd["dk"])):
        k = rd["dk"][i]; s2 = rd["ds"][i]
        game.dsm.append({"r": pygame.Rect(k[0], k[1], 30, 40), "h": (0.5+i*0.2)*game.dhc, "sl": s2[0], "sg": s2[1]})

    for mp in rd.get("mp", []):
        r = pygame.Rect(mp["x"], mp["y"], mp["w"], mp["h"])
        game.mpl.append({"r": r, "bx": mp["x"], "by": mp["y"], "dx": mp["dx"], "dy": mp["dy"], "spd": mp["spd"], "t": 0})

    cp = rd.get("cp", (100, assets.YUKSEKLIK-100))
    game.cp_x, game.cp_y = cp

    game.ox, game.oy = game.cp_x, game.cp_y
    game.hx = game.hy = 0
    game.ammo = 25
    game.weapon = game.mv
    game.rnd_bitti = False
    game.puan = 0
    game.boss_sv = False
    game.boss_hp = 0
    game.boss_max_hp = 0

    if rnd == 4 and "boss" in rd:
        b = rd["boss"]
        zh = assets.BOSS_HP[game.ayar["z"]]
        zp = 1 + (assets.MS.index(m) * 0.5)
        game.boss_sv = True
        game.boss_max_hp = int(b["hp"] * zh / 10 * zp)
        game.boss_hp = game.boss_max_hp
        game.boss_timer = 0
        game.boss_ptrn = 0
        game.boss_dir = 1
        game.boss_vx = assets.BOSS_SPD[game.ayar["z"]]
        game.boss_atk_cd = 0

    if game.mk:
        import audio
        audio.sk.stop(); audio.sk.set_volume(game.ayar["ses"] / 100)
        audio.sk.play(audio.SESLER[m], -1)

    particles.bg_par_baslat()

def dekor_ciz():
    d = game.lvl.get("d", "")
    if d == "cicek":
        for p in game.plt[1:]:
            for i in range(p.x+10, p.right-10, 35):
                pygame.draw.circle(game.ekran, assets.C1, (i, p.top-5), 4)
                pygame.draw.circle(game.ekran, assets.C2, (i-2, p.top-7), 2)
    if d == "yaprak":
        for p in game.plt[1:]:
            for i in range(p.x+10, p.right-10, 30):
                pygame.draw.ellipse(game.ekran, assets.YP, (i, p.top-8, 10, 6))
                pygame.draw.line(game.ekran, (150,100,30), (i+2, p.top-5), (i+8, p.top-5), 1)
    if d == "kar":
        for p in game.plt[1:]:
            for i in range(p.x+5, p.right-5, 20):
                pygame.draw.circle(game.ekran, assets.KR, (i, p.top-4), 3)
                pygame.draw.circle(game.ekran, assets.B, (i-1, p.top-5), 2)
    if d == "cizgi":
        for p in game.plt[1:]:
            pygame.draw.line(game.ekran, assets.ALTIN, (p.x+10, p.top-3), (p.right-10, p.top-3), 2)

def dusman_ciz(d):
    r = d["r"]; cx = r.x+15; cy = r.y+20
    m = game.mv
    S2 = assets.S; KR2 = assets.KR
    if m == "ilkbahar":
        # Mini et yiyen bitki
        pygame.draw.rect(game.ekran, (50, 130, 50), (cx-10, cy+4, 20, 14))
        pygame.draw.rect(game.ekran, (70, 150, 70), (cx-10, cy+4, 20, 14), 1)
        pygame.draw.ellipse(game.ekran, (60, 160, 60), (cx-14, cy-12, 28, 20))
        pygame.draw.ellipse(game.ekran, (80, 180, 80), (cx-14, cy-12, 28, 20), 1)
        pygame.draw.ellipse(game.ekran, (200, 50, 50), (cx-10, cy-6, 20, 12))
        for ti in range(4):
            tx = cx - 8 + ti * 5
            pygame.draw.polygon(game.ekran, (255, 255, 240), [(tx, cy-6), (tx+3, cy-6), (tx+1, cy+1)])
            pygame.draw.polygon(game.ekran, (255, 255, 240), [(tx, cy+4), (tx+3, cy+4), (tx+1, cy-1)])
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx-6, cy-14), 4)
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx+6, cy-14), 4)
        pygame.draw.circle(game.ekran, S2, (cx-4, cy-14), 2)
        pygame.draw.circle(game.ekran, S2, (cx+4, cy-14), 2)
    elif m == "yaz":
        # Mini kum golemi
        pygame.draw.polygon(game.ekran, (180, 150, 100), [(cx-14, cy+14), (cx-10, cy), (cx+10, cy), (cx+14, cy+14)])
        pygame.draw.polygon(game.ekran, (200, 170, 120), [(cx-14, cy+14), (cx-10, cy), (cx+10, cy), (cx+14, cy+14)], 1)
        pygame.draw.circle(game.ekran, (190, 160, 110), (cx, cy-4), 12)
        pygame.draw.circle(game.ekran, (210, 180, 130), (cx, cy-4), 12, 1)
        pygame.draw.circle(game.ekran, (255, 200, 50), (cx-5, cy-8), 4)
        pygame.draw.circle(game.ekran, (255, 200, 50), (cx+5, cy-8), 4)
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx-5, cy-8), 2)
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx+5, cy-8), 2)
        pygame.draw.line(game.ekran, (100, 70, 30), (cx-6, cy+2), (cx+6, cy+2), 2)
        # Kucuk kum taneleri
        for gi in range(3):
            pygame.draw.circle(game.ekran, (220, 200, 160), (cx-10+gi*10, cy+8+gi*2), 1)
    elif m == "sonbahar":
        # Mini wither iskelet
        pygame.draw.rect(game.ekran, (25, 20, 15), (cx-8, cy+2, 16, 18))
        pygame.draw.rect(game.ekran, (45, 35, 25), (cx-8, cy+2, 16, 18), 1)
        for ri in range(2):
            pygame.draw.line(game.ekran, (50, 40, 30), (cx-6, cy+6+ri*6), (cx+6, cy+6+ri*6), 1)
        pygame.draw.rect(game.ekran, (25, 20, 15), (cx-6, cy+20, 5, 10))
        pygame.draw.rect(game.ekran, (25, 20, 15), (cx+1, cy+20, 5, 10))
        pygame.draw.line(game.ekran, (30, 25, 20), (cx-14, cy+4), (cx-8, cy+4), 3)
        pygame.draw.line(game.ekran, (30, 25, 20), (cx+8, cy+4), (cx+14, cy+4), 3)
        pygame.draw.rect(game.ekran, (25, 20, 15), (cx-8, cy-14, 16, 16))
        pygame.draw.rect(game.ekran, (45, 35, 25), (cx-8, cy-14, 16, 16), 1)
        pygame.draw.rect(game.ekran, (60, 10, 60), (cx-6, cy-10, 5, 4))
        pygame.draw.rect(game.ekran, (60, 10, 60), (cx+1, cy-10, 5, 4))
        pygame.draw.rect(game.ekran, (120, 20, 120), (cx-6, cy-10, 5, 4), 1)
        pygame.draw.rect(game.ekran, (120, 20, 120), (cx+1, cy-10, 5, 4), 1)
        pygame.draw.circle(game.ekran, (150, 30, 150), (cx-3, cy-8), 1)
        pygame.draw.circle(game.ekran, (150, 30, 150), (cx+3, cy-8), 1)
        pygame.draw.line(game.ekran, (10, 8, 5), (cx-4, cy-4), (cx+4, cy-4), 1)
        # Solmus yaprak
        pygame.draw.ellipse(game.ekran, (80, 40, 10), (cx-12, cy-12, 5, 3))
        pygame.draw.ellipse(game.ekran, (80, 40, 10), (cx+7, cy-14, 5, 3))
    elif m == "kis":
        # Mini yeti
        pygame.draw.ellipse(game.ekran, (220, 230, 240), (cx-14, cy, 28, 28))
        pygame.draw.ellipse(game.ekran, (240, 245, 255), (cx-10, cy+4, 20, 20))
        pygame.draw.line(game.ekran, (220, 230, 240), (cx-12, cy+4), (cx-24, cy-2), 4)
        pygame.draw.line(game.ekran, (220, 230, 240), (cx+12, cy+4), (cx+24, cy-2), 4)
        pygame.draw.circle(game.ekran, (200, 210, 225), (cx-25, cy-4), 6)
        pygame.draw.circle(game.ekran, (200, 210, 225), (cx+25, cy-4), 6)
        pygame.draw.circle(game.ekran, (230, 235, 245), (cx, cy-6), 10)
        pygame.draw.circle(game.ekran, (240, 245, 255), (cx, cy-6), 10, 1)
        pygame.draw.circle(game.ekran, (150, 30, 30), (cx-4, cy-10), 3)
        pygame.draw.circle(game.ekran, (150, 30, 30), (cx+4, cy-10), 3)
        pygame.draw.circle(game.ekran, (255, 50, 50), (cx-4, cy-10), 1)
        pygame.draw.circle(game.ekran, (255, 50, 50), (cx+4, cy-10), 1)
        pygame.draw.ellipse(game.ekran, (180, 50, 50), (cx-5, cy-4, 10, 5))
        for ti in range(3):
            tx = cx - 4 + ti * 3
            pygame.draw.polygon(game.ekran, (255, 255, 250), [(tx, cy-4), (tx+2, cy-4), (tx+1, cy-1)])
        # Kar efekti
        for si in range(4):
            pygame.draw.circle(game.ekran, KR2, (cx-12+si*8, cy-16+math.sin(game.sz*0.1+si)*3), 1)
