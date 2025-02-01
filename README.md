# Micromouse Simulation: A* Pathfinding in a Maze

This project implements a Micromouse simulation in Python using the Pygame library. It serves as a practical demonstration of Artificial Intelligence (AI) concepts, particularly the A\* search algorithm, applied to the classic Micromouse challenge. The simulation generates a random maze and tasks a virtual mouse with finding the optimal path from a designated starting point to the center of the maze.

This project was developed as part of the CS152 - Introduction to Artificial Intelligence course at Minerva University and fulfills the requirements of the Micromouse Challenge assignment. It demonstrates an understanding of core AI concepts, including:

* **Search Algorithms:** Implementation and evaluation of the A\* search algorithm.
* **State Space Representation:** Formal definition and implementation of a state space for the Micromouse problem.
* **Heuristic Functions:** Application of the Manhattan distance heuristic within the A\* algorithm.
* **Agent Design:** Development of a goal-based and utility-based agent for exploration and exploitation.

## Simulation Controls

* **Start:** Begins the automatic pathfinding process.
* **Stop:** Pauses the simulation.
* **Reset:** Generates a new random maze and resets the mouse.
* **Mnhtn:** Toggles the display of Manhattan distances on each cell.
* **\<:** Steps backward through the mouse's path history.
* **>:** Steps forward along the mouse's path.
* **Explored:** Toggles the display of explored cells.
* **Speed Slider:** Adjusts the simulation speed (frames per second).

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Running the Simulation](#running-the-simulation)
4. [Key Components and Algorithms](#key-components-and-algorithms)
    * [Maze Generation](#maze-generation)
    * [A\* Search Algorithm](#a-search-algorithm)
    * [State Representation](#state-representation)
    * [Mouse Movement and Actions](#mouse-movement-and-actions)
    * [User Interface](#user-interface)
5. [Assignment Requirements and Grading](#assignment-requirements-and-grading)
    * [PEAS Description](#peas-description)
    * [State Space](#state-space)
    * [Rational Behavior](#rational-behavior)
    * [Agent Program Classification](#agent-program-classification)
    * [Learning Outcomes and Holistic Competencies](#learning-outcomes-and-holistic-competencies)
6. [Simulation Controls](#simulation-controls)
7. [Future Improvements](#future-improvements)
8. [Author](#author)
9. [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

* Python 3.x
* Pygame library

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/CarlKho-Minerva/25MNRV_A-Star-Micromouse_CS152.git
    cd micromouse-simulation
    ```

    (Replace `your-username` with your actual GitHub username)

2. **Install Pygame:**

    ```bash
    pip install pygame
    ```

### Running the Simulation

To run the simulation, execute the `main.py` file:

```bash
python main.py
```

This will launch the Pygame window and start the simulation.

## Key Components and Algorithms

### Maze Generation

The maze is generated using the **recursive backtracking algorithm**, implemented in `maze.py`. This algorithm ensures a randomly generated, solvable maze that adheres to the Micromouse competition specifications.

**Key functions:**

* `create_maze(width, height)`: Generates the maze grid.
* `carve_path(x, y)`: Recursively carves paths through the maze.
* `find_start_end(maze)`: Determines the start and end points according to the rules.

### A\* Search Algorithm

The core of the simulation is the **A\* search algorithm**, implemented in `pathfinding.py`. This algorithm guides the mouse's exploration and pathfinding. It uses the **Manhattan distance** as the heuristic function to estimate the distance to the goal.

**Key functions:**

* `astar(maze, start, end_points, on_step=None)`: Implements the A\* algorithm.
* `heuristic(a, end_points)`: Calculates the Manhattan distance heuristic.
* `get_neighbors(maze, pos)`: Returns valid neighboring cells.

**Mathematical Formulation of A\*:**

A\* uses the following formula to evaluate each node:

**f(n) = g(n) + h(n)**

where:

* **f(n):** The total estimated cost of the path through node `n`.
* **g(n):** The actual cost (number of steps) to reach node `n` from the start.
* **h(n):** The estimated cost (Manhattan distance) to reach the goal from node `n`.

### State Representation

The state of the mouse is represented as a tuple: `(x, y, orientation, visited, wall_front, wall_left, wall_right)`. This is primarily managed in `entities.mouse.py` and `simulation.py`.

* `(x, y)`: Coordinates of the mouse in the maze.
* `orientation`: Direction the mouse is facing (0: North, 1: East, 2: South, 3: West).
* `visited`: A 16x16 matrix tracking visited cells.
* `wall_front`, `wall_left`, `wall_right`: Boolean values indicating the presence of walls.

### Mouse Movement and Actions

The `Mouse` class in `entities.mouse.py` handles the mouse's movement logic. The mouse can perform the following actions:

* **Move Forward:** Moves one cell forward in the current orientation (if no wall is present).
* **Turn Left:** Rotates the mouse 90 degrees counterclockwise.
* **Turn Right:** Rotates the mouse 90 degrees clockwise.

### User Interface

The `ui` directory contains classes for creating interactive UI elements using Pygame.

* `button.py`: Defines the `Button` class for creating buttons.
* `slider.py`: Defines the `Slider` class for creating sliders.
* `drawing.py`: Provides functions for drawing the maze, mouse, explored cells, path, and Manhattan distances on the screen.

## Assignment Requirements and Grading

This section maps the components of the project to the specific requirements of the Micromouse Challenge assignment, making it easier for the professor to locate and grade each part.

### PEAS Description

The PEAS (Performance, Environment, Actuators, Sensors) description of the Micromouse task environment is detailed in the project report. It can also be inferred from the code:

* **Performance:** Tracked through time and the number of unique cells visited (`simulation.py`, `game_state.py`).
* **Environment:** Defined by the generated maze (`maze.py`).
* **Actuators:** Implemented as mouse movements (`entities.mouse.py`).
* **Sensors:** Simulated through wall detection (`entities.mouse.py`, using data from `maze.py`).

### State Space

The state space is defined in the project report and implemented in the code as described in the [State Representation](#state-representation) section above.

### Rational Behavior

Rational behavior, including exploration and exploitation phases, is implemented using the A\* algorithm (`pathfinding.py`) and the mouse movement logic (`entities.mouse.py`). The `simulation.py` file manages the overall flow and switching between phases.

### Agent Program Classification

The agent program classification (model-based, goal-based during exploration, and model-based, utility-based during exploitation) is discussed in the project report. The implementation reflecting this classification can be seen in the interaction between `simulation.py`, `entities.mouse.py`, and `pathfinding.py`.

### Learning Outcomes and Holistic Competencies

The application of Learning Outcomes (cs152-aiconcepts, cs152-search) and Holistic Competencies is detailed in the Appendix of the project report. The code demonstrates these through:

* **cs152-aiconcepts:** The overall implementation of AI concepts, particularly in `pathfinding.py`, `entities.mouse.py`, and `simulation.py`.
* **cs152-search:** The implementation of the A\* algorithm in `pathfinding.py`.

## Future Improvements

* **Realistic Sensor Modeling:** Incorporate noise and limited range in sensor readings.
* **Advanced Exploration:** Implement more sophisticated exploration strategies.
* **Dynamic Obstacles:** Add support for dynamic obstacles that change during the simulation.

## Author

[Carl Kho](https://www.linkedin.com/in/carlkho/)

## Acknowledgments

* Prof Shekhar, PhD, for providing the opportunity to work on this challenging and rewarding project.
* The creators of Pygame, for developing a powerful and user-friendly library for game development.
