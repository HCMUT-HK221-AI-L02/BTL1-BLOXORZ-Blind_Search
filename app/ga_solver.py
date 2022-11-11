# Import các file và thư viện liên quan
from app.terrain import Terrain
from app.member import Member
from app.ga_fitness import *
from app.ga_penaltymap import PenaltyMap
from app.ga_config2 import *
from random import choice, choices

# Định nghĩa class GA_Solver
class GA_Solver:
    # Class này nhằm giải bài toán, sử dụng dữ liệu đầu vào là terrain được tạo ban đầu,
    # cùng các tham số về GA, xuất kết quả solve là paths
    def __init__(self):
        return

    def solve(self, terrain: Terrain):
        """
        * Bước đầu tiên
        + Nhập vào terrain
        + Tạo quần thể
        + Tạo list chứa đáp án
        + Tạo biến đếm tổng ID
        + Tạo biến đếm thế hệ
        """
        self.terrain = terrain
        path = []
        population = []
        sID = 0
        gen_count = 0
        env = PenaltyMap(terrain.map)

        # Khởi tạo dân số đầu tiên, có số dân số là SELECTION_RATE*MEM_NUMBER
        for i in range(int(SELECTION_RATE*MEM_NUMBER)):
            sID = sID + 1
            newMem = Member(sID)
            population.append(newMem)

        #----------------------------------------------------------------
        # Tạo vòng lặp cho đến khi tìm thấy kết quả
        while len(path) == 0:
            gen_count = gen_count + 1
            # Tạo thêm member
            l = len(population)
            newPopulation = []
            for i in range(l):
                # Tạo thêm 4 mem con và ký hiệu 5 mem này
                mem_family = []
                mem_family.append(population[i])
                for j in range(4):
                    sID = sID + 1
                    newMem = Member(sID, mem_family[0].path)    
                    mem_family.append(newMem)
                # family này, mỗi con đi thêm 1 bước trong [LRUDS]
                mem_family[0].take_step('Space')
                mem_family[1].take_step('Left')
                mem_family[2].take_step('Right')
                mem_family[3].take_step('Up')
                mem_family[4].take_step('Down')
                # Check fitness cho family
                for j in range(5):
                    if checkFitness(mem_family[j], self.terrain, env) == True:
                        newPopulation.append(mem_family[j])
                        # Check có đáp án
                        if mem_family[j].reach_goal == True:
                            path = mem_family[j].path
                            return path
            # Đổi population thành new population
            population = newPopulation                               
            

            # Thực hiện chọn lọc tự nhiên cho đến khi mất một số lượng nhất định
            #  + Tính tỉ lệ bị select
            kill_select_rate = []
            for mem in population:
                kill_select_rate.append(1/mem.fitness)
            #  + loại trừ
            select_number = len(population) - int(SELECTION_RATE*MEM_NUMBER)
            if select_number > 0:
                for i in range(select_number):
                    pick = choices(population, weights = kill_select_rate, k = 1)
                    pick_idx = population.index(pick[0])
                    population.pop(pick_idx)
                    kill_select_rate.pop(pick_idx)


            # Thực hiện mutation, tính lại fitness
            # Tỉ lệ một cá thể bị đột biến là bằng nhau
            evo_number = int(len(population)*EVO_RATE)
            for i in range(evo_number):
                mem = choice(population)
                mem.evo()
                checkFitness(mem, self.terrain, env)


            # Cập nhật lại môi trường
            for mem in population:
                env.update(mem.p1)
                env.update(mem.p2)


            # In kết quả đại diện cho generation:
            max_fitness = population[0].fitness
            best_mem = population[0]
            for mem in population: 
                if mem.fitness > max_fitness: best_mem = mem
            print("--------------------------------")
            print("Generation: ", gen_count)
            print("Best member ID: ", best_mem.id)
            print("Max Fitness: ", best_mem.fitness)
            # print("Path: ", best_mem.print_path())
            print("Best member p1: ", best_mem.p1)
            print("Best member p2: ", best_mem.p2)


            # Log file to Debug
            debug_log = "debug/debug.txt"
            # Clear file 
            with open(debug_log, 'w') as file:
                pass
            # Draw penalty map
            f = open(debug_log, 'w')
            f.write("===================Penalty Map===================")
            f.write("\n")
            for x in range(0,env.height):
                for y in range(0, env.width):
                    f.write(f'{env.pMap[x][y]:.3f}' + "\t")
                f.write("\n")
            f.write("===================ID - P1 - P2===================")
            f.write("\n")
            for i in range(0,len(population)):
                str1 = str(i + 1) + "\t" + str(population[i].id) + "\t" + str(population[i].p1) + "\t" + str(population[i].p2)
                f.write(str1 + "\n")
            f.close()




