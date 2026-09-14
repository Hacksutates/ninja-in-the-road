# 🥷 Ninja in the Road

**Ninja in the Road** is a 2D action-platformer developed in Python using **Pygame**.

This project was created as my first full game project, combining platforming, melee combat, enemies, projectiles, animated sprites, environmental effects, and a custom level editor.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Status](https://img.shields.io/badge/status-personal%20project-orange)

## 🎮 About the Game

You play as a ninja travelling through dangerous levels while fighting enemies and avoiding projectiles.

The game features:

- 🥷 Playable ninja character
- ⚔️ Sword combat with a 3-hit combo
- 🏃 Running and jumping
- 🧱 Tile-based levels
- 👾 Enemy AI
- 🔫 Enemies that can shoot projectiles
- 💥 Sword interaction with enemy bullets
- 🌧️ Dynamic rain effects
- 🔊 Sound effects and ambient audio
- 📷 Camera following the player
- 💀 Death and respawn system
- 🎯 Level completion system
- 🗺️ Built-in level editor
- 💾 JSON-based custom maps
- ⏸️ Pause functionality

## 🕹️ Controls

### Gameplay

| Key / Input | Action |
|---|---|
| `A` | Move left |
| `D` | Move right |
| `W` | Jump |
| `SPACE` | Jump |
| `Left Mouse Button` | Attack |
| `ESC` | Pause / menu |

### Level Editor

| Key / Input | Action |
|---|---|
| `A / D` | Move horizontally |
| `W / S` | Move vertically |
| `Left Mouse Button` | Place tile |
| `Right Mouse Button` | Delete tile |
| `Middle Mouse Button` | Toggle off-grid placement |
| `Mouse Wheel` | Change tile variant |
| `SHIFT + Mouse Wheel` | Change tile group |
| `T` | Apply auto-tiling |
| `ESC` | Pause / return to menu |

The game currently provides three standard levels and allows maps to be loaded from JSON files.

## ✨ Gameplay

### Combat

The ninja has a sword-based melee system with multiple attack animations.

Enemies can:

- Move around the level
- Track the player
- Attack the player on contact
- Shoot bullets

The player can also **deflect enemy bullets with the sword**, producing a projectile effect and sound feedback.

### Movement

The player can:

- Move left and right
- Jump
- Interact with the level's tilemap
- Reach the level's finish point

The camera smoothly follows the player's position during gameplay.

### Level Editor

One of the main features of the project is the built-in level editor.

From the editor you can:

1. Create a new map
2. Open an existing map
3. Place tiles
4. Place special objects such as spawn points and the finish
5. Delete objects
6. Switch between tile variants
7. Enable off-grid placement
8. Apply automatic tiling
9. Save the map as a JSON file

Maps contain information about the tile size, tilemap and off-grid objects, allowing custom levels to be saved and loaded later.

## 🛠️ Technologies

### Python

The main programming language used for the project.

### Pygame

Used for:

- Rendering
- Game loop
- Input handling
- Collision detection
- Animations
- Audio
- Window management

### Tkinter

Used for file dialogs in the level editor, allowing players to open and save custom JSON maps.

### JSON

Used as the format for storing custom levels.

## 📁 Project Structure

```text
ninja-in-the-road/
│
├── data/
│   ├── maps/
│   │   ├── standart/
│   │   │   ├── level1.json
│   │   │   ├── level2.json
│   │   │   └── level3.json
│   │   ├── sfx/
│   │   └── ...
│   │
│   └── ...
│
├── scripts/
│   ├── entities.py
│   ├── levels.py
│   ├── rain.py
│   ├── tilemap.py
│   ├── utils.py
│   └── weapon.py
│
├── game.py
├── .gitignore
└── README.md
```

The main `game.py` file initializes Pygame, loads the game's assets and sounds, creates the player and tilemap, and controls the main menu, level editor and gameplay loop.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Hacksutates/ninja-in-the-road.git
cd ninja-in-the-road
```

### 2. Install Python

Make sure Python 3 is installed:

```bash
python --version
```

### 3. Install Pygame

```bash
pip install pygame
```

### 4. Run the game

```bash
python game.py
```

The game should open in a maximized window.

> **Note:** The project uses relative paths for assets and data files, so `game.py` should be launched from the project root directory.

## 🎯 Main Menu

The main menu provides three primary options:

- **Start** — choose and play a level
- **Editor** — create or edit maps
- **Leave** — exit the game

The game currently includes three standard levels and an option to load levels from a directory.

## 🗺️ Creating Custom Levels

To create a custom level:

1. Launch the game.
2. Select **Editor**.
3. Choose **Create New Map**.
4. Place tiles and objects using the editor.
5. Add a player spawn point.
6. Add a finish point.
7. Add enemy spawners.
8. Save the map as a `.json` file.
9. Load the map through **Start → From Directory**.

This makes it possible to create and test custom levels without modifying the game's source code.

## 🔊 Audio & Visual Effects

The game includes several sound effects and environmental elements, including:

- Rain ambience
- Background ambience
- Sword attacks
- Enemy death
- Bullet impacts
- Bullet sounds
- Player death

The game also includes animated player and enemy sprites, rain particles, screen shake and transition effects.

## 🧠 Architecture

The project is separated into several modules:

### `game.py`

Contains the main game loop, menu system, level editor and gameplay logic.

### `scripts/entities.py`

Contains game entities such as:

- Player
- Enemies
- Bodies / defeated enemies

### `scripts/tilemap.py`

Responsible for loading, storing and rendering tile-based maps.

### `scripts/utils.py`

Contains reusable utilities such as:

- Image loading
- Animations
- Buttons
- Bullets
- Projectiles

### `scripts/weapon.py`

Contains the sword and combat logic.

### `scripts/rain.py`

Handles the game's rain effect.

### `scripts/levels.py`

Contains level-related functionality.

## 📌 Project Goals

This project was primarily created as a learning project to practice:

- Python programming
- Object-oriented programming
- Game development
- Pygame
- Collision detection
- Game physics
- Animation systems
- Enemy AI
- File I/O
- JSON serialization
- Level editor development
- Structuring a larger Python project

## 🔮 Possible Future Improvements

Some possible improvements for future versions:

- [ ] More levels
- [ ] More enemy types
- [ ] Boss fights
- [ ] Health system
- [ ] More weapons
- [ ] Better enemy AI
- [ ] Main menu animations
- [ ] Settings menu
- [ ] Save/load progress
- [ ] Better level editor UI
- [ ] More tile types
- [ ] Custom key bindings
- [ ] Controller support
- [ ] Executable release for Windows
- [ ] Improved collision and physics
- [ ] More polished animations and visual effects

## 👤 Author

**Hacksutates**

GitHub:  
https://github.com/Hacksutates

Project repository:  
https://github.com/Hacksutates/ninja-in-the-road

---

⭐ If you like the project, consider giving it a star!
