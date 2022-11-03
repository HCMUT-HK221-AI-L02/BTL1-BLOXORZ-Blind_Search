# Info
# Đây là model giải game Bloxorz bằng thuật toán Genetic Algorithm
# ----------------------------------------------------------------
# Import các file và thư viện liên quan
from app.ga_solver import GA_Solver
from app.terrain import Terrain
from app.move import Move
import time

# Định nghĩa class Game để làm model giải bài toán
class Game:
    # Object mô hình giải bài toán, được xác định bởi obj terrain và obj solver
    def __init__(self, terrain, mem_number, select_rate, evo_rate):
        self.terrain = terrain
        self.solver = GA_Solver(mem_number, select_rate, evo_rate)

    def solve_game(self):
        print("-------------------Giai bai toan-------------------------")
        start_time = time.time()
        paths = self.solver.solve(self.terrain)
        print("----------------------------------------------------")
        print("Time: %s seconds" % (time.time() - start_time))
        print("Solution: ", self.print_path(paths))

    def print_path(self, paths):
        # Chuyển list gồm các obj moves thành string kết quả
        path_str = ""
        for i, path in enumerate(paths):
            if path is None:
                continue
            elif path == Move.Right:
                path_str = path_str + " Right "
            elif path == Move.Left:
                path_str = path_str + " Left "
            elif path == Move.Down:
                path_str = path_str + " Down "
            elif path == Move.Up:
                path_str = path_str + " Up "
            elif path == Move.Space:
                path_str = path_str + " Space "
            if i < len(paths) - 1:
                path_str = path_str + "->"
        return path_str

# Chạy kết quả
if __name__ == '__main__':
    # Tạo obj terrain
    terrain = Terrain(level_file = "level/level04.txt")
    mem_number = 1000
    select_rate = 0.2
    evo_rate = 0.01
    print("Start at: " + str(terrain.start))
    print("End at: " + str(terrain.goal))
    # Giải bài toán và xuất kết quả
    game = Game(terrain, mem_number, select_rate, evo_rate)
    game.solve_game()