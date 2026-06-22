"""Enemy AI, projectile updates, and boss logic."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

import assets
import audio
import game
import particles


def _oyuncuya_carpti() -> None:
    """Handle player receiving damage from any source."""
    if game.kalkan_t > 0:
        game.kalkan_t = 0
        particles.ptk_patlatma(game.ox, game.oy, assets.KR, 15)
        audio.sfx_hasar()
    else:
        game.cn -= 1
        particles.ptk_ekle(game.ox, game.oy, assets.K, 12)
        audio.sfx_hasar()
        game.ox, game.oy = game.cp_x, game.cp_y
        game.hx = game.hy = 0.0


def _platforma_carptir(entity: dict[str, Any]) -> None:
    """Apply platform collision (ground) to an enemy dictionary."""
    vy = entity.get("vy", 0)
    if vy < 0:
        return
    for p in game.plt:
        if entity["r"].colliderect(p):
            entity["r"].bottom = p.top
            entity["vy"] = 0
            break


def dusman_guncelle(oc: pygame.Rect) -> None:
    """Update all enemy AI: movement, attack, player collision."""
    for d in game.dsm:
        dx = game.ox - d["r"].centerx
        dy = game.oy - d["r"].centery
        mesafe = math.sqrt(dx * dx + dy * dy)

        tip = d["tip"]

        # ── Jumper ────────────────────────────────────────────────
        if tip == "sıçrayan":
            if mesafe < 300 and mesafe > 0:
                d["r"].x += (dx / mesafe) * d["orj_h"] * 0.5
                if d.get("ziplama_cd", 0) <= 0 and mesafe < 200:
                    d["vy"] = -10
                    d["vx"] = (dx / mesafe) * 4
                    d["ziplama_cd"] = random.randint(60, 120)
                    particles.ptk_patlatma(d["r"].centerx, d["r"].bottom, (180, 180, 200), 5, 3)
                else:
                    d["ziplama_cd"] = max(0, d.get("ziplama_cd", 0) - 1)
            else:
                d["r"].x += d["h"]
                if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]:
                    d["h"] *= -1

            d["vy"] = d.get("vy", 0) + 0.5
            d["r"].y += d["vy"]
            _platforma_carptir(d)

        # ── Chaser ────────────────────────────────────────────────
        elif tip == "kovalayan":
            if mesafe < 350 and mesafe > 0:
                hiz = d["orj_h"] * 1.8
                d["r"].x += (dx / mesafe) * hiz
                d["r"].y += (dy / mesafe) * hiz * 0.4
                d["r"].x = max(d["sl"], min(d["sg"], d["r"].x))
                d["r"].y = max(50, min(assets.YUKSEKLIK - 80, d["r"].y))

                if d.get("ates_cd", 0) <= 0 and mesafe < 250 and random.random() < 0.02:
                    game.boss_btl.append({
                        "x": d["r"].centerx, "y": d["r"].centery,
                        "vx": (dx / mesafe) * 2, "vy": (dy / mesafe) * 2, "r": assets.K,
                    })
                    d["ates_cd"] = random.randint(60, 120)
                else:
                    d["ates_cd"] = max(0, d.get("ates_cd", 0) - 1)
            else:
                d["r"].x += d["h"]
                if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]:
                    d["h"] *= -1

        # ── Patrol ────────────────────────────────────────────────
        else:
            d["r"].x += d["h"]
            if d["r"].x <= d["sl"] or d["r"].x >= d["sg"]:
                d["h"] *= -1

        # Player collision
        if oc.colliderect(d["r"]):
            _oyuncuya_carpti()


def muhafiz_guncelle(oc: pygame.Rect) -> None:
    """Update boss minion AI: track player, shoot."""
    for mu in game.boss_muh[:]:
        dx = game.ox - mu["r"].centerx
        dy = game.oy - mu["r"].centery
        mesafe = math.sqrt(dx * dx + dy * dy)

        if mesafe < 300 and mesafe > 0:
            mu["r"].x += (dx / mesafe) * mu["h"]
            mu["r"].y += (dy / mesafe) * mu["h"] * 0.3
            mu["r"].x = max(mu["sl"], min(mu["sg"], mu["r"].x))
            mu["r"].y = max(80, min(assets.YUKSEKLIK - 80, mu["r"].y))

            if mu.get("ates_cd", 0) <= 0 and mesafe < 400:
                game.boss_btl.append({
                    "x": mu["r"].centerx, "y": mu["r"].centery,
                    "vx": (dx / mesafe) * 2.5, "vy": (dy / mesafe) * 2.5,
                    "r": (255, 100, 100),
                })
                mu["ates_cd"] = random.randint(80, 150)
            else:
                mu["ates_cd"] = max(0, mu.get("ates_cd", 0) - 1)

        if oc.colliderect(mu["r"]):
            _oyuncuya_carpti()


def mermi_guncelle() -> None:
    """Update player bullets: movement, collision with enemies/boss."""
    for b in game.bullets[:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += 0.1

        if b["x"] < -20 or b["x"] > assets.GENISLIK + 20 or b["y"] < -20 or b["y"] > assets.YUKSEKLIK + 20:
            game.bullets.remove(b)
            continue

        br = pygame.Rect(b["x"] - 5, b["y"] - 5, 10, 10)
        hit = False

        # Enemy collision
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

        # Minion collision
        for mu in game.boss_muh[:]:
            if br.colliderect(mu["r"]):
                mu["hp"] -= 1
                particles.ptk_patlatma(b["x"], b["y"], assets.KR, 10)
                audio.sfx_hasar()
                hit = True
                if mu["hp"] <= 0:
                    game.boss_muh.remove(mu)
                    particles.ptk_patlatma(b["x"], b["y"], assets.ALTIN, 15)
                break
        if hit:
            game.bullets.remove(b)
            continue

        # Boss collision
        if game.boss_sv and game.boss_hp > 0:
            if br.colliderect(pygame.Rect(game.boss_x - 35, game.boss_y - 35, 70, 70)):
                game.boss_hp -= b.get("dmg", 1)
                game.bullets.remove(b)
                audio.sfx_boss_hit()
                particles.ptk_patlatma(b["x"], b["y"], b["r"], 12)


def boss_mermi_guncelle(oc: pygame.Rect) -> None:
    """Update boss bullets: movement, player collision."""
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
            _oyuncuya_carpti()


def alev_topu_guncelle() -> None:
    """Update fireball projectiles: movement, spark particles, AOE damage."""
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

        particles.ptk_ekle(
            int(fb["x"] - 5 + random.random() * 10),
            int(fb["y"] - 5 + random.random() * 10),
            (255, random.randint(100, 200), 0), 3,
        )

        # Enemy hit
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

        # Minion hit
        for mu in game.boss_muh[:]:
            if fbr.colliderect(mu["r"]):
                mu["hp"] -= 5
                particles.ptk_patlatma(fb["x"], fb["y"], assets.KR, 18)
                audio.sfx_hasar()
                hit = True
                if mu["hp"] <= 0:
                    game.boss_muh.remove(mu)
                    particles.ptk_patlatma(fb["x"], fb["y"], assets.ALTIN, 25)
                break
        if hit:
            game.fireballs.remove(fb)
            continue

        # Boss hit
        if game.boss_sv and game.boss_hp > 0:
            if fbr.colliderect(pygame.Rect(game.boss_x - 35, game.boss_y - 35, 70, 70)):
                game.boss_hp -= 10
                game.fireballs.remove(fb)
                audio.sfx_boss_hit()
                particles.ptk_patlatma(fb["x"], fb["y"], (255, 100, 0), 30)
                particles.ptk_patlatma(fb["x"], fb["y"], assets.ALTIN, 15)


def _boss_at() -> None:
    """Execute the current boss attack pattern."""
    bx, by = game.boss_x, game.boss_y
    ptrn = game.boss_ptrn % 4
    zorluk_hiz = assets.BOSS_ATK_CD[game.ayar["z"]]
    spd = 3 + random.uniform(-0.5, 0.5)

    if ptrn == 0:
        # Single aimed bullet
        dx = game.ox - bx
        dy = game.oy - by
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            game.boss_btl.append({
                "x": bx, "y": by + 30,
                "vx": dx / d * spd, "vy": dy / d * spd, "r": assets.K,
            })
        game.boss_atk_cd = max(60, zorluk_hiz * 2 - game.boss_ptrn * 2)

    elif ptrn == 1:
        # 3-spread fan
        for li in range(-1, 2):
            dx = game.ox - bx + li * 40
            dy = game.oy - by
            d = math.sqrt(dx * dx + dy * dy)
            if d > 0:
                game.boss_btl.append({
                    "x": bx + li * 15, "y": by + 30,
                    "vx": dx / d * (spd + 0.5), "vy": dy / d * (spd + 0.5),
                    "r": (255, 100, 100),
                })
        game.boss_atk_cd = max(80, zorluk_hiz * 2 - game.boss_ptrn * 2)

    elif ptrn == 2:
        # 5-wave with fake bullets
        for wi in range(5):
            a3 = -1 + wi * 0.5
            dx = game.ox - bx + a3 * 80
            dy = game.oy - by
            d = math.sqrt(dx * dx + dy * dy)
            if d > 0:
                fake = random.random() < 0.3
                game.boss_btl.append({
                    "x": bx + wi * 8, "y": by + 30,
                    "vx": dx / d * (spd - 0.5) + random.uniform(-0.3, 0.3),
                    "vy": dy / d * (spd - 0.5) + random.uniform(-0.5, 0.5),
                    "r": (200, 50, 200), "s": 8 if not fake else 4, "fake": fake,
                })
        game.boss_atk_cd = max(100, zorluk_hiz * 2 - game.boss_ptrn * 2)

    else:
        # 8-way circular fountain
        for ai in range(8):
            a5 = ai * 0.785 + game.boss_timer * 0.02
            game.boss_btl.append({
                "x": bx, "y": by + 30,
                "vx": math.cos(a5) * spd, "vy": math.sin(a5) * spd,
                "r": (255, 50, 255),
            })
        game.boss_atk_cd = max(120, zorluk_hiz * 2)

    game.boss_ptrn = (game.boss_ptrn + 1) % 8
    audio.sfx_boss_ates()


def _boss_ozel_yetenek() -> None:
    """Execute biome-specific boss special ability."""
    bx, by = game.boss_x, game.boss_y
    bm = game.mv
    spd = 2 + random.uniform(-0.5, 0.5)

    if bm == "ilkbahar":
        for bi in range(6):
            a6 = bi * 1.047 + game.boss_timer * 0.01
            game.boss_btl.append({
                "x": bx, "y": by + 30,
                "vx": math.cos(a6) * spd * 0.6, "vy": math.sin(a6) * spd * 0.6,
                "r": (255, 100, 200), "s": 6,
            })
        game.boss_ozel_yetenek_cd = max(200, 350 - game.boss_ptrn * 3)
        game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (255, 200, 255), "tip": "cicek"})

    elif bm == "yaz":
        for bi in range(5):
            dx = game.ox - bx + random.randint(-50, 50)
            dy = game.oy - by + 100
            d = math.sqrt(dx * dx + dy * dy)
            if d > 0:
                game.boss_btl.append({
                    "x": bx + random.randint(-20, 20), "y": by + 30,
                    "vx": dx / d * spd * 1.2, "vy": dy / d * spd * 1.2,
                    "r": (255, 150, 0), "s": 10,
                })
        game.boss_ozel_yetenek_cd = max(220, 380 - game.boss_ptrn * 3)
        game.boss_ozel_efekt.append({"t": 25, "x": bx, "y": by, "r": (255, 200, 0), "tip": "alev"})

    elif bm == "sonbahar":
        for bi in range(12):
            a7 = bi * 0.524 + game.boss_timer * 0.03
            fake = random.random() < 0.4
            game.boss_btl.append({
                "x": bx, "y": by + 20,
                "vx": math.cos(a7) * spd * 0.8, "vy": math.sin(a7) * spd * 0.8,
                "r": (200, 120, 50), "s": 5 if not fake else 3, "fake": fake,
            })
        game.boss_ozel_yetenek_cd = max(180, 350 - game.boss_ptrn * 3)
        game.boss_ozel_efekt.append({"t": 30, "x": bx, "y": by, "r": (200, 150, 50), "tip": "yaprak"})

    elif bm == "kis":
        for bi in range(4):
            game.boss_btl.append({
                "x": game.ox + random.randint(-100, 100), "y": -20,
                "vx": 0, "vy": spd * 1.5, "r": (180, 220, 255), "s": 7,
            })
        game.boss_ozel_yetenek_cd = max(150, 300 - game.boss_ptrn * 3)
        game.boss_ozel_efekt.append({"t": 20, "x": bx, "y": by, "r": (200, 230, 255), "tip": "buz"})

    audio.sfx_boss_ates()


def boss_guncelle() -> None:
    """Full boss AI: movement mode switch, attack patterns, specials."""
    if not game.boss_sv or game.boss_hp <= 0:
        return

    game.boss_timer += 1
    game.boss_atk_cd -= 1
    game.boss_ozel_yetenek_cd -= 1
    game.boss_lazer_t = max(0, game.boss_lazer_t - 1)
    game.boss_minyon_t = max(0, game.boss_minyon_t - 1)
    game.boss_dalga_t = max(0, game.boss_dalga_t - 1)

    # Movement mode switch every 180 frames
    if game.boss_timer % 180 == 0:
        game.boss_hareket_mod = random.randint(0, 3)
        game.boss_yon_degis = game.boss_timer + random.randint(60, 180)

    # Mode 0: horizontal sine
    if game.boss_hareket_mod == 0:
        game.boss_x += game.boss_vx * game.boss_dir
        if game.boss_x < 100 or game.boss_x > assets.GENISLIK - 100:
            game.boss_dir *= -1
        game.boss_y = 80 + math.sin(game.boss_timer * 0.03) * 40

    # Mode 1: track player
    elif game.boss_hareket_mod == 1:
        dx = game.ox - game.boss_x
        dy = game.oy - game.boss_y
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            game.boss_x += (dx / d) * game.boss_vx * 1.5
            game.boss_y += (dy / d) * game.boss_vx * 0.8
        game.boss_hedefle = True
        if game.boss_timer > game.boss_yon_degis:
            game.boss_hareket_mod = 0
            game.boss_hedefle = False

    # Mode 2: up-down cycle
    elif game.boss_hareket_mod == 2:
        cyc = (game.boss_timer % 120) / 120.0
        game.boss_y = 80 + math.sin(cyc * math.pi * 2) * 100
        game.boss_x += game.boss_vx * game.boss_dir * 0.5
        if game.boss_x < 100 or game.boss_x > assets.GENISLIK - 100:
            game.boss_dir *= -1

    # Clamp position
    game.boss_x = max(60, min(assets.GENISLIK - 60, game.boss_x))
    game.boss_y = max(40, min(assets.YUKSEKLIK - 200, game.boss_y))

    # Attack
    if game.boss_atk_cd <= 0:
        _boss_at()

    # Special ability
    if game.boss_ozel_yetenek_cd <= 0:
        _boss_ozel_yetenek()

    # Tick effects
    for ef in game.boss_ozel_efekt[:]:
        ef["t"] -= 1
        if ef["t"] <= 0:
            game.boss_ozel_efekt.remove(ef)
