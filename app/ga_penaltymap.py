# Object dùng để phạt member khi member đi vào vùng không thuận lợi

# Thư viện cần thiết
from app.map import Map
from app.position import Position

# Định nghĩa class
class PenaltyMap:
    def __init__(self, map, penalty_rate):
        self.height = len(map)
        self.width = len(map[0])
        self.pMap = []
        for x in range(0, self.height):
            row = []
            for y in range(0, self.width):
                row.append(1)
            self.pMap.append(row)
        self.penalty_rate = penalty_rate

    def update(self, p: Position):
        self.pMap[p.y][p.x] = self.pMap[p.y][p.x]*self.penalty_rate

    def penvalue(self, p1: Position, p2: Position):
        max = self.pMap[p1.y][p1.x]
        if self.pMap[p2.y][p2.x] > max: max = self.pMap[p2.y][p2.x]
        return max
