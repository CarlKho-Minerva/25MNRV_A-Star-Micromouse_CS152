import pygame
from constants import (
    CELL_SIZE,
    MAZE_HEIGHT,
    MAZE_WIDTH,
    WHITE,
    WALL_COLOR,
    START_COLOR,
    END_COLOR,
    EXPLORED_COLOR,
    PATH_COLOR,
    MOUSE_COLOR,
    SHOW_NUMBERS_COLOR,
    BORDER_COLOR,
)


def draw_maze(screen, maze, maze_x, maze_y, border_width=5):
    """Draw the maze grid, walls, and border."""
    maze_rect = pygame.Rect(
        maze_x, maze_y, MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE
    )

    # Border
    outer_border = pygame.Rect(
        maze_rect.left - border_width,
        maze_rect.top - border_width,
        maze_rect.width + (2 * border_width),
        maze_rect.height + (2 * border_width),
    )
    pygame.draw.rect(screen, BORDER_COLOR, outer_border, border_width)

    # Cells
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_rect = pygame.Rect(
                maze_x + x * CELL_SIZE, maze_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            if cell == "#":
                pygame.draw.rect(screen, WALL_COLOR, cell_rect)


def draw_markers(screen, maze, maze_x, maze_y):
    """Draw start/end markers with symbols."""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell in ["S", "E"]:
                cell_rect = pygame.Rect(
                    maze_x + x * CELL_SIZE, maze_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE
                )
                color = START_COLOR if cell == "S" else END_COLOR
                pygame.draw.rect(screen, color, cell_rect)

                symbol = "S" if cell == "S" else "E"
                font = pygame.font.Font(None, int(CELL_SIZE * 0.7))
                text = font.render(symbol, True, WHITE)
                text_rect = text.get_rect(center=cell_rect.center)
                screen.blit(text, text_rect)


def draw_explored_cells(screen, explored_cells, maze_x, maze_y):
    """Draw explored cells during pathfinding."""
    for y, x in explored_cells:
        cell_rect = pygame.Rect(
            maze_x + x * CELL_SIZE, maze_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(screen, EXPLORED_COLOR, cell_rect)


def draw_path(screen, path_cells, maze_x, maze_y):
    """Draw the path taken by the mouse."""
    for y, x in path_cells:
        cell_rect = pygame.Rect(
            maze_x + x * CELL_SIZE, maze_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(screen, PATH_COLOR, cell_rect)


def draw_manhattan_distances(screen, maze, end_points, maze_x, maze_y):
    """Draw Manhattan distance numbers on cells."""
    font = pygame.font.Font(None, 20)
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] != "#":
                min_dist = min(abs(y - e[0]) + abs(x - e[1]) for e in end_points)
                text = str(min_dist)
                text_surface = font.render(text, True, SHOW_NUMBERS_COLOR)
                text_rect = text_surface.get_rect(
                    center=(
                        maze_x + (x + 0.5) * CELL_SIZE,
                        maze_y + (y + 0.5) * CELL_SIZE,
                    )
                )
                screen.blit(text_surface, text_rect)
