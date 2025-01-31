import pygame
import random
import time
import heapq

# --- Constants ---
INITIAL_WIDTH = 1250
INITIAL_HEIGHT = 700
MAZE_WIDTH = 20  # Number of cells in width
MAZE_HEIGHT = 15  # Number of cells in height
CELL_SIZE = 30  # Size of each cell in the maze
GUI_WIDTH_PERCENTAGE = 0.2  # GUI panel width as a percentage of window width
LOG_HEIGHT_PERCENTAGE = 0.3  # Log panel height as a percentage of window height

FPS = 30  # Initial frames per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)  # Color for explored cells (initially)
FADE_BLUE = (60, 90, 180)  # New
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # New
GOLD = (255, 215, 0)  # New


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
                log_message(
                    f"A\*: ({current[0]},{current[1]}) -> ({next[0]},{next[1]}) - Cost: {new_cost}, Priority: {priority}",
                    DARK_GRAY,
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
        self.image.fill(BLUE)
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
        global current_step, explored_cells, fading_cells, new_log_messages
        if not self.path:
            self.path, explored = astar(maze, self.pos, end)  # Calculate path using A*
            if self.path:
                log_message("A* path found (if one exists): " + str(self.path), GOLD)
                # Visualize explored cells
                for ey, ex in explored:
                    if (ey, ex) != start and (ey, ex) != end:
                        explored_cells.add((ey, ex))
                        fading_cells.append((ey, ex, 255))
                self.path_index = 0
            else:
                log_message("No path found!", RED)

        if self.path:
            if current_step:
                # If we are stepping forward
                if self.path_index < len(self.path):
                    next_pos = self.path[self.path_index]

                    # Log the decision-making process at each step
                    neighbors = get_neighbors(maze, self.pos)
                    neighbor_costs = {}
                    for neighbor in neighbors:
                        cost = cost_so_far.get(neighbor, float("inf"))
                        priority = cost + heuristic(neighbor, end)
                        neighbor_costs[neighbor] = (cost, priority)
                        log_message(
                            f"  Neighbor ({neighbor[0]},{neighbor[1]}) - Cost: {cost}, Priority: {priority}",
                            DARK_GRAY,
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

            elif simulation_running:
                # Continuous mode
                if self.path_index < len(self.path):
                    next_pos = self.path[self.path_index]

                    # Log the decision-making process at each step
                    neighbors = get_neighbors(maze, self.pos)
                    neighbor_costs = {}
                    for neighbor in neighbors:
                        cost = cost_so_far.get(neighbor, float("inf"))
                        priority = cost + heuristic(neighbor, end)
                        neighbor_costs[neighbor] = (cost, priority)
                        log_message(
                            f"  Neighbor ({neighbor[0]},{neighbor[1]}) - Cost: {cost}, Priority: {priority}",
                            DARK_GRAY,
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

            log_message(f"Step back to ({self.pos[0]},{self.pos[1]})", DARK_GRAY)

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
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect)

        # Draw border
        pygame.draw.rect(screen, self.text_color, self.rect, 4)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
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
            if event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos()):
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
    global maze, start, end, mouse, all_sprites, simulation_running, explored_cells, current_step, log_messages, cost_so_far, fading_cells, new_log_messages
    maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
    start, end = find_start_end(maze)
    mouse = Mouse(start[1], start[0])
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mouse)
    simulation_running = False
    explored_cells = set()  # Clear explored cells
    fading_cells = []
    log_messages = []  # Clear log messages
    new_log_messages = []
    log_message("Simulation reset.", GOLD)
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
    global current_step, new_log_messages
    current_step = True
    # Append new log messages
    log_messages.extend(new_log_messages)
    new_log_messages = []


def step_backward():
    mouse.go_back()


# --- Logging function ---
def log_message(message, color):
    global new_log_messages
    new_log_messages.append((message, color))
    print(message)


# --- Pygame setup ---
pygame.init()
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

button_start = Button(
    0,
    0,
    button_width,
    button_height,
    "Start",
    GREEN,
    (0, 150, 0),
    WHITE,
    start_simulation,
)
button_stop = Button(
    0, 0, button_width, button_height, "Stop", RED, (150, 0, 0), WHITE, stop_simulation
)
button_reset = Button(
    0,
    0,
    button_width,
    button_height,
    "Reset",
    GRAY,
    (100, 100, 100),
    WHITE,
    reset_simulation,
)
button_step_forward = Button(
    0, 0, 40, button_height, ">", GRAY, (100, 100, 100), WHITE, step_forward
)
button_step_backward = Button(
    0, 0, 40, button_height, "<", GRAY, (100, 100, 100), WHITE, step_backward
)
button_numbers = Button(
    0,
    0,
    button_width,
    button_height,
    "Numbers",
    PURPLE,
    (100, 0, 100),
    WHITE,
    toggle_numbers,
)
button_explored_cells = Button(
    0,
    0,
    button_width + 40,
    button_height,
    "Explored Cells",
    PURPLE,
    (100, 0, 100),
    WHITE,
    toggle_explored_cells,
)

# --- Slider placement ---
slider_width = 200
slider_height = 20

speed_slider = Slider(0, 0, slider_width, slider_height, 1, 60, FPS, GRAY, WHITE)

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
log_messages = []  # List to store log messages
new_log_messages = []

# --- Get A* search cost information ---
cost_so_far = {}

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

    # Append new log messages if any
    if new_log_messages:
        log_messages.extend(new_log_messages)
        new_log_messages = []

    # --- Calculate sizes and positions based on current window size ---
    window_width, window_height = screen.get_size()
    gui_panel_width = int(window_width * GUI_WIDTH_PERCENTAGE)
    log_panel_height = int(window_height * LOG_HEIGHT_PERCENTAGE)
    maze_panel_width = window_width - gui_panel_width
    maze_panel_height = window_height - log_panel_height

    # --- Update button positions ---
    button_x = maze_panel_width + 20
    button_y_start = 20
    button_spacing = 50
    button_start.rect.topleft = (button_x, button_y_start)
    button_stop.rect.topleft = (button_x, button_y_start + button_spacing)
    button_reset.rect.topleft = (button_x, button_y_start + 2 * button_spacing)
    button_step_forward.rect.topleft = (
        button_x + button_width + 10,
        button_y_start + 2 * button_spacing,
    )
    button_step_backward.rect.topleft = (
        button_x + button_width + 60,
        button_y_start + 2 * button_spacing,
    )
    button_numbers.rect.topleft = (button_x, button_y_start + 3 * button_spacing)
    button_explored_cells.rect.topleft = (button_x, button_y_start + 4 * button_spacing)

    # --- Update slider position ---
    slider_x = maze_panel_width + 20
    slider_y = button_y_start + 5 * button_spacing + 20
    speed_slider.rect.topleft = (slider_x, slider_y)

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
    maze_rect = pygame.Rect(0, 0, maze_panel_width, maze_panel_height)
    # Draw outer border
    border_width = 5
    outer_border_rect = pygame.Rect(
        maze_rect.left - border_width,
        maze_rect.top - border_width,
        maze_rect.width + 2 * border_width,
        maze_rect.height + 2 * border_width,
    )
    pygame.draw.rect(screen, PURPLE, outer_border_rect, border_width)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell_rect.colliderect(maze_rect):
                if cell == "#":
                    pygame.draw.rect(screen, WHITE, cell_rect)
                elif cell == "S":
                    pygame.draw.rect(screen, GREEN, cell_rect)
                elif cell == "E":
                    pygame.draw.rect(screen, RED, cell_rect)

    # --- Draw explored cells ---
    if show_explored_cells:
        for y, x in explored_cells:
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHT_BLUE, cell_rect)

        # --- Draw fading cells ---
        for y, x, alpha in fading_cells:
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            fading_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            fading_surface.fill((FADE_BLUE[0], FADE_BLUE[1], FADE_BLUE[2], alpha))
            screen.blit(fading_surface, cell_rect)

    # --- Draw Manhattan distance numbers if toggled ---
    if show_numbers:
        font = pygame.font.Font(None, 20)
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] != "#":
                    distance = heuristic((y, x), end)
                    text_surface = font.render(str(distance), True, YELLOW)
                    text_rect = text_surface.get_rect(
                        center=((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE)
                    )
                    if text_rect.colliderect(maze_rect):
                        screen.blit(text_surface, text_rect)

    # --- Draw mouse ---
    for y, x in mouse.history:
        cell_rect = pygame.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, FADE_BLUE, cell_rect)
    if mouse.pos:
        cell_rect = pygame.Rect(
            mouse.pos[1] * CELL_SIZE,
            mouse.pos[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, BLUE, cell_rect)

    # --- GUI Panel ---
    gui_rect = pygame.Rect(
        maze_panel_width, 0, gui_panel_width, window_height - log_panel_height
    )
    pygame.draw.rect(screen, BLACK, gui_rect)

    # Draw GUI elements
    for button in buttons:
        button.draw(screen)
    speed_slider.draw(screen)

    # Display current FPS
    font = pygame.font.Font(None, 30)
    fps_text = font.render(f"FPS: {int(speed_slider.get_value())}", True, WHITE)
    fps_rect = fps_text.get_rect(topleft=(slider_x, slider_y + slider_height + 10))
    screen.blit(fps_text, fps_rect)

    # --- Log Panel ---
    log_rect = pygame.Rect(
        0,
        window_height - log_panel_height,
        window_width - gui_panel_width,
        log_panel_height,
    )
    pygame.draw.rect(screen, BLACK, log_rect)

    log_surface_height = (
        len(log_messages) * 30
    )  # Estimate height needed for all messages
    log_surface = pygame.Surface((log_rect.width, log_surface_height))
    log_surface.fill(BLACK)

    # Draw log messages
    log_y = 0
    font = pygame.font.Font(None, 30)
    for msg, color in log_messages:
        log_text = font.render(msg, True, color)
        log_text_rect = log_text.get_rect(topleft=(5, log_y))
        log_surface.blit(log_text, log_text_rect)
        log_y += log_text_rect.height

    # Scrollbar for log
    if log_surface_height > log_rect.height:
        scrollbar_x = log_rect.right - 15
        scrollbar_y = log_rect.top
        scrollbar_width = 10
        scrollbar_height = log_rect.height

        scroll_y_offset = 0

        # Handle mouse wheel event for scrolling
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            if log_rect.collidepoint(pygame.mouse.get_pos()):
                scroll_y_offset += event.y * 30

        # Clamp scroll_y_offset
        max_scroll_offset = log_surface_height - log_rect.height
        scroll_y_offset = max(0, min(scroll_y_offset, max_scroll_offset))

        # Draw scrollbar
        pygame.draw.rect(
            screen,
            DARK_GRAY,
            (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height),
        )

        # Draw visible part of log surface
        visible_log_rect = pygame.Rect(
            0, scroll_y_offset, log_rect.width, log_rect.height
        )
        screen.blit(log_surface, log_rect.topleft, visible_log_rect)

    else:
        # If no scrollbar is needed, draw the log surface normally
        screen.blit(log_surface, log_rect.topleft)

    pygame.display.flip()

    # --- Control the speed of the simulation ---
    if simulation_running and not current_step:
        clock.tick(int(speed_slider.get_value()))

pygame.quit()