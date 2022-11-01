from app.position import Position

class SplitCell:
    """
    SplitCell gồm 3 thuộc tính:
        + pos: là thuộc tính chứa vị trí ô Split Cell
        + part1: là thuộc tính chứa vị trí mà p1 của khối Bloxorz sẽ dịch chuyển tới
        + part2: là thuộc tính chứa vị trí mà p2 của khối Bloxorz sẽ dịch chuyển tới
    """
    def __init__(self, splitCellObj):
        self.pos = Position(splitCellObj["pos"][0], splitCellObj["pos"][1])
        self.part1 = Position(splitCellObj["p1"][0], splitCellObj["p1"][1])
        self.part2 = Position(splitCellObj["p2"][0], splitCellObj["p2"][1])
        