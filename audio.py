import math
import random
import pygame
import game

def ses_yap(f, s, v=0.08, tip="sin"):
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

SESLER = {}
for m, f in [("ilkbahar", 262), ("yaz", 330), ("sonbahar", 196), ("kis", 165)]:
    SESLER[m] = ses_yap(f, 2.0)

sk = pygame.mixer.Channel(0)
ses_kanal = pygame.mixer.Channel(1)
ses_kanal2 = pygame.mixer.Channel(2)

def sfx_ziplama():
    s = ses_yap(300, 0.1, 0.06)
    ses_kanal.play(s)

def sfx_cift_ziplama():
    s = ses_yap(500, 0.08, 0.05)
    ses_kanal.play(s)

def sfx_ates():
    s = ses_yap(800, 0.05, 0.04)
    ses_kanal2.play(s)

def sfx_topla():
    s = ses_yap(1200, 0.08, 0.05)
    ses_kanal.play(s)

def sfx_hasar():
    buf = bytearray(int(22050 * 0.15) * 2)
    for i in range(len(buf)//2):
        val = int(0.07 * 32767 * math.sin(2 * math.pi * 100 * i / 22050) * (1 - i/(len(buf)//2)))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    ses_kanal.play(s)

def sfx_checkpoint():
    buf = bytearray(int(22050 * 0.3) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.05 * 32767 * (math.sin(2 * math.pi * (400 + t*1500) * t) + math.sin(2 * math.pi * (600 + t*2000) * t)) * 0.5)
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    ses_kanal.play(s)

def sfx_powerup():
    buf = bytearray(int(22050 * 0.3) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.05 * 32767 * (math.sin(2 * math.pi * (600 + t*2000) * t) + math.sin(2 * math.pi * (900 + t*2500) * t)) * 0.5)
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    ses_kanal.play(s)

def sfx_boss_hit():
    buf = bytearray(int(22050 * 0.2) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.06 * 32767 * math.sin(2 * math.pi * 80 * t) * (1 - t/0.2) * (0.5 + 0.5*math.sin(2*math.pi*30*t)))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    ses_kanal2.play(s)

def sfx_boss_ol():
    buf = bytearray(int(22050 * 0.8) * 2)
    for i in range(len(buf)//2):
        t = i / 22050
        val = int(0.06 * 32767 * math.sin(2 * math.pi * (200 - t*150) * t) * (1 - t/0.8))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    s = pygame.mixer.Sound(buffer=bytes(buf))
    ses_kanal.play(s)

def sfx_boss_ates():
    s = ses_yap(150, 0.1, 0.05, "kare")
    ses_kanal2.play(s)
