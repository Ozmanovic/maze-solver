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
        
        
        m._Maze__break_entrance_and_exit()

        entrance_cell = m._cells[0][0]
        exit_cell = m._cells[num_cols - 1][num_rows - 1]

        self.assertFalse(entrance_cell.has_top_wall)
        self.assertFalse(exit_cell.has_bottom_wall)

    def test_cells_initially_not_visited(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        for col in m._cells:
            for cell in col:
                self.assertFalse(cell.visited)

    def test_some_cells_marked_visited(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        m._cells[0][0].visited = True
        m._cells[1][1].visited = True
        self.assertTrue(m._cells[0][0].visited)
        self.assertTrue(m._cells[1][1].visited)

    def test_reset_cells_visited(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        
        for col in m._cells:
            for cell in col:
                cell.visited = True

        m._Maze__reset_cells_visited()  

        for col in m._cells:
            for cell in col:
                self.assertFalse(cell.visited)

    def test_all_cells_visited_after_break_walls(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        m._Maze__break_walls_r(0, 0)

        for col in m._cells:
            for cell in col:
                self.assertTrue(cell.visited)

    def test_wall_removed_between_two_cells(self):
        m = Maze(0, 0, 1, 2, 10, 10)  # 2 cols, 1 row
        m._Maze__break_walls_r(0, 0)

        cell1 = m._cells[0][0]
        cell2 = m._cells[1][0]

        
        self.assertTrue(
            (not cell1.has_right_wall and not cell2.has_left_wall) or
            (not cell2.has_right_wall and not cell1.has_left_wall)
        )

    def test_no_invalid_wall_removal(self):
        m = Maze(0, 0, 2, 2, 10, 10)
        m._Maze__break_walls_r(0, 0)

        for i in range(m.num_cols):
            for j in range(m.num_rows):
                cell = m._cells[i][j]
                self.assertIn(cell.has_top_wall, [True, False])
                self.assertIn(cell.has_bottom_wall, [True, False])
                self.assertIn(cell.has_left_wall, [True, False])
                self.assertIn(cell.has_right_wall, [True, False])





if __name__ == "__main__":
    unittest.main()