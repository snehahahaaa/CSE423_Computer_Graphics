# Cellular Guardian 🧬🛡️

**Cellular Guardian** is a 3D arcade-style survival game built with **Python** and **PyOpenGL**.

In this game, the player controls a white blood cell inside a moving blood-vessel tunnel. The main goal is to survive incoming viruses, collect immunity shields, use speed boosts, defeat enemy waves, and prevent the fever level from reaching its maximum.

The game uses **OpenGL**, **GLUT**, and **GLU** to render a real-time 3D biological environment with animated blood cells, virus enemies, pickups, wave progression, boss fights, camera switching, and HUD elements.

---

## 🎮 Game Overview

In **Cellular Guardian**, you play as a white blood cell travelling through a bloodstream-like tunnel.

Your task is to protect the body by surviving virus attacks and collecting useful power-ups. Different viruses approach the player through the tunnel. If enemies pass the player, the fever level increases. If the fever reaches the maximum limit, the game ends.

The difficulty increases over time through a wave-based system, and a boss virus appears after reaching a certain score.

---

## ✨ Features

- 3D bloodstream tunnel environment
- Animated moving tunnel effect
- White blood cell player model
- Red blood cells and blood particles for atmosphere
- Multiple enemy types:
  - Spike Virus
  - Crystal Virus
  - Boss Virus
- Wave-based difficulty system
- Boss fight system
- Fever bar system
- Score tracking
- Immunity shield pickup
- Speed boost pickup
- First-person and third-person camera modes
- Keyboard and mouse controls
- Game over and restart system
- Real-time animation using GLUT idle function

---

## 🧠 Game Mechanics

### White Blood Cell Player

The player controls a white blood cell inside the bloodstream tunnel. The cell can move up, down, left, and right while staying inside the tunnel boundary.

### Fever System

The fever bar represents the danger level of the body.

- If enemies pass the player, fever increases.
- If the boss virus escapes, fever increases heavily.
- If fever reaches the maximum limit, the game is over.

### Immunity Shield

The immunity pickup gives the player temporary protection.

While the shield is active:

- The player does not take fever damage.
- Viruses can be destroyed safely.
- The player model visually changes to show shield activity.

### Speed Boost

The speed boost pickup temporarily increases player movement speed. This helps the player move faster and avoid enemies more easily.

### Enemy Waves

The game uses a wave system.

As the score increases:

- Enemy spawn rate becomes faster.
- Enemy difficulty increases.
- The wave number increases.

### Boss Virus

After the player reaches a certain score, a boss virus appears.

The boss virus:

- Has multiple health points
- Moves toward the player
- Must be hit multiple times
- Gives a large score reward when defeated

---

## 🕹️ Controls

| Key / Input | Action |
|------------|--------|
| `W` | Move up |
| `S` | Move down |
| `A` | Move left |
| `D` | Move right |
| `C` | Toggle first-person / third-person camera |
| Right Mouse Button | Toggle camera mode |
| Arrow Up | Move camera upward / look upward |
| Arrow Down | Move camera downward / look downward |
| Arrow Left | Rotate camera left |
| Arrow Right | Rotate camera right |
| `R` | Restart game after game over |

---

## 🛠️ Technologies Used

- Python
- PyOpenGL
- OpenGL
- GLUT
- GLU
- Math module
- Time module
- Random module

---

## 📦 Installation and Setup

Follow these steps to install and run **Cellular Guardian** on your computer.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cellular-guardian.git
cd cellular-guardian
```

### 2. Install Python Dependencies

Make sure Python is installed on your computer. Then install the required Python packages:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### 3. Install GLUT / FreeGLUT

Depending on your operating system, you may need to install GLUT or FreeGLUT.

#### Linux / Ubuntu

```bash
sudo apt update
sudo apt install freeglut3-dev
```

#### Windows

If you face a GLUT-related error, install FreeGLUT and make sure the required `freeglut.dll` file is available in one of these locations:

- the project folder
- the Python installation directory
- a folder included in your system PATH

### 4. Run the Game

After installing everything, run:

```bash
python Cellular_guardian.py
```

---
