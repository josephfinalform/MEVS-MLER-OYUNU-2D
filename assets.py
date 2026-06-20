import pygame

B = (255, 255, 255); S = (0, 0, 0); TEN = (255, 210, 180)
PEMBE = (255, 20, 147); NP = (255, 50, 180); MB = (0, 180, 255)
NM = (0, 255, 255); SAC = (255, 100, 200); SG = (200, 50, 150)
GB = (240, 240, 255); GM = (80, 200, 255); GI = (255, 255, 255)
AG = (200, 80, 80); ALTIN = (255, 215, 0); K = (200, 50, 50)
NY = (0, 255, 100); GT = (40, 40, 50); AGT = (60, 60, 75)
C1 = (255, 100, 200); C2 = (255, 255, 100)
DT = (220, 180, 150); DS = (180, 100, 50); DG = (255, 200, 100)
MM = (50, 100, 200); YP = (200, 150, 50); KR = (220, 230, 255)

GENISLIK = 1200
YUKSEKLIK = 700

MEV = {
    "ilkbahar": {"a": (30, 60, 40), "z": (60, 180, 60), "p": (80, 200, 80), "k": (120, 255, 120), "t": (255, 100, 100), "ac": (40, 80, 50)},
    "yaz": {"a": (50, 70, 60), "z": (200, 180, 60), "p": (220, 200, 80), "k": (255, 230, 120), "t": (255, 80, 50), "ac": (70, 60, 35)},
    "sonbahar": {"a": (50, 30, 30), "z": (180, 100, 40), "p": (200, 120, 50), "k": (255, 160, 80), "t": (200, 50, 50), "ac": (60, 35, 35)},
    "kis": {"a": (30, 40, 60), "z": (180, 200, 220), "p": (180, 200, 220), "k": (220, 240, 255), "t": (100, 150, 200), "ac": (40, 50, 70)},
}

KOSTUMLER = {
    "ilkbahar": {"i": "Cicek Taci", "r": C1, "a": "Bahar ciceklerinden tac"},
    "yaz": {"i": "Gunes Gozlugu", "r": ALTIN, "a": "Havali gunes gozlugu"},
    "sonbahar": {"i": "Yaprak Pelerin", "r": YP, "a": "Sonbahar yapragindan pelerin"},
    "kis": {"i": "Kar Taci", "r": KR, "a": "Kar tanelerinden tac"},
}

ms = ["ilkbahar", "yaz", "sonbahar", "kis"]

z_can = {"kolay": 7, "orta": 5, "zor": 3, "imkansiz": 2}
z_dh = {"kolay": 0.5, "orta": 1.0, "zor": 1.5, "imkansiz": 2.0}
z_yc = {"kolay": 0.45, "orta": 0.5, "zor": 0.6, "imkansiz": 0.7}
z_zg = {"kolay": -13, "orta": -13, "zor": -12, "imkansiz": -11}

BOSS_HP = {"kolay": 8, "orta": 12, "zor": 18, "imkansiz": 25}
BOSS_SPD = {"kolay": 1.5, "orta": 2.5, "zor": 3.5, "imkansiz": 4.5}
BOSS_ATK_CD = {"kolay": 90, "orta": 60, "zor": 40, "imkansiz": 25}

BOSS_SKIN = {"kolay": 0, "orta": 0, "zor": 1, "imkansiz": 1}
BOSS_GLOW = {"kolay": (100, 100, 100), "orta": (200, 200, 50), "zor": (255, 50, 50), "imkansiz": (255, 0, 100)}

WP_DATA = {
    "ilkbahar": {"i": "Cicek Kalasnikof", "r": C1, "dmg": 1, "spd": 10, "a": 25, "cd": 7, "s": "cicek"},
    "yaz": {"i": "Gunes Tufegi", "r": ALTIN, "dmg": 2, "spd": 10, "a": 25, "cd": 7, "s": "cizgi"},
    "sonbahar": {"i": "Yaprak Firlatan", "r": YP, "dmg": 2, "spd": 8, "a": 25, "cd": 7, "s": "yaprak"},
    "kis": {"i": "Kar Topu", "r": KR, "dmg": 3, "spd": 7, "a": 25, "cd": 7, "s": "kar"},
}

BOSS_ADI = {
    "ilkbahar": "CICEK CANAVARI",
    "yaz": "GUNES DEV",
    "sonbahar": "YAPRAK FIRTINASI",
    "kis": "KAR KRALI",
}

MS = ms

# Terraria-style biome renkleri
BIOME = {
    "ilkbahar": {
        "sky": (135, 206, 235), "sun": (255, 255, 200),
        "grass": (80, 200, 60), "soil": (140, 100, 60), "deep_soil": (100, 70, 40),
        "stone": (130, 130, 130), "tree_trunk": (100, 70, 40), "tree_leaf": (60, 180, 50),
        "bg_tree1": (50, 140, 40), "bg_tree2": (40, 120, 35), "bg_tree3": (30, 100, 30),
    },
    "yaz": {
        "sky": (100, 180, 255), "sun": (255, 230, 100),
        "grass": (160, 180, 50), "soil": (180, 140, 70), "deep_soil": (140, 100, 50),
        "stone": (160, 150, 120), "tree_trunk": (120, 80, 40), "tree_leaf": (140, 170, 40),
        "bg_tree1": (100, 140, 30), "bg_tree2": (80, 120, 25), "bg_tree3": (60, 100, 20),
    },
    "sonbahar": {
        "sky": (180, 160, 200), "sun": (255, 200, 150),
        "grass": (160, 120, 50), "soil": (130, 80, 40), "deep_soil": (90, 60, 30),
        "stone": (110, 100, 90), "tree_trunk": (80, 50, 25), "tree_leaf": (200, 100, 30),
        "bg_tree1": (150, 80, 20), "bg_tree2": (120, 60, 15), "bg_tree3": (100, 50, 10),
    },
    "kis": {
        "sky": (200, 210, 230), "sun": (220, 220, 240),
        "grass": (200, 210, 220), "soil": (140, 130, 140), "deep_soil": (100, 90, 100),
        "stone": (150, 155, 160), "tree_trunk": (80, 75, 70), "tree_leaf": (180, 190, 200),
        "bg_tree1": (150, 160, 170), "bg_tree2": (130, 140, 150), "bg_tree3": (110, 120, 130),
    }
}
