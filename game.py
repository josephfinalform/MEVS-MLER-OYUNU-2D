"""Global game state module.

All shared mutable state lives here as module-level variables.
Accessed via `import game; game.ox` throughout the project.
"""

from __future__ import annotations

from typing import Any, Optional

import pygame

from config import BASE_AMMO, MAX_AMMO

# ── Pygame resources ─────────────────────────────────────────────
ekran: Optional[pygame.Surface] = None
saat: Optional[pygame.time.Clock] = None
f: Optional[pygame.font.Font] = None
fb: Optional[pygame.font.Font] = None
fk: Optional[pygame.font.Font] = None
fm: Optional[pygame.font.Font] = None

# ── Screen state ─────────────────────────────────────────────────
drm: str = "menu"              # Current screen: menu, season_select, oyun, settings, envanter
onceki_drm: Optional[str] = None

# ── Season / round ───────────────────────────────────────────────
si: int = 0                    # Season index (0-3)
rnd: int = 1                   # Current round (1-16)
mv: Optional[str] = None       # Season key: ilkbahar/yaz/sonbahar/kis
rnk: Optional[dict[str, Any]] = None  # Season color palette
lvl: Optional[dict[str, Any]] = None  # Current level data
rnd_max: int = 16
boss_sv: bool = False

# ── Player position / physics ────────────────────────────────────
ox: float = 100.0              # Player world X
oy: float = 100.0              # Player world Y
hx: float = 0.0                # Horizontal velocity
hy: float = 0.0                # Vertical velocity
yr: bool = False               # On ground?
yn: int = 1                    # Facing direction (1=right, -1=left)

yc: float = 0.5                # Gravity strength
zg: float = -13.0              # Jump strength
dhc: float = 1.0               # Difficulty multiplier
mc: int = 5                    # Max health
cn: int = 5                    # Current health

# ── Game objects (lists) ─────────────────────────────────────────
plt: list[dict[str, Any]] = []         # Platforms
prl: list[dict[str, Any]] = []         # Prisms (collectibles)
tzl: list[dict[str, Any]] = []         # Spikes
dsm: list[dict[str, Any]] = []         # Enemies
mpl: list[dict[str, Any]] = []         # Moving platforms
ptk: list[dict[str, Any]] = []         # Particles
bullets: list[dict[str, Any]] = []     # Player bullets
fireballs: list[dict[str, Any]] = []   # Fireballs (AOE)
boss_btl: list[dict[str, Any]] = []    # Boss bullets
boss_muh: list[dict[str, Any]] = []    # Boss minions

# ── Checkpoint ───────────────────────────────────────────────────
cp_x: float = 100.0
cp_y: float = 100.0

# ── Weapon ───────────────────────────────────────────────────────
weapon: Optional[dict[str, Any]] = None
ammo: int = BASE_AMMO
max_ammo: int = MAX_AMMO
wp_lv: int = 1
shoot_cd: int = 0
fire_cd: int = 0

# ── Power-up timers (frames remaining) ────────────────────────────
hiz_t: int = 0
kalkan_t: int = 0
cift_zipla_t: int = 0
cift_zipla_kalan: int = 0
miknatis_t: int = 0
kalp_t: int = 0

# ── Boss state ───────────────────────────────────────────────────
boss_hp: float = 0
boss_max_hp: float = 0
boss_timer: int = 0
boss_ptrn: int = 0
boss_dir: int = 1
boss_vx: float = 2.0
boss_x: float = 0.0
boss_y: float = 0.0
boss_atk_cd: int = 0
boss_lazer_t: int = 0
boss_minyon_t: int = 0
boss_dalga_t: int = 0
boss_hedef_x: float = 0.0
boss_hedef_y: float = 0.0
boss_hareket_mod: int = 0
boss_ozel_yetenek_cd: int = 0
boss_ozel_efekt: list[dict[str, Any]] = []
boss_hedefle: bool = False
boss_yon_degis: int = 0

# ── Frame counters ───────────────────────────────────────────────
sh: int = 0        # Screen shake frames remaining
sz: float = 0.0    # Global animation time (increments by 0.05 per frame)
gk: int = 0        # Global frame counter

# ── Input flags ──────────────────────────────────────────────────
ft: bool = False   # Fire trigger
mk: bool = False   # Mouse/key toggle
te_mi: bool = False  # Fullscreen toggle

# ── Scores & collection ─────────────────────────────────────────
puan: int = 0
yuksek_puan: dict[str, int] = {}  # High scores per season
hava_efektleri: list[dict[str, Any]] = []
rnd_sayac: int = 0
rnd_bitti: bool = False

# ── Audio ────────────────────────────────────────────────────────
ses_acik: bool = True
ses_pos: float = 0.0
ses_mv: Optional[str] = None

# ── Settings ─────────────────────────────────────────────────────
ayar: dict[str, Any] = {
    "z": "orta",
    "te": False,
    "ses": 50,
    "lobi_ses": 50,
}

# ── Inventory / costumes ─────────────────────────────────────────
envanter: list[str] = []
aktif_k: Optional[str] = None
ikonlar: dict[str, Any] = {}
boss_zorluk: Optional[int] = None

# ── Texture atlas ────────────────────────────────────────────────
tex_sheet: Optional[pygame.Surface] = None
TEXTURE_MAP: dict[str, dict[str, tuple[int, int]]] = {
    "ilkbahar": {"grass": (2, 38), "soil": (2, 40)},
    "yaz": {"grass": (5, 21), "soil": (4, 20)},
    "sonbahar": {"grass": (22, 17), "soil": (6, 16)},
    "kis": {"grass": (4, 55), "soil": (22, 55)},
}


def oyunu_sifirla() -> None:
    """Reset all gameplay state for a new game/season."""
    global ox, oy, hx, hy, yr, yn, cn, mc, ammo, wp_lv
    global shoot_cd, fire_cd, puan, ptk, plt, prl, tzl, dsm, mpl
    global bullets, fireballs, boss_btl, boss_muh, boss_hp
    global boss_timer, boss_ptrn, boss_atk_cd, boss_ozel_efekt
    global hiz_t, kalkan_t, cift_zipla_t, cift_zipla_kalan, miknatis_t, kalp_t
    global cp_x, cp_y, weapon, sh, boss_sv
    global hava_efektleri

    ox, oy = 100.0, 100.0
    hx, hy = 0.0, 0.0
    yr, yn = False, 1
    cn = mc
    ammo = BASE_AMMO
    wp_lv = 1
    shoot_cd = fire_cd = 0
    puan = 0
    cp_x, cp_y = 100.0, 100.0
    sh = 0
    boss_sv = False
    weapon = None

    hiz_t = kalkan_t = cift_zipla_t = 0
    cift_zipla_kalan = 0
    miknatis_t = kalp_t = 0

    boss_hp = 0
    boss_timer = 0
    boss_ptrn = 0
    boss_atk_cd = 0
    boss_ozel_efekt.clear()

    plt.clear()
    prl.clear()
    tzl.clear()
    dsm.clear()
    mpl.clear()
    ptk.clear()
    bullets.clear()
    fireballs.clear()
    boss_btl.clear()
    boss_muh.clear()
    hava_efektleri.clear()
