import random
import math
import pygame

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

from assets import *
import game
import audio
import particles
import ui
import player
import levels
import screens
game.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mevsimler Oyunu")
game.saat = pygame.time.Clock()
game.f = pygame.font.Font(None, 36)
game.fb = pygame.font.Font(None, 60)
game.fk = pygame.font.Font(None, 24)
game.fm = pygame.font.Font(None, 48)

game.mv = ms[0]
game.rnk = MEV[ms[0]]
game.lvl = levels.LVL[ms[0]]
game.oy = YUKSEKLIK - 100
game.cn = 5

cal = True

while cal:
    game.ft = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cal = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: game.ft = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.drm == "oyun": game.drm = "settings"
                elif game.drm in ("settings", "envanter"): game.drm = "menu"; audio.sk.stop()
            if game.drm == "oyun":
                if event.key == pygame.K_SPACE and game.yr:
                    game.hy = game.zg; particles.ptk_ekle(game.ox, game.oy+20, NM, 5)
                if event.key == pygame.K_r and game.cn <= 0:
                    game.cn = game.mc; levels.lv_yukle(game.mv)

    if game.drm == "menu":
        game.drm = screens.menu_ciz()
    elif game.drm == "settings":
        game.drm = screens.settings_ciz()
    elif game.drm == "envanter":
        game.drm = screens.env_ciz()
    elif game.drm == "oyun":
        game.yc = z_yc[game.ayar["z"]]
        game.zg = z_zg[game.ayar["z"]]
        game.dhc = z_dh[game.ayar["z"]]
        game.mc = z_can[game.ayar["z"]]

        pn = len(game.lvl["pr"]) - len(game.prl)
        ts = pygame.key.get_pressed()
        game.hx = (ts[pygame.K_RIGHT] - ts[pygame.K_LEFT]) * 5
        if ts[pygame.K_RIGHT]: game.yn = 1
        elif ts[pygame.K_LEFT]: game.yn = -1

        oc = pygame.Rect(game.ox-14, game.oy-50, 28, 75)
        oy2 = game.oy

        game.ox += game.hx; oc.x = game.ox-14
        for p in game.plt:
            if oc.colliderect(p):
                if game.hx > 0: oc.right = p.left; game.ox = oc.x+14
                elif game.hx < 0: oc.left = p.right; game.ox = oc.x+14

        game.hy += game.yc; game.oy += game.hy
        oc.x = game.ox-14; oc.y = game.oy-50

        game.yr = False
        for p in game.plt:
            if oc.colliderect(p):
                if game.hy > 0:
                    if not game.yr and oy2 < p.top: particles.ptk_ekle(game.ox, p.top, game.rnk["z"], 4)
                    oc.bottom = p.top; game.oy = oc.y+50; game.hy = 0; game.yr = True
                elif game.hy < 0: oc.top = p.bottom; game.oy = oc.y+50; game.hy = 0

        for pr in game.prl[:]:
            if oc.colliderect(pygame.Rect(pr[0]-10, pr[1]-10, 20, 20)):
                game.prl.remove(pr); particles.ptk_ekle(pr[0], pr[1], ALTIN, 10)

        for t in game.tzl:
            if oc.colliderect(t):
                game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                game.ox, game.oy = 100, YUKSEKLIK-100; game.hx = game.hy = 0; break

        for d in game.dsm:
            d["r"].x += d["h"]
            if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]: d["h"] *= -1
            if oc.colliderect(d["r"]):
                game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                game.ox, game.oy = 100, YUKSEKLIK-100; game.hx = game.hy = 0

        if game.ox < 14: game.ox = 14
        if game.ox > GENISLIK-14: game.ox = GENISLIK-14
        if game.oy > YUKSEKLIK+50:
            game.cn -= 1; game.ox, game.oy = 100, YUKSEKLIK-100; game.hx = game.hy = 0

        if len(game.prl) == 0 and game.cn > 0:
            if game.si < len(ms)-1:
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, NM, 20)
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, ALTIN, 12)
                od = ms[game.si]
                if od not in game.envanter: game.envanter.append(od)
                game.si += 1; levels.lv_yukle(ms[game.si]); game.cn = game.mc
            else:
                od = ms[-1]
                if od not in game.envanter: game.envanter.append(od)

        particles.ptk_guncelle()
        particles.ark_ciz()

        for p in game.plt:
            pygame.draw.rect(game.ekran, game.rnk["p"], p)
            pygame.draw.rect(game.ekran, game.rnk["k"], p, 2)
        levels.dekor_ciz()

        for pr in game.prl:
            pygame.draw.circle(game.ekran, ALTIN, (pr[0], pr[1]), 10)
            pygame.draw.circle(game.ekran, (255,200,0), (pr[0], pr[1]), 7)
            pygame.draw.circle(game.ekran, B, (pr[0]-3, pr[1]-3), 3)

        for t in game.tzl:
            pygame.draw.polygon(game.ekran, K, [(t.left,t.bottom),(t.left+20,t.top),(t.left+40,t.bottom)])
            pygame.draw.polygon(game.ekran, game.rnk["k"], [(t.left,t.bottom),(t.left+20,t.top),(t.left+40,t.bottom)], 2)

        for d in game.dsm:
            levels.dusman_ciz(d)

        particles.ptk_ciz()

        yy = abs(math.sin(game.sz*2))*1.2 if game.yr and abs(game.hx)<0.5 else 0
        player.ciz_krk(game.ox, game.oy, game.yn, yy)

        if ui.ikon(GENISLIK-130, 10, "A", NM): game.drm = "settings"
        if ui.ikon(GENISLIK-86, 10, "R", NY): game.cn = game.mc; levels.lv_yukle(game.mv)
        if ui.ikon(GENISLIK-42, 10, "M", K): game.drm = "menu"; audio.sk.stop()

        bw = 200
        pygame.draw.rect(game.ekran, (60,0,0), (GENISLIK-bw-20, 55, bw, 20))
        co = game.cn/game.mc
        pygame.draw.rect(game.ekran, (0,255,100) if co>0.5 else (255,255,0) if co>0.25 else (255,50,50),
                         (GENISLIK-bw-20, 55, int(bw*co), 20))
        pygame.draw.rect(game.ekran, B, (GENISLIK-bw-20, 55, bw, 20), 2)
        game.ekran.blit(game.fk.render("CAN", True, B), (GENISLIK-bw-60, 57))
        game.ekran.blit(game.fk.render(f"{game.mv.upper()} - Zorluk: {game.lvl['z']}/4", True, B), (GENISLIK//2-80, 12))
        game.ekran.blit(game.f.render(f"Puan: {pn}/{len(game.lvl['pr'])}", True, NP), (10, 10))
        game.ekran.blit(game.fk.render("ESC: Men", True, AGT), (10, YUKSEKLIK-30))

        if game.cn <= 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,180))
            game.ekran.blit(k2, (0,0))
            game.ekran.blit(game.fb.render("OYUN BITTI", True, K), (GENISLIK//2-120, YUKSEKLIK//2-70))
            game.ekran.blit(game.f.render("R ile yeniden basla", True, B), (GENISLIK//2-110, YUKSEKLIK//2))
            if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NM):
                game.drm = "menu"; audio.sk.stop()

        if len(game.prl) == 0 and game.cn > 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,140))
            game.ekran.blit(k2, (0,0))
            if game.si < len(ms)-1:
                game.ekran.blit(game.fb.render(f"{game.mv.upper()} GECTIN!", True, NY),
                           (GENISLIK//2-150, YUKSEKLIK//2-60))
                game.ekran.blit(game.f.render(f"Sirada: {ms[game.si].upper()}", True, B),
                           (GENISLIK//2-100, YUKSEKLIK//2))
                game.ekran.blit(game.fk.render(f"Odul: {KOSTUMLER[ms[game.si-1]]['i']} kazanildi!", True, ALTIN),
                           (GENISLIK//2-120, YUKSEKLIK//2+35))
            else:
                game.ekran.blit(game.fb.render("TUM MEVSIMLERI GECTIN!", True, ALTIN),
                           (GENISLIK//2-240, YUKSEKLIK//2-60))
                game.ekran.blit(game.f.render("Tebrikler! Oyun bitti.", True, B),
                           (GENISLIK//2-100, YUKSEKLIK//2))
                game.ekran.blit(game.fk.render(f"Odul: {KOSTUMLER[ms[-1]]['i']} kazanildi!", True, ALTIN),
                           (GENISLIK//2-120, YUKSEKLIK//2+35))
                if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+80, 200, 50, GT, AGT, NM):
                    game.drm = "menu"; audio.sk.stop()

    pygame.display.flip()
    game.saat.tick(60)

pygame.quit()
