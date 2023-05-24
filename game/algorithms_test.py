import timeit
import numpy as np
import sys

import maze_generation
from algorithms import a_star, bfs, dfs, dijkstra

def generate_maze():
    maze = maze_generation.generate_maze(100, 100)
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
    algorithms = ['dijkstra', 'a_star', 'bfs', 'dfs']
    for algorithm in algorithms:
        test_algorithm_performance(algorithm)
