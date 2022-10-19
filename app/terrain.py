# Import các file và thư viện liên quan
from app.block import Block
from app.position import Position
# Định nghĩa class Terrain
class Terrain:
    """
    ***Nội dung đọc file text:
    + "-" là ô cấm
    + "0" là ô cho phép vào
    + "S" là ô bắt đầu
    + "T" là ô đích đến

    ***Class Terrain có chức năng biểu diễn màn chơi, gồm có các dữ liệu sau:
    1) map là array 2 chiều, dùng để mô phỏng các ô đi được và ô đặc biệt
        + mốc tọa độ góc trái trên
        + số 0 là block không được vào
        + số 1 là block được vào
        + số ... là block có chức năng ...
    2) tọa độ ô bắt đầu
    3) tọa độ ô đích
    4) kích thước ngang (phương X) của bản đồ
    5) kích thước dọc (phương Y) của bản đồ
    """
    map = None
    start = None
    goal = None
    width = 0
    height = 0

    def __init__(self, level_file = "level/level01.txt"):
        self.translate_terrain(level_file)

    def translate_terrain(self, level_file):
        # Dịch file txt thành obj map
        file = open(level_file, 'r')
        self.map = []
        for x, line in enumerate(file):
            row = []
            for y, char in enumerate(line):
                if char == 'S':
                    self.start = Position(x, y)
                    row.append(1)
                elif char == 'T':
                    self.goal = Position(x, y)
                    row.append(1)
                elif char == '0':
                    row.append(1)
                elif char == '-':
                    row.append(0)
            self.map.append(row)
        file.close()

    def can_hold(self, b: Block) -> bool:
        # Kiểm tra obj block có nằm được trên map không
        can_hold = True
        return can_hold

    def neighbours(self, b: Block) -> list:
        # Liệt kê danh sách các vị trí block ở nước đi tiếp theo
        return []

    def done(self, b: Block) -> bool:
        # check xem bài toán đã hoàn thành
        return True