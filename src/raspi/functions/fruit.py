import pygame
import random
from pygame.math import Vector2
class FRUIT:
    def __init__(self, screen, cell_size, apple_image,cell_number_x, cell_number_y):
        self.screen = screen 
        self.cell_size = cell_size 
        self.apple_image = apple_image
        self.cell_number_x = cell_number_x

        self.cell_number_y = cell_number_y
        self.randomize()

    def draw_fruit(self):
        r = pygame.Rect(int(self.position.x)*self.cell_size, int(self.position.y)*self.cell_size, self.cell_size, self.cell_size)
        self.screen.blit(self.apple_image, r)

    def randomize(self):
        self.x = random.randint(0, self.cell_number_x-1)
        self.y = random.randint(0, self.cell_number_y-1)
        self.position = Vector2(self.x, self.y)

        
