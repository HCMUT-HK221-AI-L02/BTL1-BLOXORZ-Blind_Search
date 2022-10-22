# Import các file và thư viện liên quan
import enum

# Định nghĩa class Move
class Move(enum.Enum):
    # Dịch các thao tác trái phải lên xuống thành dạng số
    Left = 1
    Right = 2
    Up = 3
    Down = 4
    Space = 5