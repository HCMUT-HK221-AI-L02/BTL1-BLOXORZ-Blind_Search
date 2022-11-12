# Import các file và thư viện liên quan
from app.move import Move
from app.position import Position
from app.block import Block
from app.terrain import Terrain


# Định nghĩa class Member là một cá thể trong quần thể
class Member:
    # Mỗi obj trong class này đại diện cho một đáp án, là chuỗi bước di chuyển block
    def __init__(self, id, path, block: Block, map, toggle):
        self.id = id
        # Nếu nhập vào một list rỗng thì tạo một obj list rỗng mới
        self.path = path[:len(path)]
        self.fitness = 0
        self.reach_goal = False
        # Đọc vào block, map và toggle
        self.block = Block(block.p1, block.p2, block.control)
        self.map = map
        self.toggle = toggle


    def take_step(self, step):
        # Đi thêm 1 bước
        if step == 'Space': self.path.append(Move.Space)
        elif step == 'Left': self.path.append(Move.Left)
        elif step == 'Right': self.path.append(Move.Right)
        elif step == 'Up': self.path.append(Move.Up)
        elif step == 'Down': self.path.append(Move.Down)


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