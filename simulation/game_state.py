class GameState:
    """
    Manages simulation state and control flags.

    Handles:
    - Simulation running state
    - Visualization toggles
    - Step-by-step execution
    - Explored cell tracking
    - Path cost tracking

    This implementation follows micromouse simulation guidelines:
    http://micromouseusa.com/wp-content/uploads/2016/04/CAMM2016Rules.pdf
    """

    def __init__(self):
        # Core simulation states
        self.simulation_running = False  # Controls continuous execution
        self.show_numbers = False  # Toggle Manhattan distance display
        self.show_explored_cells = True  # Toggle exploration visualization
        self.current_step = False  # For step-by-step execution

        # Pathfinding data
        self.explored_cells = set()  # Track cells examined by A*
        self.cost_so_far = {}  # Track path costs to cells

    def toggle_numbers(self):
        self.show_numbers = not self.show_numbers

    def toggle_explored_cells(self):
        self.show_explored_cells = not self.show_explored_cells

    def start_simulation(self):
        self.simulation_running = True
        self.current_step = False

    def stop_simulation(self):
        self.simulation_running = False
        self.current_step = False

    def step_forward(self):
        self.simulation_running = False
        self.current_step = True

    def step_complete(self):
        self.current_step = False

    def reset(self):
        self.simulation_running = False
        self.current_step = False
        self.explored_cells.clear()
        self.cost_so_far.clear()
