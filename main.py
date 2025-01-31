import pygame
from constants import init_display_constants

# Initialize pygame first
pygame.init()
# Then initialize display-dependent constants
init_display_constants()

# Now import everything else
from constants import *
from maze import create_maze, find_start_end
from pathfinding import astar, heuristic
from entities.mouse import Mouse
from ui.button import Button
from ui.slider import Slider
from ui.drawing import (
    draw_maze,
    draw_markers,
    draw_explored_cells,
    draw_path,
    draw_manhattan_distances,
)
from game_state import GameState


class MicromouseSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Micromouse Simulation")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()

        # Initialize maze and mouse
        self.maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.start, self.end_points = find_start_end(self.maze)
        self.mouse = Mouse(self.start[1], self.start[0])

        # Create UI elements
        self.create_ui_elements()

    def create_ui_elements(self):
        """Create and position UI controls."""
        self.buttons = [
            Button(
                0,
                0,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Start",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.game_state.start_simulation,
            ),
            Button(
                0,
                0,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Stop",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.game_state.stop_simulation,
            ),
            Button(
                0,
                0,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Reset",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.reset_simulation,
            ),
            Button(
                0,
                0,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Mnhtn",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.game_state.toggle_numbers,
            ),
            Button(
                0,
                0,
                40,
                BUTTON_HEIGHT,
                "<",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.step_backward,
            ),
            Button(
                0,
                0,
                40,
                BUTTON_HEIGHT,
                ">",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.step_forward,
            ),
            Button(
                0,
                0,
                BUTTON_WIDTH + 40,
                BUTTON_HEIGHT,
                "Explored",
                GRAY_MID,
                GRAY_DARK,
                WHITE,
                self.game_state.toggle_explored_cells,
            ),
        ]

        self.speed_slider = Slider(0, 0, 200, 20, 1, 60, FPS, GRAY_MID, WHITE)

    def reset_simulation(self):
        """Reset the simulation state."""
        self.maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.start, self.end_points = find_start_end(self.maze)
        self.mouse = Mouse(self.start[1], self.start[0])
        self.game_state.reset()

    def step_forward(self):
        """Process one step forward."""
        self.game_state.step_forward()
        if self.mouse.path and self.mouse.path_index < len(self.mouse.path):
            next_pos = self.mouse.path[self.mouse.path_index]
            manhattan_dist = min(heuristic(next_pos, end) for end in self.end_points)
            print(f"\nStep {self.mouse.path_index + 1}:")
            print(f"Current: {self.mouse.pos}, Moving to: {next_pos}")
            print(f"Manhattan distance to goal: {manhattan_dist}")

    def step_backward(self):
        """Process one step backward."""
        self.mouse.go_back()
        if self.mouse.history:
            print(f"\nStepped back to {self.mouse.pos}")

    def update(self):
        """Update simulation state."""
        if self.game_state.simulation_running or self.game_state.current_step:
            explored = self.mouse.update(self.maze, self.end_points)
            if explored:
                self.game_state.explored_cells.update(explored)

    def draw(self):
        """Draw the simulation."""
        self.screen.fill(BLACK)

        # Calculate layout
        window_width, window_height = self.screen.get_size()
        maze_x = (window_width - MAZE_WIDTH * CELL_SIZE) // 2
        maze_y = (window_height - CONTROL_HEIGHT - MAZE_HEIGHT * CELL_SIZE) // 2

        # Draw components
        draw_maze(self.screen, self.maze, maze_x, maze_y)
        if self.game_state.show_explored_cells:
            draw_explored_cells(
                self.screen, self.game_state.explored_cells, maze_x, maze_y
            )
        draw_path(self.screen, self.mouse.history, maze_x, maze_y)
        if self.game_state.show_numbers:
            draw_manhattan_distances(
                self.screen, self.maze, self.end_points, maze_x, maze_y
            )
        draw_markers(self.screen, self.maze, maze_x, maze_y)

        # Draw UI
        self.draw_ui(window_width, window_height)

        pygame.display.flip()

    def draw_ui(self, window_width, window_height):
        """Draw UI controls."""
        control_y = window_height - CONTROL_HEIGHT * 0.7

        # Position buttons
        total_width = sum(b.rect.width for b in self.buttons) + BUTTON_SPACING * (
            len(self.buttons) - 1
        )
        current_x = (window_width - total_width) // 2

        for button in self.buttons:
            button.rect.topleft = (current_x, control_y)
            current_x += button.rect.width + BUTTON_SPACING
            button.draw(self.screen)

        # Position and draw slider with FPS text
        slider_x = (window_width - self.speed_slider.rect.width) // 2
        slider_y = control_y + BUTTON_HEIGHT + 15
        self.speed_slider.rect.topleft = (slider_x, slider_y)
        self.speed_slider.background_rect.topleft = (slider_x - 5, slider_y - 5)

        # Draw slider and FPS in proper order
        self.speed_slider.draw(self.screen)

        # Draw FPS text
        font = pygame.font.Font(None, 30)
        fps_text = f"FPS: {int(self.speed_slider.get_value())}"
        fps_surface = font.render(fps_text, True, WHITE)
        fps_rect = fps_surface.get_rect(
            midleft=(slider_x + self.speed_slider.rect.width + 20, slider_y + 10)
        )
        self.screen.blit(fps_surface, fps_rect)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )

                for button in self.buttons:
                    button.check_click(event)
                self.speed_slider.update(event)

            self.update()
            self.draw()

            if self.game_state.simulation_running:
                self.clock.tick(int(self.speed_slider.get_value()))

        pygame.quit()


if __name__ == "__main__":
    simulation = MicromouseSimulation()
    simulation.run()
