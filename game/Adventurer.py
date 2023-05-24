import time


class Adventurer:
    def __init__(self, maze, start_x, start_y, color='yellow', marker='o', size=100):
        self.maze = maze
        self.x = start_x
        self.y = start_y
        self.color = color
        self.marker = marker
        self.size = size
        self.path = None
        self.path_index = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the bounds of the maze
        if 0 <= new_x < self.maze.shape[1] and 0 <= new_y < self.maze.shape[0]:
            # Check if the new position is not a wall
            if self.maze[new_y, new_x] != 0:
                self.x = new_x
                self.y = new_y

    def update_path(self, path):
        self.path = path
        self.path_index = 0

    def follow_path(self):
        if self.path is not None and self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            dx = next_x - self.x
            dy = next_y - self.y
            self.move(dx, dy)
            self.path_index += 1

    def reset_position(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.path = None

    def get_positions(self):
        return self.x, self.y
        pass

    def is_at_end(self, end):
        if self.x == end[0] and self.y == end[1]:
            return True
        pass

    def set_path(self, path):
        self.path = path
        pass

    def move_along_path(self):
        for i in range(1, len(self.path)):
            self.move(self.path[i][0], self.path[i][1])
