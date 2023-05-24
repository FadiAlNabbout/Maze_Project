import random
import numpy as np
from maze_generation import generate_maze


class Ant:
    def __init__(self, maze, starting_position, aco):
        self.maze = maze
        self.path = []
        self.aco = aco
        self.current_position = starting_position
        self.path.append(starting_position)

    def get_possible_moves(self, position):
        row, col = position
        possible_moves = []

        # Check the four adjacent positions: up, down, left, right
        # Add valid moves to the list of possible moves
        if row - 1 >= 0 and self.maze[row - 1][col] != 0 and ((row - 1, col) != self.path[-1]):
            possible_moves.append((row - 1, col))
        if row + 1 < len(self.maze) and self.maze[row + 1][col] != 0 and ((row + 1, col) != self.path[-1]):
            possible_moves.append((row + 1, col))
        if col - 1 >= 0 and self.maze[row][col - 1] != 0 and ((row, col - 1) != self.path[-1]):
            possible_moves.append((row, col - 1))
        if col + 1 < len(self.maze[row]) and self.maze[row][col + 1] != 0 and ((row, col + 1) != self.path[-1]):
            possible_moves.append((row, col + 1))

        return possible_moves

    def move(self):
        possible_moves = self.get_possible_moves(self.current_position)

        attractiveness_values = [self.aco.get_attractiveness(move) for move in possible_moves]
        total_attractiveness = sum(attractiveness_values)
        probabilities = [attractiveness / total_attractiveness for attractiveness in attractiveness_values]

        chosen_move = random.choices(possible_moves, probabilities)[0]

        self.current_position = chosen_move
        self.path.append(chosen_move)

        if self.maze[chosen_move[0]][chosen_move[1]] == 3:
            self.path.append(chosen_move)
            return


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
        self.evaporate_pheromone()

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
        ATTRACTIVENESS_MAP = {
            0: 0,  # Walls
            1: 1,  # Normal terrain
            3: 5,  # Goal points
            4: 2,  # Rough terrain
            5: 0.1  # Water terrain
        }
        terrain_type = self.maze[move[0]][move[1]]
        return ATTRACTIVENESS_MAP.get(terrain_type, 1)

    def calculate_path_length(self, path):
        # Calculate the length of a given path in the maze
        return len(path)


def solve(maze, num_tours):
    start_positions = np.where(maze == 2)
    start_position = (start_positions[0][0], start_positions[1][0])
    ant_colony = ACO(maze, num_ants=10, evaporation_rate=0.5, alpha=1, beta=1)

    ants = [Ant(maze, start_position, ant_colony) for _ in range(ant_colony.num_ants)]

    # init some parameters
    it = 0
    best_tour_length = np.inf
    ended = False

    # begin swarming
    while not ended:
        for ant in ants:
            ant.move()
            ant_tour = len(ant.path)
            if ant_tour < best_tour_length:
                best_tour_length = ant_tour
        it += 1

        ant_colony.update_pheromone_trails(ants)
        ant_colony.evaporate_pheromone()
        if it >= num_tours:
            ended = True

    best_path = max(ants, key=lambda ant: ant_colony.calculate_path_length(ant.path)).path
    best_path_length = ant_colony.calculate_path_length(best_path)
    return best_path, best_path_length


maze = generate_maze(6, 6)
print(maze)
print(solve(maze, 4))
