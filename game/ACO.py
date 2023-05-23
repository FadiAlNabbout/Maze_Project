import numpy as np
from maze_generation import generate_maze


class Ant:
    def __init__(self, maze, pheromones, probability, rng):
        self.maze = maze
        self.pheromones = pheromones
        self.probability = probability
        self.rng = rng
        self.path = []
        self.path_length = 0

    def __str__(self):
        return f"Ant, path_length: {self.path_length}"

    def search(self):
        self.path = []
        self.path_length = 0
        start_x, start_y = np.argwhere(self.maze == 2)[0]
        self.path.append((start_x, start_y))
        current_x, current_y = start_x, start_y
        end_x, end_y = np.argwhere(self.maze == 3)[0]
        while (current_x, current_y) != (end_x, end_y):
            next_x, next_y = self.get_next_move(current_x, current_y)
            self.path.append((next_x, next_y))
            self.path_length += 1
            current_x, current_y = next_x, next_y
        #print("Destination reached!")

    def get_next_move(self, x, y):
        possible_moves = self.get_valid_moves(x, y)
        num_moves = len(possible_moves)

        selection_probability = np.zeros(num_moves)
        cumulative_prob = 0

        for i, (next_x, next_y) in enumerate(possible_moves):
            selection_probability[i] = self.probability[y, x, i]
            cumulative_prob += selection_probability[i]

        if cumulative_prob == 0:
            return possible_moves[np.random.choice(num_moves)]

        choice = self.rng.uniform(0, cumulative_prob)
        cumulative_prob = 0

        for i, (next_x, next_y) in enumerate(possible_moves):
            cumulative_prob += selection_probability[i]
            if choice < cumulative_prob:
                return next_x, next_y

        # This should not be reached, but return the last move just in case
        return possible_moves[-1]

    def is_valid_move(self, x, y):
        return (
            0 <= x < self.maze.shape[1]
            and 0 <= y < self.maze.shape[0]
            and self.maze[y, x] != 0
        )

    def get_valid_moves(self, x, y):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            if self.is_valid_move(next_x, next_y):
                moves.append((next_x, next_y))
        return moves

    def compute_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def compute_path_length(self):
        if self.path_length != 0:
            return self.path_length

        path_length = 0
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            path_length += self.compute_distance(x1, y1, x2, y2)

        return path_length


class Colony:
    def __init__(self, maze, rng, n=5, alpha=1.0, beta=2.0, rho=0.5):
        self.maze = maze
        self.rng = rng
        self.pheromones = np.ones((maze.shape[0], maze.shape[1]))
        self.ants = []
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        # Initialize ants
        self.ants = [Ant(maze, self.pheromones, self.compute_probability(), rng) for _ in range(n)]

    def compute_probability(self):
        probability = np.zeros((self.maze.shape[0], self.maze.shape[1], 4))
        for y in range(self.maze.shape[0]):
            for x in range(self.maze.shape[1]):
                if self.maze[y, x] != 0:
                    possible_moves = self.get_valid_moves(x, y)
                    num_moves = len(possible_moves)
                    for i, (next_x, next_y) in enumerate(possible_moves):
                        probability[y, x, i] = (self.pheromones[next_y, next_x] ** self.alpha) * (
                                (1.0 / self.compute_distance(x, y, next_x, next_y)) ** self.beta) / num_moves
        return probability

    def get_valid_moves(self, x, y):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            if self.is_valid_move(next_x, next_y):
                moves.append((next_x, next_y))
        return moves

    def is_valid_move(self, x, y):
        return 0 <= x < self.maze.shape[1] and 0 <= y < self.maze.shape[0] and self.maze[y, x] != 0

    def compute_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def evaporate_pheromones(self):
        self.pheromones *= (1.0 - self.rho)

    def update_pheromones(self):
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                x1, y1 = ant.path[i]
                x2, y2 = ant.path[i + 1]
                self.pheromones[y1, x1] += 1.0 / ant.compute_path_length()

    def run(self, num_iterations):
        best_path_length = np.inf
        best_ant = None
        for iteration in range(num_iterations):
            for ant in self.ants:
                ant.search()
                if ant.path_length < best_path_length:
                    best_path_length = ant.path_length
                    best_ant = ant
            self.evaporate_pheromones()
            self.update_pheromones()
            #print(f"Iteration: {iteration+1} - Best path length: {best_path_length}")
        return best_ant


maze = generate_maze(3, 3)
print(maze)
colony = Colony(maze, np.random.RandomState(0), n=3, alpha=1.0, beta=2.0, rho=0.1)
best_ant = colony.run(30)
print(best_ant.path)