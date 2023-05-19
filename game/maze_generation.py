import numpy as np
import matplotlib.pyplot as plt


def generate_maze(width, height):
    maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)

    def carve_path(x, y):
        maze[y, x] = 1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        np.random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = x + 2 * dx, y + 2 * dy
            if 0 <= next_x < 2 * width + 1 and 0 <= next_y < 2 * height + 1 and maze[next_y, next_x] == 0:
                maze[y + dy, x + dx] = 1
                maze[y + dy // 2, x + dx // 2] = 1  # Carve the path by removing the wall
                carve_path(next_x, next_y)

    # Generate random start and end points on the borders
    start_x, start_y = 0, np.random.randint(1, height + 1) * 2
    end_x, end_y = 2 * width, np.random.randint(1, height + 1) * 2

    # Carve the path from start to end
    carve_path(start_x, start_y)

    # Ensure that the end point is reachable from the start point
    while not verify_path(maze, (start_x, start_y), (end_x, end_y)):
        maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=int)
        start_x, start_y = 0, np.random.randint(1, height + 1) * 2
        end_x, end_y = 2 * width, np.random.randint(1, height + 1) * 2
        carve_path(start_x, start_y)

    maze[start_y, start_x] = 2  # Set the start point
    maze[end_y, end_x] = 3  # Set the end point

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
    cmap = plt.cm.get_cmap('Spectral')  # Colormap for colors
    cmap.set_under('black')  # Set the color for the maze

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(maze, cmap=cmap, interpolation='nearest')

    # Add entry and exit points inside the maze
    start = np.argwhere(maze == 2)[0]
    end = np.argwhere(maze == 3)[0]
    ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
    ax.scatter(end[1], end[0], color='red', marker='s', s=100)

    # Add header text with better placement
    ax.text(maze.shape[1] // 2, -0.8, 'Maze Project', ha='center', fontsize=20, fontweight='bold')

    # Add shuffle button
    ax_button = plt.axes([0.4, 0.03, 0.2, 0.05])
    button = plt.Button(ax_button, 'Shuffle', color='lightblue', hovercolor='skyblue')

    def shuffle_maze(event):
        nonlocal maze
        maze = generate_maze((maze.shape[1] - 1) // 2, (maze.shape[0] - 1) // 2)
        ax.clear()
        ax.imshow(maze, cmap=cmap, interpolation='nearest')
        start = np.argwhere(maze == 2)[0]
        end = np.argwhere(maze == 3)[0]
        ax.scatter(start[1], start[0], color='blue', marker='s', s=100)
        ax.scatter(end[1], end[0], color='red', marker='s', s=100)
        ax.text(maze.shape[1] // 2, -0.8, 'Maze Project', ha='center', fontsize=20, fontweight='bold')
        plt.draw()

    button.on_clicked(shuffle_maze)

    plt.xticks([])
    plt.yticks([])
    plt.show()
