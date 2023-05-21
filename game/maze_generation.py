import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from Adventurer import Adventurer
import algorithms

game_finished = False  # Global variable to track game status



def generate_maze(width, height, num_solutions=1):
    maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)
    paths = []
    start_x, start_y, end_x, end_y = 0, np.random.randint(1, height + 1) * 2, 2 * width, np.random.randint(1,
                                                                                                           height + 1) * 2

    def carve_path(x, y, path):
        nonlocal maze, paths

        maze[y, x] = 1
        path.append((x, y))

        if (x, y) == (end_x, end_y):
            paths.append(path[:])
            return

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        np.random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = x + 2 * dx, y + 2 * dy
            if 0 <= next_x < 2 * width + 1 and 0 <= next_y < 2 * height + 1 and maze[next_y, next_x] == 0:
                maze[y + dy, x + dx] = 1
                maze[y + dy // 2, x + dx // 2] = 1
                carve_path(next_x, next_y, path)

    while len(paths) < num_solutions:
        maze.fill(0)
        paths.clear()
        carve_path(start_x, start_y, [])

    maze[start_y, start_x] = 2
    maze[end_y, end_x] = 3

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
        np.random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] == 1 and (nx, ny) not in visited:
                stack.append((nx, ny))

    return False


def display_maze(maze):
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
    ax.text(maze.shape[1] // 2, -0.9, 'Maze Project', ha='center', fontsize=20, fontweight='bold')

    # Add shuffle button
    ax_button = plt.axes([0.12, 0.03, 0.2, 0.05])
    button = plt.Button(ax_button, 'Shuffle', color='lightblue', hovercolor='skyblue')

    # Add quit button
    ax_button = plt.axes([0.7, 0.03, 0.2, 0.05])
    quit = plt.Button(ax_button, 'quit', color='red', hovercolor='green')

    # Add text
    ax.text(maze.shape[1] // 3, 33, 'a for A*', ha='center', fontsize=8)
    ax.text(maze.shape[1] // 3, 34, 'b for bfs', ha='center', fontsize=8)
    ax.text(maze.shape[1] // 2, 33, 'd for dfs', ha='center', fontsize=8)
    ax.text(maze.shape[1] // 2, 34, 'k for dijkstra', ha='center', fontsize=8)

    def quit_game(event):
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
            shuffle_maze(None)
            game_finished = True
        else:
            direction = direction_mapping.get(event.key)
            if direction:
                dx, dy = direction
                adventurer.move(dx, dy)
                adventurer_plot.set_offsets([adventurer.x, adventurer.y])
                plt.draw()

    def on_figure_key(event):
        if event.key == 'a':
            path = algorithms.a_star(maze)
            if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
                for step in path:
                    adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                    adventurer.follow_path()
                    adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                    plt.draw()
                    plt.pause(0.1)
        if event.key == 'b':
            path = algorithms.bfs(maze)
            if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
                for step in path:
                    adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                    adventurer.follow_path()
                    adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                    plt.draw()
                    plt.pause(0.1)
        if event.key == 'd':
            path = algorithms.dfs(maze)
            if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
                for step in path:
                    adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                    adventurer.follow_path()
                    adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                    plt.draw()
                    plt.pause(0.1)
        if event.key == 'k':
            path = algorithms.dijkstra(maze)
            if algorithms.verify_path_algorithm(path, maze):  # Exclude the starting position
                for step in path:
                    adventurer.move(step[0] - adventurer.x, step[1] - adventurer.y)
                    adventurer.follow_path()
                    adventurer_plot.set_offsets([adventurer.y, adventurer.x])
                    plt.draw()
                    plt.pause(0.1)
        elif event.key == 's':
            shuffle_maze(None)
        elif event.key == 'q':
            plt.close()


    def shuffle_maze(event):
        nonlocal maze, adventurer, adventurer_plot
        maze = generate_maze((maze.shape[1] - 1) // 2, (maze.shape[0] - 1) // 2)
        ax.clear()
        ax.imshow(maze, cmap=cmap, interpolation='nearest')
        start = np.argwhere(maze == 2)[0]
        end = np.argwhere(maze == 3)[0]
        ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
        ax.scatter(end[1], end[0], color='red', marker='s', s=100)
        adventurer = Adventurer(maze, start[1], start[0])  # Update adventurer with the new maze
        adventurer_plot = ax.scatter(adventurer.x, adventurer.y, color=adventurer.color, marker=adventurer.marker,
                                     s=adventurer.size)
        ax.text(maze.shape[1] // 2, -0.8, 'Maze Project', ha='center', fontsize=20, fontweight='bold')
        plt.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('key_press_event', on_figure_key)
    button.on_clicked(shuffle_maze)

    quit.on_clicked(quit_game)

    plt.show()

