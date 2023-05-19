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

    start_x, start_y = np.random.randint(1, width) * 2, np.random.randint(1, height) * 2
    maze[start_y, start_x] = 2

    end_x, end_y = np.random.randint(1, width) * 2, np.random.randint(1, height) * 2
    maze[end_y, end_x] = 3

    carve_path(start_x, start_y)

    return maze

def display_maze(maze):
    cmap = plt.cm.get_cmap('Greens')  # Colormap for colors
    cmap.set_under('white')  # Set the color for the maze

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(maze, cmap=cmap, interpolation='nearest')

    # Add entry and exit points inside the maze
    start = np.argwhere(maze == 2)
    end = np.argwhere(maze == 3)
    ax.scatter(start[:, 1], start[:, 0], color='blue', marker='s', s=100)
    ax.scatter(end[:, 1], end[:, 0], color='red', marker='s', s=100)

    # Add header text with better placement
    ax.text(maze.shape[1] // 2, -0.8, 'Maze Project', ha='center', fontsize=20, fontweight='bold')

    plt.xticks([])
    plt.yticks([])
    plt.show()

def verify_path(maze):
    start = np.argwhere(maze == 2)
    end = np.argwhere(maze == 3)

    def dfs(x, y):
        if [x, y] in end.tolist():
            return True

        maze[y, x] = -1  # Mark current cell as visited

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] in [1, 3]:
                if dfs(nx, ny):
                    return True

        return False

    return any(dfs(*point) for point in start)

# Generate a maze with a valid path between the start and end points
maze = generate_maze(10, 10)
while not verify_path(maze):
    maze = generate_maze(10, 10)

display_maze(maze)
