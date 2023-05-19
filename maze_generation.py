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

    # Position the start and end points at opposite ends
    start_x, start_y = 1, np.random.randint(1, height) * 2
    maze[start_y, start_x] = 2  # Set the start point

    end_x, end_y = width * 2, np.random.randint(1, height) * 2
    maze[end_y, end_x] = 3  # Set the end point

    carve_path(start_x, start_y)

    return maze

def display_maze(maze):
    cmap = plt.cm.colors.ListedColormap(['green', 'white', 'blue', 'red'])
    bounds = [0, 1, 2, 3, 4]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze, cmap=cmap, interpolation='nearest', norm=norm)

    ax.set_xticks([])
    ax.set_yticks([])

    # Add header text with better placement
    ax.text(maze.shape[1] // 2, -1, 'Maze Project', ha='center', fontsize=16, fontweight='bold')

    # Add shuffle button
    ax_button = plt.axes([0.4, 0.02, 0.2, 0.05])
    button = plt.Button(ax_button, 'Shuffle', color='lightblue', hovercolor='skyblue')

    def shuffle_maze(event):
        nonlocal maze
        maze = generate_maze((maze.shape[1] - 1) // 2, (maze.shape[0] - 1) // 2)
        ax.clear()
        ax.imshow(maze, cmap=cmap, interpolation='nearest', norm=norm)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(maze.shape[1] // 2, -1, 'Maze Project', ha='center', fontsize=16, fontweight='bold')
        plt.draw()

    button.on_clicked(shuffle_maze)

    plt.show()

# Example usage:
maze = generate_maze(10, 10)
display_maze(maze)
