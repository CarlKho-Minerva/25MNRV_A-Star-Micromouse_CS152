import pygame
import random

# --- Constants ---
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40  # Size of each cell in the maze
FPS = 5  # Frames per second (controls the speed of the simulation)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# --- Maze generation (simplified for now) ---
def create_maze(width, height):
    """Creates a simple maze (replace with more sophisticated generation)."""
    maze = []
    for _ in range(height):
        row = []
        for _ in range(width):
            # Simple: alternate between wall and path
            if random.random() > 0.3:  # 30% chance of being a wall
                row.append("#")
            else:
                row.append(".")
        maze.append(row)
    return maze


def find_start_end(maze):
    """Finds starting (S) and ending (E) positions."""
    start = (0, 0)
    end = (len(maze) - 2, len(maze[0]) - 2)  # Example: near bottom-right
    maze[start[0]][start[1]] = "S"
    maze[end[0]][end[1]] = "E"
    return start, end


# --- Mouse class ---
class Mouse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.pos = (y, x)

    def update(self, maze):
        """Move the mouse randomly."""
        possible_moves = [
            (self.pos[0] - 1, self.pos[1]),  # Up
            (self.pos[0] + 1, self.pos[1]),  # Down
            (self.pos[0], self.pos[1] - 1),  # Left
            (self.pos[0], self.pos[1] + 1),  # Right
        ]
        valid_moves = [
            move for move in possible_moves if self.is_valid_move(maze, move)
        ]

        if valid_moves:
            self.pos = random.choice(valid_moves)
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE

    def is_valid_move(self, maze, pos):
        """Checks if a move is within bounds and not into a wall."""
        y, x = pos
        if 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] != "#":
            return True
        return False


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Micromouse Simulation")
clock = pygame.time.Clock()

# --- Create maze and mouse ---
maze_width = WIDTH // CELL_SIZE
maze_height = HEIGHT // CELL_SIZE
maze = create_maze(maze_width, maze_height)
start, end = find_start_end(maze)
mouse = Mouse(start[1], start[0])
all_sprites = pygame.sprite.Group()
all_sprites.add(mouse)

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    if mouse.pos != end:
        mouse.update(maze)

    # --- Draw ---
    screen.fill(BLACK)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
            elif cell == "S":
                pygame.draw.rect(
                    screen,
                    GREEN,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
            elif cell == "E":
                pygame.draw.rect(
                    screen,
                    RED,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()