# Import các file và thư viện liên quan
from app.block import Block
from app.node import Node
from app.terrain import Terrain
from app.move import Move

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
        start_node = Node(terrain.map, start_block, move = None, parent = None)
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
                current = current_node
                while current is not None:
                    path.append(current.move)
                    current = current.parent
                return path[::-1]
            
            # Nếu không là kết quả thì tạo thêm node con
            children = self.get_children(current_node, terrain)
            for child in children:
                # Bỏ qua children này nếu đã nằm trong close list
                if child in close_list:
                    continue
                # Thêm node con vào trong open list (lưu ý thứ tự thêm)
                elif close_list[len(close_list) - 1].move == Move.Down and child.move == Move.Up:
                    continue
                elif close_list[len(close_list) - 1].move == Move.Up and child.move == Move.Down:
                    continue
                elif close_list[len(close_list) - 1].move == Move.Left and child.move == Move.Right:
                    continue
                elif close_list[len(close_list) - 1].move == Move.Right and child.move == Move.Left:
                    continue
                open_list.insert(0,child)

    def get_children(self, current_node: Node, terrain: Terrain):
        # Lấy ra danh sách node con
        children = []
        legal_neighbors = terrain.legal_neighbors(current_node.block)
        for (legal_neighbor, legal_move) in legal_neighbors:
            touchedMap = terrain.touch_special_cell(legal_neighbor, current_node.map)
            if touchedMap == current_node.map:
                child = Node(map=current_node.map, block=legal_neighbor, move=legal_move, parent=current_node)
            else:
                child = Node(map=touchedMap, block=legal_neighbor, move=legal_move, parent=current_node)
            children.append(child)
        return children
            
