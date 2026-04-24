# Die and Die Again

A PySide6-based dice game and simulation framework featuring custom geometric dice widgets, a development sandbox, and core game logic for dice-based probability and games.

## Features

### GUI Components (PySide6)
- **Custom Die Widget (`DieWidget`)**:
    - Supports D3, D4, D6, D8, D10, D12, and D20.
    - **Unique Geometric Shapes**:
        - D3: Triangle
        - D4: Quadrilateral
        - D6: Hexagon
        - D8: Octagon
        - D10: Decagon
        - D12: Dodecagon
        - D20: 20-pointed circle
    - **Customizable Appearance**: Set foreground and background colors with automatic thick, dark borders.
    - **Animations**: Smooth rolling animation with randomized values.
    - **Dynamic Feedback**: Foreground color darkens or lightens during animation for visibility; tooltips show current die type and value.
- **Container Widgets**: `RollingDiceWidget` and `PlayerInventoryWidget` for managing groups of dice.
- **Player Widget**: Displays player name, cash, and dice statistics.
- **Sandbox Window**: An MDI (Multiple Document Interface) environment for testing all widgets and game logic simultaneously.
    - **Window Management**: Includes a "View" menu to toggle the visibility of individual test sub-windows.

### Core Logic
- **Flexible Dice System**: `Die` and `GameDie` classes supporting weighted rolls, random variations, and different materials (Wood, Stone, Resin, Metal, etc.).
- **Game Engine**: `GamePlayer`, `Game`, and specialized games like `OddEvenGame`.
- **Chance Calculator**: Utility for calculating and simulating probability outcomes.

## Installation

This project uses `uv` for dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd die_and_die_again

# Install dependencies
uv sync
```

Alternatively, you can install via `pip`:

```bash
pip install .
```

## Usage

### GUI Mode (Sandbox)
Launch the development sandbox to experiment with the widgets:

```bash
python die_and_die_again/main.py --gui
```

### CLI Mode
Run the default terminal-based simulations:

```bash
python die_and_die_again/main.py
```

Optional flags:
- `-v`, `--verbose`: Enable detailed logging (includes weight variations).
- `-g`, `--gui`: Launch the PySide6 GUI.

## Project Structure

- `die_and_die_again/core/`: Core game logic and dice simulation.
- `die_and_die_again/ui/`: PySide6 widget implementations.
- `die_and_die_again/app.py`: Main Application class.
- `die_and_die_again/main.py`: Entry point for both CLI and GUI.

