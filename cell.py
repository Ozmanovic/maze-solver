from graphics import Line, Point


class Cell():
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window    
        self.visited = False
    
    def draw(self, x1, x2, y1, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        if self.__win:
            # LEFT wall
            line = Line(Point(x1, y1), Point(x1, y2))
            if self.has_left_wall:
                self.__win.draw_line(line)
            else:
                self.__win.draw_line(line, "#d9d9d9")

            # TOP wall
            line = Line(Point(x1, y1), Point(x2, y1))
            if self.has_top_wall:
                self.__win.draw_line(line)
            else:
                self.__win.draw_line(line, "#d9d9d9")

            # RIGHT wall
            line = Line(Point(x2, y1), Point(x2, y2))
            if self.has_right_wall:
                self.__win.draw_line(line)
            else:
                self.__win.draw_line(line, "#d9d9d9")

            # BOTTOM wall
            line = Line(Point(x1, y2), Point(x2, y2))
            if self.has_bottom_wall:
                self.__win.draw_line(line)
            else:
                self.__win.draw_line(line, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        x1 = (self.__x1 + self.__x2) / 2
        y1 = (self.__y1 + self.__y2) / 2
        x2 = (to_cell.__x1 + to_cell.__x2) / 2
        y2 = (to_cell.__y1 + to_cell.__y2) / 2

        color = "gray" if undo else "red"
        line = Line(Point(x1, y1), Point(x2, y2))
        if self.__win:
            self.__win.draw_line(line, color)
