from tkinter import Tk, BOTH, Canvas

class Window: 
    def __init__(self, width, height):
        self.__root=Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")  
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack()
        self.window_running=False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.window_running=True
        while self.window_running == True:
            self.redraw()

    def close(self):
        self.window_running = False
        

    def draw_line(self, line, fill_color="black"):
        
        line.draw(self.__canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="red"):
        
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
            )


  

        