import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from maze_generation import display_maze, generate_maze, quit
import sys


class StartGamePage(tk.Frame):
    def __init__(self, parent, start_game_callback):
        super().__init__(parent)
        self.start_game_callback = start_game_callback
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'))

        title_label = ttk.Label(self, text="Maze Game", style='Title.TLabel')
        title_label.pack(pady=(20, 10))

        width_label = ttk.Label(self, text="Width:")
        width_label.pack()

        self.width_entry = ttk.Entry(self)
        self.width_entry.pack()

        height_label = ttk.Label(self, text="Height:")
        height_label.pack()

        self.height_entry = ttk.Entry(self)
        self.height_entry.pack()

        self.algorithm_label = tk.Label(self, text="Algorithm:", font=("Arial", 12))
        self.algorithm_label.pack()

        self.algorithm_var = tk.StringVar(self)
        self.algorithm_var.set("Manual")

        self.algorithm_menu = tk.OptionMenu(self, self.algorithm_var, "Manual", "A*", "BFS", "DFS", "Ant Colony",
                                            "Dijkstra")
        self.algorithm_menu.pack()

        start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        start_button.pack(pady=(20, 10))

        shuffle_button = ttk.Button(self, text="Shuffle Game", command=self.shuffle_game)
        shuffle_button.pack(pady=(20, 10))

        quit_button = ttk.Button(self, text="Exit Game", command=self.end_game)
        quit_button.pack(pady=(30, 20))

    def start_game(self):
        width = self.width_entry.get()
        height = self.height_entry.get()
        algorithm = self.algorithm_var.get()

        if not width.isdigit() or not height.isdigit():
            messagebox.showerror("Input Error", "Width and height must be numeric values.")
        elif int(width) <= 0 or int(height) <= 0:
            messagebox.showerror("Input Error", "Width and height must be positive values, greater then 0.")

        else:
            width = int(width)
            height = int(height)
            self.start_game_callback(width, height, algorithm)

    def end_game(self):
        start_page.destroy()
        root.destroy()
        sys.exit()

    def shuffle_game(self):
        quit()
        test_display_maze(width_global,length_global,algorithm_global)


def start_game_callback(width, height, algorithm):
    start_page.width_entry.delete(0, tk.END)
    start_page.height_entry.delete(0, tk.END)
    print(f"Width: {width}")
    print(f"Height: {height}")
    global width_global, length_global, algorithm_global
    width_global = width
    length_global = height
    algorithm_global = algorithm
    test_display_maze(width, height, algorithm)


def test_display_maze(width, height, algorithm):
    # Generate a maze using your desired width and height
    width = width
    height = height
    maze = generate_maze(width, height)
    # Display the maze
    display_maze(maze, algorithm)


root = tk.Tk()
root.title("Maze Game")

content_frame = ttk.Frame(root, padding=20)
content_frame.pack()

start_page = StartGamePage(content_frame, start_game_callback)
start_page.pack()

# Adjust the window size to fit the content
root.update()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

root.mainloop()
