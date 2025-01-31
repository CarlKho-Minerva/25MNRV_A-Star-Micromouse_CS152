"""
Micromouse Simulation
====================

A Python implementation of a Micromouse maze-solving simulation using A* pathfinding.
Based on official Micromouse competition rules:
http://micromouseusa.com/wp-content/uploads/2016/04/CAMM2016Rules.pdf

Purpose:
--------
Simulates a robotic mouse finding the optimal path through a maze using A* algorithm,
with real-time visualization and interactive controls for educational purposes.

Usage:
------
Run this file to start the simulation. Controls:
- Start: Begin automatic pathfinding
- Stop: Pause simulation
- Reset: Generate new maze
- Mnhtn: Toggle Manhattan distance display
- < >: Step backward/forward
- Explored: Toggle visited cells visibility
- Slider: Adjust simulation speed

Architecture Components:
----------------------
- Maze Generation: Recursive backtracker algorithm
- Pathfinding: A* with Manhattan distance heuristic
- Visualization: Pygame-based UI with real-time updates
- State Management: Centralized game state control
- Entity System: Sprite-based mouse movement
- UI Components: Interactive buttons and slider

Author: Carl Kho
Date: January 31, 2025
"""

import pygame
from constants import init_display_constants
from simulation.manager import MicromouseSimulation


def main():
    pygame.init()
    init_display_constants()
    simulation = MicromouseSimulation()
    simulation.run()


if __name__ == "__main__":
    main()
