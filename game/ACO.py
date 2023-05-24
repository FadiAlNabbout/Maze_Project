import random


class Ant:
    def __init__(self, maze, alpha, beta, rho):
        self.maze = maze
        self.alpha = alpha  # pheromone importance
        self.beta = beta  # heuristic information importance
        self.rho = rho  # pheromone evaporation rate
        self.num_rows = len(maze)
        self.num_cols = len(maze[0])
        self.path = []
        self.visited = set()
        self.current_position = None
        self.goal_reached = False
        self.start = self.find_start()

    def find_start(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.maze[i][j] == 2:
                    return (i, j)

    def select_next_position(self):
        row, col = self.current_position
        possible_moves = []

        # Check neighboring cells
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row, next_col = row + drow, col + dcol
            if 0 <= next_row < self.num_rows and 0 <= next_col < self.num_cols:
                cell_type = self.maze[next_row][next_col]

                if cell_type == 0 or (next_row, next_col) in self.visited:
                    continue  # Ignore walls and previously visited cells

                if cell_type == 4:
                    possible_moves.append((next_row, next_col, 3))  # Rough terrain preference
                elif cell_type == 5:
                    possible_moves.append((next_row, next_col, 1))  # Water terrain preference
                else:
                    possible_moves.append((next_row, next_col, 2))  # Normal path preference

        if not possible_moves:
            return  # No valid moves available

        # Calculate probabilities based on preferences and pheromone levels
        probabilities = []
        total_pheromone = sum(self.maze[row][col] for row, col, _ in possible_moves)

        for move in possible_moves:
            pheromone = self.maze[move[0]][move[1]]
            preference = move[2]

            probabilities.append((pheromone ** self.alpha) * (preference ** self.beta) / total_pheromone)

        # Choose next position using ACO probabilities
        selected_move = random.choices(possible_moves, probabilities)[0][:2]
        self.path.append(selected_move)
        self.current_position = selected_move
        self.visited.add(selected_move)

        if self.maze[selected_move[0]][selected_move[1]] == 3:
            self.goal_reached = True

    def update_pheromone(self, pheromone_matrix):
        path_length = len(self.path)
        pheromone_deposit = 1 / path_length

        for position in self.path:
            pheromone_matrix[position[0]][position[1]] += pheromone_deposit

    def find_path(self):
        print('Finding path...')
        self.current_position = self.start
        self.visited.add(self.start)
        self.path.append(self.start)

        while not self.goal_reached:
            self.select_next_position()

        print('Path found:', self.path)
        return self.path


class ACOAlgorithm:
    def __init__(self, maze, num_ants, num_iterations, alpha, beta, rho):
        self.maze = maze
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

    def solve(self):
        best_path = None
        best_path_length = float('inf')

        # Initialize pheromone matrix
        pheromone_matrix = [[1] * len(self.maze[0]) for _ in range(len(self.maze))]

        for _ in range(self.num_iterations):
            paths = []

            for _ in range(self.num_ants):
                ant = Ant(self.maze, self.alpha, self.beta, self.rho)
                path = ant.find_path()
                paths.append(path)

                if len(path) < best_path_length:
                    best_path = path
                    best_path_length = len(path)

                ant.update_pheromone(pheromone_matrix)

            # Update pheromone matrix by evaporation
            for i in range(len(pheromone_matrix)):
                for j in range(len(pheromone_matrix[0])):
                    pheromone_matrix[i][j] *= (1 - self.rho)

        return best_path
