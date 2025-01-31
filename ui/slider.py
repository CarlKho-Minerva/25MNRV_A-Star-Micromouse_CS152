import pygame


class Slider:
    """
    A UI component that allows users to select a value within a range by dragging a knob.
    Used for controlling simulation speed (FPS) in this application.
    """

    def __init__(
        self, x, y, width, height, min_val, max_val, initial_val, color, slider_color
    ):
        # Main slider rectangle that represents the track
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

        # Knob that users can drag - fixed width of 20 pixels for better usability
        self.knob_rect = pygame.Rect(x, y, 20, height)
        self.knob_rect.centery = 558  # Fixed vertical position
        self.knob_rect.centerx = 450  # Initial horizontal position

        self.dragging = False  # Track if user is currently dragging the knob
        self.color = color
        self.slider_color = slider_color

        # Create a slightly larger background rect for visual depth
        self.background_rect = pygame.Rect(x - 5, y - 5, width + 10, height + 10)
        self.background_color = (35, 35, 35)

    def draw(self, screen):
        """Renders the slider with a layered approach: background -> track -> knob"""
        # Draw background panel with rounded corners
        pygame.draw.rect(
            screen, self.background_color, self.background_rect, border_radius=4
        )
        # Draw the main slider track
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        # Draw the interactive knob on top
        pygame.draw.rect(screen, self.slider_color, self.knob_rect, border_radius=3)
        # Add subtle border for depth
        pygame.draw.rect(screen, (90, 90, 90), self.rect, width=1, border_radius=3)

    def update(self, event):
        """
        Handles mouse interactions with the slider.
        Maps the knob's x-position to a value between min_val and max_val.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Constrain knob movement to slider boundaries
            mouse_x = event.pos[0]
            self.knob_rect.centerx = max(self.rect.left, min(mouse_x, self.rect.right))

            # Convert knob position to value using linear interpolation
            self.value = self.min_val + (
                self.knob_rect.centerx - self.rect.left
            ) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        """Returns the current value based on knob position."""
        return self.value
