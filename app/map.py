from app.position import Position
from app.terrain import Terrain


class Map:
    def __init__(self):
        self.map = []
        self.height = 0
        self.width = 0
    
    def duplicate(self, map):
        self.map = map
        self.height = len(map)
        self.width = len(map[0])
        
    def translate_map(self, level_file, terrain: Terrain):
        file = open(level_file, 'r')
        for x, line in enumerate(file):
            row = []
            self.height += 1
            for y, char in enumerate(line):
                if char == 'S':
                    terrain.start = Position(x, y)
                    row.append(1)
                elif char == 'T':
                    terrain.goal = Position(x, y)
                    row.append(1)
                elif char == 'C':
                    row.append(4)
                elif char == 'X':
                    row.append(3)
                elif char == 'O':
                    row.append(2)
                elif char == '0':
                    row.append(1)
                elif char == '-':
                    row.append(0)
                self.width += 1
            self.map.append(row)
        file.close()
    