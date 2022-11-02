"""
TODO:
- Thiếu update map sau khi đạp vào ô đặc biệt
- test_move chưa cập nhật trường hợp phím Space sẽ làm gì
"""

# Import các file và thư viện liên quan
from app.terrain import Terrain
from app.move import Move
from app.block import Block
from app.map import Map
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
        # Tạo block
        start_pos = terrain.start
        block = Block(start_pos, start_pos)
        map = terrain.map
        stop_idx = -1
        # Di chuyển block, nếu có thay đổi thì update map
        # Nếu bị rớt khỏi map phải dừng lại
        for step in self.path:
            stop_idx = stop_idx + 1
            if step is None:
                continue
            elif step == Move.Right: 
                b = block.right()
                if self.can_hold(b, map): 
                    block = b
                    continue
                else:
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Left:
                b = block.left()
                if self.can_hold(b, map): 
                    block = b
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Down:
                b = block.down()
                if self.can_hold(b, map): 
                    block = b
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            elif step == Move.Up:
                b = block.up()
                if self.can_hold(b, map): 
                    block = b
                    continue
                else: 
                    stop_idx = stop_idx - 1
                    break
            else: continue  
            # Nếu block bị rớt khỏi map thì dừng lại
            # Update map nếu có
        return (block, stop_idx)
    
    def checkFitness(self, terrain: Terrain):
        # Tạo block, chạy thử, đồng thời check reach_goal
        block = self.test_move(terrain)[0]
        # Check xem có out of bound không, nếu có thì thu hồi bước
        stop_idx = self.test_move(terrain)[1]
        if stop_idx != (len(self.path) - 1): self.path = self.path[:stop_idx]
        # Di chuyển xong, sau đó lấy tọa độ để tính fitness
        ave_px = (block.p1.x + block.p2.x)/2
        ave_py = (block.p1.y + block.p2.y)/2
        self.fitness = 1/((ave_px - terrain.goal.x)**2 + (ave_py - terrain.goal.y)**2 + 1)
        if self.fitness == 1:
            pause = 1
        # Check xem đã reach goal
        if block.is_standing() and block.p1.x == terrain.goal.x and block.p1.y == terrain.goal.y: 
            self.reach_goal = True
        

    def take_step(self,):
        # Đi thêm 1 bước random
        legal_step = []
        for step in Move:
            legal_step.append(step)
        next_step = choice(legal_step)
        new_path = self.path
        new_path.append(next_step)
        self.path = new_path

    def evo(self,):
        # Một cá thể bị đột biến sẽ chọn ngẫu nhiên một bước trong path để đổi ngẫu nhiên
        if len(self.path) == 0: return
        evo_idx = choice(range(len(self.path)))
        legal_step = []
        for step in Move:
            legal_step.append(step)
        legal_step.remove(self.path[evo_idx])
        self.path[evo_idx] = choice(legal_step)

    def can_hold(self, b: Block, map) -> bool:
        # Kiểm tra obj block có nằm được trên map không
        if b.p1.x >= (len(map[0])-1) or b.p1.y >= (len(map)-1): return False
        if b.p1.x < 0 or b.p1.y < 0: return False
        if b.p2.x >= (len(map[0])-1) or b.p2.y >= (len(map)-1): return False
        if b.p2.x < 0 or b.p2.y < 0: return False
        if map[b.p1.y][b.p1.x] == 0 or map[b.p2.y][b.p2.x] == 0: return False
        # Kiểm tra block có stand trên ô cam hay không
        if b.is_standing() and map[b.p1.y][b.p1.x] == 4: return False
        return True

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