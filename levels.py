import pygame
import assets
import game
import particles

LVL = {
    "ilkbahar": {"z": 1, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "cicek"},
    "yaz": {"z": 2, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "cizgi"},
    "sonbahar": {"z": 3, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "yaprak"},
    "kis": {"z": 4, "p": [], "pr": [], "t": [], "dk": [], "ds": [], "d": "kar"},
}

def level_hazirla():
    z = assets.GENISLIK; h = assets.YUKSEKLIK
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

def lv_yukle(m):
    game.mv = m; game.rnk = assets.MEV[m]; game.lvl = LVL[m]
    game.plt = [r.copy() for r in LVL[m]["p"]]
    game.prl = LVL[m]["pr"][:]; game.tzl = [r.copy() for r in LVL[m]["t"]]
    game.dsm = []
    for i in range(len(LVL[m]["dk"])):
        k = LVL[m]["dk"][i]; s2 = LVL[m]["ds"][i]
        game.dsm.append({"r": pygame.Rect(k[0], k[1], 30, 40), "h": (0.5+i*0.2)*game.dhc, "sl": s2[0], "sg": s2[1]})
    game.ox, game.oy = 100, assets.YUKSEKLIK-100; game.hx = game.hy = 0
    if game.mk:
        import audio
        audio.sk.stop(); audio.sk.set_volume(game.ayar["ses"] / 100)
        audio.sk.play(audio.SESLER[m], -1)

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
    pygame.draw.line(game.ekran, assets.S, (cx-5, cy+10), (cx-8, cy+20), 3)
    pygame.draw.line(game.ekran, assets.S, (cx+5, cy+10), (cx+8, cy+20), 3)
    pygame.draw.rect(game.ekran, (80,50,20), (cx-11, cy+18, 8, 5))
    pygame.draw.rect(game.ekran, (80,50,20), (cx+3, cy+18, 8, 5))
    pygame.draw.polygon(game.ekran, (40,160,40), [(cx,cy-16),(cx-14,cy+12),(cx+14,cy+12)])
    pygame.draw.polygon(game.ekran, (80,220,80), [(cx,cy-16),(cx-14,cy+12),(cx+14,cy+12)], 2)
    pygame.draw.line(game.ekran, assets.DT, (cx-14, cy-4), (cx-18, cy+8), 3)
    pygame.draw.line(game.ekran, assets.DT, (cx+14, cy-4), (cx+18, cy+8), 3)
    pygame.draw.line(game.ekran, (140,90,40), (cx-14, cy-2), (cx-20, cy-12), 3)
    pygame.draw.line(game.ekran, (180,130,50), (cx-14, cy-2), (cx-22, cy+2), 3)
    pygame.draw.circle(game.ekran, assets.DT, (cx, cy-12), 9)
    for i in range(-7, 8, 3):
        pygame.draw.line(game.ekran, assets.DS, (cx+i, cy-20), (cx+i, cy-12), 3)
    pygame.draw.circle(game.ekran, assets.DG, (cx-4, cy-14), 2)
    pygame.draw.circle(game.ekran, assets.DG, (cx+4, cy-14), 2)
    pygame.draw.circle(game.ekran, assets.S, (cx-5, cy-14), 1)
    pygame.draw.circle(game.ekran, assets.S, (cx+3, cy-14), 1)
    pygame.draw.line(game.ekran, (180,100,50), (cx-7, cy-17), (cx-2, cy-16), 2)
    pygame.draw.line(game.ekran, (180,100,50), (cx+7, cy-17), (cx+2, cy-16), 2)
    pygame.draw.rect(game.ekran, (200,180,50), (cx-4, cy, 8, 5))
