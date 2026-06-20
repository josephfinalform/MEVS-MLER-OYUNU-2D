import math
import random
import pygame
import assets
import game

def lv_yukle(m, rnd=1):
    game.mv = m
    game.rnk = assets.MEV[m]
    game.rnd = rnd
    game.plt = []
    game.prl = []
    game.tzl = []
    game.dsm = []
    game.mpl = []
    game.bullets = []
    game.fireballs = []
    game.boss_btl = []
    game.boss_muh = []
    game.boss_ozel_efekt = []
    game.boss_sv = False
    game.boss_hp = 0
    game.boss_max_hp = 0
    game.rnd_bitti = False
    game.puan = 0
    game.hiz_t = 0
    game.kalkan_t = 0
    game.cift_zipla_t = 1
    game.cift_zipla_kalan = 1
    game.miknatis_t = 0
    game.kalp_t = 0

    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    b = assets.BIOME[m]
    bos_round = rnd % 4 == 0

    # Ana zemin
    game.plt.append(pygame.Rect(0, h-20, z, 20))

    # Platformlari uret (sistematik, ziplamali)
    sayi = min(6 + rnd, 14)
    plat_x = 80
    for i in range(sayi):
        pw = random.randint(80, 220)
        py = h - 120 - i * random.randint(40, 70)
        py = max(80, min(h - 120, py))
        if i > 0:
            py = min(py, game.plt[-1].top - random.randint(30, 50))
        r2 = pygame.Rect(plat_x, py, pw, 16)
        game.plt.append(r2)
        plat_x += pw + random.randint(80, 180)
        if plat_x > z - 200:
            break

    # Zemin uzerine dikenler (platform aralari, 2. platformdan sonra)
    for i in range(2, len(game.plt) - 1):
        gap_x = game.plt[i].right + 20
        gap_w = game.plt[i + 1].left - game.plt[i].right - 40
        if gap_w > 30 and random.random() < 0.3:
            game.tzl.append(pygame.Rect(gap_x + gap_w // 2 - 20, h - 40, 40, 20))

    # Platform uzerine dikenler (buyuk platformlarda)
    for i in range(2, len(game.plt)):
        p = game.plt[i]
        if p.w > 140 and random.random() < 0.35:
            tx = p.x + random.randint(20, p.w - 60)
            game.tzl.append(pygame.Rect(tx, p.top - 20, 40, 20))

    # Prismler (2. platformdan basla)
    prism_aded = min(4 + rnd // 2, 10)
    for i in range(prism_aded):
        pi = i + 2
        if pi < len(game.plt):
            px = game.plt[pi].centerx + random.randint(-30, 30)
            py = game.plt[pi].top - 30
            game.prl.append((px, py))

    # Dusmanlar (buyuk platformlara, 3. platformdan basla)
    dusman_aded = min(1 + rnd // 3, 5)
    buyuk_plt = [p for p in game.plt[3:] if p.w > 130]
    random.shuffle(buyuk_plt)
    for i in range(min(dusman_aded, len(buyuk_plt))):
        p = buyuk_plt[i]
        dx = p.x + random.randint(10, p.w - 40)
        dy = p.top - 40
        sl = p.x
        sg = p.x + p.w - 30
        tip = "kovalayan" if (i + rnd) % 2 == 0 else "gezgin"
        hiz = game.dhc * (0.5 + i * 0.2) * (1 + rnd * 0.05)
        game.dsm.append({"r": pygame.Rect(dx, dy, 28, 50), "h": hiz, "sl": sl, "sg": sg, "tip": tip, "orj_h": hiz, "hp": 2, "ates_cd": random.randint(30, 90) if tip == "kovalayan" else 0})

    # Level metadata
    game.lvl = {"d": m, "pu": [], "wp": []}

    # Power-uplar (her levelde en az 2 tane)
    pu_sayisi = min(2 + rnd // 4, len(game.plt) - 2)
    for pi2 in range(pu_sayisi):
        put = random.choice(["hiz", "kalkan", "cift_zipla", "miknatis", "kalp"])
        idx = pi2 + 2
        if idx < len(game.plt):
            p = game.plt[idx]
            game.lvl["pu"].append((p.centerx, p.top - 30, put))

    # Mermi paketi
    if len(game.plt) > 1:
        p = game.plt[random.randint(1, len(game.plt) - 1)]
        game.lvl["wp"].append((p.centerx, p.top - 20))

    # Boss round (once platformlari degistir ki checkpoint dogru olsun)
    if bos_round:
        game.dsm.clear()
        game.prl.clear()
        game.lvl = {"d": m, "pu": [], "wp": []}
        # Boss platformlari (cok basamakli)
        game.plt = [pygame.Rect(0, h-20, z, 20)]
        for i in range(5):
            bx = 50 + i * (z - 100) // 4
            by = h - 100 - i * 80
            game.plt.append(pygame.Rect(bx, by, 180, 16))
        if len(game.plt) > 1:
            game.lvl["wp"].append((game.plt[-1].centerx, game.plt[-1].top - 30))
        bh = assets.BOSS_HP[game.ayar["z"]]
        bp = 1 + (assets.MS.index(m) * 0.5) + (rnd // 4) * 0.5
        game.boss_sv = True
        game.boss_max_hp = int(bh * bp * (1 + rnd * 0.1))
        game.boss_hp = game.boss_max_hp
        game.boss_timer = 0
        game.boss_ptrn = 0
        game.boss_dir = 1
        game.boss_vx = assets.BOSS_SPD[game.ayar["z"]]
        game.boss_x = z // 2
        game.boss_y = 80
        game.boss_atk_cd = 0
        game.boss_ozel_yetenek_cd = 0
        game.boss_hareket_mod = 0
        game.boss_hedefle = False
        game.boss_yon_degis = 0
        game.boss_ozel_efekt = []
        # Boss muhafiz yok (sadece boss)

    # Checkpoint (her zaman plt[1] uzerinde, guvenli)
    if len(game.plt) > 1:
        p = game.plt[1]
        game.cp_x, game.cp_y = p.x + 50, p.top - 50
    else:
        game.cp_x, game.cp_y = 100, h - 100

    game.ox, game.oy = game.cp_x, game.cp_y
    game.ammo = 100 if bos_round else 25
    game.weapon = game.mv

    if game.mk:
        import audio
        audio.sk.stop()
        audio.sk.set_volume(game.ayar["ses"] / 100)
        audio.sk.play(audio.SESLER[m], -1)

    import particles as p
    p.bg_par_baslat()

def _ciz_platform_kenar(p, rnk, b):
    x, y, w, h2 = p.x, p.y, p.w, p.h
    pygame.draw.rect(game.ekran, b["soil"], p)
    pygame.draw.rect(game.ekran, b["deep_soil"], p, 1)
    cim_r = pygame.Rect(x, y - 2, w, 6)
    pygame.draw.rect(game.ekran, b["grass"], cim_r)
    pygame.draw.line(game.ekran, b["grass"], (x, y - 2), (x + w, y - 2), 2)
    for ti in range(w // 40):
        tx = x + ti * 40 + 10
        if (tx * 7 + y * 13) % 10 < 3:
            pygame.draw.circle(game.ekran, b["stone"], (tx, y + 8), (tx * 3 + y) % 4 + 3)
    for ci in range(w // 20):
        cx2 = x + ci * 20 + 5
        cy2 = y - 2
        if (cx2 * 5 + cy2 * 7) % 10 < 4:
            pygame.draw.line(game.ekran, b["grass"], (cx2, cy2), (cx2 + ((cx2 * 3) % 5 - 2), cy2 - ((cy2 * 7) % 5 + 4)), 2)

def _ciz_dekorasyon(p, idx):
    if idx == 0:
        return
    b = assets.BIOME[game.mv]
    x, y, w = p.x, p.y, p.w
    m = game.mv
    sz = game.sz
    tohum = x * 7 + y * 13 + idx * 31

    if m == "ilkbahar":
        # Cicekler (3 renk)
        for fi in range(w // 25):
            fx = x + 10 + fi * 25 + (tohum + fi * 7) % 15
            if fx > x + w - 10:
                break
            if (tohum + fi * 11) % 7 < 4:
                c_renk = [(255, 100, 150), (255, 255, 100), (200, 100, 255)][fi % 3]
                # Sap
                pygame.draw.line(game.ekran, (60, 180, 60), (fx, y - 2), (fx, y - 12), 2)
                # Yaprak
                pygame.draw.ellipse(game.ekran, (80, 200, 80), (fx - 2, y - 8, 4, 3))
                # Cicek basi
                pygame.draw.circle(game.ekran, c_renk, (fx, y - 14), 4)
                pygame.draw.circle(game.ekran, (255, 255, 200), (fx, y - 14), 2)
        # Cali
        for bi in range(w // 60):
            bx = x + 10 + bi * 60 + (tohum + bi * 13) % 20
            if bx > x + w - 20:
                break
            if (tohum + bi * 17) % 5 < 2:
                pygame.draw.ellipse(game.ekran, (50, 150, 50), (bx, y - 10, 16, 12))
                pygame.draw.ellipse(game.ekran, (80, 180, 80), (bx + 2, y - 10, 16, 12))
                # Cicekli cali
                if (tohum + bi * 3) % 5 < 2:
                    pygame.draw.circle(game.ekran, (255, 150, 200), (bx + 8, y - 14), 3)

    elif m == "yaz":
        # Uzun otlar
        for gi in range(w // 20):
            gx = x + 5 + gi * 20 + (tohum + gi * 5) % 10
            if gx > x + w - 5:
                break
            if (tohum + gi * 7) % 4 < 2:
                boy = 8 + (tohum + gi * 3) % 8
                pygame.draw.line(game.ekran, (160, 190, 50), (gx, y - 2), (gx + ((gi * 7) % 5 - 2), y - 2 - boy), 2)
                pygame.draw.line(game.ekran, (180, 210, 60), (gx - 1, y - 2), (gx - 1 + ((gi * 5) % 5 - 2), y - 2 - boy // 2), 1)
        # Kaktus
        for ki in range(w // 80):
            kx = x + 10 + ki * 80 + (tohum + ki * 11) % 25
            if kx > x + w - 15:
                break
            if (tohum + ki * 19) % 7 < 3:
                pygame.draw.rect(game.ekran, (60, 140, 60), (kx, y - 20, 8, 20))
                pygame.draw.rect(game.ekran, (80, 160, 80), (kx, y - 20, 8, 20), 1)
                # Kollari
                if (tohum + ki * 3) % 5 < 3:
                    pygame.draw.rect(game.ekran, (60, 140, 60), (kx - 6, y - 14, 6, 4))
                    pygame.draw.rect(game.ekran, (60, 140, 60), (kx + 8, y - 10, 6, 4))
        # Kaya
        for ri in range(w // 70):
            rx = x + 15 + ri * 70 + (tohum + ri * 9) % 20
            if rx > x + w - 15:
                break
            if (tohum + ri * 13) % 5 < 2:
                pygame.draw.ellipse(game.ekran, (160, 150, 130), (rx, y - 4, 14, 8))
                pygame.draw.ellipse(game.ekran, (180, 170, 150), (rx + 1, y - 3, 12, 6), 1)

    elif m == "sonbahar":
        # Dusen yapraklar (hareketli)
        for li in range(w // 20):
            lx2 = x + 5 + li * 15 + (tohum + li * 7 + int(math.sin(sz * 0.02 + li) * 5)) % 12
            if lx2 > x + w - 5:
                break
            if (tohum + li * 5) % 3 < 1:
                y_renk = [(200, 120, 30), (180, 80, 20), (220, 180, 50)][li % 3]
                pygame.draw.ellipse(game.ekran, y_renk, (lx2, y - 2 - (li * 3) % 6, 5, 3))
        # Mantar
        for mi in range(w // 60):
            mx = x + 10 + mi * 60 + (tohum + mi * 11) % 20
            if mx > x + w - 10:
                break
            if (tohum + mi * 17) % 5 < 2:
                # Sap
                pygame.draw.rect(game.ekran, (220, 210, 190), (mx + 2, y - 8, 4, 8))
                # Sap
                pygame.draw.ellipse(game.ekran, (180, 80, 40), (mx, y - 12, 8, 6))
                pygame.draw.ellipse(game.ekran, (200, 100, 50), (mx + 1, y - 12, 6, 4), 1)
                # Benekler
                if (tohum + mi * 3) % 5 < 3:
                    pygame.draw.circle(game.ekran, (255, 240, 220), (mx + 2, y - 10), 1)
                    pygame.draw.circle(game.ekran, (255, 240, 220), (mx + 5, y - 9), 1)
        # Balkabagi
        for pi in range(w // 90):
            px2 = x + 15 + pi * 90 + (tohum + pi * 13) % 30
            if px2 > x + w - 15:
                break
            if (tohum + pi * 7) % 7 < 2:
                pygame.draw.ellipse(game.ekran, (220, 120, 40), (px2, y - 8, 10, 8))
                pygame.draw.ellipse(game.ekran, (240, 140, 50), (px2 + 1, y - 7, 8, 6), 1)
                pygame.draw.line(game.ekran, (80, 160, 80), (px2 + 5, y - 8), (px2 + 5, y - 12), 2)

    elif m == "kis":
        # Kar yiginlari
        for si in range(w // 30):
            sx3 = x + 5 + si * 30 + (tohum + si * 9) % 12
            if sx3 > x + w - 10:
                break
            if (tohum + si * 11) % 4 < 2:
                pygame.draw.ellipse(game.ekran, (230, 235, 245), (sx3, y - 4, 12, 6))
                pygame.draw.ellipse(game.ekran, (245, 250, 255), (sx3 + 1, y - 4, 10, 4), 1)
        # Buz kristali
        for ci2 in range(w // 50):
            cx3 = x + 10 + ci2 * 50 + (tohum + ci2 * 7) % 15
            if cx3 > x + w - 8:
                break
            if (tohum + ci2 * 13) % 6 < 2:
                cry_r = 4 + (tohum + ci2 * 3) % 3
                pygame.draw.circle(game.ekran, (200, 230, 255), (cx3, y - 2 - cry_r), cry_r)
                pygame.draw.circle(game.ekran, (220, 240, 255), (cx3, y - 2 - cry_r), cry_r, 1)
                # Isin
                if cry_r > 4:
                    for ii in range(4):
                        ia = ii * 1.57 + math.sin(sz * 0.01 + ci2) * 0.3
                        ix = cx3 + int(math.cos(ia) * (cry_r + 2))
                        iy = y - 2 - cry_r + int(math.sin(ia) * (cry_r + 2))
                        pygame.draw.line(game.ekran, (220, 240, 255), (cx3, y - 2 - cry_r), (ix, iy), 1)
        # Kardan adam mini
        for ki in range(w // 100):
            kx2 = x + 15 + ki * 100 + (tohum + ki * 17) % 35
            if kx2 > x + w - 20:
                break
            if (tohum + ki * 11) % 7 < 2:
                pygame.draw.circle(game.ekran, (230, 235, 245), (kx2 + 6, y - 8), 8)
                pygame.draw.circle(game.ekran, (245, 250, 255), (kx2 + 6, y - 8), 8, 1)
                pygame.draw.circle(game.ekran, (230, 235, 245), (kx2 + 6, y - 18), 6)
                pygame.draw.circle(game.ekran, (245, 250, 255), (kx2 + 6, y - 18), 6, 1)
                pygame.draw.circle(game.ekran, (20, 20, 20), (kx2 + 4, y - 20), 1)
                pygame.draw.circle(game.ekran, (20, 20, 20), (kx2 + 8, y - 20), 1)
                pygame.draw.line(game.ekran, (200, 100, 50), (kx2 + 6, y - 18), (kx2 + 10, y - 19), 1)

def _ciz_arka_plan():
    b = assets.BIOME[game.mv]
    z = assets.GENISLIK
    h = assets.YUKSEKLIK
    # Gokyuzu
    game.ekran.fill(b["sky"])
    # Gunes
    gunes_x = z - 150
    gunes_y = 60
    for gi in range(3):
        a2 = 255 - gi * 80
        if a2 > 0:
            s2 = pygame.Surface((60 + gi * 40, 60 + gi * 40), pygame.SRCALPHA)
            pygame.draw.circle(s2, (*b["sun"], a2 // 2), (30 + gi * 20, 30 + gi * 20), 30 + gi * 20)
            game.ekran.blit(s2, (gunes_x - 30 - gi * 20, gunes_y - 30 - gi * 20))
    pygame.draw.circle(game.ekran, b["sun"], (gunes_x, gunes_y), 30)
    pygame.draw.circle(game.ekran, (255, 255, 255), (gunes_x, gunes_y), 20)

    # Arka plan agaclari (3 katman parallax)
    katmanlar = [
        (b["bg_tree3"], 0.2, 30, 0.6),
        (b["bg_tree2"], 0.4, 20, 0.8),
        (b["bg_tree1"], 0.6, 15, 1.0),
    ]
    for renk, kayma, sayi2, boyut in katmanlar:
        for i in range(sayi2):
            tx = int(i * (z // sayi2) + math.sin(i * 3.7 + game.sz * kayma) * 30)
            ty = h - 60 - int(math.sin(i * 2.3) * 50) - 100
            # Govde
            govde_w = int(12 * boyut)
            govde_h = int(80 * boyut)
            pygame.draw.rect(game.ekran, renk, (tx - govde_w // 2, ty, govde_w, govde_h))
            pygame.draw.rect(game.ekran, (max(0, renk[0] - 20), max(0, renk[1] - 20), max(0, renk[2] - 20)), (tx - govde_w // 2, ty, govde_w, govde_h), 1)
            # Tac (yapraklar)
            tac_r = int(35 * boyut)
            pygame.draw.circle(game.ekran, renk, (tx, ty - 5), tac_r)
            pygame.draw.circle(game.ekran, (min(255, renk[0] + 30), min(255, renk[1] + 30), min(255, renk[2] + 30)), (tx, ty - 5), tac_r, 1)
            # Ek yapraklar
            for li in range(3):
                lx = tx + int(math.cos(i * 1.7 + li * 2.1) * tac_r * 0.7)
                ly = ty - 5 + int(math.sin(i * 1.7 + li * 2.1) * tac_r * 0.7)
                pygame.draw.circle(game.ekran, renk, (lx, ly), int(tac_r * 0.5))

    # Zemin katmanlari
    for yi in range(5):
        y2 = h - 20 + yi * 20
        renk2 = (max(0, b["soil"][0] - yi * 15), max(0, b["soil"][1] - yi * 15), max(0, b["soil"][2] - yi * 15))
        pygame.draw.rect(game.ekran, renk2, (0, y2, z, 20))
    # Tas bloklari
    for si in range(z // 80):
        sx2 = si * 80 + 20
        sy2 = h - 10 + ((si * 17) % 11 - 5)
        if (si * 13 + 7) % 10 < 5:
            pygame.draw.rect(game.ekran, b["stone"], (sx2, sy2, 30, 15))
            pygame.draw.rect(game.ekran, (b["stone"][0] - 20, b["stone"][1] - 20, b["stone"][2] - 20), (sx2, sy2, 30, 15), 1)
    # Kokler
    for ri in range(3):
        rx = (ri * 347) % z
        for rj in range(5):
            ry = h - 20 + rj * 8
            pygame.draw.line(game.ekran, b["deep_soil"], (rx + int(math.sin(rj * 0.5) * 10), ry), (rx + int(math.sin(rj * 0.5 + 0.3) * 10), ry + 8), 3)

    # Biyom tabanli on plan dekorasyonlari (sarkik dallar, vs)
    m = game.mv
    sz = game.sz
    if m == "ilkbahar":
        # Sarkik sarmasiklar (ustten sarkan)
        for vi in range(z // 60):
            vx = vi * 60 + int(math.sin(vi * 2.3 + sz * 0.05) * 15)
            if (vi * 13 + 7) % 7 < 3:
                for vj in range(3):
                    vy = vj * 8
                    pygame.draw.line(game.ekran, (60, 160, 60), (vx, vy), (vx + int(math.sin(sz * 0.02 + vj) * 3), vy + 8), 2)
                    if vj == 1 and (vi * 7) % 5 < 2:
                        pygame.draw.circle(game.ekran, (255, 150, 200), (vx + int(math.sin(sz * 0.02 + vj) * 3), vy + 8), 3)
        # Uzaktan ucusan kelebekler
        for bi in range(4):
            bx = (bi * 257 + int(sz * 0.3 * (bi % 2 * 2 - 1))) % z
            by = 100 + bi * 40 + int(math.sin(sz * 0.02 + bi * 2) * 20)
            if (bi * 7 + int(sz * 0.1)) % 10 < 6:
                pygame.draw.ellipse(game.ekran, (255, 200, 100), (bx, by, 6, 3))
                pygame.draw.ellipse(game.ekran, (255, 200, 100), (bx + 3, by, 6, 3))
    elif m == "yaz":
        # Sarkik kuru dallar
        for bi in range(z // 80):
            bx2 = bi * 80 + int(math.sin(bi * 1.7 + sz * 0.03) * 20)
            if (bi * 11 + 5) % 5 < 2:
                for bj in range(4):
                    bx2 = bi * 80 + int(math.sin(bi * 1.7 + sz * 0.03 + bj) * 10)
                    by2 = bj * 6
                    pygame.draw.line(game.ekran, (100, 60, 30), (bx2, by2), (bx2 + int(math.sin(sz * 0.01 + bj) * 5), by2 + 6), 2)
        # Sicak havada titresim
        for hi in range(8):
            hx = (hi * 157 + int(sz * 0.5)) % z
            hy = 150 + hi * 30 + int(math.sin(sz * 0.03 + hi) * 15)
            pygame.draw.circle(game.ekran, (255, 255, 200, 30), (hx, hy), 3 + int(math.sin(sz * 0.05 + hi) * 2))
    elif m == "sonbahar":
        # Orumcek aglari (sarkik)
        for wi in range(z // 100):
            wx = wi * 100 + int(math.sin(wi * 2.1 + sz * 0.02) * 20)
            if (wi * 17 + 3) % 7 < 3:
                for wj in range(5):
                    wy = wj * 6
                    pygame.draw.line(game.ekran, (180, 160, 140, 80), (wx, wy), (wx + int(math.sin(sz * 0.01 + wj) * 4), wy + 6), 1)
                    if wj % 2 == 0:
                        pygame.draw.line(game.ekran, (180, 160, 140, 60), (wx - 4, wy + 3), (wx + 4, wy + 3), 1)
        # Kuslar (goc eden)
        for bi in range(3):
            bxi = (bi * 347 + int(sz * 0.4 * (1 if bi % 2 == 0 else -1))) % z
            byi = 60 + bi * 25 + int(math.sin(sz * 0.01 + bi) * 10)
            pygame.draw.arc(game.ekran, (40, 30, 20), (bxi, byi, 10, 5), 0, 3.14, 1)
    elif m == "kis":
        # Sarkik buz sarkitlari (ustten)
        for ii in range(z // 40):
            ix2 = ii * 40 + int(math.sin(ii * 1.3 + sz * 0.01) * 10)
            if (ii * 19 + 11) % 5 < 2:
                boy = 8 + (ii * 7) % 15
                pygame.draw.polygon(game.ekran, (200, 230, 250), [(ix2, 0), (ix2 + 4, boy), (ix2 + 2, boy + 4), (ix2 - 2, boy + 4), (ix2 - 4, boy)])
                pygame.draw.polygon(game.ekran, (220, 240, 255), [(ix2, 0), (ix2 + 4, boy), (ix2 + 2, boy + 4), (ix2 - 2, boy + 4), (ix2 - 4, boy)], 1)

def platform_ciz():
    rnk = game.rnk
    b = assets.BIOME[game.mv]
    for i, p in enumerate(game.plt):
        if i == 0:
            # Ana zemin - Terraria tarzi
            pygame.draw.rect(game.ekran, b["soil"], p)
            pygame.draw.rect(game.ekran, b["deep_soil"], p, 1)
            cim_r = pygame.Rect(p.x, p.y - 3, p.w, 6)
            pygame.draw.rect(game.ekran, b["grass"], cim_r)
            pygame.draw.line(game.ekran, b["grass"], (p.x, p.y - 3), (p.right, p.y - 3), 3)
            for ci in range(p.w // 15):
                cx3 = p.x + ci * 15 + 5
                cy3 = p.y - 3
                if (cx3 * 7 + cy3 * 3) % 10 < 3:
                    pygame.draw.line(game.ekran, b["grass"], (cx3, cy3), (cx3 + ((cx3 * 5) % 5 - 2), cy3 - ((cy3 * 7) % 5 + 3)), 2)
            for si in range(p.w // 60):
                sx3 = p.x + si * 60 + 15
                if (sx3 * 11 + p.y * 3) % 10 < 4:
                    pygame.draw.rect(game.ekran, b["stone"], (sx3, p.y + 5, 20, 10))
        else:
            _ciz_platform_kenar(p, rnk, b)
            _ciz_dekorasyon(p, i)

def dusman_ciz(d):
    r = d["r"]
    cx = r.x + 14
    cy = r.y + 25
    m = game.mv
    tip = d.get("tip", "gezgin")

    if m == "ilkbahar":
        body_c = (50, 130, 50)
        eye_c = (255, 255, 100)
        if tip == "kovalayan":
            eye_c = (255, 50, 50)
        pygame.draw.rect(game.ekran, body_c, (cx - 10, cy + 4, 20, 18))
        pygame.draw.rect(game.ekran, (70, 150, 70), (cx - 10, cy + 4, 20, 18), 1)
        pygame.draw.ellipse(game.ekran, (60, 160, 60), (cx - 14, cy - 14, 28, 22))
        pygame.draw.ellipse(game.ekran, (80, 180, 80), (cx - 14, cy - 14, 28, 22), 1)
        pygame.draw.circle(game.ekran, eye_c, (cx - 6, cy - 12), 4)
        pygame.draw.circle(game.ekran, eye_c, (cx + 6, cy - 12), 4)
        if tip == "kovalayan":
            pygame.draw.circle(game.ekran, assets.S, (cx - 6, cy - 12), 2)
            pygame.draw.circle(game.ekran, assets.S, (cx + 6, cy - 12), 2)
            # Kizgin kas
            pygame.draw.line(game.ekran, assets.S, (cx - 10, cy - 18), (cx - 4, cy - 16), 2)
            pygame.draw.line(game.ekran, assets.S, (cx + 10, cy - 18), (cx + 4, cy - 16), 2)
    elif m == "yaz":
        body_c = (180, 150, 100)
        eye_c = (255, 200, 50)
        if tip == "kovalayan":
            eye_c = (255, 50, 50)
        pygame.draw.polygon(game.ekran, body_c, [(cx - 14, cy + 18), (cx - 10, cy), (cx + 10, cy), (cx + 14, cy + 18)])
        pygame.draw.polygon(game.ekran, (200, 170, 120), [(cx - 14, cy + 18), (cx - 10, cy), (cx + 10, cy), (cx + 14, cy + 18)], 1)
        pygame.draw.circle(game.ekran, (190, 160, 110), (cx, cy - 6), 12)
        pygame.draw.circle(game.ekran, (210, 180, 130), (cx, cy - 6), 12, 1)
        pygame.draw.circle(game.ekran, eye_c, (cx - 5, cy - 10), 4)
        pygame.draw.circle(game.ekran, eye_c, (cx + 5, cy - 10), 4)
        if tip == "kovalayan":
            pygame.draw.circle(game.ekran, assets.S, (cx - 5, cy - 10), 2)
            pygame.draw.circle(game.ekran, assets.S, (cx + 5, cy - 10), 2)
    elif m == "sonbahar":
        body_c = (25, 20, 15)
        eye_c = (60, 10, 60)
        if tip == "kovalayan":
            eye_c = (200, 20, 20)
        pygame.draw.rect(game.ekran, body_c, (cx - 8, cy + 2, 16, 22))
        pygame.draw.rect(game.ekran, (45, 35, 25), (cx - 8, cy + 2, 16, 22), 1)
        pygame.draw.rect(game.ekran, body_c, (cx - 8, cy - 16, 16, 18))
        pygame.draw.rect(game.ekran, (45, 35, 25), (cx - 8, cy - 16, 16, 18), 1)
        pygame.draw.rect(game.ekran, eye_c, (cx - 6, cy - 12, 5, 4))
        pygame.draw.rect(game.ekran, eye_c, (cx + 1, cy - 12, 5, 4))
        if tip == "kovalayan":
            pygame.draw.circle(game.ekran, (255, 100, 100), (cx - 3, cy - 10), 2)
            pygame.draw.circle(game.ekran, (255, 100, 100), (cx + 3, cy - 10), 2)
    elif m == "kis":
        body_c = (220, 230, 240)
        eye_c = (150, 30, 30)
        if tip == "kovalayan":
            eye_c = (255, 0, 0)
        pygame.draw.ellipse(game.ekran, body_c, (cx - 14, cy, 28, 28))
        pygame.draw.ellipse(game.ekran, (240, 245, 255), (cx - 10, cy + 4, 20, 20))
        pygame.draw.circle(game.ekran, (230, 235, 245), (cx, cy - 6), 10)
        pygame.draw.circle(game.ekran, (240, 245, 255), (cx, cy - 6), 10, 1)
        pygame.draw.circle(game.ekran, eye_c, (cx - 4, cy - 10), 3)
        pygame.draw.circle(game.ekran, eye_c, (cx + 4, cy - 10), 3)
        if tip == "kovalayan":
            pygame.draw.polygon(game.ekran, eye_c, [(cx - 6, cy - 14), (cx - 2, cy - 10), (cx - 6, cy - 10)])
            pygame.draw.polygon(game.ekran, eye_c, [(cx + 6, cy - 14), (cx + 2, cy - 10), (cx + 6, cy - 10)])

    if tip == "kovalayan":
        pygame.draw.circle(game.ekran, (255, 50, 50, 60), (cx, cy - 8), 18 + int(math.sin(game.sz * 0.2) * 4), 2)

def muhafiz_ciz(d):
    r = d["r"]
    cx = r.x + 12
    cy = r.y + 20
    m = game.mv
    # Mini boss versiyonu - sadece ana hatlariyla
    if m == "ilkbahar":
        pygame.draw.ellipse(game.ekran, (60, 160, 60), (cx - 12, cy - 10, 24, 20))
        pygame.draw.ellipse(game.ekran, (80, 180, 80), (cx - 12, cy - 10, 24, 20), 1)
        pygame.draw.ellipse(game.ekran, (200, 50, 50), (cx - 8, cy - 4, 16, 10))
        pygame.draw.line(game.ekran, (40, 140, 40), (cx - 10, cy + 4), (cx + 10, cy + 4), 3)
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx - 6, cy - 12), 3)
        pygame.draw.circle(game.ekran, (255, 255, 100), (cx + 6, cy - 12), 3)
        pygame.draw.circle(game.ekran, assets.S, (cx - 6, cy - 12), 1)
        pygame.draw.circle(game.ekran, assets.S, (cx + 6, cy - 12), 1)
    elif m == "yaz":
        pygame.draw.circle(game.ekran, (190, 160, 110), (cx, cy - 4), 10)
        pygame.draw.circle(game.ekran, (210, 180, 130), (cx, cy - 4), 10, 1)
        pygame.draw.polygon(game.ekran, (180, 150, 100), [(cx - 10, cy + 8), (cx - 8, cy), (cx + 8, cy), (cx + 10, cy + 8)])
        pygame.draw.circle(game.ekran, (255, 200, 50), (cx - 4, cy - 7), 3)
        pygame.draw.circle(game.ekran, (255, 200, 50), (cx + 4, cy - 7), 3)
    elif m == "sonbahar":
        pygame.draw.rect(game.ekran, (25, 20, 15), (cx - 8, cy - 8, 16, 16))
        pygame.draw.rect(game.ekran, (45, 35, 25), (cx - 8, cy - 8, 16, 16), 1)
        pygame.draw.rect(game.ekran, (60, 10, 60), (cx - 5, cy - 5, 4, 3))
        pygame.draw.rect(game.ekran, (60, 10, 60), (cx + 1, cy - 5, 4, 3))
        pygame.draw.line(game.ekran, (40, 30, 20), (cx - 8, cy + 4), (cx + 8, cy + 4), 2)
    elif m == "kis":
        pygame.draw.circle(game.ekran, (230, 235, 245), (cx, cy - 4), 8)
        pygame.draw.circle(game.ekran, (240, 245, 255), (cx, cy - 4), 8, 1)
        pygame.draw.ellipse(game.ekran, (220, 230, 240), (cx - 10, cy + 2, 20, 16))
        pygame.draw.circle(game.ekran, (150, 30, 30), (cx - 3, cy - 7), 2)
        pygame.draw.circle(game.ekran, (150, 30, 30), (cx + 3, cy - 7), 2)
    # Zirh parcasi (muhafiz oldugunu belli eden)
    pygame.draw.rect(game.ekran, (180, 180, 180), (cx - 4, cy - 14, 8, 4))
    pygame.draw.rect(game.ekran, (200, 200, 200), (cx - 4, cy - 14, 8, 4), 1)

def boss_ciz():
    if not game.boss_sv or game.boss_hp <= 0:
        return
    bx = game.boss_x
    by = game.boss_y
    m = game.mv
    zorluk = game.ayar["z"]
    skin = assets.BOSS_SKIN[zorluk]
    glow = assets.BOSS_GLOW[zorluk]
    sz2 = game.sz

    # Glow efekti (zorluga gore renk)
    for gi in range(3):
        gr = 35 + gi * 15
        s2 = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
        a2 = max(0, 60 - gi * 20)
        pygame.draw.circle(s2, (*glow, a2), (gr, gr), gr)
        game.ekran.blit(s2, (int(bx - gr), int(by - gr)))

    if m == "ilkbahar":
        saksi_offset = 10 if skin == 0 else 0
        pygame.draw.polygon(game.ekran, (180 - skin * 30, 100, 50), [(int(bx - 25), int(by + 40 + saksi_offset)), (int(bx + 25), int(by + 40 + saksi_offset)), (int(bx + 20), int(by + 55 + saksi_offset)), (int(bx - 20), int(by + 55 + saksi_offset))])
        pygame.draw.rect(game.ekran, (60, 140 + skin * 20, 60), (int(bx - 6), int(by + 10), 12, 30))
        pygame.draw.ellipse(game.ekran, (60, 160, 60), (int(bx - 28), int(by - 15), 56, 40))
        pygame.draw.ellipse(game.ekran, (200 - skin * 50, 50, 50), (int(bx - 20), int(by - 8), 40, 28))
        pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx - 16), int(by - 22)), 6)
        pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx + 4), int(by - 22)), 6)
        pygame.draw.circle(game.ekran, assets.S, (int(bx - 10), int(by - 20)), 3)
        pygame.draw.circle(game.ekran, assets.S, (int(bx + 10), int(by - 20)), 3)
        if skin == 1:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 10), int(by - 20)), 4, 1)
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 10), int(by - 20)), 4, 1)
    elif m == "yaz":
        scale = 1.1 if skin == 1 else 1.0
        bx_s = int(bx * scale - bx * (scale - 1))
        by_s = int(by * scale - by * (scale - 1))
        pygame.draw.polygon(game.ekran, (180 - skin * 40, 150, 100), [(int(bx_s - 35), int(by_s + 35)), (int(bx_s - 30), int(by_s)), (int(bx_s), int(by_s - 10)), (int(bx_s + 30), int(by_s)), (int(bx_s + 35), int(by_s + 35))])
        pygame.draw.circle(game.ekran, (190, 160, 110), (int(bx_s), int(by_s - 5)), 22)
        pygame.draw.circle(game.ekran, (255 - skin * 100, 200, 50), (int(bx_s - 8), int(by_s - 10)), 6)
        pygame.draw.circle(game.ekran, (255 - skin * 100, 200, 50), (int(bx_s + 8), int(by_s - 10)), 6)
        if skin == 1:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx_s - 8), int(by_s - 10)), 3)
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx_s + 8), int(by_s - 10)), 3)
    elif m == "sonbahar":
        renk_k = (25 - skin * 10, 20 - skin * 10, 15)
        renk_g = (60 - skin * 30, 10, 60)
        pygame.draw.rect(game.ekran, renk_k, (int(bx - 18), int(by + 8), 36, 35))
        pygame.draw.rect(game.ekran, renk_k, (int(bx - 14), int(by - 20), 28, 28))
        pygame.draw.rect(game.ekran, renk_g, (int(bx - 10), int(by - 16), 8, 6))
        pygame.draw.rect(game.ekran, renk_g, (int(bx + 2), int(by - 16), 8, 6))
        if skin == 1:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 6), int(by - 13)), 3)
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 6), int(by - 13)), 3)
    elif m == "kis":
        pygame.draw.ellipse(game.ekran, (220 - skin * 30, 230 - skin * 20, 240 - skin * 10), (int(bx - 30), int(by), 60, 50))
        pygame.draw.circle(game.ekran, (230 - skin * 30, 235 - skin * 20, 245 - skin * 10), (int(bx), int(by - 8)), 18)
        pygame.draw.circle(game.ekran, (150, 30, 30), (int(bx - 6), int(by - 12)), 4)
        pygame.draw.circle(game.ekran, (150, 30, 30), (int(bx + 6), int(by - 12)), 4)
        if skin == 1:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 6), int(by - 12)), 6, 1)
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 6), int(by - 12)), 6, 1)

    # Boss can bar (ustte)
    bbw = 300
    bbx = assets.GENISLIK // 2 - bbw // 2
    bby = 55
    pygame.draw.rect(game.ekran, (40, 0, 0), (bbx, bby, bbw, 18))
    bo = game.boss_hp / game.boss_max_hp
    bcol = glow
    pygame.draw.rect(game.ekran, bcol, (bbx, bby, int(bbw * bo), 18))
    pygame.draw.rect(game.ekran, assets.B, (bbx, bby, bbw, 18), 2)
    bn = assets.BOSS_ADI.get(game.mv, "BOSS")
    game.ekran.blit(game.fk.render(bn, True, assets.B), (bbx + 5, bby - 16))
    game.ekran.blit(game.fk.render(f"{game.boss_hp}/{game.boss_max_hp}", True, assets.B), (bbx + bbw - 60, bby + 1))
