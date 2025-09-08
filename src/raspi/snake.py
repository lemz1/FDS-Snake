#!/usr/bin/env python3
import pygame
from pygame.math import Vector2
import sqlite3
from functions.get_asset_path import get_asset_path
from functions.body import SNAKE
from functions.fruit import FRUIT
from functions.controls import read_button_input
from functions.directions import draw_direction_buttons
import functions.name as name_system
from functions.database import DataBase


pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

cell_size = 30
cell_number_x = screen_width // cell_size
cell_number_y = (screen_height - cell_size * 2) // cell_size

apple_image = pygame.image.load(get_asset_path("assets/apple.png")).convert_alpha()
apple_image_for_score = pygame.transform.scale(
    apple_image, (int(cell_size * 0.8), int(cell_size * 0.8))
)

crown_image = pygame.image.load(get_asset_path("assets/crown.png")).convert_alpha()
crown_image_for_score = pygame.transform.scale(
    crown_image, (int(cell_size * 0.8), int(cell_size * 0.8))
)
try:
    game_font = pygame.font.Font(
        get_asset_path("Font/PoetsenOne-Regular.ttf"), int(cell_size * 0.8)
    )
except pygame.error:
    game_font = pygame.font.SysFont("Arial", int(cell_size * 0.8))

current_speed = 140
SCREEN_UPDATE = pygame.USEREVENT
game_active = True


class MAIN:
    def __init__(self):
        self.snake = SNAKE(screen, cell_size)
        self.fruit = FRUIT(screen, cell_size, apple_image, cell_number_x, cell_number_y)
        self.db = DataBase()

    def update(self):
        self.snake.move_snake(cell_number_x, cell_number_y)
        self.check_fruit_collision()
        self.check_fail_collision()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_highscore()

    def check_fruit_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            for b in self.snake.body:
                if self.fruit.position == b:
                    self.fruit.randomize()
            update_speed()

    def check_fail_collision(self):
        head = self.snake.body[0]
        if not (0 <= head.x < cell_number_x and 0 <= head.y < cell_number_y):
            self.game_over()
        for b in self.snake.body[1:]:
            if b == head:
                self.game_over()

    def draw_score(self):
        s = str(len(self.snake.body) - 3)
        surf = game_font.render(s, True, (56, 74, 12))
        sx = screen_width - (cell_size * 2.5)
        sy = cell_size * 1.5
        rect = surf.get_rect(center=(sx, sy))
        bg_rect_width = surf.get_width() + cell_size
        bg = pygame.Rect(0, 0, bg_rect_width + 40, rect.height + 30)
        bg.midright = (screen_width - cell_size * 0.5, rect.centery)

        pygame.draw.rect(screen, (167, 209, 61), bg, border_radius=5)
        screen.blit(surf, surf.get_rect(midright=(bg.right - 10, bg.centery)))
        apple_width = int(cell_size * 1.5)
        apple_height = int(cell_size * 1.5)

        scaled_apple = pygame.transform.scale(
            apple_image_for_score, (apple_width, apple_height)
        )

        ar = scaled_apple.get_rect(
            midright=(bg.left + scaled_apple.get_width() + 10, bg.centery)
        )
        screen.blit(scaled_apple, ar)

    def draw_highscore(self):
        x = cell_size * 1.5
        y = cell_size * 1.5

        conn = sqlite3.connect("Leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(Punkte) FROM Highscores")
        result = cursor.fetchone()

        top_score = result[0] if result[0] is not None else 0
        score = str(top_score)

        surf = game_font.render(score, True, (56, 74, 12))
        rect = surf.get_rect(center=(x, y))

        bg_rect_width = surf.get_width() + cell_size
        bg = pygame.Rect(0, 0, bg_rect_width + 40, rect.height + 30)
        bg.midleft = (x, y)

        pygame.draw.rect(screen, (167, 209, 61), bg, border_radius=5)

        screen.blit(surf, surf.get_rect(midleft=(bg.left + 10, bg.centery)))

        crown_width = int(cell_size * 1.5)
        crown_height = int(cell_size * 1.5)

        scaled_crown = pygame.transform.scale(
            crown_image_for_score, (crown_width, crown_height)
        )

        ar = scaled_crown.get_rect(midright=(bg.right - 10, bg.centery))
        screen.blit(scaled_crown, ar)

    def game_over(self):
        global game_active
        game_active = False
        current_score_val = len(self.snake.body) - 3
        if self.db.in_top10(current_score_val):
            name_system.initialize_state(current_score_val)


def reset_game():
    global main_game, game_active, current_speed
    main_game = MAIN()
    current_speed = 100
    pygame.time.set_timer(SCREEN_UPDATE, current_speed)
    game_active = True
    name_system.NAME_INPUT_MODE = False


def update_speed():
    global current_speed, main_game
    new_speed = max(75, 140 - (len(main_game.snake.body) - 3) * 5)
    if new_speed != current_speed:
        current_speed = new_speed
        pygame.time.set_timer(SCREEN_UPDATE, current_speed)


clock = pygame.time.Clock()
main_game = MAIN()
pygame.time.set_timer(SCREEN_UPDATE, current_speed)

last_input_time = 0
INPUT_DELAY = 20


running = True
while running:
    current_time_ms = pygame.time.get_ticks()
    processed_action_this_frame = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

        if (
            event.type == SCREEN_UPDATE
            and game_active
            and not name_system.NAME_INPUT_MODE
        ):
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if name_system.NAME_INPUT_MODE:
                if current_time_ms - last_input_time >= INPUT_DELAY:
                    result = name_system.process_input(event.key)
                    if result:
                        last_input_time = current_time_ms
                        processed_action_this_frame = True
                        if result == "NAME_ENTERED":
                            player_name = name_system.get_name()
                            print(
                                f"Player: {player_name} | Score: {len(main_game.snake.body) - 3}"
                            )
                            reset_game()
                        elif result == "ESC_PRESSED":
                            pass
            elif game_active:
                if current_time_ms - last_input_time >= INPUT_DELAY:
                    d = main_game.snake.direction
                    action_taken_game = False
                    if event.key == pygame.K_UP and d.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                        action_taken_game = True
                    elif event.key == pygame.K_RIGHT and d.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                        action_taken_game = True
                    elif event.key == pygame.K_DOWN and d.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                        action_taken_game = True
                    elif event.key == pygame.K_LEFT and d.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                        action_taken_game = True
                    elif event.key == pygame.K_ESCAPE:
                        pass
                        action_taken_game = True

                    if action_taken_game:
                        last_input_time = current_time_ms
                        processed_action_this_frame = True
            else:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                else:
                    if not name_system.NAME_INPUT_MODE:
                        reset_game()

    if not processed_action_this_frame and (
        current_time_ms - last_input_time >= INPUT_DELAY
    ):
        button_command = read_button_input()

        if button_command:
            if name_system.NAME_INPUT_MODE:
                result = name_system.process_input(button_command)
                if result:
                    last_input_time = current_time_ms
                    if result == "NAME_ENTERED":
                        player_name = name_system.get_name()
                        print(
                            f"Player: {player_name} | Score: {len(main_game.snake.body) - 3}"
                        )
                        reset_game()
                    elif result == "ESC_PRESSED":
                        reset_game()
            elif game_active:
                d = main_game.snake.direction
                action_taken_button = False
                if button_command == "UP" and d.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                    action_taken_button = True
                elif button_command == "RIGHT" and d.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                    action_taken_button = True
                elif button_command == "DOWN" and d.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                    action_taken_button = True
                elif button_command == "LEFT" and d.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                    action_taken_button = True

                if action_taken_button:
                    last_input_time = current_time_ms
            else:
                if not name_system.NAME_INPUT_MODE:
                    reset_game()

    screen.fill((175, 215, 70))

    if name_system.NAME_INPUT_MODE:
        name_system.draw_ui(
            screen, screen_width, screen_height, cell_size, game_font, get_asset_path
        )
    elif game_active:
        main_game.draw_elements()
    else:
        screen.fill((0, 0, 0))
        try:
            go_t = pygame.font.Font(
                get_asset_path("Font/PoetsenOne-Regular.ttf"), int(cell_size * 3.0)
            )
            go_m = pygame.font.Font(
                get_asset_path("Font/PoetsenOne-Regular.ttf"), int(cell_size * 1.2)
            )
        except Exception as e:
            print(f"DEBUG: Could not load custom font. Error: {e}")
            go_t = pygame.font.SysFont("Arial", int(cell_size * 3.0))
            go_m = pygame.font.SysFont("Arial", int(cell_size * 1.2))

        ts = go_t.render("Game Over!", True, (190, 0, 0))
        isf_text = "Drücke einen Knopf zum starten"
        isf = go_m.render(isf_text, True, (200, 200, 200))

        tr = ts.get_rect(center=(screen_width / 2, screen_height / 2 - cell_size * 2.5))
        ir = isf.get_rect(
            center=(screen_width / 2, screen_height / 2 + cell_size * 1.5)
        )

        screen.blit(ts, tr)
        screen.blit(isf, ir)

    draw_direction_buttons(screen, screen_width, screen_height, cell_size)

    pygame.display.update()
    clock.tick(60)
