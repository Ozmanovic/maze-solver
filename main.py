from graphics import Window, Point, Line
from cell import Cell

def main():
    win = Window(800, 600)

    # Draw a line
    p1 = Point(35, 50)
    p2 = Point(120, 200)
    line = Line(p1, p2)
    win.draw_line(line, "red")

    

    # Draw cells
    # Draw cells
    cell1 = Cell(win)
    cell1.draw(100, 150, 100, 150)

    cell2 = Cell(win)
    cell2.draw(160, 210, 100, 150)

    cell3 = Cell(win)
    cell3.draw(100, 150, 160, 210)

    cell4 = Cell(win)
    cell4.draw(160, 210, 160, 210)

    # Draw move from cell1 to cell2
    cell1.draw_move(cell2, undo=False)


    win.wait_for_close()


main()