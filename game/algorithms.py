import numpy as np
from queue import Queue
from queue import PriorityQueue
import heapq


def dijkstra(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    pq = [(0, start)]
    visited = set()
    distances = {start: 0}
    parent = {}

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current in end_positions:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            new_cost = distances[current] + 1  # Assuming all edges have a cost of 1

            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))
                parent[neighbor] = current

    return None


def a_star(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    queue = Queue()
    queue.put(start)
    visited = set()
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end_positions, maze)}

    while not queue.empty():
        current = queue.get()

        if current in end_positions:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            g = g_score[current] + 1
            if neighbor not in g_score or g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = g
                f_score[neighbor] = g + heuristic(neighbor, end_positions, maze)
                if neighbor not in visited:
                    queue.put(neighbor)

    return None


def ucs(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    visited = set()
    distances = {start: 0}
    parent = {}

    while not priority_queue.empty():
        current_cost, current = priority_queue.get()

        if current in end_positions:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            new_cost = distances[current] + 1  # Assuming all edges have a cost of 1

            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                priority_queue.put((new_cost, neighbor))
                parent[neighbor] = current

    return None


def bfs(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    queue = Queue()
    queue.put(start)
    visited = set()
    parent = {}

    while not queue.empty():
        current = queue.get()

        if current in end_positions:
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
    end_positions = find_end(maze)
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()

        if current in end_positions:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    return None


def find_start(maze):
    start_positions = np.argwhere(maze == 2)
    if len(start_positions) == 0:
        raise ValueError("Start position not found in the maze.")
    return tuple(start_positions[0])


def find_end(maze):
    end_positions = []
    end_position_1 = np.argwhere(maze == 3.1)
    end_position_2 = np.argwhere(maze == 3.2)
    end_position_3 = np.argwhere(maze == 3.3)
    end_positions.append(end_position_1[0])
    end_positions.append(end_position_2[0])
    end_positions.append(end_position_3[0])
    if len(end_positions) == 0:
        raise ValueError("End positions not found in the maze.")
    return [tuple(position) for position in end_positions]


def get_neighbors(position, maze):
    x, y = position

    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] != 0:
            neighbors.append((nx, ny))

    return neighbors


def heuristic(current, end_positions, maze):
    x1, y1 = current
    min_distance = float('inf')
    sorted_end_positions = sorted(end_positions, key=lambda pos: maze[pos[0], pos[1]])

    for position in sorted_end_positions:
        x2, y2 = position
        distance = abs(x1 - x2) + abs(y1 - y2)

        # Consider terrain difficulty
        terrain_type = maze[x1, y1]
        if terrain_type == 4:  # Rough terrain
            distance += 3
        elif terrain_type == 5:  # Water terrain
            distance += 4

        min_distance = min(min_distance, distance)

    return min_distance


def reconstruct_path(parent, current):
    path = [current]
    while current in parent:
        current = parent[current]
        path.append(current)
    path.reverse()

    return path


def verify_path_algorithm(path, maze):
    # Check if the path is valid (from start to one of the end points)
    start = find_start(maze)
    end_positions = find_end(maze)
    if path[0] != start or path[-1] not in end_positions:
        return False

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False
        if maze[x2, y2] == 0:  # Check if the path passes through a wall
            return False

    return True
