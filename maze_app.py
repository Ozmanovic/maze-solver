from graphics import Window
from maze import Maze
import tkinter as tk
from tkinter import ttk, Frame, Label, Scale, Button, HORIZONTAL, IntVar
import sys

sys.setrecursionlimit(10000)  # Temporary fix for large mazes

class MazeApp:
    def __init__(self, root, width=1280, height=720):
        self.root = root
        self.root.title("Maze Generator & Solver")
        self.root.configure(bg="black")

        # Set dark theme colors
        self.bg_color = "black"
        self.fg_color = "white"
        self.accent_color = "#333333"

        # Default parameters
        self.screen_x = width
        self.screen_y = height
        self.margin = int(min(width, height) * 0.05)  # Scale margin based on window size

        # Default maze dimensions
        self.num_rows = 20
        self.num_cols = 30

        # Animation speeds
        self.maze_speed = 5.0
        self.solve_speed = 1.0

        # Create frames
        self.control_frame = Frame(root, padx=5, pady=5, bg=self.bg_color)
        self.control_frame.pack(side="left", fill="y")

        self.maze_frame = Frame(root, bg=self.bg_color)
        self.maze_frame.pack(side="right", fill="both", expand=True)

        # Create controls
        self.create_controls()

        # Create window for maze
        self.win = Window(self.screen_x, self.screen_y, master=self.maze_frame)

        # Start in standby mode (no maze)
        self.status_label.config(text="Ready")

    def create_controls(self):
        # Configure ttk style for dark theme
        style = ttk.Style()
        style.configure("TLabelframe", background=self.bg_color, foreground=self.fg_color)
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color)

        # Window size controls
        window_size_frame = ttk.LabelFrame(self.control_frame, text="Window")
        window_size_frame.pack(fill="x", pady=2)

        Label(window_size_frame, text="W:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w", pady=1)
        self.width_var = IntVar(value=self.screen_x)
        self.width_entry = ttk.Entry(window_size_frame, width=6, textvariable=self.width_var)
        self.width_entry.grid(row=0, column=1, pady=1, padx=2)

        Label(window_size_frame, text="H:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky="w", pady=1)
        self.height_var = IntVar(value=self.screen_y)
        self.height_entry = ttk.Entry(window_size_frame, width=6, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=1, pady=1, padx=2)

        # Apply size button
        self.apply_size_button = Button(window_size_frame, text="Apply", command=self.apply_window_size,
              width=8, bg=self.accent_color, fg=self.fg_color,
              activebackground=self.bg_color, activeforeground=self.fg_color)
        self.apply_size_button.grid(row=2, column=0, columnspan=2, pady=2)

        # Maze size controls
        size_frame = ttk.LabelFrame(self.control_frame, text="Maze")
        size_frame.pack(fill="x", pady=2)

        Label(size_frame, text="R:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w", pady=1)
        self.rows_var = IntVar(value=self.num_rows)
        self.rows_slider = Scale(size_frame, from_=5, to=50, orient=HORIZONTAL,
              variable=self.rows_var, length=100,
              bg=self.bg_color, fg=self.fg_color,
              troughcolor=self.accent_color, highlightbackground=self.bg_color)
        self.rows_slider.grid(row=0, column=1, pady=1)

        Label(size_frame, text="C:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky="w", pady=1)
        self.cols_var = IntVar(value=self.num_cols)
        self.cols_slider = Scale(size_frame, from_=5, to=60, orient=HORIZONTAL,
              variable=self.cols_var, length=100,
              bg=self.bg_color, fg=self.fg_color,
              troughcolor=self.accent_color, highlightbackground=self.bg_color)
        self.cols_slider.grid(row=1, column=1, pady=1)

        # Speed controls
        speed_frame = ttk.LabelFrame(self.control_frame, text="Speed")
        speed_frame.pack(fill="x", pady=2)

        Label(speed_frame, text="Gen:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w", pady=1)
        self.maze_speed_var = IntVar(value=int(self.maze_speed * 10))
        Scale(speed_frame, from_=1, to=100, orient=HORIZONTAL,
              variable=self.maze_speed_var, length=100,
              bg=self.bg_color, fg=self.fg_color,
              troughcolor=self.accent_color, highlightbackground=self.bg_color).grid(row=0, column=1, pady=1)

        Label(speed_frame, text="Sol:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky="w", pady=1)
        self.solve_speed_var = IntVar(value=int(self.solve_speed * 10))
        Scale(speed_frame, from_=1, to=100, orient=HORIZONTAL,
              variable=self.solve_speed_var, length=100,
              bg=self.bg_color, fg=self.fg_color,
              troughcolor=self.accent_color, highlightbackground=self.bg_color).grid(row=1, column=1, pady=1)

        # Action buttons
        button_frame = Frame(self.control_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=5)

        self.new_maze_button = Button(button_frame, text="New", command=self.create_maze,
              width=10, bg=self.accent_color, fg=self.fg_color,
              activebackground=self.bg_color, activeforeground=self.fg_color)
        self.new_maze_button.pack(pady=2)

        self.solve_button = Button(button_frame, text="Solve", command=self.solve_maze,
              width=10, bg=self.accent_color, fg=self.fg_color,
              activebackground=self.bg_color, activeforeground=self.fg_color,
              state="disabled")  # Initially disabled
        self.solve_button.pack(pady=2)

        # Status label
        self.status_label = Label(button_frame, text="Ready",
                                 bg=self.bg_color, fg=self.fg_color, wraplength=120)
        self.status_label.pack(pady=2)

    def create_maze(self):
        # Disable solve button and update status
        self.solve_button.config(state="disabled")
        self.status_label.config(text="Creating...")

        # Disable new maze button during creation
        self.new_maze_button.config(state="disabled")

        # Get current values from controls
        self.num_rows = self.rows_var.get()
        self.num_cols = self.cols_var.get()
        self.maze_speed = self.maze_speed_var.get() / 10.0
        self.solve_speed = self.solve_speed_var.get() / 10.0

        # Clear the canvas before creating a new maze
        self.win.clear()

        # Calculate cell size based on window dimensions
        # This ensures all elements scale proportionally
        available_width = self.screen_x - 2 * self.margin
        available_height = self.screen_y - 2 * self.margin

        # Calculate cell size to fit within available space
        cell_size_x = available_width / self.num_cols
        cell_size_y = available_height / self.num_rows

        # Ensure cells maintain proper aspect ratio
        if cell_size_x > cell_size_y * 1.5:
            # Width is too large compared to height
            cell_size_x = cell_size_y * 1.5
        elif cell_size_y > cell_size_x * 1.5:
            # Height is too large compared to width
            cell_size_y = cell_size_x * 1.5

        # Create new maze with callback
        self.maze = Maze(
            self.margin, self.margin,
            self.num_rows, self.num_cols,
            cell_size_x, cell_size_y,
            self.win,
            maze_speed=self.maze_speed,
            solve_speed=self.solve_speed,
            on_maze_created_callback=self.on_maze_created
        )



    def on_maze_created(self):
        """Called when maze creation is complete"""
        # Enable solve button and update status
        self.solve_button.config(state="normal")
        self.status_label.config(text="Ready to solve")

        # Re-enable new maze button
        self.new_maze_button.config(state="normal")

    def solve_maze(self):
        # Update status
        self.status_label.config(text="Solving...")

        # Disable buttons during solving
        self.solve_button.config(state="disabled")
        self.new_maze_button.config(state="disabled")

        # Update speeds in case they changed
        self.maze.maze_speed = self.maze_speed_var.get() / 10.0
        self.maze.solve_speed = self.solve_speed_var.get() / 10.0

        # Solve the maze
        result = self.maze.solve()

        # Update status and re-enable buttons
        if result:
            self.status_label.config(text="Solved!")
        else:
            self.status_label.config(text="No solution")

        self.new_maze_button.config(state="normal")

    def apply_window_size(self):
        """Apply the window size from the entry fields"""
        try:
            # Get the new window size
            new_width = max(400, min(3840, self.width_var.get()))
            new_height = max(300, min(2160, self.height_var.get()))

            # Update the entry fields with validated values
            self.width_var.set(new_width)
            self.height_var.set(new_height)

            # Update screen dimensions
            self.screen_x = new_width
            self.screen_y = new_height

            # Update margin based on new window size
            self.margin = int(min(new_width, new_height) * 0.05)

            # Recreate the window with new dimensions
            if hasattr(self, 'win'):
                # Remove old window
                self.maze_frame.winfo_children()[0].destroy()

                # Create new window
                self.win = Window(self.screen_x, self.screen_y, master=self.maze_frame)

            # Update status
            self.status_label.config(text="Size applied")

        except ValueError:
            # Handle invalid input
            self.status_label.config(text="Invalid size")

            # Reset to current values
            self.width_var.set(self.screen_x)
            self.height_var.set(self.screen_y)

def main(width=1280, height=720):
    root = tk.Tk()
    app = MazeApp(root, width=width, height=height)
    root.mainloop()

if __name__ == "__main__":
    main()
