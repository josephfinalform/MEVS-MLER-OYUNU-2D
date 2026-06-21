import json
import os
import game

DOSYA = "save.json"


def kaydet():
    import audio
    game.ses_pos = audio.muzik_pozisyon()
    data = {
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
    with open(DOSYA, "w") as f:
        json.dump(data, f, indent=2)


def yukle():
    if not os.path.exists(DOSYA):
        return False
    with open(DOSYA) as f:
        data = json.load(f)
    game.si = data.get("si", 0)
    game.mv = data.get("mv", game.mv)
    game.rnd = data.get("rnd", 1)
    game.puan = data.get("puan", 0)
    game.envanter = data.get("envanter", [])
    game.aktif_k = data.get("aktif_k", None)
    game.yuksek_puan = data.get("yuksek_puan", {})
    game.ayar.update(data.get("ayar", {}))
    game.ses_pos = data.get("ses_pos", 0)
    return True


def var_mi():
    return os.path.exists(DOSYA)


def sil():
    if os.path.exists(DOSYA):
        os.remove(DOSYA)
