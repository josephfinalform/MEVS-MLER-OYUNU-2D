"""Menu, season select, settings, inventory, and leaderboard screens."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

import assets
import audio
import game
import save
import ui
from assets import Screen

# ── Menu particle data ───────────────────────────────────────────
_ma: float = 0.0
_menu_yildiz: list[dict[str, Any]] = []
_menu_krl: list[dict[str, Any]] = []
_menu_toz: list[dict[str, Any]] = []


def menu_par_baslat() -> None:
    """Initialize menu background particles (stars, season orbs, dust)."""
    global _menu_yildiz, _menu_krl, _menu_toz
    G = assets.GENISLIK
    Y = assets.YUKSEKLIK

    _menu_yildiz = [
        {
            "x": random.randint(0, G), "y": random.randint(0, Y),
            "hiz": random.uniform(0.1, 0.5), "r": random.randint(1, 3),
            "p": random.uniform(0, 6.28),
        }
        for _ in range(50)
    ]

    _menu_krl = []
    for i, m in enumerate(["ilkbahar", "yaz", "sonbahar", "kis"]):
        _menu_krl.append({
            "m": m, "a": i * 1.57 + random.uniform(-0.3, 0.3),
            "r": random.uniform(180, 250), "h": random.uniform(0.005, 0.015),
        })

    renkler = [(200, 180, 120, 30), (180, 200, 100, 25), (220, 200, 150, 35)]
    _menu_toz = [
        {
            "x": random.randint(0, G), "y": random.randint(-50, Y),
            "hiz": random.uniform(0.3, 1.2), "r": random.randint(1, 3),
            "renk": random.choice(renkler), "s": random.uniform(0, 6.28),
        }
        for _ in range(40)
    ]


menu_par_baslat()


def menu_ciz() -> str:
    """Draw the main menu. Returns the next screen name or 'exit'."""
    global _ma, _menu_yildiz, _menu_krl, _menu_toz

    audio.menu_muzik()
    _ma += 0.02
    G, Y = assets.GENISLIK, assets.YUKSEKLIK
    ek = game.ekran

    # Background gradient
    ek.fill((10, 8, 25))
    for i in range(Y):
        t = i / Y
        r = int(10 + t * 20)
        g = int(8 + t * 15)
        b = int(25 + t * 30)
        pygame.draw.line(ek, (r, g, b), (0, i), (G, i))

    # Stars
    for ys in _menu_yildiz:
        ys["y"] -= ys["hiz"]
        ys["x"] += math.sin(ys["p"] + _ma * 0.5) * 0.3
        if ys["y"] < -5:
            ys["y"] = Y + 5
            ys["x"] = random.randint(0, G)
        parlak = int(100 + 155 * (0.5 + 0.5 * math.sin(_ma * 2 + ys["p"])))
        pygame.draw.circle(ek, (parlak, parlak, 200), (int(ys["x"]), int(ys["y"])), ys["r"])

    # Orbiting season circles
    for kr in _menu_krl:
        kr["a"] += kr["h"]
        cx = G // 2 + int(math.cos(kr["a"]) * kr["r"])
        cy = 120 + int(math.sin(kr["a"]) * 60)
        renk = {
            "ilkbahar": (80, 220, 100, 40),
            "yaz": (255, 220, 60, 40),
            "sonbahar": (220, 140, 40, 40),
            "kis": (180, 200, 220, 40),
        }[kr["m"]]
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(s, renk, (40, 40), 35)
        ek.blit(s, (cx - 40, cy - 40))
        pygame.draw.circle(ek, renk[:3] + (80,), (cx, cy), 38, 2)

    # Grass silhouettes
    for i in range(0, Y, 40):
        yy = i + math.sin(_ma * 0.5 + i * 0.05) * 8
        sway = int(math.sin(_ma * 0.3 + i * 0.07) * 15)
        pygame.draw.line(ek, (30, 80, 40), (0, i), (25 + sway, yy), 3)
        if i % 80 < 5:
            pygame.draw.ellipse(ek, (40, 120, 50), (12 + int(math.sin(_ma * 0.2 + i * 0.1) * 5), yy - 10, 16, 8))
    for i in range(0, Y, 40):
        yy = i + math.sin(_ma * 0.5 + 2 + i * 0.05) * 8
        sway = int(math.sin(_ma * 0.3 + 1 + i * 0.07) * 15)
        pygame.draw.line(ek, (30, 80, 40), (G, i), (G - 25 + sway, yy), 3)
        if i % 80 < 5:
            pygame.draw.ellipse(ek, (40, 120, 50), (G - 28 + int(math.sin(_ma * 0.2 + 1 + i * 0.1) * 5), yy - 10, 16, 8))

    # Floating dust
    for tz in _menu_toz:
        tz["y"] += tz["hiz"]
        tz["x"] += math.sin(tz["s"] + _ma) * 0.5
        if tz["y"] > Y + 10:
            tz["y"] = -10
            tz["x"] = random.randint(0, G)
        s2 = pygame.Surface((tz["r"] * 4, tz["r"] * 4), pygame.SRCALPHA)
        pygame.draw.circle(s2, tz["renk"], (tz["r"] * 2, tz["r"] * 2), tz["r"])
        ek.blit(s2, (int(tz["x"] - tz["r"] * 2), int(tz["y"] - tz["r"] * 2)))

    # Title border
    pygame.draw.rect(ek, (180, 100, 255, 30), (0, 0, G, Y), 3, border_radius=12)

    # "MEVSIMLER" title
    ts = game.fb.render("MEVSIMLER", True, (50, 20, 80))
    ek.blit(ts, (G // 2 - ts.get_width() // 2 + 3, 103))
    p = abs(math.sin(_ma)) * 60
    t2 = game.fb.render("MEVSIMLER", True, (255, int(50 + p * 0.5), int(180 + p * 0.3)))
    ek.blit(t2, (G // 2 - ts.get_width() // 2 + 2, 102))
    t = game.fb.render("MEVSIMLER", True, assets.NP)
    ek.blit(t, (G // 2 - t.get_width() // 2, 100))

    pygame.draw.line(ek, assets.NP, (G // 2 - 150, 145), (G // 2 + 150, 145), 2)
    for i in range(4):
        ren = [assets.C1, assets.ALTIN, assets.YP, assets.KR][i]
        x = G // 2 - 120 + i * 80
        pygame.draw.circle(ek, ren, (x, 155), 5)
        pygame.draw.circle(ek, assets.B, (x, 155), 5, 1)
    a = game.fk.render("Bir Platform Oyunu", True, assets.NM)
    ek.blit(a, (G // 2 - a.get_width() // 2, 165))

    # Buttons panel
    y = 240
    p_surf = pygame.Surface((300, 410), pygame.SRCALPHA)
    p_surf.fill((30, 15, 50, 100))
    pygame.draw.rect(p_surf, (80, 40, 120, 120), p_surf.get_rect(), 2, border_radius=12)
    ek.blit(p_surf, (G // 2 - 150, y - 15))

    if save.var_mi():
        if ui.btn("DEVAM ET", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT, assets.NY):
            save.yukle()
            import levels
            game.cn = assets.z_can[game.ayar["z"]]
            levels.lv_yukle(game.mv, game.rnd)
            return Screen.OYUN.value
        y += 65

    if ui.btn("BASLA", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT,
              assets.NY if not save.var_mi() else assets.NM):
        return Screen.SEASON_SELECT.value
    y += 65

    if ui.btn("AYARLAR", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT, assets.NM):
        return Screen.SETTINGS.value
    y += 65

    if ui.btn("ENVANTER", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT, assets.ALTIN):
        return Screen.ENVANTER.value
    y += 65

    if ui.btn("PUAN TABLOSU", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT, assets.ALTIN):
        return Screen.LEADERBOARD.value
    y += 65

    if ui.btn("CIKIS", G // 2 - 120, y, 240, 55, assets.GT, assets.AGT, assets.K):
        return "exit"

    # Season strip at bottom
    season_colors = [(80, 220, 100), (255, 220, 60), (220, 140, 40), (180, 200, 220)]
    for i in range(G):
        ren = season_colors[(i // 150) % 4]
        pygame.draw.line(ek, ren, (i, Y - 3), (i, Y))

    return Screen.MENU.value


def season_select_ciz() -> str:
    """Draw the season selection grid. Returns next screen."""
    ek = game.ekran
    G, Y = assets.GENISLIK, assets.YUKSEKLIK
    ek.fill((15, 10, 30))

    for i in range(0, G, 80):
        pygame.draw.line(ek, (25, 15, 45), (i, 0), (i, Y), 1)

    t = game.fb.render("MEVSIM SEC", True, assets.NP)
    ek.blit(t, (G // 2 - t.get_width() // 2, 60))

    sezonlar = [
        ("ilkbahar", "ILKBAHAR", assets.C1),
        ("yaz", "YAZ", assets.ALTIN),
        ("sonbahar", "SONBAHAR", assets.YP),
        ("kis", "KIS", assets.KR),
    ]
    for i, (anahtar, isim, renk) in enumerate(sezonlar):
        bx = G // 2 - 200 + (i % 2) * 210
        by = 160 + (i // 2) * 160
        hover = pygame.Rect(bx, by, 190, 130).collidepoint(pygame.mouse.get_pos())

        pygame.draw.rect(ek, (40, 20, 60) if hover else (25, 15, 45), (bx, by, 190, 130), border_radius=12)
        pygame.draw.rect(ek, renk, (bx, by, 190, 130), 3, border_radius=12)

        pygame.draw.circle(ek, renk, (bx + 50, by + 40), 25)
        pygame.draw.circle(ek, (255, 255, 255, 60), (bx + 45, by + 35), 8)

        ek.blit(game.fm.render(isim, True, renk), (bx + 90, by + 25))
        ek.blit(game.fk.render(anahtar.upper(), True, assets.AGT), (bx + 90, by + 60))

        if hover and game.ft:
            save.sil()
            import levels
            game.si = assets.ms.index(anahtar)
            game.envanter.clear()
            game.aktif_k = None
            game.yuksek_puan.clear()
            game.cn = assets.z_can[game.ayar["z"]]
            levels.lv_yukle(anahtar)
            return Screen.OYUN.value

    if ui.btn("GERI", G // 2 - 100, Y - 100, 200, 50, assets.GT, assets.AGT, assets.NP):
        return Screen.MENU.value
    return Screen.SEASON_SELECT.value


def _ciz_slider(
    etiket: str,
    x: int,
    y: int,
    deger: int,
    w: int = 200,
) -> int:
    """Draw a horizontal slider, return updated value."""
    ek = game.ekran
    sl_x = x + 10
    pygame.draw.rect(ek, assets.GT, (sl_x, y + 15, w, 10))
    pygame.draw.rect(ek, assets.NM, (sl_x, y + 15, int(w * deger / 100), 10))
    if pygame.Rect(sl_x, y + 5, w, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        deger = max(0, min(100, int((pygame.mouse.get_pos()[0] - sl_x) / w * 100)))
    return deger


def settings_ciz() -> str:
    """Draw the settings screen. Returns next screen."""
    ek = game.ekran
    G, Y = assets.GENISLIK, assets.YUKSEKLIK
    ek.fill((20, 20, 40))

    for i in range(0, G, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, Y), 1)

    t = game.fb.render("AYARLAR", True, assets.NM)
    ek.blit(t, (G // 2 - t.get_width() // 2, 50))

    # Difficulty
    ek.blit(game.f.render("ZORLUK", True, assets.B), (G // 2 - 200, 130))
    for i, z in enumerate(["kolay", "orta", "zor", "imkansiz"]):
        sx = G // 2 - 280 + i * 140
        secili = game.ayar["z"] == z
        if ui.btn(z.upper(), sx, 165, 120, 40, assets.MM if secili else assets.GT, assets.AGT):
            game.ayar["z"] = z

    # Fullscreen toggle
    ek.blit(game.f.render("TAM EKRAN", True, assets.B), (G // 2 - 200, 240))
    td = "ACIK" if game.te_mi else "KAPALI"
    if ui.btn(td, G // 2 + 50, 235, 140, 40, assets.GT, assets.AGT, assets.NY if game.te_mi else assets.K):
        game.te_mi = not game.te_mi
        pygame.display.toggle_fullscreen()

    # Lobby volume
    oy = 310
    ek.blit(game.f.render(f"LOBI SES: {game.ayar['lobi_ses']}%", True, assets.B), (G // 2 - 200, oy))
    if ui.btn("-", G // 2 + 10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["lobi_ses"] = max(0, game.ayar["lobi_ses"] - 10)
        audio.muzik_ses(game.ayar["lobi_ses"] / 100)
    game.ayar["lobi_ses"] = _ciz_slider("", G // 2 + 70, oy, game.ayar["lobi_ses"])
    audio.muzik_ses(game.ayar["lobi_ses"] / 100)
    if ui.btn("+", G // 2 + 70 + 200 + 10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["lobi_ses"] = min(100, game.ayar["lobi_ses"] + 10)
        audio.muzik_ses(game.ayar["lobi_ses"] / 100)

    # Game volume
    oy += 75
    ek.blit(game.f.render(f"OYUN SES: {game.ayar['ses']}%", True, assets.B), (G // 2 - 200, oy))
    if ui.btn("-", G // 2 + 10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = max(0, game.ayar["ses"] - 10)
        audio.sfx_ses_ayarla()
    game.ayar["ses"] = _ciz_slider("", G // 2 + 70, oy, game.ayar["ses"])
    audio.sfx_ses_ayarla()
    if ui.btn("+", G // 2 + 70 + 200 + 10, oy, 50, 35, assets.GT, assets.AGT):
        game.ayar["ses"] = min(100, game.ayar["ses"] + 10)
        audio.sfx_ses_ayarla()

    # Controls reference
    oy += 75
    ek.blit(game.f.render("KONTROLLER", True, assets.B), (G // 2 - 200, oy))
    kontroller = [
        "OK SAG/SOL - Hareket",
        "SPACE - Zipla",
        "SAG TIK - Alev Topu",
        "ESC - Menuye don",
        "R - Yeniden baslat",
    ]
    for i, k in enumerate(kontroller):
        ek.blit(game.fk.render(k, True, assets.AGT), (G // 2 - 200, oy + 35 + i * 25))

    if ui.btn("GERI", G // 2 - 100, 620, 200, 50, assets.GT, assets.AGT, assets.NP):
        return game.onceki_drm or "menu"
    return Screen.SETTINGS.value


def env_ciz() -> str:
    """Draw the inventory/costume screen. Returns next screen."""
    ek = game.ekran
    G, Y = assets.GENISLIK, assets.YUKSEKLIK
    ek.fill((20, 20, 40))

    for i in range(0, G, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, Y), 1)

    t = game.fb.render("ENVANTER", True, assets.ALTIN)
    ek.blit(t, (G // 2 - t.get_width() // 2, 50))

    if not game.envanter:
        ek.blit(game.f.render("Henuz kostumun yok!", True, assets.AGT), (G // 2 - 120, 200))
        ek.blit(game.f.render("Mevsimleri tamamlayarak kostum kazan.", True, assets.AGT), (G // 2 - 180, 240))
    else:
        for i, k in enumerate(game.envanter):
            kx = G // 2 - 200 + (i % 2) * 220
            ky = 130 + (i // 2) * 120
            kr2 = pygame.Rect(kx, ky, 200, 100)
            secili = game.aktif_k == k

            pygame.draw.rect(ek, assets.MM if secili else assets.GT, kr2, border_radius=8)
            pygame.draw.rect(ek, assets.ALTIN if secili else assets.AGT, kr2, 2, border_radius=8)

            kostum = assets.KOSTUMLER[k]
            ek.blit(game.f.render(kostum.name, True, assets.B), (kx + 10, ky + 10))
            ek.blit(game.fk.render(kostum.description, True, assets.AGT), (kx + 10, ky + 45))

            hover = kr2.collidepoint(pygame.mouse.get_pos())
            if secili or hover:
                ox2, oy2 = kx + 170, ky + 50
                pygame.draw.circle(ek, assets.MM, (ox2, oy2 - 8), 8)
                pygame.draw.rect(ek, kostum.color, (ox2 - 6, oy2, 12, 30))
                pygame.draw.circle(ek, kostum.color, (ox2, oy2 - 10), 6)

            if hover and game.ft:
                game.aktif_k = k if game.aktif_k != k else None

    if ui.btn("GERI", G // 2 - 100, 580, 200, 50, assets.GT, assets.AGT, assets.NP):
        return Screen.MENU.value
    return Screen.ENVANTER.value


def leaderboard_ciz() -> str:
    """Draw the leaderboard screen. Returns next screen."""
    ek = game.ekran
    G, Y = assets.GENISLIK, assets.YUKSEKLIK
    ek.fill((20, 20, 40))

    for i in range(0, G, 100):
        pygame.draw.line(ek, (30, 0, 50), (i, 0), (i, Y), 1)

    t = game.fb.render("PUAN TABLOSU", True, assets.ALTIN)
    ek.blit(t, (G // 2 - t.get_width() // 2, 50))

    sirali = sorted(game.yuksek_puan.items(), key=lambda x: x[1], reverse=True)
    if not sirali:
        ek.blit(game.f.render("Henuz puan kaydi yok!", True, assets.AGT), (G // 2 - 140, 250))
    else:
        medal_colors = [(255, 215, 0), (200, 200, 200), (180, 120, 60), (150, 150, 180)]
        for i, (sezon, p) in enumerate(sirali):
            renk = medal_colors[i] if i < 4 else (200, 200, 200)
            sira = f"{i + 1}. {sezon.upper()}"
            pyazi = game.fm.render(f"{sira}  -  {p}", True, renk)
            ek.blit(pyazi, (G // 2 - pyazi.get_width() // 2, 150 + i * 55))

    if ui.btn("GERI", G // 2 - 100, 580, 200, 50, assets.GT, assets.AGT, assets.NP):
        return Screen.MENU.value
    return Screen.LEADERBOARD.value


def lbl_ciz(metin: str) -> None:
    """Draw a transition label screen."""
    ek = game.ekran
    ek.fill((10, 8, 25))
    t = game.fb.render(metin, True, assets.NP)
    ek.blit(t, (assets.GENISLIK // 2 - t.get_width() // 2, 230))
    t2 = game.fk.render("Bir sonraki mevsime geciliyor...", True, assets.NM)
    ek.blit(t2, (assets.GENISLIK // 2 - t2.get_width() // 2, 280))
