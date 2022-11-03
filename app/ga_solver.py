# Import các file và thư viện liên quan
from app.terrain import Terrain
from app.member import Member
from random import choice, choices

# Định nghĩa class GA_Solver
class GA_Solver:
    # Class này nhằm giải bài toán, sử dụng dữ liệu đầu vào là terrain được tạo ban đầu,
    # xuất kết quả solve là paths
    def __init__(self, mem_number, select_rate, duplicate_rate, evo_rate):
        self.mem_number = mem_number
        self.select_rate = select_rate
        self.duplicate_rate = duplicate_rate
        self.evo_rate = evo_rate

    def solve(self, terrain: Terrain):
        """
        * Bước đầu tiên
        + Nhập vào terrain
        + Tạo quần thể
        + Tạo list chứa đáp án
        + Tạo biến đếm tổng ID
        """
        self.terrain = terrain
        path = []
        population = []
        sID = 0
        gen_count = 0

        #----------------------------------------------------------------
        # Tạo vòng lặp cho đến khi tìm thấy kết quả
        while len(path) == 0:
            gen_count = gen_count + 1
            # Bù cho đủ số lượng
            while len(population) < self.mem_number:
                sID = sID + 1
                newMem = Member(sID)
                population.append(newMem)
            
            # Mỗi member đi thêm một bước
            newPopulation = []
            for mem in population:
                mem.take_step()
                # Check Out of Bound và tính fitness
                if mem.checkFitness(self.terrain) == True:
                    newPopulation.append(mem)
                    # Check có đáp án
                    if mem.reach_goal == True:
                        path = mem.path
                        return path
            population = newPopulation

            # # Thực hiện chọn lọc tự nhiên cho đến khi mất một số lượng nhất định
            # # Tính tỉ lệ bị select
            # kill_select_rate = []
            # for mem in population:
            #     kill_select_rate.append(1/mem.fitness)
            # # loại trừ
            # select_number = int(self.select_rate*len(population))
            # for i in range(select_number):
            #     pick = choices(population, weights = kill_select_rate, k = 1)
            #     pick_idx = population.index(pick[0])
            #     population.pop(pick_idx)
            #     kill_select_rate.pop(pick_idx)

            # --------------------------------
            # Cách 1

            # Thực hiện cross over cho đến khi đủ dân số
                # Nhớ tính fitness và check out of bound cho member mới
                # Check xem có đáp án
            if len(population) < self.mem_number:
                duplicate_select_rate = []
                new_child = []
                for mem in population: duplicate_select_rate.append(mem.fitness)                
                for i in range(int(self.duplicate_rate*len(population))):
                    sID = sID + 1
                    p = choices(population, weights = duplicate_select_rate, k = 1)[0]
                    child = Member(sID, path = p.path)
                    # child.checkFitness(self.terrain)
                    new_child.append(child)
                population.extend(new_child)

            # ----------------------------------------------------------------
            # Cách 2
            # cross_select_rate = []
            # population_path = []
            # new_child = []
            # population_count = len(population)
            # for mem in population:
            #     cross_select_rate.append(mem.fitness)
            #     population_path.append(mem.path)
            # while population_count < self.mem_number:
            #     p1 = choices(population_path, weights = cross_select_rate, k = 1)[0]
            #     p2 = choices(population_path, weights = cross_select_rate, k = 1)[0]
            #     min_len = min(len(p1), len(p2))
            #     if min_len == 0: keep_len = 0
            #     else: keep_len = choice(range(min_len))
            #     # Tạo con 1
            #     c1 = p1[:keep_len]
            #     c1.extend(p2[keep_len:])
            #     sID = sID + 1
            #     child = Member(sID, path = c1)
            #     child.checkFitness(self.terrain)
            #     if child.reach_goal == True:
            #             path = child.path
            #             return path
            #     new_child.append(child)
            #     population_count = population_count + 1
            #     # Tạo con 2
            #     c2 = p2[:keep_len]
            #     c2.extend(p1[keep_len:])
            #     sID = sID + 1
            #     child = Member(sID, path = c2)
            #     child.checkFitness(self.terrain)
            #     if child.reach_goal == True:
            #             path = child.path
            #             return path
            #     new_child.append(child)
            #     population_count = population_count + 1
            # population.extend(new_child)
            # ---------------------------------

            # Thực hiện mutation, tính lại fitness và OOB, check xem có đáp án
            # Tỉ lệ một cá thể bị đột biến là bằng nhau
            evo_number = int(len(population)*self.evo_rate)
            for i in range(evo_number):
                mem = choice(population)
                mem.evo()
                if mem.checkFitness(self.terrain) == False:
                    population.remove(mem)
                else:
                    # Check có đáp án
                    if mem.reach_goal == True:
                        path = mem.path
                        return path

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

