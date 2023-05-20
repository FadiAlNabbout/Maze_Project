import numpy as np
from queue import Queue


def a_star(maze):
    start = find_start(maze)
    end = find_end(maze)
    queue = Queue()
    queue.put(start)
    visited = set()
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while not queue.empty():
        current = queue.get()

        if current == end:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            g = g_score[current] + 1
            if neighbor not in g_score or g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = g
                f_score[neighbor] = g + heuristic(neighbor, end)
                if neighbor not in visited:
                    queue.put(neighbor)
    return None


def bfs(maze):
    start = find_start(maze)
    end = find_end(maze)
    queue = Queue()
    queue.put(start)
    visited = set()
    parent = {}

    while not queue.empty():
        current = queue.get()

        if current == end:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.put(neighbor)
                parent[neighbor] = current

    return None


def dfs(maze):
    start = find_start(maze)
    end = find_end(maze)
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()

        if current == end:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    return None


def ant_colony(maze):
    # TODO: Implement Ant Colony Optimization algorithm for finding the shortest path
    pass


def find_start(maze):
    start_positions = np.argwhere(maze == 2)
    if len(start_positions) == 0:
        raise ValueError("Start position not found in the maze.")
    return tuple(start_positions[0])


def find_end(maze):
    end_positions = np.argwhere(maze == 3)
    if len(end_positions) == 0:
        raise ValueError("End position not found in the maze.")
    return tuple(end_positions[0])


def get_neighbors(position, maze):
    x, y = position
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] != 0:
            neighbors.append((nx, ny))

    return neighbors


def heuristic(current, end):
    x1, y1 = current
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(parent, current):
    path = [current]
    while current in parent:
        current = parent[current]
        path.append(current)
    path.reverse()

    return path


def verify_path(path, maze):
    # Check if the path is valid (from start to end)
    start = find_start(maze)
    end = find_end(maze)
    if path[0] != start or path[-1] != end:
        return False

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False

    return True
