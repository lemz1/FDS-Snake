import pygame
import sys
import random
import serial
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Successfully connected to serial port {SERIAL_PORT}")
    time.sleep(1)
except Exception as e:
    print(f"Serial port error on {SERIAL_PORT}: {e}")
    print("Proceeding without serial input.")
    ser = None

def read_button_input():
    if ser and ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line in ("LEFT", "DOWN", "UP", "RIGHT"):
                return line
        except Exception as e:
            return None
    return None

pygame.init()

INITIAL_FPS = 10
SCORE_BAR_HEIGHT = 70
APPROX_GRID_WIDTH = 30
APPROX_GRID_HEIGHT = 20

COLOR_BG_LIGHT = (87, 138, 52)
COLOR_BG_DARK = (80, 128, 48)
COLOR_SNAKE = (50, 100, 200)
COLOR_APPLE = (231, 71, 29)
COLOR_TEXT = (255, 255, 255)
COLOR_SCORE_BG = (40, 60, 20)
COLOR_SCORE_TEXT = (220, 220, 220)
COLOR_OVERLAY = (0, 0, 0, 190)

screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

PLAYABLE_HEIGHT = HEIGHT - SCORE_BAR_HEIGHT
size_w = WIDTH // APPROX_GRID_WIDTH
size_h = PLAYABLE_HEIGHT // APPROX_GRID_HEIGHT
GRID_SIZE = max(1, min(size_w, size_h))
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = PLAYABLE_HEIGHT // GRID_SIZE
total_grid_width = GRID_WIDTH * GRID_SIZE
total_grid_height = GRID_HEIGHT * GRID_SIZE
x_offset = (WIDTH - total_grid_width) // 2
y_offset = (PLAYABLE_HEIGHT - total_grid_height) // 2

print(f"Screen: {WIDTH}x{HEIGHT}, Playable: {WIDTH}x{PLAYABLE_HEIGHT}")
print(f"Approx Desired Cells: {APPROX_GRID_WIDTH}x{APPROX_GRID_HEIGHT}")
print(f"Calculated Cell Size: {GRID_SIZE}")
print(f"Actual Grid Cells: {GRID_WIDTH}x{GRID_HEIGHT}")
print(f"Total Grid Area: {total_grid_width}x{total_grid_height}")
print(f"Offsets: x={x_offset}, y={y_offset}")

try:
    large_font = pygame.font.SysFont('Consolas', 50)
    medium_font = pygame.font.SysFont('Consolas', 36)
    small_font = pygame.font.SysFont('Consolas', 28)
except:
    print("Defaulting font.")
    large_font = pygame.font.Font(None, 50)
    medium_font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOPPED = (0, 0)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y)]
        if start_x > 0:
            self.body.append((start_x - 1, start_y))
        if start_x > 1:
            self.body.append((start_x - 2, start_y))
        self.direction = RIGHT
        self.new_direction = RIGHT
        self.grow = False
        self.alive = True

    def move(self):
        if not self.alive:
            return
        if self.new_direction == LEFT and self.direction != RIGHT:
            self.direction = self.new_direction
        elif self.new_direction == RIGHT and self.direction != LEFT:
            self.direction = self.new_direction
        elif self.new_direction == UP and self.direction != DOWN:
            self.direction = self.new_direction
        elif self.new_direction == DOWN and self.direction != UP:
            self.direction = self.new_direction
        current_head = self.body[0]
        new_x = current_head[0] + self.direction[0]
        new_y = current_head[1] + self.direction[1]
        new_head = (new_x, new_y)
        if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
            self.alive = False
            return
        collision_check_body = self.body if self.grow else self.body[:-1]
        if new_head in collision_check_body:
            self.alive = False
            return
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(x_offset + segment[0] * GRID_SIZE, y_offset + segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            inner_rect = rect.inflate(-GRID_SIZE*0.1, -GRID_SIZE*0.1)
            pygame.draw.rect(surface, COLOR_SNAKE, inner_rect, border_radius=int(GRID_SIZE*0.2))

class Apple:
    def __init__(self, snake_body):
        self.position = self._generate_new_position(snake_body)

    def _generate_new_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def respawn(self, snake_body):
        self.position = self._generate_new_position(snake_body)

    def draw(self, surface):
        center_x = x_offset + self.position[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = y_offset + self.position[1] * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 2 - max(1, GRID_SIZE // 10)
        pygame.draw.circle(surface, COLOR_APPLE, (center_x, center_y), radius)

def draw_background(surface):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = COLOR_BG_LIGHT if (row + col) % 2 == 0 else COLOR_BG_DARK
            rect = pygame.Rect(x_offset + col * GRID_SIZE, y_offset + row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)

def draw_score(surface, score):
    score_bar_rect = pygame.Rect(0, PLAYABLE_HEIGHT, WIDTH, SCORE_BAR_HEIGHT)
    pygame.draw.rect(surface, COLOR_SCORE_BG, score_bar_rect)
    score_text = small_font.render(f"Score: {score}", True, COLOR_SCORE_TEXT)
    text_rect = score_text.get_rect(center=(WIDTH / 2, PLAYABLE_HEIGHT + SCORE_BAR_HEIGHT / 2))
    surface.blit(score_text, text_rect)

def draw_text_overlay(surface, text_lines, font):
    overlay_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay_surf.fill(COLOR_OVERLAY)
    surface.blit(overlay_surf, (0, 0))
    v_spacing = font.get_linesize() * 1.2
    total_text_height = len(text_lines) * v_spacing
    start_y = (HEIGHT // 2) - (total_text_height // 2)
    current_y = start_y
    for line in text_lines:
        text_surf = font.render(line, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, int(current_y)))
        surface.blit(text_surf, text_rect)
        current_y += v_spacing

def start_screen():
    screen.fill(COLOR_BG_DARK)
    draw_text_overlay(screen, ["Snake Game!", "Press ANY KEY or BUTTON", "to Play"], large_font)
    pygame.display.flip()
    if ser:
        ser.reset_input_buffer()
    pygame.event.clear(pygame.KEYDOWN)
    while True:
        serial_cmd = read_button_input()
        if serial_cmd:
            return "PLAY"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                else:
                    return "PLAY"
        clock.tick(15)

def game_loop():
    snake = Snake()
    apple = Apple(snake.body)
    score = 0
    current_fps = INITIAL_FPS
    running = True

    while running and snake.alive:
        command = read_button_input()
        if command:
            if command == "LEFT":
                snake.new_direction = LEFT
            elif command == "RIGHT":
                snake.new_direction = RIGHT
            elif command == "UP":
                snake.new_direction = UP
            elif command == "DOWN":
                snake.new_direction = DOWN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return "QUIT", score
                if event.key == pygame.K_LEFT:
                    snake.new_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.new_direction = RIGHT
                elif event.key == pygame.K_UP:
                    snake.new_direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.new_direction = DOWN
        snake.move()
        if snake.alive and snake.body[0] == apple.position:
            score += 1
            snake.grow_snake()
            apple.respawn(snake.body)
        if running:
            screen.fill(COLOR_BG_DARK)
            draw_background(screen)
            if snake.alive:
                snake.draw(screen)
            apple.draw(screen)
            draw_score(screen, score)
            pygame.display.flip()
        clock.tick(current_fps)

    if not snake.alive:
        return "GAME_OVER", score
    else:
        return "QUIT", score

def game_over_screen(score):
    time.sleep(0.3)
    pygame.event.clear(pygame.KEYDOWN)
    if ser:
        ser.reset_input_buffer()
    draw_text_overlay(screen, [f"Game Over!", f"Score: {score}", "Press ANY KEY or BUTTON", "to Play Again"], medium_font)
    pygame.display.flip()
    while True:
        serial_cmd = read_button_input()
        if serial_cmd:
            if ser:
                ser.reset_input_buffer()
            return "RESTART"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                else:
                    if ser:
                        ser.reset_input_buffer()
                    return "RESTART"
        clock.tick(15)

if __name__ == "__main__":
    game_state = "START"
    final_score = 0
    while game_state != "QUIT":
        if game_state == "START":
            game_state = start_screen()
        elif game_state == "PLAY":
            game_state, final_score = game_loop()
        elif game_state == "GAME_OVER":
            game_state = game_over_screen(final_score)
        elif game_state == "RESTART":
            game_state = "PLAY"

    print("Exiting game.")
    if ser:
        try:
            ser.close()
            print("Serial port closed.")
        except Exception as e:
            print(f"Error closing serial port: {e}")
    pygame.quit()
    sys.exit()
