"""Level generation and rendering: platforms, enemies, boss, background."""

from __future__ import annotations

import math
import os
import random
from typing import Any

import pygame

import animations
import assets
import config
import game


# ── Background state ─────────────────────────────────────────────
_arka_resimler: dict[str, Any] = {}
_arka_bulut: list[dict[str, Any]] = []
_arka_duman: list[dict[str, Any]] = []


def _arka_anim_baslat() -> None:
    """Initialize cloud and mist particles for background animation."""
    global _arka_bulut, _arka_duman
    z, h = assets.GENISLIK, assets.YUKSEKLIK

    _arka_bulut = [
        {
            "x": random.randint(-200, z), "y": random.randint(20, 120),
            "w": random.randint(60, 150), "h": random.randint(15, 35),
            "hiz": random.uniform(0.1, 0.4), "s": random.uniform(0, 6.28),
        }
        for _ in range(6)
    ]

    _arka_duman = [
        {
            "x": random.randint(0, z), "y": random.randint(h - 120, h - 20),
            "hiz": random.uniform(0.2, 0.6), "r": random.randint(8, 20),
            "s": random.uniform(0, 6.28), "o": random.randint(20, 50),
        }
        for _ in range(10)
    ]


def lv_yukle(m: str, rnd: int = 1) -> None:
    """Generate a complete level layout for the given season and round."""
    game.mv = m
    game.rnk = assets.MEV[m]
    game.rnd = rnd
    game.plt.clear()
    game.prl.clear()
    game.tzl.clear()
    game.dsm.clear()
    game.mpl.clear()
    game.bullets.clear()
    game.fireballs.clear()
    game.boss_btl.clear()
    game.boss_muh.clear()
    game.boss_ozel_efekt.clear()
    game.boss_sv = False
    game.boss_hp = 0.0
    game.boss_max_hp = 0.0
    game.boss_zorluk = None
    game.puan = 0
    game.hiz_t = 0
    game.kalkan_t = 0
    game.cift_zipla_t = 1
    game.cift_zipla_kalan = 1
    game.miknatis_t = 0
    game.kalp_t = 0

    z, h = assets.GENISLIK, assets.YUKSEKLIK
    bos_round = rnd % 4 == 0

    # ── Floor ────────────────────────────────────────────────────
    game.plt.append(pygame.Rect(0, h - 20, z, 20))

    # ── Platforms ─────────────────────────────────────────────────
    sayi = min(6 + rnd, 14)
    plat_x = 80
    for i in range(sayi):
        pw = random.randint(80, 220)
        py = h - 120 - i * random.randint(40, 70)
        py = max(80, min(h - 120, py))
        if i > 0:
            py = min(py, game.plt[-1].top - random.randint(30, 50))
        game.plt.append(pygame.Rect(plat_x, py, pw, 16))
        plat_x += pw + random.randint(80, 180)
        if plat_x > z - 200:
            break

    # ── Spikes ────────────────────────────────────────────────────
    # Between platforms
    for i in range(2, len(game.plt) - 1):
        gap_x = game.plt[i].right + 20
        gap_w = game.plt[i + 1].left - game.plt[i].right - 40
        if gap_w > 30 and random.random() < 0.3:
            game.tzl.append(pygame.Rect(gap_x + gap_w // 2 - 20, h - 40, 40, 20))

    # On large platforms
    for i in range(2, len(game.plt)):
        p = game.plt[i]
        if p.w > 140 and random.random() < 0.35:
            tx = p.x + random.randint(20, p.w - 60)
            game.tzl.append(pygame.Rect(tx, p.top - 20, 40, 20))

    # ── Prisms (collectibles) ─────────────────────────────────────
    prism_adet = min(4 + rnd // 2, 10)
    for i in range(prism_adet):
        pi = i + 2
        if pi < len(game.plt):
            p = game.plt[pi]
            px = p.centerx + random.randint(-30, 30)
            py = p.top - 30
            tuzak_var = any(
                t.colliderect(pygame.Rect(p.x, p.top - 20, p.w, 40))
                for t in game.tzl
            )
            if not tuzak_var:
                game.prl.append((px, py))

    # ── Enemies ───────────────────────────────────────────────────
    dusman_adet = min(1 + rnd // 3, 5)
    buyuk_plt = [p for p in game.plt[3:] if p.w > 130]
    random.shuffle(buyuk_plt)
    for i in range(min(dusman_adet, len(buyuk_plt))):
        p = buyuk_plt[i]
        dx = p.x + random.randint(10, p.w - 40)
        dy = p.top - 40
        sl, sg = p.x, p.x + p.w - 30
        tip = "kovalayan" if (i + rnd) % 2 == 0 else "gezgin"
        hiz = game.dhc * (0.5 + i * 0.2) * (1 + rnd * 0.05)
        game.dsm.append({
            "r": pygame.Rect(dx, dy, 28, 50), "h": hiz, "sl": sl, "sg": sg,
            "tip": tip, "orj_h": hiz, "hp": 2,
            "ates_cd": random.randint(30, 90) if tip == "kovalayan" else 0,
        })

    # ── Level metadata ────────────────────────────────────────────
    game.lvl = {"d": m, "pu": [], "wp": []}

    # ── Power-ups ─────────────────────────────────────────────────
    pu_sayisi = min(2 + rnd // 4, len(game.plt) - 2)
    for pi in range(pu_sayisi):
        put = random.choice(["hiz", "kalkan", "cift_zipla", "miknatis", "kalp"])
        idx = pi + 2
        if idx < len(game.plt):
            p = game.plt[idx]
            px, py = p.centerx, p.top - 30
            tuzak_var = any(
                t.colliderect(pygame.Rect(p.x, p.top - 20, p.w, 40))
                for t in game.tzl
            )
            if not tuzak_var:
                game.lvl["pu"].append((px, py, put))

    # ── Ammo pack ─────────────────────────────────────────────────
    if len(game.plt) > 1:
        temiz_plt = [
            p for i, p in enumerate(game.plt)
            if i > 0 and not any(
                t.colliderect(pygame.Rect(p.x, p.top - 20, p.w, 40))
                for t in game.tzl
            )
        ]
        if temiz_plt:
            p = random.choice(temiz_plt)
            game.lvl["wp"].append((p.centerx, p.top - 20))

    # ── Boss round ────────────────────────────────────────────────
    if bos_round:
        game.dsm.clear()
        game.prl.clear()
        game.lvl = {"d": m, "pu": [], "wp": []}

        game.plt = [pygame.Rect(0, h - 20, z, 20)]
        for i in range(5):
            bx = 50 + i * (z - 100) // 4
            by = h - 100 - i * 80
            game.plt.append(pygame.Rect(bx, by, 180, 16))

        if len(game.plt) > 1:
            game.lvl["wp"].append((game.plt[-1].centerx, game.plt[-1].top - 30))

        # Boss difficulty scales with round
        if rnd <= 4:
            bz = "kolay"
        elif rnd <= 8:
            bz = "orta"
        elif rnd <= 12:
            bz = "zor"
        else:
            bz = "imkansiz"

        game.boss_zorluk = bz
        bh = assets.BOSS_HP[bz]
        bp = 1 + (assets.ms.index(m) * 0.5) + (rnd // 4) * 0.5
        game.boss_sv = True
        game.boss_max_hp = int(bh * bp * (1 + rnd * 0.1))
        game.boss_hp = float(game.boss_max_hp)
        game.boss_timer = 0
        game.boss_ptrn = 0
        game.boss_dir = 1
        game.boss_vx = assets.BOSS_SPD[bz]
        game.boss_x = z // 2
        game.boss_y = 80
        game.boss_atk_cd = 0
        game.boss_ozel_yetenek_cd = 0
        game.boss_hareket_mod = 0
        game.boss_hedefle = False
        game.boss_yon_degis = 0
        game.boss_ozel_efekt.clear()

    # ── Checkpoint (always on plt[1]) ─────────────────────────────
    if len(game.plt) > 1:
        p = game.plt[1]
        game.cp_x, game.cp_y = float(p.x + 50), float(p.top - 50)
    else:
        game.cp_x, game.cp_y = 100.0, float(h - 100)

    game.ox, game.oy = game.cp_x, game.cp_y
    game.ammo = 100 if bos_round else 25
    game.weapon = game.mv

    import audio
    audio.sezon_muzik(m)

    import particles as p
    p.bg_par_baslat()
    _arka_anim_baslat()
    animations.animasyon_baslat()


# ── Texture atlas drawing ────────────────────────────────────────
def _ciz_texture(tx: int, ty: int, x: float, y: float, w: float, h: float) -> None:
    """Draw a tiled texture region from the sprite sheet."""
    if game.tex_sheet is None:
        return
    tile = game.tex_sheet.subsurface((tx * 16, ty * 16, 16, 16))
    for px in range(int(x), int(x + w), 16):
        for py in range(int(y), int(y + h), 16):
            game.ekran.blit(tile, (px, py))


def _ciz_platform_kenar(p: pygame.Rect, rnk: dict[str, Any], b: dict[str, Any]) -> None:
    """Draw a single platform with soil, grass, and stone details."""
    x, y, w, h2 = p.x, p.y, p.w, p.h
    tex = game.TEXTURE_MAP.get(game.mv)
    if tex and game.tex_sheet:
        _ciz_texture(tex["soil"][0], tex["soil"][1], x, y, w, h2)
        _ciz_texture(tex["grass"][0], tex["grass"][1], x, y - 2, w, 16)
    else:
        pygame.draw.rect(game.ekran, b["soil"], p)
        pygame.draw.rect(game.ekran, b["deep_soil"], p, 1)
        cim_r = pygame.Rect(x, y - 2, w, 6)
        pygame.draw.rect(game.ekran, b["grass"], cim_r)
        pygame.draw.line(game.ekran, b["grass"], (x, y - 2), (x + w, y - 2), 2)
        for ti in range(w // 40):
            tx2 = x + ti * 40 + 10
            if (tx2 * 7 + y * 13) % 10 < 3:
                pygame.draw.circle(game.ekran, b["stone"], (tx2, y + 8), (tx2 * 3 + y) % 4 + 3)
        for ci in range(w // 20):
            cx = x + ci * 20 + 5
            cy = y - 2
            if (cx * 5 + cy * 7) % 10 < 4:
                dx = (cx * 3) % 5 - 2
                dy = (cy * 7) % 5 + 4
                pygame.draw.line(game.ekran, b["grass"], (cx, cy), (cx + dx, cy - dy), 2)


def _ciz_dekorasyon(p: pygame.Rect, idx: int) -> None:
    """Draw biome-specific platform decoration (flowers, cacti, mushrooms, etc.)."""
    if idx == 0:
        return

    b = assets.BIOME[game.mv]
    x, y, w = p.x, p.y, p.w
    m = game.mv
    sz = game.sz
    tohum = x * 7 + y * 13 + idx * 31

    if m == "ilkbahar":
        for fi in range(w // 25):
            fx = x + 10 + fi * 25 + (tohum + fi * 7) % 15
            if fx > x + w - 10:
                break
            if (tohum + fi * 11) % 7 < 4:
                c_renk = [(255, 255, 240), (255, 255, 100), (200, 100, 255)][fi % 3]
                pygame.draw.line(game.ekran, (60, 180, 60), (fx, y - 2), (fx, y - 12), 2)
                pygame.draw.ellipse(game.ekran, (80, 200, 80), (fx - 2, y - 8, 4, 3))
                pygame.draw.circle(game.ekran, c_renk, (fx, y - 14), 4)
                pygame.draw.circle(game.ekran, (255, 255, 200), (fx, y - 14), 2)
        for bi in range(w // 60):
            bx = x + 10 + bi * 60 + (tohum + bi * 13) % 20
            if bx > x + w - 20:
                break
            if (tohum + bi * 17) % 5 < 2:
                pygame.draw.ellipse(game.ekran, (50, 150, 50), (bx, y - 10, 16, 12))
                pygame.draw.ellipse(game.ekran, (80, 180, 80), (bx + 2, y - 10, 16, 12))
                if (tohum + bi * 3) % 5 < 2:
                    pygame.draw.circle(game.ekran, (255, 255, 230), (bx + 6, y - 14), 3)
                    pygame.draw.circle(game.ekran, (255, 255, 200), (bx + 6, y - 14), 1)

    elif m == "yaz":
        for gi in range(w // 20):
            gx = x + 5 + gi * 20 + (tohum + gi * 5) % 10
            if gx > x + w - 5:
                break
            if (tohum + gi * 7) % 4 < 2:
                boy = 8 + (tohum + gi * 3) % 8
                ox = (gi * 7) % 5 - 2
                pygame.draw.line(game.ekran, (160, 190, 50), (gx, y - 2), (gx + ox, y - 2 - boy), 2)
                pygame.draw.line(game.ekran, (180, 210, 60), (gx - 1, y - 2), (gx - 1 + (gi * 5) % 5 - 2, y - 2 - boy // 2), 1)
        for ki in range(w // 80):
            kx = x + 10 + ki * 80 + (tohum + ki * 11) % 25
            if kx > x + w - 15:
                break
            if (tohum + ki * 19) % 7 < 3:
                pygame.draw.rect(game.ekran, (60, 140, 60), (kx, y - 20, 8, 20))
                pygame.draw.rect(game.ekran, (80, 160, 80), (kx, y - 20, 8, 20), 1)
                if (tohum + ki * 3) % 5 < 3:
                    pygame.draw.rect(game.ekran, (60, 140, 60), (kx - 6, y - 14, 6, 4))
                    pygame.draw.rect(game.ekran, (60, 140, 60), (kx + 8, y - 10, 6, 4))
        for ri in range(w // 70):
            rx = x + 15 + ri * 70 + (tohum + ri * 9) % 20
            if rx > x + w - 15:
                break
            if (tohum + ri * 13) % 5 < 2:
                pygame.draw.ellipse(game.ekran, (160, 150, 130), (rx, y - 4, 14, 8))
                pygame.draw.ellipse(game.ekran, (180, 170, 150), (rx + 1, y - 3, 12, 6), 1)

    elif m == "sonbahar":
        for li in range(w // 20):
            lx = x + 5 + li * 15 + (tohum + li * 7 + int(math.sin(sz * 0.02 + li) * 5)) % 12
            if lx > x + w - 5:
                break
            if (tohum + li * 5) % 3 < 1:
                y_renk = [(200, 120, 30), (180, 80, 20), (220, 180, 50)][li % 3]
                pygame.draw.ellipse(game.ekran, y_renk, (lx, y - 2 - (li * 3) % 6, 5, 3))
        for mi in range(w // 60):
            mx = x + 10 + mi * 60 + (tohum + mi * 11) % 20
            if mx > x + w - 10:
                break
            if (tohum + mi * 17) % 5 < 2:
                pygame.draw.rect(game.ekran, (220, 210, 190), (mx + 2, y - 8, 4, 8))
                pygame.draw.ellipse(game.ekran, (180, 80, 40), (mx, y - 12, 8, 6))
                pygame.draw.ellipse(game.ekran, (200, 100, 50), (mx + 1, y - 12, 6, 4), 1)
                if (tohum + mi * 3) % 5 < 3:
                    pygame.draw.circle(game.ekran, (255, 240, 220), (mx + 2, y - 10), 1)
                    pygame.draw.circle(game.ekran, (255, 240, 220), (mx + 5, y - 9), 1)
        for pi in range(w // 90):
            pxx = x + 15 + pi * 90 + (tohum + pi * 13) % 30
            if pxx > x + w - 15:
                break
            if (tohum + pi * 7) % 7 < 2:
                pygame.draw.ellipse(game.ekran, (220, 120, 40), (pxx, y - 8, 10, 8))
                pygame.draw.ellipse(game.ekran, (240, 140, 50), (pxx + 1, y - 7, 8, 6), 1)
                pygame.draw.line(game.ekran, (80, 160, 80), (pxx + 5, y - 8), (pxx + 5, y - 12), 2)

    elif m == "kis":
        for si in range(w // 30):
            sx = x + 5 + si * 30 + (tohum + si * 9) % 12
            if sx > x + w - 10:
                break
            if (tohum + si * 11) % 4 < 2:
                pygame.draw.ellipse(game.ekran, (230, 235, 245), (sx, y - 4, 12, 6))
                pygame.draw.ellipse(game.ekran, (245, 250, 255), (sx + 1, y - 4, 10, 4), 1)
        for ci in range(w // 50):
            cx = x + 10 + ci * 50 + (tohum + ci * 7) % 15
            if cx > x + w - 8:
                break
            if (tohum + ci * 13) % 6 < 2:
                cry_r = 4 + (tohum + ci * 3) % 3
                pygame.draw.circle(game.ekran, (200, 230, 255), (cx, y - 2 - cry_r), cry_r)
                pygame.draw.circle(game.ekran, (220, 240, 255), (cx, y - 2 - cry_r), cry_r, 1)
                if cry_r > 4:
                    for ii in range(4):
                        ia = ii * 1.57 + math.sin(sz * 0.01 + ci) * 0.3
                        ix = cx + int(math.cos(ia) * (cry_r + 2))
                        iy = y - 2 - cry_r + int(math.sin(ia) * (cry_r + 2))
                        pygame.draw.line(game.ekran, (220, 240, 255), (cx, y - 2 - cry_r), (ix, iy), 1)
        for ki in range(w // 100):
            kx = x + 15 + ki * 100 + (tohum + ki * 17) % 35
            if kx > x + w - 20:
                break
            if (tohum + ki * 11) % 7 < 2:
                pygame.draw.circle(game.ekran, (230, 235, 245), (kx + 6, y - 8), 8)
                pygame.draw.circle(game.ekran, (245, 250, 255), (kx + 6, y - 8), 8, 1)
                pygame.draw.circle(game.ekran, (230, 235, 245), (kx + 6, y - 18), 6)
                pygame.draw.circle(game.ekran, (245, 250, 255), (kx + 6, y - 18), 6, 1)
                pygame.draw.circle(game.ekran, (20, 20, 20), (kx + 4, y - 20), 1)
                pygame.draw.circle(game.ekran, (20, 20, 20), (kx + 8, y - 20), 1)
                pygame.draw.line(game.ekran, (200, 100, 50), (kx + 6, y - 18), (kx + 10, y - 19), 1)


# ── Background ───────────────────────────────────────────────────
def _arka_ciz_anim() -> None:
    """Draw animated background elements: clouds, then seasonal anims."""
    m = game.mv
    z, h = assets.GENISLIK, assets.YUKSEKLIK
    sz = game.sz

    for bu in _arka_bulut:
        bu["x"] += bu["hiz"]
        bu["y"] += math.sin(sz * 0.01 + bu["s"]) * 0.1
        if bu["x"] > z + 200:
            bu["x"] = -bu["w"] - 50
            bu["y"] = random.randint(20, 120)
        s2 = pygame.Surface((bu["w"], bu["h"] * 2), pygame.SRCALPHA)
        a2 = max(0, min(60, 30 + int(math.sin(sz * 0.02 + bu["s"]) * 15)))
        pygame.draw.ellipse(s2, (255, 255, 255, a2), (0, bu["h"] // 2, bu["w"], bu["h"]))
        pygame.draw.ellipse(s2, (255, 255, 255, a2 - 10), (bu["w"] // 4, 0, bu["w"] // 2, bu["h"]))
        game.ekran.blit(s2, (int(bu["x"]), int(bu["y"])))

    animations.tum_animasyonlari_ciz()


def _ciz_arka_plan() -> None:
    """Load and draw the seasonal background image, then overlay animations."""
    global _arka_resimler
    m = game.mv
    z, h = assets.GENISLIK, assets.YUKSEKLIK

    if m not in _arka_resimler:
        img = None
        taban = os.path.dirname(os.path.abspath(__file__))
        for ext in ("png", "jpg"):
            path = os.path.join(taban, "resources", f"arka_{m}.{ext}")
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert()
                    break
                except Exception:
                    pass
        _arka_resimler[m] = img

    img = _arka_resimler.get(m)
    if img:
        if img.get_width() != z or img.get_height() != h:
            img = pygame.transform.scale(img, (z, h))
        game.ekran.blit(img, (0, 0))
    else:
        game.ekran.fill((30, 30, 50))

    _arka_ciz_anim()


# ── Public draw functions ────────────────────────────────────────
def platform_ciz() -> None:
    """Draw all platforms with textures and decorations."""
    rnk = game.rnk
    b = assets.BIOME[game.mv]

    for i, p in enumerate(game.plt):
        if i == 0:
            # Floor platform
            tex = game.TEXTURE_MAP.get(game.mv)
            if tex and game.tex_sheet:
                _ciz_texture(tex["soil"][0], tex["soil"][1], p.x, p.y, p.w, p.h)
                _ciz_texture(tex["grass"][0], tex["grass"][1], p.x, p.y - 3, p.w, 16)
            else:
                pygame.draw.rect(game.ekran, b["soil"], p)
                pygame.draw.rect(game.ekran, b["deep_soil"], p, 1)
                cim_r = pygame.Rect(p.x, p.y - 3, p.w, 6)
                pygame.draw.rect(game.ekran, b["grass"], cim_r)
                pygame.draw.line(game.ekran, b["grass"], (p.x, p.y - 3), (p.right, p.y - 3), 3)
                for ci in range(p.w // 15):
                    cx = p.x + ci * 15 + 5
                    cy = p.y - 3
                    if (cx * 7 + cy * 3) % 10 < 3:
                        dx = (cx * 5) % 5 - 2
                        dy = (cy * 7) % 5 + 3
                        pygame.draw.line(game.ekran, b["grass"], (cx, cy), (cx + dx, cy - dy), 2)
                for si in range(p.w // 60):
                    sx = p.x + si * 60 + 15
                    if (sx * 11 + p.y * 3) % 10 < 4:
                        pygame.draw.rect(game.ekran, b["stone"], (sx, p.y + 5, 20, 10))
        else:
            _ciz_platform_kenar(p, rnk, b)
            _ciz_dekorasyon(p, i)


def dusman_ciz(d: dict[str, Any]) -> None:
    """Draw an enemy with biome-specific appearance."""
    r = d["r"]
    cx, cy = r.x + 14, r.y + 25
    m = game.mv
    tip = d.get("tip", "gezgin")

    if m == "ilkbahar":
        body_c, eye_c = (50, 130, 50), (255, 255, 100) if tip != "kovalayan" else (255, 50, 50)
        pygame.draw.rect(game.ekran, body_c, (cx - 10, cy + 4, 20, 18))
        pygame.draw.rect(game.ekran, (70, 150, 70), (cx - 10, cy + 4, 20, 18), 1)
        pygame.draw.ellipse(game.ekran, (60, 160, 60), (cx - 14, cy - 14, 28, 22))
        pygame.draw.ellipse(game.ekran, (80, 180, 80), (cx - 14, cy - 14, 28, 22), 1)
        pygame.draw.circle(game.ekran, eye_c, (cx - 6, cy - 12), 4)
        pygame.draw.circle(game.ekran, eye_c, (cx + 6, cy - 12), 4)
        if tip == "kovalayan":
            pygame.draw.circle(game.ekran, assets.S, (cx - 6, cy - 12), 2)
            pygame.draw.circle(game.ekran, assets.S, (cx + 6, cy - 12), 2)
            pygame.draw.line(game.ekran, assets.S, (cx - 10, cy - 18), (cx - 4, cy - 16), 2)
            pygame.draw.line(game.ekran, assets.S, (cx + 10, cy - 18), (cx + 4, cy - 16), 2)

    elif m == "yaz":
        body_c, eye_c = (180, 150, 100), (255, 200, 50) if tip != "kovalayan" else (255, 50, 50)
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
        body_c, eye_c = (25, 20, 15), (60, 10, 60) if tip != "kovalayan" else (200, 20, 20)
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
        body_c, eye_c = (220, 230, 240), (150, 30, 30) if tip != "kovalayan" else (255, 0, 0)
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


def muhafiz_ciz(d: dict[str, Any]) -> None:
    """Draw a boss minion with a small armor plate."""
    r = d["r"]
    cx, cy = r.x + 12, r.y + 20
    m = game.mv

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

    # Armor plate
    pygame.draw.rect(game.ekran, (180, 180, 180), (cx - 4, cy - 14, 8, 4))
    pygame.draw.rect(game.ekran, (200, 200, 200), (cx - 4, cy - 14, 8, 4), 1)


def boss_ciz() -> None:
    """Draw the biome boss with difficulty-scaled skin and glow."""
    if not game.boss_sv or game.boss_hp <= 0:
        return

    bx, by = game.boss_x, game.boss_y
    m = game.mv
    zorluk = game.boss_zorluk or game.ayar["z"]
    skin = assets.BOSS_SKIN[zorluk]
    glow = assets.BOSS_GLOW[zorluk]
    sz = game.sz

    # Glow effect
    for gi in range(3 + skin):
        gr = 35 + gi * 15 + skin * 3
        s2 = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
        a2 = max(0, 60 - gi * 20)
        pygame.draw.circle(s2, (*glow, a2), (gr, gr), gr)
        game.ekran.blit(s2, (int(bx - gr), int(by - gr)))

    sc = 1.0 + skin * 0.12
    ofs = int(20 * (sc - 1))

    if m == "ilkbahar":
        pygame.draw.ellipse(game.ekran, (60, 140 + skin * 10, 60), (int(bx - 28 * sc), int(by - 15 * sc + ofs), int(56 * sc), int(40 * sc)))
        pygame.draw.ellipse(game.ekran, (200 - skin * 40, 50, 50), (int(bx - 20 * sc), int(by - 8 * sc + ofs), int(40 * sc), int(28 * sc)))
        pygame.draw.rect(game.ekran, (60, 140 + skin * 20, 60), (int(bx - 6 * sc), int(by + 10 + ofs), int(12 * sc), int(30 * sc)))
        pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx - 16 * sc), int(by - 22 * sc + ofs)), int(6 * sc))
        pygame.draw.circle(game.ekran, (255, 255, 100), (int(bx + 4 * sc), int(by - 22 * sc + ofs)), int(6 * sc))
        pygame.draw.circle(game.ekran, assets.S, (int(bx - 10 * sc), int(by - 20 * sc + ofs)), int(3 * sc))
        pygame.draw.circle(game.ekran, assets.S, (int(bx + 10 * sc), int(by - 20 * sc + ofs)), int(3 * sc))
        saksi_w = int(50 * sc)
        pygame.draw.polygon(game.ekran, (180 - skin * 30, 100 - skin * 10, 50), [
            (int(bx - saksi_w // 2), int(by + 40 * sc + ofs)),
            (int(bx + saksi_w // 2), int(by + 40 * sc + ofs)),
            (int(bx + saksi_w // 2 * 0.8), int(by + 60 * sc + ofs)),
            (int(bx - saksi_w // 2 * 0.8), int(by + 60 * sc + ofs)),
        ])
        if skin >= 1:
            for di in range(4):
                dx = bx - 30 + di * 20
                pygame.draw.polygon(game.ekran, (100, 180, 100), [(dx, int(by - 10 * sc + ofs)), (dx - 6, int(by - 20 * sc + ofs)), (dx + 6, int(by - 20 * sc + ofs))])
        if skin >= 2:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 10 * sc), int(by - 20 * sc + ofs)), int(5 * sc), int(2 * sc))
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 10 * sc), int(by - 20 * sc + ofs)), int(5 * sc), int(2 * sc))
            for _ in range(3):
                vx = bx - 20 + _ * 20
                vy = by + 20 * sc + ofs
                for _ in range(4):
                    pygame.draw.circle(game.ekran, (40, 100, 40), (int(vx), int(vy)), int(4 * sc))
                    vy += 8
        if skin >= 3:
            for ai in range(6):
                aa = sz * 0.1 + ai * 1.047
                ax = bx + int(math.cos(aa) * 34 * sc)
                ay = by - 28 * sc + int(math.sin(aa) * 8 * sc) + ofs
                pygame.draw.circle(game.ekran, (255, 50, 50), (ax, ay), int(6 * sc))
                pygame.draw.circle(game.ekran, (255, 200, 50), (ax, ay), int(3 * sc))

    elif m == "yaz":
        sc2 = 1.0 + skin * 0.15
        bx2 = int(bx * sc2 - bx * (sc2 - 1))
        by2 = int(by * sc2 - by * (sc2 - 1)) + ofs
        pygame.draw.polygon(game.ekran, (180 - skin * 40, 150 - skin * 20, 100 - skin * 20), [
            (int(bx2 - 35 * sc2), int(by2 + 35 * sc2)), (int(bx2 - 30 * sc2), int(by2)),
            (int(bx2), int(by2 - 10 * sc2)), (int(bx2 + 30 * sc2), int(by2)),
            (int(bx2 + 35 * sc2), int(by2 + 35 * sc2)),
        ])
        pygame.draw.circle(game.ekran, (190 - skin * 20, 160 - skin * 30, 110 - skin * 30), (int(bx2), int(by2 - 5 * sc2)), int(22 * sc2))
        pygame.draw.circle(game.ekran, (255 - skin * 80, 200 - skin * 50, 50), (int(bx2 - 8 * sc2), int(by2 - 10 * sc2)), int(6 * sc2))
        pygame.draw.circle(game.ekran, (255 - skin * 80, 200 - skin * 50, 50), (int(bx2 + 8 * sc2), int(by2 - 10 * sc2)), int(6 * sc2))
        if skin >= 1:
            for ri in range(8):
                ra = ri * 0.785 + sz * 0.02
                rx = bx2 + int(math.cos(ra) * 32 * sc2)
                ry = by2 + int(math.sin(ra) * 32 * sc2)
                pygame.draw.line(game.ekran, (255, 200, 50), (bx2, by2), (rx, ry), max(1, int(3 * sc2)))
        if skin >= 2:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx2 - 8 * sc2), int(by2 - 10 * sc2)), int(3 * sc2))
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx2 + 8 * sc2), int(by2 - 10 * sc2)), int(3 * sc2))
            for ki in range(4):
                ka = sz * 0.15 + ki * 1.57
                kx = bx2 + int(math.cos(ka) * 28 * sc2)
                ky = by2 + int(math.sin(ka) * 28 * sc2)
                pygame.draw.circle(game.ekran, (255, 100, 0), (kx, ky), int(4 * sc2))
        if skin >= 3:
            for hi in range(12):
                ha = sz * 0.05 + hi * 0.523
                hx = bx2 + int(math.cos(ha) * 40 * sc2)
                hy = by2 + int(math.sin(ha) * 10 * sc2)
                pygame.draw.circle(game.ekran, (200, 50, 255), (hx, hy), int(3 * sc2))
            for pi in range(5):
                pa = sz * 0.3 + pi * 1.256
                px = bx2 + int(math.cos(pa) * 50 * sc2)
                py = by2 - 10 + int(math.sin(pa) * 5)
                pygame.draw.circle(game.ekran, (255, 255, 100), (px, py), int(2 * sc2))

    elif m == "sonbahar":
        renk_k = (25 - skin * 5, 20 - skin * 5, 15)
        renk_g = (60 - skin * 15, 10, 60 - skin * 10)
        pygame.draw.rect(game.ekran, renk_k, (int(bx - 18 * sc), int(by + 8 * sc + ofs), int(36 * sc), int(35 * sc)))
        pygame.draw.rect(game.ekran, renk_k, (int(bx - 14 * sc), int(by - 20 * sc + ofs), int(28 * sc), int(28 * sc)))
        pygame.draw.rect(game.ekran, renk_g, (int(bx - 10 * sc), int(by - 16 * sc + ofs), int(8 * sc), int(6 * sc)))
        pygame.draw.rect(game.ekran, renk_g, (int(bx + 2 * sc), int(by - 16 * sc + ofs), int(8 * sc), int(6 * sc)))
        if skin >= 1:
            pygame.draw.line(game.ekran, renk_k, (int(bx - 18 * sc), int(by + 12 * sc + ofs)), (int(bx - 30 * sc), int(by + 25 * sc + ofs)), max(1, int(4 * sc)))
            pygame.draw.line(game.ekran, renk_k, (int(bx + 18 * sc), int(by + 12 * sc + ofs)), (int(bx + 30 * sc), int(by + 25 * sc + ofs)), max(1, int(4 * sc)))
        if skin >= 2:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 6 * sc), int(by - 13 * sc + ofs)), int(3 * sc))
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 6 * sc), int(by - 13 * sc + ofs)), int(3 * sc))
            for yi in range(3):
                ya = sz * 0.1 + yi * 2.0
                yx = bx + int(math.cos(ya) * 30 * sc)
                yy = by - 10 + int(math.sin(ya) * 5 * sc) + ofs
                pygame.draw.ellipse(game.ekran, (200 - yi * 30, 100 - yi * 20, 20), (yx, yy, int(8 * sc), int(4 * sc)))
        if skin >= 3:
            for si in range(8):
                sa = sz * 0.03 + si * 0.785
                sx = bx + int(math.cos(sa) * 38 * sc)
                sy = by + int(math.sin(sa) * 38 * sc) + ofs
                pygame.draw.circle(game.ekran, (150, 50, 200), (sx, sy), int(3 * sc))
                pygame.draw.circle(game.ekran, (200, 100, 255), (sx, sy), int(1 * sc))

    elif m == "kis":
        pygame.draw.ellipse(game.ekran, (220 - skin * 20, 230 - skin * 15, 240 - skin * 20), (int(bx - 30 * sc), int(by + ofs), int(60 * sc), int(50 * sc)))
        pygame.draw.circle(game.ekran, (230 - skin * 20, 235 - skin * 15, 245 - skin * 20), (int(bx), int(by - 8 * sc + ofs)), int(18 * sc))
        pygame.draw.circle(game.ekran, (150 + skin * 20, 30, 30), (int(bx - 6 * sc), int(by - 12 * sc + ofs)), int(4 * sc))
        pygame.draw.circle(game.ekran, (150 + skin * 20, 30, 30), (int(bx + 6 * sc), int(by - 12 * sc + ofs)), int(4 * sc))
        if skin >= 1:
            for bi in range(5):
                bx3 = bx - 25 + bi * 12
                by3 = by + 20 * sc + ofs
                pygame.draw.polygon(game.ekran, (200 - skin * 10, 220 - skin * 10, 255), [(bx3, by3), (bx3 - 5, int(by3 + 10 * sc)), (bx3 + 5, int(by3 + 10 * sc))])
        if skin >= 2:
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx - 6 * sc), int(by - 12 * sc + ofs)), int(6 * sc), int(2 * sc))
            pygame.draw.circle(game.ekran, (255, 0, 0), (int(bx + 6 * sc), int(by - 12 * sc + ofs)), int(6 * sc), int(2 * sc))
            for ti in range(6):
                ta = sz * 0.05 + ti * 1.047
                tx = bx + int(math.cos(ta) * 28 * sc)
                ty = by - 20 * sc + int(math.sin(ta) * 8 * sc) + ofs
                pygame.draw.circle(game.ekran, (200, 220, 255), (tx, ty), int(4 * sc))
        if skin >= 3:
            for fi in range(6):
                fa = sz * 0.04 + fi * 1.047
                fx = bx + int(math.cos(fa) * 40 * sc)
                fy = by + int(math.sin(fa) * 40 * sc) + ofs
                pygame.draw.circle(game.ekran, (180, 200, 255), (fx, fy), int(2 * sc))
                pygame.draw.line(game.ekran, (150, 180, 255), (bx, by + ofs), (fx, fy), 1)

    # Boss HP bar
    bbw, bbx = 300, assets.GENISLIK // 2 - 150
    bby = 55
    pygame.draw.rect(game.ekran, (40, 0, 0), (bbx, bby, bbw, 18))
    ratio = game.boss_hp / game.boss_max_hp
    pygame.draw.rect(game.ekran, glow, (bbx, bby, int(bbw * ratio), 18))
    pygame.draw.rect(game.ekran, assets.B, (bbx, bby, bbw, 18), 2)
    bn = config.BOSS_ADI.get(game.mv, "BOSS")
    game.ekran.blit(game.fk.render(bn, True, assets.B), (bbx + 5, bby - 16))
    game.ekran.blit(game.fk.render(f"{game.boss_hp}/{game.boss_max_hp}", True, assets.B), (bbx + bbw - 60, bby + 1))
