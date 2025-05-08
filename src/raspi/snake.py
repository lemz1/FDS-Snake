import pygame
import sys
import random
import serial

# Initialize serial port for ESP32 buttons
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
except Exception as e:
    print("Serial port error:", e)
    ser = None

def read_button_input():
    if ser and ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            # Accept only the four directional commands
            if line in ("LEFT", "DOWN", "UP", "RIGHT"):
                return line
        except Exception as e:
            return None
    return None

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 30
GRID_HEIGHT = 20
FPS = 10

# Colors
LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (162, 209, 73)
RED = (231, 71, 29)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_COLOR = (80, 110, 30)

# Screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
GRID_SIZE = min(WIDTH // GRID_WIDTH, (HEIGHT - 70) // GRID_HEIGHT)
x_offset = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2

pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 28)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, 0)
        self.new_direction = (0, 0)
        self.grow = False
        
    def move(self):
        if self.new_direction != (0, 0):
            self.direction = self.new_direction
        
        new_x = self.body[0][0] + self.direction[0]
        new_y = self.body[0][1] + self.direction[1]
        
        # Check for collisions with walls or itself
        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            return False
        
        new_head = (new_x, new_y)
        if new_head in self.body[1:]:
            return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

class Apple:
    def __init__(self, snake_body):
        self.position = self.new_position(snake_body)
        
    def new_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

def draw_grid():
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            color = LIGHT_GREEN if (i + j) % 2 == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (x_offset + i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_score(score):
    pygame.draw.rect(screen, SCORE_COLOR, (0, HEIGHT - 70, WIDTH, 70))
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, HEIGHT - 55))

def game_loop():
    snake = Snake()
    apple = Apple(snake.body)
    score = 0
    
    running = True
    while running:
        # Process serial (ESP32) button input
        command = read_button_input()
        if command:
            if command == "LEFT" and snake.direction != (1, 0):
                snake.new_direction = (-1, 0)
            elif command == "RIGHT" and snake.direction != (-1, 0):
                snake.new_direction = (1, 0)
            elif command == "UP" and snake.direction != (0, 1):
                snake.new_direction = (0, -1)
            elif command == "DOWN" and snake.direction != (0, -1):
                snake.new_direction = (0, 1)
        
        # Process keyboard arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.new_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.new_direction = (1, 0)
                elif event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.new_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.new_direction = (0, 1)
        
        if not snake.move():
            game_over_screen(score)
            running = False
        
        if snake.body[0] == apple.position:
            snake.grow = True
            score += 1
            apple = Apple(snake.body)
        
        screen.fill(BLACK)
        draw_grid()
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, (50, 90, 30), 
                             (x_offset + segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw apple
        pygame.draw.circle(screen, RED, 
                           (x_offset + apple.position[0] * GRID_SIZE + GRID_SIZE // 2,
                            apple.position[1] * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE // 2 - 2)
        
        draw_score(score)
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(score):
    over_text = title_font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.fill(BLACK)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.delay(2000)
    if ser:
        ser.reset_input_buffer()  # Clear any remaining serial input

if __name__ == "__main__":
    while True:
        game_loop()
