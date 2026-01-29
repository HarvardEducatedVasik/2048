"""Utility functions and constants for 2048."""
import numpy as np
import pygame as pg

# ==================== SCREEN CONSTANTS ====================
# Auto-detect screen size and scale accordingly
def get_screen_dimensions():
    """Get appropriate screen dimensions based on display size."""
    pg.init()
    display_info = pg.display.Info()
    screen_w = display_info.current_w
    screen_h = display_info.current_h
    
    height = min(int(screen_h), 900)
    # Keep aspect ratio close to square
    width = min(int(height), 850)
    
    return height, width

SCREEN_HEIGHT, SCREEN_WIDTH = get_screen_dimensions()
TILE_GAP = 10

# ================== COLOR CONSTANTS =================
BACKGROUND_COLOR = (250, 248, 239)
SCORE_BOX_COLOR = (187, 173, 160)
GRID_BACKGROUND_COLOR = (187, 173, 160)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

TILE_TEXT_COLORS = {
    'light': (119, 110, 101),
    'dark': (249, 246, 242)
}

SCORE_TEXT_COLORS = {
    'label': (249, 246, 242),
    'number': (255, 255, 255)
}

# ================== FONT CONSTANTS ====================
LABEL_FONT_SIZE = 13
SCORE_FONT_SIZE = 22
TITLE_FONT_SIZE = 65
GAME_OVER_FONT_SIZE = 90

# ================== UI DIMENSIONS ===================
SCORE_BOX_SIZE = (140, 70)
HIGHSCORE_BOX_SIZE = (140, 70)
TITLE_BOX_SIZE = (160, 160)

UI_TOP_MARGIN = 80
BOX_SPACING = 15

# ================== GAME LOGIC ===================
def combine_line(line):
    """
    Handles the complete 2048 logic (compress, merge, compress again)
    for a single 1D numpy array (a row or column).

    Args:
        line (np.ndarray): One-dimensional numpy array (e.g., length 4).

    Returns:
        tuple: (new_line, score_gained)
            new_line (np.ndarray): Processed array with shifted and merged tiles.
            score_gained (int): Points gained from merging.
    """
    non_zero = line[line != 0]
    new_line_list = []
    score_gained = 0
    i = 0

    while i < len(non_zero):
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
            merged_value = non_zero[i] * 2
            new_line_list.append(merged_value)
            score_gained += merged_value
            i += 2
        else:
            new_line_list.append(non_zero[i])
            i += 1

    new_line_padded = np.zeros_like(line, dtype=int)
    new_line_padded[:len(new_line_list)] = new_line_list

    return new_line_padded, score_gained

# ================== COLOR FUNCTIONS =================
def get_rgb(val):
    """Legacy function - returns (background_color, font_color) tuple."""
    dic_background = {
        2: (205, 193, 180), 4: (238, 228, 218),
        8: (242, 177, 121), 16: (245, 149, 99),
        32: (246, 124, 95), 64: (246, 94, 59),
        128: (237, 207, 114), 256: (237, 204, 97),
        512: (237, 200, 80), 1024: (237, 197, 63),
        2048: (237, 194, 46)
    }
    font = (119, 110, 101) if val in [2, 4] else (249, 246, 242)
    return (dic_background.get(val, (60, 58, 50)), font)

def get_tile_color(value):
    """Return background color for a tile value."""
    return TILE_COLORS.get(value, (60, 58, 50))

def get_tile_text_color(value):
    """Return text color for a tile value."""
    return TILE_TEXT_COLORS['light'] if value <= 4 else TILE_TEXT_COLORS['dark']

# ==================== GRID DIMENSIONS ===================
def get_grid_dimensions(size):
    """Calculate grid dimensions for a given board size.

    Returns:
        tuple: (tile_size, start_x, start_y, grid_width, grid_height)
    """
    available_height = int(SCREEN_HEIGHT * 2/3)
    available_width = SCREEN_WIDTH

    max_grid_size = min(available_width, available_height) * 0.9

    tile_size = (max_grid_size - (size + 1) * TILE_GAP) / size

    grid_width = size * tile_size + (size + 1) * TILE_GAP
    grid_height = size * tile_size + (size + 1) * TILE_GAP

    start_x = (SCREEN_WIDTH - grid_width) / 2
    start_y = SCREEN_HEIGHT / 3 + (available_height - grid_height) / 2 - 50

    return tile_size, start_x, start_y, grid_width, grid_height

def get_tile_size(size):
    """Get tile size for a given board size."""
    tile_size, _, _, _, _ = get_grid_dimensions(size)
    return tile_size

# =================== UI LAYOUT ==================
def calculate_ui_layout(grid_start_x, grid_width):
    """
    Calculate positions of all UI elements.

    Args:
        grid_start_x: The x-coordinate where the grid starts
        grid_width: The width of the grid

    Returns:
        dict: Dictionary containing positions and sizes of UI elements
    """
    grid_end_x = grid_start_x + grid_width

    score_x = grid_end_x - SCORE_BOX_SIZE[0] - BOX_SPACING - HIGHSCORE_BOX_SIZE[0]
    highscore_x = grid_end_x - HIGHSCORE_BOX_SIZE[0]

    layout = {
        'title': {
            'rect': (grid_start_x, UI_TOP_MARGIN, TITLE_BOX_SIZE[0], TITLE_BOX_SIZE[1]),
            'color': get_tile_color(2048),
            'text_color': SCORE_TEXT_COLORS['number']
        },
        'score': {
            'rect': (score_x, UI_TOP_MARGIN, SCORE_BOX_SIZE[0], SCORE_BOX_SIZE[1]),
            'color': SCORE_BOX_COLOR,
            'label_color': SCORE_TEXT_COLORS['label'],
            'text_color': SCORE_TEXT_COLORS['number']
        },
        'highscore': {
            'rect': (highscore_x, UI_TOP_MARGIN, HIGHSCORE_BOX_SIZE[0], HIGHSCORE_BOX_SIZE[1]),
            'color': SCORE_BOX_COLOR,
            'label_color': SCORE_TEXT_COLORS['label'],
            'text_color': SCORE_TEXT_COLORS['number']
        }
    }

    return layout