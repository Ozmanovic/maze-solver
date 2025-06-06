from cell import Cell
from graphics import Window
import time
import random

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
        maze_speed=5.0,  # Speed factor for maze creation
        solve_speed=1.0,  # Speed factor for solving
        on_maze_created_callback=None,  # Callback function when maze is created
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        self.maze_speed = maze_speed
        self.solve_speed = solve_speed
        self.is_maze_created = False
        self.on_maze_created_callback = on_maze_created_callback

        if seed != None:
            random.seed(seed)

        self.__create_cells()
        self.__break_walls_r(0, 0)
        self.__break_entrance_and_exit()
        self.__reset_cells_visited()

        # Mark maze as created and call callback if provided
        self.is_maze_created = True
        if self.on_maze_created_callback:
            self.on_maze_created_callback()


    def __create_cells(self):

        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                cell = Cell(self.__win)
                col.append(cell)
            self._cells.append(col)

        if self.__win:
            for i in range(self.num_cols):
                for j in range(self.num_rows):
                    self.__draw_cell(i, j)

        self.__break_entrance_and_exit()

    def __draw_cell(self, i, j):
        x1_cell = self.x1 + i * self.cell_size_x
        y1_cell = self.y1 + j * self.cell_size_y
        x2_cell = x1_cell + self.cell_size_x
        y2_cell = y1_cell + self.cell_size_y
        self.cell = self._cells[i][j]
        if self.__win:
            self.cell.draw(x1_cell, x2_cell, y1_cell, y2_cell)
            self.animate(self.maze_speed)

    def animate(self, speed_factor=1.0):
        """
        Animate the maze with configurable speed
        speed_factor: 1.0 is normal speed, higher is faster, lower is slower
        """
        if self.__win:
            self.__win.redraw()
            base_delay = 0.02  # Base delay in seconds
            time.sleep(base_delay / speed_factor)

    def __break_entrance_and_exit(self):
        # Create entrance at top-left
        cell = self._cells[0][0]
        cell.has_top_wall = False
        self.__draw_cell(0, 0)

        # Draw green entrance wall
        if self.__win:
            # Calculate the top wall of the first cell
            x1_cell = self.x1 + 0 * self.cell_size_x
            y1_cell = self.y1 + 0 * self.cell_size_y

            # Draw a green line for the top wall
            from graphics import Line, Point
            entrance_line = Line(Point(x1_cell, y1_cell), Point(x1_cell + self.cell_size_x, y1_cell))
            self.__win.draw_line(entrance_line, "green")

        # Create exit at bottom-right
        last_col = len(self._cells) - 1
        last_row = len(self._cells[0]) - 1
        cell2 = self._cells[last_col][last_row]
        cell2.has_bottom_wall = False
        self.__draw_cell(last_col, last_row)

        # Draw green exit wall
        if self.__win:
            # Calculate the bottom wall of the last cell
            x1_cell = self.x1 + last_col * self.cell_size_x
            y1_cell = self.y1 + last_row * self.cell_size_y
            y_bottom = y1_cell + self.cell_size_y

            # Draw a green line for the bottom wall
            exit_line = Line(Point(x1_cell, y_bottom), Point(x1_cell + self.cell_size_x, y_bottom))
            self.__win.draw_line(exit_line, "green")

    def __break_walls_r(self, i, j):


        current = self._cells[i][j]
        current.visited = True

        need_visit = []
        if i + 1 < self.num_cols and not self._cells[i+1][j].visited:
            right = self._cells[i+1][j]
            need_visit.append((i + 1, j, right))
        if i - 1 >= 0 and not self._cells[i-1][j].visited:
            left = self._cells[i-1][j]
            need_visit.append((i - 1, j, left))
        if j - 1 >= 0 and not self._cells[i][j-1].visited:
            up = self._cells[i][j-1]
            need_visit.append((i, j- 1, up))
        if j + 1 < self.num_rows and not self._cells[i][j+1].visited:
            down = self._cells[i][j+1]
            need_visit.append((i, j+1, down))


        if not need_visit:
            self.__draw_cell(i, j)

            return
        else:
            random.shuffle(need_visit)

            for random_i, random_j, neighbour in need_visit:
                if not neighbour.visited:


                    if random_i == i + 1:  # right
                        current.has_right_wall = False
                        neighbour.has_left_wall = False
                        self.__draw_cell(i, j)
                        self.__draw_cell(random_i, random_j)
                    elif random_i == i - 1:  # left
                        current.has_left_wall = False
                        neighbour.has_right_wall = False
                        self.__draw_cell(i, j)
                        self.__draw_cell(random_i, random_j)
                    elif random_j == j + 1:  # down
                        current.has_bottom_wall = False
                        neighbour.has_top_wall = False
                        self.__draw_cell(i, j)
                        self.__draw_cell(random_i, random_j)
                    elif random_j == j - 1:  # up
                        current.has_top_wall = False
                        neighbour.has_bottom_wall = False
                        self.__draw_cell(i, j)
                        self.__draw_cell(random_i, random_j)

                    self.__break_walls_r(random_i, random_j)

    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _solve(self, i, j):
        print(f"Exploring cell ({i},{j})")
        self.animate(self.solve_speed)

        # Mark current cell as visited
        self._cells[i][j].visited = True

        # Check if we've reached the exit
        last_col = self.num_cols - 1
        last_row = self.num_rows - 1
        if i == last_col and j == last_row:
            print(f"Found exit at ({i},{j})!")
            return True

        # Try right
        if (i + 1 < self.num_cols and
            not self._cells[i+1][j].visited and
            not self._cells[i][j].has_right_wall):

            print(f"Moving right from ({i},{j}) to ({i+1},{j})")
            self._cells[i][j].draw_move(self._cells[i+1][j])
            self.animate(self.solve_speed)

            if self._solve(i+1, j):
                return True

            # Backtrack
            print(f"Backtracking from right ({i+1},{j}) to ({i},{j})")
            self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
            self.animate(self.solve_speed)

        # Try down
        if (j + 1 < self.num_rows and
            not self._cells[i][j+1].visited and
            not self._cells[i][j].has_bottom_wall):

            print(f"Moving down from ({i},{j}) to ({i},{j+1})")
            self._cells[i][j].draw_move(self._cells[i][j+1])
            self.animate(self.solve_speed)

            if self._solve(i, j+1):
                return True

            # Backtrack
            print(f"Backtracking from down ({i},{j+1}) to ({i},{j})")
            self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)
            self.animate(self.solve_speed)

        # Try left
        if (i - 1 >= 0 and
            not self._cells[i-1][j].visited and
            not self._cells[i][j].has_left_wall):

            print(f"Moving left from ({i},{j}) to ({i-1},{j})")
            self._cells[i][j].draw_move(self._cells[i-1][j])
            self.animate(self.solve_speed)

            if self._solve(i-1, j):
                return True

            # Backtrack
            print(f"Backtracking from left ({i-1},{j}) to ({i},{j})")
            self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
            self.animate(self.solve_speed)

        # Try up
        if (j - 1 >= 0 and
            not self._cells[i][j-1].visited and
            not self._cells[i][j].has_top_wall):

            print(f"Moving up from ({i},{j}) to ({i},{j-1})")
            self._cells[i][j].draw_move(self._cells[i][j-1])
            self.animate(self.solve_speed)

            if self._solve(i, j-1):
                return True

            # Backtrack
            print(f"Backtracking from up ({i},{j-1}) to ({i},{j})")
            self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
            self.animate(self.solve_speed)

        print(f"No path found from ({i},{j}), backtracking")
        # If we get here, no path was found
        return False

    def solve(self):
        if not self.is_maze_created:
            print("Cannot solve maze: Maze is still being created")
            return False

        print("\n--- STARTING MAZE SOLVER ---")
        print(f"Maze dimensions: {self.num_cols}x{self.num_rows}")
        print(f"Exit location: ({self.num_cols-1},{self.num_rows-1})")
        self.__reset_cells_visited()
        result = self._solve(0, 0)
        print(f"\nMaze solved: {result}")
        return result



