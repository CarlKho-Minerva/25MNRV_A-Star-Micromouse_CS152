import heapq


def heuristic(a, end_points):
    """Calculate Manhattan distance to nearest end point."""
    if isinstance(end_points, tuple):
        return abs(a[0] - end_points[0]) + abs(a[1] - end_points[1])
    return min(abs(a[0] - e[0]) + abs(a[1] - e[1]) for e in end_points)


def get_neighbors(maze, pos):
    """Get valid neighboring cells."""
    y, x = pos
    neighbors = []
    for ny, nx in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#":
            neighbors.append((ny, nx))
    return neighbors


def astar(maze, start, end_points, on_step=None):
    """A* pathfinding algorithm with multiple end points."""
    cost_so_far = {}
    open_set = [(0, start)]
    came_from = {start: None}
    cost_so_far[start] = 0
    explored = set()
    reached_end = None

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current in end_points:
            reached_end = current
            break

        explored.add(current)

        for next in get_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + min(heuristic(next, end) for end in end_points)
                heapq.heappush(open_set, (priority, next))
                came_from[next] = current

                if on_step:
                    on_step(current, next, new_cost, priority)

    if reached_end is None:
        return None, explored, cost_so_far

    path = []
    current = reached_end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, explored, cost_so_far
