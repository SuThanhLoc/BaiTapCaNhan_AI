import math # Needed for Simulated Annealing
import random
import time # Có thể dùng để đo thời gian nếu cần
from collections import deque
import heapq # heapq có thể dùng thay PriorityQueue nếu muốn (ít khác biệt hiệu năng)
from queue import PriorityQueue # Đang dùng cái này
import copy # copy.deepcopy needed for GA and potentially others

# --- Trạng thái Bắt đầu và Đích ---
# Sử dụng trạng thái bắt đầu đã thống nhất từ yêu cầu trước
Start = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
Goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

Moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lên, Xuống, Trái, Phải
Moves_Dir_Name = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)} # Dùng cho Conformant BFS

# --- Các hàm tiện ích ---
# (Giữ nguyên các hàm tiện ích đã có)
def tim_X(x):
    """Tìm tọa độ (hàng, cột) của giá trị x trong ma trận Đích (Goal)."""
    if not hasattr(tim_X, "goal_pos_cache"):
        tim_X.goal_pos_cache = {Goal[i][j]: (i, j) for i in range(3) for j in range(3)}
    return tim_X.goal_pos_cache.get(x, (-1,-1))

def khoang_cach_mahathan(Matran_HienTai, goal_state=Goal):
    """Tính tổng khoảng cách Manhattan từ vị trí hiện tại của các ô số đến vị trí đích."""
    sum_val = 0
    if Matran_HienTai is None: return float('inf')
    # Tạo cache dựa trên goal_state để linh hoạt nếu goal thay đổi
    goal_str = change_matran_string(goal_state)
    cache_attr_name = f"goal_pos_cache_{goal_str}"
    if not hasattr(khoang_cach_mahathan, cache_attr_name):
        # print(f"Creating Manhattan cache for goal: {goal_str}") # Debug cache creation
        cache = {goal_state[i][j]: (i, j) for i in range(3) for j in range(3) if goal_state[i][j] != 0}
        setattr(khoang_cach_mahathan, cache_attr_name, cache)

    goal_pos_cache = getattr(khoang_cach_mahathan, cache_attr_name)

    for i in range(3):
        for j in range(3):
            tile = Matran_HienTai[i][j]
            if tile != 0:
                pos_x, pos_y = goal_pos_cache.get(tile, (-1, -1))
                if pos_x != -1:
                    sum_val += abs(i - pos_x) + abs(j - pos_y)
                else:
                    # print(f"Warning: Tile {tile} not found in goal cache for goal {goal_str}")
                    return float('inf') # Trạng thái không hợp lệ so với đích
    return sum_val


def Tim_0(Matran_hientai):
    """Tìm tọa độ ô trống (số 0)."""
    if Matran_hientai is None: return -1, -1
    for i in range(3):
        # Check if row is valid before accessing
        if not isinstance(Matran_hientai[i], (list, tuple)) or len(Matran_hientai[i]) != 3:
             # print(f"Warning: Invalid row format in Tim_0 at index {i}")
             return -1, -1
        for j in range(3):
            try:
                 if Matran_hientai[i][j] == 0: return i, j
            except IndexError:
                 # print(f"Warning: IndexError accessing [{i}][{j}] in Tim_0")
                 return -1,-1
    return -1, -1 # Không tìm thấy số 0

def Check(x, y):
    """Kiểm tra tọa độ có hợp lệ trong bảng 3x3 không."""
    return 0 <= x < 3 and 0 <= y < 3

def Chiphi(matran_HienTai):
    """Tính số ô sai vị trí (không kể ô trống)."""
    dem = 0
    if matran_HienTai is None: return float('inf')
    for i in range(3):
        for j in range(3):
            if matran_HienTai[i][j] != 0 and matran_HienTai[i][j] != Goal[i][j]: dem+=1
    return dem

def DiChuyen(Matran_HienTai, x, y, new_x, new_y):
    """Tạo bản sao và thực hiện di chuyển ô trống."""
    # Input là tọa độ CŨ (x,y) và MỚI (new_x, new_y) của ô trống
    if not isinstance(Matran_HienTai, list) or not Matran_HienTai: return None
    # Deep copy để đảm bảo không ảnh hưởng bản gốc
    new_state = [row[:] for row in Matran_HienTai]
    # Swap giá trị tại vị trí cũ của ô trống và vị trí mới của ô trống
    try:
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    except IndexError:
        # print(f"Warning: IndexError during swap in DiChuyen ({x},{y}) <-> ({new_x},{new_y})")
        return None # Trả về None nếu có lỗi
    return new_state

def print_matrix(matran):
    """In ma trận ra màn hình cho dễ nhìn."""
    if matran and isinstance(matran, list) and all(isinstance(row, list) for row in matran):
        print("-" * 5);
        for row in matran: print(" ".join(map(str, row)))
        print("-" * 5)
    else: print("Invalid matrix format")

def change_matran_string(matran):
    """Chuyển ma trận thành chuỗi để dùng làm key trong set/dict (visited)."""
    if matran is None: return ""
    # Đảm bảo là ma trận hợp lệ trước khi chuyển đổi
    if not isinstance(matran, (list, tuple)) or len(matran) != 3: return ""
    if not all(isinstance(row, (list, tuple)) and len(row) == 3 for row in matran): return ""
    try:
        return ''.join(str(num) for row in matran for num in row)
    except TypeError:
        return "" # Trả về chuỗi rỗng nếu có lỗi type

# --- Các thuật toán tìm kiếm thông tin ---
# (Giữ nguyên BFS, UCS, DFS, IDDFS, Greedy, A*, IDA*)
def BFS(start_node):
    queue = deque([(start_node,[])])
    visited = set()
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("BFS Error: Invalid start node."); return [] # Check valid start
    visited.add(start_node_str)
    nodes_expanded = 0
    goal_str = change_matran_string(Goal) # So sánh chuỗi cho nhanh

    while queue:
        matran_hientai, path = queue.popleft(); nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai) # Lấy chuỗi của trạng thái hiện tại
        if matran_hientai_str == goal_str: print(f"BFS: Expanded {nodes_expanded} nodes."); return path + [matran_hientai]

        x,y = Tim_0(matran_hientai);
        if x == -1: continue # Trạng thái không hợp lệ

        for dx,dy in Moves:
            new_X, new_Y = x + dx, y + dy # Tọa độ MỚI của ô trống
            if(Check(new_X,new_Y)):
                new_matran = DiChuyen(matran_hientai,x,y,new_X,new_Y) # Truyền tọa độ cũ và mới của ô trống
                if new_matran: # Check if DiChuyen succeeded
                    new_matran_str = change_matran_string(new_matran)
                    if(new_matran_str and new_matran_str not in visited):
                        visited.add(new_matran_str); queue.append((new_matran,path+[matran_hientai]))

    print(f"BFS: Expanded {nodes_expanded} nodes. Goal not found."); return []

def UCS(start_node):
    qp = PriorityQueue()
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("UCS Error: Invalid start node."); return []
    qp.put( (0, start_node, []) ) # (cost, state, path)
    visited = {start_node_str: 0}; nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while not qp.empty():
        cost, matran_hientai, path = qp.get(); nodes_expanded += 1
        matran_str = change_matran_string(matran_hientai)
        if not matran_str: continue # Bỏ qua nếu trạng thái không hợp lệ

        if matran_str == goal_str: print(f"UCS: Expanded {nodes_expanded} nodes."); return path + [matran_hientai]

        # Optimization: Nếu chi phí hiện tại để đến trạng thái này lớn hơn chi phí đã biết, bỏ qua
        if cost > visited.get(matran_str, float('inf')): continue

        x,y = Tim_0(matran_hientai);
        if x == -1: continue

        for dx,dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if(Check(new_X,new_Y)):
                new_matran = DiChuyen(matran_hientai,x,y,new_X,new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str:
                         new_cost = cost + 1 # Chi phí mỗi bước là 1
                         if new_cost < visited.get(new_matran_str, float('inf')):
                             visited[new_matran_str] = new_cost
                             qp.put((new_cost, new_matran, path + [matran_hientai]))

    print(f"UCS: Expanded {nodes_expanded} nodes. Goal not found."); return []

def DFS(start_node, max_depth=50): # Thêm giới hạn độ sâu cho DFS để tránh treo
    stack = [(start_node,[], 0)] # (state, path, depth)
    visited = set();
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("DFS Error: Invalid start node."); return []
    visited.add(start_node_str); nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while stack:
        matran_hientai, path, depth = stack.pop(); nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai)
        if not matran_hientai_str: continue

        if matran_hientai_str == goal_str: print(f"DFS: Expanded {nodes_expanded} nodes."); return path + [matran_hientai]

        if depth >= max_depth: continue # Giới hạn độ sâu

        x,y = Tim_0(matran_hientai);
        if x == -1: continue

        # Duyệt ngược để có thứ tự khám phá giống DFS chuẩn hơn (L, R, D, U)
        for dx,dy in reversed(Moves):
            new_X, new_Y = x + dx, y + dy
            if (Check(new_X,new_Y)):
                new_matran = DiChuyen(matran_hientai,x,y,new_X,new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str and new_matran_str not in visited:
                        visited.add(new_matran_str)
                        stack.append((new_matran, path + [matran_hientai], depth + 1))

    print(f"DFS: Expanded {nodes_expanded} nodes. Goal not found within depth {max_depth}."); return []

def DFS_limited_recursive(current_node, limit, path, visited):
    global nodes_expanded_iddfs; nodes_expanded_iddfs += 1
    current_node_str = change_matran_string(current_node)
    goal_str = change_matran_string(Goal)
    if not current_node_str: return None

    current_path = path + [current_node] # Path lưu trữ các trạng thái matrix
    if current_node_str == goal_str: return current_path
    if limit == 0: return None

    x, y = Tim_0(current_node);
    if x == -1: return None

    for dx, dy in Moves: # Thứ tự không quá quan trọng trong DLS/IDDFS
        new_X, new_Y = x + dx, y + dy
        if Check(new_X, new_Y):
            neighbor_node = DiChuyen(current_node, x, y, new_X, new_Y)
            if neighbor_node:
                 neighbor_node_str = change_matran_string(neighbor_node)
                 if neighbor_node_str and neighbor_node_str not in visited:
                      visited.add(neighbor_node_str)
                      result = DFS_limited_recursive(neighbor_node, limit - 1, current_path, visited)
                      if result is not None: return result
                      visited.remove(neighbor_node_str) # Backtrack: remove khi quay lui khỏi nhánh này

    return None

def IDDFS(start_node, max_depth=50):
    global nodes_expanded_iddfs; total_nodes_expanded = 0
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("IDDFS Error: Invalid start node."); return []
    print(f"Running IDDFS up to depth {max_depth}...")
    for depth in range(max_depth + 1):
        # print(f"  Trying depth limit: {depth}")
        # Visited set reset cho mỗi lần lặp độ sâu
        visited = {start_node_str}; nodes_expanded_iddfs = 0 # Reset counter and visited per depth
        result = DFS_limited_recursive(start_node, depth, [], visited)
        total_nodes_expanded += nodes_expanded_iddfs
        # print(f"    Expanded {nodes_expanded_iddfs} nodes at depth {depth}.")
        if result is not None:
            print(f"  Goal found at depth {depth}."); print(f"IDDFS: Total expanded nodes: {total_nodes_expanded}.")
            return result
    print(f"  Goal not found within depth limit {max_depth}."); print(f"IDDFS: Total expanded nodes: {total_nodes_expanded}.")
    return []

def Greedy(start_node):
    qp = PriorityQueue()
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("Greedy Error: Invalid start node."); return []
    h_start = khoang_cach_mahathan(start_node)
    if h_start == float('inf'): print("Greedy Error: Start node invalid vs Goal."); return []
    qp.put( (h_start, start_node, []) ) # (heuristic, state, path)
    visited = set(); visited.add(start_node_str); nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while not qp.empty():
        h, matran_hientai, path = qp.get(); nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai)
        if not matran_hientai_str: continue

        if matran_hientai_str == goal_str: print(f"Greedy Search: Expanded {nodes_expanded} nodes."); return path + [matran_hientai]

        x,y = Tim_0(matran_hientai);
        if x == -1: continue

        for dx,dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if(Check(new_X,new_Y)):
                new_matran = DiChuyen(matran_hientai,x,y,new_X,new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str and new_matran_str not in visited:
                        visited.add(new_matran_str)
                        h_new = khoang_cach_mahathan(new_matran)
                        if h_new != float('inf'): # Only add valid states
                            qp.put((h_new, new_matran, path + [matran_hientai]))

    print(f"Greedy Search: Expanded {nodes_expanded} nodes. Goal not found."); return []

def A_Star(start_node):
    qp = PriorityQueue()
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("A* Error: Invalid start node."); return []
    g_cost = 0
    h_cost = khoang_cach_mahathan(start_node)
    if h_cost == float('inf'): print("A* Error: Start node invalid vs Goal."); return []
    f_cost = g_cost + h_cost
    qp.put( (f_cost, g_cost, start_node, []) ) # (f_cost, g_cost, state, path)
    visited = {start_node_str: 0}; nodes_expanded = 0 # Store min g_cost to reach state
    goal_str = change_matran_string(Goal)

    while not qp.empty():
        f_n, g_n, matran_hientai, path = qp.get(); nodes_expanded += 1
        matran_str = change_matran_string(matran_hientai)
        if not matran_str: continue

        # Optimization: If we found a shorter path already, skip
        if g_n > visited.get(matran_str, float('inf')): continue

        if matran_str == goal_str: print(f"A*: Expanded {nodes_expanded} nodes."); return path + [matran_hientai]

        x,y = Tim_0(matran_hientai);
        if x == -1: continue

        for dx,dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if(Check(new_X,new_Y)):
                new_matran = DiChuyen(matran_hientai,x,y,new_X,new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str:
                        g_new = g_n + 1
                        if g_new < visited.get(new_matran_str, float('inf')):
                            h_new = khoang_cach_mahathan(new_matran)
                            if h_new != float('inf'):
                                visited[new_matran_str] = g_new
                                f_new = g_new + h_new
                                qp.put((f_new, g_new, new_matran, path + [matran_hientai]))

    print(f"A*: Expanded {nodes_expanded} nodes. Goal not found."); return []

def IDA_Search(node, g_cost, threshold, path, visited_in_path):
    global nodes_expanded_ida; nodes_expanded_ida += 1
    node_str = change_matran_string(node)
    goal_str = change_matran_string(Goal)
    if not node_str: return None, float('inf')

    current_path = path + [node] # Path stores states
    h_cost = khoang_cach_mahathan(node)
    if h_cost == float('inf'): return None, float('inf') # Invalid state vs goal
    f_cost = g_cost + h_cost

    if f_cost > threshold: return None, f_cost # Prune if exceeds threshold
    if node_str == goal_str: return current_path, f_cost # Goal found

    min_f_cost_above_threshold = float('inf') # Track min f-cost that exceeds threshold

    x, y = Tim_0(node);
    if x == -1: return None, float('inf') # Invalid state

    # Generate neighbors
    for dx, dy in Moves:
        new_X, new_Y = x + dx, y + dy
        if Check(new_X, new_Y):
            neighbor_node = DiChuyen(node, x, y, new_X, new_Y)
            if neighbor_node:
                neighbor_str = change_matran_string(neighbor_node)
                # Avoid cycles within the current path search
                if neighbor_str and neighbor_str not in visited_in_path:
                     visited_in_path.add(neighbor_str) # Add before recursive call
                     result_path, new_threshold_component = IDA_Search(neighbor_node, g_cost + 1, threshold, current_path, visited_in_path)
                     visited_in_path.remove(neighbor_str) # Remove after recursive call (backtrack)

                     if result_path is not None: return result_path, threshold # Goal found in subtree

                     # Update the minimum cost found that was > threshold
                     min_f_cost_above_threshold = min(min_f_cost_above_threshold, new_threshold_component)

    return None, min_f_cost_above_threshold # Return path=None and the minimum f exceeding threshold

def IDA(start_node, initial_threshold=None, max_threshold=100):
    global nodes_expanded_ida; total_nodes_expanded = 0
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("IDA* Error: Invalid start node."); return []
    h_start = khoang_cach_mahathan(start_node)
    if h_start == float('inf'): print("IDA* Error: Start node invalid vs Goal."); return []

    threshold = h_start if initial_threshold is None else initial_threshold
    print(f"Running IDA*..."); ida_step_limit = 50; steps = 0 # Limit iterations

    while steps < ida_step_limit and threshold <= max_threshold:
        # print(f"  Trying threshold: {threshold}")
        # visited_in_path reset for each iteration, starts with only the start node
        visited_in_path = {start_node_str}; nodes_expanded_ida = 0 # Reset counter and visited per threshold
        result_path, new_threshold = IDA_Search(start_node, 0, threshold, [], visited_in_path)
        total_nodes_expanded += nodes_expanded_ida
        # print(f"    Expanded {nodes_expanded_ida} nodes with threshold {threshold}.")

        if result_path is not None:
            print(f"  Goal found with threshold {threshold}."); print(f"IDA*: Total expanded nodes: {total_nodes_expanded}.")
            return result_path # Return the path of states

        if new_threshold == float('inf'):
            print("  No solution found (explored all reachable states or threshold too low initially).")
            break
        if new_threshold <= threshold:
            # This might happen if goal has f_cost equal to current threshold but wasn't found due to path constraints
            # Or if heuristic is inconsistent? Usually we just increase. Let's force increase slightly.
            print(f"  Warning: New threshold {new_threshold} <= current {threshold}. Incrementing slightly.")
            threshold += 1 # Or some small epsilon if using floats
        else:
             threshold = new_threshold # Update threshold for next iteration

        steps += 1

    if threshold > max_threshold: print(f"  Threshold limit ({max_threshold}) reached, stopping.")
    elif steps >= ida_step_limit: print(f"  IDA* reached step limit ({ida_step_limit}) without finding solution.")
    print(f"IDA*: Total expanded nodes: {total_nodes_expanded}."); return []


# --- Thuật toán Local Search ---
# (Giữ nguyên Simple_Hill_Climbing_First_Choice, Steepest_Ascent_Hill_Climbing, Stochastic_Hill_Climbing, Simulated_Annealing)
def Simple_Hill_Climbing_First_Choice(start_node, max_steps=1000):
    print(f"Running Simple Hill Climbing (First Choice) with max_steps={max_steps}")
    current_state = start_node; path = [current_state]; steps = 0; nodes_evaluated = 0
    goal_str = change_matran_string(Goal)
    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str: print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states."); return path # Return path of states

        x, y = Tim_0(current_state);
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state); moved = False

        # Generate neighbors and check in random order
        random_moves = random.sample(Moves, len(Moves))
        for dx, dy in random_moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1 # Count neighbor evaluation
                    h_neighbor = khoang_cach_mahathan(neighbor_state)
                    if h_neighbor < h_current:
                        current_state = neighbor_state
                        path.append(current_state) # Add new state to path
                        moved = True
                        break # Take the first better move found

        if not moved:
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            # Return path found so far, even if stuck
            return path

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    # Return path found so far
    return path

def Steepest_Ascent_Hill_Climbing(start_node, max_steps=1000):
    print(f"Running Steepest Ascent Hill Climbing with max_steps={max_steps}")
    current_state = start_node; path = [current_state]; steps = 0; nodes_evaluated = 0
    goal_str = change_matran_string(Goal)
    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SAHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str: print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states."); return path

        x, y = Tim_0(current_state);
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state)
        best_neighbor = None
        h_best_neighbor = h_current # Initialize with current heuristic

        # Evaluate all neighbors
        for dx, dy in Moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1
                    h_neighbor = khoang_cach_mahathan(neighbor_state)
                    # Find neighbor with the strictly lowest heuristic
                    if h_neighbor < h_best_neighbor:
                        h_best_neighbor = h_neighbor
                        best_neighbor = neighbor_state # Store the best state found

        # Move to the best neighbor only if it's strictly better than current
        if best_neighbor is not None:
            current_state = best_neighbor
            path.append(current_state)
        else:
            # Stuck at local optimum or plateau
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            return path

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    return path

def Stochastic_Hill_Climbing(start_node, max_steps=1000):
    print(f"Running Stochastic Hill Climbing with max_steps={max_steps}")
    current_state = start_node; path = [current_state]; steps = 0; nodes_evaluated = 0
    goal_str = change_matran_string(Goal)
    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str: print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states."); return path

        x, y = Tim_0(current_state);
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state)
        better_neighbors = [] # List of states that are better

        # Find all strictly better neighbors
        for dx, dy in Moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1
                    h_neighbor = khoang_cach_mahathan(neighbor_state)
                    if h_neighbor < h_current:
                        better_neighbors.append(neighbor_state)

        # Choose randomly among the better neighbors if any exist
        if better_neighbors:
            next_state = random.choice(better_neighbors)
            current_state = next_state
            path.append(current_state)
        else:
            # Stuck if no better neighbors
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            return path

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    return path

def Simulated_Annealing(start_node, initial_temp=100.0, cooling_rate=0.95, min_temp=0.1, max_iterations=10000):
    print(f"Running Simulated Annealing (T_init={initial_temp}, alpha={cooling_rate}, T_min={min_temp}, max_iter={max_iterations})")
    current_state = start_node
    current_h = khoang_cach_mahathan(current_state)
    if current_h == float('inf'): print("SA Error: Invalid start state."); return []

    T = initial_temp
    iterations = 0
    nodes_evaluated = 1 # Count initial state
    path = [current_state] # Track sequence of accepted states

    # Track the best state encountered globally
    best_state_so_far = copy.deepcopy(current_state) # Use deepcopy for safety
    best_h_so_far = current_h

    goal_str = change_matran_string(Goal)

    while T > min_temp and iterations < max_iterations:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SA Error: Invalid current state during run."); return []

        if current_state_str == goal_str:
            print(f"  Goal found after {iterations} iterations (T={T:.2f}). Evaluated {nodes_evaluated} states.")
            return path # Return path that led to the goal

        x, y = Tim_0(current_state);
        if x == -1: print("  Error: Cannot find blank tile."); return []

        # Generate possible moves (new blank positions)
        possible_moves_coords = []
        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                possible_moves_coords.append((new_X, new_Y))

        if not possible_moves_coords:
            # print("  No possible moves from current state.")
            break # Stop if no moves possible

        # Choose a random move (random new blank position)
        chosen_new_blank_pos = random.choice(possible_moves_coords)
        next_state = DiChuyen(current_state, x, y, chosen_new_blank_pos[0], chosen_new_blank_pos[1])

        if next_state:
            nodes_evaluated += 1
            next_h = khoang_cach_mahathan(next_state)
            if next_h == float('inf'): # Avoid moving to invalid states
                continue

            # Update best state found so far
            if next_h < best_h_so_far:
                best_h_so_far = next_h
                best_state_so_far = copy.deepcopy(next_state)

            # Decide whether to accept the move
            delta_e = next_h - current_h
            accept = False
            if delta_e < 0: # Always accept better moves
                accept = True
            else: # Accept worse moves with probability exp(-delta_e / T)
                # Add a check for T > 0 to avoid potential division by zero if min_temp is 0
                if T > 1e-9 and random.random() < math.exp(-delta_e / T):
                    accept = True

            if accept:
                current_state = next_state
                current_h = next_h
                path.append(current_state) # Append accepted state to path

        # Cool down
        T *= cooling_rate
        iterations += 1

    # After loop finishes, check if current or best state is goal
    final_state_str = change_matran_string(current_state)
    best_state_str = change_matran_string(best_state_so_far)

    if final_state_str == goal_str:
        print(f"  Goal found at the end (Iter {iterations}, T={T:.2f}). Evaluated {nodes_evaluated} states.")
        return path # Path led to goal
    elif best_state_str == goal_str:
        print(f"  Goal was visited (best state) but ended elsewhere. Returning path to goal is complex. Reporting Goal Found. Evaluated {nodes_evaluated} states.")
        # Difficult to return the actual path TO best_state_so_far unless tracked explicitly.
        # For consistency with other local searches, return [Goal] to indicate success.
        return [Goal] # Indicate goal was found
    else:
        reason = f"Reached max iterations ({iterations})" if iterations >= max_iterations else f"Temperature dropped below minimum ({T:.2f})"
        print(f"  Simulated Annealing finished without finding goal ({reason}). Evaluated {nodes_evaluated} states.")
        print(f"  Ended at state with h={current_h}. Best state found had h={best_h_so_far}.")
        # Return path found so far, even if not goal
        return path

# --- Beam Search ---
# (Giữ nguyên Beam_Search)
def Beam_Search(start_node, beam_width, max_iterations=1000):
    print(f"Running Beam Search (beam_width={beam_width}, max_iter={max_iterations})")
    start_node_str = change_matran_string(start_node)
    if not start_node_str: print("Beam Search Error: Invalid start node."); return []
    h_start = khoang_cach_mahathan(start_node)
    if h_start == float('inf'): print("Beam Search Error: Start node invalid vs Goal."); return []

    # Beam stores tuples: (heuristic_cost, state, path_list_of_states)
    beam = [(h_start, start_node, [start_node])] # Initial beam with start state
    visited = {start_node_str} # Keep track of visited states overall
    iterations = 0
    total_nodes_evaluated = 1 # Count initial state
    goal_str = change_matran_string(Goal)

    while iterations < max_iterations and beam:
        candidates = [] # Candidates for the next beam

        # Check if goal is already in the current beam
        for h, current_state, path in beam:
             current_state_str = change_matran_string(current_state)
             if current_state_str == goal_str:
                  print(f"  Goal found within beam after {iterations} iterations. Total evaluated states (approx): {total_nodes_evaluated}.")
                  return path # Return the path leading to the goal state

        # Generate successors (candidates) for all states currently in the beam
        for h, current_state, path in beam:
             # Skip if goal was found above (redundant but safe)
             current_state_str = change_matran_string(current_state)
             if current_state_str == goal_str: continue

             x, y = Tim_0(current_state);
             if x == -1: continue # Skip invalid states in beam

             for dx, dy in Moves:
                 new_X, new_Y = x + dx, y + dy
                 if Check(new_X, new_Y):
                     neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                     if neighbor_state:
                         neighbor_str = change_matran_string(neighbor_state)
                         # Add to candidates if valid and not visited before
                         if neighbor_str and neighbor_str not in visited:
                              visited.add(neighbor_str)
                              total_nodes_evaluated += 1
                              h_neighbor = khoang_cach_mahathan(neighbor_state)
                              if h_neighbor != float('inf'): # Only add valid states
                                  # Append the new state to the path
                                  candidates.append((h_neighbor, neighbor_state, path + [neighbor_state]))

        # If no valid, unvisited candidates generated, stop
        if not candidates:
            print(f"  Beam Search stopped after {iterations} iterations: No new valid candidates generated.")
            break

        # Sort candidates by heuristic cost (ascending)
        candidates.sort(key=lambda item: item[0])

        # Select the top 'beam_width' candidates for the next beam (pruning)
        beam = candidates[:beam_width]
        iterations += 1

    # Final check in the last beam after loop finishes
    for h, state, path in beam:
        state_str = change_matran_string(state)
        if state_str == goal_str:
            print(f"  Goal found in the final beam after {iterations} iterations. Total evaluated states (approx): {total_nodes_evaluated}.")
            return path

    reason = f"Reached max iterations ({iterations})" if iterations >= max_iterations else "Beam became empty"
    print(f"  Beam Search finished without finding goal ({reason}). Total evaluated states (approx): {total_nodes_evaluated}.")
    return [] # Return empty list if goal not found


# --- Thuật toán Tiến hóa / Metaheuristic ---
# (Giữ nguyên Genetic_Algorithm)
def Genetic_Algorithm(start, goal, population_size=100, generations=100, mutation_rate=0.1):
    print(f"Running Genetic Algorithm (pop_size={population_size}, gens={generations}, mutation_rate={mutation_rate})")
    nodes_evaluated_ga = 0 # Local counter for GA evaluations

    def fitness(individual, goal_state=goal):
        nonlocal nodes_evaluated_ga
        nodes_evaluated_ga += 1
        # Fitness is lower for better states (closer to 0)
        return khoang_cach_mahathan(individual, goal_state)

    # Crossover: Single point crossover on flattened representation
    def crossover(parent1, parent2):
        # Basic validation
        if not isinstance(parent1, list) or len(parent1)!=3 or not all(isinstance(r, list) and len(r)==3 for r in parent1): return None
        if not isinstance(parent2, list) or len(parent2)!=3 or not all(isinstance(r, list) and len(r)==3 for r in parent2): return None

        flat1 = [num for row in parent1 for num in row]
        flat2 = [num for row in parent2 for num in row]
        size = len(flat1)
        child_flat = [-1] * size # Initialize with placeholder

        # Choose crossover point
        point1, point2 = random.sample(range(size), 2)
        start_point = min(point1, point2)
        end_point = max(point1, point2)

        # Copy the segment from parent1
        child_flat[start_point : end_point+1] = flat1[start_point : end_point+1]

        # Fill the remaining spots with genes from parent2 in order, avoiding duplicates
        current_parent2_idx = 0
        for i in range(size):
            if child_flat[i] == -1: # If spot needs filling
                while flat2[current_parent2_idx] in child_flat[start_point : end_point+1]:
                    current_parent2_idx += 1
                    if current_parent2_idx >= size: return None # Error case
                child_flat[i] = flat2[current_parent2_idx]
                current_parent2_idx += 1

        # Check if valid (should contain 0-8 exactly once) - Basic check
        if len(set(child_flat)) != 9 or set(child_flat) != set(range(9)):
             # print("Warning: Crossover produced invalid child")
             return None # Or return a copy of a parent? Returning None is safer

        # Reshape back to 3x3
        return [child_flat[i*3:(i+1)*3] for i in range(3)]

    # Mutation: Swap the blank tile with a random adjacent tile
    def mutate(individual):
         if not isinstance(individual, list) or len(individual)!=3: return individual # Basic check
         mutated_individual = [row[:] for row in individual] # Work on a copy
         x, y = Tim_0(mutated_individual)
         if x == -1: return individual # Cannot mutate if no blank tile

         possible_moves = []
         for dx, dy in Moves:
             new_x, new_y = x + dx, y + dy
             if Check(new_x, new_y):
                 possible_moves.append((new_x, new_y))

         if possible_moves:
             new_x, new_y = random.choice(possible_moves)
             # Perform the swap using DiChuyen logic (or directly)
             mutated_individual[x][y], mutated_individual[new_x][new_y] = mutated_individual[new_x][new_y], mutated_individual[x][y]

         return mutated_individual

    # --- GA Main Loop ---
    population = []
    visited_init_strings = set() # Track initial population states

    # Initialize Population: Generate diverse states by random walks from Goal
    print("  Initializing population...")
    nodes_evaluated_ga += population_size # Approximate cost of generation
    max_init_attempts = population_size * 5 # Prevent infinite loop if Goal is hard to move from
    attempts = 0
    goal_copy = [row[:] for row in goal] # Work with a copy of goal
    goal_str = change_matran_string(goal_copy)
    visited_init_strings.add(goal_str)
    population.append(goal_copy) # Add goal state itself

    while len(population) < population_size and attempts < max_init_attempts:
        attempts += 1
        # Start from Goal and walk back randomly
        current = [row[:] for row in goal]
        steps = random.randint(15, 50) # Number of random moves from goal
        for _ in range(steps):
            x, y = Tim_0(current)
            if x == -1: break # Should not happen starting from goal

            possible_moves_coords = []
            for dx, dy in Moves:
                nx, ny = x + dx, y + dy
                if Check(nx, ny):
                    possible_moves_coords.append((nx, ny))

            if not possible_moves_coords: break
            nx, ny = random.choice(possible_moves_coords)
            current = DiChuyen(current, x, y, nx, ny)
            if current is None: # If DiChuyen failed, break walk
                 current = [row[:] for row in goal]; break # Reset to goal

        current_str = change_matran_string(current)
        # Add to population if it's a valid state and not already added
        if current_str and current_str not in visited_init_strings:
            population.append(current)
            visited_init_strings.add(current_str)

    if len(population) < population_size:
         print(f"Warning: Could only initialize {len(population)} unique states for population.")
         if not population: print("Error: Failed to initialize any population."); return []


    best_overall_individual = None
    best_overall_fitness = float('inf')

    # Evolution Loop
    for generation in range(generations):
        # Evaluate fitness of current population
        # Sort population by fitness (lower is better)
        population.sort(key=lambda ind: fitness(ind, goal))

        current_best_fitness = fitness(population[0], goal)

        # Check for solution
        if current_best_fitness == 0:
            print(f"  Goal found in generation {generation+1}. Total states evaluated (approx): {nodes_evaluated_ga}.")
            # GA returns the goal state found, not the path
            return [population[0]]

        # Update overall best
        if current_best_fitness < best_overall_fitness:
            best_overall_fitness = current_best_fitness
            best_overall_individual = copy.deepcopy(population[0]) # Store the best state matrix

        # Selection and Reproduction
        next_generation = []

        # Elitism: Carry over the best individuals directly
        elite_count = max(1, int(population_size * 0.1)) # Keep top 10% or at least 1
        next_generation.extend(copy.deepcopy(ind) for ind in population[:elite_count])

        # Select parents from a better portion of the population
        parent_pool_size = max(elite_count, population_size // 2) # Pool size at least elite_count
        parent_pool = population[:parent_pool_size]

        # Generate the rest of the new generation through crossover and mutation
        while len(next_generation) < population_size:
             # Select two parents randomly from the pool
             parent1 = random.choice(parent_pool)
             parent2 = random.choice(parent_pool)

             child = crossover(parent1, parent2)

             # If crossover failed, maybe try again or skip
             if child is None:
                 continue # Skip this attempt

             # Apply mutation with a certain probability
             if random.random() < mutation_rate:
                 child = mutate(child)

             # Add the valid child to the next generation
             if change_matran_string(child): # Ensure child is valid before adding
                 next_generation.append(child)

        population = next_generation # Replace old population with the new one

        # Optional: Print progress
        # if (generation + 1) % 10 == 0:
        #      print(f"  Generation {generation+1}/{generations}, Best Fitness: {best_overall_fitness}")


    # If loop finishes without finding the goal
    print(f"  Genetic Algorithm finished after {generations} generations without finding goal.")
    print(f"  Best fitness found: {best_overall_fitness}. Total states evaluated (approx): {nodes_evaluated_ga}.")
    # Return the best individual found during the search
    # Return [] for consistency like local search, or return best_overall_individual?
    # Let's return [] to indicate goal *state* wasn't the final state.
    return []

# --- Thuật toán Conformant BFS (Thêm vào) ---
# Cần định nghĩa lại các hàm helper cần thiết hoặc điều chỉnh thuật toán
# Sử dụng các hàm helper hiện có: change_matran_string, Tim_0, DiChuyen, Check

def conformant_bfs(initial_belief_state_list, goal_state=Goal):
    """BFS on the belief state space. Returns path of move *names* ('U', 'D', 'L', 'R') or None."""
    print(f"Running Conformant BFS...")
    nodes_expanded_conf = 0

    # --- Validation ---
    if not initial_belief_state_list:
        print("Conformant BFS Error: Initial belief state list is empty.")
        return None
    goal_str = change_matran_string(goal_state)
    if not goal_str:
        print("Conformant BFS Error: Invalid goal state.")
        return None

    # --- Initial Belief State Setup ---
    # Convert initial list of lists into a frozenset of strings for hashing
    initial_belief_set_str = set()
    for state in initial_belief_state_list:
        state_str = change_matran_string(state)
        if state_str:
            initial_belief_set_str.add(state_str)
        else:
            print(f"Warning: Invalid state removed from initial belief set: {state}")
    if not initial_belief_set_str:
        print("Conformant BFS Error: Initial belief state contains no valid states.")
        return None
    initial_belief_frozenset = frozenset(initial_belief_set_str)

    # --- Check if initial state is goal ---
    is_initial_goal = all(state_str == goal_str for state_str in initial_belief_frozenset)
    if is_initial_goal:
        print("  Initial belief state is already the goal state.")
        return [] # Empty path

    # --- BFS Initialization ---
    queue = deque([(initial_belief_frozenset, [])]) # (current_belief_frozenset_of_strings, path_of_move_names)
    visited = {initial_belief_frozenset} # Set of frozensets of strings
    MAX_BFS_NODES = 50000 # Safety limit to prevent excessive memory usage

    while queue:
        nodes_expanded_conf += 1
        if nodes_expanded_conf > MAX_BFS_NODES:
            print(f"  Conformant BFS: Node limit ({MAX_BFS_NODES}) reached. Aborting.")
            return None

        current_belief_fset_str, path_names = queue.popleft()

        # --- Try each possible move ---
        for move_name, move_dir in Moves_Dir_Name.items(): # e.g., move_name='U', move_dir=(-1, 0)
            next_belief_set_str = set()
            possible_move = True # Flag to check if move is valid for all states in belief

            # Apply move to each state in the current belief set
            for state_str in current_belief_fset_str:
                # Convert string back to matrix to apply move (less efficient but works with current helpers)
                state_list = [list(map(int, list(state_str[i*3:(i+1)*3]))) for i in range(3)]

                x, y = Tim_0(state_list)
                if x == -1:
                    # print(f"Warning: Could not find blank in state {state_str} within belief set.")
                    possible_move = False; break # Move invalid if blank isn't found in one state

                new_x, new_y = x + move_dir[0], y + move_dir[1]

                if Check(new_x, new_y):
                    next_state_list = DiChuyen(state_list, x, y, new_x, new_y)
                    if next_state_list:
                        next_state_str = change_matran_string(next_state_list)
                        if next_state_str:
                            next_belief_set_str.add(next_state_str)
                        else:
                            # print(f"Warning: DiChuyen resulted in invalid state string for move {move_name} from {state_str}")
                            possible_move = False; break
                    else:
                        # print(f"Warning: DiChuyen failed for move {move_name} from {state_str}")
                        possible_move = False; break
                else:
                    # If the move is invalid for *this specific state*, the resulting
                    # belief state still only contains the *original* state (as if no move happened).
                    # However, conformant planning usually assumes actions *must* be applicable
                    # to all states, or the plan fails. Let's assume failure if not applicable to all.
                    # Alternative: only add `state_str` back if move invalid? Depends on exact semantics.
                    # Let's stick to: If move is invalid for ANY state, the action is invalid for the belief state.
                    # Correction: A move *is* applicable if it's valid for *at least one* state? No, conformant means it must achieve the desired outcome regardless of the *actual* physical state. If a move leads to different *relative* outcomes or fails for some, it's problematic.
                    # Let's reconsider: If move (e.g., 'U') is attempted:
                    # State A: Blank at (1,1). 'U' moves blank to (0,1). -> New state A'
                    # State B: Blank at (0,0). 'U' is invalid.
                    # What is the resulting belief state? It's {A', B}. The action 'U' was applied, resulting in a new set of possibilities.
                    # So, if Check(new_x, new_y) is false, the state *doesn't change* for that member of the belief set.

                    next_belief_set_str.add(state_str) # Add the original state back if move invalid

            # Skip this move direction if it caused an issue like invalid state generation
            # Or if the resulting belief set is empty (shouldn't happen with the logic above)
            if not possible_move or not next_belief_set_str:
                continue

            # --- Process Next Belief State ---
            next_belief_frozenset = frozenset(next_belief_set_str)

            # Skip if already visited
            if next_belief_frozenset in visited:
                continue

            # --- Check if Goal Reached ---
            # Goal is reached if *all* states in the belief set are the goal state
            is_goal = all(s_str == goal_str for s_str in next_belief_frozenset)
            if is_goal:
                print(f"  Conformant BFS: Goal reached! Expanded {nodes_expanded_conf} belief states.")
                return path_names + [move_name] # Return list of move names

            # --- Add to Queue and Visited ---
            visited.add(next_belief_frozenset)
            queue.append((next_belief_frozenset, path_names + [move_name]))

    print(f"Conformant BFS: Goal not found after expanding {nodes_expanded_conf} belief states.");
    return None # Return None if no solution found


# --- Phần chạy thử nghiệm ---
if __name__ == "__main__":
    print("="*30); print("Running ThuatToan.py as main script"); print("Trạng thái bắt đầu (Start):"); print_matrix(Start)
    print("\nTrạng thái đích (Goal):"); print_matrix(Goal); print("="*30 + "\n")

    # Reset global counters if they exist
    nodes_expanded_iddfs = 0
    nodes_expanded_ida = 0

    # Define algorithms to test
    algorithms_to_test = {
        "BFS": BFS,
        "UCS": UCS,
        #"DFS (Depth=50)": lambda s: DFS(s, max_depth=50), # DFS can be slow/deep
        "IDDFS (Depth=25)": lambda s: IDDFS(s, max_depth=25), # Limit depth for IDDFS test
        "Greedy": Greedy,
        "A*": A_Star,
        "IDA* (Thresh=80)": lambda s: IDA(s, max_threshold=80), # Limit threshold for IDA* test
        "Simple HC (First Choice)": lambda s: Simple_Hill_Climbing_First_Choice(s, max_steps=2000),
        "Steepest Ascent HC": lambda s: Steepest_Ascent_Hill_Climbing(s, max_steps=2000),
        "Stochastic HC": lambda s: Stochastic_Hill_Climbing(s, max_steps=2000),
        "Simulated Annealing": lambda s: Simulated_Annealing(s, initial_temp=50, cooling_rate=0.98, min_temp=0.01, max_iterations=15000), # Adjusted params
        "Beam Search (k=5)": lambda s: Beam_Search(s, beam_width=5, max_iterations=1000),
        "Beam Search (k=20)": lambda s: Beam_Search(s, beam_width=20, max_iterations=1000),
        "Genetic Algorithm": lambda s: Genetic_Algorithm(s, Goal, population_size=100, generations=200, mutation_rate=0.2),
        # Add Conformant BFS Test - requires an initial belief state list
        # "Conformant BFS": lambda belief_list: conformant_bfs(belief_list, Goal) # Uncomment later
    }

    # --- Run Standard Tests ---
    results = {}
    print("\n--- Running Standard Algorithm Tests ---")
    for name, func in algorithms_to_test.items():
        # Skip Conformant BFS for now in this loop
        if name == "Conformant BFS": continue

        print(f"\n--- Testing {name} ---")
        start_time = time.time()
        # Always pass a deep copy of Start to avoid modification issues
        start_state_copy = copy.deepcopy(Start)
        result = func(start_state_copy) # Standard algs take a single start state
        end_time = time.time()
        elapsed = end_time - start_time

        # Analyze result (most return list of states, GA/Local might return [Goal] or [])
        if result:
            # Check if it's a path (list of states)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0 and isinstance(result[0][0], list):
                 path_len = len(result) # Number of states in path
                 print(f"{name} found path length: {path_len} ({path_len-1} moves) in {elapsed:.4f}s")
                 # Optional: Verify last state is Goal
                 # if change_matran_string(result[-1]) == change_matran_string(Goal): print("  Path ends at Goal.")
                 # else: print("  Warning: Path does not end at Goal state!")
                 results[name] = (path_len, elapsed)
            # Check if it's specifically [Goal] returned by GA/Local Search
            elif isinstance(result, list) and len(result) == 1 and change_matran_string(result[0]) == change_matran_string(Goal):
                 print(f"{name} found the goal state in {elapsed:.4f}s")
                 results[name] = ("Goal Found", elapsed)
            else:
                 print(f"{name} returned an unexpected result format in {elapsed:.4f}s")
                 results[name] = ("Error/Unknown", elapsed)
        else:
             # Empty list [] usually means goal not found or search failed
             print(f"{name} did not find the goal in {elapsed:.4f}s")
             results[name] = (None, elapsed) # Use None for path length if not found

        print("-"*(len(name) + 12))


    # --- Run Conformant BFS Test Separately ---
    print("\n--- Running Conformant BFS Test ---")
    # Define an example initial belief state (must be a list of states)
    initial_belief_state = [
        [[2, 6, 5], [0, 8, 7], [4, 3, 1]], # The original Start state
        [[2, 6, 5], [8, 0, 7], [4, 3, 1]], # Blank swapped with 8
        [[2, 6, 5], [4, 8, 7], [0, 3, 1]]  # Blank swapped with 4
    ]
    print("Initial Belief State:")
    for i, state in enumerate(initial_belief_state):
        print(f" State {i+1}:")
        print_matrix(state)

    start_time = time.time()
    # Make sure to pass the list, not a single state
    conf_bfs_result_path_names = conformant_bfs(initial_belief_state, Goal)
    end_time = time.time()
    elapsed = end_time - start_time

    if conf_bfs_result_path_names is not None: # Returns list of move names or None
        path_len = len(conf_bfs_result_path_names)
        print(f"Conformant BFS found path length: {path_len} moves ({path_len} belief steps) in {elapsed:.4f}s")
        print(f"  Path (Move Names): {conf_bfs_result_path_names}")
        results["Conformant BFS"] = (path_len, elapsed)
    else:
        print(f"Conformant BFS did not find the goal in {elapsed:.4f}s")
        results["Conformant BFS"] = (None, elapsed)
    print("---------------------------------")


    # --- Print Summary ---
    print("\n" + "="*30); print("Summary of Results:"); print("-" * 30)
    # Sort results for better readability, maybe? For now, keep dict order.
    for name, (res, duration) in results.items():
         if res is not None:
             if isinstance(res, int): # Path length (number of states or moves depending on context)
                # For standard algs, res = states in path. For Conf BFS, res = moves. Adjust print.
                if name == "Conformant BFS":
                     print(f"{name:<25}: Path Length = {res:<5} moves, Time = {duration:.4f}s")
                else:
                     print(f"{name:<25}: Path Length = {res:<5} states ({max(0, res-1)} moves), Time = {duration:.4f}s")
             elif res == "Goal Found": # For GA/Local Search successful termination
                 print(f"{name:<25}: Goal Found{'':<16}, Time = {duration:.4f}s")
             else: # Error/Unknown
                 print(f"{name:<25}: Result = {str(res):<21}, Time = {duration:.4f}s")
         else: # Goal not found (returned [] or None)
             print(f"{name:<25}: Goal Not Found{'':<16}, Time = {duration:.4f}s")
    print("="*30)