# Import các file và thư viện liên quan
from app.terrain import Terrain
from app.move import Move
from app.block import Block
from random import choice

# Định nghĩa class Member là một cá thể trong quần thể
class Member:
    # Mỗi obj trong class này đại diện cho một đáp án, là chuỗi bước di chuyển block
    def __init__(self, id, *, path = []):
        self.id = id
        # Nếu nhập vào một list rỗng thì tạo một obj list rỗng mới
        self.path = path[:len(path)]
        self.fitness = 0
        self.reach_goal = False

    def test_move(self, terrain: Terrain):
        # Đi thử path đang lưu, kết quả trả ra là block đã đi và idx trong path khi bị dừng
        start_pos = terrain.start
        block = Block(start_pos, start_pos)
        map = terrain.map
        stop_idx = -1
        remain_rate = 0.7
        remain_distance_trigger = 3
        num_step_back = 5
        ave_pos = []
        # Di chuyển block, nếu có thay đổi thì update map
        # Nếu bị rớt khỏi map phải dừng lại
        for step in self.path:
            stop_idx = stop_idx + 1
            # Nếu block bị rớt khỏi map thì dừng lại
            # Update map nếu có
            if step is None:
                continue
            elif step == Move.Right: 
                b = block.right()
                if terrain.can_hold(b, map):
                    (map, block) = terrain.touch_special_cell(b, map)
                    if block.control != None: block = block.join_block()
                    ave_pos.append(block.ave_pos_cal())
                    continue
                else:
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Left:
                b = block.left()
                if terrain.can_hold(b, map):
                    (map, block) = terrain.touch_special_cell(b, map)
                    if block.control != None: block = block.join_block()
                    ave_pos.append(block.ave_pos_cal())
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Down:
                b = block.down()
                if terrain.can_hold(b, map):
                    (map, block) = terrain.touch_special_cell(b, map)
                    if block.control != None: block = block.join_block()
                    ave_pos.append(block.ave_pos_cal())
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Up:
                b = block.up()
                if terrain.can_hold(b, map):
                    (map, block) = terrain.touch_special_cell(b, map)
                    if block.control != None: block = block.join_block()
                    ave_pos.append(block.ave_pos_cal())
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Space:
                if block.control != None: 
                    block = block.switch()
                    continue
                else:
                    stop_idx = stop_idx - 1
                    break
            else: continue  
        # Tính penalty rồi trả kết quả
        remain = 1
        if len(ave_pos) >= num_step_back + 1:
            for i in range(num_step_back, len(ave_pos)):
                dis = (ave_pos[i].x - ave_pos[i-num_step_back].x)**2
                dis = dis + (ave_pos[i].y - ave_pos[i-num_step_back].y)**2
                dis = dis**(1/2)
                if dis <= remain_distance_trigger: remain = remain*remain_rate
        return (block, stop_idx, remain)
    
    def checkFitness(self, terrain: Terrain) -> bool: # False là member sẽ bị kill
        # Tạo block, chạy thử, đồng thời check reach_goal
        (block, stop_idx, remain) = self.test_move(terrain)
        # Check xem có out of bound không, nếu có thì thu hồi bước
        if stop_idx == -1: return False
        elif stop_idx != (len(self.path) - 1): return False
        # Di chuyển xong, sau đó lấy tọa độ để tính fitness
        ave_px = (block.p1.x + block.p2.x)/2
        ave_py = (block.p1.y + block.p2.y)/2
        dStart = (ave_px - terrain.start.x)**2 + (ave_py - terrain.start.y)**2
        dStart = dStart**(0.5) + 1
        dGoal = (ave_px - terrain.goal.x)**2 + (ave_py - terrain.goal.y)**2
        dGoal = dGoal**(0.5) + 1
        self.fitness = remain*len(self.path)*dStart/dGoal        
        if terrain.done(block): self.reach_goal = True
        return True
        

    def take_step(self,):
        # Đi thêm 1 bước random
        legal_step = []
        for step in Move:
            legal_step.append(step)
        next_step = choice(legal_step)
        self.path.append(next_step)

    def evo(self,):
        # Một cá thể bị đột biến sẽ quay lại 1/3 quảng đường để đi ngẫu nhiên
        if len(self.path) == 0: return
        self.path = self.path[:int(len(self.path)*2/3)]

    def print_path(self):
        # Chuyển list gồm các obj moves thành string kết quả
        path_str = ""
        for i, path in enumerate(self.path):
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
            if i < len(self.path) - 1:
                path_str = path_str + "->"
        return path_str