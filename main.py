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
import levels
import screens
import player
import save
game.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mevsimler Oyunu")
game.saat = pygame.time.Clock()
game.f = pygame.font.Font(None, 36)
game.fb = pygame.font.Font(None, 60)
game.fk = pygame.font.Font(None, 24)
game.fm = pygame.font.Font(None, 48)

game.mv = ms[0]
game.rnk = MEV[ms[0]]
game.lvl = {}
game.oy = YUKSEKLIK - 100
game.cn = 5
particles.bg_par_baslat()

# Joystick / tus durumu
joy_x = 0
joy_y = 0
joy_tut = False
joy_mx = 0
joy_my = 0
fire_btn_tut = False

cal = True

while cal:
    game.ft = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cal = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: game.ft = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.drm == "oyun": game.drm = "settings"
                elif game.drm == "settings": game.drm = "oyun"
            if game.drm == "oyun":
                if event.key == pygame.K_SPACE:
                    if game.yr:
                        game.hy = game.zg
                        audio.sfx_ziplama()
                        particles.ptk_ekle(game.ox, game.oy+20, NM, 5)
                    elif game.cift_zipla_t > 0 and game.cift_zipla_kalan > 0:
                        game.hy = game.zg * 0.85
                        game.cift_zipla_kalan -= 1
                        audio.sfx_cift_ziplama()
                        particles.ptk_ekle(game.ox, game.oy+20, NM, 5)
                        particles.ptk_patlatma(game.ox, game.oy, NM, 5)
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

        ts = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()

        # Joystick kontrol (sol alt, daha kucuk)
        joy_merkez_x = 55
        joy_merkez_y = YUKSEKLIK - 60
        joy_r = 28
        joy_tut = pygame.mouse.get_pressed()[0] and math.sqrt((mx - joy_merkez_x)**2 + (my - joy_merkez_y)**2) < joy_r * 2
        if joy_tut:
            dx = mx - joy_merkez_x
            dy = my - joy_merkez_y
            d = math.sqrt(dx*dx + dy*dy)
            if d > joy_r:
                dx = dx / d * joy_r
                dy = dy / d * joy_r
            joy_x = dx / joy_r
            joy_y = dy / joy_r
        else:
            joy_x = ts[pygame.K_d] - ts[pygame.K_a]
            joy_y = 0

        # Alev topu tusu (sag alt)
        fire_btn_x = GENISLIK - 55
        fire_btn_y = YUKSEKLIK - 60
        fire_btn_r = 28
        fire_btn_tut = pygame.mouse.get_pressed()[2] and math.sqrt((mx - fire_btn_x)**2 + (my - fire_btn_y)**2) < fire_btn_r

        spd = 5 + (2 if game.hiz_t > 0 else 0)
        game.hx = joy_x * spd
        if joy_x > 0.3: game.yn = 1
        elif joy_x < -0.3: game.yn = -1

        # Sol tik ile ates (ikonlara tiklamayi algilama)
        if pygame.mouse.get_pressed()[0] and not joy_tut and game.weapon and game.ammo > 0 and game.shoot_cd <= 0 and my < YUKSEKLIK - 120 and not (mx > GENISLIK - 250 and my < 55):
            arad = -1 if game.yn < 0 else 1
            wd = WP_DATA[game.mv]
            shot_spd = wd["spd"]
            if game.shoot_cd > wd["cd"] - 3:
                vy_b = -2
            else:
                vy_b = -1.5 + math.sin(game.sz * 4) * 1.5
            game.bullets.append({"x": game.ox, "y": game.oy-20, "vx": shot_spd*arad, "vy": vy_b, "r": wd["r"], "dmg": wd["dmg"], "t": wd["s"], "mv": game.mv})
            game.ammo -= 1
            game.shoot_cd = wd["cd"]
            audio.sfx_ates()
            particles.ptk_patlatma(game.ox + arad*20, game.oy-20, wd["r"], 6, 3)
            for _ in range(3):
                particles.ptk_ekle(game.ox + arad*20, game.oy-20, (200, 200, 200), 1)

        # Sag tik / tus ile alev topu (ikonlara tiklamayi algilama)
        if (fire_btn_tut or (pygame.mouse.get_pressed()[2] and my < YUKSEKLIK - 120 and not (mx > GENISLIK - 250 and my < 55))) and game.fire_cd <= 0:
            arad = -1 if game.yn < 0 else 1
            game.fireballs.append({"x": game.ox, "y": game.oy-20, "vx": 8*arad, "vy": -3, "t": 0})
            game.fire_cd = 300
            audio.sfx_ates()
            particles.ptk_patlatma(game.ox + arad*20, game.oy-20, (255, 100, 0), 12, 5)
            particles.ptk_patlatma(game.ox + arad*20, game.oy-20, (255, 200, 50), 8, 3)

        if game.shoot_cd > 0: game.shoot_cd -= 1
        if game.fire_cd > 0: game.fire_cd -= 1

        oc = pygame.Rect(game.ox-14, game.oy-50, 28, 75)
        oy2 = game.oy

        # Hareketli platform
        for mp in game.mpl:
            mp["t"] += mp["spd"] * 0.02
            ny = mp["by"] + math.sin(mp["t"]) * mp["dy"]
            nx = mp["bx"] + math.sin(mp["t"]) * mp["dx"]
            mp["vx"] = nx - mp["r"].x
            mp["vy"] = ny - mp["r"].y
            mp["r"].x = nx
            mp["r"].y = ny

        # Yatay
        game.ox += game.hx; oc.x = game.ox-14
        for p in game.plt:
            if oc.colliderect(p):
                if game.hx > 0: oc.right = p.left; game.ox = oc.x+14
                elif game.hx < 0: oc.left = p.right; game.ox = oc.x+14
        for mp in game.mpl:
            if oc.colliderect(mp["r"]):
                if game.hx > 0: oc.right = mp["r"].left; game.ox = oc.x+14
                elif game.hx < 0: oc.left = mp["r"].right; game.ox = oc.x+14

        # Dikey
        game.hy += game.yc; game.oy += game.hy
        oc.x = game.ox-14; oc.y = game.oy-50

        game.yr = False; mpl_u = -1
        for p in game.plt:
            if oc.colliderect(p):
                if game.hy > 0:
                    if not game.yr and oy2 < p.top: particles.ptk_ekle(game.ox, p.top, game.rnk["z"], 4)
                    oc.bottom = p.top; game.oy = oc.y+50; game.hy = 0; game.yr = True; game.cift_zipla_kalan = 1
                elif game.hy < 0: oc.top = p.bottom; game.oy = oc.y+50; game.hy = 0

        for i, mp in enumerate(game.mpl):
            if oc.colliderect(mp["r"]):
                if game.hy >= 0 and oy2 + 25 < mp["r"].top + 20:
                    if not game.yr: particles.ptk_ekle(game.ox, mp["r"].top, game.rnk["z"], 3)
                    oc.bottom = mp["r"].top; game.oy = oc.y+50; game.hy = 0; game.yr = True; game.dj_k = False
                    mpl_u = i
                elif game.hy < 0:
                    oc.top = mp["r"].bottom; game.oy = oc.y+50; game.hy = 0

        if mpl_u >= 0:
            game.ox += game.mpl[mpl_u]["vx"]
            game.oy += game.mpl[mpl_u]["vy"]

        # Prism
        for pr in game.prl[:]:
            if oc.colliderect(pygame.Rect(pr[0]-10, pr[1]-10, 20, 20)):
                game.prl.remove(pr); particles.ptk_ekle(pr[0], pr[1], ALTIN, 10)
                game.puan += 100 + max(0, 50 - len(game.prl)*5)
                audio.sfx_topla()

        if game.miknatis_t > 0:
            for pr in game.prl[:]:
                dx = game.ox - pr[0]; dy = game.oy - pr[1]
                d = math.sqrt(dx*dx + dy*dy)
                if d < 200 and d > 0:
                    game.prl.remove(pr); particles.ptk_ekle(pr[0], pr[1], ALTIN, 8)
                    game.puan += 100 + max(0, 50 - len(game.prl)*5)
                    audio.sfx_topla()

        # Dikenler
        for t in game.tzl:
            if oc.colliderect(t):
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_ekle(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0; break

        # Dusman AI
        for d in game.dsm:
            if d["tip"] == "kovalayan":
                dx = game.ox - d["r"].centerx
                dy = game.oy - d["r"].centery
                mesafe = math.sqrt(dx*dx + dy*dy)
                if mesafe < 350:
                    hiz = d["orj_h"] * 1.8
                    d["r"].x += (dx / mesafe) * hiz if mesafe > 0 else 0
                    d["r"].y += (dy / mesafe) * hiz * 0.4 if mesafe > 0 else 0
                    if d["r"].x < d["sl"]: d["r"].x = d["sl"]
                    if d["r"].x > d["sg"]: d["r"].x = d["sg"]
                    if d["r"].y < 50: d["r"].y = 50
                    if d["r"].y > YUKSEKLIK - 80: d["r"].y = YUKSEKLIK - 80
                    # Ates et (kovalayan tipler)
                    if d.get("ates_cd", 0) <= 0 and mesafe < 250 and random.random() < 0.02:
                        game.boss_btl.append({"x": d["r"].centerx, "y": d["r"].centery, "vx": (dx/mesafe)*2, "vy": (dy/mesafe)*2, "r": K})
                        d["ates_cd"] = random.randint(60, 120)
                    else:
                        d["ates_cd"] = max(0, d.get("ates_cd", 0) - 1)
                else:
                    d["r"].x += d["h"]
                    if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]: d["h"] *= -1
            else:
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

        # Boss muhafiz AI
        for mu in game.boss_muh[:]:
            dx = game.ox - mu["r"].centerx
            dy = game.oy - mu["r"].centery
            mesafe = math.sqrt(dx*dx + dy*dy)
            if mesafe < 300:
                mu["r"].x += (dx/mesafe) * mu["h"] if mesafe > 0 else 0
                mu["r"].y += (dy/mesafe) * mu["h"] * 0.3 if mesafe > 0 else 0
                if mu["r"].x < mu["sl"]: mu["r"].x = mu["sl"]
                if mu["r"].x > mu["sg"]: mu["r"].x = mu["sg"]
                if mu["r"].y < 80: mu["r"].y = 80
                if mu["r"].y > YUKSEKLIK - 80: mu["r"].y = YUKSEKLIK - 80
                if mu.get("ates_cd", 0) <= 0 and mesafe < 400:
                    game.boss_btl.append({"x": mu["r"].centerx, "y": mu["r"].centery, "vx": (dx/mesafe)*2.5, "vy": (dy/mesafe)*2.5, "r": (255, 100, 100)})
                    mu["ates_cd"] = random.randint(80, 150)
                else:
                    mu["ates_cd"] = max(0, mu.get("ates_cd", 0) - 1)
            if oc.colliderect(mu["r"]):
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_patlatma(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0

        # Checkpoint
        if game.lvl and isinstance(game.lvl, dict) and game.lvl.get("cp"):
            cpx, cpy = game.lvl["cp"]
            if abs(game.ox - cpx) < 30 and abs(game.oy - cpy) < 30:
                if game.cp_x != cpx or game.cp_y != cpy:
                    game.cp_x, game.cp_y = cpx, cpy
                    audio.sfx_checkpoint()
                    particles.ptk_ekle(cpx, cpy, NM, 12)

        # Power-up
        if game.lvl and isinstance(game.lvl, dict):
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

        # Mermi paketi
        if game.lvl and isinstance(game.lvl, dict):
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
                    d["hp"] -= 1
                    particles.ptk_patlatma(b["x"], b["y"], KR, 12)
                    audio.sfx_hasar(); hit = True
                    if d["hp"] <= 0:
                        game.dsm.remove(d)
                        particles.ptk_patlatma(b["x"], b["y"], b["r"], 15)
                    break
            if hit: game.bullets.remove(b); continue
            for mu in game.boss_muh[:]:
                if br.colliderect(mu["r"]):
                    mu["hp"] -= 1
                    particles.ptk_patlatma(b["x"], b["y"], KR, 10)
                    audio.sfx_hasar()
                    if mu["hp"] <= 0:
                        game.boss_muh.remove(mu)
                        particles.ptk_patlatma(b["x"], b["y"], ALTIN, 15)
                    hit = True; break
            if hit: game.bullets.remove(b); continue
            if game.boss_sv and game.boss_hp > 0:
                if br.colliderect(pygame.Rect(game.boss_x-35, game.boss_y-35, 70, 70)):
                    game.boss_hp -= b["dmg"]
                    game.bullets.remove(b)
                    audio.sfx_boss_hit()
                    particles.ptk_patlatma(b["x"], b["y"], b["r"], 12)

        # Boss mermisi
        for b in game.boss_btl[:]:
            b["x"] += b["vx"]; b["y"] += b["vy"]
            b["vy"] += 0.05
            if b["x"] < -20 or b["x"] > GENISLIK+20 or b["y"] < -20 or b["y"] > YUKSEKLIK+20:
                game.boss_btl.remove(b); continue
            if b.get("fake"): continue
            bs2 = b.get("s", 6)
            br = pygame.Rect(b["x"]-bs2//2-1, b["y"]-bs2//2-1, bs2+2, bs2+2)
            if oc.colliderect(br):
                game.boss_btl.remove(b)
                if game.kalkan_t > 0:
                    game.kalkan_t = 0; particles.ptk_patlatma(game.ox, game.oy, KR, 15)
                    audio.sfx_hasar()
                else:
                    game.cn -= 1; particles.ptk_ekle(game.ox, game.oy, K, 12)
                    audio.sfx_hasar()
                    game.ox, game.oy = game.cp_x, game.cp_y; game.hx = game.hy = 0

        # Alev topu
        for fb in game.fireballs[:]:
            fb["x"] += fb["vx"]; fb["y"] += fb["vy"]
            fb["vy"] += 0.05
            fb["t"] += 1
            if fb["t"] > 60 or fb["x"] < -30 or fb["x"] > GENISLIK+30 or fb["y"] < -30 or fb["y"] > YUKSEKLIK+30:
                game.fireballs.remove(fb); continue
            fbr = pygame.Rect(fb["x"]-12, fb["y"]-12, 24, 24)
            hit = False
            particles.ptk_ekle(int(fb["x"]-5+random.random()*10), int(fb["y"]-5+random.random()*10), (255, random.randint(100,200), 0), 3)
            for d in game.dsm[:]:
                if fbr.colliderect(d["r"]):
                    d["hp"] -= 5
                    particles.ptk_patlatma(fb["x"], fb["y"], KR, 20)
                    audio.sfx_hasar(); hit = True
                    if d["hp"] <= 0:
                        game.dsm.remove(d)
                        particles.ptk_patlatma(fb["x"], fb["y"], (255, 100, 0), 30)
                    break
            if hit: game.fireballs.remove(fb); continue
            for mu in game.boss_muh[:]:
                if fbr.colliderect(mu["r"]):
                    mu["hp"] -= 5
                    particles.ptk_patlatma(fb["x"], fb["y"], KR, 18)
                    audio.sfx_hasar()
                    if mu["hp"] <= 0:
                        game.boss_muh.remove(mu)
                        particles.ptk_patlatma(fb["x"], fb["y"], ALTIN, 25)
                    hit = True; break
            if hit: game.fireballs.remove(fb); continue
            if game.boss_sv and game.boss_hp > 0:
                if fbr.colliderect(pygame.Rect(game.boss_x-35, game.boss_y-35, 70, 70)):
                    game.boss_hp -= 10
                    game.fireballs.remove(fb)
                    audio.sfx_boss_hit()
                    particles.ptk_patlatma(fb["x"], fb["y"], (255, 100, 0), 30)
                    particles.ptk_patlatma(fb["x"], fb["y"], ALTIN, 15)

        # Boss AI (gelişmiş: dikey hareket, takip, biyom özel yetenek)
        if game.boss_sv and game.boss_hp > 0:
            bx = game.boss_x
            by = game.boss_y
            bm = game.mv
            game.boss_timer += 1
            game.boss_atk_cd -= 1
            game.boss_ozel_yetenek_cd -= 1
            game.boss_lazer_t = max(0, game.boss_lazer_t - 1)
            game.boss_minyon_t = max(0, game.boss_minyon_t - 1)
            game.boss_dalga_t = max(0, game.boss_dalga_t - 1)

            # Hareket modu (0: yatay, 1: takip, 2: iniş-çıkış, 3: bekle)
            if game.boss_timer % 180 == 0:
                game.boss_hareket_mod = random.randint(0, 3)
                game.boss_yon_degis = game.boss_timer + random.randint(60, 180)

            if game.boss_hareket_mod == 0:
                # Yatay git-gel + hafif sinüs
                game.boss_x += game.boss_vx * game.boss_dir
                if game.boss_x < 100 or game.boss_x > GENISLIK - 100:
                    game.boss_dir *= -1
                game.boss_y = 80 + math.sin(game.boss_timer * 0.03) * 40
            elif game.boss_hareket_mod == 1:
                # Oyuncuyu takip et (3sn, sonra yataya dön)
                dx = game.ox - bx
                dy = game.oy - by
                d = math.sqrt(dx*dx + dy*dy)
                if d > 0:
                    game.boss_x += (dx/d) * game.boss_vx * 1.5
                    game.boss_y += (dy/d) * game.boss_vx * 0.8
                game.boss_hedefle = True
                if game.boss_timer > game.boss_yon_degis:
                    game.boss_hareket_mod = 0
                    game.boss_hedefle = False
            elif game.boss_hareket_mod == 2:
                # İniş-çıkış: aşağı in, yatay hareket et, yukarı çık
                cyc = (game.boss_timer % 120) / 120.0
                game.boss_y = 80 + math.sin(cyc * math.pi * 2) * 100
                game.boss_x += game.boss_vx * game.boss_dir * 0.5
                if game.boss_x < 100 or game.boss_x > GENISLIK - 100:
                    game.boss_dir *= -1
            else:
                # Bekleme: sabit dur, etrafa bak
                pass

            # Sinirlar
            game.boss_x = max(60, min(GENISLIK - 60, game.boss_x))
            game.boss_y = max(40, min(YUKSEKLIK - 200, game.boss_y))

            # Normal saldiri desenleri (her biyomda ortak)
            if game.boss_atk_cd <= 0:
                ptrn = game.boss_ptrn % 4
                zorluk_hiz = BOSS_ATK_CD[game.ayar["z"]]
                spd = 3 + random.uniform(-0.5, 0.5)
                if ptrn == 0:
                    # Tek hedef mermisi
                    dx = game.ox - bx; dy = game.oy - by
                    d = math.sqrt(dx*dx + dy*dy)
                    if d > 0:
                        game.boss_btl.append({"x": bx, "y": by+30, "vx": dx/d*spd, "vy": dy/d*spd, "r": K})
                    game.boss_atk_cd = max(60, zorluk_hiz*2 - game.boss_ptrn*2)
                elif ptrn == 1:
                    # 3'lü yelpaze
                    for li in range(-1, 2):
                        dx = game.ox - bx + li*40; dy = game.oy - by
                        d = math.sqrt(dx*dx + dy*dy)
                        if d > 0:
                            game.boss_btl.append({"x": bx + li*15, "y": by+30, "vx": dx/d*(spd+0.5), "vy": dy/d*(spd+0.5), "r": (255, 100, 100)})
                    game.boss_atk_cd = max(80, zorluk_hiz*2 - game.boss_ptrn*2)
                elif ptrn == 2:
                    # 5'li dalga (bazilari yalancı)
                    for wi in range(5):
                        a3 = -1 + wi * 0.5
                        dx = game.ox - bx + a3*80; dy = game.oy - by
                        d = math.sqrt(dx*dx + dy*dy)
                        if d > 0:
                            fake = random.random() < 0.3
                            game.boss_btl.append({"x": bx + wi*8, "y": by+30, "vx": dx/d*(spd-0.5) + random.uniform(-0.3, 0.3), "vy": dy/d*(spd-0.5) + random.uniform(-0.5, 0.5), "r": (200, 50, 200), "s": 8 if not fake else 4, "fake": fake})
                    game.boss_atk_cd = max(100, zorluk_hiz*2 - game.boss_ptrn*2)
                else:
                    # Dairesel fıskiye
                    for ai in range(8):
                        a5 = ai * 0.785 + game.boss_timer * 0.02
                        game.boss_btl.append({"x": bx, "y": by+30, "vx": math.cos(a5)*spd, "vy": math.sin(a5)*spd, "r": (255, 50, 255)})
                    game.boss_atk_cd = max(120, zorluk_hiz*2)

                game.boss_ptrn = (game.boss_ptrn + 1) % 8
                audio.sfx_boss_ates()

            # Biyom özel yetenekleri
            if game.boss_ozel_yetenek_cd <= 0:
                bm_spd = 2 + random.uniform(-0.5, 0.5)
                if bm == "ilkbahar":
                    # Cicek tohumu: etrafa yayilan, yavas hareket eden mermiler
                    for bi in range(6):
                        a6 = bi * 1.047 + game.boss_timer * 0.01
                        game.boss_btl.append({"x": bx, "y": by+30, "vx": math.cos(a6)*bm_spd*0.6, "vy": math.sin(a6)*bm_spd*0.6, "r": (255, 100, 200), "s": 6})
                    game.boss_ozel_yetenek_cd = max(200, 350 - game.boss_ptrn*3)
                    game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (255, 200, 255), "tip": "cicek"})
                elif bm == "yaz":
                    # Alev dalgasi: yere dogru 5 mermi, yavas
                    for bi in range(5):
                        dx = game.ox - bx + random.randint(-50, 50)
                        dy = game.oy - by + 100
                        d = math.sqrt(dx*dx + dy*dy)
                        if d > 0:
                            game.boss_btl.append({"x": bx + random.randint(-20, 20), "y": by+30, "vx": dx/d*bm_spd*1.2, "vy": dy/d*bm_spd*1.2, "r": (255, 150, 0), "s": 10})
                    game.boss_ozel_yetenek_cd = max(220, 380 - game.boss_ptrn*3)
                    game.boss_ozel_efekt.append({"t": 25, "x": bx, "y": by, "r": (255, 200, 0), "tip": "alev"})
                elif bm == "sonbahar":
                    # Yaprak firtinasi: spiral mermiler (bazilari gosterlik)
                    for bi in range(12):
                        a7 = bi * 0.524 + game.boss_timer * 0.03
                        fake = random.random() < 0.4
                        game.boss_btl.append({"x": bx, "y": by+20, "vx": math.cos(a7)*bm_spd*0.8, "vy": math.sin(a7)*bm_spd*0.8, "r": (200, 120, 50), "s": 5 if not fake else 3, "fake": fake})
                    game.boss_ozel_yetenek_cd = max(180, 350 - game.boss_ptrn*3)
                    game.boss_ozel_efekt.append({"t": 30, "x": bx, "y": by, "r": (200, 150, 50), "tip": "yaprak"})
                elif bm == "kis":
                    # Buz sivri: gokten yere dogru hizli mermiler
                    for bi in range(4):
                        game.boss_btl.append({"x": game.ox + random.randint(-100, 100), "y": -20, "vx": 0, "vy": bm_spd*1.5, "r": (180, 220, 255), "s": 7})
                    game.boss_ozel_yetenek_cd = max(150, 300 - game.boss_ptrn*3)
                    game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (200, 230, 255), "tip": "buz"})
                audio.sfx_boss_ates()

            # Ozel efektleri guncelle
            for ef in game.boss_ozel_efekt[:]:
                ef["t"] -= 1
                if ef["t"] <= 0:
                    game.boss_ozel_efekt.remove(ef)

        # Boss olumu
        if game.boss_sv and game.boss_hp <= 0 and game.cn > 0:
            game.boss_sv = False
            audio.sfx_boss_ol()
            particles.ptk_patlatma(int(game.boss_x), int(game.boss_y), ALTIN, 40, 8)
            particles.ptk_patlatma(int(game.boss_x), int(game.boss_y), NM, 30, 6)

        # Tur bitis
        if len(game.prl) == 0 and game.cn > 0 and not game.boss_sv:
            if not hasattr(game, 'rnd_bitti') or not game.rnd_bitti:
                game.rnd_bitti = True
                game.rnd_sayac = 0
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, NM, 20)
                particles.ptk_ekle(GENISLIK//2, YUKSEKLIK//2, ALTIN, 12)
        elif game.boss_sv and game.boss_hp <= 0 and game.cn > 0:
            if not getattr(game, 'rnd_bitti', False):
                game.rnd_bitti = True
                game.rnd_sayac = 0

        # Power-up sure
        if game.hiz_t > 0: game.hiz_t -= 1
        if game.miknatis_t > 0: game.miknatis_t -= 1

        particles.ptk_guncelle()

        # CIZIM
        particles.ark_ciz()

        # Terraria platformlari
        levels.platform_ciz()

        # Diken ciz
        for t in game.tzl:
            cx, cy = t.centerx, t.centery
            for si in range(5):
                sx = cx - 16 + si * 8
                pygame.draw.polygon(game.ekran, (140, 140, 140), [(sx, cy+8), (sx+3, cy-10), (sx+6, cy+8)])
                pygame.draw.polygon(game.ekran, (200, 200, 200), [(sx, cy+8), (sx+3, cy-10), (sx+6, cy+8)], 1)
            pygame.draw.rect(game.ekran, (100, 100, 100), (cx-18, cy+6, 36, 6))
            pygame.draw.line(game.ekran, (80, 80, 80), (cx-18, cy+9), (cx+18, cy+9), 2)

        # Prism
        for pr in game.prl:
            pygame.draw.circle(game.ekran, ALTIN, (pr[0], pr[1]), 10)
            pygame.draw.circle(game.ekran, (255,200,0), (pr[0], pr[1]), 7)
            pygame.draw.circle(game.ekran, B, (pr[0]-3, pr[1]-3), 3)

        # Dusman
        for d in game.dsm:
            levels.dusman_ciz(d)

        # Muhafiz
        for mu in game.boss_muh:
            levels.muhafiz_ciz(mu)

        # Mermi
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

        # Boss mermisi (biyom renkli, yalancilar farkli)
        for b in game.boss_btl:
            bs = b.get("s", 6)
            if b.get("fake"):
                pygame.draw.circle(game.ekran, (100, 100, 100, 80), (int(b["x"]), int(b["y"])), bs)
                pygame.draw.circle(game.ekran, (150, 150, 150, 120), (int(b["x"]), int(b["y"])), bs, 1)
                pygame.draw.line(game.ekran, (200, 200, 200), (int(b["x"])-3, int(b["y"])-3), (int(b["x"])+3, int(b["y"])+3), 1)
            else:
                rnk = b.get("r", K)
                pygame.draw.circle(game.ekran, rnk, (int(b["x"]), int(b["y"])), bs)
                pygame.draw.circle(game.ekran, B, (int(b["x"]), int(b["y"])), bs-2, 1)
                # Parlama efekti
                if bs > 6:
                    pygame.draw.circle(game.ekran, B, (int(b["x"])-2, int(b["y"])-2), bs//3)

        # Alev topu (animasyonlu)
        for fb in game.fireballs:
            flicker = random.randint(-3, 3)
            fx, fy = int(fb["x"]), int(fb["y"])
            # Dis alev
            for ri in range(4):
                a4 = fb["t"] * 0.5 + ri * 1.57
                r2 = 14 + int(math.sin(fb["t"] * 0.3 + ri) * 4)
                pygame.draw.circle(game.ekran, (200, 50, 0, 100), (fx+int(math.cos(a4)*3), fy+int(math.sin(a4)*3)), r2)
            # Ic katmanlar
            pygame.draw.circle(game.ekran, (200, 50, 0), (fx+flicker, fy+flicker), 16)
            pygame.draw.circle(game.ekran, (255, 100, 0), (fx, fy), 12)
            pygame.draw.circle(game.ekran, (255, 200, 50), (fx-2, fy-2), 7)
            pygame.draw.circle(game.ekran, (255, 255, 200), (fx-4, fy-4), 4)
            # Savrulan alev parcaciklari
            for fi in range(5):
                a3 = fb["t"] * 0.4 + fi * 1.26
                r3 = random.randint(2, 5)
                pygame.draw.circle(game.ekran, (255, random.randint(50, 150), 0), (fx+int(math.cos(a3+random.random())*14), fy+int(math.sin(a3+random.random())*14)), r3)
            # Duman efekti
            if fb["t"] % 3 == 0:
                particles.ptk_ekle(fx+random.randint(-5,5), fy+random.randint(-5,5), (100, 100, 100), 2)

        # Power-up
        if game.lvl and isinstance(game.lvl, dict):
            for pu in game.lvl.get("pu", []):
                pux, puy, put = pu
                puy2 = puy + math.sin(game.sz * 2 + pux * 0.1) * 3
                if put == "hiz":
                    pygame.draw.polygon(game.ekran, NM, [(pux, puy2-7),(pux-6,puy2+5),(pux+6,puy2+5)])
                    pygame.draw.polygon(game.ekran, B, [(pux, puy2-7),(pux-6,puy2+5),(pux+6,puy2+5)], 1)
                elif put == "kalkan":
                    pygame.draw.circle(game.ekran, KR, (pux, puy2), 8, 2)
                    pygame.draw.circle(game.ekran, KR, (pux, puy2), 3)
                elif put == "cift_zipla":
                    pygame.draw.polygon(game.ekran, NY, [(pux, puy2+5),(pux-6,puy2-4),(pux+6,puy2-4)])
                    pygame.draw.polygon(game.ekran, B, [(pux, puy2+5),(pux-6,puy2-4),(pux+6,puy2-4)], 1)
                elif put == "miknatis":
                    pygame.draw.circle(game.ekran, ALTIN, (pux, puy2), 7)
                    pygame.draw.circle(game.ekran, B, (pux, puy2), 4)
                elif put == "kalp":
                    pygame.draw.polygon(game.ekran, K, [(pux, puy2+5),(pux-7,puy2-2),(pux+7,puy2-2)])
                    pygame.draw.polygon(game.ekran, B, [(pux, puy2+5),(pux-7,puy2-2),(pux+7,puy2-2)], 1)

        # Mermi paketi
        if game.lvl and isinstance(game.lvl, dict):
            for wp in game.lvl.get("wp", []):
                wpx, wpy = wp
                wr = WP_DATA[game.mv]["r"]
                pygame.draw.rect(game.ekran, wr, (wpx-6, wpy-4, 12, 8))
                pygame.draw.rect(game.ekran, B, (wpx-6, wpy-4, 12, 8), 1)

        # Boss ciz
        levels.boss_ciz()

        # Boss ozel efekt cizimi
        for ef in game.boss_ozel_efekt:
            efx, efy = int(ef["x"]), int(ef["y"])
            if ef["tip"] == "cicek":
                for ci in range(6):
                    a8 = ci * 1.047 + game.sz * 0.1
                    pygame.draw.circle(game.ekran, (255, 150, 200), (efx+int(math.cos(a8)*15), efy+int(math.sin(a8)*15)), 5)
                    pygame.draw.circle(game.ekran, (255, 200, 220), (efx+int(math.cos(a8)*10), efy+int(math.sin(a8)*10)), 3)
            elif ef["tip"] == "alev":
                for ai2 in range(8):
                    a9 = ai2 * 0.785 + game.sz * 0.2
                    r9 = random.randint(5, 12)
                    pygame.draw.circle(game.ekran, (255, random.randint(50, 150), 0), (efx+int(math.cos(a9)*r9), efy+int(math.sin(a9)*r9)), 4)
            elif ef["tip"] == "yaprak":
                for yi in range(8):
                    a10 = yi * 0.785 + game.sz * 0.15
                    pygame.draw.ellipse(game.ekran, (200, 150, 50), (efx+int(math.cos(a10)*18)-4, efy+int(math.sin(a10)*18)-2, 8, 4))
            elif ef["tip"] == "buz":
                for zi in range(6):
                    a11 = zi * 1.047 + game.sz * 0.05
                    pygame.draw.line(game.ekran, (200, 230, 255), (efx+int(math.cos(a11)*12), efy+int(math.sin(a11)*12)), (efx+int(math.cos(a11)*20), efy+int(math.sin(a11)*20)), 3)
                    pygame.draw.line(game.ekran, (255, 255, 255), (efx+int(math.cos(a11)*14), efy+int(math.sin(a11)*14)), (efx+int(math.cos(a11)*18), efy+int(math.sin(a11)*18)), 1)

        particles.ptk_ciz()

        # Karakter
        yy = abs(math.sin(game.sz*2))*1.2 if game.yr and abs(game.hx)<0.5 else 0
        player.ciz_krk(game.ox, game.oy, game.yn, yy)

        if game.kalkan_t > 0:
            pygame.draw.circle(game.ekran, KR, (int(game.ox), int(game.oy-20)), 40, 3)

        # HUD
        if ui.ikon(GENISLIK-130, 10, "A", NM): game.onceki_drm = game.drm; game.drm = "settings"
        if ui.ikon(GENISLIK-86, 10, "R", NY):
            game.cn = game.mc
            game.ox, game.oy = game.cp_x, game.cp_y
            game.hx = game.hy = 0
        if ui.ikon(GENISLIK-42, 10, "M", K): game.drm = "menu"; audio.muzik_durdur(); save.kaydet()
        if ui.ikon(GENISLIK-174, 10, "S", NM if game.ses_acik else K):
            game.ses_acik = not game.ses_acik
            audio.sfx_ses_ayarla()
        if ui.disket(GENISLIK-218, 10):
            save.kaydet()

        # Can bar
        bw = 200
        pygame.draw.rect(game.ekran, (60,0,0), (GENISLIK-bw-20, 55, bw, 20))
        co = game.cn/game.mc if game.mc > 0 else 0
        pygame.draw.rect(game.ekran, (0,255,100) if co>0.5 else (255,255,0) if co>0.25 else (255,50,50), (GENISLIK-bw-20, 55, int(bw*co), 20))
        pygame.draw.rect(game.ekran, B, (GENISLIK-bw-20, 55, bw, 20), 2)
        game.ekran.blit(game.fk.render("CAN", True, B), (GENISLIK-bw-60, 57))
        game.ekran.blit(game.fk.render(f"{game.mv.upper()} - Tur {game.rnd}/16 - {game.ayar['z'].upper()}", True, B), (GENISLIK//2-160, 12))
        game.ekran.blit(game.f.render(f"Puan: {game.puan}", True, NP), (10, 10))

        if game.yuksek_puan.get(game.mv, 0) > 0:
            game.ekran.blit(game.fk.render(f"En Yuksek: {game.yuksek_puan[game.mv]}", True, ALTIN), (10, 30))

        # Silah
        if game.weapon:
            wr = WP_DATA[game.mv]["r"]
            wname = WP_DATA[game.mv]["i"]
            pygame.draw.rect(game.ekran, (20,20,30), (10, 40, 200, 30))
            game.ekran.blit(game.fk.render(f"{wname}: {game.ammo}", True, wr), (15, 45))

        puy = 75
        if game.hiz_t > 0:
            game.ekran.blit(game.fk.render(f"HIZ: {game.hiz_t//60}s", True, NM), (15, puy)); puy += 18
        if game.miknatis_t > 0:
            game.ekran.blit(game.fk.render(f"MIKNATIS: {game.miknatis_t//60}s", True, ALTIN), (15, puy)); puy += 18
        if game.cift_zipla_t > 0:
            game.ekran.blit(game.fk.render("CIFT ZIPLA: AKTIF", True, NY), (15, puy)); puy += 18
        if game.kalkan_t > 0:
            game.ekran.blit(game.fk.render("KALKAN: AKTIF", True, KR), (15, puy)); puy += 18

        game.ekran.blit(game.fk.render("ESC: Men | SOL TIK: Ates | SAG TIK: Alev | SPACE: Zipla", True, AGT), (10, YUKSEKLIK-30))

        # Joystick ciz (yarim saydam)
        js = pygame.Surface(((joy_r+16)*2, (joy_r+16)*2), pygame.SRCALPHA)
        pygame.draw.circle(js, (40, 40, 60, 100), (joy_r+16, joy_r+16), joy_r + 12)
        pygame.draw.circle(js, (60, 60, 80, 150), (joy_r+16, joy_r+16), joy_r + 12, 2)
        pygame.draw.circle(js, (80, 80, 120, 150), (joy_r+16 + int(joy_x * joy_r), joy_r+16 + int(joy_y * joy_r)), 14)
        pygame.draw.circle(js, NP + (200,), (joy_r+16 + int(joy_x * joy_r), joy_r+16 + int(joy_y * joy_r)), 14, 2)
        game.ekran.blit(js, (joy_merkez_x - joy_r - 16, joy_merkez_y - joy_r - 16))

        # Alev topu tusu (yarim saydam)
        fs = pygame.Surface(((fire_btn_r+12)*2, (fire_btn_r+12)*2), pygame.SRCALPHA)
        fire_renk = (200, 100, 0) if game.fire_cd <= 0 else (60, 60, 60)
        pygame.draw.circle(fs, (40, 20, 0, 120), (fire_btn_r+12, fire_btn_r+12), fire_btn_r + 8)
        pygame.draw.circle(fs, fire_renk + (180,), (fire_btn_r+12, fire_btn_r+12), fire_btn_r)
        pygame.draw.circle(fs, (255, 200, 50, 200), (fire_btn_r+14, fire_btn_r+14), fire_btn_r, 2)
        if game.fire_cd > 0:
            cd_oran = game.fire_cd / 300
            pygame.draw.arc(fs, (60, 60, 60, 200), (4, 4, fire_btn_r*2+16, fire_btn_r*2+16), 0, cd_oran * math.pi * 2, 4)
        for fi in range(3):
            fa = game.sz * 0.2 + fi * 2.1
            fx2 = fire_btn_r+12 + int(math.cos(fa) * 7)
            fy2 = fire_btn_r+8 + int(math.sin(fa) * 7)
            pygame.draw.circle(fs, (255, 150, 0, 200), (fx2, fy2), 4)
            pygame.draw.circle(fs, (255, 255, 100, 200), (fx2 - 1, fy2 - 1), 2)
        game.ekran.blit(fs, (fire_btn_x - fire_btn_r - 12, fire_btn_y - fire_btn_r - 12))

        # Olum ekrani
        if game.cn <= 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,180))
            game.ekran.blit(k2, (0,0))
            game.ekran.blit(game.fb.render("OYUN BITTI", True, K), (GENISLIK//2-120, YUKSEKLIK//2-70))
            game.ekran.blit(game.f.render("R ile yeniden basla", True, B), (GENISLIK//2-110, YUKSEKLIK//2))
            if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NM):
                game.drm = "menu"; audio.muzik_durdur()

        # Tur bitis
        if getattr(game, 'rnd_bitti', False) and game.cn > 0:
            k2 = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA); k2.fill((0,0,0,140))
            game.ekran.blit(k2, (0,0))
            game.rnd_sayac += 1

            if game.boss_max_hp > 0 and game.boss_hp <= 0:
                od = game.mv
                if od not in game.envanter: game.envanter.append(od)
                if game.puan > game.yuksek_puan.get(od, 0): game.yuksek_puan[od] = game.puan
                if game.si < len(ms)-1:
                    game.ekran.blit(game.fb.render(f"{game.mv.upper()} GECTIN!", True, NY), (GENISLIK//2-140, YUKSEKLIK//2-70))
                    game.ekran.blit(game.f.render(f"Odul: {KOSTUMLER[od]['i']}", True, ALTIN), (GENISLIK//2-100, YUKSEKLIK//2))
                    if ui.btn("ILERLE", GENISLIK//2-100, YUKSEKLIK//2+50, 200, 50, GT, AGT, NY):
                        game.si += 1
                        levels.lv_yukle(ms[game.si])
                        game.cn = game.mc; game.rnd_bitti = False; game.boss_max_hp = 0
                else:
                    game.ekran.blit(game.fb.render("TUM MEVSIMLERI GECTIN!", True, ALTIN), (GENISLIK//2-240, YUKSEKLIK//2-60))
                    game.ekran.blit(game.f.render("Tebrikler! Oyun bitti.", True, B), (GENISLIK//2-100, YUKSEKLIK//2))
                    game.ekran.blit(game.fk.render(f"Odul: {KOSTUMLER[od]['i']} kazanildi!", True, ALTIN), (GENISLIK//2-120, YUKSEKLIK//2+35))
                    if ui.btn("MENU", GENISLIK//2-100, YUKSEKLIK//2+80, 200, 50, GT, AGT, NM):
                        game.drm = "menu"; audio.muzik_durdur(); game.rnd_bitti = False; game.boss_max_hp = 0
            elif game.boss_sv:
                pass
            elif game.rnd < 16:
                game.ekran.blit(game.fb.render(f"TUR {game.rnd} GECTIN!", True, NY), (GENISLIK//2-130, YUKSEKLIK//2-60))
                game.ekran.blit(game.f.render(f"Siradaki: Tur {game.rnd+1}/16", True, B), (GENISLIK//2-80, YUKSEKLIK//2))
                if game.rnd_sayac > 30:
                    game.rnd += 1
                    levels.lv_yukle(game.mv, game.rnd)
                    game.cn = game.mc; game.rnd_bitti = False

    pygame.display.flip()
    game.saat.tick(60)

pygame.quit()
