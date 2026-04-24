import pygame
import random
import sys
import json
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Game settings
GRID_WIDTH = 20
GRID_HEIGHT = 15
CELL_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + 200  # Extra space for UI
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 100

FPS = 60
INITIAL_SPEED = 0.5  # Level 1 speed (slow)
MIN_SPEED = 0.05  # Level 10 speed (fast)
LEVEL_SPEED_DECAY = 0.95  # Speed multiplier per level (5% faster per level)
SPEED_INCREASE_THRESHOLD = 50
LEVEL_THRESHOLD = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

# Food types
FOOD_TYPES = {
    'regular': {'symbol': 'F', 'points': 10, 'growth': 1, 'weight': 70, 'color': RED},
    'golden': {'symbol': 'G', 'points': 30, 'growth': 2, 'weight': 20, 'color': YELLOW},
    'speed': {'symbol': 'S', 'points': 20, 'growth': 1, 'speed_boost': 0.7, 'weight': 8, 'color': CYAN},
    'bonus': {'symbol': 'B', 'points': 50, 'growth': 3, 'weight': 2, 'color': ORANGE}
}

# Score file path
SCORES_FILE = os.path.join(os.path.dirname(__file__), 'snake_scores.json')


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nokia Snake Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        
        self.player_name = ""
        self.game_scores = self.load_scores()
        self.input_mode = True  # Start with name input
        self.input_text = ""
        self.reset_game()
        
    def load_scores(self):
        """Load scores from file"""
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_scores(self, scores):
        """Save scores to file"""
        try:
            with open(SCORES_FILE, 'w') as f:
                json.dump(scores, f, indent=2)
        except:
            pass
    
    def add_score(self, name, score, level):
        """Add a new score to the list"""
        self.game_scores.append({
            'name': name,
            'score': score,
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        # Keep only last 10 scores
        self.game_scores = self.game_scores[-10:]
        self.save_scores(self.game_scores)
        
    def reset_game(self):
        """Initialize game state"""
        self.snake = [(GRID_WIDTH // 4, GRID_HEIGHT // 2), (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Right
        self.next_direction = (1, 0)
        self.food = (0, 0)
        self.food_type = 'regular'
        self.score = 0
        self.level = 1
        self.game_over = False
        self.game_started = False
        self.speed_boost = 1.0
        self.growth_counter = 0
        self.walls = []
        self.last_move_time = 0
        self.speed_boost_timer = 0
        self.input_mode = True  # Go back to name input for next game
        self.input_text = ""
        self.place_food()
        
    def get_random_food_type(self):
        """Select random food type based on weights"""
        total_weight = sum(food['weight'] for food in FOOD_TYPES.values())
        rand_val = random.randint(1, total_weight)
        
        cumulative = 0
        for ftype, fdata in FOOD_TYPES.items():
            cumulative += fdata['weight']
            if rand_val <= cumulative:
                return ftype
        return 'regular'
    
    def place_food(self):
        """Place food at random location"""
        while True:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            if (x, y) not in self.snake and (x, y) not in self.walls:
                self.food = (x, y)
                self.food_type = self.get_random_food_type()
                break
    
    def generate_walls(self):
        """Generate walls based on level"""
        self.walls = []
        
        if self.level >= 3:
            num_walls = random.randint(2, 4)
            for _ in range(num_walls):
                for _ in range(20):
                    x = random.randint(2, GRID_WIDTH - 3)
                    y = random.randint(2, GRID_HEIGHT - 3)
                    if (x, y) not in self.snake and (x, y) not in self.walls:
                        self.walls.append((x, y))
                        break
        
        if self.level >= 5:
            num_extra_walls = random.randint(1, 2)
            for _ in range(num_extra_walls):
                for _ in range(20):
                    x = random.randint(2, GRID_WIDTH - 3)
                    y = random.randint(2, GRID_HEIGHT - 3)
                    if (x, y) not in self.snake and (x, y) not in self.walls:
                        self.walls.append((x, y))
                        break
    
    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.input_mode:
                    # Handle name input
                    if event.key == pygame.K_RETURN and len(self.input_text) > 0:
                        self.player_name = self.input_text
                        self.input_text = ""
                        self.input_mode = False
                        self.game_started = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif len(self.input_text) < 15:
                        if event.unicode.isalnum() or event.unicode == ' ':
                            self.input_text += event.unicode
                else:
                    # Handle game input
                    if event.key == pygame.K_q:
                        return False
                    elif self.game_over and event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif self.game_started and not self.game_over:
                        dx, dy = self.direction
                        if event.key == pygame.K_w and dy != 1:
                            self.next_direction = (0, -1)
                        elif event.key == pygame.K_s and dy != -1:
                            self.next_direction = (0, 1)
                        elif event.key == pygame.K_a and dx != 1:
                            self.next_direction = (-1, 0)
                        elif event.key == pygame.K_d and dx != -1:
                            self.next_direction = (1, 0)
        return True
    
    def update(self, delta_time):
        """Update game state"""
        if not self.game_started or self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate current speed based on level
        # Speed gets faster as level increases
        speed = INITIAL_SPEED * (LEVEL_SPEED_DECAY ** (self.level - 1))
        if speed < MIN_SPEED:
            speed = MIN_SPEED
        speed = speed * self.speed_boost
        
        self.last_move_time += delta_time
        
        # Move snake if enough time has passed
        if self.last_move_time >= speed:
            self.last_move_time = 0
            self.move_snake()
        
        # Update speed boost timer
        if self.speed_boost < 1.0:
            self.speed_boost_timer -= delta_time
            if self.speed_boost_timer <= 0:
                self.speed_boost += 0.05
                if self.speed_boost > 1.0:
                    self.speed_boost = 1.0
                self.speed_boost_timer = 0.1  # Decay interval
    
    def move_snake(self):
        """Move snake and handle collisions"""
        dx, dy = self.direction
        new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
        
        # Check collisions
        head_x, head_y = new_head
        if head_x <= 0 or head_x >= GRID_WIDTH - 1 or head_y <= 0 or head_y >= GRID_HEIGHT - 1:
            self.game_over = True
            self.add_score(self.player_name, self.score, self.level)
            return
        
        if new_head in self.snake or new_head in self.walls:
            self.game_over = True
            self.add_score(self.player_name, self.score, self.level)
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        ate_food = (new_head == self.food)
        
        if ate_food:
            self.score += FOOD_TYPES[self.food_type]['points']
            
            total_growth = 1
            if self.food_type == 'golden':
                total_growth += 1
            elif self.food_type == 'bonus':
                total_growth += 2
            
            self.growth_counter = total_growth
            
            if self.food_type == 'speed':
                self.speed_boost = 0.7
                self.speed_boost_timer = 5.0  # 5 second boost
            
            self.place_food()
        else:
            self.growth_counter = 0
        
        # Remove tail if not growing
        if self.growth_counter > 0:
            self.growth_counter -= 1
        else:
            self.snake.pop()
        
        # Check level progression
        new_level = (self.score // LEVEL_THRESHOLD) + 1
        if new_level > self.level:
            self.level = new_level
            self.generate_walls()
    
    def draw(self):
        """Render game to screen"""
        self.screen.fill(BLACK)
        
        if self.input_mode:
            # Draw name input screen
            self.draw_name_input()
        elif self.game_over:
            # Draw game over screen with scores
            self.draw_game_over_with_scores()
        else:
            # Draw normal game screen
            self.draw_game_screen()
        
        pygame.display.flip()
    
    def draw_name_input(self):
        """Draw the name input screen"""
        title_text = self.font_large.render("NOKIA SNAKE GAME", True, WHITE)
        prompt_text = self.font_medium.render("Enter Your Name:", True, YELLOW)
        input_box_text = self.font_medium.render(self.input_text + "|", True, GREEN)
        hint_text = self.font_small.render("Press ENTER to start", True, GRAY)
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        self.screen.blit(title_text, (center_x - title_text.get_width() // 2, center_y - 100))
        self.screen.blit(prompt_text, (center_x - prompt_text.get_width() // 2, center_y - 20))
        
        # Draw input box
        input_rect = pygame.Rect(center_x - 120, center_y + 20, 240, 50)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        self.screen.blit(input_box_text, (center_x - input_box_text.get_width() // 2, center_y + 25))
        
        self.screen.blit(hint_text, (center_x - hint_text.get_width() // 2, center_y + 100))
    
    def draw_game_screen(self):
        """Draw the normal game screen"""
        # Draw game area border
        pygame.draw.rect(self.screen, WHITE, (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
        
        # Draw grid
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(self.screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw walls
        for wx, wy in self.walls:
            pygame.draw.rect(self.screen, GRAY, (wx * CELL_SIZE + 2, wy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        # Draw food
        fx, fy = self.food
        food_color = FOOD_TYPES[self.food_type]['color']
        pygame.draw.rect(self.screen, food_color, (fx * CELL_SIZE + 2, fy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        # Draw snake
        for i, (sx, sy) in enumerate(self.snake):
            if i == 0:
                pygame.draw.rect(self.screen, GREEN, (sx * CELL_SIZE + 1, sy * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, (sx * CELL_SIZE + 2, sy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        # Draw UI panel
        ui_x = GRID_WIDTH * CELL_SIZE + 10
        pygame.draw.rect(self.screen, GRAY, (ui_x - 5, 0, 200, SCREEN_HEIGHT), 1)
        
        # Player name display
        name_text = self.font_small.render(f"Player: {self.player_name}", True, CYAN)
        self.screen.blit(name_text, (ui_x, 10))
        
        # Score display
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (ui_x, 45))
        
        # Level display
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (ui_x, 85))
        
        # Food type display
        food_text = self.font_small.render(f"Food: {self.food_type}", True, FOOD_TYPES[self.food_type]['color'])
        self.screen.blit(food_text, (ui_x, 125))
        
        # Speed boost display
        if self.speed_boost < 1.0:
            boost_text = self.font_small.render(f"Boost: {self.speed_boost:.2f}x", True, CYAN)
            self.screen.blit(boost_text, (ui_x, 155))
        
        # Controls info at bottom
        controls_y = GRID_HEIGHT * CELL_SIZE + 10
        controls_text = self.font_small.render("W/A/S/D: Move | Q: Quit", True, WHITE)
        self.screen.blit(controls_text, (10, controls_y))
    
    def draw_game_over_with_scores(self):
        """Draw game over screen with last 10 scores"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over message
        game_over_text = self.font_large.render("GAME OVER!", True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 20))
        
        # Draw current game stats
        stats_y = 70
        final_score_text = self.font_medium.render(f"Your Score: {self.score} | Level: {self.level}", True, YELLOW)
        self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, stats_y))
        
        # Draw last 10 scores
        scores_title = self.font_medium.render("Last 10 Games:", True, CYAN)
        self.screen.blit(scores_title, (20, stats_y + 50))
        
        scores_y = stats_y + 85
        for i, score_data in enumerate(reversed(self.game_scores[-10:])):
            score_line = f"{i+1}. {score_data['name']:15} Score: {score_data['score']:4d} Lvl: {score_data['level']:2d}"
            score_text = self.font_tiny.render(score_line, True, WHITE)
            self.screen.blit(score_text, (30, scores_y + i * 20))
        
        # Draw restart instruction
        restart_text = self.font_medium.render("Press SPACE to play again or Q to quit", True, YELLOW)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            delta_time = self.clock.tick(FPS) / 1000.0
            
            running = self.handle_input()
            self.update(delta_time)
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Exiting.")
