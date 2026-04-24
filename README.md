# Nokia Snake Game 🐍

A modern Python recreation of the classic Nokia Snake game with enhanced graphics, multiple food types, progressive difficulty levels, and score tracking.

## Features

✨ **Graphical Interface**
- Built with Pygame for smooth, interactive gameplay
- Colorful grid-based game board
- Real-time rendering with proper collision detection

🎮 **Gameplay Elements**
- Progressive levels (1-10) with increasing difficulty
- Multiple food types with different effects:
  - 🔴 **Regular Food** - 10 points, grow by 1
  - 🟡 **Golden Food** - 30 points, grow by 2
  - 🔵 **Speed Boost** - 20 points + temporary speed boost
  - 🟠 **Bonus Food** - 50 points, grow by 3
- Dynamic wall generation (appears at Level 3+)
- Speed increases progressively from Level 1 to Level 10

👤 **Player Tracking**
- Enter your name at the start of each game
- Automatic score recording and persistence
- Last 10 games leaderboard displayed after each game
- Score history saved to `snake_scores.json`

## Installation

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Setup

1. **Install Python dependencies:**
```bash
pip install pygame
```

2. **Navigate to the game directory:**
```bash
cd path/to/snake_game
```

3. **Run the game:**
```bash
python snake_game.py
```

## How to Play

### Starting the Game
1. Launch the game
2. Enter your player name (up to 15 characters)
3. Press ENTER to start playing

### Controls
- **W** - Move Up
- **S** - Move Down
- **A** - Move Left
- **D** - Move Right
- **Q** - Quit Game
- **SPACE** - Restart after Game Over

### Gameplay Mechanics

**Scoring System:**
- Collect food to earn points and grow your snake
- Higher point values for special food items
- Reach higher levels by accumulating points

**Difficulty Progression:**
- **Level 1**: Very slow, easy to play (0.5 seconds per move)
- **Levels 2-9**: Gradually increase in speed
- **Level 10**: Fast gameplay (0.05 seconds per move)

**Obstacles:**
- **Walls**: Appear starting at Level 3, more at Level 5+
- **Borders**: Collision with game boundaries ends the game
- **Self-collision**: Running into your own body ends the game

**Speed Boost:**
- Eat Speed food to temporarily make the snake 30% faster
- Boost effect lasts 5 seconds
- Speed gradually returns to normal after boost wears off

### Game Over
When your snake collides with a wall, border, or itself:
1. Your final score and level are displayed
2. The last 10 games are shown with player names and scores
3. Press SPACE to play again or Q to quit

## Game Interface

### Main Game Screen
- **Left side**: 20×15 grid-based game board
- **Right side**: UI panel showing:
  - Player name
  - Current score
  - Current level
  - Current food type and color
  - Active speed boost indicator (if active)
- **Bottom**: Control instructions

### Name Input Screen
- Clean interface prompting for player name
- Real-time text input display
- Instructions to press ENTER to start

### Game Over Screen
- Your final score and level reached
- Leaderboard with last 10 games
- Shows player name, score, level, and date/time for each game
- Option to play again or quit

## File Structure

```
snake_game.py           # Main game application
README_SNAKE_GAME.md    # This file
snake_scores.json       # Score history (auto-generated)
```

## Technical Details

### Architecture
- **Object-Oriented Design**: Single `SnakeGame` class encapsulates all game logic
- **State Management**: Tracks game states (input, playing, game over)
- **Delta Time**: Frame-independent movement using delta time calculations
- **Persistent Storage**: JSON-based score storage

### Key Classes and Methods

**SnakeGame**
- `__init__()` - Initialize the game window and state
- `reset_game()` - Reset game state for a new game
- `handle_input()` - Process keyboard events
- `update(delta_time)` - Update game state each frame
- `move_snake()` - Handle snake movement and collisions
- `draw()` - Render current game state
- `run()` - Main game loop

### Food System
- Weighted random selection for food types
- Special effects applied based on food type
- Growth counter system for multi-segment growth

### Level System
- Speed determined by level (not score)
- Walls generated dynamically per level
- Smooth progression with exponential difficulty scaling

## Configuration

You can modify these constants in the code to customize gameplay:

```python
INITIAL_SPEED = 0.5      # Level 1 speed (seconds)
MIN_SPEED = 0.05         # Level 10 speed cap
LEVEL_SPEED_DECAY = 0.95 # Speed increase per level
LEVEL_THRESHOLD = 100    # Points needed for next level
GRID_WIDTH = 20          # Game board width
GRID_HEIGHT = 15         # Game board height
```

## Tips for Playing

1. **Early Levels**: Use this time to practice and build up points safely
2. **Food Selection**: Prioritize regular/speed food in early levels, save risky bonus food for later
3. **Wall Navigation**: At higher levels, navigate around walls carefully - they spawn randomly
4. **Speed Boost**: Use Speed food strategically when you need a temporary advantage
5. **Score Tracking**: Try to beat your own scores by reaching higher levels!

## Troubleshooting

**Game won't start?**
- Ensure Pygame is installed: `pip install pygame`
- Check Python version is 3.7+: `python --version`

**Scores not saving?**
- Verify write permissions in the game directory
- Check `snake_scores.json` exists or can be created

**Game runs slowly?**
- Close other applications to free up system resources
- Check your system meets minimum requirements

## Version History

**v1.0** - Initial release
- Complete graphical Snake game with Pygame
- Progressive difficulty levels
- Multiple food types
- Player name and score tracking
- Last 10 games leaderboard

## Credits

Classic Nokia Snake gameplay reimagined with modern Python and Pygame technology.

## License

This project is open-source and available for personal and educational use.

---

**Enjoy the game! 🎮**
