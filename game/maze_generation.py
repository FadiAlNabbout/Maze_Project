import numpy as np
import random
import matplotlib.pyplot as plt
from Adventurer import Adventurer
import algorithms

global game_finished  # Global variable to track game status
game_finished = False

import numpy as np
import random

def generate_maze(width, height, num_paths):
    maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)

    def carve_path(x, y):
        maze[y, x] = 1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = x + 2 * dx, y + 2 * dy
            if 0 <= next_x < 2 * width + 1 and 0 <= next_y < 2 * height + 1 and maze[next_y, next_x] == 0:
                maze[y + dy, x + dx] = 1
                maze[y + dy // 2, x + dx // 2] = 1  # Carve the path by removing the wall
                carve_path(next_x, next_y)

        # Add dead-ends
        if random.random() < 0.5:  # Adjust the probability as desired
            add_dead_end(x, y)

    def add_dead_end(x, y):
        dead_end_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(dead_end_directions)

        for dx, dy in dead_end_directions:
            dead_x, dead_y = x + 2 * dx, y + 2 * dy
            if 0 <= dead_x < 2 * width + 1 and 0 <= dead_y < 2 * height + 1 and maze[dead_y, dead_x] == 0:
                maze[y + dy, x + dx] = 1
                maze[y + dy // 2, x + dx // 2] = 1  # Carve the dead-end path by removing the wall
                break


    def generate_paths(start_x, start_y, end_x, end_y):
        maze[start_y, start_x] = 1
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = start_x + 2 * dx, start_y + 2 * dy
            if 0 <= next_x < 2 * width + 1 and 0 <= next_y < 2 * height + 1 and maze[next_y, next_x] == 0:
                maze[start_y + dy, start_x + dx] = 1
                maze[start_y + dy // 2, start_x + dx // 2] = 1  # Carve the path by removing the wall
                add_dead_end(start_x + dx, start_y + dy)
                generate_paths(next_x, next_y, end_x, end_y)

    # Generate random start and end points on the borders
    start_x, start_y = 0, random.randint(1, height) * 2
    start_points = [(start_x, start_y)]
    end_points = []

    for _ in range(num_paths):
        end_x, end_y = 2 * width, random.randint(1, height) * 2
        end_points.append((end_x, end_y))

    for start, end in zip(start_points, end_points):
        generate_paths(start[0], start[1], end[0], end[1])

    # Ensure that all end points are reachable from the corresponding start points
    for start, end in zip(start_points, end_points):
        while not verify_path(maze, start, end):
            maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)
            generate_paths(start[0], start[1], end[0], end[1])

    for start in start_points:
        maze[start[1], start[0]] = 2  # Set the start point

    for end in end_points:
        maze[end[1], end[0]] = 3  # Set the end point

    return maze


def verify_path(maze, start, end):
    stack = [start]
    visited = set()

    while stack:
        x, y = stack.pop()
        visited.add((x, y))

        if (x, y) == end:
            return True

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] == 1 and (nx, ny) not in visited:
                stack.append((nx, ny))

    return False

def quit():
    plt.close()


def display_maze(maze, algorithm):
    cmap = plt.cm.get_cmap('Greens_r')  # Colormap for colors
    cmap.set_under('black')  # Set the color for the maze

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
    ax.imshow(maze, cmap=cmap, interpolation='nearest')

    # Add entry and exit points inside the maze
    start = np.argwhere(maze == 2)[0]
    end = np.argwhere(maze == 3)[0]
    ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
    ax.scatter(end[1], end[0], color='red', marker='s', s=100)

    adventurer = Adventurer(maze, start[1], start[0])
    adventurer_plot = ax.scatter(adventurer.x, adventurer.y, color=adventurer.color, marker=adventurer.marker,
                                 s=adventurer.size)

    # Add header text with better placement
    ax.text(maze.shape[1] // 2, -0.9, 'Maze Game', ha='center', fontsize=20, fontweight='bold')

    # Add quit button
    ax_button = plt.axes([0.4, 0.03, 0.2, 0.06])
    quit = plt.Button(ax_button, 'Quit', color='orange', hovercolor='red')

    def quit_game(event):
        global game_finished
        game_finished = True
        plt.close()



    def on_key(event):
        global game_finished  # Access the global variable
        direction_mapping = {
            'right': (1, 0),
            'left': (-1, 0),
            'down': (0, 1),
            'up': (0, -1)
        }

        if (adventurer.x, adventurer.y) == (end[1], end[0]):
            adventurer.move(0, 0)  # Stop the adventurer's movement
            adventurer_plot.set_offsets([adventurer.x, adventurer.y])
            print("Congratulations! You win!")
            game_finished = True
        else:
            direction = direction_mapping.get(event.key)
            if direction:
                dx, dy = direction
                adventurer.move(dx, dy)
                adventurer_plot.set_offsets([adventurer.x, adventurer.y])
                quit.on_clicked(quit_game)
                plt.draw()

    if algorithm == 'A*':
        path = algorithms.a_star(maze)
        print("A* path: ")
        if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
            for step in path:
                adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                adventurer.follow_path()
                adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                quit.on_clicked(quit_game)
                plt.draw()
                plt.pause(0.2)
    if algorithm == 'BFS':
        path = algorithms.bfs(maze)
        print("BFS path: ")
        if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
            for step in path:
                adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                adventurer.follow_path()
                adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                quit.on_clicked(quit_game)
                plt.draw()
                plt.pause(0.2)
    if algorithm == 'DFS':
        path = algorithms.dfs(maze)
        print("DFS path: ")
        if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
            for step in path:
                adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                adventurer.follow_path()
                adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                quit.on_clicked(quit_game)
                plt.draw()
                plt.pause(0.2)
    if algorithm == 'Dijkstra':
        path = algorithms.dijkstra(maze)
        print("Dijkstra path: ")
        if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
            for step in path:
                adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                adventurer.follow_path()
                adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                quit.on_clicked(quit_game)
                plt.draw()
                plt.pause(0.2)

        if algorithm == "manual":
            on_key(None)



    fig.canvas.mpl_connect('key_press_event', on_key)

    quit.on_clicked(quit_game)

    plt.show()
