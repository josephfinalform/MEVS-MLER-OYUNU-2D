"""JSON-based save/load system for game progress."""

from __future__ import annotations

import json
import os
from typing import Any

import game

DOSYA: str = "save.json"

# Type alias for the save data dict
SaveData = dict[str, Any]


def _read_save() -> SaveData | None:
    """Read save file contents, return None if missing."""
    if not os.path.exists(DOSYA):
        return None
    with open(DOSYA) as f:
        return json.load(f)


def _write_save(data: SaveData) -> None:
    """Write save data to file."""
    with open(DOSYA, "w") as f:
        json.dump(data, f, indent=2)


def kaydet() -> None:
    """Persist current game state to save.json."""
    import audio
    game.ses_pos = audio.muzik_pozisyon()
    data: SaveData = {
        "si": game.si,
        "mv": game.mv,
        "rnd": game.rnd,
        "puan": game.puan,
        "envanter": game.envanter,
        "aktif_k": game.aktif_k,
        "yuksek_puan": game.yuksek_puan,
        "ayar": game.ayar,
        "ses_pos": game.ses_pos,
    }
    _write_save(data)


def yukle() -> bool:
    """Restore game state from save.json. Returns True if loaded."""
    data = _read_save()
    if data is None:
        return False

    game.si = data.get("si", 0)
    game.mv = data.get("mv", game.mv)
    game.rnd = data.get("rnd", 1)
    game.puan = data.get("puan", 0)
    game.envanter = data.get("envanter", [])
    game.aktif_k = data.get("aktif_k", None)
    game.yuksek_puan = data.get("yuksek_puan", {})
    game.ayar.update(data.get("ayar", {}))
    game.ses_pos = data.get("ses_pos", 0.0)
    return True


def var_mi() -> bool:
    """Check if a save file exists."""
    return os.path.exists(DOSYA)


def sil() -> None:
    """Delete the save file."""
    if os.path.exists(DOSYA):
        os.remove(DOSYA)
