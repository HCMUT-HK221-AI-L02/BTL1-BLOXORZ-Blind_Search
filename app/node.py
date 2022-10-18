# Import các file và thư viện liên quan
from app.block import Block
from app.move import Move

# Định nghĩa class Node
class Node:
    def __init__(self, block: Block, move: Move, parent):
        self.block = block
        self.move = move
        self.parent = parent