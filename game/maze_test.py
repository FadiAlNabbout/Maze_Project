from maze_generation import generate_maze, display_maze


def test_display_maze():
    # Generate a maze using your desired width and height
    width = 6
    height = 6
    maze = generate_maze(width, height)

    # Display the maze
    display_maze(maze)


if __name__ == "__main__":
    test_display_maze()
