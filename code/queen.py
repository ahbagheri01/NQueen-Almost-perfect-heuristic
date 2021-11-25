import copy
import datetime
import numpy as np
class CSP:
    def __init__(self,n):
        self.startbound = n
        self.endbound = -n + 1
        self.size = n
        self.grid = np.zeros((n, n), bool)
        self.turn = 0
        self.min_free_col = n
        self.min_free_row = n
        middle = self.size // 2
        col_list = [0] * self.size
        counter = 0
        for i in range(middle):
            col_list[counter] = i
            counter += 1
            col_list[counter] = self.size - i - 1
            counter += 1
        if self.size % 2 == 1:
            col_list[counter] = middle
        self.from_start = col_list
        middle = self.size // 2
        col_list = [0] * self.size
        counter = 0
        col_list[counter] = middle
        counter += 1
        for i in range(1, middle):
            col_list[counter] = middle + i
            counter += 1
            col_list[counter] = middle - i
            counter += 1
        col_list[counter] = 0
        counter += 1
        if self.size % 2 == 1:
            col_list[counter] = self.size - 1
        self.from_middle = col_list
        self.underattacks = np.zeros((n, n), bool)
        self.free_count_cols = {i: set() for i in range(n)}
        self.free_count_cols[n] = set(range(n))
        self.number_col_free_each= [n] * n
        self.number_row_free_each = [n] * n
        self.free_count_rows = {i: set() for i in range(n)}
        self.free_count_rows[n] = set(range(n))
        self.starttime = datetime.datetime.now()

    def save_ans(self):
        result = "NQueen = " + str(self.size) + "\n"
        result += "start time : " + str(self.starttime) + "\n"
        board = ""
        result += "finish time : " + str(endtime := datetime.datetime.now()) + "\n"
        result += "duration : " + str(endtime - self.starttime) + "\n"
        result += "result chessboard : " + "\n"
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[(i, j)]:
                    board+="o"

                else:
                    board += "-"
            board += "\n"
        result+=copy.deepcopy(board)
        f = open("result(n=" + str(self.size) + ").txt", 'w')
        f.write(result)
        f.close()
        print(board)
    def is_it_possible(self,index):
        return not (len(self.free_count_rows[index]) == self.size or
                len(self.free_count_cols[index]) == self.size)
    def select_row_col(self):
        if (self.min_free_col < 4 and
                self.min_free_row > self.min_free_col):
            for index in self.free_count_cols[self.min_free_col]:
                return index,'c'
        for index in self.free_count_rows[self.min_free_row]:
            return  index,'r'
    def get_col_base_row(self, row_index):
        if self.size/ 3 < row_index < 2 * self.size/3:
            return self.from_start
        return self.from_middle
    def attack_to_safe_cells(self, points, not_attacked_cells):
        points = tuple(points)
        row, col = points
        if not (0 <= row < self.size and 0 <= col < self.size):
            return
        if not self.underattacks[points]:
            not_attacked_cells.append(points)
            self.underattacks[points] = True

            cols_free_count = self.number_col_free_each[col]
            self.free_count_cols[cols_free_count].remove(col)
            self.free_count_cols[cols_free_count-1].add(col)
            if len(self.free_count_cols[cols_free_count]) == 0:
                if cols_free_count - 1 == 0:
                    for i in range(1, self.size):
                        if len(self.free_count_cols[i]) != 0:
                            self.min_free_col = i
                            break
                else:
                    self.min_free_col = min(self.min_free_col, cols_free_count)
            self.number_col_free_each[col] = cols_free_count - 1

            rows_free_count = self.number_row_free_each[row]
            self.free_count_rows[rows_free_count].remove(row)
            self.free_count_rows[rows_free_count - 1].add(row)
            if len(self.free_count_rows[rows_free_count]) == 0:
                if rows_free_count - 1 == 0:
                    for i in range(1, self.size):
                        if len(self.free_count_rows[i]) != 0:
                            self.min_free_row = i
                            break
                else:
                    self.min_free_row = min(self.min_free_row, rows_free_count - 1)
            self.number_row_free_each[row] = rows_free_count - 1
    def go_to_prevoius(self, safe_cells, new_queens):
        for pos in new_queens:
            self.grid[pos] = False
            self.turn -= 1

        for row, col in safe_cells:
            self.underattacks[(row, col)] = False

            cols_free_count = self.number_col_free_each[col]
            self.free_count_cols[cols_free_count].remove(col)
            self.free_count_cols[cols_free_count + 1].add(col)
            if len(self.free_count_cols[cols_free_count]) == 0:
                self.min_free_col = min(self.min_free_col, cols_free_count + 1)
            self.number_col_free_each[col] = cols_free_count + 1

            rows_free_count = self.number_row_free_each[row]
            self.free_count_rows[rows_free_count].remove(row)
            self.free_count_rows[rows_free_count + 1].add(row)
            if len(self.free_count_rows[rows_free_count]) == 0:
                self.min_free_row = min(self.min_free_row, rows_free_count + 1)
            self.number_row_free_each[row] = rows_free_count + 1
    def backtrack(self):
        if self.turn == self.size:
            self.save_ans()
            return True
        if self.is_it_possible(0):
            index,type = self.select_row_col()
            if type == 'r':
                for col in self.get_col_base_row(index):
                    if not self.underattacks[(index, col)]:
                        turn_holder = self.turn
                        prevoius,prevoius_q = self.add_queen(index, col)
                        if self.backtrack():
                            return True
                        self.go_to_prevoius(prevoius,prevoius_q)
                        self.turn = turn_holder
            else:
                for row in range(self.size):
                    if not self.underattacks[(row, index)]:
                        prevoius,prevoius_q = self.add_queen(row, index)
                        if self.backtrack():
                            return True
                        self.go_to_prevoius(prevoius,prevoius_q)
        return False
    def add_queen(self, row, col, safe_cells=None, new_queens=None):
        if new_queens is None:
            new_queens = []
        if safe_cells is None:
            safe_cells = []
        self.turn += 1
        self.grid[(row, col)] = True
        new_queens.append((row, col))
        for i in range(-self.size + 1, self.size):
            self.attack_to_safe_cells([row + i, col], safe_cells)
            self.attack_to_safe_cells([row + i, col + i], safe_cells)
            self.attack_to_safe_cells([row + i, col - i], safe_cells)
            self.attack_to_safe_cells([row, col + i], safe_cells)
        for row in list(self.free_count_rows[1]):
            for col in range(self.size):
                if not self.underattacks[(row, col)]:
                    self.add_queen(row, col, safe_cells, new_queens)
        for col in list(self.free_count_cols[1]):
            for row in range(self.size):
                if not self.underattacks[(row, col)]:
                    self.add_queen(row, col, safe_cells, new_queens)
        return safe_cells, new_queens

n = int(input())
nqueen = CSP(n)
nqueen.backtrack()