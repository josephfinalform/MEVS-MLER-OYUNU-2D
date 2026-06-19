import pygame
import math
import random

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)
GENISLIK = 1200
YUKSEKLIK = 700
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mevsimler Oyunu")
saat = pygame.time.Clock()

# Renkler
B = (255, 255, 255); S = (0, 0, 0); TEN = (255, 210, 180)
PEMBE = (255, 20, 147); NP = (255, 50, 180); MB = (0, 180, 255)
NM = (0, 255, 255); SAC = (255, 100, 200); SG = (200, 50, 150)
GB = (240, 240, 255); GM = (80, 200, 255); GI = (255, 255, 255)
AG = (200, 80, 80); ALTIN = (255, 215, 0); K = (200, 50, 50)
NY = (0, 255, 100); GT = (40, 40, 50); AGT = (60, 60, 75)
C1 = (255, 100, 200); C2 = (255, 255, 100)
DT = (220, 180, 150); DS = (180, 100, 50); DG = (255, 200, 100)
MM = (50, 100, 200); YP = (200, 150, 50); KR = (220, 230, 255)

# Ses - basit yumusak dalga
def ses_yap(f, s, v=0.08):
    sr = 22050
    n = int(sr * s)
    buf = bytearray(n * 2)
    for i in range(n):
        val = int(v * 32767 * math.sin(2 * math.pi * f * i / sr))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))

SESLER = {}
for m, f in [("ilkbahar", 262), ("yaz", 330), ("sonbahar", 196), ("kis", 165)]:
    SESLER[m] = ses_yap(f, 2.0)
sk = pygame.mixer.Channel(0)

# Envanter
KOSTUMLER = {
    "ilkbahar": {"i": "Cicek Taci", "r": C1, "a": "Bahar ciceklerinden tac"},
    "yaz": {"i": "Gunes Gozlugu", "r": ALTIN, "a": "Havali gunes gozlugu"},
    "sonbahar": {"i": "Yaprak Pelerin", "r": YP, "a": "Sonbahar yapragindan pelerin"},
    "kis": {"i": "Kar Taci", "r": KR, "a": "Kar tanelerinden tac"},
}
envanter = []
aktif_k = None

# Mevsimler
MEV = {
    "ilkbahar": {"a": (30, 60, 40), "z": (60, 180, 60), "p": (80, 200, 80), "k": (120, 255, 120), "t": (255, 100, 100), "ac": (40, 80, 50)},
    "yaz": {"a": (50, 70, 60), "z": (200, 180, 60), "p": (220, 200, 80), "k": (255, 230, 120), "t": (255, 80, 50), "ac": (70, 60, 35)},
    "sonbahar": {"a": (50, 30, 30), "z": (180, 100, 40), "p": (200, 120, 50), "k": (255, 160, 80), "t": (200, 50, 50), "ac": (60, 35, 35)},
    "kis": {"a": (30, 40, 60), "z": (180, 200, 220), "p": (180, 200, 220), "k": (220, 240, 255), "t": (100, 150, 200), "ac": (40, 50, 70)},
}

LVL = {
    "ilkbahar": {"z": 1, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "cicek"},
    "yaz": {"z": 2, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "cizgi"},
    "sonbahar": {"z": 3, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "yaprak"},
    "kis": {"z": 4, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "kar"},
}

# Platformlar - daha alcak, daha kolay
def level_hazirla():
    z = GENISLIK; h = YUKSEKLIK
    LVL["ilkbahar"]["p"] = [
        pygame.Rect(0, h-20, z, 20), pygame.Rect(80, h-120, 220, 20),
        pygame.Rect(380, h-220, 200, 20), pygame.Rect(680, h-300, 240, 20),
        pygame.Rect(250, h-380, 200, 20), pygame.Rect(600, h-460, 220, 20),
        pygame.Rect(900, h-520, 220, 20),
    ]
    LVL["ilkbahar"]["pr"] = [(170, h-140), (470, h-240), (790, h-320), (340, h-400), (700, h-480), (990, h-540)]
    LVL["ilkbahar"]["t"] = [pygame.Rect(500, h-40, 40, 20)]
    LVL["ilkbahar"]["dk"] = [(400, h-240)]; LVL["ilkbahar"]["ds"] = [(380, 580)]

    LVL["yaz"]["p"] = [
        pygame.Rect(0, h-20, z, 20), pygame.Rect(50, h-120, 200, 20),
        pygame.Rect(320, h-220, 200, 20), pygame.Rect(620, h-300, 200, 20),
        pygame.Rect(350, h-380, 220, 20), pygame.Rect(700, h-460, 200, 20),
        pygame.Rect(500, h-540, 200, 20),
    ]
    LVL["yaz"]["pr"] = [(140, h-140), (410, h-240), (710, h-320), (450, h-400), (790, h-480), (590, h-560)]
    LVL["yaz"]["t"] = [pygame.Rect(460, h-40, 40, 20), pygame.Rect(700, h-150, 40, 20)]
    LVL["yaz"]["dk"] = [(340, h-240), (720, h-480)]; LVL["yaz"]["ds"] = [(320, 520), (700, 900)]

    LVL["sonbahar"]["p"] = [
        pygame.Rect(0, h-20, z, 20), pygame.Rect(50, h-120, 180, 20),
        pygame.Rect(300, h-210, 180, 20), pygame.Rect(580, h-300, 180, 20),
        pygame.Rect(200, h-380, 180, 20), pygame.Rect(500, h-460, 180, 20),
        pygame.Rect(800, h-520, 200, 20),
    ]
    LVL["sonbahar"]["pr"] = [(140, h-140), (380, h-230), (660, h-320), (280, h-400), (580, h-480), (890, h-540)]
    LVL["sonbahar"]["t"] = [pygame.Rect(200, h-40, 40, 20), pygame.Rect(650, h-60, 40, 20)]
    LVL["sonbahar"]["dk"] = [(320, h-230), (520, h-480)]; LVL["sonbahar"]["ds"] = [(300, 480), (500, 680)]

    LVL["kis"]["p"] = [
        pygame.Rect(0, h-20, z, 20), pygame.Rect(40, h-110, 160, 20),
        pygame.Rect(260, h-200, 160, 20), pygame.Rect(500, h-290, 160, 20),
        pygame.Rect(120, h-370, 160, 20), pygame.Rect(380, h-450, 160, 20),
        pygame.Rect(660, h-520, 160, 20), pygame.Rect(900, h-570, 160, 20),
    ]
    LVL["kis"]["pr"] = [(120, h-130), (330, h-220), (570, h-310), (190, h-390), (450, h-470), (730, h-540), (970, h-590)]
    LVL["kis"]["t"] = [pygame.Rect(150, h-40, 40, 20), pygame.Rect(400, h-150, 40, 20), pygame.Rect(620, h-130, 40, 20)]
    LVL["kis"]["dk"] = [(280, h-220), (400, h-470), (680, h-540)]; LVL["kis"]["ds"] = [(260, 420), (380, 540), (660, 820)]

level_hazirla()

ms = ["ilkbahar", "yaz", "sonbahar", "kis"]
si = 0; mv = ms[0]; rnk = MEV[mv]; lvl = LVL[mv]
ox = 100; oy = YUKSEKLIK - 100
hx = 0; hy = 0; yr = False; yn = 1
yc = 0.5; zg = -13; dhc = 1.0; mc = 5; cn = 5
plt = []; prl = []; tzl = []; dsm = []
ptk = []

yldzlar = [{"x": random.randint(0, GENISLIK), "y": random.randint(0, YUKSEKLIK), "h": random.uniform(0.1, 0.3), "b": random.randint(1, 2)} for _ in range(25)]

f = pygame.font.Font(None, 36); fb = pygame.font.Font(None, 60); fk = pygame.font.Font(None, 24); fm = pygame.font.Font(None, 48)

gs = pygame.Surface((60, 80), pygame.SRCALPHA)
pygame.draw.ellipse(gs, (255, 20, 147, 25), (5, 5, 50, 65))
pygame.draw.ellipse(gs, (255, 50, 180, 40), (10, 10, 40, 55))

ft = False; mk = False

def btn(m, x, y, w, h, n, u, yr=B):
    global ft
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, w, h)
    u2 = r.collidepoint(mx, my)
    # Gölge
    pygame.draw.rect(ekran, (0, 0, 0, 60), (x+3, y+3, w, h), border_radius=8)
    pygame.draw.rect(ekran, u if u2 else n, r, border_radius=8)
    pygame.draw.rect(ekran, yr, r, 2, border_radius=8)
    t = fm.render(m, True, yr)
    ekran.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return u2 and ft

def ikon(x, y, s, rn=B):
    global ft
    mx, my = pygame.mouse.get_pos()
    r = pygame.Rect(x, y, 36, 36)
    u = r.collidepoint(mx, my)
    # İkon daire
    pygame.draw.circle(ekran, AGT if u else GT, (x+18, y+18), 20)
    pygame.draw.circle(ekran, rn, (x+18, y+18), 20, 2)
    if s == "A":
        pygame.draw.circle(ekran, rn, (x+18, y+18), 8, 2)
        pygame.draw.line(ekran, rn, (x+18, y+8), (x+18, y+10), 2)
        pygame.draw.line(ekran, rn, (x+8, y+18), (x+10, y+18), 2)
        pygame.draw.line(ekran, rn, (x+26, y+18), (x+28, y+18), 2)
    elif s == "R":
        pygame.draw.line(ekran, rn, (x+12, y+12), (x+22, y+12), 3)
        pygame.draw.line(ekran, rn, (x+12, y+12), (x+12, y+22), 3)
        pygame.draw.line(ekran, rn, (x+22, y+12), (x+22, y+22), 3)
        pygame.draw.line(ekran, rn, (x+12, y+22), (x+22, y+22), 3)
        pygame.draw.polygon(ekran, rn, [(x+24, y+14), (x+28, y+18), (x+24, y+22)])
    elif s == "M":
        pygame.draw.rect(ekran, rn, (x+10, y+16, 16, 12), 2)
        pygame.draw.polygon(ekran, rn, [(x+9, y+18), (x+18, y+10), (x+27, y+18)])
        pygame.draw.rect(ekran, rn, (x+16, y+22, 4, 6))
    return u and ft

def ptk_ekle(x, y, r, s=8):
    for _ in range(s):
        a = random.uniform(0, math.pi*2)
        h = random.uniform(1, 3)
        ptk.append({"x":x,"y":y,"vx":math.cos(a)*h,"vy":math.sin(a)*h-2,"r":r,"o":random.randint(15,25),"b":random.randint(2,4)})

def lv_yukle(m):
    global mv, rnk, lvl, plt, prl, tzl, dsm, ox, oy, hx, hy, si, mk
    mv = m; rnk = MEV[m]; lvl = LVL[m]
    plt = [r.copy() for r in lvl["p"]]
    prl = lvl["pr"][:]; tzl = [r.copy() for r in lvl["t"]]
    dsm = []
    for i in range(len(lvl["dk"])):
        k = lvl["dk"][i]; s2 = lvl["ds"][i]
        dsm.append({"r": pygame.Rect(k[0], k[1], 30, 40), "h": (0.5+i*0.2)*dhc, "sl": s2[0], "sg": s2[1]})
    ox, oy = 100, YUKSEKLIK-100; hx = hy = 0
    if mk:
        sk.stop(); sk.set_volume(ayar["ses"] / 100)
        sk.play(SESLER[m], -1)

def oy_bas():
    global si, cn, mk
    mc = {"kolay":7,"orta":5,"zor":3}[ayar["z"]]
    cn = mc
    si = 0; lv_yukle(ms[0])

ayar = {"z": "orta", "te": False, "ses": 50}
te_mi = False
z_can = {"kolay":7,"orta":5,"zor":3}
z_dh = {"kolay":0.5,"orta":1.0,"zor":1.5}
z_yc = {"kolay":0.45,"orta":0.5,"zor":0.6}
z_zg = {"kolay":-13,"orta":-13,"zor":-12}

sh = 0; sz = 0; gk = 0

def ciz_krk(x, y, yn, yy=0):
    global sh, sz, gk
    sz += 0.05; gk += 1; y += yy
    sh += (hx*0.3 - sh)*0.15
    iv = pygame.Vector2(math.sin(sz)*2, math.sin(sz*0.6)*0.8)
    sy2 = sh*0.6 + hy*0.3 + iv.x
    ekran.blit(gs, (x-30, y-15))
    for o in range(-16, 18, 4):
        u = 20 + abs(o)*0.5; e = sy2*(1-abs(o)/20)
        pygame.draw.rect(ekran, SG, (x+o+e-2, y-50, 4, 18+u))
    sk2 = max(-8, min(8, sy2))
    pygame.draw.ellipse(ekran, SAC, (x-18+sk2, y-58, 36, 28))
    pygame.draw.ellipse(ekran, SAC, (x-20+sk2*1.5, y-52, 15, 22))
    pygame.draw.ellipse(ekran, SAC, (x+5+sk2*1.5, y-52, 15, 22))
    pygame.draw.ellipse(ekran, TEN, (x-13, y-44, 26, 30))
    pygame.draw.ellipse(ekran, TEN, (x-15, y-40, 12, 18))
    pygame.draw.ellipse(ekran, TEN, (x+3, y-40, 12, 18))
    ga = gk % 180 > 5
    if ga:
        pygame.draw.ellipse(ekran, GB, (x-11, y-38, 12, 14))
        pygame.draw.ellipse(ekran, GB, (x-1, y-38, 12, 14))
        pygame.draw.ellipse(ekran, GM, (x-9, y-36, 8, 10))
        pygame.draw.ellipse(ekran, GM, (x+1, y-36, 8, 10))
        pygame.draw.circle(ekran, GI, (x-5, y-33), 3)
        pygame.draw.circle(ekran, GI, (x+5, y-33), 3)
        pygame.draw.circle(ekran, S, (x-6, y-33), 2)
        pygame.draw.circle(ekran, S, (x+4, y-33), 2)
    else:
        pygame.draw.line(ekran, S, (x-10, y-31), (x-3, y-31), 2)
        pygame.draw.line(ekran, S, (x+3, y-31), (x+10, y-31), 2)
    if yr and abs(hx)<0.5: pygame.draw.arc(ekran, AG, (x-5, y-28, 10, 8), 0.2, 2.9, 2)
    else: pygame.draw.arc(ekran, AG, (x-4, y-26, 8, 6), 0, 3.14, 2)
    pygame.draw.rect(ekran, TEN, (x-4, y-14, 8, 6))
    nf = math.sin(sz*0.8)*1.5
    pygame.draw.ellipse(ekran, PEMBE, (x-16, y-10+nf, 32, 22))
    pygame.draw.line(ekran, NP, (x, y-8), (x, y+8), 2)
    pygame.draw.line(ekran, NM, (x-8, y-4), (x-8, y+4), 1)
    pygame.draw.line(ekran, NM, (x+8, y-4), (x+8, y+4), 1)
    if aktif_k == "sonbahar":
        pygame.draw.polygon(ekran, YP, [(x-16,y-6),(x-22,y+20),(x-8,y+18)])
        pygame.draw.polygon(ekran, YP, [(x+16,y-6),(x+22,y+20),(x+8,y+18)])
    pygame.draw.rect(ekran, S, (x-16, y+6, 32, 28))
    pygame.draw.rect(ekran, (30,30,40), (x-16, y+6, 32, 28), 1)
    pygame.draw.line(ekran, NM, (x-8, y+8), (x-8, y+32), 2)
    pygame.draw.line(ekran, NP, (x-6, y+10), (x-6, y+30), 1)
    pygame.draw.line(ekran, NM, (x+8, y+8), (x+8, y+32), 2)
    pygame.draw.line(ekran, NP, (x+6, y+10), (x+6, y+30), 1)
    pygame.draw.rect(ekran, PEMBE, (x-17, y+4, 34, 5))
    pygame.draw.rect(ekran, NP, (x-17, y+4, 34, 5), 1)
    if aktif_k == "yaz":
        pygame.draw.circle(ekran, ALTIN, (x-8, y-35), 7, 2)
        pygame.draw.circle(ekran, ALTIN, (x+8, y-35), 7, 2)
        pygame.draw.line(ekran, ALTIN, (x-1, y-35), (x+1, y-35), 2)
    if not yr: ba=0; syk=-6; sagk=-6
    elif abs(hx)>1:
        ba=math.sin(sz*8)*30*(1 if hx>0 else -1)
        syk=abs(math.sin(sz*8))*6; sagk=abs(math.cos(sz*8))*6
    else: ba=iv.x*3; syk=iv.x*0.5; sagk=-iv.x*0.5
    sx=x-9+ba*0.08; gx=x+2-ba*0.08
    pygame.draw.rect(ekran, S, (sx, y+28+syk, 7, 10))
    pygame.draw.rect(ekran, S, (gx, y+28+sagk, 7, 10))
    pygame.draw.rect(ekran, MB, (sx-3, y+36+syk, 14, 10))
    pygame.draw.rect(ekran, MB, (gx-3, y+36+sagk, 14, 10))
    pygame.draw.line(ekran, NM, (sx-1, y+38+syk), (sx+9, y+38+syk), 2)
    pygame.draw.line(ekran, NM, (gx-1, y+38+sagk), (gx+9, y+38+sagk), 2)
    pygame.draw.rect(ekran, NM, (sx-4, y+44+syk, 16, 3))
    pygame.draw.rect(ekran, NM, (gx-4, y+44+sagk, 16, 3))
    if aktif_k == "ilkbahar":
        for i in range(5):
            a=x-12+i*6; pygame.draw.circle(ekran, C1, (a, y-52), 4)
            pygame.draw.circle(ekran, C2, (a, y-52), 2)
    if aktif_k == "kis":
        for i in range(5):
            a=x-12+i*6; pygame.draw.circle(ekran, KR, (a, y-54), 5)
            pygame.draw.circle(ekran, B, (a, y-54), 3)

def dekor_ciz():
    d = lvl.get("d", "")
    if d == "cicek":
        for p in plt[1:]:
            for i in range(p.x+10, p.right-10, 35):
                pygame.draw.circle(ekran, C1, (i, p.top-5), 4)
                pygame.draw.circle(ekran, C2, (i-2, p.top-7), 2)
    if d == "yaprak":
        for p in plt[1:]:
            for i in range(p.x+10, p.right-10, 30):
                pygame.draw.ellipse(ekran, YP, (i, p.top-8, 10, 6))
                pygame.draw.line(ekran, (150,100,30), (i+2, p.top-5), (i+8, p.top-5), 1)
    if d == "kar":
        for p in plt[1:]:
            for i in range(p.x+5, p.right-5, 20):
                pygame.draw.circle(ekran, KR, (i, p.top-4), 3)
                pygame.draw.circle(ekran, B, (i-1, p.top-5), 2)
    if d == "cizgi":
        for p in plt[1:]:
            pygame.draw.line(ekran, ALTIN, (p.x+10, p.top-3), (p.right-10, p.top-3), 2)

def ark_ciz():
    ekran.fill(rnk["a"])
    for y in yldzlar:
        y["y"] += y["h"]
        if y["y"] > YUKSEKLIK: y["y"] = 0; y["x"] = random.randint(0, GENISLIK)
        pygame.draw.circle(ekran, rnk["ac"], (int(y["x"]), int(y["y"])), y["b"])
    for i in range(0, GENISLIK, 100):
        pygame.draw.line(ekran, rnk["ac"], (i, 0), (i, YUKSEKLIK), 1)
    d = lvl.get("d", "")
    if d == "cicek":
        for _ in range(10):
            cx = random.randint(0, GENISLIK); cy = random.randint(0, YUKSEKLIK-100)
            pygame.draw.circle(ekran, C1, (cx, cy), 3)
            pygame.draw.circle(ekran, C2, (cx-1, cy-1), 1)
    if d == "kar":
        for _ in range(15):
            kx = random.randint(0, GENISLIK); ky = random.randint(0, YUKSEKLIK)
            pygame.draw.circle(ekran, KR, (kx, ky), 2)

ma = 0
cal = True
drm = "menu"

def menu_ciz():
    global ma, si
    ma += 0.02
    ekran.fill((15, 15, 35))
    for i in range(0, GENISLIK, 80):
        pygame.draw.line(ekran, (25, 0, 45), (i, 0), (i, YUKSEKLIK), 1)
    for _ in range(30):
        if random.random() < 0.03:
            pygame.draw.circle(ekran, (100, 100, 150), (random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK)), 1)
    t = fb.render("MEVSIMLER", True, NP)
    p = abs(math.sin(ma))*60
    t2 = fb.render("MEVSIMLER", True, (255, int(50+p*0.5), int(180+p*0.3)))
    ekran.blit(t2, (GENISLIK//2 - t.get_width()//2 + 2, 102))
    ekran.blit(t, (GENISLIK//2 - t.get_width()//2, 100))
    a = fk.render("Bir Platform Oyunu", True, NM)
    ekran.blit(a, (GENISLIK//2 - a.get_width()//2, 160))
    if btn("BASLA", GENISLIK//2-120, 250, 240, 55, GT, AGT, NY): si=0; oy_bas(); return "oyun"
    if btn("AYARLAR", GENISLIK//2-120, 325, 240, 55, GT, AGT, NM): return "settings"
    if btn("ENVANTER", GENISLIK//2-120, 400, 240, 55, GT, AGT, ALTIN): return "envanter"
    if btn("CIKIS", GENISLIK//2-120, 475, 240, 55, GT, AGT, K): return "exit"
    return "menu"

def settings_ciz():
    global ayar, te_mi
    ekran.fill((20, 20, 40))
    for i in range(0, GENISLIK, 100):
        pygame.draw.line(ekran, (30, 0, 50), (i, 0), (i, YUKSEKLIK), 1)
    t = fb.render("AYARLAR", True, NM)
    ekran.blit(t, (GENISLIK//2 - t.get_width()//2, 50))
    ekran.blit(f.render("ZORLUK", True, B), (GENISLIK//2-200, 130))
    for i, z in enumerate(["kolay", "orta", "zor"]):
        sx = GENISLIK//2 - 200 + i*140
        s = ayar["z"] == z
        if btn(z.upper(), sx, 165, 120, 40, MM if s else GT, AGT): ayar["z"] = z
    ekran.blit(f.render("TAM EKRAN", True, B), (GENISLIK//2-200, 240))
    td = "ACIK" if te_mi else "KAPALI"
    if btn(td, GENISLIK//2+50, 235, 140, 40, GT, AGT, NY if te_mi else K):
        te_mi = not te_mi; pygame.display.toggle_fullscreen()
    ekran.blit(f.render(f"SES: {ayar['ses']}%", True, B), (GENISLIK//2-200, 310))
    if btn("-", GENISLIK//2+10, 310, 50, 35, GT, AGT): ayar["ses"] = max(0, ayar["ses"]-10)
    sl_x = GENISLIK//2+70; sl_w = 200
    pygame.draw.rect(ekran, GT, (sl_x, 325, sl_w, 10))
    pygame.draw.rect(ekran, NM, (sl_x, 325, int(sl_w*ayar["ses"]/100), 10))
    if pygame.Rect(sl_x, 315, sl_w, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        ayar["ses"] = max(0, min(100, int((pygame.mouse.get_pos()[0]-sl_x)/sl_w*100)))
    if btn("+", sl_x+sl_w+10, 310, 50, 35, GT, AGT): ayar["ses"] = min(100, ayar["ses"]+10)
    ekran.blit(f.render("KONTROLLER", True, B), (GENISLIK//2-200, 380))
    for i, k in enumerate(["OK SAG/SOL - Hareket", "SPACE - Zipla", "ESC - Menuye don", "R - Yeniden baslat"]):
        ekran.blit(fk.render(k, True, AGT), (GENISLIK//2-200, 415+i*25))
    if btn("GERI", GENISLIK//2-100, 550, 200, 50, GT, AGT, NP): return "menu"
    return "settings"

def env_ciz():
    global aktif_k
    ekran.fill((20, 20, 40))
    for i in range(0, GENISLIK, 100):
        pygame.draw.line(ekran, (30, 0, 50), (i, 0), (i, YUKSEKLIK), 1)
    t = fb.render("ENVANTER", True, ALTIN)
    ekran.blit(t, (GENISLIK//2 - t.get_width()//2, 50))
    if not envanter:
        ekran.blit(f.render("Henuz kostumun yok!", True, AGT), (GENISLIK//2-120, 200))
        ekran.blit(f.render("Mevsimleri tamamlayarak kostum kazan.", True, AGT), (GENISLIK//2-180, 240))
    else:
        for i, k in enumerate(envanter):
            kx = GENISLIK//2-200 + (i%2)*220
            ky = 130 + (i//2)*120
            kr2 = pygame.Rect(kx, ky, 200, 100)
            s = aktif_k == k
            pygame.draw.rect(ekran, MM if s else GT, kr2, border_radius=8)
            pygame.draw.rect(ekran, ALTIN if s else AGT, kr2, 2, border_radius=8)
            ekran.blit(f.render(KOSTUMLER[k]["i"], True, B), (kx+10, ky+10))
            ekran.blit(fk.render(KOSTUMLER[k]["a"], True, AGT), (kx+10, ky+45))
            if kr2.collidepoint(pygame.mouse.get_pos()) and ft:
                aktif_k = k if aktif_k != k else None
    if btn("GERI", GENISLIK//2-100, 580, 200, 50, GT, AGT, NP): return "menu"
    return "envanter"

# Ana döngü
while cal:
    ft = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cal = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: ft = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if drm == "oyun": drm = "settings"
                elif drm in ("settings","envanter"): drm = "menu"; sk.stop()
            if drm == "oyun":
                if event.key == pygame.K_SPACE and yr:
                    hy = zg; ptk_ekle(ox, oy+20, NM, 5)
                if event.key == pygame.K_r and cn <= 0:
                    cn = mc; lv_yukle(mv)

    if drm == "menu":
        drm = menu_ciz()
    elif drm == "settings":
        drm = settings_ciz()
    elif drm == "envanter":
        drm = env_ciz()
    elif drm == "oyun":
        # Zorluk ayarlarını uygula
        yc = z_yc[ayar["z"]]
        zg = z_zg[ayar["z"]]
        dhc = z_dh[ayar["z"]]
        mc = z_can[ayar["z"]]

        pn = len(lvl["pr"]) - len(prl)
        ts = pygame.key.get_pressed()
        hx = (ts[pygame.K_RIGHT] - ts[pygame.K_LEFT]) * 5
        if ts[pygame.K_RIGHT]: yn = 1
        elif ts[pygame.K_LEFT]: yn = -1

        oc = pygame.Rect(ox-14, oy-50, 28, 75)
        oy2 = oy

        ox += hx; oc.x = ox-14
        for p in plt:
            if oc.colliderect(p):
                if hx > 0: oc.right = p.left; ox = oc.x+14
                elif hx < 0: oc.left = p.right; ox = oc.x+14

        hy += yc; oy += hy
        oc.x = ox-14; oc.y = oy-50

        yr = False
        for p in plt:
            if oc.colliderect(p):
                if hy > 0:
                    if not yr and oy2 < p.top: ptk_ekle(ox, p.top, rnk["z"], 4)
                    oc.bottom = p.top; oy = oc.y+50; hy = 0; yr = True
                elif hy < 0: oc.top = p.bottom; oy = oc.y+50; hy = 0

        for pr in prl[:]:
            if oc.colliderect(pygame.Rect(pr[0]-10, pr[1]-10, 20, 20)):
                prl.remove(pr); ptk_ekle(pr[0], pr[1], ALTIN, 10)

        for t in tzl:
            if oc.colliderect(t):
                cn -= 1; ptk_ekle(ox, oy, K, 12)
                ox, oy = 100, YUKSEKLIK-100; hx = hy = 0; break

        for d in dsm:
            d["r"].x += d["h"]
            if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]: d["h"] *= -1
            if oc.colliderect(d["r"]):
                cn -= 1; ptk_ekle(ox, oy, K, 12)
                ox, oy = 100, YUKSEKLIK-100; hx = hy = 0

        if ox < 14: ox = 14
        if ox > GENISLIK-14: ox = GENISLIK-14
        if oy > YUKSEKLIK+50:
            cn -= 1; ox, oy = 100, YUKSEKLIK-100; hx = hy = 0

        if len(prl) == 0 and cn > 0:
            if si < len(ms)-1:
                ptk_ekle(GENISLIK//2, YUKSEKLIK//2, NM, 20)
                ptk_ekle(GENISLIK//2, YUKSEKLIK//2, ALTIN, 12)
                od = ms[si]
                if od not in envanter: envanter.append(od)
                si += 1; lv_yukle(ms[si]); cn = mc
            else:
                od = ms[-1]
                if od not in envanter: envanter.append(od)

        for p in ptk[:]:
            p["x"] += p["vx"]; p["y"] += p["vy"]
            p["vy"] += 0.1; p["o"] -= 1
            if p["o"] <= 0: ptk.remove(p)

        ark_ciz()
        for p in plt:
            pygame.draw.rect(ekran, rnk["p"], p)
            pygame.draw.rect(ekran, rnk["k"], p, 2)
        dekor_ciz()
        for pr in prl:
            pygame.draw.circle(ekran, ALTIN, (pr[0], pr[1]), 10)
            pygame.draw.circle(ekran, (255,200,0), (pr[0], pr[1]), 7)
            pygame.draw.circle(ekran, B, (pr[0]-3, pr[1]-3), 3)
        for t in tzl:
            pygame.draw.polygon(ekran, K, [(t.left,t.bottom),(t.left+20,t.top),(t.left+40,t.bottom)])
            pygame.draw.polygon(ekran, rnk["k"], [(t.left,t.bottom),(t.left+20,t.top),(t.left+40,t.bottom)], 2)

        for d in dsm:
            r = d["r"]; cx = r.x+15; cy = r.y+20
            pygame.draw.line(ekran, S, (cx-5, cy+10), (cx-8, cy+20), 3)
            pygame.draw.line(ekran, S, (cx+5, cy+10), (cx+8, cy+20), 3)
            pygame.draw.rect(ekran, (80,50,20), (cx-11, cy+18, 8, 5))
            pygame.draw.rect(ekran, (80,50,20), (cx+3, cy+18, 8, 5))
            pygame.draw.polygon(ekran, (40,160,40), [(cx,cy-16),(cx-14,cy+12),(cx+14,cy+12)])
            pygame.draw.polygon(ekran, (80,220,80), [(cx,cy-16),(cx-14,cy+12),(cx+14,cy+12)], 2)
            pygame.draw.line(ekran, DT, (cx-14, cy-4), (cx-18, cy+8), 3)
            pygame.draw.line(ekran, DT, (cx+14, cy-4), (cx+18, cy+8), 3)
            pygame.draw.line(ekran, (140,90,40), (cx-14, cy-2), (cx-20, cy-12), 3)
            pygame.draw.line(ekran, (180,130,50), (cx-14, cy-2), (cx-22, cy+2), 3)
            pygame.draw.circle(ekran, DT, (cx, cy-12), 9)
            for i in range(-7, 8, 3):
                pygame.draw.line(ekran, DS, (cx+i, cy-20), (cx+i, cy-12), 3)
            pygame.draw.circle(ekran, DG, (cx-4, cy-14), 2)
            pygame.draw.circle(ekran, DG, (cx+4, cy-14), 2)
            pygame.draw.circle(ekran, S, (cx-5, cy-14), 1)
            pygame.draw.circle(ekran, S, (cx+3, cy-14), 1)
            pygame.draw.line(ekran, (180,100,50), (cx-7, cy-17), (cx-2, cy-16), 2)
            pygame.draw.line(ekran, (180,100,50), (cx+7, cy-17), (cx+2, cy-16), 2)
            pygame.draw.rect(ekran, (200,180,50), (cx-4, cy, 8, 5))

        for p in ptk:
            a = max(0, min(255, p["o"]*12))
            s2 = pygame.Surface((p["b"]*2, p["b"]*2), pygame.SRCALPHA)
            pygame.draw.circle(s2, (*p["r"], a), (p["b"], p["b"]), p["b"])
            ekran.blit(s2, (p["x"]-p["b"], p["y"]-p["b"]))

        yy = abs(math.sin(sz*2))*1.2 if yr and abs(hx)<0.5 else 0
        ciz_krk(ox, oy, yn, yy)

        # UI
        if ikon(GENISLIK-130, 10, "A", NM): drm = "settings"
        if ikon(GENISLIK-86, 10, "R", NY): cn = mc; lv_yukle(mv)
        if ikon(GENISLIK-42, 10, "M", K): drm = "menu"; sk.stop()

        bw = 200
        pygame.draw.rect(ekran, (60,0,0), (GENISLIK-bw-20, 55, bw, 20))
        co = cn/mc
        pygame.draw.rect(ekran, (0,255,100) if co>0.5 else (255,255,0) if co>0.25 else (255,50,50),
                         (GENISLIK-bw-20, 55, int(bw*co), 20))
        pygame.draw.rect(ekran, B, (GENISLIK-bw-20, 55, bw, 20), 2)
        ekran.blit(fk.render("CAN", True, B), (GENISLIK-bw-60, 57))
        ekran.blit(fk.render(f"{mv.upper()} - Zorluk: {lvl['z']}/4", True, B), (GENISLIK//2-80, 12))
        ekran.blit(f.render(f"Puan: {pn}/{len(lvl['pr'])}", True, NP), (10, 10))
        ekran.blit(fk.render("ESC: Men", True, AGT), (10, YUKSEKLIK-30))

        if cn <= 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,180))
            ekran.blit(k2, (0,0))
            ekran.blit(fb.render("OYUN BITTI", True, K), (GENISLIK//2-120, YUKSEKLIK//2-70))
            ekran.blit(f.render("R ile yeniden basla", True, B), (GENISLIK//2-110, YUKSEKLIK//2))
            if btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NM):
                drm = "menu"; sk.stop()

        if len(prl) == 0 and cn > 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,140))
            ekran.blit(k2, (0,0))
            if si < len(ms)-1:
                ekran.blit(fb.render(f"{mv.upper()} GECTIN!", True, NY),
                           (GENISLIK//2-150, YUKSEKLIK//2-60))
                ekran.blit(f.render(f"Sirada: {ms[si].upper()}", True, B),
                           (GENISLIK//2-100, YUKSEKLIK//2))
                ekran.blit(fk.render(f"Odul: {KOSTUMLER[ms[si-1]]['i']} kazanildi!", True, ALTIN),
                           (GENISLIK//2-120, YUKSEKLIK//2+35))
            else:
                ekran.blit(fb.render("TUM MEVSIMLERI GECTIN!", True, ALTIN),
                           (GENISLIK//2-240, YUKSEKLIK//2-60))
                ekran.blit(f.render("Tebrikler! Oyun bitti.", True, B),
                           (GENISLIK//2-100, YUKSEKLIK//2))
                ekran.blit(fk.render(f"Odul: {KOSTUMLER[ms[-1]]['i']} kazanildi!", True, ALTIN),
                           (GENISLIK//2-120, YUKSEKLIK//2+35))
                if btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+80, 200, 50, GT, AGT, NM):
                    drm = "menu"; sk.stop()

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
