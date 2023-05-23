import matplotlib.pyplot as plt
from Adventurer import Adventurer
import algorithms
import numpy as np
import random

game_finished = False  # Global variable to track game status


def generate_maze(width, height):
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

    # Generate random start point on the left wall of the maze
    start_x, start_y = 0, random.randint(1, height) * 2
    start_point = (start_x, start_y)

    # Generate end point on the upper wall of the maze
    end_x, end_y = random.randint(1, width) * 2, 0
    end_point_upper = (end_x, end_y)

    # Generate end point on the outer wall of the maze
    end_x, end_y = random.randint(1, width) * 2, height * 2
    end_point_outer = (end_x, end_y)

    # Generate end point of the right wall of the maze
    end_x, end_y = 2 * width, random.randint(1, height) * 2
    end_point_left = (end_x, end_y)

    generate_paths(start_point[0], start_point[1], end_point_upper[0], end_point_upper[1])
    generate_paths(start_point[0], start_point[1], end_point_outer[0], end_point_outer[1])
    generate_paths(start_point[0], start_point[1], end_point_left[0], end_point_left[1])

    # Ensure that both end points are reachable from the start point
    while not verify_path(maze, start_point, end_point_upper) or not verify_path(maze, start_point, end_point_outer):
        maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)
        generate_paths(start_point[0], start_point[1], end_point_upper[0], end_point_upper[1])
        generate_paths(start_point[0], start_point[1], end_point_outer[0], end_point_outer[1])
        generate_paths(start_point[0], start_point[1], end_point_left[0], end_point_left[1])

    maze[start_point[1], start_point[0]] = 2  # Set the start point
    maze[end_point_upper[1], end_point_upper[0]] = 3  # Set the upper exit point
    maze[end_point_outer[1], end_point_outer[0]] = 3  # Set the outer exit point
    maze[end_point_left[1], end_point_left[0]] = 3  # Set the left exit point

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


def display_maze(maze, algorithm):
    cmap = plt.cm.get_cmap('Greens_r')  # Colormap for colors
    cmap.set_under('black')  # Set the color for the maze

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
    ax.imshow(maze, cmap=cmap, interpolation='nearest')

    # Add entry and exit points inside the maze
    start = np.argwhere(maze == 2)[0]
    ends = np.argwhere(maze == 3)

    ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
    for end_point in ends:
        ax.scatter(end_point[1], end_point[0], color='red', marker='s', s=100)

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

        # Check if the game is already finished
        if game_finished:
            return

        direction = direction_mapping.get(event.key)
        if direction:
            dx, dy = direction
            adventurer.move(dx, dy)
            adventurer_plot.set_offsets([adventurer.x, adventurer.y])
            plt.draw()

            # Check if the adventurer has reached the end point
            if any((adventurer.x, adventurer.y) == (end[1], end[0]) for end in ends):
                game_finished = True
                print("You won!")

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

    def shuffle_maze(event):
        nonlocal maze, adventurer, adventurer_plot
        global game_finished
        game_finished = False  # Reset game status
        maze = generate_maze((maze.shape[1] - 1) // 2, (maze.shape[0] - 1) // 2)
        ax.clear()
        ax.imshow(maze, cmap=cmap, interpolation='nearest')
        start = np.argwhere(maze == 2)[0]
        ends = np.argwhere(maze == 3)
        ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
        for end_point in ends:
            ax.scatter(end_point[1], end_point[0], color='red', marker='s', s=100)
        adventurer = Adventurer(maze, start[1], start[0])  # Update adventurer with the new maze
        adventurer_plot = ax.scatter(adventurer.x, adventurer.y, color=adventurer.color, marker=adventurer.marker,
                                     s=adventurer.size)
        ax.text(maze.shape[1] // 2, -0.8, 'Maze Project', ha='center', fontsize=20, fontweight='bold')
        plt.draw()

        fig.canvas.mpl_connect('key_press_event', on_key)  # Reconnect the key press event

    fig.canvas.mpl_connect('key_press_event', on_key)
    button.on_clicked(shuffle_maze)

    quit.on_clicked(quit_game)

    plt.show()


maze =generate_maze(10, 10)
display_maze(maze, 'A*')
