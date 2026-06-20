import math
import pygame
import game

def ses_yap(f, s, v=0.08):
    sr = 22050
    n = int(sr * s)
    buf = bytearray(n * 2)
    for i in range(n):
        val = int(v * 32767 * math.sin(2 * math.pi * f * i / sr))
        buf[i*2] = val & 0xFF
        buf[i*2+1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))

SESLER = {}
for m, f in [("ilkbahar", 262), ("yaz", 330), ("sonbahar", 196), ("kis", 165)]:
    SESLER[m] = ses_yap(f, 2.0)

sk = pygame.mixer.Channel(0)
