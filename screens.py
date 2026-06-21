import random
import math
import pygame
import assets
import game
import ui
import audio
import save

ma = 0
menu_yildiz = []
menu_krl = []
menu_toz = []

def menu_par_baslat():
    global menu_yildiz, menu_krl, menu_toz
    menu_yildiz = [{"x": random.randint(0, assets.GENISLIK), "y": random.randint(0, assets.YUKSEKLIK), "hiz": random.uniform(0.1, 0.5), "r": random.randint(1, 3), "p": random.uniform(0, 6.28)} for _ in range(50)]
    for i, m in enumerate(["ilkbahar", "yaz", "sonbahar", "kis"]):
        a = i * 1.57 + random.uniform(-0.3, 0.3)
        menu_krl.append({"m": m, "a": a, "r": random.uniform(180, 250), "h": random.uniform(0.005, 0.015)})
    menu_toz = [{"x": random.randint(0, assets.GENISLIK), "y": random.randint(-50, assets.YUKSEKLIK), "hiz": random.uniform(0.3, 1.2), "r": random.randint(1, 3), "renk": random.choice([(200, 180, 120, 30), (180, 200, 100, 25), (220, 200, 150, 35)]), "s": random.uniform(0, 6.28)} for _ in range(40)]

menu_par_baslat()

def menu_ciz():
    global ma, menu_yildiz, menu_krl, menu_toz
    audio.menu_muzik()
    ma += 0.02
    G = assets.GENISLIK
    Y = assets.YUKSEKLIK
    ek = game.ekran
    ek.fill((10, 8, 25))
    for i in range(Y):
        t = i / Y
        r = int(10 + t * 20); g = int(8 + t * 15); b = int(25 + t * 30)
        pygame.draw.line(ek, (r, g, b), (0, i), (G, i))

    for ys in menu_yildiz:
        ys["y"] -= ys["hiz"]
        ys["x"] += math.sin(ys["p"] + ma * 0.5) * 0.3
        if ys["y"] < -5:
            ys["y"] = Y + 5; ys["x"] = random.randint(0, G)
        parlak = int(100 + 155 * (0.5 + 0.5 * math.sin(ma * 2 + ys["p"])))
        pygame.draw.circle(ek, (parlak, parlak, 200), (int(ys["x"]), int(ys["y"])), ys["r"])

    for kr in menu_krl:
        kr["a"] += kr["h"]
        cx = G // 2 + int(math.cos(kr["a"]) * kr["r"])
        cy = 120 + int(math.sin(kr["a"]) * 60)
        renk = {"ilkbahar": (80, 220, 100, 40), "yaz": (255, 220, 60, 40), "sonbahar": (220, 140, 40, 40), "kis": (180, 200, 220, 40)}[kr["m"]]
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(s, renk, (40, 40), 35)
        ek.blit(s, (cx - 40, cy - 40))
        pygame.draw.circle(ek, renk[:3] + (80,), (cx, cy), 38, 2)

    for i in range(0, Y, 40):
        yy = i + math.sin(ma * 0.5 + i * 0.05) * 8
        pygame.draw.line(ek, (30, 80, 40), (0, i), (25 + int(math.sin(ma * 0.3 + i * 0.07) * 15), yy), 3)
        if i % 80 < 5:
            pygame.draw.ellipse(ek, (40, 120, 50), (12 + int(math.sin(ma * 0.2 + i * 0.1) * 5), yy - 10, 16, 8))
    for i in range(0, Y, 40):
        yy = i + math.sin(ma * 0.5 + 2 + i * 0.05) * 8
        pygame.draw.line(ek, (30, 80, 40), (G, i), (G - 25 + int(math.sin(ma * 0.3 + 1 + i * 0.07) * 15), yy), 3)
        if i % 80 < 5:
            pygame.draw.ellipse(ek, (40, 120, 50), (G - 28 + int(math.sin(ma * 0.2 + 1 + i * 0.1) * 5), yy - 10, 16, 8))

    for tz in menu_toz:
        tz["y"] += tz["hiz"]
        tz["x"] += math.sin(tz["s"] + ma) * 0.5
        if tz["y"] > Y + 10:
            tz["y"] = -10; tz["x"] = random.randint(0, G)
        s2 = pygame.Surface((tz["r"] * 4, tz["r"] * 4), pygame.SRCALPHA)
        pygame.draw.circle(s2, tz["renk"], (tz["r"] * 2, tz["r"] * 2), tz["r"])
        ek.blit(s2, (int(tz["x"] - tz["r"] * 2), int(tz["y"] - tz["r"] * 2)))

    pygame.draw.rect(ek, (180, 100, 255, 30), (0, 0, G, Y), 3, border_radius=12)
    for dx, dy in [(3, 3), (5, 5)]:
        ts = game.fb.render("MEVSIMLER", True, (50, 20, 80))
        ek.blit(ts, (G//2 - ts.get_width()//2 + dx, 100 + dy))
    t = game.fb.render("MEVSIMLER", True, assets.NP)
    p = abs(math.sin(ma))*60
    t2 = game.fb.render("MEVSIMLER", True, (255, int(50+p*0.5), int(180+p*0.3)))
    ek.blit(t2, (G//2 - t.get_width()//2 + 2, 102))
    ek.blit(t, (G//2 - t.get_width()//2, 100))
    pygame.draw.line(ek, assets.NP, (G//2 - 150, 145), (G//2 + 150, 145), 2)
    for i in range(4):
        ren = [assets.C1, assets.ALTIN, assets.YP, assets.KR][i]
        x = G//2 - 120 + i * 80
        pygame.draw.circle(ek, ren, (x, 155), 5)
        pygame.draw.circle(ek, assets.B, (x, 155), 5, 1)
    a = game.fk.render("Bir Platform Oyunu", True, assets.NM)
    ek.blit(a, (G//2 - a.get_width()//2, 165))

    y = 240
    p_surf = pygame.Surface((300, 410), pygame.SRCALPHA)
    p_surf.fill((30, 15, 50, 100))
    pygame.draw.rect(p_surf, (80, 40, 120, 120), p_surf.get_rect(), 2, border_radius=12)
    ek.blit(p_surf, (G//2 - 150, y - 15))
    if save.var_mi():
        if ui.btn("DEVAM ET", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.NY):
            save.yukle()
            import levels
            game.cn = assets.z_can[game.ayar["z"]]
            levels.lv_yukle(game.mv, game.rnd)
            return "oyun"
        y += 65
    if ui.btn("BASLA", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.NY if not save.var_mi() else assets.NM):
        save.sil()
        import levels
        game.si = 0; game.envanter = []; game.aktif_k = None; game.yuksek_puan = {}
        game.cn = assets.z_can[game.ayar["z"]]
        levels.lv_yukle(assets.ms[0])
        return "oyun"
    y += 65
    if ui.btn("AYARLAR", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.NM): return "settings"
    y += 65
    if ui.btn("ENVANTER", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.ALTIN): return "envanter"
    y += 65
    if ui.btn("PUAN TABLOSU", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.ALTIN): return "leaderboard"
    y += 65
    if ui.btn("CIKIS", G//2-120, y, 240, 55, assets.GT, assets.AGT, assets.K): return "exit"
    for i in range(G):
        ren = [(80, 220, 100), (255, 220, 60), (220, 140, 40), (180, 200, 220), (80, 220, 100), (255, 220, 60), (220, 140, 40), (180, 200, 220)][(i // 150) % 8]
        pygame.draw.line(ek, ren, (i, Y - 3), (i, Y))
    return "menu"

def settings_ciz():
    ek = game.ekran
    ek.fill((20, 20, 40))
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, assets.YUKSEKLIK), 1)
    t = game.fb.render("AYARLAR", True, assets.NM)
    ek.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 50))
    ek.blit(game.f.render("ZORLUK", True, assets.B), (assets.GENISLIK//2-200, 130))
    for i, z in enumerate(["kolay", "orta", "zor", "imkansiz"]):
        sx = assets.GENISLIK//2 - 280 + i*140
        s = game.ayar["z"] == z
        if ui.btn(z.upper(), sx, 165, 120, 40, assets.MM if s else assets.GT, assets.AGT): game.ayar["z"] = z
    ek.blit(game.f.render("TAM EKRAN", True, assets.B), (assets.GENISLIK//2-200, 240))
    td = "ACIK" if game.te_mi else "KAPALI"
    if ui.btn(td, assets.GENISLIK//2+50, 235, 140, 40, assets.GT, assets.AGT, assets.NY if game.te_mi else assets.K):
        game.te_mi = not game.te_mi; pygame.display.toggle_fullscreen()
    oy = 310
    ek.blit(game.f.render(f"LOBI SES: {game.ayar['lobi_ses']}%", True, assets.B), (assets.GENISLIK//2-200, oy))
    if ui.btn("-", assets.GENISLIK//2+10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["lobi_ses"] = max(0, game.ayar["lobi_ses"]-10); audio.muzik_ses(game.ayar["lobi_ses"]/100)
    sl_x = assets.GENISLIK//2+70; sl_w = 200
    pygame.draw.rect(ek, assets.GT, (sl_x, oy+15, sl_w, 10))
    pygame.draw.rect(ek, assets.NM, (sl_x, oy+15, int(sl_w*game.ayar["lobi_ses"]/100), 10))
    if pygame.Rect(sl_x, oy+5, sl_w, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        game.ayar["lobi_ses"] = max(0, min(100, int((pygame.mouse.get_pos()[0]-sl_x)/sl_w*100)))
        audio.muzik_ses(game.ayar["lobi_ses"]/100)
    if ui.btn("+", sl_x+sl_w+10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["lobi_ses"] = min(100, game.ayar["lobi_ses"]+10); audio.muzik_ses(game.ayar["lobi_ses"]/100)
    oy += 75
    ek.blit(game.f.render(f"OYUN SES: {game.ayar['ses']}%", True, assets.B), (assets.GENISLIK//2-200, oy))
    if ui.btn("-", assets.GENISLIK//2+10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = max(0, game.ayar["ses"]-10)
        audio.sfx_ses_ayarla()
    sl_x = assets.GENISLIK//2+70; sl_w = 200
    pygame.draw.rect(ek, assets.GT, (sl_x, oy+15, sl_w, 10))
    pygame.draw.rect(ek, assets.NM, (sl_x, oy+15, int(sl_w*game.ayar["ses"]/100), 10))
    if pygame.Rect(sl_x, oy+5, sl_w, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        game.ayar["ses"] = max(0, min(100, int((pygame.mouse.get_pos()[0]-sl_x)/sl_w*100)))
        audio.sfx_ses_ayarla()
    if ui.btn("+", sl_x+sl_w+10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = min(100, game.ayar["ses"]+10)
        audio.sfx_ses_ayarla()
    oy += 75
    ek.blit(game.f.render("KONTROLLER", True, assets.B), (assets.GENISLIK//2-200, oy))
    for i, k in enumerate(["OK SAG/SOL - Hareket", "SPACE - Zipla", "SAG TIK - Alev Topu", "ESC - Menuye don", "R - Yeniden baslat"]):
        ek.blit(game.fk.render(k, True, assets.AGT), (assets.GENISLIK//2-200, oy+35+i*25))
    if ui.btn("GERI", assets.GENISLIK//2-100, 620, 200, 50, assets.GT, assets.AGT, assets.NP): return game.onceki_drm or "menu"
    return "settings"

def env_ciz():
    ek = game.ekran
    ek.fill((20, 20, 40))
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, assets.YUKSEKLIK), 1)
    t = game.fb.render("ENVANTER", True, assets.ALTIN)
    ek.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 50))
    if not game.envanter:
        ek.blit(game.f.render("Henuz kostumun yok!", True, assets.AGT), (assets.GENISLIK//2-120, 200))
        ek.blit(game.f.render("Mevsimleri tamamlayarak kostum kazan.", True, assets.AGT), (assets.GENISLIK//2-180, 240))
    else:
        for i, k in enumerate(game.envanter):
            kx = assets.GENISLIK//2-200 + (i%2)*220; ky = 130 + (i//2)*120
            kr2 = pygame.Rect(kx, ky, 200, 100)
            s = game.aktif_k == k
            pygame.draw.rect(ek, assets.MM if s else assets.GT, kr2, border_radius=8)
            pygame.draw.rect(ek, assets.ALTIN if s else assets.AGT, kr2, 2, border_radius=8)
            ek.blit(game.f.render(assets.KOSTUMLER[k]["i"], True, assets.B), (kx+10, ky+10))
            ek.blit(game.fk.render(assets.KOSTUMLER[k]["a"], True, assets.AGT), (kx+10, ky+45))
            r2 = kr2.collidepoint(pygame.mouse.get_pos())
            if s or r2:
                ox2 = kx+170; oy2 = ky+50
                pygame.draw.circle(ek, assets.MM, (ox2, oy2-8), 8)
                pygame.draw.rect(ek, assets.KOSTUMLER[k]["r"], (ox2-6, oy2, 12, 30))
                pygame.draw.circle(ek, assets.KOSTUMLER[k]["r"], (ox2, oy2-10), 6)
            if kr2.collidepoint(pygame.mouse.get_pos()) and game.ft:
                game.aktif_k = k if game.aktif_k != k else None
    if ui.btn("GERI", assets.GENISLIK//2-100, 580, 200, 50, assets.GT, assets.AGT, assets.NP): return "menu"
    return "envanter"

def leaderboard_ciz():
    ek = game.ekran
    ek.fill((20, 20, 40))
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, assets.YUKSEKLIK), 1)
    t = game.fb.render("PUAN TABLOSU", True, assets.ALTIN)
    ek.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 50))
    sirali = sorted(game.yuksek_puan.items(), key=lambda x: x[1], reverse=True)
    if not sirali:
        ek.blit(game.f.render("Henuz puan kaydi yok!", True, assets.AGT), (assets.GENISLIK//2-140, 250))
    else:
        for i, (sezon, p) in enumerate(sirali):
            renk = [(255, 215, 0), (200, 200, 200), (180, 120, 60), (150, 150, 180)][i] if i < 4 else (200, 200, 200)
            sira = f"{i+1}. {sezon.upper()}"
            pyazi = game.fm.render(f"{sira}  -  {p}", True, renk)
            ek.blit(pyazi, (assets.GENISLIK//2 - pyazi.get_width()//2, 150 + i*55))
    if ui.btn("GERI", assets.GENISLIK//2-100, 580, 200, 50, assets.GT, assets.AGT, assets.NP): return "menu"
    return "leaderboard"

def lbl_ciz(m):
    game.ekran.fill((10, 8, 25))
    t = game.fb.render(m, True, assets.NP)
    game.ekran.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 230))
    t2 = game.fk.render("Bir sonraki mevsime geciliyor...", True, assets.NM)
    game.ekran.blit(t2, (assets.GENISLIK//2 - t2.get_width()//2, 280))
