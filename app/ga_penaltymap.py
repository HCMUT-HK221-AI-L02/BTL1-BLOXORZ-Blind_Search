# Object dùng để phạt member khi member đi vào vùng không thuận lợi

# Thư viện cần thiết
from app.position import Position
from app.ga_config2 import *

# Định nghĩa class
class PenaltyMap:
    def __init__(self, map):
        self.height = len(map)
        self.width = len(map[0])
        self.pMap = []
        for x in range(0, self.height):
            row = []
            for y in range(0, self.width):
                row.append(1)
            self.pMap.append(row)
        self.penalty_rate = PENALTY_RATE

    def update(self, p: Position):
        self.pMap[p.y][p.x] = self.pMap[p.y][p.x]*self.penalty_rate

    def penvalue(self, p1: Position, p2: Position):
        max = self.pMap[p1.y][p1.x]
        if self.pMap[p2.y][p2.x] > max: max = self.pMap[p2.y][p2.x]
        return max

    def refill(self):
        for y in range(self.height):
            for x in range(self.width):
                self.pMap[y][x] = self.pMap[y][x]*REFILL_RATE
