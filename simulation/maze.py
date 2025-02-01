import random
from constants import MAZE_WIDTH, MAZE_HEIGHT


def create_maze(width, height):
    """
    Creates a maze using recursive backtracker algorithm.

    Algorithm steps:
    1. Start with a grid full of walls
    2. Begin at (0,0) and mark as path
    3. Recursively carve paths to unvisited neighbors
    4. Use a 2-cell spacing to ensure walls between passages
    """
    # Initialize maze with all walls (#)
    maze = [["#" for _ in range(width)] for _ in range(height)]

    # Set up starting configuration
    maze[0][0] = "."  # Start cell
    maze[0][1] = "."  # Ensure path from start
    maze[1][0] = "#"  # Wall to prevent diagonal movement

    def carve_path(x, y):
        """
        Recursive function to carve paths through the maze.
        Uses depth-first search with randomized neighbor selection.
        """
        maze[y][x] = "."  # Mark current cell as path

        # Define possible directions to move (right, down, left, up)
        # Move 2 cells at a time to maintain walls between paths
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  # Randomize direction choice

        # Try each direction
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Calculate new position
            # Check if new position is within bounds and unvisited
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                # Carve path by marking intermediate cell
                maze[ny - dy // 2][nx - dx // 2] = "."
                carve_path(nx, ny)  # Recursively continue from new position

    # Start carving from position (1,0)
    carve_path(1, 0)
    return maze


def find_start_end(maze):
    """
    Places start and end points according to micromouse competition rules:
    http://micromouseusa.com/wp-content/uploads/2016/04/CAMM2016Rules.pdf
    - Start at (0,0)
    - End points form 2x2 square in center of maze
    """
    start = (0, 0)
    maze[0][0] = "S"  # Mark start position

    # Calculate center position for 2x2 end zone
    center_y = MAZE_HEIGHT // 2 - 1
    center_x = MAZE_WIDTH // 2 - 1

    # Place end points in 2x2 square formation
    end_points = []
    for dy in range(2):
        for dx in range(2):
            y, x = center_y + dy, center_x + dx
            maze[y][x] = "E"  # Mark as end point
            end_points.append((y, x))

    # Ensure path from start is open
    maze[0][1] = "."
    return start, end_points
