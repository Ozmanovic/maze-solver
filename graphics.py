from tkinter import Tk, BOTH, Canvas

class Window: 
    def __init__(self, width, height):
        self.__root=Tk()
        self.__root.title("My window")
        self.__root.geometry(f"{width}x{height}")  
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack
        self.window_running=False

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.window_running=True
        while self.window_running == True:
            self.redraw()

    def close(self):
        self.window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)


