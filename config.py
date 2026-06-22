"""Central configuration constants for the game."""

from pathlib import Path
from typing import Final

# Display
FPS: Final = 60
BASLIK: Final = "MEVSIMLER"

# File paths
KOK: Final = Path(__file__).parent
KAYNAK: Final = KOK / "resources"
IKONLAR: Final = KAYNAK / "icons"
MUZIK: Final = KAYNAK / "music"
KAYIT_DOSYASI: Final = "save.json"
ARKAPLAN: Final = {
    "ilkbahar": KAYNAK / "arka_ilkbahar.png",
    "yaz": KAYNAK / "arka_yaz.jpg",
    "sonbahar": KAYNAK / "arka_sonbahar.jpg",
    "kis": KAYNAK / "arka_kis.jpg",
}
KARAKTER_SHEET: Final = KAYNAK / "char.png"
TILE_SHEET: Final = KAYNAK / "Season_collection.png"

# Game mechanics
GRAVITY_BASE: Final = 0.5
JUMP_BASE: Final = -13
SPIKE_DAMAGE: Final = 1
BOSS_ROUND_INTERVAL: Final = 4
MAX_ROUNDS: Final = 16
WEATHER_PARTICLE_COUNT: Final = 30
BG_PAR_COUNT: Final = 40

# Player
BASE_HEALTH: Final = 5
BASE_AMMO: Final = 25
MAX_AMMO: Final = 100
SHOOT_COOLDOWN: Final = 7
FIREBALL_COOLDOWN: Final = 20
POWERUP_DURATION: Final = 600

# Weapon names
WP_NAMES: Final = {
    "ilkbahar": "Cicek Kalasnikof",
    "yaz": "Gunes Tufegi",
    "sonbahar": "Yaprak Firlatan",
    "kis": "Kar Topu",
}

# Boss names
BOSS_ADI: Final = {
    "ilkbahar": "CICEK CANAVARI",
    "yaz": "GUNES DEV",
    "sonbahar": "YAPRAK FIRTINASI",
    "kis": "KAR KRALI",
}


