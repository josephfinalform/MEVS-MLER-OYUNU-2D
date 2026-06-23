# Mevsimler Oyunu (Seasons Game)

2D platformer built with **Pygame** and **Pillow**.

## Features

- 4 seasons: İlkbahar, Yaz, Sonbahar, Kış
- 16 rounds per season with unique bosses
- Seasonal weapons (e.g. Gunes Tufegi, Kar Topu)
- Power-ups: speed, shield, double jump, magnet, heart
- Difficulty modes: kolay, orta, zor, imkansiz
- Touch/joystick support

## Requirements

- Python 3.10+
- `pygame`, `Pillow`

## Quick Start

```bash
pip install pygame Pillow
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D | Move left/right |
| Space | Jump |
| Left Click | Shoot |
| Right Click | Fireball |
| Esc | Settings |
| R | Restart (on death) |

## Project Structure

- `main.py` – Game loop, physics, AI, rendering
- `config.py` – Constants
- `assets.py` – Color/asset definitions
- `levels.py` – Level generation and drawing
- `player.py` – Character sprite rendering
- `screens.py` – Menu, season select, settings, inventory
- `entities.py` – Game state object
- `audio.py` – Sound & music
- `particles.py` – Particle effects
- `ui.py` – UI button helper
- `save.py` – Save/load system
- `animations.py` – Animation utilities
- `build_exe.bat` – Windows executable build script
