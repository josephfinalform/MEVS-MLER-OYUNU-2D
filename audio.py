import math
import random
import os

def _ses_hazir():
    import pygame
    try:
        pygame.mixer.get_init()
        return True
    except:
        return False

def ses_yap(f, s, v=0.08, tip="sin"):
    import pygame
    sr = 22050
    n = int(sr * s)
    buf = bytearray(n * 2)
    for i in range(n):
        t = i / sr
        if tip == "sin":
            val = math.sin(2 * math.pi * f * t)
        elif tip == "kare":
            val = 1.0 if math.sin(2 * math.pi * f * t) > 0 else -1.0
        elif tip == "gurultu":
            val = math.sin(2 * math.pi * f * t) * random.random()
        else:
            val = math.sin(2 * math.pi * f * t)
        val = int(v * 32767 * val)
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))

muzik_caliniyor = False

def _dosya_parca(parca):
    taban = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(taban, "music", f"{parca}.mp3")
    if os.path.exists(path):
        return path
    return None

def muzik_oynat(parca, loop=-1, basla=0.0, fade_ms=500):
    global muzik_caliniyor
    import pygame
    import game
    path = _dosya_parca(parca)
    if path is None:
        return
    try:
        pygame.mixer.music.load(path)
        ses = game.ayar["lobi_ses" if parca == "menu" else "ses"] / 100
        pygame.mixer.music.set_volume(ses)
        pygame.mixer.music.play(loop, basla, fade_ms)
        game.ses_mv = parca
        muzik_caliniyor = True
    except:
        pass

def muzik_durdur(fade_ms=0):
    global muzik_caliniyor
    import pygame
    try:
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
    except:
        pass
    muzik_caliniyor = False

def muzik_ses(volume):
    import pygame
    try:
        pygame.mixer.music.set_volume(volume)
    except:
        pass

def muzik_pozisyon():
    import pygame
    try:
        return pygame.mixer.music.get_pos() / 1000.0
    except:
        return 0.0

def menu_muzik():
    global muzik_caliniyor
    import game
    if getattr(game, 'ses_mv', None) == "menu" and muzik_caliniyor:
        return
    muzik_oynat("menu", fade_ms=300)

def sezon_muzik(m):
    global muzik_caliniyor
    import game
    path = _dosya_parca(m)
    if path is None:
        return
    if getattr(game, 'ses_mv', None) == m and muzik_caliniyor:
        muzik_ses(game.ayar["ses"] / 100)
        return
    eski = getattr(game, 'ses_pos', 0)
    muzik_oynat(m, basla=eski, fade_ms=500)

ses_kanal = None
ses_kanal2 = None

def _kanal_hazirla():
    global ses_kanal, ses_kanal2
    if ses_kanal is None:
        import pygame
        try:
            ses_kanal = pygame.mixer.Channel(1)
            ses_kanal2 = pygame.mixer.Channel(2)
        except:
            pass

def sfx_ziplama():
    _kanal_hazirla()
    if ses_kanal: ses_kanal.play(ses_yap(300, 0.1, 0.06))

def sfx_cift_ziplama():
    _kanal_hazirla()
    if ses_kanal: ses_kanal.play(ses_yap(500, 0.08, 0.05))

def sfx_ates():
    _kanal_hazirla()
    if ses_kanal2: ses_kanal2.play(ses_yap(800, 0.05, 0.04))

def sfx_topla():
    _kanal_hazirla()
    if ses_kanal: ses_kanal.play(ses_yap(1200, 0.08, 0.05))

def sfx_hasar():
    _kanal_hazirla()
    import pygame
    buf = bytearray(int(22050 * 0.15) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.07 * 32767 * math.sin(2 * math.pi * 100 * t) * (1 - i/(len(buf)//2)))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    if ses_kanal: ses_kanal.play(s)

def sfx_checkpoint():
    _kanal_hazirla()
    import pygame
    buf = bytearray(int(22050 * 0.3) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.05 * 32767 * (math.sin(2 * math.pi * (400 + t*1500) * t) + math.sin(2 * math.pi * (600 + t*2000) * t)) * 0.5)
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    if ses_kanal: ses_kanal.play(s)

def sfx_powerup():
    _kanal_hazirla()
    import pygame
    buf = bytearray(int(22050 * 0.3) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.05 * 32767 * (math.sin(2 * math.pi * (600 + t*2000) * t) + math.sin(2 * math.pi * (900 + t*2500) * t)) * 0.5)
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    if ses_kanal: ses_kanal.play(s)

def sfx_boss_hit():
    _kanal_hazirla()
    import pygame
    buf = bytearray(int(22050 * 0.2) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.06 * 32767 * math.sin(2 * math.pi * 80 * t) * (1 - t/0.2) * (0.5 + 0.5*math.sin(2*math.pi*30*t)))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    if ses_kanal2: ses_kanal2.play(s)

def sfx_boss_ol():
    _kanal_hazirla()
    import pygame
    buf = bytearray(int(22050 * 0.8) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.06 * 32767 * math.sin(2 * math.pi * (200 - t*150) * t) * (1 - t/0.8))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    if ses_kanal: ses_kanal.play(s)

def sfx_boss_ates():
    _kanal_hazirla()
    if ses_kanal2: ses_kanal2.play(ses_yap(150, 0.1, 0.05, "kare"))

def sfx_ses_ayarla():
    global ses_kanal, ses_kanal2
    import game
    import pygame
    _kanal_hazirla()
    v = game.ayar["ses"] / 100 if game.ses_acik else 0
    if ses_kanal:
        try: ses_kanal.set_volume(v)
        except: pass
    if ses_kanal2:
        try: ses_kanal2.set_volume(v)
        except: pass
    try:
        mv = game.ayar["lobi_ses" if game.ses_mv == "menu" else "ses"] / 100
        pygame.mixer.music.set_volume(mv if game.ses_acik else 0)
    except:
        pass
