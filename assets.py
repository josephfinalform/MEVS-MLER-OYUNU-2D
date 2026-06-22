"""Asset constants: colors, biome data, weapon stats, difficulty tables."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final, TypedDict


# ── Color constants ──────────────────────────────────────────────
B: Final = (255, 255, 255)
S: Final = (0, 0, 0)
TEN: Final = (255, 210, 180)
PEMBE: Final = (255, 20, 147)
NP: Final = (255, 50, 180)
MB: Final = (0, 180, 255)
NM: Final = (0, 255, 255)
SAC: Final = (255, 100, 200)
SG: Final = (200, 50, 150)
GB: Final = (240, 240, 255)
GM: Final = (80, 200, 255)
GI: Final = (255, 255, 255)
AG: Final = (200, 80, 80)
ALTIN: Final = (255, 215, 0)
K: Final = (200, 50, 50)
NY: Final = (0, 255, 100)
GT: Final = (40, 40, 50)
AGT: Final = (60, 60, 75)
C1: Final = (255, 100, 200)
C2: Final = (255, 255, 100)
DT: Final = (220, 180, 150)
DS: Final = (180, 100, 50)
DG: Final = (255, 200, 100)
MM: Final = (50, 100, 200)
YP: Final = (200, 150, 50)
KR: Final = (220, 230, 255)


# ── Enums ─────────────────────────────────────────────────────────
class Season(str, Enum):
    ILKBAHAR = "ilkbahar"
    YAZ = "yaz"
    SONBAHAR = "sonbahar"
    KIS = "kis"


class Difficulty(str, Enum):
    KOLAY = "kolay"
    ORTA = "orta"
    ZOR = "zor"
    IMKANSIZ = "imkansiz"


class Screen(str, Enum):
    MENU = "menu"
    SEASON_SELECT = "season_select"
    OYUN = "oyun"
    SETTINGS = "settings"
    ENVANTER = "envanter"
    LEADERBOARD = "leaderboard"
    LABEL = "lbl"
    OLDEN = "olden"


# ── Season order ─────────────────────────────────────────────────
MEVSIM_SIRASI: Final[list[str]] = ["ilkbahar", "yaz", "sonbahar", "kis"]
ms: Final[list[str]] = MEVSIM_SIRASI
MS: Final[list[str]] = MEVSIM_SIRASI


# ── Season color palettes ────────────────────────────────────────
class SeasonColors(TypedDict):
    a: tuple[int, int, int]
    z: tuple[int, int, int]
    p: tuple[int, int, int]
    k: tuple[int, int, int]
    t: tuple[int, int, int]
    ac: tuple[int, int, int]


MEV: dict[str, SeasonColors] = {
    Season.ILKBAHAR.value: {"a": (30, 60, 40), "z": (60, 180, 60), "p": (80, 200, 80), "k": (120, 255, 120), "t": (255, 100, 100), "ac": (40, 80, 50)},
    Season.YAZ.value:     {"a": (50, 70, 60), "z": (200, 180, 60), "p": (220, 200, 80), "k": (255, 230, 120), "t": (255, 80, 50), "ac": (70, 60, 35)},
    Season.SONBAHAR.value: {"a": (50, 30, 30), "z": (180, 100, 40), "p": (200, 120, 50), "k": (255, 160, 80), "t": (200, 50, 50), "ac": (60, 35, 35)},
    Season.KIS.value:     {"a": (30, 40, 60), "z": (180, 200, 220), "p": (180, 200, 220), "k": (220, 240, 255), "t": (100, 150, 200), "ac": (40, 50, 70)},
}


# ── Biome environment colors ─────────────────────────────────────
class BiomeColors(TypedDict):
    sky: tuple[int, int, int]
    sun: tuple[int, int, int]
    grass: tuple[int, int, int]
    soil: tuple[int, int, int]
    deep_soil: tuple[int, int, int]
    stone: tuple[int, int, int]
    tree_trunk: tuple[int, int, int]
    tree_leaf: tuple[int, int, int]
    bg_tree1: tuple[int, int, int]
    bg_tree2: tuple[int, int, int]
    bg_tree3: tuple[int, int, int]


BIOME: dict[str, BiomeColors] = {
    Season.ILKBAHAR.value: {
        "sky": (135, 206, 235), "sun": (255, 255, 200),
        "grass": (80, 200, 60), "soil": (140, 100, 60), "deep_soil": (100, 70, 40),
        "stone": (130, 130, 130), "tree_trunk": (100, 70, 40), "tree_leaf": (60, 180, 50),
        "bg_tree1": (50, 140, 40), "bg_tree2": (40, 120, 35), "bg_tree3": (30, 100, 30),
    },
    Season.YAZ.value: {
        "sky": (100, 180, 255), "sun": (255, 230, 100),
        "grass": (160, 180, 50), "soil": (180, 140, 70), "deep_soil": (140, 100, 50),
        "stone": (160, 150, 120), "tree_trunk": (120, 80, 40), "tree_leaf": (140, 170, 40),
        "bg_tree1": (100, 140, 30), "bg_tree2": (80, 120, 25), "bg_tree3": (60, 100, 20),
    },
    Season.SONBAHAR.value: {
        "sky": (180, 160, 200), "sun": (255, 200, 150),
        "grass": (160, 120, 50), "soil": (130, 80, 40), "deep_soil": (90, 60, 30),
        "stone": (110, 100, 90), "tree_trunk": (80, 50, 25), "tree_leaf": (200, 100, 30),
        "bg_tree1": (150, 80, 20), "bg_tree2": (120, 60, 15), "bg_tree3": (100, 50, 10),
    },
    Season.KIS.value: {
        "sky": (200, 210, 230), "sun": (220, 220, 240),
        "grass": (200, 210, 220), "soil": (140, 130, 140), "deep_soil": (100, 90, 100),
        "stone": (150, 155, 160), "tree_trunk": (80, 75, 70), "tree_leaf": (180, 190, 200),
        "bg_tree1": (150, 160, 170), "bg_tree2": (130, 140, 150), "bg_tree3": (110, 120, 130),
    },
}


# ── Costume definitions ──────────────────────────────────────────
@dataclass
class Costume:
    name: str
    color: tuple[int, int, int]
    description: str


KOSTUMLER: dict[str, Costume] = {
    Season.ILKBAHAR.value: Costume("Cicek Taci", C1, "Bahar ciceklerinden tac"),
    Season.YAZ.value:     Costume("Gunes Gozlugu", ALTIN, "Havali gunes gozlugu"),
    Season.SONBAHAR.value: Costume("Yaprak Pelerin", YP, "Sonbahar yapragindan pelerin"),
    Season.KIS.value:     Costume("Kar Taci", KR, "Kar tanelerinden tac"),
}


# ── Difficulty tables ────────────────────────────────────────────
CAN: Final[dict[str, int]] = {"kolay": 14, "orta": 10, "zor": 6, "imkansiz": 4}
ZORLUK_CAN: Final = CAN

HASAR_CARPI: Final[dict[str, float]] = {"kolay": 0.5, "orta": 1.0, "zor": 1.5, "imkansiz": 2.0}
ZORLUK_HASAR: Final = HASAR_CARPI

GRAVITE: Final[dict[str, float]] = {"kolay": 0.45, "orta": 0.5, "zor": 0.6, "imkansiz": 0.7}
ZORLUK_GRAVITE: Final = GRAVITE

ZIPLAMA: Final[dict[str, float]] = {"kolay": -13, "orta": -13, "zor": -12, "imkansiz": -11}
ZORLUK_ZIPLAMA: Final = ZIPLAMA


# ── Boss difficulty ──────────────────────────────────────────────
BOSS_HP: Final[dict[str, int]] = {"kolay": 8, "orta": 12, "zor": 18, "imkansiz": 25}
BOSS_SPD: Final[dict[str, float]] = {"kolay": 1.5, "orta": 2.5, "zor": 3.5, "imkansiz": 4.5}
BOSS_ATK_CD: Final[dict[str, int]] = {"kolay": 90, "orta": 60, "zor": 40, "imkansiz": 25}
BOSS_SKIN: Final[dict[str, int]] = {"kolay": 0, "orta": 1, "zor": 2, "imkansiz": 3}
BOSS_GLOW: Final[dict[str, tuple[int, int, int]]] = {
    "kolay": (100, 100, 100), "orta": (200, 200, 50),
    "zor": (255, 50, 50), "imkansiz": (255, 0, 100),
}

# Backward-compatible aliases
z_can: Final = CAN
z_dh: Final = HASAR_CARPI
z_yc: Final = GRAVITE
z_zg: Final = ZIPLAMA


# ── Weapon data ──────────────────────────────────────────────────
@dataclass
class WeaponData:
    name: str
    color: tuple[int, int, int]
    damage: int
    speed: int
    ammo: int
    cooldown: int
    shape: str


WP_DATA: dict[str, WeaponData] = {
    Season.ILKBAHAR.value: WeaponData("Cicek Kalasnikof", C1, 1, 10, 25, 7, "cicek"),
    Season.YAZ.value:     WeaponData("Gunes Tufegi", ALTIN, 2, 10, 25, 7, "cizgi"),
    Season.SONBAHAR.value: WeaponData("Yaprak Firlatan", YP, 2, 8, 25, 7, "yaprak"),
    Season.KIS.value:     WeaponData("Kar Topu", KR, 3, 7, 25, 7, "kar"),
}


# ── Season dimensions (backward compat) ──────────────────────────
GENISLIK: Final[int] = 1200
YUKSEKLIK: Final[int] = 700
