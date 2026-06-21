import math
import random
import os
import pygame
import assets
import game
import particles

CHAR = None
_onceki_oy = 0
_onceki_yr = True

def _yukle_char():
    global CHAR
    if CHAR is None:
        taban = os.path.dirname(os.path.abspath(__file__))
        try:
            img = pygame.image.load(os.path.join(taban, "char.png")).convert_alpha()
            CHAR = img
        except:
            CHAR = None

MEME_K = 0.3; MEME_D = 0.6; GOT_K = 0.4; GOT_D = 0.7

class KrkFizik:
    def __init__(self):
        self.msx = 0; self.msy = 0; self.mxv = 0; self.myv = 0
        self.gsx = 0; self.gsy = 0; self.gv = 0
        self.sf = 0; self.kb = 0

    def guncelle(self, hizlanma):
        self.mxv += (hizlanma * 0.3 - self.msx) * 0.05
        self.msx += self.mxv; self.msx *= 0.9
        self.myv += (-self.msy * MEME_K - self.myv * MEME_D) * 0.1
        self.myv += abs(hizlanma) * 0.02
        self.msy += self.myv

        self.gv += (-self.gsy * GOT_K - self.gv * GOT_D) * 0.1
        self.gv += abs(hizlanma) * 0.03
        self.gsy += self.gv

        self.sf += 0.08
        self.kb = max(0, self.kb - 0.05)

fizik = KrkFizik()

def ciz_krk(x, y, yn, yy=0):
    game.sz += 0.05; game.gk += 1; y += yy
    game.sh += (game.hx*0.3 - game.sh)*0.15
    iv = pygame.Vector2(math.sin(game.sz)*2, math.sin(game.sz*0.6)*0.8)

    global _onceki_oy, _onceki_yr

    hizlanma = game.hx * 0.1
    fizik.guncelle(hizlanma)

    yon = 1 if yn >= 0 else -1
    sx = x
    sy = y

    # === BAS ===
    pygame.draw.ellipse(game.ekran, assets.TEN, (sx - 13, sy - 46, 26, 36))
    pygame.draw.ellipse(game.ekran, (245, 210, 195), (sx - 12, sy - 40, 12, 16))
    pygame.draw.ellipse(game.ekran, (245, 210, 195), (sx + 1, sy - 40, 12, 16))
    pygame.draw.line(game.ekran, (240, 195, 180), (sx - 9, sy - 28), (sx - 4, sy - 30), 1)
    pygame.draw.line(game.ekran, (240, 195, 180), (sx + 4, sy - 30), (sx + 9, sy - 28), 1)
    pygame.draw.arc(game.ekran, (230, 190, 175), (sx - 11, sy - 18, 22, 12), 0.1, 3.0, 1)

    # === BURUN ===
    pygame.draw.line(game.ekran, (225, 185, 165), (sx, sy - 24), (sx, sy - 19), 1)
    pygame.draw.circle(game.ekran, (220, 180, 160), (sx, sy - 19), 1)
    pygame.draw.line(game.ekran, (230, 190, 170), (sx - 1, sy - 22), (sx - 3, sy - 21), 1)
    pygame.draw.line(game.ekran, (230, 190, 170), (sx + 1, sy - 22), (sx + 3, sy - 21), 1)

    # === GOZLER ===
    ga = game.gk % 180 > 5
    if ga:
        pygame.draw.ellipse(game.ekran, assets.B, (sx - 11, sy - 39, 11, 9))
        pygame.draw.ellipse(game.ekran, assets.B, (sx + 1, sy - 39, 11, 9))
        pygame.draw.ellipse(game.ekran, (250, 250, 255), (sx - 10, sy - 38, 9, 7))
        pygame.draw.ellipse(game.ekran, (250, 250, 255), (sx + 2, sy - 38, 9, 7))
        pygame.draw.circle(game.ekran, (255, 220, 50), (sx - 5, sy - 35), 5)
        pygame.draw.circle(game.ekran, (255, 220, 50), (sx + 5, sy - 35), 5)
        pygame.draw.circle(game.ekran, (255, 160, 30), (sx - 5, sy - 35), 5, 1)
        pygame.draw.circle(game.ekran, (255, 160, 30), (sx + 5, sy - 35), 5, 1)
        for i in range(4):
            a_s = i * 1.57
            pygame.draw.line(game.ekran, (255, 180, 40), (sx - 5 + int(math.cos(a_s)*3), sy - 35 + int(math.sin(a_s)*3)), (sx - 5 + int(math.cos(a_s)*4), sy - 35 + int(math.sin(a_s)*4)), 1)
            pygame.draw.line(game.ekran, (255, 180, 40), (sx + 5 + int(math.cos(a_s)*3), sy - 35 + int(math.sin(a_s)*3)), (sx + 5 + int(math.cos(a_s)*4), sy - 35 + int(math.sin(a_s)*4)), 1)
        pygame.draw.circle(game.ekran, assets.S, (sx - 5, sy - 35), 2)
        pygame.draw.circle(game.ekran, assets.S, (sx + 5, sy - 35), 2)
        pygame.draw.circle(game.ekran, (255, 255, 255), (sx - 7, sy - 37), 1)
        pygame.draw.circle(game.ekran, (255, 255, 255), (sx + 3, sy - 37), 1)
        for k, kx in enumerate([-11, -9, 9, 11]):
            kys = -39 if k < 2 else -39
            ky2 = -42 + k * 0.5 if k < 2 else -42 + (k - 2) * 0.5
            pygame.draw.line(game.ekran, (30, 30, 30), (sx + kx, sy + kys), (sx + kx - 1 + k * 0.5, sy + ky2), 1)
        for kx in [-8, -4, 4, 8]:
            pygame.draw.line(game.ekran, (60, 60, 60), (sx + kx, sy - 31), (sx + kx - 0.5, sy - 29), 1)
    else:
        pygame.draw.line(game.ekran, (40, 40, 40), (sx - 10, sy - 35), (sx - 1, sy - 35), 2)
        pygame.draw.line(game.ekran, (40, 40, 40), (sx + 1, sy - 35), (sx + 10, sy - 35), 2)

    # === KASLAR ===
    pygame.draw.line(game.ekran, (180, 120, 140), (sx - 10, sy - 43), (sx - 2, sy - 44), 2)
    pygame.draw.line(game.ekran, (180, 120, 140), (sx + 2, sy - 44), (sx + 10, sy - 43), 2)

    # === AGIZ ===
    if game.yr and abs(game.hx) < 0.5:
        pygame.draw.arc(game.ekran, (220, 170, 160), (sx - 5, sy - 24, 10, 7), 0.1, 3.0, 2)
    else:
        pygame.draw.arc(game.ekran, (210, 160, 150), (sx - 4, sy - 22, 8, 5), 0, 3.14, 2)
        pygame.draw.line(game.ekran, (190, 140, 130), (sx - 5, sy - 23), (sx + 5, sy - 23), 2)
        pygame.draw.line(game.ekran, (180, 130, 120), (sx, sy - 22), (sx, sy - 21), 1)
    pygame.draw.line(game.ekran, (230, 190, 180), (sx - 2, sy - 20), (sx + 2, sy - 20), 1)

    # === BOYUN ===
    pygame.draw.rect(game.ekran, assets.TEN, (sx - 4, sy - 14, 8, 6))
    pygame.draw.line(game.ekran, (220, 180, 165), (sx - 3, sy - 14), (sx - 3, sy - 9), 1)
    pygame.draw.line(game.ekran, (220, 180, 165), (sx + 3, sy - 14), (sx + 3, sy - 9), 1)
    pygame.draw.line(game.ekran, (215, 175, 160), (sx - 6, sy - 8), (sx + 6, sy - 8), 1)

    # === GOVDE ===
    pygame.draw.rect(game.ekran, (240, 235, 225), (sx - 13, sy - 10, 26, 28), border_radius=2)
    for i in range(3):
        yy_tmp = sy - 6 + i * 8
        pygame.draw.line(game.ekran, (235, 230, 220), (sx - 10, yy_tmp), (sx + 10, yy_tmp), 1)
    pygame.draw.rect(game.ekran, (215, 210, 200), (sx - 13, sy - 10, 26, 28), 1, border_radius=2)

    pygame.draw.polygon(game.ekran, (230, 225, 215), [(sx - 5, sy - 10), (sx - 9, sy - 3), (sx, sy - 4)])
    pygame.draw.polygon(game.ekran, (230, 225, 215), [(sx + 5, sy - 10), (sx + 9, sy - 3), (sx, sy - 4)])
    pygame.draw.polygon(game.ekran, (220, 215, 205), [(sx - 5, sy - 10), (sx - 9, sy - 3), (sx, sy - 4)], 1)
    pygame.draw.polygon(game.ekran, (220, 215, 205), [(sx + 5, sy - 10), (sx + 9, sy - 3), (sx, sy - 4)], 1)

    pygame.draw.polygon(game.ekran, (15, 15, 15), [(sx - 2, sy - 4), (sx + 2, sy - 4), (sx + 1, sy + 6), (sx, sy + 10), (sx - 1, sy + 6)])
    pygame.draw.polygon(game.ekran, (30, 30, 30), [(sx - 2, sy - 4), (sx + 2, sy - 4), (sx + 1, sy + 6), (sx, sy + 10), (sx - 1, sy + 6)], 1)
    pygame.draw.line(game.ekran, (40, 40, 40), (sx, sy - 3), (sx, sy + 4), 1)
    pygame.draw.circle(game.ekran, (200, 200, 200), (sx, sy + 2), 1)

    for i in range(4):
        yy_tmp = sy - 4 + i * 6
        pygame.draw.circle(game.ekran, (210, 205, 195), (sx, yy_tmp), 1)
        pygame.draw.circle(game.ekran, (225, 220, 210), (sx - 1, yy_tmp - 1), 1)

    pygame.draw.line(game.ekran, (230, 225, 215), (sx - 12, sy + 6), (sx - 16, sy + 12), 1)
    pygame.draw.line(game.ekran, (230, 225, 215), (sx + 12, sy + 6), (sx + 16, sy + 12), 1)

    # === MEMELER ===
    meme_renk = (240, 235, 225)
    meme_sol_x = sx - 9 + fizik.msx; meme_sol_y = sy - 4 + abs(fizik.msy) * 2
    meme_sag_x = sx + 9 + fizik.msx; meme_sag_y = sy - 4 + abs(fizik.msy) * 2
    pygame.draw.ellipse(game.ekran, meme_renk, (meme_sol_x - 5, meme_sol_y - 4, 10, 12))
    pygame.draw.ellipse(game.ekran, meme_renk, (meme_sag_x - 5, meme_sag_y - 4, 10, 12))
    pygame.draw.ellipse(game.ekran, (250, 245, 235), (meme_sol_x - 4, meme_sol_y - 3, 8, 10))
    pygame.draw.ellipse(game.ekran, (250, 245, 235), (meme_sag_x - 4, meme_sag_y - 3, 8, 10))
    pygame.draw.ellipse(game.ekran, (230, 225, 215), (meme_sol_x - 3, meme_sol_y - 1, 6, 8))
    pygame.draw.ellipse(game.ekran, (230, 225, 215), (meme_sag_x - 3, meme_sag_y - 1, 6, 8))

    # === BEL ===
    pygame.draw.rect(game.ekran, (240, 235, 225), (sx - 13, sy + 14, 26, 6))
    pygame.draw.rect(game.ekran, (15, 15, 20), (sx - 11, sy + 18, 22, 5))
    pygame.draw.rect(game.ekran, (25, 25, 30), (sx - 11, sy + 18, 22, 5), 1)
    pygame.draw.rect(game.ekran, (180, 180, 180), (sx - 2, sy + 19, 4, 3))
    pygame.draw.rect(game.ekran, (200, 200, 200), (sx - 1, sy + 20, 2, 1))

    # === BACAKLAR ===
    ba = 0; syk = -6; sagk = -6
    if not game.yr:
        ba = 0; syk = -6; sagk = -6
    elif abs(game.hx) > 1:
        ba = math.sin(game.sz * 8) * 30 * yon
        syk = abs(math.sin(game.sz * 8)) * 6
        sagk = abs(math.cos(game.sz * 8)) * 6
    else:
        ba = iv.x * 3; syk = iv.x * 0.5; sagk = -iv.x * 0.5

    sol_b_x = sx - 9 + ba * 0.08; sag_b_x = sx + 2 - ba * 0.08

    pygame.draw.rect(game.ekran, (15, 15, 22), (sol_b_x, sy + 22 + syk, 9, 16))
    pygame.draw.rect(game.ekran, (15, 15, 22), (sag_b_x, sy + 22 + sagk, 9, 16))
    pygame.draw.line(game.ekran, (25, 25, 32), (sol_b_x + 4, sy + 24 + syk), (sol_b_x + 4, sy + 36 + syk), 1)
    pygame.draw.line(game.ekran, (25, 25, 32), (sag_b_x + 4, sy + 24 + sagk), (sag_b_x + 4, sy + 36 + sagk), 1)
    pygame.draw.line(game.ekran, (20, 20, 28), (sol_b_x + 1, sy + 26 + syk), (sol_b_x + 7, sy + 28 + syk), 1)
    pygame.draw.line(game.ekran, (20, 20, 28), (sag_b_x + 1, sy + 26 + sagk), (sag_b_x + 7, sy + 28 + sagk), 1)
    pygame.draw.line(game.ekran, (30, 30, 38), (sol_b_x, sy + 22 + syk), (sol_b_x, sy + 38 + syk), 1)
    pygame.draw.line(game.ekran, (30, 30, 38), (sag_b_x, sy + 22 + sagk), (sag_b_x, sy + 38 + sagk), 1)

    # === GOT ===
    got_y = sy + 20 + abs(fizik.gsy) * 3
    pygame.draw.ellipse(game.ekran, (20, 20, 30), (sol_b_x - 2, got_y - 3, 12, 10))
    pygame.draw.ellipse(game.ekran, (20, 20, 30), (sag_b_x - 2, got_y - 3, 12, 10))
    pygame.draw.ellipse(game.ekran, (30, 30, 40), (sol_b_x - 1, got_y - 2, 10, 8))
    pygame.draw.ellipse(game.ekran, (30, 30, 40), (sag_b_x - 1, got_y - 2, 10, 8))

    # === AYAKKABI ===
    pygame.draw.ellipse(game.ekran, (100, 60, 35), (sol_b_x - 4, sy + 36 + syk, 14, 8))
    pygame.draw.ellipse(game.ekran, (100, 60, 35), (sag_b_x - 4, sy + 36 + sagk, 14, 8))
    pygame.draw.ellipse(game.ekran, (120, 75, 45), (sol_b_x - 3, sy + 37 + syk, 12, 6))
    pygame.draw.ellipse(game.ekran, (120, 75, 45), (sag_b_x - 3, sy + 37 + sagk, 12, 6))
    pygame.draw.rect(game.ekran, (60, 35, 20), (sol_b_x - 4, sy + 42 + syk, 14, 3))
    pygame.draw.rect(game.ekran, (60, 35, 20), (sag_b_x - 4, sy + 42 + sagk, 14, 3))
    pygame.draw.line(game.ekran, (50, 25, 15), (sol_b_x - 2, sy + 43 + syk), (sol_b_x + 8, sy + 43 + syk), 1)
    pygame.draw.line(game.ekran, (50, 25, 15), (sag_b_x - 2, sy + 43 + sagk), (sag_b_x + 8, sy + 43 + sagk), 1)
    for i in range(3):
        pygame.draw.circle(game.ekran, (50, 30, 15), (sol_b_x + i * 3 - 1, sy + 38 + syk), 1)
        pygame.draw.circle(game.ekran, (50, 30, 15), (sag_b_x + i * 3 - 1, sy + 38 + sagk), 1)
    pygame.draw.line(game.ekran, (50, 30, 15), (sol_b_x + 1, sy + 37 + syk), (sol_b_x + 4, sy + 40 + syk), 1)
    pygame.draw.line(game.ekran, (50, 30, 15), (sag_b_x + 1, sy + 37 + sagk), (sag_b_x + 4, sy + 40 + sagk), 1)
    pygame.draw.line(game.ekran, (140, 90, 55), (sol_b_x - 1, sy + 38 + syk), (sol_b_x + 5, sy + 38 + syk), 1)
    pygame.draw.line(game.ekran, (140, 90, 55), (sag_b_x - 1, sy + 38 + sagk), (sag_b_x + 5, sy + 38 + sagk), 1)

    # === KOLLAR ===
    wd_cd = assets.WP_DATA[game.mv]["cd"] if game.weapon else 10
    ates_geri_tepme = (wd_cd - game.shoot_cd) / wd_cd if game.shoot_cd > 0 else 0
    ates_geri_tepme = max(0, min(1, ates_geri_tepme))
    kol_sag = math.sin(game.sz * 6) * 3 if abs(game.hx) > 1 else 0
    kol_sag += ates_geri_tepme * 8 * yon
    if game.weapon:
        pygame.draw.line(game.ekran, (240, 235, 225), (sx - 15, sy - 8), (sx - 28 + kol_sag, sy + 2), 5)
        pygame.draw.line(game.ekran, (240, 235, 225), (sx + 15, sy - 8), (sx + 26 - kol_sag, sy + 2), 5)
        pygame.draw.line(game.ekran, (225, 220, 210), (sx - 15, sy - 7), (sx - 27 + kol_sag, sy + 3), 1)
        pygame.draw.line(game.ekran, (225, 220, 210), (sx + 15, sy - 7), (sx + 25 - kol_sag, sy + 3), 1)
        pygame.draw.line(game.ekran, (220, 215, 205), (sx - 27 + kol_sag, sy), (sx - 27 + kol_sag, sy + 4), 2)
        pygame.draw.line(game.ekran, (220, 215, 205), (sx + 25 - kol_sag, sy), (sx + 25 - kol_sag, sy + 4), 2)

        m = game.mv
        wr = assets.WP_DATA[m]["r"]
        w_x = sx + (22 if yon >= 0 else -22)
        w_y = sy - 2
        w_yon = 1 if yon >= 0 else -1

        if m == "ilkbahar":
            pygame.draw.rect(game.ekran, (60, 80, 60), (w_x, w_y - 3, 30 * w_yon, 6))
            pygame.draw.rect(game.ekran, (80, 110, 80), (w_x, w_y - 3, 30 * w_yon, 6), 1)
            pygame.draw.rect(game.ekran, (100, 140, 100), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
            pygame.draw.circle(game.ekran, (255, 220, 180), (w_x + 31 * w_yon, w_y), 4)
            pygame.draw.circle(game.ekran, (255, 200, 50), (w_x + 31 * w_yon, w_y), 2)
            pygame.draw.rect(game.ekran, (50, 70, 50), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
            pygame.draw.rect(game.ekran, (70, 90, 70), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
            mag_x = w_x + 2 * w_yon
            pygame.draw.polygon(game.ekran, (70, 50, 30), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
            pygame.draw.polygon(game.ekran, (90, 70, 50), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
            pygame.draw.polygon(game.ekran, (50, 80, 50), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
            pygame.draw.rect(game.ekran, (50, 70, 40), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
            pygame.draw.rect(game.ekran, (70, 90, 60), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
            for ci in range(3):
                cx2 = w_x + (ci * 10 - 5) * w_yon
                cy2 = w_y - 6 + ci * 6
                pygame.draw.circle(game.ekran, (255, 220, 200), (int(cx2), int(cy2)), 3)
                pygame.draw.circle(game.ekran, (255, 200, 50), (int(cx2), int(cy2)), 1)
            for vi in range(4):
                vx2 = w_x + vi * 7 * w_yon
                pygame.draw.line(game.ekran, (60, 140, 60), (int(vx2), w_y - 4), (int(vx2 - 2 * w_yon), w_y + 6 + vi * 2), 1)
        elif m == "yaz":
            pygame.draw.rect(game.ekran, (200, 140, 20), (w_x, w_y - 4, 30 * w_yon, 8))
            pygame.draw.rect(game.ekran, (255, 200, 50), (w_x, w_y - 4, 30 * w_yon, 8), 1)
            pygame.draw.line(game.ekran, (255, 255, 100), (w_x, w_y), (w_x + 28 * w_yon, w_y), 2)
            pygame.draw.rect(game.ekran, (255, 180, 50), (w_x + 26 * w_yon, w_y - 5, 8 * w_yon, 10))
            pygame.draw.circle(game.ekran, (255, 255, 200), (w_x + 32 * w_yon, w_y), 5)
            pygame.draw.circle(game.ekran, (255, 255, 255), (w_x + 32 * w_yon, w_y), 2)
            pygame.draw.rect(game.ekran, (180, 120, 30), (w_x - 4 * w_yon, w_y - 6, 14 * w_yon, 12))
            pygame.draw.rect(game.ekran, (220, 160, 40), (w_x - 4 * w_yon, w_y - 6, 14 * w_yon, 12), 1)
            mag_x = w_x + 3 * w_yon
            pygame.draw.polygon(game.ekran, (160, 100, 20), [(mag_x, w_y + 6), (mag_x + 6 * w_yon, w_y + 6), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
            pygame.draw.polygon(game.ekran, (200, 140, 40), [(mag_x, w_y + 6), (mag_x + 6 * w_yon, w_y + 6), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
            pygame.draw.polygon(game.ekran, (140, 80, 20), [(w_x + 6 * w_yon, w_y + 6), (w_x + 10 * w_yon, w_y + 6), (w_x + 8 * w_yon, w_y + 16)])
            pygame.draw.rect(game.ekran, (130, 80, 20), (w_x - 10 * w_yon, w_y - 6, 8 * w_yon, 12))
            pygame.draw.rect(game.ekran, (170, 110, 30), (w_x - 10 * w_yon, w_y - 6, 8 * w_yon, 12), 1)
            for ri in range(5):
                rx2 = w_x + ri * 6 * w_yon
                pygame.draw.line(game.ekran, (255, 220, 50), (int(rx2), w_y - 8), (int(rx2), w_y - 12 - ri % 2 * 3), 1)
                pygame.draw.line(game.ekran, (255, 220, 50), (int(rx2), w_y + 8), (int(rx2), w_y + 12 + ri % 2 * 3), 1)
        elif m == "sonbahar":
            pygame.draw.rect(game.ekran, (100, 60, 30), (w_x, w_y - 3, 30 * w_yon, 6))
            pygame.draw.rect(game.ekran, (130, 80, 40), (w_x, w_y - 3, 30 * w_yon, 6), 1)
            pygame.draw.rect(game.ekran, (80, 50, 20), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
            pygame.draw.polygon(game.ekran, (200, 80, 30), [(w_x + 30 * w_yon, w_y), (w_x + 28 * w_yon, w_y - 5), (w_x + 28 * w_yon, w_y + 5)])
            pygame.draw.rect(game.ekran, (80, 50, 30), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
            pygame.draw.rect(game.ekran, (110, 70, 40), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
            mag_x = w_x + 2 * w_yon
            pygame.draw.polygon(game.ekran, (120, 60, 20), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
            pygame.draw.polygon(game.ekran, (150, 80, 30), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
            pygame.draw.polygon(game.ekran, (80, 40, 20), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
            pygame.draw.rect(game.ekran, (70, 40, 20), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
            pygame.draw.rect(game.ekran, (100, 60, 30), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
            for li in range(4):
                lx2 = w_x + li * 7 * w_yon
                ly2 = w_y - 5 + li * 3
                pygame.draw.ellipse(game.ekran, (200, 100, 30), (int(lx2), int(ly2), 5 * w_yon, 3))
                pygame.draw.ellipse(game.ekran, (255, 150, 50), (int(lx2 + 1), int(ly2 + 1), 3 * w_yon, 1))
            for bi in range(3):
                bx2 = w_x + bi * 8 * w_yon
                pygame.draw.line(game.ekran, (60, 40, 20), (int(bx2), w_y - 4), (int(bx2 + 2 * w_yon), w_y - 10 + bi * 2), 1)
        elif m == "kis":
            pygame.draw.rect(game.ekran, (150, 200, 230), (w_x, w_y - 3, 30 * w_yon, 6))
            pygame.draw.rect(game.ekran, (200, 230, 255), (w_x, w_y - 3, 30 * w_yon, 6), 1)
            pygame.draw.rect(game.ekran, (180, 220, 240), (w_x + 28 * w_yon, w_y - 4, 6 * w_yon, 8))
            pygame.draw.circle(game.ekran, (200, 240, 255), (w_x + 31 * w_yon, w_y), 4)
            pygame.draw.circle(game.ekran, (255, 255, 255), (w_x + 31 * w_yon, w_y), 2)
            pygame.draw.rect(game.ekran, (130, 180, 210), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10))
            pygame.draw.rect(game.ekran, (170, 210, 235), (w_x - 4 * w_yon, w_y - 5, 12 * w_yon, 10), 1)
            mag_x = w_x + 2 * w_yon
            pygame.draw.polygon(game.ekran, (140, 190, 220), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)])
            pygame.draw.polygon(game.ekran, (180, 220, 245), [(mag_x, w_y + 5), (mag_x + 6 * w_yon, w_y + 5), (mag_x + 10 * w_yon, w_y + 18), (mag_x + 2 * w_yon, w_y + 18)], 1)
            pygame.draw.polygon(game.ekran, (120, 170, 200), [(w_x + 6 * w_yon, w_y + 5), (w_x + 10 * w_yon, w_y + 5), (w_x + 8 * w_yon, w_y + 16)])
            pygame.draw.rect(game.ekran, (110, 160, 190), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10))
            pygame.draw.rect(game.ekran, (150, 200, 230), (w_x - 10 * w_yon, w_y - 5, 8 * w_yon, 10), 1)
            for si in range(4):
                sx2 = w_x + (si * 7 + 2) * w_yon
                sy2 = w_y - 6 + si * 4
                pygame.draw.line(game.ekran, (220, 240, 255), (int(sx2 - 3), int(sy2)), (int(sx2 + 3), int(sy2)), 1)
                pygame.draw.line(game.ekran, (220, 240, 255), (int(sx2), int(sy2 - 3)), (int(sx2), int(sy2 + 3)), 1)
            for bi in range(3):
                bxi = w_x + bi * 9 * w_yon
                byi = w_y + 10 + bi * 3
                pygame.draw.circle(game.ekran, (200, 235, 255), (int(bxi), int(byi)), 2)
                pygame.draw.circle(game.ekran, (255, 255, 255), (int(bxi), int(byi)), 1)

        wd_cd = assets.WP_DATA[game.mv]["cd"]
        if game.shoot_cd > wd_cd - 3:
            flash_r = assets.WP_DATA[game.mv]["r"] if m != "kis" else (200, 230, 255)
            pygame.draw.circle(game.ekran, flash_r, (w_x + 32 * w_yon, w_y), 6)
            pygame.draw.circle(game.ekran, (255, 255, 255), (w_x + 32 * w_yon, w_y), 3)
    else:
        pygame.draw.line(game.ekran, (240, 235, 225), (sx - 15, sy - 8), (sx - 22 + kol_sag, sy + 6), 5)
        pygame.draw.line(game.ekran, (240, 235, 225), (sx + 15, sy - 8), (sx + 22 - kol_sag, sy + 6), 5)
        pygame.draw.line(game.ekran, (225, 220, 210), (sx - 15, sy - 7), (sx - 21 + kol_sag, sy + 7), 1)
        pygame.draw.line(game.ekran, (225, 220, 210), (sx + 15, sy - 7), (sx + 21 - kol_sag, sy + 7), 1)
        pygame.draw.line(game.ekran, (220, 215, 205), (sx - 21 + kol_sag, sy + 4), (sx - 21 + kol_sag, sy + 8), 2)
        pygame.draw.line(game.ekran, (220, 215, 205), (sx + 21 - kol_sag, sy + 4), (sx + 21 - kol_sag, sy + 8), 2)

    # === WIZARD SPRITE ===
    _yukle_char()

    if CHAR:
        sprite = CHAR
        if yon < 0:
            sprite = pygame.transform.flip(CHAR, True, False)
        game.ekran.blit(sprite, (sx - sprite.get_width()//2, sy + 25 - sprite.get_height()))

    if abs(game.hx) < 0.5 and game.yr:
        if random.random() < 0.04:
            px = sx + random.randint(-18, 18)
            py = sy + 10 + random.randint(-20, 5)
            renk = random.choice([(100, 150, 255), (150, 200, 255), (200, 230, 255)])
            particles.ptk_ekle(px, py, renk, 1)

    if game.yr and abs(game.hx) > 1.5:
        if random.random() < 0.12:
            particles.ptk_ekle(sx + random.randint(-6, 6), sy + 22, (180, 180, 200), 2)

    if not _onceki_yr and game.yr:
        for _ in range(5):
            particles.ptk_ekle(sx + random.randint(-10, 10), sy + 22, (180, 200, 255), 2)
        particles.ptk_patlatma(sx, sy + 22, (180, 200, 255), 6, 3)

    if not game.yr and random.random() < 0.06:
        particles.ptk_ekle(sx + random.randint(-8, 8), sy + random.randint(-5, 15), (150, 200, 255), 1)

    _onceki_oy = game.oy
    _onceki_yr = game.yr

    # MEVSIM KOSTUMLERI
    if game.aktif_k == "sonbahar":
        pygame.draw.polygon(game.ekran, assets.YP, [(sx - 16, sy - 6), (sx - 22, sy + 20), (sx - 8, sy + 18)])
        pygame.draw.polygon(game.ekran, assets.YP, [(sx + 16, sy - 6), (sx + 22, sy + 20), (sx + 8, sy + 18)])
        pygame.draw.line(game.ekran, (150, 80, 20), (sx - 15, sy - 4), (sx - 15, sy + 14), 1)
        pygame.draw.line(game.ekran, (150, 80, 20), (sx + 15, sy - 4), (sx + 15, sy + 14), 1)
    if game.aktif_k == "ilkbahar":
        for i in range(5):
            a = sx - 12 + i * 6
            pygame.draw.circle(game.ekran, assets.C1, (a, sy - 54), 5)
            pygame.draw.circle(game.ekran, assets.C2, (a, sy - 54), 3)
            pygame.draw.circle(game.ekran, (255, 200, 50), (a, sy - 54), 1)
    if game.aktif_k == "kis":
        for i in range(5):
            a = sx - 12 + i * 6
            pygame.draw.circle(game.ekran, assets.KR, (a, sy - 56), 6)
            pygame.draw.circle(game.ekran, assets.B, (a, sy - 56), 4)
            pygame.draw.circle(game.ekran, (200, 230, 255), (a - 1, sy - 57), 2)
    if game.aktif_k == "yaz":
        pygame.draw.circle(game.ekran, assets.ALTIN, (sx - 9, sy - 36), 8, 2)
        pygame.draw.circle(game.ekran, assets.ALTIN, (sx + 9, sy - 36), 8, 2)
        pygame.draw.line(game.ekran, assets.ALTIN, (sx - 1, sy - 36), (sx + 1, sy - 36), 2)
        for i in range(6):
            a = i * 60
            pygame.draw.line(game.ekran, assets.ALTIN, (sx + int(math.cos(a)*9), sy - 36 + int(math.sin(a)*9)), (sx + int(math.cos(a)*14), sy - 36 + int(math.sin(a)*14)), 1)
