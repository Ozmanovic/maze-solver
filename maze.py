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
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        if seed != None:
            random.seed(seed)

        self.__create_cells()

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
            self.animate()

    def animate(self):
        if self.__win:
            self.__win.redraw()
            time.sleep(0.05)


    def __break_entrance_and_exit(self):
        cell = self._cells[0][0]
        cell.has_top_wall = False
        self.__draw_cell(0, 0)
        last_col = len(self._cells) -1
        last_row = len(self._cells[0]) - 1
        cell2 = self._cells[last_col][last_row]
        cell2.has_bottom_wall = False
        self.__draw_cell(last_col, last_row)

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
            self.__draw_cell(self._cells[i][j])
            return
        else:
            random_i, random_j, neighbour = random.choice(need_visit)
            if random_i == i + 1:  # right
                current.has_right_wall = False
                neighbour.has_left_wall = False
            elif random_i == i - 1:  # left
                current.has_left_wall = False
                neighbour.has_right_wall = False
            elif random_j == j + 1:  # down
                current.has_bottom_wall = False
                neighbour.has_top_wall = False
            elif random_j == j - 1:  # up
                current.has_top_wall = False
                neighbour.has_bottom_wall = False
                
            neighbour.__break_walls_r(random_i, random_j)
                    





