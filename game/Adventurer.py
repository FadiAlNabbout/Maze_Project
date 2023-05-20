class Adventurer:
    def __init__(self, maze, start_x, start_y, color='yellow', marker='o', size=100):
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.color = color
        self.marker = marker
        self.size = size

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the bounds of the maze
        if 0 <= new_x < self.maze.shape[1] and 0 <= new_y < self.maze.shape[0]:
            # Check if the new position is not a wall
            if self.maze[new_y, new_x] != 0:
                self.x = new_x
                self.y = new_y


    def reset_position(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

