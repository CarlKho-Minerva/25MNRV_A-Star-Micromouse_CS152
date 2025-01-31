class GameState:
    def __init__(self):
        self.simulation_running = False
        self.show_numbers = False
        self.show_explored_cells = True
        self.current_step = False
        self.explored_cells = set()
        self.cost_so_far = {}

    def toggle_numbers(self):
        self.show_numbers = not self.show_numbers

    def toggle_explored_cells(self):
        self.show_explored_cells = not self.show_explored_cells

    def start_simulation(self):
        self.simulation_running = True
        self.current_step = False

    def stop_simulation(self):
        self.simulation_running = False

    def step_forward(self):
        self.current_step = True

    def reset(self):
        self.simulation_running = False
        self.current_step = False
        self.explored_cells.clear()
        self.cost_so_far.clear()
