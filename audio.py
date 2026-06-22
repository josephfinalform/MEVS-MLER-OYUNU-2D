"""Procedural sound generation and music playback."""

from __future__ import annotations

import math
import os
import random
from typing import Callable, Optional

import pygame

import config

_muzik_caliniyor: bool = False
_ses_kanal: Optional[pygame.mixer.Channel] = None
_ses_kanal2: Optional[pygame.mixer.Channel] = None


def _ses_hazir() -> bool:
    """Check if pygame mixer is initialized."""
    try:
        return pygame.mixer.get_init() is not None
    except Exception:
        return False


def ses_yap(
    freq: float,
    sure: float,
    vol: float = 0.08,
    tip: str = "sin",
) -> pygame.mixer.Sound:
    """Generate a procedural sound effect waveform."""
    sr = 22050
    n = int(sr * sure)
    buf = bytearray(n * 2)
    for i in range(n):
        t = i / sr
        if tip == "sin":
            val = math.sin(2 * math.pi * freq * t)
        elif tip == "kare":
            val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        elif tip == "gurultu":
            val = math.sin(2 * math.pi * freq * t) * random.random()
        else:
            val = math.sin(2 * math.pi * freq * t)
        val = int(vol * 32767 * val)
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


def _ses_buf(
    sure: float,
    vol: float,
    freq_func: Callable[[float], float],
    tip_func: Callable[[float, float], float] | None = None,
) -> pygame.mixer.Sound:
    """Generate a sound from a per-sample frequency/envelope function.

    Args:
        sure: Duration in seconds.
        vol: Base volume (0.0-1.0).
        freq_func: Callable(t) returning frequency at time t.
        tip_func: Callable(t, freq) returning sample value (-1..1). Defaults to sine.
    """
    sr = 22050
    n = int(sr * sure)
    buf = bytearray(n * 2)
    for i in range(n):
        t = i / sr
        f = freq_func(t)
        if tip_func:
            val = tip_func(t, f)
        else:
            val = math.sin(2 * math.pi * f * t)
        val = int(vol * 32767 * val)
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


def _dosya_parca(parca: str) -> str | None:
    """Resolve path to a music track file."""
    path = os.path.join(str(config.KAYNAK), "music", f"{parca}.mp3")
    return path if os.path.exists(path) else None


def muzik_oynat(parca: str, loop: int = -1, basla: float = 0.0, fade_ms: int = 500) -> None:
    """Start playing background music."""
    global _muzik_caliniyor
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
        _muzik_caliniyor = True
    except Exception:
        pass


def muzik_durdur(fade_ms: int = 0) -> None:
    """Stop background music."""
    global _muzik_caliniyor
    try:
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
    except Exception:
        pass
    _muzik_caliniyor = False


def muzik_ses(volume: float) -> None:
    """Set music volume (0.0 - 1.0)."""
    try:
        pygame.mixer.music.set_volume(volume)
    except Exception:
        pass


def muzik_pozisyon() -> float:
    """Get current music playback position in seconds."""
    try:
        return pygame.mixer.music.get_pos() / 1000.0
    except Exception:
        return 0.0


def menu_muzik() -> None:
    """Start/ensure menu music is playing."""
    global _muzik_caliniyor
    import game
    if getattr(game, "ses_mv", None) == "menu" and _muzik_caliniyor:
        return
    muzik_oynat("menu", fade_ms=300)


def sezon_muzik(m: str) -> None:
    """Start/ensure season-appropriate music is playing."""
    global _muzik_caliniyor
    import game
    path = _dosya_parca(m)
    if path is None:
        return
    if getattr(game, "ses_mv", None) == m and _muzik_caliniyor:
        muzik_ses(game.ayar["ses"] / 100)
        return
    eski = getattr(game, "ses_pos", 0.0)
    muzik_oynat(m, basla=eski, fade_ms=500)


def _kanal_hazirla() -> None:
    """Lazy-init sound effect channels."""
    global _ses_kanal, _ses_kanal2
    if _ses_kanal is not None:
        return
    try:
        _ses_kanal = pygame.mixer.Channel(1)
        _ses_kanal2 = pygame.mixer.Channel(2)
    except Exception:
        pass


def sfx_ziplama() -> None:
    """Play jump sound."""
    _kanal_hazirla()
    if _ses_kanal:
        _ses_kanal.play(ses_yap(300, 0.1, 0.06))


def sfx_cift_ziplama() -> None:
    """Play double-jump sound."""
    _kanal_hazirla()
    if _ses_kanal:
        _ses_kanal.play(ses_yap(500, 0.08, 0.05))


def sfx_ates() -> None:
    """Play weapon fire sound."""
    _kanal_hazirla()
    if _ses_kanal2:
        _ses_kanal2.play(ses_yap(800, 0.05, 0.04))


def sfx_topla() -> None:
    """Play collectible pickup sound."""
    _kanal_hazirla()
    if _ses_kanal:
        _ses_kanal.play(ses_yap(1200, 0.08, 0.05))


def sfx_hasar() -> None:
    """Play damage sound (decaying sine wave at 100 Hz)."""
    _kanal_hazirla()
    s = _ses_buf(0.15, 0.07, lambda t: 100, lambda t, f: math.sin(2 * math.pi * f * t) * (1.0 - t / 0.15))
    if _ses_kanal:
        _ses_kanal.play(s)


def sfx_checkpoint() -> None:
    """Play checkpoint sound (rising dual-frequency)."""
    _kanal_hazirla()
    def _f(t: float) -> float:
        return (400 + t * 1500 + 600 + t * 2000) / 2
    def _env(t: float, f: float) -> float:
        return (math.sin(2 * math.pi * (400 + t * 1500) * t) + math.sin(2 * math.pi * (600 + t * 2000) * t)) * 0.5
    s = _ses_buf(0.3, 0.05, _f, _env)
    if _ses_kanal:
        _ses_kanal.play(s)


def sfx_powerup() -> None:
    """Play power-up sound (rising dual-frequency)."""
    _kanal_hazirla()
    def _f(t: float) -> float:
        return (600 + t * 2000 + 900 + t * 2500) / 2
    def _env(t: float, f: float) -> float:
        return (math.sin(2 * math.pi * (600 + t * 2000) * t) + math.sin(2 * math.pi * (900 + t * 2500) * t)) * 0.5
    s = _ses_buf(0.3, 0.05, _f, _env)
    if _ses_kanal:
        _ses_kanal.play(s)


def sfx_boss_hit() -> None:
    """Play boss hit sound (low rumble with amplitude modulation)."""
    _kanal_hazirla()
    def _env(t: float, f: float) -> float:
        env = 1.0 - t / 0.2
        return math.sin(2 * math.pi * 80 * t) * env * (0.5 + 0.5 * math.sin(2 * math.pi * 30 * t))
    s = _ses_buf(0.2, 0.06, lambda t: 80, _env)
    if _ses_kanal2:
        _ses_kanal2.play(s)


def sfx_boss_ol() -> None:
    """Play boss death sound (descending tone)."""
    _kanal_hazirla()
    def _env(t: float, f: float) -> float:
        return math.sin(2 * math.pi * f * t) * (1.0 - t / 0.8)
    s = _ses_buf(0.8, 0.06, lambda t: 200 - t * 150, _env)
    if _ses_kanal:
        _ses_kanal.play(s)


def sfx_boss_ates() -> None:
    """Play boss attack sound."""
    _kanal_hazirla()
    if _ses_kanal2:
        _ses_kanal2.play(ses_yap(150, 0.1, 0.05, "kare"))


def sfx_ses_ayarla() -> None:
    """Sync all volume levels with game settings."""
    global _ses_kanal, _ses_kanal2
    import game
    _kanal_hazirla()
    v = game.ayar["ses"] / 100 if game.ses_acik else 0
    if _ses_kanal:
        try:
            _ses_kanal.set_volume(v)
        except Exception:
            pass
    if _ses_kanal2:
        try:
            _ses_kanal2.set_volume(v)
        except Exception:
            pass
    try:
        mv_key = "lobi_ses" if game.ses_mv == "menu" else "ses"
        mv = game.ayar[mv_key] / 100
        pygame.mixer.music.set_volume(mv if game.ses_acik else 0)
    except Exception:
        pass
