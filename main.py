"""
A* Pathfinding Micromouse Simulation
Author: Carl Kho
Description: Visualizes A* pathfinding algorithm in a maze environment with step-by-step exploration
"""

import pygame
import random
import time
import heapq

# Initialize pygame first
pygame.init()

# Get display info after initialization
info = pygame.display.Info()
INITIAL_WIDTH = int(info.current_w * 0.7)  # 70% of screen width
INITIAL_HEIGHT = int(info.current_h * 0.7)  # 70% of screen height
MAZE_WIDTH = 25
MAZE_HEIGHT = 18
CELL_SIZE = min(
    INITIAL_WIDTH // (MAZE_WIDTH + 4), INITIAL_HEIGHT // (MAZE_HEIGHT + 6)
)  # More margin
CONTROL_HEIGHT = 120  # Increased for better spacing
BUTTON_SPACING = 10  # Reduced spacing between buttons
BUTTON_WIDTH = 90  # Slightly smaller buttons
BUTTON_HEIGHT = 35

# Colors - Minimalist scheme
BLACK = (18, 18, 18)  # Soft black
WHITE = (245, 245, 245)  # Soft white
GRAY_DARK = (45, 45, 45)  # Dark gray
GRAY_MID = (75, 75, 75)  # Mid gray
GRAY_LIGHT = (120, 120, 120)  # Light gray
EXPLORED_COLOR = (80, 41, 35)  # Subtle copper/orange tone
PATH_COLOR = (60, 60, 65)  # Slightly lighter for path
WALL_COLOR = (200, 200, 200)  # Soft white for walls
MOUSE_COLOR = (90, 90, 95)  # Mouse color
START_COLOR = (70, 70, 70)  # Start position
END_COLOR = (100, 100, 100)  # End position
BORDER_COLOR = (50, 50, 55)  # Border color
SHOW_NUMBERS_COLOR = (180, 180, 180)  # Light gray for numbers

FPS = 30  # Initial frames per second

# Add new global variables
show_decisions = False  # Toggle for decision logs
decision_logs = []  # Store decision logs for display


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
                if show_decisions:
                    reason = (
                        f"Chose this path because it has the lowest combined cost (distance so far + "
                        f"estimated distance to goal) of {priority}"
                    )
                    log_message(
                        f"Decision at ({current[0]},{current[1]}): Moving to ({next[0]},{next[1]}) - {reason}",
                        GRAY_LIGHT,
                    )

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
        self.image.fill(MOUSE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.pos = (y, x)
        self.path = []  # Path found by A*
        self.path_index = 0  # Current position on the path
        self.prev_pos = None  # Previous position for backtracking
        self.history = []  # Past positions

    def update(self, maze, end):
        """Move the mouse along the A* path."""
        global current_step, explored_cells, fading_cells
        if not self.path:
            self.path, explored = astar(maze, self.pos, end)  # Calculate path using A*
            if self.path:
                log_message(
                    "A* path found (if one exists): " + str(self.path), GRAY_LIGHT
                )
                # Add explored cells without fading
                for ey, ex in explored:
                    if (ey, ex) != start and (ey, ex) != end:
                        explored_cells.add((ey, ex))
            else:
                log_message("No path found!", GRAY_LIGHT)

        # Remove fading mechanism, cells stay explored
        if self.path:
            if current_step or simulation_running:
                if self.path_index < len(self.path):
                    next_pos = self.path[self.path_index]

                    # Log the decision-making process at each step
                    neighbors = get_neighbors(maze, self.pos)
                    for neighbor in neighbors:
                        cost = cost_so_far.get(neighbor, float("inf"))
                        priority = cost + heuristic(neighbor, end)
                        log_message(
                            f"  Neighbor ({neighbor[0]},{neighbor[1]}) - Cost: {cost}, Priority: {priority}",
                            GRAY_DARK,
                        )

                    chosen_cost = cost_so_far.get(next_pos, float("inf"))
                    chosen_priority = chosen_cost + heuristic(next_pos, end)
                    log_message(
                        f"  **Chosen:** ({next_pos[0]},{next_pos[1]}) - Cost: {chosen_cost}, Priority: {chosen_priority}",
                        WHITE,
                    )

                    # Update the mouse's position and add it to the history
                    self.prev_pos = self.pos
                    self.history.append(self.pos)
                    self.pos = next_pos
                    self.rect.x = self.pos[1] * CELL_SIZE
                    self.rect.y = self.pos[0] * CELL_SIZE
                    self.path_index += 1

                current_step = False

    def go_back(self):
        """Move the mouse back one step."""
        global current_step
        if self.history:
            current_step = False
            # Move the mouse back to its previous position
            self.pos = self.history.pop()
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE

            # Decrement the path index to align with the previous position
            self.path_index = max(0, self.path_index - 1)

            log_message(f"Step back to ({self.pos[0]},{self.pos[1]})", GRAY_DARK)

    def reset_path(self):
        """Resets the mouse's path and history."""
        self.path = []
        self.path_index = 0
        self.history = []


# --- Button class ---
class Button:
    def __init__(
        self, x, y, width, height, text, color, hover_color, text_color, action
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.font = pygame.font.Font(None, 28)  # Slightly smaller font
        self.padding = 2  # Padding for modern look

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        # Draw main button with rounded corners
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)

        # Modern subtle border
        border_color = tuple(
            max(0, c - 30) for c in current_color
        )  # Slightly darker than button color
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=8)

        # Text with slight shadow effect
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw subtle shadow
        shadow_surface = self.font.render(self.text, True, (0, 0, 0, 128))
        shadow_rect = shadow_surface.get_rect(
            center=(text_rect.centerx + 1, text_rect.centery + 1)
        )
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        """Check if button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()


# --- Slider class ---
class Slider:
    def __init__(
        self, x, y, width, height, min_val, max_val, initial_val, color, slider_color
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.knob_rect = pygame.Rect(x, y, 10, height)
        self.knob_rect.centerx = (
            x + (initial_val - min_val) / (max_val - min_val) * width
        )
        self.dragging = False
        self.color = color
        self.slider_color = slider_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.slider_color, self.knob_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
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
    global simulation_running, current_step
    simulation_running = True
    current_step = False
    mouse.reset_path()


def stop_simulation():
    global simulation_running
    simulation_running = False


def reset_simulation():
    global maze, start, end, mouse, all_sprites, simulation_running, explored_cells, current_step, cost_so_far, fading_cells
    maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
    start, end = find_start_end(maze)
    mouse = Mouse(start[1], start[0])
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mouse)
    simulation_running = False
    explored_cells = set()  # Clear explored cells
    fading_cells = []
    log_message("Simulation reset.", GRAY_LIGHT)
    current_step = False
    mouse.path = []
    cost_so_far = {}
    mouse.reset_path()


def toggle_numbers():
    global show_numbers
    show_numbers = not show_numbers


def toggle_explored_cells():
    global show_explored_cells
    show_explored_cells = not show_explored_cells


def step_forward():
    global current_step
    current_step = True
    # Print decision for current step
    if mouse.path and mouse.path_index < len(mouse.path):
        next_pos = mouse.path[mouse.path_index]
        cost = cost_so_far.get(next_pos, float("inf"))
        priority = cost + heuristic(next_pos, end)
        print(f"\nStep {mouse.path_index + 1}:")
        print(f"Moving to ({next_pos[0]}, {next_pos[1]})")
        print(f"Total cost: {cost}, Priority: {priority}")


def step_backward():
    global current_step
    mouse.go_back()
    # Print state after stepping back
    if mouse.history:
        print(f"\nStepped back to ({mouse.pos[0]}, {mouse.pos[1]})")
        print(f"Remaining steps: {len(mouse.path) - mouse.path_index}")


# --- Pygame setup ---
screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Micromouse Simulation")
clock = pygame.time.Clock()

# --- Create maze, mouse, buttons, slider, and explored cells set ---
maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
start, end = find_start_end(maze)
mouse = Mouse(start[1], start[0])
all_sprites = pygame.sprite.Group()
all_sprites.add(mouse)


# --- Logging function ---
def log_message(message, color):
    print(message)  # Only print to terminal, remove GUI logging


# --- Pygame setup ---
screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Micromouse Simulation")
clock = pygame.time.Clock()

# --- Create maze, mouse, buttons, slider, and explored cells set ---
maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
start, end = find_start_end(maze)
mouse = Mouse(start[1], start[0])
all_sprites = pygame.sprite.Group()
all_sprites.add(mouse)

# --- Button placement ---
button_width = 100
button_height = 40

# Update button colors when creating buttons
button_start = Button(
    0,
    0,
    button_width,
    button_height,
    "Start",
    GRAY_MID,
    GRAY_DARK,
    WHITE,
    start_simulation,
)
button_stop = Button(
    0,
    0,
    button_width,
    button_height,
    "Stop",
    GRAY_MID,
    GRAY_DARK,
    WHITE,
    stop_simulation,
)
button_reset = Button(
    0,
    0,
    button_width,
    button_height,
    "Reset",
    GRAY_MID,
    GRAY_DARK,
    WHITE,
    reset_simulation,
)
button_step_forward = Button(
    0, 0, 40, button_height, ">", GRAY_MID, GRAY_DARK, WHITE, step_forward
)
button_step_backward = Button(
    0, 0, 40, button_height, "<", GRAY_MID, GRAY_DARK, WHITE, step_backward
)
button_numbers = Button(
    0,
    0,
    button_width,
    button_height,
    "Numbers",
    GRAY_MID,
    GRAY_DARK,
    WHITE,
    toggle_numbers,
)
button_explored_cells = Button(
    0,
    0,
    button_width + 40,
    button_height,
    "Explored Cells",
    GRAY_MID,
    GRAY_DARK,
    WHITE,
    toggle_explored_cells,
)

# --- Slider placement ---
slider_width = 200
slider_height = 20

speed_slider = Slider(0, 0, slider_width, slider_height, 1, 60, FPS, GRAY_MID, WHITE)

buttons = [
    button_start,
    button_stop,
    button_reset,
    button_numbers,
    button_step_forward,
    button_step_backward,
    button_explored_cells,
]

simulation_running = False  # Initial state of the simulation
show_numbers = False  # Initial state for showing numbers
show_explored_cells = True
current_step = False

explored_cells = set()  # Set to store explored cells for visualization
fading_cells = []  # Keep track of cells to fade out

# --- Get A* search cost information ---
cost_so_far = {}


def draw_manhattan_distances(screen, maze, end, maze_x, maze_y):
    """Draw Manhattan distance numbers on the maze cells."""
    if show_numbers:  # Use the global flag
        font = pygame.font.Font(None, 20)
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] != "#":
                    distance = heuristic((y, x), end)
                    text = str(distance)
                    text_surface = font.render(text, True, SHOW_NUMBERS_COLOR)
                    text_rect = text_surface.get_rect(
                        center=(
                            maze_x + (x + 0.5) * CELL_SIZE,
                            maze_y + (y + 0.5) * CELL_SIZE,
                        )
                    )
                    screen.blit(text_surface, text_rect)


# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        for button in buttons:
            button.check_click(event)
        speed_slider.update(event)

    # --- Update ---
    if simulation_running or current_step:
        mouse.update(maze, end)

    # --- Calculate sizes and positions based on current window size ---
    window_width, window_height = screen.get_size()
    control_panel_height = CONTROL_HEIGHT
    maze_area_width = window_width
    maze_area_height = window_height - control_panel_height

    # Center maze in available space
    maze_width = MAZE_WIDTH * CELL_SIZE
    maze_height = MAZE_HEIGHT * CELL_SIZE
    maze_x = (maze_area_width - maze_width) // 2
    maze_y = (maze_area_height - maze_height) // 2

    # Control panel at bottom
    control_panel_y = window_height - control_panel_height

    # --- Draw maze ---
    maze_rect = pygame.Rect(maze_x, maze_y, maze_width, maze_height)
    # Draw outer border
    border_width = 5
    outer_border_rect = pygame.Rect(
        maze_rect.left - border_width,
        maze_rect.top - border_width,
        maze_rect.width + (2 * border_width),
        maze_rect.height + (2 * border_width)  # Added missing height parameter
    )
    pygame.draw.rect(screen, BORDER_COLOR, outer_border_rect, border_width)

    # --- Update button positions ---
    # Calculate total buttons width including spacing
    button_group_width = sum(b.rect.width for b in buttons) + BUTTON_SPACING * (len(buttons) - 1)

    # Center all controls horizontally
    start_x = (window_width - button_group_width) // 2
    controls_y = window_height - (CONTROL_HEIGHT * 0.7)  # Position controls higher in panel

    # Position buttons in a row
    current_x = start_x
    for button in buttons:
        button.rect.topleft = (current_x, controls_y)
        current_x += button.rect.width + BUTTON_SPACING

    # Position slider
    slider_width = min(300, button_group_width)  # Match buttons group width
    slider_x = (window_width - slider_width) // 2
    slider_y = controls_y + BUTTON_HEIGHT + 10
    speed_slider.rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    speed_slider.knob_rect = pygame.Rect(
        speed_slider.knob_rect.x,
        slider_y,
        10,
        slider_height
    )

    # Draw slider panel background
    slider_panel = pygame.Rect(
        slider_x - 5,
        slider_y - 5,
        slider_width + 10,
        slider_height + 25
    )
    pygame.draw.rect(screen, GRAY_DARK, slider_panel, border_radius=5)

    # --- Update fading cells ---
    for i in range(len(fading_cells) - 1, -1, -1):
        y, x, alpha = fading_cells[i]
        alpha -= 0.5  # Adjust fading speed here
        if alpha <= 0:
            fading_cells.pop(i)
            if (y, x) in explored_cells:
                explored_cells.remove((y, x))
        else:
            fading_cells[i] = (y, x, alpha)

    # --- Draw ---
    screen.fill(BLACK)

    # --- Draw maze ---
    # Create and position maze rect only once
    maze_rect = pygame.Rect(maze_x, maze_y, maze_width, maze_height)

    # Draw outer border with proper parameters
    border_width = 5
    outer_border_rect = pygame.Rect(
        maze_rect.left - border_width,
        maze_rect.top - border_width,
        maze_rect.width + (2 * border_width),
        maze_rect.height + (2 * border_width)
    )
    pygame.draw.rect(screen, BORDER_COLOR, outer_border_rect, border_width)

    # Draw maze cells
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_rect = pygame.Rect(
                maze_x + x * CELL_SIZE,
                maze_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            if cell == "#":
                pygame.draw.rect(screen, WALL_COLOR, cell_rect)
            elif cell == "S":
                pygame.draw.rect(screen, START_COLOR, cell_rect)
            elif cell == "E":
                pygame.draw.rect(screen, END_COLOR, cell_rect)

    # --- Draw explored cells ---
    if show_explored_cells:
        for y, x in explored_cells:
            cell_rect = pygame.Rect(
                maze_x + x * CELL_SIZE, maze_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, EXPLORED_COLOR, cell_rect)

    # --- Draw mouse path ---
    for y, x in mouse.history:
        cell_rect = pygame.Rect(
            maze_x + x * CELL_SIZE,
            maze_y + y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, PATH_COLOR, cell_rect)
    if mouse.pos:
        cell_rect = pygame.Rect(
            maze_x + mouse.pos[1] * CELL_SIZE,
            maze_y + mouse.pos[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, MOUSE_COLOR, cell_rect)

    # --- Control Panel ---
    control_rect = pygame.Rect(0, control_panel_y, window_width, control_panel_height)
    pygame.draw.rect(screen, BLACK, control_rect)

    # Draw numbers if enabled
    draw_manhattan_distances(screen, maze, end, maze_x, maze_y)

    # Draw GUI elements
    for button in buttons:
        button.draw(screen)
    speed_slider.draw(screen)

    # Display current FPS and decisions
    font = pygame.font.Font(None, 30)
    fps_text = f"FPS: {int(speed_slider.get_value())}"
    fps_surface = font.render(fps_text, True, WHITE)
    fps_rect = fps_surface.get_rect(topleft=(slider_x, slider_y + slider_height + 10))
    screen.blit(fps_surface, fps_rect)

    pygame.display.flip()

    # --- Control the speed of the simulation ---
    if simulation_running and not current_step:
        clock.tick(int(speed_slider.get_value()))

pygame.quit()
