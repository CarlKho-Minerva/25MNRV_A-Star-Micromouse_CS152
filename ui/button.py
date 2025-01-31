import pygame
from constants import WHITE


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
        self.font = pygame.font.Font(None, 28)

    def draw(self, screen):
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()
