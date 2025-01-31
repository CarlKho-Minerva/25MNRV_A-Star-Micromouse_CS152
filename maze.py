import random
from constants import MAZE_WIDTH, MAZE_HEIGHT


def create_maze(width, height):
    """Creates a maze using recursive backtracker algorithm."""
    maze = [["#" for _ in range(width)] for _ in range(height)]

    # Configure start position
    maze[0][0] = "."
    maze[0][1] = "."
    maze[1][0] = "#"

    def carve_path(x, y):
        maze[y][x] = "."
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                maze[ny - dy // 2][nx - dx // 2] = "."
                carve_path(nx, ny)

    carve_path(1, 0)
    return maze


def find_start_end(maze):
    """Places start and end points according to competition rules."""
    start = (0, 0)
    maze[0][0] = "S"

    center_y = MAZE_HEIGHT // 2 - 1
    center_x = MAZE_WIDTH // 2 - 1

    end_points = []
    for dy in range(2):
        for dx in range(2):
            y, x = center_y + dy, center_x + dx
            maze[y][x] = "E"
            end_points.append((y, x))

    maze[0][1] = "."
    return start, end_points
