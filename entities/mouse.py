import pygame
from constants import CELL_SIZE, MOUSE_COLOR
from simulation.pathfinding import astar


class Mouse(pygame.sprite.Sprite):
    """
    Mouse entity that navigates the maze using A* pathfinding.
    Inherits from pygame.sprite.Sprite for rendering and collision detection.
    Implements movement, path tracking, and backtracking capabilities.
    """

    def __init__(self, x, y):
        """
        Initialize mouse with starting position and visual representation.
        Args:
            x: Starting X coordinate in grid cells
            y: Starting Y coordinate in grid cells
        """
        super().__init__()
        # Visual representation setup
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(MOUSE_COLOR)
        self.rect = self.image.get_rect()

        # Position in pixels (for rendering)
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

        # Position in grid coordinates (y, x) format for pathfinding
        self.pos = (y, x)

        # Path tracking variables
        self.path = []  # List of positions to follow
        self.path_index = 0  # Current position in path
        self.history = []  # Stack of previous positions for backtracking
        self.has_explored = False  # Add this line to track exploration state

    def update(self, maze, end_points, on_step=None):
        """Updates mouse position and pathfinding."""
        # Initial A* search if needed
        if not self.path and not self.has_explored:
            self.path, explored, cost_so_far = astar(maze, self.pos, end_points, on_step)
            self.has_explored = True
            if self.path:
                self.history = [self.pos]  # Initialize history with start position
            return explored if self.path else None

        # Handle movement separately
        if self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            self.pos = next_pos
            self.history.append(self.pos)  # Add new position to history
            # Update visual position
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE
            self.path_index += 1

        return None

    def go_back(self):
        """
        Move mouse back one step using position history.
        Updates both grid position and visual representation.
        """
        if self.history:
            self.history.pop()  # Remove current position
            self.pos = self.history[-1] if self.history else self.path[0]
            # Update visual position
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE
            self.path_index = max(0, self.path_index - 1)

    def reset(self):
        """Clear all path-related data to initial state."""
        self.path = []
        self.path_index = 0
        self.history = []
        self.has_explored = False  # Add this line to reset exploration state

    def reset_position(self):
        if self.path:
            self.pos = self.path[0]
            self.path_index = 0
            self.history = [self.pos]
