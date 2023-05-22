import numpy as np
import random


class AntColonyOptimization:
    def __init__(self, maze, num_ants, num_iterations, alpha=1.0, beta=1.0, rho=0.5, q=5):
        self.maze = maze
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha  # Pheromone factor
        self.beta = beta    # Heuristic factor
        self.rho = rho      # Evaporation rate
        self.q = q          # Pheromone deposit quantity

        self.num_nodes = maze.size
        self.pheromone = np.ones((self.num_nodes, self.num_nodes))  # Pheromone matrix
        self.heuristic = self.calculate_heuristic()  # Heuristic matrix

    def calculate_heuristic(self):
        heuristic = np.zeros((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            x1, y1 = np.unravel_index(i, self.maze.shape)
            for j in range(self.num_nodes):
                x2, y2 = np.unravel_index(j, self.maze.shape)
                heuristic[i, j] = abs(x1 - x2) + abs(y1 - y2)
        return heuristic

    def get_neighbors(self, node):
        neighbors = []
        x, y = np.unravel_index(node, self.maze.shape)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.shape[0] and 0 <= ny < self.maze.shape[1] and self.maze[nx, ny] != 0:
                neighbors.append(np.ravel_multi_index((nx, ny), self.maze.shape))
        return neighbors

    def ant_colony_optimization(self):
        best_path = None
        best_path_length = float('inf')

        for iteration in range(self.num_iterations):
            paths = []
            path_lengths = []

            for ant in range(self.num_ants):
                path = self.construct_path()
                paths.append(path)

                path_length = self.calculate_path_length(path)
                path_lengths.append(path_length)

                if path_length < best_path_length:
                    best_path = path
                    best_path_length = path_length

            self.update_pheromone(paths, path_lengths)
            self.evaporate_pheromone()

        return best_path

    def construct_path(self):
        start = self.find_start()
        end = self.find_end()

        path = [start]
        visited = set()
        visited.add(start)

        current = start
        while current != end:
            next_node = self.select_next_node(current, visited)
            path.append(next_node)
            visited.add(next_node)
            current = next_node

        return path

    def select_next_node(self, current, visited):
        neighbors = self.get_neighbors(current)
        probabilities = self.calculate_probabilities(current, neighbors)

        if len(neighbors) == 0 or len(probabilities) == 0:
            return None

        next_node = random.choices(neighbors, probabilities, k=1)[0]
        return next_node

    def calculate_probabilities(self, current, neighbors):
        probabilities = []
        total = 0.0

        for neighbor in neighbors:
            pheromone = self.pheromone[current, neighbor]
            heuristic = self.heuristic[current, neighbor]
            probability = (pheromone ** self.alpha) * ((1.0 / heuristic) ** self.beta)
            probabilities.append(probability)
            total += probability

        probabilities = [p / total for p in probabilities]
        return probabilities

    def update_pheromone(self, paths, path_lengths):
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                delta_pheromone = 0
                for path, length in zip(paths, path_lengths):
                    if j in path:
                        path_index = path.index(j)
                        if path_index < len(path) - 1 and path[path_index + 1] == i:
                            delta_pheromone += self.q / length
                self.pheromone[i, j] = (1 - self.rho) * self.pheromone[i, j] + delta_pheromone

    def evaporate_pheromone(self):
        self.pheromone *= self.rho

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            length += self.heuristic[current, next_node]
        return length

    def find_start(self):
        indices = np.where(self.maze == 2)
        if len(indices[0]) > 0 and len(indices[1]) > 0:
            return np.ravel_multi_index((indices[0][0], indices[1][0]), self.maze.shape)
        return None

    def find_end(self):
        indices = np.where(self.maze == 3)
        if len(indices[0]) > 0 and len(indices[1]) > 0:
            return np.ravel_multi_index((indices[0][0], indices[1][0]), self.maze.shape)
        return None



# Generate a maze
maze = np.array([
    [1, 1, 1, 1, 1],
    [2, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 3],
    [1, 1, 1, 1, 1]
])

# Run Ant Colony Optimization
aco = AntColonyOptimization(maze, num_ants=5, num_iterations=10)
best_path = aco.ant_colony_optimization()
print("Best Path:", best_path)


