import math
import random
import pygame
import assets
import game
import particles
import audio


def dusman_guncelle(oc):
    for d in game.dsm:
        if d["tip"] == "sıçrayan":
            dx = game.ox - d["r"].centerx
            dy = game.oy - d["r"].centery
            mesafe = math.sqrt(dx * dx + dy * dy)
            if mesafe < 300:
                d["r"].x += (dx / mesafe) * d["orj_h"] * 0.5 if mesafe > 0 else 0
                if d.get("ziplama_cd", 0) <= 0 and mesafe < 200:
                    d["vy"] = -10
                    d["vx"] = (dx / mesafe) * 4 if mesafe > 0 else 0
                    d["ziplama_cd"] = random.randint(60, 120)
                    particles.ptk_patlatma(d["r"].centerx, d["r"].bottom, (180, 180, 200), 5, 3)
                else:
                    d["ziplama_cd"] = max(0, d.get("ziplama_cd", 0) - 1)
            else:
                d["r"].x += d["h"]
                if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]: d["h"] *= -1
            d["vy"] = d.get("vy", 0) + 0.5
            d["r"].y += d["vy"]
            for p in game.plt:
                if d["r"].colliderect(p) and d["vy"] >= 0:
                    d["r"].bottom = p.top
                    d["vy"] = 0

        elif d["tip"] == "kovalayan":
            dx = game.ox - d["r"].centerx
            dy = game.oy - d["r"].centery
            mesafe = math.sqrt(dx * dx + dy * dy)
            if mesafe < 350:
                hiz = d["orj_h"] * 1.8
                if mesafe > 0:
                    d["r"].x += (dx / mesafe) * hiz
                    d["r"].y += (dy / mesafe) * hiz * 0.4
                if d["r"].x < d["sl"]: d["r"].x = d["sl"]
                if d["r"].x > d["sg"]: d["r"].x = d["sg"]
                if d["r"].y < 50: d["r"].y = 50
                if d["r"].y > assets.YUKSEKLIK - 80: d["r"].y = assets.YUKSEKLIK - 80
                if d.get("ates_cd", 0) <= 0 and mesafe < 250 and random.random() < 0.02:
                    game.boss_btl.append({"x": d["r"].centerx, "y": d["r"].centery,
                                          "vx": (dx / mesafe) * 2, "vy": (dy / mesafe) * 2, "r": assets.K})
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
                game.kalkan_t = 0
                particles.ptk_patlatma(game.ox, game.oy, assets.KR, 15)
                audio.sfx_hasar()
            else:
                game.cn -= 1
                particles.ptk_ekle(game.ox, game.oy, assets.K, 12)
                audio.sfx_hasar()
                game.ox, game.oy = game.cp_x, game.cp_y
                game.hx = game.hy = 0


def muhafiz_guncelle(oc):
    for mu in game.boss_muh[:]:
        dx = game.ox - mu["r"].centerx
        dy = game.oy - mu["r"].centery
        mesafe = math.sqrt(dx * dx + dy * dy)
        if mesafe < 300:
            if mesafe > 0:
                mu["r"].x += (dx / mesafe) * mu["h"]
                mu["r"].y += (dy / mesafe) * mu["h"] * 0.3
            if mu["r"].x < mu["sl"]: mu["r"].x = mu["sl"]
            if mu["r"].x > mu["sg"]: mu["r"].x = mu["sg"]
            if mu["r"].y < 80: mu["r"].y = 80
            if mu["r"].y > assets.YUKSEKLIK - 80: mu["r"].y = assets.YUKSEKLIK - 80
            if mu.get("ates_cd", 0) <= 0 and mesafe < 400:
                if mesafe > 0:
                    game.boss_btl.append({"x": mu["r"].centerx, "y": mu["r"].centery,
                                          "vx": (dx / mesafe) * 2.5, "vy": (dy / mesafe) * 2.5, "r": (255, 100, 100)})
                mu["ates_cd"] = random.randint(80, 150)
            else:
                mu["ates_cd"] = max(0, mu.get("ates_cd", 0) - 1)
        if oc.colliderect(mu["r"]):
            if game.kalkan_t > 0:
                game.kalkan_t = 0
                particles.ptk_patlatma(game.ox, game.oy, assets.KR, 15)
                audio.sfx_hasar()
            else:
                game.cn -= 1
                particles.ptk_ekle(game.ox, game.oy, assets.K, 12)
                audio.sfx_hasar()
                game.ox, game.oy = game.cp_x, game.cp_y
                game.hx = game.hy = 0


def mermi_guncelle():
    for b in game.bullets[:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += 0.1
        if b["x"] < -20 or b["x"] > assets.GENISLIK + 20 or b["y"] < -20 or b["y"] > assets.YUKSEKLIK + 20:
            game.bullets.remove(b)
            continue
        br = pygame.Rect(b["x"] - 5, b["y"] - 5, 10, 10)
        hit = False
        for d in game.dsm[:]:
            if br.colliderect(d["r"]):
                d["hp"] -= 1
                particles.ptk_patlatma(b["x"], b["y"], assets.KR, 12)
                audio.sfx_hasar()
                hit = True
                if d["hp"] <= 0:
                    game.dsm.remove(d)
                    particles.ptk_patlatma(b["x"], b["y"], b["r"], 15)
                break
        if hit:
            game.bullets.remove(b)
            continue
        for mu in game.boss_muh[:]:
            if br.colliderect(mu["r"]):
                mu["hp"] -= 1
                particles.ptk_patlatma(b["x"], b["y"], assets.KR, 10)
                audio.sfx_hasar()
                if mu["hp"] <= 0:
                    game.boss_muh.remove(mu)
                    particles.ptk_patlatma(b["x"], b["y"], assets.ALTIN, 15)
                hit = True
                break
        if hit:
            game.bullets.remove(b)
            continue
        if game.boss_sv and game.boss_hp > 0:
            if br.colliderect(pygame.Rect(game.boss_x - 35, game.boss_y - 35, 70, 70)):
                game.boss_hp -= b["dmg"]
                game.bullets.remove(b)
                audio.sfx_boss_hit()
                particles.ptk_patlatma(b["x"], b["y"], b["r"], 12)


def boss_mermi_guncelle(oc):
    for b in game.boss_btl[:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += 0.05
        if b["x"] < -20 or b["x"] > assets.GENISLIK + 20 or b["y"] < -20 or b["y"] > assets.YUKSEKLIK + 20:
            game.boss_btl.remove(b)
            continue
        if b.get("fake"):
            continue
        bs2 = b.get("s", 6)
        br = pygame.Rect(b["x"] - bs2 // 2 - 1, b["y"] - bs2 // 2 - 1, bs2 + 2, bs2 + 2)
        if oc.colliderect(br):
            game.boss_btl.remove(b)
            if game.kalkan_t > 0:
                game.kalkan_t = 0
                particles.ptk_patlatma(game.ox, game.oy, assets.KR, 15)
                audio.sfx_hasar()
            else:
                game.cn -= 1
                particles.ptk_ekle(game.ox, game.oy, assets.K, 12)
                audio.sfx_hasar()
                game.ox, game.oy = game.cp_x, game.cp_y
                game.hx = game.hy = 0


def alev_topu_guncelle():
    for fb in game.fireballs[:]:
        fb["x"] += fb["vx"]
        fb["y"] += fb["vy"]
        fb["vy"] += 0.05
        fb["t"] += 1
        if fb["t"] > 60 or fb["x"] < -30 or fb["x"] > assets.GENISLIK + 30 or fb["y"] < -30 or fb["y"] > assets.YUKSEKLIK + 30:
            game.fireballs.remove(fb)
            continue
        fbr = pygame.Rect(fb["x"] - 12, fb["y"] - 12, 24, 24)
        hit = False
        particles.ptk_ekle(int(fb["x"] - 5 + random.random() * 10), int(fb["y"] - 5 + random.random() * 10),
                           (255, random.randint(100, 200), 0), 3)
        for d in game.dsm[:]:
            if fbr.colliderect(d["r"]):
                d["hp"] -= 5
                particles.ptk_patlatma(fb["x"], fb["y"], assets.KR, 20)
                audio.sfx_hasar()
                hit = True
                if d["hp"] <= 0:
                    game.dsm.remove(d)
                    particles.ptk_patlatma(fb["x"], fb["y"], (255, 100, 0), 30)
                break
        if hit:
            game.fireballs.remove(fb)
            continue
        for mu in game.boss_muh[:]:
            if fbr.colliderect(mu["r"]):
                mu["hp"] -= 5
                particles.ptk_patlatma(fb["x"], fb["y"], assets.KR, 18)
                audio.sfx_hasar()
                if mu["hp"] <= 0:
                    game.boss_muh.remove(mu)
                    particles.ptk_patlatma(fb["x"], fb["y"], assets.ALTIN, 25)
                hit = True
                break
        if hit:
            game.fireballs.remove(fb)
            continue
        if game.boss_sv and game.boss_hp > 0:
            if fbr.colliderect(pygame.Rect(game.boss_x - 35, game.boss_y - 35, 70, 70)):
                game.boss_hp -= 10
                game.fireballs.remove(fb)
                audio.sfx_boss_hit()
                particles.ptk_patlatma(fb["x"], fb["y"], (255, 100, 0), 30)
                particles.ptk_patlatma(fb["x"], fb["y"], assets.ALTIN, 15)


def boss_guncelle():
    if not game.boss_sv or game.boss_hp <= 0:
        return
    bx = game.boss_x
    by = game.boss_y
    bm = game.mv
    game.boss_timer += 1
    game.boss_atk_cd -= 1
    game.boss_ozel_yetenek_cd -= 1
    game.boss_lazer_t = max(0, game.boss_lazer_t - 1)
    game.boss_minyon_t = max(0, game.boss_minyon_t - 1)
    game.boss_dalga_t = max(0, game.boss_dalga_t - 1)

    if game.boss_timer % 180 == 0:
        game.boss_hareket_mod = random.randint(0, 3)
        game.boss_yon_degis = game.boss_timer + random.randint(60, 180)

    if game.boss_hareket_mod == 0:
        game.boss_x += game.boss_vx * game.boss_dir
        if game.boss_x < 100 or game.boss_x > assets.GENISLIK - 100:
            game.boss_dir *= -1
        game.boss_y = 80 + math.sin(game.boss_timer * 0.03) * 40
    elif game.boss_hareket_mod == 1:
        dx = game.ox - bx
        dy = game.oy - by
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            game.boss_x += (dx / d) * game.boss_vx * 1.5
            game.boss_y += (dy / d) * game.boss_vx * 0.8
        game.boss_hedefle = True
        if game.boss_timer > game.boss_yon_degis:
            game.boss_hareket_mod = 0
            game.boss_hedefle = False
    elif game.boss_hareket_mod == 2:
        cyc = (game.boss_timer % 120) / 120.0
        game.boss_y = 80 + math.sin(cyc * math.pi * 2) * 100
        game.boss_x += game.boss_vx * game.boss_dir * 0.5
        if game.boss_x < 100 or game.boss_x > assets.GENISLIK - 100:
            game.boss_dir *= -1

    game.boss_x = max(60, min(assets.GENISLIK - 60, game.boss_x))
    game.boss_y = max(40, min(assets.YUKSEKLIK - 200, game.boss_y))

    if game.boss_atk_cd <= 0:
        ptrn = game.boss_ptrn % 4
        zorluk_hiz = assets.BOSS_ATK_CD[game.ayar["z"]]
        spd = 3 + random.uniform(-0.5, 0.5)
        if ptrn == 0:
            dx = game.ox - bx
            dy = game.oy - by
            d = math.sqrt(dx * dx + dy * dy)
            if d > 0:
                game.boss_btl.append({"x": bx, "y": by + 30, "vx": dx / d * spd, "vy": dy / d * spd, "r": assets.K})
            game.boss_atk_cd = max(60, zorluk_hiz * 2 - game.boss_ptrn * 2)
        elif ptrn == 1:
            for li in range(-1, 2):
                dx = game.ox - bx + li * 40
                dy = game.oy - by
                d = math.sqrt(dx * dx + dy * dy)
                if d > 0:
                    game.boss_btl.append(
                        {"x": bx + li * 15, "y": by + 30, "vx": dx / d * (spd + 0.5), "vy": dy / d * (spd + 0.5),
                         "r": (255, 100, 100)})
            game.boss_atk_cd = max(80, zorluk_hiz * 2 - game.boss_ptrn * 2)
        elif ptrn == 2:
            for wi in range(5):
                a3 = -1 + wi * 0.5
                dx = game.ox - bx + a3 * 80
                dy = game.oy - by
                d = math.sqrt(dx * dx + dy * dy)
                if d > 0:
                    fake = random.random() < 0.3
                    game.boss_btl.append({"x": bx + wi * 8, "y": by + 30,
                                          "vx": dx / d * (spd - 0.5) + random.uniform(-0.3, 0.3),
                                          "vy": dy / d * (spd - 0.5) + random.uniform(-0.5, 0.5),
                                          "r": (200, 50, 200), "s": 8 if not fake else 4, "fake": fake})
            game.boss_atk_cd = max(100, zorluk_hiz * 2 - game.boss_ptrn * 2)
        else:
            for ai in range(8):
                a5 = ai * 0.785 + game.boss_timer * 0.02
                game.boss_btl.append(
                    {"x": bx, "y": by + 30, "vx": math.cos(a5) * spd, "vy": math.sin(a5) * spd, "r": (255, 50, 255)})
            game.boss_atk_cd = max(120, zorluk_hiz * 2)

        game.boss_ptrn = (game.boss_ptrn + 1) % 8
        audio.sfx_boss_ates()

    if game.boss_ozel_yetenek_cd <= 0:
        bm_spd = 2 + random.uniform(-0.5, 0.5)
        if bm == "ilkbahar":
            for bi in range(6):
                a6 = bi * 1.047 + game.boss_timer * 0.01
                game.boss_btl.append({"x": bx, "y": by + 30, "vx": math.cos(a6) * bm_spd * 0.6,
                                      "vy": math.sin(a6) * bm_spd * 0.6, "r": (255, 100, 200), "s": 6})
            game.boss_ozel_yetenek_cd = max(200, 350 - game.boss_ptrn * 3)
            game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (255, 200, 255), "tip": "cicek"})
        elif bm == "yaz":
            for bi in range(5):
                dx = game.ox - bx + random.randint(-50, 50)
                dy = game.oy - by + 100
                d = math.sqrt(dx * dx + dy * dy)
                if d > 0:
                    game.boss_btl.append(
                        {"x": bx + random.randint(-20, 20), "y": by + 30, "vx": dx / d * bm_spd * 1.2,
                         "vy": dy / d * bm_spd * 1.2, "r": (255, 150, 0), "s": 10})
            game.boss_ozel_yetenek_cd = max(220, 380 - game.boss_ptrn * 3)
            game.boss_ozel_efekt.append({"t": 25, "x": bx, "y": by, "r": (255, 200, 0), "tip": "alev"})
        elif bm == "sonbahar":
            for bi in range(12):
                a7 = bi * 0.524 + game.boss_timer * 0.03
                fake = random.random() < 0.4
                game.boss_btl.append(
                    {"x": bx, "y": by + 20, "vx": math.cos(a7) * bm_spd * 0.8, "vy": math.sin(a7) * bm_spd * 0.8,
                     "r": (200, 120, 50), "s": 5 if not fake else 3, "fake": fake})
            game.boss_ozel_yetenek_cd = max(180, 350 - game.boss_ptrn * 3)
            game.boss_ozel_efekt.append({"t": 30, "x": bx, "y": by, "r": (200, 150, 50), "tip": "yaprak"})
        elif bm == "kis":
            for bi in range(4):
                game.boss_btl.append({"x": game.ox + random.randint(-100, 100), "y": -20, "vx": 0,
                                      "vy": bm_spd * 1.5, "r": (180, 220, 255), "s": 7})
            game.boss_ozel_yetenek_cd = max(150, 300 - game.boss_ptrn * 3)
            game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (200, 230, 255), "tip": "buz"})
        audio.sfx_boss_ates()

    for ef in game.boss_ozel_efekt[:]:
        ef["t"] -= 1
        if ef["t"] <= 0:
            game.boss_ozel_efekt.remove(ef)
