import pygame


class Slider:
    def __init__(
        self, x, y, width, height, min_val, max_val, initial_val, color, slider_color
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val  # rename val to value for clarity
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
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            self.knob_rect.centerx = max(self.rect.left, min(mouse_x, self.rect.right))
            self.value = self.min_val + (
                self.knob_rect.centerx - self.rect.left
            ) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        """Get the current value of the slider."""
        return self.value
