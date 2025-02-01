from simulation.main import MicromouseSimulation
"""
MicromouseSimulation: Main simulation class implementing micromouse competition rules
http://micromouseusa.com/wp-content/uploads/2016/04/CAMM2016Rules.pdf

Architecture:
- Pygame-based UI with resizable window
- Real-time visualization of A* pathfinding
- Interactive controls (buttons/slider) for simulation management
- Step-by-step or continuous execution modes
"""

if __name__ == "__main__":
    simulation = MicromouseSimulation()
    simulation.run()
