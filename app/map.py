class Map:
    def __init__(self):
        self.map = []
        self.height = 0
        self.width = 0
 
    def duplicate(self, map):
        self.height = len(map)
        self.width = len(map[0])
        for x in range(0, self.height):
            row = []
            for y in range(0, self.width):
                row.append(map[x][y])
            self.map.append(row)