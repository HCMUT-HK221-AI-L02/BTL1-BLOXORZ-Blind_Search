# Info
# Đây là model giải game Bloxorz bằng thuật toán deep first search

# ----------------------------------------------------------------
# Import các file và thư viện liên quan
from app.dfs_solver import DFS_Solver
from app.terrain import Terrain
import time


# Định nghĩa class Game để làm model giải bài toán
class Game:
    # Object mô hình giải bài toán, được xác định bởi obj terrain và obj solver
    def __init__(self, terrain):
        self.terrain = terrain
        self.solver = DFS_Solver()

    def solve_game(self):
        print("Giai bai toan ")
        start_time = time.time()
        paths = self.solver.solve(self.terrain)
        print("Time: %s seconds" % (time.time() - start_time))
        print("Solution: ", self.print_path(paths))

    def print_path(self, paths):
        # Chuyển list gồm các obj moves thành string kết quả
        path_str = ""

        return path_str

# Chạy kết quả
if __name__ == '__name__':
    # Tạo obj terrain
    terrain = Terrain(level_file = "level/level01.txt")
    # Tạo obj game
    game = Game(terrain)
    # Giải bài toán vào xuất kết quả
    game.solve_game