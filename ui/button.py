import pygame
from constants import WHITE


class Button:
    """
    Interactive button component with hover effects and visual feedback.
    Features:
    - Rounded corners for modern look
    - Hover state changes
    - Text shadow for depth
    - Border for definition
    """

    def __init__(
        self, x, y, width, height, text, color, hover_color, text_color, action
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color  # Color when mouse hovers
        self.text_color = text_color
        self.action = action  # Callback function
        self.font = pygame.font.Font(None, 28)

    def draw(self, screen):
        """
        Renders button with visual effects:
        1. Base button with hover state
        2. Rounded corners
        3. Border for depth
        4. Text with shadow effect
        """
        current_color = (
            self.hover_color
            if self.rect.collidepoint(pygame.mouse.get_pos())
            else self.color
        )

        # Draw button with rounded corners
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)

        # Border
        border_color = tuple(max(0, c - 30) for c in current_color)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=8)

        # Text with shadow
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        shadow_surface = self.font.render(self.text, True, (0, 0, 0, 128))
        shadow_rect = shadow_surface.get_rect(
            center=(text_rect.centerx + 1, text_rect.centery + 1)
        )

        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        """Handles mouse click events and triggers action callback."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()
