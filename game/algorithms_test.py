import timeit
import numpy as np
import sys

from algorithms import a_star, bfs, dfs, ant_colony

def generate_maze():
    maze = np.random.randint(2, size=(100, 100))
    maze[0, 0] = 2  # Start point
    maze[-1, -1] = 3  # End point
    return maze

def test_algorithm_performance(algorithm):
    setup_code = '''
from __main__ import generate_maze, {algorithm}
maze = generate_maze()
    '''.format(algorithm=algorithm)

    test_code = '''
{algorithm}(maze)
    '''.format(algorithm=algorithm)

    execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=1)
    print("{algorithm}: Execution time: {time:.6f} seconds".format(algorithm=algorithm, time=execution_time))

if __name__ == "__main__":
    algorithms = ['a_star', 'bfs', 'dfs', 'ant_colony']
    for algorithm in algorithms:
        test_algorithm_performance(algorithm)
