# Import các file và thư viện liên quan
from app.block import Block
from app.node import Node
from app.terrain import Terrain

# Định nghĩa class DFS_Solver
class DFS_Solver:
    # Class này nhằm giải bài toán, sử dụng dữ liệu đầu vào là terrain được tạo ban đầu,
    # xuất kết quả là paths
    def __init__(self,):
        return

    def solve(self, terrain: Terrain):
        """
        Giải bài toán, gồm có các thành phần:
        + Open list là stack để chưa các node chuẩn bị xét
        + close list là danh sách các node đã xét
        """
        # Khởi tạo các biến
        open_list = []
        close_list = []
        start_pos = terrain.start
        start_block = Block(start_pos, start_pos)
        start_node = Node(start_block, move = None, parent = None)
        open_list.append(start_node)
        # Tạo vòng lặp giải
        while len(open_list) > 0:
            # Lấy node đứng đầu stack ra để tính
            # Lưu ý cách thêm node con vào open_list
            current_node = open_list[0]
            open_list.pop(0)
            close_list.append(current_node)

            # Kiểm tra node đang xét có là kết quả không
            if terrain.done(current_node.block):
                # Nếu là kết quả thì xuất đáp án
                path =[]
                return
            
            # Nếu không là kết quả thì tạo thêm node con
            children = self.get_children(current_node, terrain)
            for child in children:
                # Bỏ qua children này nếu đã nằm trong close list
                if child in close_list:
                    continue
                # Thêm node con vào trong open list (lưu ý thứ tự thêm)
                open_list.append(child)

    def get_children(self, current_node: Node, terrain: Terrain):
        # Lấy ra danh sách node con
        children = []
        return children
            
