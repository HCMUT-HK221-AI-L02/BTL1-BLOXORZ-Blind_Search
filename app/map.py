class Map:
    def __init__(self):
        self.map = []
        self.height = 0
        self.width = 0
    
    def duplicate(self, map):
        self.map = map
        self.height = len(map)
        self.width = len(map[0])

    