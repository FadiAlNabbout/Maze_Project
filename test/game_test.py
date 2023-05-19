import tkinter as tk
from tkinter import messagebox
import sys
sys.path.append('C:/Users/Personal/PycharmProjects/Maze/game/')
from maze_generation import generate_maze, verify_path
from algorithms import a_star, bfs, dfs
from game import MazeGameApp

class TestMazeGameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.app = MazeGameApp()

        self.width_entry = tk.Entry(self, font=("Arial", 12))
        self.width_entry.pack()

        self.height_entry = tk.Entry(self, font=("Arial", 12))
        self.height_entry.pack()

        self.algorithm_var = tk.StringVar(self)
        self.algorithm_var.set("A*")

        self.algorithm_menu = tk.OptionMenu(self, self.algorithm_var, "A*", "BFS", "DFS", "Ant Colony")
        self.algorithm_menu.pack()

        self.start_button = tk.Button(self, text="Start", font=("Arial", 12), command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        width = self.width_entry.get()
        height = self.height_entry.get()
        algorithm = self.algorithm_var.get()

        self.app.width_entry.insert(0, width)
        self.app.height_entry.insert(0, height)
        self.app.algorithm_var.set(algorithm)
        self.app.start_game()

if __name__ == "__main__":
    test_app = TestMazeGameApp()
    test_app.mainloop()
