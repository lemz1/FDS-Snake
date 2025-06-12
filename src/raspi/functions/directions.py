
import pygame

def draw_direction_buttons(screen, screen_width, screen_height, cell_size):
    # Höhe des unteren Rands
    margin_height = cell_size * 2
    margin_rect = pygame.Rect(0, screen_height - margin_height, screen_width, margin_height)

    # Hintergrund (schwarz)
    pygame.draw.rect(screen, (0, 0, 0), margin_rect)

    # Kästen definieren
    button_width = screen_width // 4
    button_height = margin_height - 10  # Etwas Abstand zum oberen Rand

    colors = [
        (0, 102, 255),    # Blau
        (255, 0, 0),      # Rot
        (0, 204, 0),      # Grün
        (255, 204, 0),    # Gelb
    ]

    directions = ["LEFT", "UP", "DOWN", "RIGHT"]

    for i in range(4):
        x = i * button_width + 5
        y = screen_height - button_height - 5
        rect = pygame.Rect(x, y, button_width - 10, button_height)

        # Farbfeld zeichnen
        pygame.draw.rect(screen, colors[i], rect, border_radius=10)

        # Pfeil zeichnen
        arrow_color = (255, 255, 255)
        cx, cy = rect.center
        size = cell_size * 0.6

        if directions[i] == "LEFT":
            points = [
                (cx - size, cy),  # left tip
                (cx + size, cy - size),  # top right
                (cx + size, cy + size),  # bottom right
            ]
        elif directions[i] == "UP":
            points = [
                (cx, cy - size),  # top tip
                (cx - size, cy + size),  # bottom left
                (cx + size, cy + size),  # bottom right
            ]
        elif directions[i] == "DOWN":
            points = [
                (cx, cy + size),  # bottom tip
                (cx - size, cy - size),  # top left
                (cx + size, cy - size),  # top right
            ]
        elif directions[i] == "RIGHT":
            points = [
                (cx + size, cy),  # right tip
                (cx - size, cy - size),  # top left
                (cx - size, cy + size),  # bottom left
            ]

        pygame.draw.polygon(screen, arrow_color, points)
