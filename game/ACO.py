import numpy as np

# Define the maze
maze = np.array(
    [
        [1, 1, 1, 1, 3, 1, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [2, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 3],
        [1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1],
        [1, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1],
    ]
)

# Define ACO parameters
num_ants = 10
alpha = 1.0
beta = 2.0
evaporation_rate = 0.5
pheromone_deposit = 1.0
num_iterations = 100

# Initialize pheromone matrix
pheromone = np.ones_like(maze, dtype=float)


# Define the update rule for pheromone deposit
def deposit_pheromone(path):
    for row, col in path:
        pheromone[row, col] += pheromone_deposit


# Define the update rule for pheromone evaporation
def evaporate_pheromone(pheromone):
    pheromone *= (1 - evaporation_rate)


# Define the heuristic function for ant movement
def heuristic(row, col):
    if maze[row, col] == 0:
        return 0
    else:
        return 1 / maze[row, col]


# Perform ACO iterations
for iteration in range(num_iterations):
    # Initialize ant positions to the starting point
    ant_positions = [(np.where(maze == 2)[0][0], np.where(maze == 2)[1][0])] * num_ants

    # Initialize paths and distances
    paths = [[] for _ in range(num_ants)]
    distances = np.zeros(num_ants)

    # Move ants through the maze
    for step in range(maze.size):
        for ant in range(num_ants):
            row, col = ant_positions[ant]
            pheromone_values = pheromone ** alpha * heuristic(row, col) ** beta

            # Calculate available moves
            available_moves = np.argwhere(maze != 1)
            available_moves = available_moves.tolist()

            if (row, col) in available_moves:
                available_moves.remove((row, col))

            if not available_moves:
                break

            next_move = max(available_moves, key=lambda move: pheromone_values[move])
            ant_positions[ant] = next_move
            paths[ant].append(next_move)
            distances[ant] += 1

            if maze[next_move] == 3:
                deposit_pheromone(paths[ant])
                break

        # Find the shortest path among the paths that reach the goal
    shortest_path = min(paths, key=len)

    # Print the shortest path
    print(f"Iteration {iteration+1} - Shortest Path:")
    if shortest_path:
        for row, col in shortest_path:
            print(f"({row}, {col})")
    else:
        print("No path found.")

    # Evaporate pheromone
    evaporate_pheromone(pheromone)




