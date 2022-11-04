# Import các file và thư viện liên quan
from app.block import Block
from app.position import Position
from app.bridgeCell import BridgeCell
from app.splitCell import SplitCell
from app.move import Move
from app.map import Map
import os
import json


# Định nghĩa class Terrain
class Terrain:
    """
    ***Nội dung đọc file text:
    + "-" là ô cấm
    + "0" là ô cho phép vào
    + "S" là ô bắt đầu
    + "T" là ô đích đến
    + "X" là ô Hard Bridge
    + "O" là ô Soft Bridge
    + "C" là ô Cam (Block cần nằm trên 2 ô cam liền kề)
    + "P" là ô Split Cell

    ***Class Terrain có chức năng biểu diễn màn chơi, gồm có các dữ liệu sau:
    1) map là array 2 chiều, dùng để mô phỏng các ô đi được và ô đặc biệt
        + mốc tọa độ góc trái trên
        + số 0 là block không được vào
        + số 1 là block được vào
        + số 2 là ô có chức năng Soft Bridge (O)
        + số 3 là ô có chức năng Hard Bridge (X)
        + số 4 là các ô màu cam
        + số 5 là ô có chức năng tách khối Bloxorz thành 2 
    2) tọa độ ô bắt đầu
    3) tọa độ ô đích
    4) kích thước ngang (phương X) của bản đồ
    5) kích thước dọc (phương Y) của bản đồ
    """
    map = None
    start = None
    goal = None
    soft_bridge_cell = []
    hard_bridge_cell = []
    split_cell = []
    width = 0
    height = 0

    def __init__(self, level_file = "level/level01.json"):
        self.translate_terrain(level_file)

    def translate_terrain(self, level_file):
        # Đọc các điểm đặc biệt trên map
        # level_json_file = level_file[0:-4] + ".json"
        if os.path.isfile(level_file):
            f = open(level_file, 'r')
            jsontext = json.loads(f.read())
            num_soft_bridge = len(jsontext["sb"])
            num_hard_bridge = len(jsontext["hb"])
            num_split_cell = len(jsontext["sc"])
            f.close()
        else:
            num_split_cell = 0
            num_soft_bridge = 0
            num_hard_bridge = 0

        for i in range(0,num_soft_bridge):
            self.soft_bridge_cell.append(BridgeCell(jsontext["sb"][i]))
        
        for i in range(0,num_hard_bridge):
            self.hard_bridge_cell.append(BridgeCell(jsontext["hb"][i]))

        for i in range(0, num_split_cell):
            self.split_cell.append(SplitCell(jsontext["sc"][i]))

        # Dịch file txt thành obj map
        newMap = self.translate_map(level_file)
        self.map = newMap.map
        self.height = newMap.height
        self.width = newMap.width

    def translate_map(self, level_file):
        file = open(level_file, 'r')
        jsonObj = json.loads(file.read())
        newMap = Map()
        for y in range(0,len(jsonObj["map"])):
            row = []
            newMap.height += 1
            w = 0
            for x in range(0,len(jsonObj["map"][y])):
                if jsonObj["map"][y][x] == 'S':
                    self.start = Position(x, y)
                    row.append(1)
                elif jsonObj["map"][y][x] == 'T':
                    self.goal = Position(x, y)
                    row.append(1)
                elif jsonObj["map"][y][x] == 'C':
                    row.append(4)
                elif jsonObj["map"][y][x] == 'X':
                    row.append(3)
                elif jsonObj["map"][y][x] == 'O':
                    row.append(2)
                elif jsonObj["map"][y][x] == 0:
                    row.append(1)
                elif jsonObj["map"][y][x] == '-':
                    row.append(0)
                elif jsonObj["map"][y][x] == 'P':
                    row.append(5)
                w += 1
            newMap.map.append(row)    
        newMap.width = w
        file.close()
        return newMap
            

    def can_hold(self, b: Block, m: Map) -> bool:
        # Kiểm tra obj block có nằm được trên map không
        can_hold = True
        # if b.p1.x >= self.width or b.p1.y >= self.height or b.p2.x >= self.width or b.p2.y >= self.height:
        if not(
            b.p1.x >= 0 and 
            b.p1.x < self.width and 
            b.p1.y >= 0 and 
            b.p1.y < self.height and 
            b.p2.x >= 0 and 
            b.p2.x < self.width and 
            b.p2.y >= 0 and 
            b.p2.y < self.height):
            can_hold = False
        else :
            if m[b.p1.y][b.p1.x] == 0 or m[b.p2.y][b.p2.x] == 0:
                can_hold = False
            elif b.is_standing() and self.map[b.p1.y][b.p1.x] == 4: # Kiểm tra block có stand trên ô cam hay không
                can_hold = False

        return can_hold

    def neighbours(self, b: Block) -> list:
        # Liệt kê danh sách các vị trí block ở nước đi tiếp theo
        if b.control == None:
            return [
                (b.right(), Move.Right),
                (b.up(), Move.Up),
                (b.down(), Move.Down),
                (b.left(), Move.Left)
            ]
        else:
            return [
                (b.right(), Move.Right),
                (b.up(), Move.Up),
                (b.down(), Move.Down),
                (b.left(), Move.Left),
                (b.switch(), Move.Space),
                (b.right(), Move.Right),
                (b.up(), Move.Up),
                (b.down(), Move.Down),
                (b.left(), Move.Left),
                (b.switch(), Move.Space)
            ]

    def legal_neighbors(self, b: Block, m: Map) -> list: 
        """
        Trả về danh sách các tuples(Block, Move) hợp lệ
        """
        return [(n, move) for (n, move) in self.neighbours(b) if self.can_hold(n,m)]

    def touch_special_cell(self, b: Block, map: Map):
        """
        Khi block Bloxorz chạm đến các vị trí đặc biệt như (Soft Bridge, Hard Bridge)
        """
        newMap = Map()
        newMap.duplicate(map)
        change = False
        # Check Block bloxorz standing or not
        if b.is_standing():
            for i in range(0,len(self.soft_bridge_cell)):
                if (b.p1.x == self.soft_bridge_cell[i].pos.x and b.p1.y == self.soft_bridge_cell[i].pos.y):
                    change = True
                    self.soft_bridge_cell[i].active(newMap)
            for j in range(0,len(self.hard_bridge_cell)):
                if (b.p1.x == self.hard_bridge_cell[j].pos.x and b.p1.y == self.hard_bridge_cell[j].pos.y):
                    self.hard_bridge_cell[j].active(newMap)
                    change = True
            for k in range(0,len(self.split_cell)):
                if (b.p1.x == self.split_cell[k].pos.x and b.p1.y == self.split_cell[k].pos.y):
                    return (map, b.split_block(self.split_cell[k].part1, self.split_cell[k].part2))
        else:
            for i in range(0,len(self.soft_bridge_cell)):
                if ((b.p1.x == self.soft_bridge_cell[i].pos.x and b.p1.y == self.soft_bridge_cell[i].pos.y) or 
                (b.p2.x == self.soft_bridge_cell[i].pos.x and b.p2.y == self.soft_bridge_cell[i].pos.y)):
                    change = True
                    self.soft_bridge_cell[i].active(newMap)
        if change: return (newMap.map, b)
        else: return (map,b)

    def done(self, b: Block) -> bool:
        # check xem bài toán đã hoàn thành
        return b.is_standing() and b.p1.x == self.goal.x and b.p1.y == self.goal.y