import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from Adventurer import Adventurer
import algorithms

sys.setrecursionlimit(10 ** 6)  # Increase the recursion limit

global game_finished  # Global variable to track game status
game_finished = False


def generate_maze(width, height):
    maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=float)

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

    def generate_paths(start_x, start_y, end_x, end_y):
        maze[start_y, start_x] = 1
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = start_x + 2 * dx, start_y + 2 * dy
            if 0 <= next_x < 2 * width + 1 and 0 <= next_y < 2 * height + 1 and maze[next_y, next_x] == 0:
                maze[start_y + dy, start_x + dx] = 1
                maze[start_y + dy // 2, start_x + dx // 2] = 1  # Carve the path by removing the wall
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

    # Ensure that both end points are reachable from the start point
    while not verify_path(maze, start_point, end_point_upper) or not verify_path(maze, start_point, end_point_outer):
        maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=float)
        generate_paths(start_point[0], start_point[1], end_point_upper[0], end_point_upper[1])
        generate_paths(start_point[0], start_point[1], end_point_outer[0], end_point_outer[1])
        generate_paths(start_point[0], start_point[1], end_point_left[0], end_point_left[1])

    maze[start_point[1], start_point[0]] = 2  # Set the start point
    maze[end_point_upper[1], end_point_upper[0]] = 3.3  # Set the upper exit point
    maze[end_point_outer[1], end_point_outer[0]] = 3.1  # Set the outer exit point
    maze[end_point_left[1], end_point_left[0]] = 3.2  # Set the left exit point

    # Add rough terrain
    for y in range(1, 2 * height, 2):
        for x in range(1, 2 * width, 2):
            if random.random() < 0.05:  # Adjust the probability as desired
                maze[y, x] = 4  # Rough terrain

    # Add water
    for y in range(1, 2 * height, 2):
        for x in range(1, 2 * width, 2):
            if random.random() < 0.05:  # Adjust the probability as desired
                maze[y, x] = 5  # Water
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
    ends = []
    end_position_1 = np.argwhere(maze == 3.1)
    end_position_2 = np.argwhere(maze == 3.2)
    end_position_3 = np.argwhere(maze == 3.3)
    ends.append(end_position_1[0])
    ends.append(end_position_2[0])
    ends.append(end_position_3[0])

    ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
    ax.text(start[1], start[0], "s", color='white', fontsize=12, ha='center', va='center')
    for i, end_point in enumerate(ends):
        ax.scatter(end_point[1], end_point[0], color='red', marker='s', s=100)
        ax.text(end_point[1], end_point[0], str(i + 1), color='black', fontsize=12, ha='center', va='center')

    # Add rough terrain in brown
    rough_terrain = np.argwhere(maze == 4)
    for terrain in rough_terrain:
        ax.scatter(terrain[1], terrain[0], color='brown', marker='s', s=100)

    # Add water terrain in sky blue
    water_terrain = np.argwhere(maze == 5)
    for terrain in water_terrain:
        ax.scatter(terrain[1], terrain[0], color='skyblue', marker='s', s=100)

    adventurer = Adventurer(maze, start[1], start[0])
    adventurer_plot = ax.scatter(adventurer.x, adventurer.y, color=adventurer.color, marker=adventurer.marker,
                                 s=100)

    # Add header text with better placement
    ax.text(maze.shape[1] // 2, -0.9, 'Maze Project', ha='center', fontsize=20, fontweight='bold')

    # Add quit button
    ax_button = plt.axes([0.7, 0.03, 0.2, 0.05])
    quit = plt.Button(ax_button, 'quit', color='red', hovercolor='green')

    # Add number steps
    num_steps=adventurer.num_steps


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

        # Check if the adventurer has reached the end point
        if any((adventurer.x, adventurer.y) == (end[1], end[0]) for end in ends):
            adventurer.move(0, 0)  # Stop the adventurer's movement
            game_finished = True
            print("You won!")
            ax.text(maze.shape[1] // 2, maze.shape[0] + 1.5, 'Number of steps: ' + str(num_steps), ha='center',
                    fontsize=12, fontweight='bold')

        else:
            direction = direction_mapping.get(event.key)
            if direction:
                dx, dy = direction
                adventurer.move(dx, dy)
                adventurer_plot.set_offsets([adventurer.x, adventurer.y])
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
    if algorithm == 'UCS':
        path = algorithms.ucs(maze)
        print("UCS path: ")
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

