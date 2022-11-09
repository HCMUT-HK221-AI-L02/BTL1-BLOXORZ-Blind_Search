# Thư viện các hàm tính fitness

# Các thư viện liên quan
from app.terrain import Terrain
from app.block import Block
from app.move import Move
from app.member import Member
from app.ga_penaltymap import PenaltyMap

# Nội dung các hàm tính
def test_move(member: Member, terrain: Terrain):
    # Đi thử path đang lưu, kết quả trả ra là block đã đi và idx trong path khi bị dừng
    start_pos = terrain.start
    block = Block(start_pos, start_pos)
    map = terrain.map
    stop_idx = -1
    # Di chuyển block, nếu có thay đổi thì update map
    # Nếu bị rớt khỏi map phải dừng lại
    for step in member.path:
        stop_idx = stop_idx + 1
        # Nếu block bị rớt khỏi map thì dừng lại
        # Update map nếu có
        if step is None:
            continue
        elif step == Move.Right: 
            b = block.right()
            if terrain.can_hold(b, map):
                (map, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                continue
            else:
                stop_idx = stop_idx - 1
                break
        elif step == Move.Left:
            b = block.left()
            if terrain.can_hold(b, map):
                (map, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif step == Move.Down:
            b = block.down()
            if terrain.can_hold(b, map):
                (map, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif step == Move.Up:
            b = block.up()
            if terrain.can_hold(b, map):
                (map, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif step == Move.Space:
            if block.control != None: 
                block = block.switch()
                continue
            else:
                stop_idx = stop_idx - 1
                break
        else: continue      
    return (block, stop_idx)

def checkFitness(member: Member, terrain: Terrain, env: PenaltyMap) -> bool: 
    # False là member sẽ bị kill
    # Tạo block, chạy thử, đồng thời check reach_goal
    (block, stop_idx) = test_move(member, terrain)
    # Check xem có out of bound không, nếu có đi trả tín hiệu kill block
    if stop_idx == -1: return False
    elif stop_idx != (len(member.path) - 1): return False
    # Di chuyển xong, sau đó lấy tọa độ để tính fitness
    ave_px = (block.p1.x + block.p2.x)/2
    ave_py = (block.p1.y + block.p2.y)/2
    dStart = (ave_px - terrain.start.x)**2 + (ave_py - terrain.start.y)**2
    dStart = dStart**(0.5) + 1
    dGoal = (ave_px - terrain.goal.x)**2 + (ave_py - terrain.goal.y)**2
    dGoal = dGoal**(0.5) + 1
    remain = env.penvalue(block.p1, block.p2)
    member.fitness = remain*dStart/dGoal     
    # Lưu lại position
    member.p1.x = block.p1.x
    member.p1.y = block.p1.y
    member.p2.x = block.p2.x
    member.p2.y = block.p2.y
    # Kiểm tra về đích và kết thúc
    if terrain.done(block): member.reach_goal = True
    return True