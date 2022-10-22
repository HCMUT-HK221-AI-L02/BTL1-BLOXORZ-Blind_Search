# Import các file và thư viện liên quan
from app.block import Block
from app.map import Map
from app.move import Move
from app.terrain import Terrain

# Định nghĩa class Node
class Node:
    def __init__(self, map: Map, block: Block, move: Move, parent):
        self.block = block
        self.move = move
        self.parent = parent
        self.map = map

