# 💣 Minesweeper

A modern, feature-rich implementation of the classic Minesweeper puzzle game, built with Python and Kivy. Uncover all safe cells without triggering any mines, use logic to deduce mine locations, and challenge yourself across multiple difficulty levels!

![Minesweeper Demo](Screenshot.png)

## 🎮 About the Game

Minesweeper is a logic puzzle game where players must uncover all cells on a grid that don't contain mines. Numbers reveal how many mines are adjacent to that cell, helping you deduce safe moves. Flag suspected mines with a right-click and clear safe cells with a left-click. One wrong move and it's game over!

## ✨ Features

### 🎯 Core Gameplay
- **Classic Minesweeper mechanics** with left-click to reveal and right-click to flag
- **Smart zero-cell expansion** - automatically reveals adjacent cells when you click a zero
- **Real-time timer** with precision down to tenths of a second
- **Flag counter** to track remaining mines
- **Intelligent flag system** - prevents placing more flags than mines exist
- **Auto-win detection** - automatically wins when all mines are correctly flagged

### 🎨 Visual & Audio
- **6 unique visual themes** including:
  - Classic Gaming sprites
  - Heart theme
  - Green nature theme  
  - Shark theme
  - Bat theme
  - Heat map
- **Repeating background texture** for a polished look
- **Sound effects** for clicks, wins, losses, and reveals
- **Custom Ultra font** for crisp text rendering

### 🎚️ Difficulty Levels
| Level | Grid Size | Mines | Cells to Clear |
|-------|-----------|-------|----------------|
| **Easy** | 9×16 (144 cells) | ~24 | ~120 |
| **Medium** | 16×16 (256 cells) | ~43 | ~213 |
| **Hard** | 20×30 (600 cells) | ~100 | ~500 |
| **Expert** | 33×40 (1,320 cells) | ~220 | ~1,100 |

### 🤖 Intelligent Solver
Built-in algorithmic solver that can automatically solve the puzzle using:
- **Pattern recognition** - identifies common mine patterns
- **Subset analysis** - deduces mine locations through logical subset relationships
- **Neighbor counting** - tracks revealed numbers and adjacent flags
- **Progressive solving** - applies increasingly sophisticated strategies

### 🎮 How to Play
1. **Left-click** a cell to reveal it
2. **Right-click** to place/remove a flag (cycles through flag → question mark → blank)
3. **Numbers** show how many mines are adjacent to that cell
4. **Reveal all safe cells** without clicking a mine to win!
5. Use the **Level** menu to change difficulty or enable the auto-solver
6. Click **Theme** in the Level menu to switch visual themes
7. Click **Restart** to generate a new random board

## 🚀 Quick Start

### Windows Users (Easiest)
Just double-click `StarApp.bat` or `MS_EXE.exe` - and you're playing!

### Everyone Else

## 📋 Requirements

- Python 3.7 or higher
- Kivy 2.3.0 or higher
- Windows (for pywin32 dependencies) or Unix-based system

## 🔧 Installation

1. **Clone or download this repository**

2. **Create a virtual environment**
   ```bash
   python -m venv MyVenv
   ```

3. **Activate the virtual environment**
   
   Windows:
   ```bash
   .\MyVenv\Scripts\activate
   ```
   
   macOS/Linux:
   ```bash
   source MyVenv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Game

### Method 1: Batch File (Windows)
```bash
StarApp.bat
```

### Method 2: Python Command
```bash
# Activate virtual environment first
.\MyVenv\Scripts\activate  # Windows
# OR
source MyVenv/bin/activate  # macOS/Linux

# Run the game
python src/minesweeper.py

# When done
deactivate
```

### Method 3: Executable (Windows)
```bash
MS_EXE.exe
```

## 📁 Project Structure

```
Minesweeper/
├── src/
│   └── minesweeper.py       # Main game logic and UI
├── images/
│   ├── gaming_SpriteSheet.png  # Classic theme sprites
│   ├── heart1.png              # Heart theme
│   ├── green3.png              # Nature theme
│   ├── shark1.png              # Shark theme
│   ├── bat1.png                # Bat theme
│   ├── heat_map.png            # Heat map theme
│   └── background/             # Background textures
├── sounds/
│   ├── click-button-140881.mp3      # Click sound
│   ├── low-impactwav-14905.mp3      # Lose sound
│   ├── punch-a-rock-161647.mp3      # Reveal sound
│   └── you-win-sequence-1-183948.mp3 # Win sound
├── fonts/
│   └── Ultra-Regular.ttf       # Custom font
├── MyVenv/                     # Virtual environment (excluded from git)
├── Screenshot.png              # Game screenshot
├── requirements.txt            # Python dependencies
└── README.md                   # You are here!
```

## 🧩 Algorithm Details

The solver uses sophisticated minesweeper-solving algorithms:

1. **Strip Zeros**: Opens all connected zero-value cells efficiently
2. **Add Flags**: Identifies cells that must be mines based on neighbor counts
3. **Remove Equal Mine Numbers**: Opens cells that can't possibly be mines
4. **Find Subsets (Type 1)**: Identifies common cells between neighbors to deduce safe moves
5. **Find Subsets (Type 2)**: Uses advanced set theory to identify mine patterns

The solver applies these strategies iteratively until no more moves can be deduced.

## 🐛 Known Issues

- **Cold start issues**: If launching from CMD fails, try reinitializing the virtual environment with `python -m venv MyVenv`
- **VSCode terminal**: More reliable for development and testing

## 🛠️ Development

Built with:
- **Kivy 2.3.0** - Cross-platform GUI framework
- **Python 3** - Core language
- **pywin32** - Windows integration

## 📄 License

See [LICENSE.txt](src/LICENSE.txt) for code licensing information.

## 🙏 Credits

- **Sounds**: See [sounds/ACCREDITATION.txt](sounds/ACCREDITATION.txt)
- **Images**: See [images/ACCREDITATION.txt](images/ACCREDITATION.txt)
- **Font**: Ultra font family - See [fonts/Ultra/LICENSE.txt](fonts/Ultra/LICENSE.txt)

## 🎯 Tips & Strategies

- Start by clicking corners or edges - statistically safer first moves
- Numbers indicate **exact** mine counts in the 8 surrounding cells
- If a revealed cell shows "3" and has 3 adjacent unrevealed cells, they're all mines!
- Use the question mark flag (?) to mark cells you're uncertain about
- The solver is great for learning advanced patterns and strategies

---

**Enjoy the game! Happy mine sweeping! 💣🎮**
