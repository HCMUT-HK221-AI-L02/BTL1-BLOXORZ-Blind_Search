# Import các file và thư viện liên quan
from app.block import Block
from app.node import Node
from app.terrain import Terrain
from app.move import Move
from app.position import Position

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
                list = []
                current = current_node
                while current is not None:
                    path.append(current.move)
                    list.insert(0,(current.move, current.block, current.map))
                    temp = current
                    current = current.parent
                    if current != None:
                        if temp.block.control != None and current.block.control != None:
                            if temp.block.control != current.block.control and temp.move != Move.Space and current.move != Move.Space:
                                path.append(Move.Space)
                                list.insert(0, (Move.Space, temp.block, temp.map))

                return path[::-1]
            
            # Nếu không là kết quả thì tạo thêm node con (lưu ý thứ tự thêm)
            children = self.get_children(current_node, terrain)
            to_insert = []
            for child in children:
                # Bỏ qua children này nếu đã nằm trong close list
                skip_child = False
                for closed_child in close_list:
                    if self.is_same_node(child, closed_child): 
                        skip_child = True
                        break
                if skip_child:
                    continue
                # Thêm node con vào trong list tạm
                to_insert.append(child)
            # Cập nhật open_list
            to_insert.extend(open_list)
            open_list = to_insert

    def get_children(self, current_node: Node, terrain: Terrain):
        # Lấy ra danh sách node con
        children = []
        legal_neighbors = terrain.legal_neighbors(current_node.block, current_node.map)

        for (legal_neighbor, legal_move) in legal_neighbors:
            (touchedMap, touchSplitCell) = terrain.touch_special_cell(legal_neighbor, current_node.map)
            if touchSplitCell.control != None:
                if touchSplitCell.can_join():
                    touchSplitCell = touchSplitCell.join_block()

            if touchedMap == current_node.map and touchSplitCell == legal_neighbor:
                child = Node(map=current_node.map, block=legal_neighbor, \
                    move=legal_move, parent=current_node)
            elif touchedMap != current_node.map:
                child = Node(map=touchedMap, block=legal_neighbor, \
                    move=legal_move, parent=current_node)
            elif touchSplitCell != legal_neighbor:
                child = Node(map=current_node.map, block=touchSplitCell,\
                    move=legal_move, parent=current_node)

            children.append(child)
        return children

    def is_same_node(self, node1: Node, node2: Node):
        is_same_node = False
        if node1.map == node2.map and self.is_same_position(node1.block.p1, node2.block.p1) and \
            self.is_same_control(node1.block, node2.block) and \
            self.is_same_position(node1.block.p2, node2.block.p2): 
                is_same_node = True
        return is_same_node

    def is_same_position(self, p1: Position, p2: Position):
        if p1.x == p2.x and p1.y == p2.y: return True
        else: return False

    def is_same_control(self, b1: Block, b2: Block):
        if b1.control == b2.control: return True
        else: return False
            
