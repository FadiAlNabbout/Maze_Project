import random
import numpy as np


class Ant:
    def __init__(self, maze, aco):
        self.maze = maze
        self.path = []
        self.aco = aco
        self.current_position = self.get_start_position()

    def get_start_position(self):
        start_positions = np.where(self.maze == 2)
        return tuple((start_positions[0][0], start_positions[1][0]))

    def get_possible_moves(self, position):
        row, col = position
        possible_moves = []

        # Check the four adjacent positions: up, down, left, right
        # Add valid moves to the list of possible moves
        if row - 1 >= 0 and self.maze[row - 1][col] != 0:
            possible_moves.append((row - 1, col))
        if row + 1 < len(self.maze) and self.maze[row + 1][col] != 0:
            possible_moves.append((row + 1, col))
        if col - 1 >= 0 and self.maze[row][col - 1] != 0:
            possible_moves.append((row, col - 1))
        if col + 1 < len(self.maze[row]) and self.maze[row][col + 1] != 0:
            possible_moves.append((row, col + 1))

        return possible_moves

    def move(self):
        possible_moves = self.get_possible_moves(self.current_position)

        attractiveness_values = [
            self.aco.get_attractiveness(move) for move in possible_moves
        ]
        total_attractiveness = sum(attractiveness_values)
        probabilities = [
            attractiveness / total_attractiveness for attractiveness in attractiveness_values
        ]

        chosen_move = random.choices(possible_moves, probabilities)[0]

        self.current_position = chosen_move
        self.path.append(chosen_move)


class ACO:
    def __init__(self, maze, num_ants, evaporation_rate, alpha, beta):
        self.maze = maze
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromone = self.initialize_pheromone()

    def initialize_pheromone(self):
        # Initialize the pheromone trails in the maze with initial intensity values
        pheromone = np.ones(self.maze.shape, dtype=float)
        pheromone[self.maze == 0] = 0  # Set pheromone on walls (0) to 0
        return pheromone

    def update_pheromone_trails(self, ants):
        # Evaporate pheromone trails
        self.pheromone *= (1 - self.evaporation_rate)

        # Update pheromone trails based on ant paths
        for ant in ants:
            path_length = self.calculate_path_length(ant.path)
            pheromone_deposit = 1 / path_length
            for i in range(len(ant.path) - 1):
                current_pos = ant.path[i]
                next_pos = ant.path[i + 1]
                self.pheromone[current_pos, next_pos] += pheromone_deposit

    def evaporate_pheromone(self):
        self.pheromone *= (1 - self.evaporation_rate)

    def get_attractiveness(self, move):
        terrain_type = self.maze[move]
        if terrain_type == 1:  # Normal terrain
            return 1
        elif terrain_type == 4:  # Rough terrain
            return 2
        elif terrain_type == 5:  # Water terrain
            return 0.1
        else:
            return 1

    def solve(self, num_iterations):
        start_position = np.where(self.maze == 2)
        start_position = list(zip(start_position[0], start_position[1]))[0]
        ants = [Ant(self.maze, self) for _ in range(self.num_ants)]

        for _ in range(num_iterations):
            for ant in ants:
                ant.move()

            self.update_pheromone_trails(ants)
            self.evaporate_pheromone()

        best_path = max(ants, key=lambda ant: self.calculate_path_length(ant.path)).path

        return best_path

    def calculate_path_length(self, path):
        # Calculate the length of a given path in the maze
        return len(path)





