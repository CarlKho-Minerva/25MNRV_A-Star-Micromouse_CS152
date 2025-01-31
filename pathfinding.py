import heapq


def heuristic(a, end_points):
    """
    Calculates the Manhattan distance (|x1-x2| + |y1-y2|) to the nearest end point.
    This heuristic is admissible for grid movement, meaning it never overestimates.
    """
    if isinstance(end_points, tuple):
        # Single end point case
        return abs(a[0] - end_points[0]) + abs(a[1] - end_points[1])
    # Multiple end points case - take minimum distance to any end point
    return min(abs(a[0] - e[0]) + abs(a[1] - e[1]) for e in end_points)


def get_neighbors(maze, pos):
    """
    Returns list of valid adjacent cells (up, down, left, right).
    Checks bounds and wall collisions.
    """
    y, x = pos
    neighbors = []
    # Check all four directions (up, down, left, right)
    for ny, nx in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
        if (
            0 <= ny < len(maze)  # Verify y-coordinate is in bounds
            and 0 <= nx < len(maze[0])  # Verify x-coordinate is in bounds
            and maze[ny][nx] != "#"
        ):  # Check if not a wall
            neighbors.append((ny, nx))
    return neighbors


def astar(maze, start, end_points, on_step=None):
    """
    A* pathfinding implementation with support for multiple end points.

    Data structures used:
    - Priority Queue (heap): for efficiently getting lowest f-score cell
    - Dictionary (came_from): for reconstructing path
    - Dictionary (cost_so_far): for storing g-scores
    - Set (explored): for tracking visited cells

    f(n) = g(n) + h(n) where:
    - g(n) is the cost to reach node n
    - h(n) is the heuristic estimate to goal
    """
    cost_so_far = {}  # Stores g-scores (actual cost from start)
    open_set = [(0, start)]  # Priority queue of (f-score, position)
    came_from = {start: None}  # For path reconstruction
    cost_so_far[start] = 0
    explored = set()  # Track explored cells for visualization
    reached_end = None

    while open_set:
        # Get node with lowest f-score from priority queue
        current_cost, current = heapq.heappop(open_set)

        # Check if we've reached any end point
        if current in end_points:
            reached_end = current
            break

        explored.add(current)

        # Examine each neighbor of current position
        for next in get_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1  # Cost of 1 for each step

            # If new path is cheaper or first time visiting
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # Calculate f-score = g-score + h-score
                priority = new_cost + min(heuristic(next, end) for end in end_points)
                heapq.heappush(open_set, (priority, next))
                came_from[next] = current

                # Optional callback for visualization
                if on_step:
                    on_step(current, next, new_cost, priority)

    # If no path found
    if reached_end is None:
        return None, explored, cost_so_far

    # Reconstruct path from end to start
    path = []
    current = reached_end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, explored, cost_so_far
