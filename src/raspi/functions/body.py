import pygame
from pygame.math import Vector2
from .get_asset_path import get_asset_path
import json
import asyncio
import websockets

def send_position_to_server(pos):
    async def send():
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                # Convert the list of tuples to a JSON string to send it
                await websocket.send(json.dumps(pos))
        except ConnectionRefusedError:
            # This will happen if the server isn't running.
            # We'll just ignore it so the game doesn't crash.
            pass
    # Run the async function
    asyncio.run(send())
class SNAKE:
    def __init__(self ,screen, cell_size):
        self.screen = screen 
        self.cell_size = cell_size
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
            x = int(b.x * self.cell_size)
            y = int(b.y * self.cell_size)
            r = pygame.Rect(x, y, self.cell_size, self.cell_size)
            if i == 0:
                self.screen.blit(self.head, r)
            elif i == len(self.body)-1:
                self.screen.blit(self.tail, r)
            else:
                prev = self.body[i+1] - b
                nxt  = self.body[i-1] - b
                if prev.x == nxt.x:
                    self.screen.blit(self.body_vertical, r)
                elif prev.y == nxt.y:
                    self.screen.blit(self.body_horizontal, r)
                else:
                    if (prev.x,prev.y) in [(-1,0),(0,-1)] and (nxt.x,nxt.y) in [(-1,0),(0,-1)]:
                        self.screen.blit(self.body_tl, r)
                    elif (prev.x,prev.y) in [(-1,0),(0,1)] and (nxt.x,nxt.y) in [(-1,0),(0,1)]:
                        self.screen.blit(self.body_bl, r)
                    elif (prev.x,prev.y) in [(1,0),(0,-1)] and (nxt.x,nxt.y) in [(1,0),(0,-1)]:
                        self.screen.blit(self.body_tr, r)
                    else:
                        self.screen.blit(self.body_br, r)


    def move_snake(self, cell_num_x, cell_num_y):
        c = self.body[:] if self.new_block else self.body[:-1]
    

        temp_vector = c[0] + self.direction
        temp_vector.x = temp_vector.x % cell_num_x
        temp_vector.y = temp_vector.y % cell_num_y


        c.insert(0, temp_vector)

        self.body = c
        self.new_block = False

        pos_to_send = [[int(vec.x), int(vec.y)] for vec in self.body]
        send_position_to_server(pos_to_send)



    def add_block(self):
        self.new_block = True

    def update_head_graphics(self):
        rel = self.body[1] - self.body[0]
        
        if rel.x > 1:
            rel.x = -1
        elif rel.x < - 1:
            rel.x = 1
        
        if rel.y > 1:
            rel.y = -1
        elif rel.y < -1:
            rel.y = 1

        if rel == Vector2(1, 0):  
            self.head = self.head_left
        elif rel == Vector2(-1, 0): 
            self.head = self.head_right
        elif rel == Vector2(0, 1):
            self.head = self.head_up
        elif rel == Vector2(0, -1):
            self.head = self.head_down
        else:
            self.head = self.head_down
            pass

    def update_tail_graphics(self):
        rel = self.body[-2] - self.body[-1]

        if rel.x > 1:
            rel.x = -1
        elif rel.x < - 1:
            rel.x = 1
        
        if rel.y > 1:
            rel.y = -1
        elif rel.y < -1:
            rel.y = 1

        if rel == Vector2(1, 0):  
            self.tail = self.tail_left
        elif rel == Vector2(-1, 0): 
            self.tail = self.tail_right
        elif rel == Vector2(0, 1): 
            self.tail = self.tail_up
        elif rel == Vector2(0, -1):
            self.tail = self.tail_down
        else:
            self.tail = self.tail_down
            pass

    def get_body_as_json(self):
        positions = [(int(seg.x), int(seg.y)) for seg in self.body]
        return json.dumps({"snake": positions})

