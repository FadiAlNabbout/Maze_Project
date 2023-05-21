import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from maze_generation import generate_maze, display_maze

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


        start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        start_button.pack(pady=(20, 10))

        quit_button = ttk.Button(self, text="Exit Game", command=self.end_game)
        quit_button.pack(pady=(30, 20))

    def start_game(self):
        width = self.width_entry.get()
        height = self.height_entry.get()

        if not width.isdigit() or not height.isdigit():
            messagebox.showerror("Input Error", "Width and height must be numeric values.")

        else:
            width = int(width)
            height = int(height)
            self.start_game_callback(width, height)

    def end_game(self):
        start_page.destroy()
        root.destroy()


def start_game_callback(width, height):
    print(f"Width: {width}")
    print(f"Height: {height}")
    test_display_maze(width, height)

def test_display_maze(width, height):
        # Generate a maze using your desired width and height
        width = width
        height = height
        maze = generate_maze(width, height)

        # Display the maze
        display_maze(maze)


        if __name__ == "__main__":
            test_display_maze()


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

