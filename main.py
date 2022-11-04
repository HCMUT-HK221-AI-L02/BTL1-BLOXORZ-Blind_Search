# Info
# Đây là file main để giải bài toán Bloxorz
# ----------------------------------------------------------------
# Import các file và thư viện liên quan
from app.ga_solver import GA_Solver
from app.dfs_solver import DFS_Solver
from app.terrain import Terrain
from app.move import Move
import sys
import time
import json
import os
import psutil


def print_path(paths):
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


def main():
    # Thông tin sơ bộ:
    print("Thuat toan DFS giai duoc map 01->27.")
    print("Thuat toan GA giai duoc map 01->04.")
    level_file: str = input("Nhap file input (VD: level/level01.txt): ")
    try:
        open(level_file, 'rb')
    except OSError:
        print("Puzzle khong ton tai.")
        sys.exit()
    terrain = Terrain(level_file)
    
    # Chọn thuật toán
    algorithm: str = input ("Chon thuat toan, nhap DFS hoặc GA: ")
    if algorithm == "DFS":
        if int(level_file[11:13]) > 27:
            print("Map nam ngoai kha nang giai cua thuat toan DFS.")
            sys.exit()
        else:
            process = psutil.Process(os.getpid())
            print("-------------------Giai bai toan-------------------------")
            print("Start at: " + str(terrain.start))
            print("End at: " + str(terrain.goal))
            start_time = time.time()
            solver = DFS_Solver()
            paths = solver.solve(terrain)

    elif algorithm == "GA":
        if int(level_file[11:13]) > 4:
            print("Map nam ngoai kha nang giai cua thuat toan GA.")
            sys.exit()
        else:
            process = psutil.Process(os.getpid())
            print("-------------------Giai bai toan-------------------------")
            # Đọc file config của GA
            f = open("app/ga_config.json", 'r')
            jsontext = json.loads(f.read())
            mem_number = jsontext["mem_number"]
            select_rate = jsontext["select_rate"]
            duplicate_rate = jsontext["duplicate_rate"]
            evo_rate = jsontext["evo_rate"]
            f.close()
            # Giải bài toán
            print("Start at: " + str(terrain.start))
            print("End at: " + str(terrain.goal))
            start_time = time.time()
            solver = GA_Solver(mem_number, select_rate, duplicate_rate, evo_rate)
            paths = solver.solve(terrain)
    
    else:
        print("Thuat toan nhap vao khong ton tai.")
        sys.exit()

    # Xuất kết quả cuối cùng:
    print("----------------------------------------------------")
    print("Thoi gian: %s giay" % (time.time() - start_time))
    print("Ton bo nho:", process.memory_info().rss / (1024 * 1024), "MB")
    print("Ket qua: ", print_path(paths))


if __name__ == '__main__':
    main()
    