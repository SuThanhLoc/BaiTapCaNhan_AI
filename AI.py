from collections import deque
import copy
from queue import PriorityQueue
import random
import math

Moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


def Find_Empty(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j
    return None


def Check(x, y):
    return 0 <= x < 3 and 0 <= y < 3


def Chinh_Sua_Ma_Tran(board, x, y, new_x, new_y):
    new_board = copy.deepcopy(board)
    new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
    return new_board


def BFS(start, goal):
    visited = set()
    queue = deque()
    queue.append((start, [start]))
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        current_tuple = tuple(tuple(row) for row in current)  # Chuyển đổi sớm hơn
        if current_tuple in visited:  # Kiểm tra trước khi xử lý
            continue
        visited.add(current_tuple)

        x, y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = x + dx, y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, x, y, new_x, new_y)
                # Không cần kiểm tra visited ở đây nữa nếu đã kiểm tra ở đầu vòng lặp
                new_path = path + [new_state]
                queue.append((new_state, new_path))
    return None


def Uniform_Cost_Search(start, goal):
    visited = set()
    open_queue = PriorityQueue()
    open_queue.put((0, start, [start]))  # (cost, state, path)

    # Lưu trữ chi phí tốt nhất đến mỗi trạng thái đã mở hoặc đã thăm
    # Điều này quan trọng cho UCS để đảm bảo tìm đường đi ngắn nhất
    g_costs = {tuple(map(tuple, start)): 0}

    while not open_queue.empty():
        cost, current, path = open_queue.get()
        current_tuple = tuple(tuple(row) for row in current)

        if current_tuple in visited and g_costs.get(current_tuple, float('inf')) <= cost:
            continue  # Nếu đã thăm với chi phí tốt hơn hoặc bằng thì bỏ qua

        visited.add(current_tuple)
        # g_costs[current_tuple] = cost # Đã được xử lý khi thêm vào open_queue

        if current == goal:
            return path

        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                new_state_tuple = tuple(tuple(row) for row in new_state)
                new_cost = cost + 1

                if new_state_tuple not in visited or new_cost < g_costs.get(new_state_tuple, float('inf')):
                    g_costs[new_state_tuple] = new_cost
                    open_queue.put((new_cost, new_state, path + [new_state]))
    return None


def DFS(start, goal):
    visited = set()  # Chỉ lưu các trạng thái đã được mở rộng hoàn toàn
    open_stack = []
    open_stack.append((start, [start]))

    while open_stack:
        current, path = open_stack.pop()
        current_tuple = tuple(tuple(row) for row in current)

        if current == goal:
            return path

        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        X, Y = Find_Empty(current)
        for dx, dy in reversed(Moves):  # Duyệt ngược để có thể khớp với hành vi của DFS truyền thống
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                # Không kiểm tra visited ở đây, để cho phép khám phá lại nếu tìm được đường đi khác (mặc dù DFS thường không làm vậy)
                # Hoặc, nếu muốn tránh chu trình hoàn toàn:
                # new_state_tuple_for_check = tuple(tuple(row) for row in new_state)
                # if new_state_tuple_for_check not in visited:
                open_stack.append((new_state, path + [new_state]))
    return None


def depth_bounded_search(start, goal, depth_bound, path_so_far_tuples):
    current_tuple = tuple(tuple(row) for row in start)

    if start == goal:
        return [start]  # Trả về list chứa goal state

    if depth_bound <= 0:
        return None

    if current_tuple in path_so_far_tuples:  # Tránh chu trình trong đường đi hiện tại
        return None

    path_so_far_tuples.add(current_tuple)  # Thêm vào tập các trạng thái của đường đi hiện tại

    X, Y = Find_Empty(start)
    for dx, dy in Moves:
        new_x, new_y = X + dx, Y + dy
        if Check(new_x, new_y):
            new_state = Chinh_Sua_Ma_Tran(start, X, Y, new_x, new_y)
            # Tạo một bản sao của path_so_far_tuples cho mỗi nhánh đệ quy nếu không muốn side-effect
            # Hoặc xóa sau khi gọi đệ quy (backtrack)
            solution = depth_bounded_search(new_state, goal, depth_bound - 1, path_so_far_tuples)
            if solution is not None:
                return [start] + solution  # Xây dựng đường đi ngược lên

    path_so_far_tuples.remove(current_tuple)  # Backtrack: xóa khỏi tập trạng thái của đường đi hiện tại
    return None


def Iterative_Deepening_DFS(start, goal):
    depth = 0
    max_allowable_depth = 35  # Giới hạn thực tế cho 8-puzzle, có thể cần điều chỉnh
    while depth <= max_allowable_depth:
        visited_for_current_depth = set()  # Dùng để tránh lặp trong một lần DBS
        solution = depth_bounded_search(start, goal, depth, visited_for_current_depth)
        if solution is not None:
            return solution
        depth += 1
    return None  # Nếu vượt quá max_allowable_depth


def Manhattan_Heuristic(current, goal):
    distance = 0
    pos_map = {}  # Lưu vị trí của các số trong bảng đích để tra cứu nhanh
    for r_idx, row in enumerate(goal):
        for c_idx, val in enumerate(row):
            if val != 0:  # Không tính ô trống
                pos_map[val] = (r_idx, c_idx)

    for r_idx, row in enumerate(current):
        for c_idx, val in enumerate(row):
            if val != 0:
                if val in pos_map:
                    goal_x, goal_y = pos_map[val]
                    distance += abs(r_idx - goal_x) + abs(c_idx - goal_y)
                # else: trường hợp số không có trong goal (không nên xảy ra với 8-puzzle chuẩn)
    return distance


def Greedy_Search(start, goal):
    visited = set()  # Lưu các trạng thái đã được mở rộng (tuple)
    open_queue = PriorityQueue()
    # (heuristic_cost, state, path)
    open_queue.put((Manhattan_Heuristic(start, goal), start, [start]))

    while not open_queue.empty():
        h_cost, current, path = open_queue.get()
        current_tuple = tuple(tuple(row) for row in current)

        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        if current == goal:
            return path

        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                # Không cần kiểm tra visited ở đây vì ta kiểm tra ở đầu vòng lặp
                open_queue.put((Manhattan_Heuristic(new_state, goal), new_state, path + [new_state]))
    return None


def A_Star_Search(start, goal):
    open_queue = PriorityQueue()
    # (f_cost, g_cost, state, path)
    # g_costs lưu chi phí thực tế (số bước) từ start đến một trạng thái
    g_costs = {tuple(map(tuple, start)): 0}
    # f_cost = g_cost + h_cost
    open_queue.put((0 + Manhattan_Heuristic(start, goal), 0, start, [start]))

    # closed_set (visited) không hoàn toàn cần thiết nếu ta kiểm tra g_costs khi lấy ra từ open_queue
    # và khi thêm vào. Nhưng để an toàn, có thể dùng visited.
    visited_for_expansion = set()

    while not open_queue.empty():
        f_cost_curr, g_cost_curr, current, path = open_queue.get()
        current_tuple = tuple(tuple(row) for row in current)

        if current_tuple in visited_for_expansion:  # Nếu đã mở rộng rồi thì bỏ qua
            continue
        visited_for_expansion.add(current_tuple)

        if current == goal:
            return path

        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                new_state_tuple = tuple(tuple(row) for row in new_state)

                g_cost_new = g_cost_curr + 1

                # Nếu trạng thái mới đã có trong g_costs và chi phí cũ tốt hơn, bỏ qua
                if g_cost_new >= g_costs.get(new_state_tuple, float('inf')):
                    continue

                g_costs[new_state_tuple] = g_cost_new
                h_cost_new = Manhattan_Heuristic(new_state, goal)
                f_cost_new = g_cost_new + h_cost_new
                open_queue.put((f_cost_new, g_cost_new, new_state, path + [new_state]))
    return None


def Find_X(x_val, goal_board):  # Giữ nguyên hàm này
    for r in range(3):
        for c in range(3):
            if x_val == goal_board[r][c]:
                return r, c
    return None, None


# --- IDA* ---
def ida_star_search_recursive(current_path, g_cost, bound, goal, nodes_generated_count):
    nodes_generated_count += 1
    current_state = current_path[-1]
    h_cost = Manhattan_Heuristic(current_state, goal)
    f_cost = g_cost + h_cost

    if f_cost > bound:
        return f_cost, nodes_generated_count  # Trả về f_cost để có thể làm new_bound

    if current_state == goal:
        return 'FOUND', nodes_generated_count

    min_f_cost_above_bound = float('inf')

    empty_r, empty_c = Find_Empty(current_state)

    for dr, dc in Moves:  # Có thể thử random.shuffle(Moves)
        new_r, new_c = empty_r + dr, empty_c + dc
        if Check(new_r, new_c):
            new_state = Chinh_Sua_Ma_Tran(current_state, empty_r, empty_c, new_r, new_c)
            # Kiểm tra new_state có trong current_path (trừ state cuối) để tránh chu trình đơn giản
            # Đối với IDA*, việc tránh chu trình hoàn toàn có thể phức tạp hơn.
            # Cách đơn giản là không quay lại trạng thái തൊട്ടു മുന്നിലെ.
            # Hoặc, nếu current_path không quá dài, có thể kiểm tra:
            is_cycle = False
            new_state_tuple_for_cycle_check = tuple(map(tuple, new_state))
            for past_state in current_path:  # Không nên duyệt toàn bộ path nếu path dài
                if tuple(map(tuple, past_state)) == new_state_tuple_for_cycle_check:
                    is_cycle = True
                    break
            if not is_cycle:
                # if len(current_path) < 2 or new_state != current_path[-2]: # Tránh quay lại trạng thái trước đó ngay
                current_path.append(new_state)
                result, nodes_generated_count = ida_star_search_recursive(current_path, g_cost + 1, bound, goal,
                                                                          nodes_generated_count)
                current_path.pop()  # Backtrack

                if result == 'FOUND':
                    return 'FOUND', nodes_generated_count
                if result < min_f_cost_above_bound:
                    min_f_cost_above_bound = result

    return min_f_cost_above_bound, nodes_generated_count


def IDA(start, goal, initial_bound_depreciated=30):  # initial_bound không thực sự dùng ở đây
    bound = Manhattan_Heuristic(start, goal)
    current_path = [start]  # current_path được thay đổi trực tiếp trong hàm đệ quy
    nodes_generated = 0
    max_ida_iterations = 20  # Giới hạn số lần tăng bound
    iter_count = 0

    while iter_count < max_ida_iterations:
        iter_count += 1
        # print(f"IDA* Iteration {iter_count}, Bound: {bound}")
        # Tạo lại path từ start cho mỗi lần lặp bound mới
        path_for_this_iteration = [start]
        result, nodes_generated = ida_star_search_recursive(path_for_this_iteration, 0, bound, goal, nodes_generated)

        if result == 'FOUND':
            # print(f"IDA* Solved! Nodes generated: {nodes_generated}")
            return path_for_this_iteration  # path_for_this_iteration đã chứa lời giải
        if result == float('inf'):  # Không tìm thấy ngưỡng tiếp theo
            # print(f"IDA* No solution (or next bound is infinity). Nodes generated: {nodes_generated}")
            return None
        bound = result  # Cập nhật bound mới
        if bound > 80:  # Giới hạn bound tối đa để tránh chạy quá lâu
            # print(f"IDA* Bound limit exceeded {bound}. Nodes: {nodes_generated}")
            return None
    # print(f"IDA* Max iterations reached. Nodes: {nodes_generated}")
    return None


# --- Hill Climbing Variants ---
def Simple_Hill_Climbing(start, goal, max_iterations=1000):
    current = start
    path = [current]
    iterations = 0

    while iterations < max_iterations:
        if current == goal: break
        iterations += 1

        current_h = Manhattan_Heuristic(current, goal)
        best_neighbor = None

        empty_x, empty_y = Find_Empty(current)
        # Tạo danh sách các nước đi ngẫu nhiên để Simple HC có tính ngẫu nhiên hơn
        shuffled_moves = list(Moves)  # Tạo bản sao
        random.shuffle(shuffled_moves)

        for dx, dy in shuffled_moves:
            new_x, new_y = empty_x + dx, empty_y + dy
            if Check(new_x, new_y):
                neighbor = Chinh_Sua_Ma_Tran(current, empty_x, empty_y, new_x, new_y)
                if Manhattan_Heuristic(neighbor, goal) < current_h:
                    best_neighbor = neighbor  # Tìm thấy một neighbor tốt hơn
                    break  # Simple HC chọn cái đầu tiên tốt hơn

        if best_neighbor is None:  # Không có neighbor nào tốt hơn
            break

        current = best_neighbor
        path.append(current)
        if current == goal: break

    return path


def Stochastic_Hill_Climbing(start, goal, max_iterations=1000):
    current = start
    path = [current]
    iterations = 0

    while iterations < max_iterations:
        if current == goal: break
        iterations += 1

        empty_x, empty_y = Find_Empty(current)
        neighbors = []
        for dx, dy in Moves:
            new_x, new_y = empty_x + dx, empty_y + dy
            if Check(new_x, new_y):
                neighbors.append(Chinh_Sua_Ma_Tran(current, empty_x, empty_y, new_x, new_y))

        if not neighbors: break

        random_neighbor = random.choice(neighbors)

        # Chỉ di chuyển nếu neighbor ngẫu nhiên tốt hơn hoặc bằng (để cho phép đi ngang)
        # Hoặc, nếu muốn nghiêm ngặt hơn, chỉ khi <
        if Manhattan_Heuristic(random_neighbor, goal) <= Manhattan_Heuristic(current, goal):
            current = random_neighbor
            path.append(current)
        # Nếu không, có thể thử lại N lần hoặc dừng nếu không có cải thiện.
        # Phiên bản đơn giản: nếu không tốt hơn, có thể bị kẹt.
        # Nếu muốn thoát local optima, cần cơ chế chấp nhận nước đi tệ hơn.
        # Ở đây, nếu random choice không tốt hơn, nó sẽ không di chuyển và có thể dừng ở vòng lặp sau nếu không có cải thiện.
        elif len(path) > 1 and current == path[-2] and iterations > max_iterations / 2:  # Nếu bị kẹt lặp lại
            break

        if current == goal: break
    return path


def Steepest_Ascent_Hill_Climbing(start, goal, max_iterations=1000):
    current = start
    path = [current]
    iterations = 0

    while iterations < max_iterations:
        if current == goal: break
        iterations += 1

        empty_x, empty_y = Find_Empty(current)
        best_neighbor = None
        min_h = Manhattan_Heuristic(current, goal)

        for dx, dy in Moves:  # Duyệt tất cả các neighbors
            new_x, new_y = empty_x + dx, empty_y + dy
            if Check(new_x, new_y):
                neighbor = Chinh_Sua_Ma_Tran(current, empty_x, empty_y, new_x, new_y)
                h_neighbor = Manhattan_Heuristic(neighbor, goal)
                if h_neighbor < min_h:
                    min_h = h_neighbor
                    best_neighbor = neighbor

        if best_neighbor is None:  # Không có neighbor nào tốt hơn
            break

        current = best_neighbor
        path.append(current)
        if current == goal: break
    return path


def Simulated_Annealing(start, goal, initial_temp=1000.0, cooling_rate=0.99, min_temp=0.1, max_iterations_per_temp=50):
    current_state = start
    current_path = [current_state]
    current_heuristic = Manhattan_Heuristic(current_state, goal)

    temp = initial_temp

    best_state_so_far = current_state
    best_heuristic_so_far = current_heuristic
    best_path_so_far = list(current_path)

    while temp > min_temp:
        if current_heuristic == 0:  # Đã đến goal
            break

        for _ in range(max_iterations_per_temp):  # Số lần thử ở mỗi nhiệt độ
            empty_x, empty_y = Find_Empty(current_state)
            possible_moves = []
            for dx, dy in Moves:
                new_x, new_y = empty_x + dx, empty_y + dy
                if Check(new_x, new_y):
                    possible_moves.append(Chinh_Sua_Ma_Tran(current_state, empty_x, empty_y, new_x, new_y))

            if not possible_moves: continue  # Bỏ qua nếu không có nước đi

            next_state = random.choice(possible_moves)
            next_heuristic = Manhattan_Heuristic(next_state, goal)

            delta_e = current_heuristic - next_heuristic  # Nếu next tốt hơn, delta_e > 0

            if delta_e > 0:  # next_state tốt hơn
                current_state = next_state
                current_heuristic = next_heuristic
                current_path.append(current_state)  # Xây dựng đường đi thực tế
                if current_heuristic < best_heuristic_so_far:
                    best_state_so_far = current_state
                    best_heuristic_so_far = current_heuristic
                    best_path_so_far = list(current_path)  # Lưu đường đi tốt nhất
            else:  # next_state tệ hơn, chấp nhận với một xác suất
                if math.exp(delta_e / temp) > random.random():
                    current_state = next_state
                    current_heuristic = next_heuristic
                    current_path.append(current_state)

            if current_heuristic == 0: break  # Đã đến goal

        temp *= cooling_rate
        if current_heuristic == 0: break

    # Trả về đường đi dẫn đến trạng thái tốt nhất tìm được (có thể là goal hoặc không)
    # Nếu muốn trả về đường đi thực tế đã đi, thì return current_path
    # Nếu muốn trả về đường đi dẫn đến trạng thái tốt nhất đã từng thấy, return best_path_so_far
    if best_heuristic_so_far == 0:  # Nếu trạng thái tốt nhất là goal
        # Cần đảm bảo best_path_so_far là đường đi đến goal.
        # Nếu current_path dẫn đến goal thì nó đã được cập nhật vào best_path_so_far.
        # Cần tinh chỉnh logic lưu path.
        # Cách đơn giản: nếu goal đạt được, thì current_path lúc đó là đường đi.
        if Manhattan_Heuristic(current_path[-1], goal) == 0:
            return current_path
        else:  # Trường hợp hiếm, best_heuristic_so_far là 0 nhưng current_path lại không
            # Điều này có nghĩa là ta đã từng ở goal, rồi lại đi ra.
            # Ta cần tìm lại đường đi đến goal trong best_path_so_far.
            # Hoặc đơn giản là chạy A* từ start đến best_state_so_far nếu nó là goal.
            # Hiện tại, sẽ trả về current_path nếu nó kết thúc ở goal, nếu không thì best_path_so_far
            # có thể không phải là đường đi trực tiếp.
            # Để đơn giản nhất, nếu best_heuristic_so_far == 0, nghĩa là ta đã tìm thấy goal
            # và current_path tại thời điểm đó nên là đường đi.
            # Logic hiện tại của current_path có thể chứa các bước đi "tệ hơn".
            # Ta nên trả về một đường đi được xây dựng lại đến best_state_so_far nếu cần.
            # Hoặc chỉ trả về best_state_so_far nếu nó là goal.
            # Với mục đích UI, nếu best_state_so_far là goal, ta trả [best_state_so_far]
            return [best_state_so_far]  # Trả về trạng thái goal như path 1 bước

    return best_path_so_far  # Trả về đường đi tốt nhất đã thấy, có thể không phải goal


def Beam_Search(Start, Goal, beam_width=3):  # Giữ nguyên, đã được sửa ở lần trước
    current_beam = PriorityQueue()
    current_beam.put((Manhattan_Heuristic(Start, Goal), Start, [Start]))
    visited_states = {tuple(map(tuple, Start))}

    while not current_beam.empty():
        next_beam_candidates = PriorityQueue()

        # Số lượng trạng thái thực tế trong beam hiện tại để mở rộng
        num_to_expand = current_beam.qsize()

        for _ in range(num_to_expand):
            if current_beam.empty(): break  # Đề phòng
            h_cost, current_state, current_path = current_beam.get()

            if current_state == Goal:
                return current_path

            empty_x, empty_y = Find_Empty(current_state)

            for dx, dy in Moves:
                nx, ny = empty_x + dx, empty_y + dy
                if Check(nx, ny):
                    new_state = Chinh_Sua_Ma_Tran(current_state, empty_x, empty_y, nx, ny)
                    new_state_tuple = tuple(map(tuple, new_state))

                    if new_state_tuple not in visited_states:
                        visited_states.add(new_state_tuple)
                        new_h_cost = Manhattan_Heuristic(new_state, Goal)
                        next_beam_candidates.put((new_h_cost, new_state, current_path + [new_state]))

        if next_beam_candidates.empty(): break

        current_beam = PriorityQueue()
        for _ in range(min(beam_width, next_beam_candidates.qsize())):
            item = next_beam_candidates.get()
            current_beam.put(item)

    return None


def flatten(board):
    return [tile for row in board for tile in row]


def unflatten(lst):
    return [lst[i:i + 3] for i in range(0, 9, 3)]


def fitness(board, goal):
    return -Manhattan_Heuristic(board, goal)


def is_solvable(tiles_list_flat_or_nested):
    if not tiles_list_flat_or_nested: return False
    if isinstance(tiles_list_flat_or_nested[0], list):
        tiles = flatten(tiles_list_flat_or_nested)
    else:
        tiles = list(tiles_list_flat_or_nested)

    tiles_for_inversion = [t for t in tiles if t != 0]
    if len(tiles_for_inversion) != 8:
        return False

    inv_count = 0
    for i in range(len(tiles_for_inversion)):
        for j in range(i + 1, len(tiles_for_inversion)):
            if tiles_for_inversion[i] > tiles_for_inversion[j]:
                inv_count += 1

    # For 3x3 grid, solvability depends only on inversion count parity
    return inv_count % 2 == 0


def generate_random_board():
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):  # is_solvable nhận list phẳng
            return unflatten(tiles)


def crossover(parent1_board, parent2_board, crossover_rate=0.8):
    if random.random() > crossover_rate:
        return copy.deepcopy(parent1_board) if random.random() < 0.5 else copy.deepcopy(parent2_board)

    p1 = flatten(parent1_board)
    p2 = flatten(parent2_board)
    size = len(p1)

    # One-point crossover for permutations (Cycle Crossover - CX is better but more complex)
    # Simpler: Order Crossover (OX1)
    child1 = [-1] * size

    # 1. Select a random subsequence from parent1
    start, end = sorted(random.sample(range(size), 2))
    subsequence = p1[start:end + 1]
    child1[start:end + 1] = subsequence

    # 2. Fill remaining positions from parent2, preserving order, avoiding duplicates
    current_p2_idx = 0
    current_child_idx = 0
    while -1 in child1:
        if current_child_idx == start:  # Skip the copied subsequence part
            current_child_idx = end + 1
            if current_child_idx >= size: break  # Reached end of child

        if child1[current_child_idx] == -1:  # If this position in child is empty
            val_from_p2 = p2[current_p2_idx]
            while val_from_p2 in subsequence:  # Ensure value from p2 is not in the copied subsequence
                current_p2_idx = (current_p2_idx + 1) % size
                val_from_p2 = p2[current_p2_idx]

            child1[current_child_idx] = val_from_p2
            current_p2_idx = (current_p2_idx + 1) % size

        current_child_idx = (current_child_idx + 1) % size
        if current_child_idx == start and start != 0:  # Wrapped around to start of subsequence
            current_child_idx = end + 1  # Jump past it

    child_board = unflatten(child1)
    if is_solvable(child_board):  # Rất quan trọng
        return child_board
    # Nếu con không giải được, trả về cha/mẹ (hoặc thử lại, hoặc một heuristic khác)
    return copy.deepcopy(parent1_board) if random.random() < 0.5 else copy.deepcopy(parent2_board)


def mutate(board, mutation_rate=0.1):
    if random.random() < mutation_rate:
        flat_board = flatten(board)
        idx1, idx2 = random.sample(range(len(flat_board)), 2)  # Swap mutation
        flat_board[idx1], flat_board[idx2] = flat_board[idx2], flat_board[idx1]
        mutated_board = unflatten(flat_board)
        if is_solvable(mutated_board):  # Đảm bảo sau đột biến vẫn giải được
            return mutated_board
    return board


def Genetic_Algorithm(start, goal, population_size=100, generations=100, mutation_rate=0.15, elitism_size=10,
                      tournament_size=5):
    print("Bắt đầu Giải thuật Di truyền...")
    population = [generate_random_board() for _ in range(population_size)]

    start_tuple = tuple(map(tuple, start))
    population_tuples = {tuple(map(tuple, ind)) for ind in population}
    if is_solvable(start) and start_tuple not in population_tuples:
        if population:
            population[0] = copy.deepcopy(start)
        else:
            population.append(copy.deepcopy(start))

    for gen in range(generations):
        population_with_fitness = []
        for individual_board in population:
            population_with_fitness.append((fitness(individual_board, goal), individual_board))

        population_with_fitness.sort(key=lambda x: x[0], reverse=True)  # Sắp xếp theo fitness giảm dần

        population = [ind[1] for ind in population_with_fitness]  # Lấy lại chỉ các board

        best_in_gen_board = population[0]
        best_in_gen_fitness = fitness(best_in_gen_board, goal)

        if gen % 10 == 0:
            print(f"Thế hệ {gen}: Fitness tốt nhất = {best_in_gen_fitness:.0f}")

        if best_in_gen_board == goal:
            print(f"Tìm thấy lời giải ở thế hệ {gen}!")
            return [best_in_gen_board]

        next_generation = []

        # Elitism
        next_generation.extend(copy.deepcopy(population[:elitism_size]))

        # Tournament Selection and Crossover
        while len(next_generation) < population_size:
            # Select parents using tournament selection
            parents = []
            for _ in range(2):  # Chọn 2 cha mẹ
                tournament = random.sample(population, tournament_size)
                tournament.sort(key=lambda b: fitness(b, goal), reverse=True)
                parents.append(tournament[0])  # Cha/mẹ là người thắng tournament

            parent1, parent2 = parents[0], parents[1]
            child = crossover(parent1, parent2)  # Crossover đã bao gồm kiểm tra is_solvable
            child = mutate(child, mutation_rate)  # Mutate đã bao gồm kiểm tra is_solvable
            next_generation.append(child)

        population = next_generation

    print("GA: Không tìm thấy lời giải sau số thế hệ tối đa.")
    final_best_board = population[0]  # Trả về cá thể tốt nhất từ thế hệ cuối
    # print(f"GA: Trạng thái tốt nhất cuối cùng (fitness {fitness(final_best_board, goal)}): {final_best_board}")
    return [final_best_board]


# --- AND-OR Search (Conceptual for 8-puzzle, not fully implemented) ---
def And_Or_Search(current_state, goal_state):
    print("And_Or_Search cho 8-puzzle là một khái niệm phức tạp để triển khai đúng nghĩa.")
    print("Nó phù hợp hơn cho các bài toán có các điều kiện AND rõ ràng để đạt được một mục tiêu con,")
    print("hoặc các game tree với các lựa chọn của người chơi (OR) và đối thủ (AND).")
    print("Đối với 8-puzzle, các thuật toán tìm kiếm trạng thái như A* thường hiệu quả hơn.")
    print("Hàm này sẽ không trả về một đường đi giải quyết.")
    # Nếu muốn thử nghiệm một cấu trúc cây AND-OR đơn giản:
    # Một OR node có thể là trạng thái hiện tại. Các nhánh OR là các nước đi có thể.
    # Một AND node là kết quả của một nước đi (trạng thái mới).
    #   Nếu trạng thái mới này là goal, thì nhánh đó thành công.
    #   Nếu không, trạng thái mới này lại trở thành một OR node.
    # Điều này nhanh chóng trở thành một dạng DFS hoặc BFS.
    # Để có AND-OR thực sự, cần có các "vấn đề con" (subproblems) mà TẤT CẢ phải được giải quyết (AND part).
    return None  # Không trả về đường đi


# --- Belief State Search ---
class BeliefState8Puzzle:  # Giữ nguyên, đã được sửa ở lần trước
    def __init__(self, possible_states_tuples):  # Luôn lưu trữ dạng tuple of tuples
        self.possible_states = set(possible_states_tuples)  # Dùng set để tự động loại bỏ trùng lặp

    def update(self, action_str, get_obs_func, actual_state_after_action_for_obs):
        new_belief_states_after_action = set()
        for state_tuple in self.possible_states:
            state_after_action = self._apply_action_to_state(state_tuple, action_str)
            if state_after_action:
                new_belief_states_after_action.add(state_after_action)

        if not new_belief_states_after_action:
            return BeliefState8Puzzle(set())

        actual_observation = get_obs_func(actual_state_after_action_for_obs)
        if actual_observation is None:  # Nếu không có observation thực tế (lỗi?)
            return BeliefState8Puzzle(new_belief_states_after_action)  # Trả về các trạng thái sau action

        final_possible_states = set()
        for s_prime_tuple in new_belief_states_after_action:
            if self._observation_matches_state(s_prime_tuple, actual_observation, get_obs_func):
                final_possible_states.add(s_prime_tuple)

        return BeliefState8Puzzle(final_possible_states)

    def _apply_action_to_state(self, state_tuple, action_str):
        # state_tuple là tuple of tuples
        state_list_of_lists = [list(row) for row in state_tuple]  # Chuyển sang list để thay đổi
        x, y = self._find_blank_in_state(state_tuple)
        if x is None: return None

        dr, dc = 0, 0
        if action_str == 'UP':
            dr = -1
        elif action_str == 'DOWN':
            dr = 1
        elif action_str == 'LEFT':
            dc = -1
        elif action_str == 'RIGHT':
            dc = 1
        else:
            return None

        new_x, new_y = x + dr, y + dc

        if Check(new_x, new_y):
            state_list_of_lists[x][y], state_list_of_lists[new_x][new_y] = state_list_of_lists[new_x][new_y], \
            state_list_of_lists[x][y]
            return tuple(map(tuple, state_list_of_lists))
        return None

    def _observation_matches_state(self, state_tuple_to_check, target_observation, get_obs_func):
        # Chuyển state_tuple_to_check (đã là tuple of tuples) sang dạng list of lists nếu get_obs_func cần
        state_list_for_obs_func = list(map(list, state_tuple_to_check))
        observation_from_state = get_obs_func(state_list_for_obs_func)
        return observation_from_state == target_observation

    def _find_blank_in_state(self, state_tuple):
        for r_idx, row in enumerate(state_tuple):
            for c_idx, val in enumerate(row):
                if val == 0:
                    return r_idx, c_idx
        return None, None

    def is_goal(self, goal_state_tuple):
        if not self.possible_states: return False
        return len(self.possible_states) == 1 and (goal_state_tuple in self.possible_states)


def get_8puzzle_observation(actual_state_list_of_list):  # Giữ nguyên
    if actual_state_list_of_list is None: return None
    blank_pos = (-1, -1);
    num1_pos = (-1, -1)
    for r, row_val in enumerate(actual_state_list_of_list):
        for c, cell_val in enumerate(row_val):
            if cell_val == 0:
                blank_pos = (r, c)
            elif cell_val == 1:
                num1_pos = (r, c)
    return (blank_pos, num1_pos)


def generate_initial_belief_states(initial_observation, all_possible_numbers=None):  # Giữ nguyên
    if all_possible_numbers is None: all_possible_numbers = list(range(9))
    (obs_blank_pos, obs_num1_pos) = initial_observation
    if obs_blank_pos == (-1, -1) or obs_num1_pos == (-1, -1) or obs_blank_pos == obs_num1_pos:
        return []
    possible_states_tuples = set()
    remaining_numbers = [n for n in all_possible_numbers if n not in [0, 1]]
    empty_cells_coords = []
    for r in range(3):
        for c in range(3):
            if (r, c) != obs_blank_pos and (r, c) != obs_num1_pos:
                empty_cells_coords.append((r, c))
    if len(remaining_numbers) != len(empty_cells_coords): return []
    from itertools import permutations
    for p_nums in permutations(remaining_numbers):
        temp_board_list = [[-1] * 3 for _ in range(3)]
        temp_board_list[obs_blank_pos[0]][obs_blank_pos[1]] = 0
        temp_board_list[obs_num1_pos[0]][obs_num1_pos[1]] = 1
        current_perm_idx = 0
        for r_coord, c_coord in empty_cells_coords:
            temp_board_list[r_coord][c_coord] = p_nums[current_perm_idx]
            current_perm_idx += 1
        possible_states_tuples.add(tuple(map(tuple, temp_board_list)))
    return list(possible_states_tuples)


def Belief_State_Search(initial_actual_state, goal_state, max_iterations=10000,
                        max_q_size=5000):  # Giữ nguyên, đã được sửa
    print("Bắt đầu Belief State Search...")
    goal_state_tuple = tuple(map(tuple, goal_state))
    initial_obs = get_8puzzle_observation(initial_actual_state)
    if initial_obs is None: return None
    initial_possible_states_tuples = generate_initial_belief_states(initial_obs)
    if not initial_possible_states_tuples: return None
    initial_belief = BeliefState8Puzzle(initial_possible_states_tuples)
    print(f"Số trạng thái trong belief state ban đầu: {len(initial_belief.possible_states)}")

    queue = deque()
    # (current_belief_state_obj, path_of_actions_list, current_simulated_actual_state_list_of_list)
    queue.append((initial_belief, [], initial_actual_state))
    visited_belief_keys = set()
    iterations = 0

    while queue:
        iterations += 1
        if iterations > max_iterations or len(queue) > max_q_size:
            print(
                f"Belief State Search: Đạt giới hạn ({'iterations' if iterations > max_iterations else 'queue size'}).")
            break

        current_belief, path_actions, current_sim_actual_state_lol = queue.popleft()

        if len(path_actions) > 30: continue  # Giới hạn độ sâu đường đi

        if current_belief.is_goal(goal_state_tuple):
            print(f"Belief state đạt goal sau {len(path_actions)} hành động!")
            # Xây dựng đường đi của các trạng thái thực tế mô phỏng
            sim_path_states_result = [initial_actual_state]
            temp_actual_state_for_path = initial_actual_state
            bs_path_helper = BeliefState8Puzzle(set())
            for act_str_for_path in path_actions:
                next_sim_state_tuple = bs_path_helper._apply_action_to_state(
                    tuple(map(tuple, temp_actual_state_for_path)), act_str_for_path)
                if next_sim_state_tuple:
                    temp_actual_state_for_path = list(map(list, next_sim_state_tuple))
                    sim_path_states_result.append(temp_actual_state_for_path)
                else:
                    break
            return sim_path_states_result

        # Key cho visited: tuple của các state_tuples đã sắp xếp trong belief
        sorted_states_in_belief_tuples = tuple(sorted(list(current_belief.possible_states)))
        if sorted_states_in_belief_tuples in visited_belief_keys:
            continue
        visited_belief_keys.add(sorted_states_in_belief_tuples)

        for action_str_loop in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            bs_action_helper = BeliefState8Puzzle(set())  # Helper để gọi _apply_action
            # 1. Mô phỏng action trên trạng thái thực tế hiện tại (đã là list of lists)
            new_sim_actual_state_tuple_after_action = bs_action_helper._apply_action_to_state(
                tuple(map(tuple, current_sim_actual_state_lol)), action_str_loop)

            if new_sim_actual_state_tuple_after_action:
                new_sim_actual_state_lol_after_action = list(map(list, new_sim_actual_state_tuple_after_action))
                # 2. Cập nhật belief state
                next_belief_obj = current_belief.update(action_str_loop, get_8puzzle_observation,
                                                        new_sim_actual_state_lol_after_action)

                if next_belief_obj.possible_states:
                    new_path_actions_list = path_actions + [action_str_loop]
                    queue.append((next_belief_obj, new_path_actions_list, new_sim_actual_state_lol_after_action))
    print("Belief State Search: Không tìm thấy giải pháp.")
    return None


# --- Backtracking Search (giữ nguyên, đã sửa ở lần trước) ---
def Backtracking_Search(start, goal, path_list=None, visited_tuples=None, max_depth=30):
    if path_list is None: path_list = []
    if visited_tuples is None: visited_tuples = set()

    current_state_tuple_for_visited = tuple(map(tuple, start))

    # Thêm vào visited *trước khi* kiểm tra goal hoặc max_depth
    # để đảm bảo nó được xóa khi backtrack từ nhánh này.
    if current_state_tuple_for_visited in visited_tuples:
        return None
    visited_tuples.add(current_state_tuple_for_visited)

    current_path_list_extended = path_list + [start]

    if start == goal:
        # Không cần xóa khỏi visited ở đây vì ta đã tìm thấy giải pháp qua nhánh này
        return current_path_list_extended

    if max_depth <= 0:
        visited_tuples.remove(current_state_tuple_for_visited)  # Xóa khi backtrack do hết độ sâu
        return None

    empty_x, empty_y = Find_Empty(start)

    for dx, dy in Moves:  # Thứ tự mặc định của Moves
        new_x, new_y = empty_x + dx, empty_y + dy
        if Check(new_x, new_y):
            new_state = Chinh_Sua_Ma_Tran(start, empty_x, empty_y, new_x, new_y)
            result = Backtracking_Search(new_state, goal, current_path_list_extended, visited_tuples, max_depth - 1)
            if result is not None:
                # Không remove current_state_tuple_for_visited nếu tìm thấy giải pháp qua nhánh này
                # vì nó là một phần của đường đi hợp lệ đã được đánh dấu.
                # Việc remove chỉ xảy ra khi một nhánh cụ thể không dẫn đến giải pháp.
                return result

    visited_tuples.remove(current_state_tuple_for_visited)  # Xóa khi backtrack từ tất cả các nhánh con của state này
    return None


# --- Q-Learning (giữ nguyên, đã sửa ở lần trước) ---
def q_study(start, goal, episodes=100, epsilon=0.1, learning_rate=0.1, discount_factor=0.9, max_steps_per_episode=200):
    print(f"Bắt đầu Q-learning với {episodes} episodes...")
    q_table = {}  # {(empty_x, empty_y): [q_up, q_down, q_left, q_right]}
    for r_init in range(3):
        for c_init in range(3):
            q_table[(r_init, c_init)] = [0.0] * len(Moves)

    for episode in range(episodes):
        current_board = copy.deepcopy(start)
        # current_path_episode = [current_board] # Không cần thiết nếu không lưu toàn bộ đường đi của episode
        is_done_episode = False

        for step_count in range(max_steps_per_episode):
            empty_x_curr, empty_y_curr = Find_Empty(current_board)
            q_state_key_curr = (empty_x_curr, empty_y_curr)

            if random.random() < epsilon:  # Explore
                action_idx_curr = random.randint(0, len(Moves) - 1)
            else:  # Exploit
                max_q_val_curr = max(q_table[q_state_key_curr])
                best_actions_indices = [i for i, q in enumerate(q_table[q_state_key_curr]) if q == max_q_val_curr]
                action_idx_curr = random.choice(best_actions_indices)

            dr_curr, dc_curr = Moves[action_idx_curr]
            next_empty_x_candidate, next_empty_y_candidate = empty_x_curr + dr_curr, empty_y_curr + dc_curr

            reward_curr = 0
            if Check(next_empty_x_candidate, next_empty_y_candidate):
                next_board_state = Chinh_Sua_Ma_Tran(current_board, empty_x_curr, empty_y_curr, next_empty_x_candidate,
                                                     next_empty_y_candidate)
                # current_path_episode.append(next_board_state)

                if next_board_state == goal:
                    reward_curr = 100
                    is_done_episode = True
                # elif tuple(map(tuple,next_board_state)) in [tuple(map(tuple,s_hist)) for s_hist in current_path_episode[:-1]]:
                #      reward_curr = -10 # Phạt lặp lại
                else:
                    reward_curr = -1  # Phạt cho mỗi bước

                q_state_key_next = (next_empty_x_candidate, next_empty_y_candidate)
                old_q_val = q_table[q_state_key_curr][action_idx_curr]

                if is_done_episode:
                    td_target_val = reward_curr
                else:
                    td_target_val = reward_curr + discount_factor * max(q_table[q_state_key_next])

                new_q_val = old_q_val + learning_rate * (td_target_val - old_q_val)
                q_table[q_state_key_curr][action_idx_curr] = new_q_val
                current_board = next_board_state
            else:  # Hành động dẫn ra ngoài biên
                reward_curr = -5
                old_q_val = q_table[q_state_key_curr][action_idx_curr]
                td_target_val = reward_curr  # Không có trạng thái tiếp theo
                new_q_val = old_q_val + learning_rate * (td_target_val - old_q_val)
                q_table[q_state_key_curr][action_idx_curr] = new_q_val
                # is_done_episode có thể True nếu muốn kết thúc episode khi cố đi ra ngoài

            if is_done_episode: break

        if episode % (episodes // 10 if episodes >= 10 else 1) == 0:
            print(f"Episode {episode}: {'Goal!' if is_done_episode else 'Max steps'}. Steps: {step_count + 1}")

    # Xây dựng đường đi tối ưu từ Q-table
    optimal_path_q = [start]
    current_board_q_optimal = copy.deepcopy(start)
    max_optimal_path_steps = 50
    for _ in range(max_optimal_path_steps):
        if current_board_q_optimal == goal: break
        empty_x_opt, empty_y_opt = Find_Empty(current_board_q_optimal)
        q_state_key_opt = (empty_x_opt, empty_y_opt)
        if q_state_key_opt not in q_table: break  # Nên có
        max_q_val_opt = max(q_table[q_state_key_opt])
        best_actions_opt_indices = [i for i, q_opt in enumerate(q_table[q_state_key_opt]) if q_opt == max_q_val_opt]
        if not best_actions_opt_indices: break
        action_idx_opt = random.choice(best_actions_opt_indices)
        dr_opt_final, dc_opt_final = Moves[action_idx_opt]
        next_empty_x_opt_final, next_empty_y_opt_final = empty_x_opt + dr_opt_final, empty_y_opt + dc_opt_final
        if Check(next_empty_x_opt_final, next_empty_y_opt_final):
            current_board_q_optimal = Chinh_Sua_Ma_Tran(current_board_q_optimal, empty_x_opt, empty_y_opt,
                                                        next_empty_x_opt_final, next_empty_y_opt_final)
            optimal_path_q.append(current_board_q_optimal)
        else:
            break

    if optimal_path_q[-1] != goal: print("Q-Learning: Không tìm thấy đường đi đến goal bằng Q-table.")
    return optimal_path_q


def Rangbuoc(state):  # Giữ nguyên
    x, y = Find_Empty(state)
    move_dict = {(0, 0): [(1, 0), (0, 1)], (0, 1): [(1, 0), (0, -1), (0, 1)], (0, 2): [(1, 0), (0, -1)],
                 (1, 0): [(-1, 0), (1, 0), (0, 1)], (1, 1): [(-1, 0), (1, 0), (0, -1), (0, 1)],
                 (1, 2): [(-1, 0), (1, 0), (0, -1)],
                 (2, 0): [(-1, 0), (0, 1)], (2, 1): [(-1, 0), (0, -1), (0, 1)], (2, 2): [(-1, 0), (0, -1)]}
    return move_dict.get((x, y), [])


def Forward_Check_Heuristic_for_FC(new_state, visited_tuples_in_current_path_fc):  # Đổi tên để tránh nhầm lẫn
    # Đây là một heuristic đơn giản, không phải Forward Checking chuẩn của CSP
    new_state_tuple = tuple(map(tuple, new_state))
    if new_state_tuple in visited_tuples_in_current_path_fc:
        return False  # Tránh lặp lại trong đường đi hiện tại

    # Kiểm tra xem từ new_state có ít nhất một nước đi hợp lệ không dẫn đến bế tắc ngay lập tức
    # (ví dụ: không quay lại trạng thái vừa rời đi mà không có lựa chọn khác)
    # Điều này có thể được làm phức tạp hơn, nhưng sẽ tăng chi phí.
    # empty_x_fc, empty_y_fc = Find_Empty(new_state)
    # possible_next_moves = Rangbuoc(new_state)
    # if not possible_next_moves: return False # Bị kẹt

    # if len(possible_next_moves) == 1:
    #     # Nếu chỉ có 1 nước đi, kiểm tra xem nó có quay lại trạng thái trước đó không
    #     # Điều này cần thông tin về trạng thái trước đó của new_state
    #     pass # Logic phức tạp hơn có thể thêm ở đây
    return True


def Forward_Checking(start_state_fc, goal_state_fc, path_taken_fc=None, visited_fc=None, max_depth_fc=30):
    # Đây là một thuật toán tìm kiếm sử dụng một heuristic "forward check" đơn giản,
    # không phải là Forward Checking chuẩn trong giải quyết CSP.
    if path_taken_fc is None: path_taken_fc = []
    if visited_fc is None: visited_fc = set()  # visited_fc để tránh lặp toàn cục (khác với path_taken)

    current_state_fc_tuple = tuple(map(tuple, start_state_fc))

    # Nếu đã mở rộng trạng thái này rồi thì không cần (giống A*, BFS...)
    # Tuy nhiên, Backtracking/DFS thường kiểm tra lặp trong đường đi hiện tại.
    # Để nhất quán với Backtracking_Search, ta có thể dùng visited_fc như một global visited set.
    # Hoặc, nếu muốn nó giống DFS thuần túy hơn (chỉ tránh lặp trong path), thì không cần global visited.
    # Giả sử visited_fc là để tránh lặp trong đường đi hiện tại cho phiên bản này.

    if current_state_fc_tuple in visited_fc:  # Nếu dùng visited_fc như global visited
        return None
    visited_fc.add(current_state_fc_tuple)

    current_path_fc_extended = path_taken_fc + [start_state_fc]

    if start_state_fc == goal_state_fc:
        return current_path_fc_extended

    if max_depth_fc <= 0:
        visited_fc.remove(current_state_fc_tuple)  # Xóa khỏi global visited khi backtrack
        return None

    empty_x_fc_main, empty_y_fc_main = Find_Empty(start_state_fc)

    # Sắp xếp các nước đi có thể giúp tìm kiếm có định hướng hơn
    # Hoặc dùng random.shuffle(Rangbuoc(start_state_fc))

    for dx_fc, dy_fc in Rangbuoc(start_state_fc):
        new_empty_x_fc, new_empty_y_fc = empty_x_fc_main + dx_fc, empty_y_fc_main + dy_fc
        # Check() đã được thực hiện ngầm trong Rangbuoc()

        new_state_fc = Chinh_Sua_Ma_Tran(start_state_fc, empty_x_fc_main, empty_y_fc_main, new_empty_x_fc,
                                         new_empty_y_fc)

        # "Forward Check" heuristic
        if Forward_Check_Heuristic_for_FC(new_state_fc, visited_fc):  # Truyền visited_fc để kiểm tra lặp
            result_fc = Forward_Checking(new_state_fc, goal_state_fc, current_path_fc_extended, visited_fc,
                                         max_depth_fc - 1)
            if result_fc is not None:
                # Không remove khỏi visited_fc ở đây vì đã tìm thấy giải pháp
                return result_fc

    visited_fc.remove(current_state_fc_tuple)  # Xóa khỏi global visited khi backtrack từ nhánh này
    return None


def DoiMotKhacNhau(board_state_dmkn):  # Giữ nguyên
    seen_values = set()
    flat_board_dmkn = flatten(board_state_dmkn)
    if len(flat_board_dmkn) != 9: return False
    for val_dmkn in flat_board_dmkn:
        if not (0 <= val_dmkn <= 8): return False
        if val_dmkn in seen_values: return False
        seen_values.add(val_dmkn)
    return len(seen_values) == 9


def GiaiDuoc(puzzle_state_gd):  # Giữ nguyên
    return is_solvable(puzzle_state_gd)


# --- AC-3 Algorithm Implementation (Đã thêm ở lần trước, giữ nguyên) ---
def get_all_arcs_for_ac3(variables_ac3, neighbors_map_ac3):
    arcs_ac3 = deque()
    for var1_ac3 in variables_ac3:
        if var1_ac3 in neighbors_map_ac3:
            for var2_ac3 in neighbors_map_ac3[var1_ac3]:
                arcs_ac3.append((var1_ac3, var2_ac3))
    return arcs_ac3


def revise_ac3(csp_ac3, X_i_ac3, X_j_ac3, constraint_func_ac3):
    revised_ac3 = False
    domain_i_copy_ac3 = list(csp_ac3['domains'][X_i_ac3])
    for x_val_ac3 in domain_i_copy_ac3:
        found_satisfying_y_ac3 = False
        for y_val_ac3 in csp_ac3['domains'][X_j_ac3]:
            if constraint_func_ac3(x_val_ac3, y_val_ac3):
                found_satisfying_y_ac3 = True
                break
        if not found_satisfying_y_ac3:
            csp_ac3['domains'][X_i_ac3].remove(x_val_ac3)
            revised_ac3 = True
            if not csp_ac3['domains'][X_i_ac3]: break
    return revised_ac3


def ac3_main_constraint_propagation(csp_ac3, constraint_func_ac3):
    queue_arcs_ac3 = get_all_arcs_for_ac3(csp_ac3['variables'], csp_ac3['neighbors'])
    while queue_arcs_ac3:
        (X_i_ac3, X_j_ac3) = queue_arcs_ac3.popleft()
        if revise_ac3(csp_ac3, X_i_ac3, X_j_ac3, constraint_func_ac3):
            if not csp_ac3['domains'][X_i_ac3]:
                return False
            for X_k_ac3 in csp_ac3['neighbors'][X_i_ac3]:
                if X_k_ac3 != X_j_ac3:
                    queue_arcs_ac3.append((X_k_ac3, X_i_ac3))
    return True


def AC3_Algorithm(board_state_ac3, goal_state_unused_ac3):
    print("Chạy AC-3 Algorithm để kiểm tra tính nhất quán all-different...")
    variables_ac3_list = []
    for r_ac3 in range(3):
        for c_ac3 in range(3):
            variables_ac3_list.append((r_ac3, c_ac3))

    domains_ac3_dict = {}
    for r_idx_ac3, row_list_ac3 in enumerate(board_state_ac3):
        for c_idx_ac3, cell_value_ac3 in enumerate(row_list_ac3):
            var_ac3 = (r_idx_ac3, c_idx_ac3)
            domains_ac3_dict[var_ac3] = [cell_value_ac3]

    neighbors_map_ac3_dict = {}
    for var1_ac3_map in variables_ac3_list:
        neighbors_map_ac3_dict[var1_ac3_map] = []
        for var2_ac3_map in variables_ac3_list:
            if var1_ac3_map != var2_ac3_map:
                neighbors_map_ac3_dict[var1_ac3_map].append(var2_ac3_map)

    csp_ac3_obj = {'variables': variables_ac3_list, 'domains': domains_ac3_dict, 'neighbors': neighbors_map_ac3_dict}

    def all_different_constraint_ac3(val1_ac3, val2_ac3):
        return val1_ac3 != val2_ac3

    is_consistent_ac3 = ac3_main_constraint_propagation(csp_ac3_obj, all_different_constraint_ac3)

    if is_consistent_ac3:
        print("AC-3: Trạng thái nhất quán (all-different).")
        return [board_state_ac3]
    else:
        print("AC-3: Trạng thái KHÔNG nhất quán (có số trùng lặp).")
        return None