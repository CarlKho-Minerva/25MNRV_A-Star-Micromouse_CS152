# Algorithm 1: Micromouse Agent Program (Exploration and Pathfinding)

## Input
- Maze grid
- Start position
- Goal positions

## Output
- Path to goal (if found)
- Explored cells

## Functions
- `sense_walls()`: Returns `[front_wall, left_wall, right_wall]` (boolean - wall detected?)
- `move_forward()`: Actuates motors to move one cell forward
- `turn_left()`: Actuates motors to turn 90 degrees left
- `turn_right()`: Actuates motors to turn 90 degrees right
- `mark_cell_visited(position)`: Marks a cell as visited in the internal map
- `is_cell_visited(position)`: Checks if a cell has been visited
- `get_current_position()`: Returns current (y, x) grid position
- `set_current_position(position)`: Sets current (y, x) grid position
- `update_current_position_forward()`: Updates position after moving forward
- `get_current_orientation()`: Returns current orientation (North, East, South, West)
- `choose_next_direction(walls, current_orientation, current_position)`: Decides next exploration direction

## Data Structures
- `maze_map`: Internal representation of the maze (initially unknown)
- `path_stack`: Stack to track path during exploration (for backtracking)
- `explored_cells`: Set to keep track of visited cells for visualization

## Algorithm Steps
1. `initialize_maze_map()`
2. `current_position = start_position`
3. `current_orientation = North`
4. `mark_cell_visited(current_position)`
5. `path_stack = [current_position]`
6. while path_stack is not empty:
    1. `current_position = get_current_position()`
    2. `current_orientation = get_current_orientation()`
    3. `walls = sense_walls()`  // Get wall sensor readings
    4. `next_direction = choose_next_direction(walls, current_orientation, current_position)`
    5. if next_direction is not None: // Unvisited path found
        1. if next_direction is Forward:
            1. if not walls[0]: `move_forward()`; `update_current_position_forward()`
        2. else if next_direction is Left:
            1. `turn_left()`; if not walls[1]: `move_forward()`; `update_current_position_forward()`
        3. else if next_direction is Right: // next_direction is Right
            1. `turn_right()`; if not walls[2]: `move_forward()`; `update_current_position_forward()`
        4. `mark_cell_visited(get_current_position())`
        5. `path_stack.append(get_current_position())`
    6. else: // No unvisited neighbors: Backtrack
        1. if path_stack has more than one cell:
            1. `path_stack.pop()`; `set_current_position(path_stack[-1])`
        2. else: break // Back at start, exploration complete
7. // --- Pathfinding (A* Algorithm) ---
8. `path, explored_cells, cost_so_far = A*(maze_map, start_position, goal_positions)`
9. return path, explored_cells

