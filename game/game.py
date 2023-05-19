import tkinter as tk
from tkinter import messagebox
from maze_generation import generate_maze, verify_path
from algorithms import a_star, bfs, dfs

class MazeGameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.width = None
        self.height = None
        self.algorithm = None

        self.label = tk.Label(self, text="Maze Game", font=("Arial", 18))
        self.label.pack(side="top", pady=10)

        self.width_label = tk.Label(self, text="Width:", font=("Arial", 12))
        self.width_label.pack()
        self.width_entry = tk.Entry(self, font=("Arial", 12))
        self.width_entry.pack()

        self.height_label = tk.Label(self, text="Height:", font=("Arial", 12))
        self.height_label.pack()
        self.height_entry = tk.Entry(self, font=("Arial", 12))
        self.height_entry.pack()

        self.algorithm_label = tk.Label(self, text="Algorithm:", font=("Arial", 12))
        self.algorithm_label.pack()

        self.algorithm_var = tk.StringVar(self)
        self.algorithm_var.set("A*")

        self.algorithm_menu = tk.OptionMenu(self, self.algorithm_var, "A*", "BFS", "DFS", "Ant Colony")
        self.algorithm_menu.pack()

        self.start_button = tk.Button(self, text="Start Game", font=("Arial", 12), command=self.start_game)
        self.start_button.pack()

        self.frames = {}

        self.frames["MazeGameApp"] = self

    def start_game(self):
        width = self.width_entry.get()
        height = self.height_entry.get()
        algorithm = self.algorithm_var.get()

        if width.isdigit() and height.isdigit():
            width = int(width)
            height = int(height)

            if width <= 0 or height <= 0:
                messagebox.showerror("Error", "Invalid dimensions. Width and height must be greater than zero.")
                return
        else:
            messagebox.showerror("Error", "Invalid input. Width and height must be positive integers.")
            return

        self.width = width
        self.height = height
        self.algorithm = algorithm

        self.show_frame("MazeGameApp")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = MazeGameApp()
    app.mainloop()
