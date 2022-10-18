# Import các file và thư viện liên quan
from app.position import Position
# Định nghĩa class Block
class Block:
    # Class Block định nghĩa obj có 2 khối có tọa độ
    def __init__(self, p1: Position, p2: Position):
        self.p1 = p1
        self.p2 = p2

    def is_standing(self) -> bool:
        # Check xem block có đang đứng
        return True

    def right(self):
        # Di chuyển block qua phải
        return self

    def down(self):
        # Di chuyển block xuống dưới
        return self

    def left(self):
        # Di chuyển block qua trái
        return self

    def up(self):
        # Di chuyển block lên trên
        return self

    def dx(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương x
        return Block(self.p1.dx(d1), self.p2.dx(d2))

    def dy(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương y
        return Block(self.p1.dy(d1), self.p2.dy(d2))