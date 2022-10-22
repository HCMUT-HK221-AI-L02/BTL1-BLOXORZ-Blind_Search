# Định nghĩa class Position
class Position:
    # Class được dùng để xác định vị trí của phần tử khối
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dx(self, d):
        # Hàm thay đổi giá trị x
        return Position(self.x + d, self.y)

    def dy(self, d):
        # Hàm thay đổi giá trị y
        return Position(self.x, self.y + d)