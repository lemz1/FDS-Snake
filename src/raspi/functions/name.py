import pygame
from .database import append_team

NAME_INPUT_MODE = False
ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
NAME_LENGTH = 5
_player_name_chars_list = ["A"] * NAME_LENGTH
_current_focus_index = 0
final_entered_name = ""
_current_score = 0

OK_BUTTON_INDEX = NAME_LENGTH
NUM_FOCUS_ITEMS = NAME_LENGTH + 1

_last_input_time = 0
INPUT_DELAY = 500


def initialize_state(score_value):
    global \
        NAME_INPUT_MODE, \
        _player_name_chars_list, \
        _current_focus_index, \
        _current_score, \
        _last_input_time

    NAME_INPUT_MODE = True
    _player_name_chars_list = ["A"] * NAME_LENGTH
    _current_focus_index = 0
    _current_score = score_value
    _last_input_time = pygame.time.get_ticks()  


def process_input(input_signal):
    global \
        _current_focus_index, \
        _player_name_chars_list, \
        NAME_INPUT_MODE, \
        final_entered_name, \
        _current_score, \
        _last_input_time

    if not NAME_INPUT_MODE:
        return None

    now = pygame.time.get_ticks()
    if now - _last_input_time < INPUT_DELAY:
        return None  

    _last_input_time = now

    action = None
    if isinstance(input_signal, int):
        if input_signal == pygame.K_UP:
            action = "UP"
        elif input_signal == pygame.K_DOWN:
            action = "DOWN"
        elif input_signal == pygame.K_LEFT:
            action = "LEFT"
        elif input_signal == pygame.K_RIGHT:
            action = "RIGHT"
        elif input_signal == pygame.K_RETURN:
            action = "CONFIRM_GLOBAL"
        elif input_signal == pygame.K_ESCAPE:
            action = "ESCAPE"
    elif isinstance(input_signal, str):
        if input_signal in {"UP", "DOWN", "LEFT", "RIGHT"}:
            action = input_signal

    if action == "LEFT":
        _current_focus_index = (
            _current_focus_index - 1 + NUM_FOCUS_ITEMS
        ) % NUM_FOCUS_ITEMS
        return "ACTION_TAKEN"

    elif action == "RIGHT":
        _current_focus_index = (_current_focus_index + 1) % NUM_FOCUS_ITEMS
        return "ACTION_TAKEN"

    elif action in {"UP", "DOWN"}:
        if _current_focus_index < NAME_LENGTH:
            char_idx = ALLOWED_CHARS.find(_player_name_chars_list[_current_focus_index])
            if action == "UP":
                char_idx = (char_idx - 1) % len(ALLOWED_CHARS)
            else:
                char_idx = (char_idx + 1) % len(ALLOWED_CHARS)
            _player_name_chars_list[_current_focus_index] = ALLOWED_CHARS[char_idx]
            return "ACTION_TAKEN"

        elif _current_focus_index == OK_BUTTON_INDEX:
            final_entered_name = "".join(_player_name_chars_list)
            append_team(final_entered_name, _current_score)
            NAME_INPUT_MODE = False
            return "NAME_ENTERED"

    elif action == "CONFIRM_GLOBAL":
        final_entered_name = "".join(_player_name_chars_list)
        append_team(final_entered_name, _current_score)
        NAME_INPUT_MODE = False
        return "NAME_ENTERED"

    elif action == "ESCAPE":
        NAME_INPUT_MODE = False
        return "ESC_PRESSED"

    return None


def get_name():
    return final_entered_name


def draw_ui(
    screen, screen_width, screen_height, cell_size, main_game_font, get_asset_path_func
):
    if not NAME_INPUT_MODE:
        return

    title_font = main_game_font
    char_font = main_game_font
    ok_font = main_game_font

    try:
        font_path = get_asset_path_func("Font/PoetsenOne-Regular.ttf")
        title_font = pygame.font.Font(font_path, int(cell_size * 1.2))
        char_font = pygame.font.Font(font_path, int(cell_size * 1.5))
        ok_font = pygame.font.Font(font_path, int(cell_size * 1.0))
    except (pygame.error, FileNotFoundError, TypeError):
        title_font = pygame.font.SysFont("Arial", int(cell_size * 1.2))
        char_font = pygame.font.SysFont("Arial", int(cell_size * 1.5))
        ok_font = pygame.font.SysFont("Arial", int(cell_size * 1.0))

    title_surf = title_font.render("Teamnamen eingeben", True, (56, 74, 12))
    title_rect = title_surf.get_rect(center=(screen_width / 2, screen_height / 2 - cell_size * 3.5))
    screen.blit(title_surf, title_rect)

    char_width = char_font.size("W")[0]
    spacing = cell_size // 1.5
    total_name_width = NAME_LENGTH * char_width + (NAME_LENGTH - 1) * spacing
    ok_text_surf = ok_font.render("OK", True, (56, 74, 12))
    ok_width = ok_text_surf.get_width() + cell_size
    ok_spacing = spacing * 1.5

    block_width = total_name_width + ok_spacing + ok_width
    x_start = screen_width / 2 - block_width / 2
    x_offset = x_start

    for i in range(NAME_LENGTH):
        char = _player_name_chars_list[i]
        char_surf = char_font.render(char, True, (56, 74, 12))
        char_center = (x_offset + char_width / 2, screen_height / 2 - cell_size * 0.5)
        char_rect = char_surf.get_rect(center=char_center)
        screen.blit(char_surf, char_rect)

        if i == _current_focus_index:
            underline = pygame.Rect(char_rect.left, char_rect.bottom + 2, char_rect.width, 4)
            pygame.draw.rect(screen, (56, 74, 12), underline)

        x_offset += char_width + spacing

    x_offset -= spacing
    x_offset += ok_spacing
    ok_color = (167, 209, 61)
    text_color = (56, 74, 12)

    example_height = char_font.render("A", True, (0, 0, 0)).get_height()
    ok_height = example_height + cell_size * 0.5

    ok_rect = pygame.Rect(
        x_offset,
        char_center[1] - ok_height / 2,
        ok_width,
        ok_height,
    )

    if _current_focus_index == OK_BUTTON_INDEX:
        ok_color = (56, 74, 12)
        text_color = (220, 220, 220)
        pygame.draw.rect(screen, (255, 255, 255), ok_rect.inflate(6, 6), border_radius=7)

    pygame.draw.rect(screen, ok_color, ok_rect, border_radius=5)
    ok_final_surf = ok_font.render("OK", True, text_color)
    ok_text_rect = ok_final_surf.get_rect(center=ok_rect.center)
    screen.blit(ok_final_surf, ok_text_rect)
