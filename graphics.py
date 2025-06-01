from tkinter import Tk, BOTH, Canvas, Frame

class Window:
    def __init__(self, width, height, master=None):
        self.window_running = False

        if master:
            self.__root = master
            self.__canvas = Canvas(self.__root, width=width, height=height, bg="black")
            self.__canvas.pack(fill=BOTH, expand=True)
            # When used within another window, we don't need to handle window closing
        else:
            self.__root = Tk()
            self.__root.title("Maze Solver")
            self.__root.geometry(f"{width}x{height}")
            self.__root.configure(bg="black")

            # Fix window size to prevent dynamic resizing
            self.__root.resizable(False, False)

            # Create canvas with fixed size
            self.__canvas = Canvas(self.__root, width=width, height=height, bg="black")
            self.__canvas.pack(fill=BOTH, expand=True)

            # Only set protocol for the main window
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


    def clear(self):
        """Clear all drawings from the canvas"""
        self.__canvas.delete("all")

    def force_update(self):
        """Force an immediate update of the window"""
        self.__root.update()
        self.__root.update_idletasks()

    def get_size(self):
        """Get the current size of the canvas"""
        if self.__canvas.winfo_ismapped():
            return (self.__canvas.winfo_width(), self.__canvas.winfo_height())
        else:
            return (self.__canvas.winfo_reqwidth(), self.__canvas.winfo_reqheight())

    def bind_resize_handler(self, callback):
        """Bind a function to handle window resize events"""
        if not self.__root:
            return

        def on_resize(event):
            # Only trigger if it's a genuine resize (not just a redraw)
            if event.width != self.__canvas.winfo_width() or event.height != self.__canvas.winfo_height():
                # Update canvas size
                callback(event.width, event.height)

        # Bind to the Configure event of the canvas
        self.__canvas.bind("<Configure>", on_resize)

    def draw_line(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="white"):

        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
            )




