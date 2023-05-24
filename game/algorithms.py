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
            edge_cost = get_edge_cost(current, neighbor, maze)
            new_cost = distances[current] + edge_cost

            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))
                parent[neighbor] = current

    return None


def a_star(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end_positions, maze)}

    while not queue.empty():
        current_cost, current = queue.get()

        if current in end_positions:
            return reconstruct_path(parent, current)

        visited.add(current)

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            edge_cost = get_edge_cost(current, neighbor, maze)
            g = g_score[current] + edge_cost
            if neighbor not in g_score or g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = g
                f_score[neighbor] = g + heuristic(neighbor, end_positions, maze)
                if neighbor not in visited:
                    queue.put((f_score[neighbor], neighbor))

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
            edge_cost = get_edge_cost(current, neighbor, maze)
            new_cost = distances[current] + edge_cost

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
            edge_cost = get_edge_cost(current, neighbor, maze)
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
            edge_cost = get_edge_cost(current, neighbor, maze)
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    return None


def get_valid_neighbors(position, maze, visited):
    x, y = position

    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (
                0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] != 0
                and (nx, ny) not in visited
        ):
            neighbors.append((nx, ny))

    return neighbors


def iddfs(maze):
    start = find_start(maze)
    end_positions = find_end(maze)
    max_depth = maze.shape[0] * maze.shape[1]  # Maximum possible depth of the maze

    for depth_limit in range(max_depth + 1):
        visited = set()
        path = dfs_recursive(start, end_positions, maze, depth_limit, visited)
        if path is not None:
            return path

    return None


def dfs_recursive(current, end_positions, maze, depth_limit, visited):
    if current in end_positions:
        return [current]

    if depth_limit == 0:
        return None

    visited.add(current)

    neighbors = get_valid_neighbors(current, maze, visited)

    for neighbor in neighbors:
        path = dfs_recursive(neighbor, end_positions, maze, depth_limit - 1, visited)
        if path is not None:
            return [current] + path

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


def get_edge_cost(position1, position2, maze):
    terrain_type1 = maze[position1]
    terrain_type2 = maze[position2]

    if terrain_type1 == 4 or terrain_type2 == 4:  # Rough terrain
        return 2
    elif terrain_type1 == 5 or terrain_type2 == 5:  # Water terrain
        return 3
    else:
        return 1


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
