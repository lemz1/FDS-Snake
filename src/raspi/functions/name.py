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


def initialize_state(score_value):
    global \
        NAME_INPUT_MODE, \
        _player_name_chars_list, \
        _current_focus_index, \
        _current_score
    NAME_INPUT_MODE = True
    _player_name_chars_list = ["A"] * NAME_LENGTH
    _current_focus_index = 0
    _current_score = score_value


def process_input(input_signal):
    global \
        _current_focus_index, \
        _player_name_chars_list, \
        NAME_INPUT_MODE, \
        final_entered_name, \
        _current_score

    if not NAME_INPUT_MODE:
        return None

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
        if input_signal == "UP":
            action = "UP"
        elif input_signal == "DOWN":
            action = "DOWN"
        elif input_signal == "LEFT":
            action = "LEFT"
        elif input_signal == "RIGHT":
            action = "RIGHT"

    if action == "LEFT":
        _current_focus_index = (
            _current_focus_index - 1 + NUM_FOCUS_ITEMS
        ) % NUM_FOCUS_ITEMS
        return "ACTION_TAKEN"
    elif action == "RIGHT":
        _current_focus_index = (_current_focus_index + 1) % NUM_FOCUS_ITEMS
        return "ACTION_TAKEN"
    elif action == "UP" or action == "DOWN":
        if _current_focus_index < NAME_LENGTH:
            char_idx_in_allowed = ALLOWED_CHARS.find(
                _player_name_chars_list[_current_focus_index]
            )
            if action == "UP":
                char_idx_in_allowed = (
                    char_idx_in_allowed - 1 + len(ALLOWED_CHARS)
                ) % len(ALLOWED_CHARS)
            else:
                char_idx_in_allowed = (char_idx_in_allowed + 1) % len(ALLOWED_CHARS)
            _player_name_chars_list[_current_focus_index] = ALLOWED_CHARS[
                char_idx_in_allowed
            ]
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

    title_font_to_use = main_game_font
    char_font_to_use = main_game_font
    ok_button_font_to_use = main_game_font

    try:
        font_path = get_asset_path_func("Font/PoetsenOne-Regular.ttf")
        title_font_to_use = pygame.font.Font(font_path, int(cell_size * 1.2))
        char_font_to_use = pygame.font.Font(font_path, int(cell_size * 1.5))
        ok_button_font_to_use = pygame.font.Font(font_path, int(cell_size * 1.0))
    except (pygame.error, FileNotFoundError, TypeError):
        title_font_to_use = pygame.font.SysFont("Arial", int(cell_size * 1.2))
        char_font_to_use = pygame.font.SysFont("Arial", int(cell_size * 1.5))
        ok_button_font_to_use = pygame.font.SysFont("Arial", int(cell_size * 1.0))

    title_surf = title_font_to_use.render("Teamnamen eingeben", True, (56, 74, 12))
    title_rect = title_surf.get_rect(
        center=(screen_width / 2, screen_height / 2 - cell_size * 3.5)
    )
    screen.blit(title_surf, title_rect)

    char_width_approx = char_font_to_use.size("W")[0]
    spacing_between_chars = cell_size // 1.5
    total_name_width = (
        NAME_LENGTH * char_width_approx + (NAME_LENGTH - 1) * spacing_between_chars
    )
    ok_button_text_surf = ok_button_font_to_use.render("OK", True, (56, 74, 12))
    ok_button_width = ok_button_text_surf.get_width() + cell_size
    ok_button_spacing = spacing_between_chars * 1.5

    total_block_width = total_name_width + ok_button_spacing + ok_button_width
    start_x_pos_block = screen_width / 2 - total_block_width / 2
    current_x_offset = start_x_pos_block

    for i in range(NAME_LENGTH):
        char_surf = char_font_to_use.render(
            _player_name_chars_list[i], True, (56, 74, 12)
        )
        char_x_center_pos = current_x_offset + char_width_approx / 2
        char_y_center_pos = screen_height / 2 - cell_size * 0.5
        char_rect = char_surf.get_rect(center=(char_x_center_pos, char_y_center_pos))
        screen.blit(char_surf, char_rect)

        if i == _current_focus_index:
            underline_height = 4
            underline_rect = pygame.Rect(
                char_rect.left, char_rect.bottom + 2, char_rect.width, underline_height
            )
            pygame.draw.rect(screen, (56, 74, 12), underline_rect)
        current_x_offset += char_width_approx + spacing_between_chars

    current_x_offset -= spacing_between_chars
    current_x_offset += ok_button_spacing
    ok_button_color = (167, 209, 61)
    ok_text_color = (56, 74, 12)

    example_char_render_for_height = char_font_to_use.render("A", True, (0, 0, 0))
    ok_button_height = example_char_render_for_height.get_height() + cell_size * 0.5

    ok_button_rect_visual = pygame.Rect(
        current_x_offset,
        char_y_center_pos - ok_button_height / 2,
        ok_button_width,
        ok_button_height,
    )

    if _current_focus_index == OK_BUTTON_INDEX:
        ok_button_color = (56, 74, 12)
        ok_text_color = (220, 220, 220)
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            ok_button_rect_visual.inflate(6, 6),
            border_radius=7,
        )

    pygame.draw.rect(screen, ok_button_color, ok_button_rect_visual, border_radius=5)
    ok_button_text_surf_final = ok_button_font_to_use.render("OK", True, ok_text_color)
    ok_text_rect = ok_button_text_surf_final.get_rect(
        center=ok_button_rect_visual.center
    )
    screen.blit(ok_button_text_surf_final, ok_text_rect)
