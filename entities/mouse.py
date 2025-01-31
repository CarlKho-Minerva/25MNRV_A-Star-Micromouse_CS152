import pygame
from constants import CELL_SIZE, MOUSE_COLOR
from pathfinding import astar


class Mouse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(MOUSE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.pos = (y, x)
        self.path = []
        self.path_index = 0
        self.history = []

    def update(self, maze, end_points, on_step=None):
        if not self.path:
            self.path, explored, cost_so_far = astar(
                maze, self.pos, end_points, on_step
            )
            return explored if self.path else None

        if self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            self.history.append(self.pos)
            self.pos = next_pos
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE
            self.path_index += 1
            return None

    def go_back(self):
        if self.history:
            self.pos = self.history.pop()
            self.rect.x = self.pos[1] * CELL_SIZE
            self.rect.y = self.pos[0] * CELL_SIZE
            self.path_index = max(0, self.path_index - 1)

    def reset(self):
        self.path = []
        self.path_index = 0
        self.history = []
