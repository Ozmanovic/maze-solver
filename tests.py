import unittest
from maze import Maze
from cell import Cell


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_small_maze(self):
        m = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m._cells), 1)
        self.assertEqual(len(m._cells[0]), 1)


    def test_square_maze(self):
        m = Maze(0, 0, 5, 5, 10, 10)
        self.assertEqual(len(m._cells), 5)
        self.assertEqual(len(m._cells[0]), 5)

    def test_wide_maze(self):
        m = Maze(0, 0, 5, 10, 10, 10)
        self.assertEqual(len(m._cells), 10)
        self.assertEqual(len(m._cells[0]), 5)



    def test_cell_instances(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        for col in m._cells:
            for cell in col:
                self.assertIsInstance(cell, Cell)

    def test_break_entrance_and_exit(self):
        num_cols = 4
        num_rows = 4
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        
        # Call the private method using name mangling
        m._Maze__break_entrance_and_exit()

        entrance_cell = m._cells[0][0]
        exit_cell = m._cells[num_cols - 1][num_rows - 1]

        self.assertFalse(entrance_cell.has_top_wall)
        self.assertFalse(exit_cell.has_bottom_wall)



if __name__ == "__main__":
    unittest.main()