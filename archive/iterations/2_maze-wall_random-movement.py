import pygame
import random
import time

# --- Constants ---
WIDTH = 1000
HEIGHT = 700
MAZE_WIDTH = 20  # Number of cells in width
MAZE_HEIGHT = 15  # Number of cells in height
CELL_SIZE = 30  # Size of each cell in the maze
GUI_HEIGHT = 100  # Height of the GUI panel

FPS = 30  # Initial frames per second (controls the speed of the simulation)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)


# --- Maze generation (Recursive Backtracker) ---
def create_maze(width, height):
    maze = [["#" for _ in range(width)] for _ in range(height)]

    def carve_path(x, y):
        maze[y][x] = "."  # Mark current cell as open

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Possible moves (dx, dy)
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                maze[ny - dy // 2][nx - dx // 2] = "."  # Carve wall between cells
                carve_path(nx, ny)

    start_x = random.choice(range(1, width - 1, 2))
    start_y = random.choice(range(1, height - 1, 2))
    carve_path(start_x, start_y)

    return maze


def find_start_end(maze):
    """Finds starting (S) and ending (E) positions."""
    start = None
    end = None

    # Find start on the left side
    for y in range(len(maze)):
        if maze[y][1] == ".":
            start = (y, 0)
            maze[y][0] = "S"
            break

    # Find end on the right side
    for y in range(len(maze)):
        if maze[y][len(maze[0]) - 2] == ".":
            end = (y, len(maze[0]) - 1)
            maze[y][len(maze[0]) - 1] = "E"
            break

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
        self.moves = []  # Stack to store the path

    def update(self, maze):
        """Move the mouse using DFS (Depth-First Search)."""
        if not self.moves:  # If no planned moves, find a new move
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
                next_pos = random.choice(valid_moves)
                self.moves.append(next_pos)
                self.moves.append(self.pos)  # Add current position to backtrack

        if self.moves:
            next_pos = self.moves.pop()  # Get the next move (or backtrack)
            self.pos = next_pos
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE

    def is_valid_move(self, maze, pos):
        """Checks if a move is within bounds and not into a wall."""
        y, x = pos
        if 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] != "#":
            return True
        return False


# --- Button class ---
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()


# --- Slider class ---
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.knob_rect = pygame.Rect(x, y, 10, height)
        self.knob_rect.centerx = (
            x + (initial_val - min_val) / (max_val - min_val) * width
        )
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.knob_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                self.knob_rect.centerx = max(
                    self.rect.left, min(mouse_x, self.rect.right)
                )
                self.val = self.min_val + (
                    self.knob_rect.centerx - self.rect.left
                ) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.val


# --- Functions for button actions ---
def start_simulation():
    global simulation_running
    simulation_running = True


def stop_simulation():
    global simulation_running
    simulation_running = False


def reset_simulation():
    global maze, start, end, mouse, all_sprites, simulation_running
    maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
    start, end = find_start_end(maze)
    mouse = Mouse(start[1], start[0])
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mouse)
    simulation_running = False


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Micromouse Simulation")
clock = pygame.time.Clock()

# --- Create maze, mouse, buttons, and slider ---
maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
start, end = find_start_end(maze)
mouse = Mouse(start[1], start[0])
all_sprites = pygame.sprite.Group()
all_sprites.add(mouse)

button_start = Button(
    MAZE_WIDTH * CELL_SIZE + 20,
    20,
    100,
    40,
    "Start",
    GREEN,
    (0, 200, 0),
    start_simulation,
)
button_stop = Button(
    MAZE_WIDTH * CELL_SIZE + 20, 70, 100, 40, "Stop", RED, (200, 0, 0), stop_simulation
)
button_reset = Button(
    MAZE_WIDTH * CELL_SIZE + 20,
    120,
    100,
    40,
    "Reset",
    GRAY,
    (100, 100, 100),
    reset_simulation,
)

speed_slider = Slider(MAZE_WIDTH * CELL_SIZE + 20, 180, 200, 20, 1, 60, FPS)

buttons = [button_start, button_stop, button_reset]

simulation_running = False  # Initial state of the simulation

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_click(event)
        speed_slider.update(event)

    # --- Update ---
    if simulation_running and mouse.pos != end:
        mouse.update(maze)

    # --- Draw ---
    screen.fill(BLACK)
    # Draw maze
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

    # Draw GUI elements
    for button in buttons:
        button.draw(screen)
    speed_slider.draw(screen)

    # Display current FPS
    font = pygame.font.Font(None, 30)
    fps_text = font.render(f"FPS: {int(speed_slider.get_value())}", True, WHITE)
    screen.blit(fps_text, (MAZE_WIDTH * CELL_SIZE + 20, 220))

    pygame.display.flip()

    # --- Control the speed of the simulation ---
    clock.tick(int(speed_slider.get_value()))

pygame.quit()
