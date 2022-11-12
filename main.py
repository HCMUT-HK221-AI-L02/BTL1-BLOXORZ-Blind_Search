# Info
# Đây là file main để giải bài toán Bloxorz
# ----------------------------------------------------------------
# Import các file và thư viện liên quan
from app.block import Block
from app.ga_solver import GA_Solver
from app.dfs_solver import DFS_Solver
from app.terrain import Terrain
from app.move import Move

import sys
import time
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

def export_log(paths, level_file, time, mem, algo):
    terrain = Terrain(level_file)
    list = exe_paths(paths, terrain)
    log_file = "log/" + algo + level_file[5:13] + ".txt"
    f = open(log_file, "w")
    f.write("Algorithm: " + algo + "\n")
    f.write("Time Consuming: " + str(time) + " Secs\n")
    f.write("Memory Consuming: " + str(mem) + " MB\n")
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
    
def exe_paths(paths, terrain):
    block = Block(terrain.start, terrain.start)
    map = terrain.map
    list = []
    list.append((None, block, map))
    for step in paths:
        if step is None: continue
        elif step == Move.Right:
            block = block.right()
        elif step == Move.Left:
            block = block.left()
        elif step == Move.Up:
            block = block.up()
        elif step == Move.Down:
            block = block.down()
        elif step == Move.Space:
            block = block.switch()
        
        if terrain.can_hold(block, map):
            (map, block) = terrain.touch_special_cell(block, map)
            if block.control != None: block = block.join_block()
            list.append((step, block, map))
    return list

def main():
    # Thông tin sơ bộ:
    level_file: str = input("Nhap file input (VD: level/level01.json): ")
    try:
        open(level_file, 'rb')
    except OSError:
        print("Puzzle khong ton tai.")
        sys.exit()
    terrain = Terrain(level_file)
    
    # Chọn thuật toán
    algorithm: str = input ("Chon thuat toan, nhap DFS hoặc GA: ")
    if algorithm == "DFS":
        if int(level_file[11:13]) > 33:
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
        if int(level_file[11:13]) > 33:
            print("Map nam ngoai kha nang giai cua thuat toan GA.")
            sys.exit()
        else:
            process = psutil.Process(os.getpid())
            print("-------------------Giai bai toan-------------------------")
            # Giải bài toán
            print("Start at: " + str(terrain.start))
            print("End at: " + str(terrain.goal))
            start_time = time.time()
            solver = GA_Solver()
            paths = solver.solve(terrain)
    
    else:
        print("Thuat toan nhap vao khong ton tai.")
        sys.exit()

    # Xuất kết quả cuối cùng:
    time_consuming = time.time() - start_time
    mem_consuming = process.memory_info().rss / (1024 * 1024)
    export_log(paths, level_file, time_consuming, mem_consuming, algorithm)
    print("----------------------------------------------------")
    print("Thoi gian: %s giay" % time_consuming)
    print("Ton bo nho:", mem_consuming, "MB")
    print("Ket qua: ", print_path(paths))


if __name__ == '__main__':
    main()
    