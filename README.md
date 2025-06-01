# Maze Generator & Solver

A Python application that generates random mazes and solves them with visual animation.

## Features

- **Random Maze Generation**: Creates unique mazes using recursive backtracking algorithm
- **Visual Solving**: Animated pathfinding with red solution paths and purple backtracking
- **Customizable Size**: Adjustable rows (5-50) and columns (5-60)
- **Animation Speed Control**: Separate speed settings for maze generation and solving
- **Window Sizing**: Configurable window dimensions for optimal display
- **Dark Theme**: Black background with white walls and green entry/exit markers

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Usage

### Basic Usage
```bash
python3 main.py
```

### Custom Window Size
```bash
python3 main.py --width 800 --height 600
```

## Controls

- **Window Size**: Set width and height, then click "Apply"
- **Maze Size**: Use sliders to set rows (R) and columns (C)
- **Speed**: Adjust generation (Gen) and solving (Sol) animation speeds
- **New**: Create a new maze
- **Solve**: Find and animate the solution path

## How It Works

1. Set your desired window and maze dimensions
2. Click "Apply" to apply window size
3. Click "New" to generate a maze
4. Click "Solve" to watch the animated solution

The maze uses:
- **White lines**: Walls
- **Black areas**: Passages
- **Green lines**: Entry (top-left) and exit (bottom-right)
- **Red lines**: Solution path
- **Purple lines**: Backtracking during solving

## Files

- `main.py`: Entry point with command line argument parsing
- `maze_app.py`: Main application with UI controls
- `maze.py`: Maze generation and solving algorithms
- `cell.py`: Individual maze cell implementation
- `graphics.py`: Window and drawing utilities
