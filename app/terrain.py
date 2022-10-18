# Import các file và thư viện liên quan
from app.block import Block
# Định nghĩa class Terrain
class Terrain:
    """
    Class Terrain có chức năng biểu diễn màn chơi, gồm có các dữ liệu sau:
    1) map là array 2 chiều, dùng để mô phỏng các ô đi được và ô đặc biệt
        mốc tọa độ góc trái trên
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
        # Xử lý file

        # Kết thúc
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