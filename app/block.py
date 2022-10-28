# Import các file và thư viện liên quan
from app.position import Position
import json
# Định nghĩa class Block
class Block:
    # Class Block định nghĩa obj có 2 khối có tọa độ, với gốc tọa độ là bottom - left
    def __init__(self, p1: Position, p2: Position):
        """p1.x <= p2.x and p1.y <= p2.y"""
        self.p1 = p1
        self.p2 = p2
        self.control = None

    def is_standing(self) -> bool:
        # Check xem block có đang đứng
        return self.p1.x == self.p2.x and self.p1.y == self.p2.y

    def right(self):
        # Di chuyển block qua phải
        if self.is_standing():
            return self.dx(1,2)
        elif self.p1.y == self.p2.y:
            return self.dx(2,1)
        else: return self.dx(1,1)

    def left(self):
        # Di chuyển block qua trái
        if self.is_standing():
            return self.dx(-2,-1)
        elif self.p1.y == self.p2.y:
            return self.dx(-1,-2)
        else: return self.dx(-1,-1)

    def down(self):
        # Di chuyển block xuống dưới
        if self.is_standing():
            return self.dy(1,2)
        elif self.p1.x == self.p2.x:
            return self.dy(2,1)
        else: return self.dy(1,1)

    def up(self):
        # Di chuyển block lên trên
        if self.is_standing():
            return self.dy(-2,-1)
        elif self.p1.x == self.p2.x:
            return self.dy(-1,-2)
        else: return self.dy(-1,-1)

    def dx(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương x
        return Block(self.p1.dx(d1), self.p2.dx(d2))

    def dy(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương y
        return Block(self.p1.dy(d1), self.p2.dy(d2))

    def switch(self):
        pass

    def join_blocK(self):
        pass

    def __str__(self):
        return json.dumps([str(self.p1), str(self.p2)])