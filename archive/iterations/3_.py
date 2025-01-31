import pygame
import random
import time
import heapq

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
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)  # Color for explored cells


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


# --- A\* Search Algorithm ---
def heuristic(a, b):
    """Calculates the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze, start, end):
    """A\* search algorithm."""
    open_set = []  # Priority queue (cost, node)
    heapq.heappush(open_set, (0, start))
    came_from = {}  # Path from start to a given node
    cost_so_far = {}  # Cost to reach a given node from start
    came_from[start] = None
    cost_so_far[start] = 0
    explored = set()  # Keep track of explored cells

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current == end:
            break

        explored.add(current)

        for next in get_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1  # Cost of a single step
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(open_set, (priority, next))
                came_from[next] = current

    # Reconstruct path
    path = []
    current = end
    while current != start:
        if current in came_from:
            path.append(current)
            current = came_from[current]
        else:
            return None, explored  # No path found

    path.append(start)
    path.reverse()
    return path, explored


def get_neighbors(maze, pos):
    """Gets the valid neighbors of a cell."""
    y, x = pos
    neighbors = []
    possible_moves = [
        (y - 1, x),
        (y + 1, x),
        (y, x - 1),
        (y, x + 1),
    ]  # Up, Down, Left, Right
    for ny, nx in possible_moves:
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#":
            neighbors.append((ny, nx))
    return neighbors


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
        self.path = []  # Path found by A*
        self.path_index = 0  # Current position on the path

    def update(self, maze, end):
        """Move the mouse along the A* path."""
        if not self.path:
            self.path, explored = astar(maze, self.pos, end)  # Calculate path using A*
            log_message("A* path found (if one exists): " + str(self.path))
            log_message("Explored nodes: " + str(explored))
            # Visualize explored cells
            for ey, ex in explored:
                if (ey, ex) != start and (ey, ex) != end:
                    explored_cells.add((ey, ex))
            if self.path:
                self.path_index = 0
            else:
                log_message("No path found!")

        if self.path and self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            self.pos = next_pos
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE
            self.path_index += 1


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
    global maze, start, end, mouse, all_sprites, simulation_running, explored_cells
    maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
    start, end = find_start_end(maze)
    mouse = Mouse(start[1], start[0])
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mouse)
    simulation_running = False
    explored_cells = set()  # Clear explored cells
    log_message("Simulation reset.")


# --- Logging function ---
def log_message(message):
    log_messages.append(message)
    if len(log_messages) > 5:  # Keep only the last 5 messages
        log_messages.pop(0)


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Micromouse Simulation")
clock = pygame.time.Clock()

# --- Create maze, mouse, buttons, slider, and explored cells set ---
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

explored_cells = set()  # Set to store explored cells for visualization
log_messages = []  # List to store log messages

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
        mouse.update(maze, end)

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

    # Draw explored cells
    for y, x in explored_cells:
        pygame.draw.rect(
            screen,
            LIGHT_BLUE,
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

    # Display log messages
    log_y = 260
    for msg in log_messages:
        log_text = font.render(msg, True, WHITE)
        screen.blit(log_text, (MAZE_WIDTH * CELL_SIZE + 20, log_y))
        log_y += 30

    pygame.display.flip()

    # --- Control the speed of the simulation ---
    clock.tick(int(speed_slider.get_value()))

pygame.quit()