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
    block = member.block
    map = member.map
    stop_idx = 0
    # Di chuyển block, nếu có thay đổi thì update map
    member.toggle = member.toggle + 1     
    # Nếu block bị rớt khỏi map thì dừng lại
    # Update map nếu có    
    if member.path[len(member.path) - 1] == Move.Right: 
        b = block.right()
        if terrain.can_hold(b, map):
            (m, block) = terrain.touch_special_cell(b, map)                
            if block.control != None: block = block.join_block()
            if m != map or block.control != b.control: member.toggle = 0
            if len(member.path) > 1 and member.path[len(member.path) - 1 - 1] == Move.Left \
                 and member.toggle > 1:
                stop_idx = -1
        else:
            stop_idx = -1
    elif member.path[len(member.path) - 1] == Move.Left:
        b = block.left()
        if terrain.can_hold(b, map):
            (m, block) = terrain.touch_special_cell(b, map)                
            if block.control != None: block = block.join_block()
            if m != map or block.control != b.control: member.toggle = 0
            if len(member.path) > 1 and member.path[len(member.path) - 1 - 1] == Move.Right \
                 and member.toggle > 1:
                stop_idx = -1
        else: 
            stop_idx = -1
    elif member.path[len(member.path) - 1] == Move.Down:
        b = block.down()
        if terrain.can_hold(b, map):
            (m, block) = terrain.touch_special_cell(b, map)
            if block.control != None: block = block.join_block()
            if m != map or block.control != b.control: member.toggle = 0
            if len(member.path) > 1 and member.path[len(member.path) - 1 - 1] == Move.Up \
                 and member.toggle > 1:
                stop_idx = -1
        else: 
            stop_idx = -1
    elif member.path[len(member.path) - 1] == Move.Up:
        b = block.up()
        if terrain.can_hold(b, map):
            (m, block) = terrain.touch_special_cell(b, map)
            if block.control != None: block = block.join_block()
            if m != map or block.control != b.control: member.toggle = 0
            if len(member.path) > 1 and member.path[len(member.path) - 1 - 1] == Move.Down \
                 and member.toggle > 1:
                stop_idx = -1
        else: 
            stop_idx = -1
    elif member.path[len(member.path) - 1] == Move.Space:
        if block.control != None: 
            block = block.switch()
            m = map
            member.toggle = 0
            if member.path[len(member.path) - 1 - 1] == Move.Space:
                stop_idx = -1
        else:
            stop_idx = -1
    if stop_idx == 0:
        member.map = m 
        member.block = block
    return stop_idx

def checkFitness(member: Member, terrain: Terrain, env: PenaltyMap) -> bool: 
    # False là member sẽ bị kill
    # Tạo block, chạy thử, đồng thời check reach_goal
    stop_idx = test_move(member, terrain)
    # Check xem có out of bound không, nếu có đi trả tín hiệu kill block
    if stop_idx == -1: return False
    # Di chuyển xong, sau đó lấy tọa độ để tính fitness
    ave_px = (member.block.p1.x + member.block.p2.x)/2
    ave_py = (member.block.p1.y + member.block.p2.y)/2
    dStart = (ave_px - terrain.start.x)**2 + (ave_py - terrain.start.y)**2
    dStart = dStart**(0.5) + 1
    dGoal = (ave_px - terrain.goal.x)**2 + (ave_py - terrain.goal.y)**2
    dGoal = dGoal**(0.5) + 1
    remain = env.penvalue(member.block.p1, member.block.p2)
    member.fitness = remain*dStart/dGoal     
    # Kiểm tra về đích và kết thúc
    if terrain.done(member.block): member.reach_goal = True
    return True