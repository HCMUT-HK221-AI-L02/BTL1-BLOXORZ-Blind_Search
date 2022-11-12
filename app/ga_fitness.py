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
    toggle = 1
    for i in range(0,len(member.path)):
        stop_idx = stop_idx + 1   
        toggle = toggle + 1     
        # Nếu block bị rớt khỏi map thì dừng lại
        # Update map nếu có
        if member.path[i] is None:
            continue
        elif member.path[i] == Move.Right: 
            b = block.right()
            if terrain.can_hold(b, map):
                (m, block) = terrain.touch_special_cell(b, map)                
                if block.control != None: block = block.join_block()
                if m != map or block.control != b.control: toggle = 0
                if i > 0 and member.path[i - 1] == Move.Left and toggle > 1:
                    stop_idx = stop_idx - 1
                    break
                map = m
                continue
            else:
                stop_idx = stop_idx - 1
                break
        elif member.path[i] == Move.Left:
            b = block.left()
            if terrain.can_hold(b, map):
                (m, block) = terrain.touch_special_cell(b, map)                
                if block.control != None: block = block.join_block()
                if m != map or block.control != b.control: toggle = 0
                if i > 0 and member.path[i - 1] == Move.Right and toggle > 1:
                    stop_idx = stop_idx - 1
                    break
                map = m
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif member.path[i] == Move.Down:
            b = block.down()
            if terrain.can_hold(b, map):
                (m, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                if m != map or block.control != b.control: toggle = 0
                if i > 0 and member.path[i - 1] == Move.Up and toggle > 1:
                    stop_idx = stop_idx - 1
                    break
                map = m
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif member.path[i] == Move.Up:
            b = block.up()
            if terrain.can_hold(b, map):
                (m, block) = terrain.touch_special_cell(b, map)
                if block.control != None: block = block.join_block()
                if m != map or block.control != b.control: toggle = 0
                if i > 0 and member.path[i - 1] == Move.Down and toggle > 1:
                    stop_idx = stop_idx - 1
                    break
                map = m
                continue
            else: 
                stop_idx = stop_idx - 1
                break
        elif member.path[i] == Move.Space:
            if block.control != None: 
                block = block.switch()
                toggle = 0
                if member.path[i - 1] == Move.Space:
                    stop_idx = stop_idx - 1
                    break
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