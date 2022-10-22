from app.block import Block
from app.position import Position
from app.terrain import Terrain

class BridgeCell:
    """
    BridgeCell gồm 3 thuộc tính:
    + pos: thuộc tính dùng để lưu vị trí của bản thân ô BridgeCell
    + toggle: thuộc tính chỉ ra ô BridgeCell có toggle hay chỉ mở và chỉ đóng
    + bridge[]: list để chứa các ô trên map sẽ thay đổi khi block Bloxorz tác động vào ô BridgeCell
    """
    def __init__(self, bridObj):
        self.pos = Position(bridObj["pos"][0],bridObj["pos"][1])
        self.toggle = bridObj["toggle"]
        self.bridge = []
        for i in range(0, len(bridObj["bridge"])):
            self.bridge.append(Position(bridObj["bridge"][i][0],bridObj["bridge"][i][1]))

    def active(self, map):
        for b in range(0,len(self.bridge)):
            if self.toggle == "toggle":
                if map[self.bridge[b].y][self.bridge[b].x] == 1:
                    map[self.bridge[b].y][self.bridge[b].x] = 0
                else: map[self.bridge[b].y][self.bridge[b].x] = 1
            elif self.toggle == "open":
                if map[self.bridge[b].y][self.bridge[b].x] == 1:
                    map[self.bridge[b].y][self.bridge[b].x] = 0
            elif self.toggle == "close":
                if map[self.bridge[b].y][self.bridge[b].x] == 0:
                    map[self.bridge[b].y][self.bridge[b].x] = 1