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
    def __init__(self, mem_number, duplicate_rate, penalty_rate, evo_rate):
        self.mem_number = mem_number
        self.duplicate_rate = duplicate_rate
        self.penalty_rate = penalty_rate
        self.evo_rate = evo_rate

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
        env = PenaltyMap(terrain.map, self.penalty_rate)

        # Khởi tạo dân số đầu tiên, có số dân số là 

        #----------------------------------------------------------------
        # Tạo vòng lặp cho đến khi tìm thấy kết quả
        while len(path) == 0:
            gen_count = gen_count + 1
            # Tạo thêm member cho đủ số lượng
            while len(population) < self.mem_number:
                sID = sID + 1
                newMem = Member(sID)
                population.append(newMem)
            
            # Mỗi member đi thêm một bước
            newPopulation = []
            for mem in population:
                mem.take_step()
                # Check Out of Bound và tính fitness
                if checkFitness(mem, self.terrain, env) == True:
                    newPopulation.append(mem)
                    # Check có đáp án
                    if mem.reach_goal == True:
                        path = mem.path
                        return path
            population = newPopulation

            # Thực hiện duplicate cho đến khi đủ dân số
            if len(population) < self.mem_number:
                duplicate_select_rate = []
                new_child = []
                for mem in population: duplicate_select_rate.append(mem.fitness)                
                for i in range(int(self.duplicate_rate*len(population))):
                    sID = sID + 1
                    p = choices(population, weights = duplicate_select_rate, k = 1)[0]
                    child = Member(sID, path = p.path)
                    new_child.append(child)
                population.extend(new_child)
            
            # Thực hiện mutation, tính lại fitness
            # Tỉ lệ một cá thể bị đột biến là bằng nhau
            evo_number = int(len(population)*self.evo_rate)
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
            print("Path: ", best_mem.print_path())

