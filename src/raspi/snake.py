import random
import sys
import pygame
from pygame.math import Vector2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(path):
    return os.path.join(script_dir, path)

current_speed = 100
SCREEN_UPDATE = pygame.USEREVENT
game_active = True

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def update(self):
        self.snake.move_snake()
        self.check_fruit_collision()
        self.check_fail_collision()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
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
        surf = game_font.render(s, True, (56,74,12))
        sx = int(cell_size * min(cell_number_x, cell_number_y) - cell_size * 1.5)
        sy = int(cell_size * 1.5)
        rect = surf.get_rect(center=(sx, sy))
        bg = pygame.Rect(rect.left-5, rect.top-5, rect.width+10, rect.height+10)
        pygame.draw.rect(screen, (167,209,61), bg, border_radius=5)
        screen.blit(surf, rect)
        ar = apple_image_for_score.get_rect(midright=(rect.left-10, rect.centery))
        screen.blit(apple_image_for_score, ar)
    def game_over(self):
        global game_active
        game_active = False

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.head_up     = pygame.image.load(get_asset_path('assets/head_up.png')).convert_alpha()
        self.head_down   = pygame.image.load(get_asset_path('assets/head_down.png')).convert_alpha()
        self.head_right  = pygame.image.load(get_asset_path('assets/head_right.png')).convert_alpha()
        self.head_left   = pygame.image.load(get_asset_path('assets/head_left.png')).convert_alpha()
        self.tail_up     = pygame.image.load(get_asset_path('assets/tail_up.png')).convert_alpha()
        self.tail_down   = pygame.image.load(get_asset_path('assets/tail_down.png')).convert_alpha()
        self.tail_right  = pygame.image.load(get_asset_path('assets/tail_right.png')).convert_alpha()
        self.tail_left   = pygame.image.load(get_asset_path('assets/tail_left.png')).convert_alpha()
        self.body_vertical   = pygame.image.load(get_asset_path('assets/body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(get_asset_path('assets/body_horizontal.png')).convert_alpha()
        self.body_tr = pygame.image.load(get_asset_path('assets/body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(get_asset_path('assets/body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(get_asset_path('assets/body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(get_asset_path('assets/body_bl.png')).convert_alpha()
        self.head = self.head_right
        self.tail = self.tail_left
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for i, b in enumerate(self.body):
            x = int(b.x * cell_size)
            y = int(b.y * cell_size)
            r = pygame.Rect(x, y, cell_size, cell_size)
            if i == 0:
                screen.blit(self.head, r)
            elif i == len(self.body)-1:
                screen.blit(self.tail, r)
            else:
                prev = self.body[i+1] - b
                nxt  = self.body[i-1] - b
                if prev.x == nxt.x:
                    screen.blit(self.body_vertical, r)
                elif prev.y == nxt.y:
                    screen.blit(self.body_horizontal, r)
                else:
                    if (prev.x,prev.y) in [(-1,0),(0,-1)] and (nxt.x,nxt.y) in [(-1,0),(0,-1)]:
                        screen.blit(self.body_tl, r)
                    elif (prev.x,prev.y) in [(-1,0),(0,1)] and (nxt.x,nxt.y) in [(-1,0),(0,1)]:
                        screen.blit(self.body_bl, r)
                    elif (prev.x,prev.y) in [(1,0),(0,-1)] and (nxt.x,nxt.y) in [(1,0),(0,-1)]:
                        screen.blit(self.body_tr, r)
                    else:
                        screen.blit(self.body_br, r)
    def move_snake(self):
        c = self.body[:] if self.new_block else self.body[:-1]
        c.insert(0, c[0] + self.direction)
        self.body = c
        self.new_block = False
    def add_block(self):
        self.new_block = True
    def update_head_graphics(self):
        rel = self.body[1] - self.body[0]
        if rel == Vector2(1,0):  self.head = self.head_left
        elif rel == Vector2(-1,0): self.head = self.head_right
        elif rel == Vector2(0,1):  self.head = self.head_up
        else:                      self.head = self.head_down
    def update_tail_graphics(self):
        rel = self.body[-2] - self.body[-1]
        if rel == Vector2(1,0):  self.tail = self.tail_left
        elif rel == Vector2(-1,0): self.tail = self.tail_right
        elif rel == Vector2(0,1):  self.tail = self.tail_up
        else:                      self.tail = self.tail_down

class FRUIT:
    def __init__(self):
        self.randomize()
    def draw_fruit(self):
        r = pygame.Rect(int(self.position.x)*cell_size, int(self.position.y)*cell_size, cell_size, cell_size)
        screen.blit(apple_image, r)
    def randomize(self):
        self.x = random.randint(0, cell_number_x-1)
        self.y = random.randint(0, cell_number_y-1)
        self.position = Vector2(self.x, self.y)

def reset_game():
    global main_game, game_active, current_speed
    main_game = MAIN()
    current_speed = 100
    pygame.time.set_timer(SCREEN_UPDATE, current_speed)
    game_active = True

def update_speed():
    global current_speed, main_game
    new_speed = max(30, 100 - (len(main_game.snake.body) - 3) * 5)
    if new_speed != current_speed:
        current_speed = new_speed
        pygame.time.set_timer(SCREEN_UPDATE, current_speed)
        pygame.event.post(pygame.event.Event(SCREEN_UPDATE))

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
cell_size = 30
cell_number_x = screen_width // cell_size
cell_number_y = screen_height // cell_size
clock = pygame.time.Clock()
apple_image = pygame.image.load(get_asset_path('assets/apple.png')).convert_alpha()
apple_image_for_score = pygame.transform.scale(apple_image, (int(cell_size*0.8), int(cell_size*0.8)))
try:
    game_font = pygame.font.Font(get_asset_path('Font/PoetsenOne-Regular.ttf'), int(cell_size*0.8))
except pygame.error:
    game_font = pygame.font.SysFont("Arial", int(cell_size*0.8))
main_game = MAIN()
pygame.time.set_timer(SCREEN_UPDATE, current_speed)
last_input_time = 0
INPUT_DELAY = 60

running = True
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN and now - last_input_time >= INPUT_DELAY:
                last_input_time = now
                d = main_game.snake.direction
                if event.key == pygame.K_UP and d.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
                elif event.key == pygame.K_RIGHT and d.x != -1:
                    main_game.snake.direction = Vector2(1,0)
                elif event.key == pygame.K_DOWN and d.y != -1:
                    main_game.snake.direction = Vector2(0,1)
                elif event.key == pygame.K_LEFT and d.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        else:
            if event.type == pygame.KEYDOWN:
                reset_game()

    screen.fill((175,215,70))
    if game_active:
        main_game.draw_elements()
    else:
        try:
            go_t = pygame.font.Font(get_asset_path('Font/playthings/Playthings.ttf'), int(cell_size*1.5))
            go_m = pygame.font.Font(get_asset_path('Font/playthings/Playthings.ttf'), int(cell_size*0.9))
        except pygame.error:
            go_t = pygame.font.SysFont("Arial", int(cell_size*1.5))
            go_m = pygame.font.SysFont("Arial", int(cell_size*0.9))
        ts = go_t.render("Game Over!", True, (190,0,0))
        isf = go_m.render("Press any key to restart", True, (56,74,12))
        tr = ts.get_rect(center=(screen_width/2, screen_height/2 - cell_size*1.2))
        ir = isf.get_rect(center=(screen_width/2, screen_height/2 + cell_size*0.8))
        screen.blit(ts, tr)
        screen.blit(isf, ir)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
