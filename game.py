# Info
# Đây là model giải game Bloxorz bằng thuật toán deep first search
# ----------------------------------------------------------------
# Import các file và thư viện liên quan
from app.dfs_solver import DFS_Solver
from app.terrain import Terrain
from app.move import Move
import time

# Định nghĩa class Game để làm model giải bài toán
class Game:
    # Object mô hình giải bài toán, được xác định bởi obj terrain và obj solver
    def __init__(self, terrain):
        self.terrain = terrain
        self.solver = DFS_Solver()

    def solve_game(self, level_file):
        print("-------------------Giai bai toan-------------------------")
        start_time = time.time()
        (paths, list) = self.solver.solve(self.terrain)
        time_consuming = time.time() - start_time
        print("Time: %s seconds" % (time_consuming))
        print("Solution: ", self.print_path(paths, level_file))
        self.export_log(list, level_file, time_consuming)

    def print_path(self, paths, level_file):
        sol_file = "result" + level_file[5:13] + ".txt"
        f = open(sol_file, "w")
        # Chuyển list gồm các obj moves thành string kết quả
        path_str = ""
        for i, path in enumerate(paths):
            if path is None:
                continue
            elif path == Move.Right:
                path_str = path_str + " Right "
                f.write(str(i) + "_Right\n")
            elif path == Move.Left:
                path_str = path_str + " Left "
                f.write(str(i) + "_Left\n")
            elif path == Move.Down:
                f.write(str(i) + "_Down\n")
                path_str = path_str + " Down "
            elif path == Move.Up:
                f.write(str(i) + "_Up\n")
                path_str = path_str + " Up "
            elif path == Move.Space:
                f.write(str(i) + "_Space\n")
                path_str = path_str + " Space "
            if i < len(paths) - 1:
                path_str = path_str + "->"
        f.close()
        return path_str

    def export_log(self, list, level_file, time):
        log_file = "log" + level_file[5:13] + ".txt"
        f = open(log_file, "w")
        f.write("Time Consuming: " + str(time) + " Secs\n")
        log_step = """\nSTEP {}
    Block Positions: p1: [{},{}], p2: [{},{}]
    Block Control: {}
    Move: {}

"""
        for i in range(0, len(list)):
            f.write(log_step.format(i, list[i][1].p1.x, list[i][1].p1.y, list[i][1].p2.x, list[i][1].p2.y, list[i][1].control, list[i][0]))
            for row in list[i][2]:
                map_log = "\t"
                for elem in row:
                    map_log += str(elem) + " "
                map_log += "\n"
                f.write(map_log)
            f.write("====================================\n")
        f.close()


# Chạy kết quả
if __name__ == '__main__':
    lv_input = input("Vui long nhap level man choi: ")

    level_file = "level/" + lv_input + ".json"
    # Tạo obj terrain
    terrain = Terrain(level_file)
    print("Start at: " + str(terrain.start))
    print("End at: " + str(terrain.goal))
    # Tạo obj game
    game = Game(terrain)

    # Giải bài toán vào xuất kết quả
    game.solve_game(level_file)