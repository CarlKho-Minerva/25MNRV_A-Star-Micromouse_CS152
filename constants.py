import pygame

# Core constants (no pygame dependency)
MAZE_WIDTH = 16
MAZE_HEIGHT = 16
CENTER_GOAL_SIZE = 2
CONTROL_HEIGHT = 120
BUTTON_SPACING = 10
BUTTON_WIDTH = 90
BUTTON_HEIGHT = 35
FPS = 30

# Colors
BLACK = (18, 18, 18)
WHITE = (245, 245, 245)
GRAY_DARK = (45, 45, 45)
GRAY_MID = (75, 75, 75)
GRAY_LIGHT = (120, 120, 120)
EXPLORED_COLOR = (80, 41, 35)
PATH_COLOR = (60, 60, 65)
WALL_COLOR = (200, 200, 200)
MOUSE_COLOR = (90, 90, 95)
START_COLOR = (67, 160, 71)
END_COLOR = (121, 40, 40)
BORDER_COLOR = (50, 50, 55)
SHOW_NUMBERS_COLOR = (180, 180, 180)

# Display-dependent constants will be set after pygame init
INITIAL_WIDTH = None
INITIAL_HEIGHT = None
CELL_SIZE = None


def init_display_constants():
    """Initialize constants that depend on display info."""
    global INITIAL_WIDTH, INITIAL_HEIGHT, CELL_SIZE

    info = pygame.display.Info()
    INITIAL_WIDTH = int(info.current_w * 0.7)
    INITIAL_HEIGHT = int(info.current_h * 0.7)
    CELL_SIZE = min(
        INITIAL_WIDTH // (MAZE_WIDTH + 4), INITIAL_HEIGHT // (MAZE_HEIGHT + 6)
    )
