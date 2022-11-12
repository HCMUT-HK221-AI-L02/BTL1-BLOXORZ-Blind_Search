# Import các file và thư viện liên quan
from app.position import Position
import json

# Định nghĩa class Block
class Block:
    # Class Block định nghĩa obj có 2 khối có tọa độ, với gốc tọa độ là bottom - left
    def __init__(self, p1: Position, p2: Position, control = None):
        """
        Điều kiện: p1.x <= p2.x and p1.y <= p2.y
        Thuộc tính control có các giá trị:
            + None: Block Bloxorz đang là 1 khối
            + "p1": đang ở trạng thái điều khiển khối p1
            + "p2": đang ở trạng thái điều khiển khối p2
        """
        self.p1 = p1
        self.p2 = p2
        self.control = control

    def is_standing(self) -> bool:
        # Check xem block có đang đứng
        return self.p1.x == self.p2.x and self.p1.y == self.p2.y

    def right(self):
        # Bloxorz là 1 khối
        if self.control == None:
            # Di chuyển block qua phải
            if self.is_standing():
                return self.dx(1,2)
            elif self.p1.y == self.p2.y:
                return self.dx(2,1)
            else: return self.dx(1,1)
        elif self.control == "p1":
            return self.dx(1,0)
        elif self.control == "p2":
            return self.dx(0,1)

    def left(self):
        # Bloxorz là 1 khối
        if self.control == None:
            # Di chuyển block qua trái
            if self.is_standing():
                return self.dx(-2,-1)
            elif self.p1.y == self.p2.y:
                return self.dx(-1,-2)
            else: return self.dx(-1,-1)
        elif self.control == "p1":
            return self.dx(-1,0)
        elif self.control == "p2":
            return self.dx(0,-1)

    def down(self):
        # Bloxorz là 1 khối
        if self.control == None:
            # Di chuyển block xuống dưới
            if self.is_standing():
                return self.dy(1,2)
            elif self.p1.x == self.p2.x:
                return self.dy(2,1)
            else: return self.dy(1,1)
        elif self.control == "p1":
            return self.dy(1,0)
        elif self.control == "p2":
            return self.dy(0,1)

    def up(self):
        # Bloxorz là 1 khối
        if self.control == None:
            # Di chuyển block lên trên
            if self.is_standing():
                return self.dy(-2,-1)
            elif self.p1.x == self.p2.x:
                return self.dy(-1,-2)
            else: return self.dy(-1,-1)
        elif self.control == "p1":
            return self.dy(-1,0)
        elif self.control == "p2":
            return self.dy(0,-1)

    def dx(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương x
        return Block(self.p1.dx(d1), self.p2.dx(d2), self.control)

    def dy(self, d1, d2):
        # Dịch chuyển vị trí của khối đơn vị theo phương y
        return Block(self.p1.dy(d1), self.p2.dy(d2), self.control)

    def split_block(self, pos1: Position, pos2: Position):
        """
        Split khối Bloxorz thành 2 khối riêng biệt tại 2 vị
        trí pos1, pos2. Mặc định quyền điều khiển sẽ ở khối p1
        """
        return Block(pos1,pos2,"p1")

    def join_block(self):
        if self.can_join():
            if self.p1.x > self.p2.x:
                return Block(self.p2, self.p1)
            elif self.p1.y > self.p2.y:
                return Block(self.p2, self.p1)
            else:
                return Block(self.p1, self.p2)
        else: return self

    def can_join(self):
        x_diff = abs(self.p1.x - self.p2.x)
        y_diff = abs(self.p1.y - self.p2.y)
        if x_diff + y_diff == 1:
            return True
        else: return False

    def switch(self):
        if self.control == "p1":
            self.control = "p2"
            return Block(self.p1, self.p2, self.control)
        elif self.control == "p2":
            self.control = "p1"
            return Block(self.p1, self.p2, self.control)

    def ave_pos_cal(self):
            posx = (self.p1.x + self.p2.x)/2
            posy = (self.p1.y + self.p2.y)/2
            return Position(posx, posy)

    def __str__(self):
        return json.dumps([str(self.p1), str(self.p2)])