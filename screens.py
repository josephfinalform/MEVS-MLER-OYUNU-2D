import random
import math
import pygame
import assets
import game
import ui
import audio

ma = 0

def menu_ciz():
    global ma
    ma += 0.02
    game.ekran.fill((15, 15, 35))
    for i in range(0, assets.GENISLIK, 80):
        pygame.draw.line(game.ekran, (25, 0, 45), (i, 0), (i, assets.YUKSEKLIK), 1)
    for _ in range(30):
        if random.random() < 0.03:
            pygame.draw.circle(game.ekran, (100, 100, 150), (random.randint(0, assets.GENISLIK), random.randint(0, assets.YUKSEKLIK)), 1)
    t = game.fb.render("MEVSIMLER", True, assets.NP)
    p = abs(math.sin(ma))*60
    t2 = game.fb.render("MEVSIMLER", True, (255, int(50+p*0.5), int(180+p*0.3)))
    game.ekran.blit(t2, (assets.GENISLIK//2 - t.get_width()//2 + 2, 102))
    game.ekran.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 100))
    a = game.fk.render("Bir Platform Oyunu", True, assets.NM)
    game.ekran.blit(a, (assets.GENISLIK//2 - a.get_width()//2, 160))
    if ui.btn("BASLA", assets.GENISLIK//2-120, 250, 240, 55, assets.GT, assets.AGT, assets.NY):
        import levels
        game.si = 0
        game.cn = assets.z_can[game.ayar["z"]]
        levels.lv_yukle(assets.ms[0])
        return "oyun"
    if ui.btn("AYARLAR", assets.GENISLIK//2-120, 325, 240, 55, assets.GT, assets.AGT, assets.NM): return "settings"
    if ui.btn("ENVANTER", assets.GENISLIK//2-120, 400, 240, 55, assets.GT, assets.AGT, assets.ALTIN): return "envanter"
    if ui.btn("CIKIS", assets.GENISLIK//2-120, 475, 240, 55, assets.GT, assets.AGT, assets.K): return "exit"
    return "menu"

def settings_ciz():
    game.ekran.fill((20, 20, 40))
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(game.ekran, (30, 0, 50), (i, 0), (i, assets.YUKSEKLIK), 1)
    t = game.fb.render("AYARLAR", True, assets.NM)
    game.ekran.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 50))
    game.ekran.blit(game.f.render("ZORLUK", True, assets.B), (assets.GENISLIK//2-200, 130))
    for i, z in enumerate(["kolay", "orta", "zor", "imkansiz"]):
        sx = assets.GENISLIK//2 - 280 + i*140
        s = game.ayar["z"] == z
        if ui.btn(z.upper(), sx, 165, 120, 40, assets.MM if s else assets.GT, assets.AGT): game.ayar["z"] = z
    game.ekran.blit(game.f.render("TAM EKRAN", True, assets.B), (assets.GENISLIK//2-200, 240))
    td = "ACIK" if game.te_mi else "KAPALI"
    if ui.btn(td, assets.GENISLIK//2+50, 235, 140, 40, assets.GT, assets.AGT, assets.NY if game.te_mi else assets.K):
        game.te_mi = not game.te_mi; pygame.display.toggle_fullscreen()
    game.ekran.blit(game.f.render(f"SES: {game.ayar['ses']}%", True, assets.B), (assets.GENISLIK//2-200, 310))
    if ui.btn("-", assets.GENISLIK//2+10, 310, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = max(0, game.ayar["ses"]-10)
        audio.sk.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal2.set_volume(game.ayar["ses"]/100)
    sl_x = assets.GENISLIK//2+70; sl_w = 200
    pygame.draw.rect(game.ekran, assets.GT, (sl_x, 325, sl_w, 10))
    pygame.draw.rect(game.ekran, assets.NM, (sl_x, 325, int(sl_w*game.ayar["ses"]/100), 10))
    if pygame.Rect(sl_x, 315, sl_w, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        game.ayar["ses"] = max(0, min(100, int((pygame.mouse.get_pos()[0]-sl_x)/sl_w*100)))
        audio.sk.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal2.set_volume(game.ayar["ses"]/100)
    if ui.btn("+", sl_x+sl_w+10, 310, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = min(100, game.ayar["ses"]+10)
        audio.sk.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal.set_volume(game.ayar["ses"]/100)
        audio.ses_kanal2.set_volume(game.ayar["ses"]/100)
    game.ekran.blit(game.f.render("KONTROLLER", True, assets.B), (assets.GENISLIK//2-200, 380))
    for i, k in enumerate(["OK SAG/SOL - Hareket", "SPACE - Zipla", "SAG TIK - Alev Topu", "ESC - Menuye don", "R - Yeniden baslat"]):
        game.ekran.blit(game.fk.render(k, True, assets.AGT), (assets.GENISLIK//2-200, 415+i*25))
    if ui.btn("GERI", assets.GENISLIK//2-100, 550, 200, 50, assets.GT, assets.AGT, assets.NP): return "menu"
    return "settings"

def env_ciz():
    game.ekran.fill((20, 20, 40))
    for i in range(0, assets.GENISLIK, 100):
        pygame.draw.line(game.ekran, (30, 0, 50), (i, 0), (i, assets.YUKSEKLIK), 1)
    t = game.fb.render("ENVANTER", True, assets.ALTIN)
    game.ekran.blit(t, (assets.GENISLIK//2 - t.get_width()//2, 50))
    if not game.envanter:
        game.ekran.blit(game.f.render("Henuz kostumun yok!", True, assets.AGT), (assets.GENISLIK//2-120, 200))
        game.ekran.blit(game.f.render("Mevsimleri tamamlayarak kostum kazan.", True, assets.AGT), (assets.GENISLIK//2-180, 240))
    else:
        for i, k in enumerate(game.envanter):
            kx = assets.GENISLIK//2-200 + (i%2)*220
            ky = 130 + (i//2)*120
            kr2 = pygame.Rect(kx, ky, 200, 100)
            s = game.aktif_k == k
            pygame.draw.rect(game.ekran, assets.MM if s else assets.GT, kr2, border_radius=8)
            pygame.draw.rect(game.ekran, assets.ALTIN if s else assets.AGT, kr2, 2, border_radius=8)
            game.ekran.blit(game.f.render(assets.KOSTUMLER[k]["i"], True, assets.B), (kx+10, ky+10))
            game.ekran.blit(game.fk.render(assets.KOSTUMLER[k]["a"], True, assets.AGT), (kx+10, ky+45))
            # Karakter onizleme
            r2 = kr2.collidepoint(pygame.mouse.get_pos())
            if s or r2:
                ox2 = kx + 170
                oy2 = ky + 50
                pygame.draw.circle(game.ekran, assets.MM, (ox2, oy2-8), 8)
                pygame.draw.rect(game.ekran, assets.KOSTUMLER[k]["r"], (ox2-6, oy2, 12, 30))
                pygame.draw.circle(game.ekran, assets.KOSTUMLER[k]["r"], (ox2, oy2-10), 6)
            if kr2.collidepoint(pygame.mouse.get_pos()) and game.ft:
                game.aktif_k = k if game.aktif_k != k else None
    if ui.btn("GERI", assets.GENISLIK//2-100, 580, 200, 50, assets.GT, assets.AGT, assets.NP): return "menu"
    return "envanter"
