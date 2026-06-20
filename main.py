import random
import math
import pygame

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=4)

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
game.lvl = levels.LVL[ms[0]]["rounds"][1]
game.oy = YUKSEKLIK - 100
game.cn = 5
particles.bg_par_baslat()

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
                if event.key == pygame.K_SPACE:
                    if game.yr:
                        game.hy = game.zg
                        audio.sfx_ziplama()
                        particles.ptk_ekle(game.ox, game.oy+20, NM, 5)
                    elif game.cift_zipla_t > 0 and not game.dj_k:
                        game.hy = game.zg * 0.85
                        game.dj_k = True
                        audio.sfx_cift_ziplama()
                        particles.ptk_ekle(game.ox, game.oy+20, NM, 5)
                if event.key == pygame.K_r and game.cn <= 0:
                    game.cn = game.mc
                    game.ox, game.oy = game.cp_x, game.cp_y
                    game.hx = game.hy = 0


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

        spd = 5 + (2 if game.hiz_t > 0 else 0)
        game.hx = (ts[pygame.K_d] - ts[pygame.K_a]) * spd
        if ts[pygame.K_d]: game.yn = 1
        elif ts[pygame.K_a]: game.yn = -1

        # Sol mouse tusu ile ates (sadece oyun alaninda)
        if pygame.mouse.get_pressed()[0] and game.weapon and game.ammo > 0 and game.shoot_cd <= 0:
            mx, my = pygame.mouse.get_pos()
            if my < YUKSEKLIK - 40:  # HUD alani disinda
                arad = -1 if game.yn < 0 else 1
                wd = WP_DATA[game.mv]
                shot_spd = wd["spd"]
                if game.shoot_cd > wd["cd"] - 3:  # hizli tik (ardi ardina) -> duz gidis
                    vy_b = -2
                else:  # yavas tik -> dalgali
                    vy_b = -1.5 + math.sin(game.sz * 4) * 1.5
                game.bullets.append({"x": game.ox, "y": game.oy-20, "vx": shot_spd*arad, "vy": vy_b, "r": wd["r"], "dmg": wd["dmg"], "t": wd["s"], "mv": game.mv})
                game.ammo -= 1
                game.shoot_cd = wd["cd"]
                audio.sfx_ates()
                particles.ptk_birim(game.ox + arad*20, game.oy-20, wd["r"])

        if game.shoot_cd > 0: game.shoot_cd -= 1

        oc = pygame.Rect(game.ox-14, game.oy-50, 28, 75)
        oy2 = game.oy

        # Hareketli platformlari guncelle (once yeni konumlari hesapla)
        for mp in game.mpl:
            mp["t"] += mp["spd"] * 0.02
            ny = mp["by"] + math.sin(mp["t"]) * mp["dy"]
            nx = mp["bx"] + math.sin(mp["t"]) * mp["dx"]
            mp["vx"] = nx - mp["r"].x
            mp["vy"] = ny - mp["r"].y
            mp["r"].x = nx
            mp["r"].y = ny

        # Yatay hareket
        game.ox += game.hx; oc.x = game.ox-14
        for p in game.plt:
            if oc.colliderect(p):
                if game.hx > 0: oc.right = p.left; game.ox = oc.x+14
                elif game.hx < 0: oc.left = p.right; game.ox = oc.x+14
        for mp in game.mpl:
            if oc.colliderect(mp["r"]):
                if game.hx > 0: oc.right = mp["r"].left; game.ox = oc.x+14
                elif game.hx < 0: oc.left = mp["r"].right; game.ox = oc.x+14

        # Dikey hareket
        game.hy += game.yc; game.oy += game.hy
        oc.x = game.ox-14; oc.y = game.oy-50

        game.yr = False; mpl_u = -1
        for p in game.plt:
            if oc.colliderect(p):
                if game.hy > 0:
                    if not game.yr and oy2 < p.top: particles.ptk_ekle(game.ox, p.top, game.rnk["z"], 4)
                    oc.bottom = p.top; game.oy = oc.y+50; game.hy = 0; game.yr = True; game.dj_k = False
                elif game.hy < 0: oc.top = p.bottom; game.oy = oc.y+50; game.hy = 0

        for i, mp in enumerate(game.mpl):
            if oc.colliderect(mp["r"]):
                if game.hy >= 0 and oy2 + 25 < mp["r"].top + 20:
                    if not game.yr: particles.ptk_ekle(game.ox, mp["r"].top, game.rnk["z"], 3)
                    oc.bottom = mp["r"].top; game.oy = oc.y+50; game.hy = 0; game.yr = True; game.dj_k = False
                    mpl_u = i
                elif game.hy < 0:
                    oc.top = mp["r"].bottom; game.oy = oc.y+50; game.hy = 0

        # Ustunde durulan platformun hizini karaktere ekle
        if mpl_u >= 0:
            game.ox += game.mpl[mpl_u]["vx"]
            game.oy += game.mpl[mpl_u]["vy"]

        # Prism toplama
        for pr in game.prl[:]:
            if oc.colliderect(pygame.Rect(pr[0]-10, pr[1]-10, 20, 20)):
                game.prl.remove(pr); particles.ptk_ekle(pr[0], pr[1], ALTIN, 10)
                game.puan += 100 + max(0, 50 - len(game.prl)*5)
                audio.sfx_topla()

        # Miknatis efekti
        if game.miknatis_t > 0:
            for pr in game.prl[:]:
                dx = game.ox - pr[0]; dy = game.oy - pr[1]
                d = math.sqrt(dx*dx + dy*dy)
                if d < 200 and d > 0:
                    game.prl.remove(pr); particles.ptk_ekle(pr[0], pr[1], ALTIN, 8)
                    game.puan += 100 + max(0, 50 - len(game.prl)*5)
                    audio.sfx_topla()

        # Tuzak kontrol
        for t in game.tzl:
            if oc.colliderect(t):
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_ekle(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0; break

        # Dusman kontrol
        for d in game.dsm:
            d["r"].x += d["h"]
            if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]: d["h"] *= -1
            if oc.colliderect(d["r"]):
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_patlatma(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0

        # Checkpoint kontrol
        if game.lvl.get("cp"):
            cpx, cpy = game.lvl["cp"]
            if abs(game.ox - cpx) < 30 and abs(game.oy - cpy) < 30:
                if game.cp_x != cpx or game.cp_y != cpy:
                    game.cp_x, game.cp_y = cpx, cpy
                    audio.sfx_checkpoint()
                    particles.ptk_ekle(cpx, cpy, NM, 12)

        # Power-up kontrol
        for pu in game.lvl.get("pu", [])[:]:
            pux, puy, put = pu
            if oc.colliderect(pygame.Rect(pux-8, puy-8, 16, 16)):
                game.lvl["pu"].remove(pu)
                audio.sfx_powerup()
                particles.ptk_patlatma(pux, puy, NM, 15)
                if put == "hiz": game.hiz_t = 300
                elif put == "kalkan": game.kalkan_t = 1
                elif put == "cift_zipla": game.cift_zipla_t = 1
                elif put == "miknatis": game.miknatis_t = 300
                elif put == "kalp":
                    game.cn = min(game.mc, game.cn + 1)
                    particles.ptk_patlatma(pux, puy, K, 20, 6)

        # Silah mermisi toplama
        for wp in game.lvl.get("wp", [])[:]:
            wpx, wpy = wp
            if oc.colliderect(pygame.Rect(wpx-8, wpy-8, 16, 16)):
                game.lvl["wp"].remove(wp)
                game.weapon = game.mv
                game.ammo = min(game.max_ammo, game.ammo + WP_DATA[game.mv]["a"])
                audio.sfx_powerup()
                particles.ptk_patlatma(wpx, wpy, WP_DATA[game.mv]["r"], 12)

        # Sinirlar
        if game.ox < 14: game.ox = 14
        if game.ox > GENISLIK-14: game.ox = GENISLIK-14
        if game.oy > YUKSEKLIK+50:
            if game.kalkan_t > 0:
                game.kalkan_t = 0; particles.ptk_ekle(game.ox, game.oy, KR, 15)
                game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0
            else:
                game.cn -= 1; audio.sfx_hasar()
                game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0

        # Mermi guncelle
        for b in game.bullets[:]:
            b["x"] += b["vx"]; b["y"] += b["vy"]
            b["vy"] += 0.1
            if b["x"] < -20 or b["x"] > GENISLIK+20 or b["y"] < -20 or b["y"] > YUKSEKLIK+20:
                game.bullets.remove(b); continue
            br = pygame.Rect(b["x"]-5, b["y"]-5, 10, 10)
            hit = False
            for d in game.dsm[:]:
                if br.colliderect(d["r"]):
                    game.dsm.remove(d); particles.ptk_patlatma(b["x"], b["y"], b["r"], 15)
                    audio.sfx_hasar(); hit = True; break
            if hit: game.bullets.remove(b); continue
            if game.boss_sv and game.boss_hp > 0:
                bpx = GENISLIK//2 + math.sin(game.boss_timer * 0.01) * (GENISLIK//2 - 100)
                bpy = 80 + math.sin(game.boss_timer * 0.02) * 20
                if br.colliderect(pygame.Rect(bpx-35, bpy-35, 70, 70)):
                    game.boss_hp -= b["dmg"]
                    game.bullets.remove(b)
                    audio.sfx_boss_hit()
                    particles.ptk_patlatma(b["x"], b["y"], b["r"], 12)
                    continue

        # Boss mermisi guncelle
        for b in game.boss_btl[:]:
            b["x"] += b["vx"]; b["y"] += b["vy"]
            b["vy"] += 0.05
            if b["x"] < -20 or b["x"] > GENISLIK+20 or b["y"] < -20 or b["y"] > YUKSEKLIK+20:
                game.boss_btl.remove(b); continue
            br = pygame.Rect(b["x"]-6, b["y"]-6, 12, 12)
            if oc.colliderect(br):
                game.boss_btl.remove(b)
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_patlatma(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0

        # Boss AI
        if game.boss_sv and game.boss_hp > 0:
            bx = GENISLIK//2 + math.sin(game.boss_timer * 0.01) * (GENISLIK//2 - 100)
            by = 80 + math.sin(game.boss_timer * 0.02) * 20
            game.boss_timer += 1
            game.boss_atk_cd -= 1
            game.boss_lazer_t = max(0, game.boss_lazer_t - 1)
            game.boss_minyon_t = max(0, game.boss_minyon_t - 1)
            game.boss_dalga_t = max(0, game.boss_dalga_t - 1)

            if game.boss_atk_cd <= 0:
                ptrn = game.boss_ptrn % 3
                if ptrn == 0:
                    # Normal ates - hedefe dogru
                    dx = game.ox - bx; dy = game.oy - by
                    d = math.sqrt(dx*dx + dy*dy)
                    if d > 0:
                        spd = 3 + random.uniform(-0.5, 0.5)
                        game.boss_btl.append({"x": bx, "y": by+30, "vx": dx/d*spd, "vy": dy/d*spd, "r": K})
                    game.boss_atk_cd = max(20, 60 - game.boss_ptrn*5)
                elif ptrn == 1:
                    # Lazer - 3 paralel mermi
                    for li in range(-1, 2):
                        dx = game.ox - bx + li*30; dy = game.oy - by
                        d = math.sqrt(dx*dx + dy*dy)
                        if d > 0:
                            game.boss_btl.append({"x": bx + li*15, "y": by+30, "vx": dx/d*4, "vy": dy/d*4, "r": (255, 100, 100)})
                    game.boss_atk_cd = max(30, 80 - game.boss_ptrn*5)
                    game.boss_lazer_t = 15
                else:
                    # Dalga - acili yayilim
                    for wi in range(5):
                        a3 = -1 + wi * 0.5
                        dx = game.ox - bx + a3*80
                        dy = game.oy - by
                        d = math.sqrt(dx*dx + dy*dy)
                        if d > 0:
                            game.boss_btl.append({"x": bx + wi*8, "y": by+30, "vx": dx/d*3 + random.uniform(-0.3, 0.3), "vy": dy/d*3 + random.uniform(-0.5, 0.5), "r": (200, 50, 200)})
                    game.boss_atk_cd = max(40, 100 - game.boss_ptrn*5)
                    game.boss_dalga_t = 20
                game.boss_ptrn = (game.boss_ptrn + 1) % 6
                audio.sfx_boss_ates()

            # Lazer gostergesi
            if game.boss_lazer_t > 10:
                lazer_y = by + 40
                for li in range(-1, 2):
                    lx = bx + li*15
                    ldx = game.ox - lx; ldy = game.oy - lazer_y
                    ld = math.sqrt(ldx*ldx + ldy*ldy)
                    if ld > 0:
                        ldx /= ld; ldy /= ld
                        pygame.draw.line(game.ekran, (255, 50, 50, 100), (int(lx), int(lazer_y)), (int(lx+ldx*500), int(lazer_y+ldy*500)), 2)

        # Boss olumu
        if game.boss_sv and game.boss_hp <= 0 and game.cn > 0:
            game.boss_sv = False
            audio.sfx_boss_ol()
            particles.ptk_patlatma(GENISLIK//2, 100, ALTIN, 40, 8)
            particles.ptk_patlatma(GENISLIK//2, 100, NM, 30, 6)

        # Tur bitis kontrolu
        if len(game.prl) == 0 and game.cn > 0 and not game.boss_sv:
            if not hasattr(game, 'rnd_bitti') or not game.rnd_bitti:
                game.rnd_bitti = True
                game.rnd_sayac = 0
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, NM, 20)
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, ALTIN, 12)
        elif game.boss_sv and game.boss_hp <= 0 and game.cn > 0 and game.boss_max_hp > 0:
            if not getattr(game, 'rnd_bitti', False):
                game.rnd_bitti = True
                game.rnd_sayac = 0

        # Power-up sureleri
        if game.hiz_t > 0: game.hiz_t -= 1
        if game.miknatis_t > 0: game.miknatis_t -= 1

        particles.ptk_guncelle()
        particles.ark_ciz()

        # Cizim
        for p in game.plt:
            pygame.draw.rect(game.ekran, game.rnk["p"], p)
            pygame.draw.rect(game.ekran, game.rnk["k"], p, 2)

        for mp in game.mpl:
            pygame.draw.rect(game.ekran, (100, 100, 150), mp["r"])
            pygame.draw.rect(game.ekran, (150, 150, 200), mp["r"], 2)

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

        # Mermi ciz (mevsime ozel)
        for b in game.bullets:
            bx2, by2 = int(b["x"]), int(b["y"])
            if b.get("mv") == "ilkbahar":
                pygame.draw.circle(game.ekran, C1, (bx2, by2), 5)
                pygame.draw.circle(game.ekran, C2, (bx2-2, by2-2), 2)
                pygame.draw.circle(game.ekran, C2, (bx2+2, by2+2), 2)
            elif b.get("mv") == "yaz":
                for ri in range(4):
                    a2 = ri * 1.57 + game.sz * 0.1
                    pygame.draw.line(game.ekran, ALTIN, (bx2+int(math.cos(a2)*5), by2+int(math.sin(a2)*5)), (bx2+int(math.cos(a2)*8), by2+int(math.sin(a2)*8)), 2)
                pygame.draw.circle(game.ekran, ALTIN, (bx2, by2), 5)
                pygame.draw.circle(game.ekran, (255, 255, 200), (bx2, by2), 3)
            elif b.get("mv") == "sonbahar":
                pygame.draw.ellipse(game.ekran, YP, (bx2-6, by2-3, 12, 6))
                pygame.draw.line(game.ekran, (150, 80, 20), (bx2-5, by2), (bx2+5, by2), 1)
                pygame.draw.line(game.ekran, (150, 80, 20), (bx2, by2-2), (bx2, by2+2), 1)
            elif b.get("mv") == "kis":
                pygame.draw.circle(game.ekran, KR, (bx2, by2), 5)
                pygame.draw.circle(game.ekran, (200, 230, 255), (bx2, by2), 3)
                for ri in range(3):
                    a2 = ri * 2.09 + game.sz * 0.05
                    pygame.draw.line(game.ekran, (200, 230, 255), (bx2+int(math.cos(a2)*3), by2+int(math.sin(a2)*3)), (bx2+int(math.cos(a2)*6), by2+int(math.sin(a2)*6)), 1)
            else:
                pygame.draw.circle(game.ekran, b["r"], (bx2, by2), 5)
                pygame.draw.circle(game.ekran, B, (bx2, by2), 3)

        for b in game.boss_btl:
            pygame.draw.circle(game.ekran, K, (int(b["x"]), int(b["y"])), 6)
            pygame.draw.circle(game.ekran, K, (int(b["x"]), int(b["y"])), 4, 1)

        # Power-up ciz (animasyonlu)
        for pu in game.lvl.get("pu", []):
            pux, puy, put = pu
            puy2 = puy + math.sin(game.sz * 2 + pux * 0.1) * 3
            pr2 = pygame.Rect(pux-8, puy2-8, 16, 16)
            if put == "hiz":
                pygame.draw.polygon(game.ekran, NM, [(pux, puy2-7),(pux-6,puy2+5),(pux+6,puy2+5)])
                pygame.draw.polygon(game.ekran, B, [(pux, puy2-7),(pux-6,puy2+5),(pux+6,puy2+5)], 1)
                pygame.draw.line(game.ekran, (200, 200, 255), (pux-2, puy2-3), (pux+2, puy2-3), 2)
                pygame.draw.line(game.ekran, (200, 200, 255), (pux-2, puy2), (pux+2, puy2), 2)
            elif put == "kalkan":
                pygame.draw.circle(game.ekran, KR, (pux, puy2), 8, 2)
                pygame.draw.circle(game.ekran, KR, (pux, puy2), 3)
                pygame.draw.circle(game.ekran, (255, 100, 100), (pux, puy2), 9, 1)
                pygame.draw.line(game.ekran, KR, (pux-3, puy2-5), (pux+3, puy2-5), 2)
            elif put == "cift_zipla":
                pygame.draw.polygon(game.ekran, NY, [(pux, puy2+5),(pux-6,puy2-4),(pux+6,puy2-4)])
                pygame.draw.polygon(game.ekran, B, [(pux, puy2+5),(pux-6,puy2-4),(pux+6,puy2-4)], 1)
                pygame.draw.polygon(game.ekran, NY, [(pux, puy2-3),(pux-4,puy2-10),(pux+4,puy2-10)])
                pygame.draw.polygon(game.ekran, B, [(pux, puy2-3),(pux-4,puy2-10),(pux+4,puy2-10)], 1)
            elif put == "miknatis":
                pygame.draw.circle(game.ekran, ALTIN, (pux, puy2), 7)
                pygame.draw.circle(game.ekran, B, (pux, puy2), 4)
                pygame.draw.line(game.ekran, ALTIN, (pux-8, puy2-4), (pux+8, puy2-4), 2)
                pygame.draw.line(game.ekran, ALTIN, (pux-8, puy2+4), (pux+8, puy2+4), 2)
            elif put == "kalp":
                pygame.draw.polygon(game.ekran, K, [(pux, puy2+5),(pux-7,puy2-2),(pux+7,puy2-2)])
                pygame.draw.polygon(game.ekran, B, [(pux, puy2+5),(pux-7,puy2-2),(pux+7,puy2-2)], 1)
                pygame.draw.circle(game.ekran, K, (pux-4, puy2-4), 4)
                pygame.draw.circle(game.ekran, K, (pux+4, puy2-4), 4)
                pygame.draw.circle(game.ekran, B, (pux-4, puy2-4), 4, 1)
                pygame.draw.circle(game.ekran, B, (pux+4, puy2-4), 4, 1)
            # Parlama efekti
            alfa_pu = int(80 + math.sin(game.sz * 3 + pux) * 40)
            aura_pu = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(aura_pu, (255, 255, 200, alfa_pu // 3), (10, 10), 10)
            game.ekran.blit(aura_pu, (pux-10, puy2-10), special_flags=pygame.BLEND_ADD)

        # Silah mermisi goster
        for wp in game.lvl.get("wp", []):
            wpx, wpy = wp
            wr = WP_DATA[game.mv]["r"]
            pygame.draw.rect(game.ekran, wr, (wpx-6, wpy-4, 12, 8))
            pygame.draw.rect(game.ekran, B, (wpx-6, wpy-4, 12, 8), 1)

        # Checkpoint ciz
        cpx, cpy = game.lvl.get("cp", (100, YUKSEKLIK-100))
        pygame.draw.rect(game.ekran, (200,200,50), (cpx-3, cpy-20, 6, 20))
        pygame.draw.polygon(game.ekran, (200,200,50), [(cpx-6, cpy-20), (cpx+6, cpy-20), (cpx, cpy-32)])

        # Boss ciz (mevsime ozel)
        if game.boss_sv and game.boss_hp > 0:
            bx = GENISLIK//2 + math.sin(game.boss_timer * 0.01) * (GENISLIK//2 - 100)
            by = 80 + math.sin(game.boss_timer * 0.02) * 20
            by2 = by

            if game.mv == "ilkbahar":
                # === ET YIYEN BITKI (saksida) ===
                # Saksi
                pygame.draw.polygon(game.ekran, (180, 100, 50), [(int(bx-25), int(by2+40)), (int(bx+25), int(by2+40)), (int(bx+20), int(by2+55)), (int(bx-20), int(by2+55))])
                pygame.draw.polygon(game.ekran, (200, 120, 60), [(int(bx-25), int(by2+40)), (int(bx+25), int(by2+40)), (int(bx+20), int(by2+55)), (int(bx-20), int(by2+55))], 1)
                # Saksida cizgi
                pygame.draw.line(game.ekran, (160, 80, 40), (int(bx-22), int(by2+45)), (int(bx+22), int(by2+45)), 1)
                # Govde/sap
                pygame.draw.rect(game.ekran, (60, 140, 60), (int(bx-6), int(by2+10), 12, 30))
                pygame.draw.rect(game.ekran, (80, 160, 80), (int(bx-6), int(by2+10), 12, 30), 1)
                # Yapraklar
                for li in range(3):
                    lx = bx - 18 + li * 18
                    pygame.draw.ellipse(game.ekran, (50, 130, 50), (int(lx), int(by2+15+li*5), 14, 6))
                    pygame.draw.ellipse(game.ekran, (70, 150, 70), (int(lx), int(by2+15+li*5), 14, 6), 1)
                # Kafa - et yiyen bitki agzi
                pygame.draw.ellipse(game.ekran, (60, 160, 60), (int(bx-28), int(by2-15), 56, 40))
                pygame.draw.ellipse(game.ekran, (80, 180, 80), (int(bx-28), int(by2-15), 56, 40), 1)
                # Ic kisim (kirmizi)
                pygame.draw.ellipse(game.ekran, (200, 50, 50), (int(bx-20), int(by2-8), 40, 28))
                pygame.draw.ellipse(game.ekran, (220, 80, 80), (int(bx-20), int(by2-8), 40, 28), 1)
                # Disler (ucgen)
                for ti in range(6):
                    tx = bx - 18 + ti * 7
                    pygame.draw.polygon(game.ekran, (255, 255, 240), [(int(tx), int(by2-8)), (int(tx+4), int(by2-8)), (int(tx+2), int(by2+2))])
                    pygame.draw.polygon(game.ekran, (255, 255, 240), [(int(tx), int(by2+12)), (int(tx+4), int(by2+12)), (int(tx+2), int(by2+2))])
                # Alt disler
                for ti in range(5):
                    tx = bx - 15 + ti * 7
                    pygame.draw.polygon(game.ekran, (255, 255, 240), [(int(tx), int(by2+12)), (int(tx+4), int(by2+12)), (int(tx+2), int(by2+18))])
                # Gozler (bobrek)
                pygame.draw.ellipse(game.ekran, (255, 255, 100), (int(bx-16), int(by2-20), 12, 8))
                pygame.draw.ellipse(game.ekran, (255, 255, 100), (int(bx+4), int(by2-20), 12, 8))
                pygame.draw.circle(game.ekran, S, (int(bx-10), int(by2-18)), 3)
                pygame.draw.circle(game.ekran, S, (int(bx+10), int(by2-18)), 3)
                # Salya efekti
                for si in range(3):
                    sy = by2 + 16 + si * 5
                    pygame.draw.line(game.ekran, (150, 200, 150), (int(bx-8+si*8), int(by2+16)), (int(bx-8+si*8+math.sin(game.boss_timer*0.1+si)*2), int(sy)), 2)
                # Sarmaşıklar (hareketli)
                for vi in range(4):
                    vx = bx - 35 + vi * 24
                    vy = by2 + math.sin(game.boss_timer * 0.05 + vi) * 8
                    pygame.draw.line(game.ekran, (40, 160, 40), (int(vx), int(by2+30)), (int(vx + math.sin(game.boss_timer*0.03+vi)*10), int(vy+25)), 3)

            elif game.mv == "yaz":
                # === DEV KUM CANAVARI (Malphite tarzi) ===
                # Govde - kaya goleyi
                pygame.draw.polygon(game.ekran, (180, 150, 100), [(int(bx-35), int(by2+35)), (int(bx-30), int(by2)), (int(bx), int(by2-10)), (int(bx+30), int(by2)), (int(bx+35), int(by2+35))])
                pygame.draw.polygon(game.ekran, (200, 170, 120), [(int(bx-35), int(by2+35)), (int(bx-30), int(by2)), (int(bx), int(by2-10)), (int(bx+30), int(by2)), (int(bx+35), int(by2+35))], 1)
                # Kaya dokusu
                for ri in range(4):
                    rx = bx - 25 + ri * 15
                    ry = by2 + 10 + ri * 5
                    pygame.draw.line(game.ekran, (160, 130, 80), (int(rx), int(ry)), (int(rx+10), int(ry+5)), 1)
                # Kol (sag)
                pygame.draw.polygon(game.ekran, (180, 150, 100), [(int(bx+30), int(by2+5)), (int(bx+48), int(by2-5)), (int(bx+50), int(by2+15)), (int(bx+35), int(by2+15))])
                pygame.draw.polygon(game.ekran, (200, 170, 120), [(int(bx+30), int(by2+5)), (int(bx+48), int(by2-5)), (int(bx+50), int(by2+15)), (int(bx+35), int(by2+15))], 1)
                # Kol (sol)
                pygame.draw.polygon(game.ekran, (180, 150, 100), [(int(bx-30), int(by2+5)), (int(bx-48), int(by2-5)), (int(bx-50), int(by2+15)), (int(bx-35), int(by2+15))])
                pygame.draw.polygon(game.ekran, (200, 170, 120), [(int(bx-30), int(by2+5)), (int(bx-48), int(by2-5)), (int(bx-50), int(by2+15)), (int(bx-35), int(by2+15))], 1)
                # Yumruk (sag)
                pygame.draw.circle(game.ekran, (200, 170, 120), (int(bx+50), int(by2+5)), 12)
                pygame.draw.circle(game.ekran, (220, 190, 140), (int(bx+50), int(by2+5)), 12, 1)
                # Yumruk (sol)
                pygame.draw.circle(game.ekran, (200, 170, 120), (int(bx-50), int(by2+5)), 12)
                pygame.draw.circle(game.ekran, (220, 190, 140), (int(bx-50), int(by2+5)), 12, 1)
                # Kafa - yuvarlak kaya
                pygame.draw.circle(game.ekran, (190, 160, 110), (int(bx), int(by2-5)), 22)
                pygame.draw.circle(game.ekran, (210, 180, 130), (int(bx), int(by2-5)), 22, 1)
                # Gozler (parlayan altin)
                pygame.draw.circle(game.ekran, (255, 200, 50), (int(bx-8), int(by2-10)), 6)
                pygame.draw.circle(game.ekran, (255, 200, 50), (int(bx+8), int(by2-10)), 6)
                pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx-8), int(by2-10)), 3)
                pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx+8), int(by2-10)), 3)
                # Agiz (kaya yarigi)
                pygame.draw.line(game.ekran, (100, 70, 30), (int(bx-10), int(by2+5)), (int(bx+10), int(by2+5)), 3)
                # Kum parlamasi
                for pi in range(5):
                    px = bx - 25 + pi * 12
                    py = by2 - 15 + int(math.sin(game.boss_timer*0.1+pi)*5)
                    pygame.draw.circle(game.ekran, ALTIN, (int(px), int(py)), 2)
                # Kum taneleri dusuyor
                for gi in range(6):
                    gx = bx - 30 + gi * 12
                    gy = by2 + 20 + gi * 3 + math.sin(game.boss_timer*0.05+gi)*5
                    pygame.draw.circle(game.ekran, (220, 200, 160), (int(gx), int(gy)), 1)

            elif game.mv == "sonbahar":
                # === WITHER/SOLMUS ISKELLET CANAVARI (Minecraft tarzi) ===
                # Govde - kara kemik
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx-18), int(by2+8), 36, 35))
                pygame.draw.rect(game.ekran, (40, 30, 20), (int(bx-18), int(by2+8), 36, 35), 1)
                # Kaburga kemikleri
                for ri in range(3):
                    ry = by2 + 14 + ri * 8
                    pygame.draw.line(game.ekran, (50, 40, 30), (int(bx-16), int(ry)), (int(bx+16), int(ry)), 1)
                # Bacaklar (ince kemik)
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx-14), int(by2+43), 8, 18))
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx+6), int(by2+43), 8, 18))
                # Ayaklar
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx-18), int(by2+58), 14, 6))
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx+4), int(by2+58), 14, 6))
                # Kollar (iskelet)
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx-30), int(by2+10), 14, 6))
                pygame.draw.rect(game.ekran, (20, 15, 10), (int(bx+16), int(by2+10), 14, 6))
                # El (kanca gibi)
                pygame.draw.line(game.ekran, (30, 25, 20), (int(bx-30), int(by2+10)), (int(bx-38), int(by2+2)), 2)
                pygame.draw.line(game.ekran, (30, 25, 20), (int(bx+30), int(by2+10)), (int(bx+38), int(by2+2)), 2)
                # Kafa - kafatasi
                pygame.draw.rect(game.ekran, (25, 20, 15), (int(bx-14), int(by2-20), 28, 28))
                pygame.draw.rect(game.ekran, (45, 35, 25), (int(bx-14), int(by2-20), 28, 28), 1)
                # Kafatasi cizgileri
                pygame.draw.line(game.ekran, (35, 25, 18), (int(bx-12), int(by2-8)), (int(bx+12), int(by2-8)), 1)
                # Goz cukurlari (bos, parlayan mor)
                pygame.draw.rect(game.ekran, (60, 10, 60), (int(bx-10), int(by2-16), 8, 6))
                pygame.draw.rect(game.ekran, (60, 10, 60), (int(bx+2), int(by2-16), 8, 6))
                pygame.draw.rect(game.ekran, (120, 20, 120), (int(bx-10), int(by2-16), 8, 6), 1)
                pygame.draw.rect(game.ekran, (120, 20, 120), (int(bx+2), int(by2-16), 8, 6), 1)
                # Mor isil
                pygame.draw.circle(game.ekran, (150, 30, 150), (int(bx-6), int(by2-13)), 2)
                pygame.draw.circle(game.ekran, (150, 30, 150), (int(bx+6), int(by2-13)), 2)
                # Burun deligi
                pygame.draw.rect(game.ekran, (10, 8, 5), (int(bx-2), int(by2-8), 4, 3))
                # Agiz
                pygame.draw.line(game.ekran, (10, 8, 5), (int(bx-8), int(by2-2)), (int(bx+8), int(by2-2)), 1)
                pygame.draw.line(game.ekran, (10, 8, 5), (int(bx-6), int(by2)), (int(bx+6), int(by2)), 1)
                # Eski agac dallari (vucuttan cikan)
                for bi in range(4):
                    dx = bx - 20 + bi * 14
                    dy = by2 - 5 + bi * 8
                    pygame.draw.line(game.ekran, (40, 25, 15), (int(dx), int(dy)), (int(dx-8+bi*4), int(dy-10+bi*2)), 2)
                # Solmus yapraklar
                for li in range(4):
                    lx = bx - 25 + li * 16
                    ly = by2 - 18 + li * 8
                    pygame.draw.ellipse(game.ekran, (80, 40, 10), (int(lx), int(ly), 6, 3))
                # Mor efekt (wither)
                for ei in range(3):
                    ex = bx - 20 + ei * 20
                    ey = by2 - 25 + ei * 12
                    pygame.draw.circle(game.ekran, (80, 20, 80, 100), (int(ex + math.sin(game.boss_timer*0.1+ei)*3), int(ey)), 4 + ei)

            elif game.mv == "kis":
                # === YETI (Koca Ayak) ===
                # Govde (kocaman, beyaz tuylu)
                pygame.draw.ellipse(game.ekran, (220, 230, 240), (int(bx-30), int(by2), 60, 50))
                pygame.draw.ellipse(game.ekran, (230, 240, 250), (int(bx-30), int(by2), 60, 50), 1)
                # Gocek
                pygame.draw.ellipse(game.ekran, (240, 245, 255), (int(bx-20), int(by2+8), 40, 35))
                # Kollar
                pygame.draw.line(game.ekran, (220, 230, 240), (int(bx-28), int(by2+8)), (int(bx-50), int(by2-5)), 6)
                pygame.draw.line(game.ekran, (220, 230, 240), (int(bx+28), int(by2+8)), (int(bx+50), int(by2-5)), 6)
                # Kollar (uzun)
                # Eller (kocaman)
                pygame.draw.circle(game.ekran, (200, 210, 225), (int(bx-52), int(by2-8)), 10)
                pygame.draw.circle(game.ekran, (200, 210, 225), (int(bx+52), int(by2-8)), 10)
                pygame.draw.circle(game.ekran, (210, 220, 235), (int(bx-52), int(by2-8)), 10, 1)
                pygame.draw.circle(game.ekran, (210, 220, 235), (int(bx+52), int(by2-8)), 10, 1)
                # Kafa (kucuk, govdeye gomulu)
                pygame.draw.circle(game.ekran, (230, 235, 245), (int(bx), int(by2-8)), 18)
                pygame.draw.circle(game.ekran, (240, 245, 255), (int(bx), int(by2-8)), 18, 1)
                # Kulaklar
                pygame.draw.circle(game.ekran, (220, 225, 235), (int(bx-18), int(by2-12)), 6)
                pygame.draw.circle(game.ekran, (220, 225, 235), (int(bx+18), int(by2-12)), 6)
                pygame.draw.circle(game.ekran, (200, 210, 220), (int(bx-18), int(by2-12)), 4)
                pygame.draw.circle(game.ekran, (200, 210, 220), (int(bx+18), int(by2-12)), 4)
                # Gozler (kucuk, kirmizi)
                pygame.draw.circle(game.ekran, (150, 30, 30), (int(bx-6), int(by2-12)), 4)
                pygame.draw.circle(game.ekran, (150, 30, 30), (int(bx+6), int(by2-12)), 4)
                pygame.draw.circle(game.ekran, (255, 50, 50), (int(bx-6), int(by2-12)), 2)
                pygame.draw.circle(game.ekran, (255, 50, 50), (int(bx+6), int(by2-12)), 2)
                # Agiz
                pygame.draw.ellipse(game.ekran, (180, 50, 50), (int(bx-8), int(by2-4), 16, 8))
                pygame.draw.ellipse(game.ekran, (200, 60, 60), (int(bx-8), int(by2-4), 16, 8), 1)
                # Dis (sivri)
                for ti in range(4):
                    tx = bx - 6 + ti * 4
                    pygame.draw.polygon(game.ekran, (255, 255, 250), [(int(tx), int(by2-4)), (int(tx+2), int(by2-4)), (int(tx+1), int(by2))])
                # Bacaklar (kalin)
                pygame.draw.ellipse(game.ekran, (220, 230, 240), (int(bx-22), int(by2+42), 18, 18))
                pygame.draw.ellipse(game.ekran, (220, 230, 240), (int(bx+4), int(by2+42), 18, 18))
                # Ayaklar (kocaman)
                pygame.draw.ellipse(game.ekran, (200, 210, 225), (int(bx-28), int(by2+55), 28, 10))
                pygame.draw.ellipse(game.ekran, (200, 210, 225), (int(bx+2), int(by2+55), 28, 10))
                pygame.draw.ellipse(game.ekran, (210, 220, 235), (int(bx-28), int(by2+55), 28, 10), 1)
                pygame.draw.ellipse(game.ekran, (210, 220, 235), (int(bx+2), int(by2+55), 28, 10), 1)
                # Tirnak
                for ti in range(3):
                    pygame.draw.circle(game.ekran, (180, 190, 200), (int(bx-22+ti*8), int(by2+58)), 2)
                    pygame.draw.circle(game.ekran, (180, 190, 200), (int(bx+8+ti*8), int(by2+58)), 2)
                # Kar efektı
                for si in range(8):
                    sx = bx - 35 + si * 10
                    sy = by2 - 20 + math.sin(game.boss_timer*0.08+si*2)*8
                    pygame.draw.circle(game.ekran, KR, (int(sx + math.sin(game.boss_timer*0.03+si)*5), int(sy + si*3)), 2)
                # Nefes (buz)
                if game.boss_ptrn % 2 == 0:
                    pygame.draw.ellipse(game.ekran, (200, 230, 255, 80), (int(bx-20), int(by2+5), 40, 15))

        particles.ptk_ciz()

        yy = abs(math.sin(game.sz*2))*1.2 if game.yr and abs(game.hx)<0.5 else 0
        player.ciz_krk(game.ox, game.oy, game.yn, yy)

        # Kalkan goruntusu
        if game.kalkan_t > 0:
            pygame.draw.circle(game.ekran, KR, (int(game.ox), int(game.oy-20)), 40, 3)

        # HUD
        if ui.ikon(GENISLIK-130, 10, "A", NM): game.drm = "settings"
        if ui.ikon(GENISLIK-86, 10, "R", NY):
            game.cn = game.mc
            game.ox, game.oy = game.cp_x, game.cp_y
            game.hx = game.hy = 0
        if ui.ikon(GENISLIK-42, 10, "M", K): game.drm = "menu"; audio.sk.stop()
        # Ses toggle
        if ui.ikon(10, 55, "S", NM if game.ses_acik else K):
            game.ses_acik = not game.ses_acik
            audio.sk.set_volume(game.ayar["ses"]/100 if game.ses_acik else 0)
            audio.ses_kanal.set_volume(game.ayar["ses"]/100 if game.ses_acik else 0)
            audio.ses_kanal2.set_volume(game.ayar["ses"]/100 if game.ses_acik else 0)

        bw = 200
        pygame.draw.rect(game.ekran, (60,0,0), (GENISLIK-bw-20, 55, bw, 20))
        co = game.cn/game.mc if game.mc > 0 else 0
        pygame.draw.rect(game.ekran, (0,255,100) if co>0.5 else (255,255,0) if co>0.25 else (255,50,50),
                         (GENISLIK-bw-20, 55, int(bw*co), 20))
        pygame.draw.rect(game.ekran, B, (GENISLIK-bw-20, 55, bw, 20), 2)
        game.ekran.blit(game.fk.render("CAN", True, B), (GENISLIK-bw-60, 57))
        game.ekran.blit(game.fk.render(f"{game.mv.upper()} - Tur {game.rnd}/4 - Zorluk: {game.lvl['z']}/4", True, B), (GENISLIK//2-160, 12))
        game.ekran.blit(game.f.render(f"Puan: {game.puan}", True, NP), (10, 10))

        # Yüksek skor
        if game.yuksek_puan.get(game.mv, 0) > 0:
            game.ekran.blit(game.fk.render(f"En Yuksek: {game.yuksek_puan[game.mv]}", True, ALTIN), (10, 30))

        # Silah HUD
        if game.weapon:
            wr = WP_DATA[game.mv]["r"]
            wname = WP_DATA[game.mv]["i"]
            pygame.draw.rect(game.ekran, (20,20,30), (10, 40, 200, 30))
            game.ekran.blit(game.fk.render(f"{wname}: {game.ammo}", True, wr), (15, 45))

        # Power-up HUD
        puy = 75
        if game.hiz_t > 0:
            game.ekran.blit(game.fk.render(f"HIZ: {game.hiz_t//60}s", True, NM), (15, puy)); puy += 18
        if game.miknatis_t > 0:
            game.ekran.blit(game.fk.render(f"MIKNATIS: {game.miknatis_t//60}s", True, ALTIN), (15, puy)); puy += 18
        if game.cift_zipla_t > 0:
            game.ekran.blit(game.fk.render("CIFT ZIPLA: AKTIF", True, NY), (15, puy)); puy += 18
        if game.kalkan_t > 0:
            game.ekran.blit(game.fk.render("KALKAN: AKTIF", True, KR), (15, puy)); puy += 18
        if game.kalp_t > 0:
            game.ekran.blit(game.fk.render(f"KALP: {game.kalp_t//60}s", True, K), (15, puy)); puy += 18

        game.ekran.blit(game.fk.render("ESC: Men | SOL TIK: Ates | SPACE: Zipla", True, AGT), (10, YUKSEKLIK-30))

        # Boss can bar
        if game.boss_sv and game.boss_hp > 0:
            bbw = 300; bbx = GENISLIK//2 - bbw//2; bby = 55
            bcol = K if game.mv == "kis" else (ALTIN if game.mv == "yaz" else (YP if game.mv == "sonbahar" else C1))
            pygame.draw.rect(game.ekran, (40,0,0), (bbx, bby, bbw, 18))
            bo = game.boss_hp / game.boss_max_hp
            pygame.draw.rect(game.ekran, bcol, (bbx, bby, int(bbw*bo), 18))
            pygame.draw.rect(game.ekran, B, (bbx, bby, bbw, 18), 2)
            bn = BOSS_ADI.get(game.mv, "BOSS")
            game.ekran.blit(game.fk.render(bn, True, B), (bbx+5, bby-16))

        # Olum ekrani
        if game.cn <= 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,180))
            game.ekran.blit(k2, (0,0))
            game.ekran.blit(game.fb.render("OYUN BITTI", True, K), (GENISLIK//2-120, YUKSEKLIK//2-70))
            game.ekran.blit(game.f.render("R ile yeniden basla", True, B), (GENISLIK//2-110, YUKSEKLIK//2))
            if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NM):
                game.drm = "menu"; audio.sk.stop()

        # Tur bitis overlays
        if getattr(game, 'rnd_bitti', False) and game.cn > 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,140))
            game.ekran.blit(k2, (0,0))
            game.rnd_sayac += 1

            if game.boss_max_hp > 0 and game.boss_hp <= 0:
                # Boss yenildi
                od = game.mv
                if od not in game.envanter: game.envanter.append(od)
                if game.puan > game.yuksek_puan.get(od, 0): game.yuksek_puan[od] = game.puan
                if game.si < len(ms)-1:
                    game.ekran.blit(game.fb.render(f"{game.mv.upper()} GECTIN!", True, NY),
                               (GENISLIK//2-140, YUKSEKLIK//2-70))
                    game.ekran.blit(game.f.render(f"Odul: {KOSTUMLER[od]['i']}", True, ALTIN),
                               (GENISLIK//2-100, YUKSEKLIK//2))
                    if ui.btn("ILERLE", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NY):
                        game.si += 1
                        levels.lv_yukle(ms[game.si], 1)
                        game.cn = game.mc; game.rnd_bitti = False; game.boss_max_hp = 0
                else:
                    game.ekran.blit(game.fb.render("TUM MEVSIMLERI GECTIN!", True, ALTIN),
                               (GENISLIK//2-240, YUKSEKLIK//2-60))
                    game.ekran.blit(game.f.render("Tebrikler! Oyun bitti.", True, B),
                               (GENISLIK//2-100, YUKSEKLIK//2))
                    game.ekran.blit(game.fk.render(f"Odul: {KOSTUMLER[od]['i']} kazanildi!", True, ALTIN),
                               (GENISLIK//2-120, YUKSEKLIK//2+35))
                    if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+80, 200, 50, GT, AGT, NM):
                        game.drm = "menu"; audio.sk.stop(); game.rnd_bitti = False; game.boss_max_hp = 0
            elif game.boss_sv:
                # Boss aktif (devam etmek icin bekleme)
                pass
            elif game.rnd < 3:
                # Normal tur tamamlandi
                game.ekran.blit(game.fb.render(f"TUR {game.rnd} GECTIN!", True, NY),
                           (GENISLIK//2-130, YUKSEKLIK//2-60))
                game.ekran.blit(game.f.render(f"Siradaki: Tur {game.rnd+1}", True, B),
                           (GENISLIK//2-80, YUKSEKLIK//2))
                if game.rnd_sayac > 30:
                    game.rnd += 1
                    levels.lv_yukle(game.mv, game.rnd)
                    game.cn = game.mc; game.rnd_bitti = False
            elif game.rnd == 3:
                # Tum normal turlar bitti, boss'a gecis
                game.ekran.blit(game.fb.render("TUM TURLAR GECTIN!", True, ALTIN),
                           (GENISLIK//2-150, YUKSEKLIK//2-60))
                game.ekran.blit(game.f.render("BOSSA HAZIR OL!", True, K),
                           (GENISLIK//2-90, YUKSEKLIK//2))
                if ui.btn("BOSSA GIT", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NM):
                    game.rnd = 4
                    levels.lv_yukle(game.mv, 4)
                    game.cn = game.mc; game.rnd_bitti = False

    pygame.display.flip()
    game.saat.tick(60)

pygame.quit()
