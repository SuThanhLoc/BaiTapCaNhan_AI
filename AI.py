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
    # Tạo bản sao sâu của board để không thay đổi board gốc
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

        visited.add(tuple(tuple(row) for row in current))

        x, y = Find_Empty(current)

        for dx, dy in Moves:
            new_x, new_y = x + dx, y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, x, y, new_x, new_y)

                tuple_state = tuple(tuple(row) for row in new_state)

                if tuple_state not in visited:
                    new_path = path + [new_state]
                    queue.append((new_state, new_path))
                    visited.add(tuple_state)
    return None
def Uniform_Cost_Search(start, goal):
    visited = set()
    open_queue = PriorityQueue() # Đổi tên biến để tránh nhầm lẫn với hàm open() tích hợp
    # Đưa vào một tuple: (cost, state, path)
    open_queue.put((0, start, [start]))

    while not open_queue.empty(): # Kiểm tra xem hàng đợi có rỗng không
        cost, current, path = open_queue.get() # Lấy ra tuple

        # Chuyển current (list of lists) thành tuple of tuples để thêm vào visited
        current_tuple_form = tuple(tuple(row) for row in current)

        if current_tuple_form not in visited: # So sánh với dạng tuple
            visited.add(current_tuple_form)

            if current == goal:
                return path

            X, Y = Find_Empty(current)
            for dx, dy in Moves:
                new_x, new_y = X + dx, Y + dy
                if Check(new_x, new_y):
                    new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                    new_state_tuple_form = tuple(tuple(row) for row in new_state) # Chuyển sang dạng tuple

                    if new_state_tuple_form not in visited:
                        # Đưa vào một tuple: (new_cost, new_state, new_path)
                        open_queue.put((cost + 1, new_state, path + [new_state]))
    return None
def DFS(start, goal):
    visited = set()
    open = []
    open.append((start, [start]))
    while open:
        current, path = open.pop()
        if current == goal:
            return path
        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                tuple_state = tuple(tuple(row) for row in new_state)
                if tuple_state not in visited:
                    open.append((new_state, path + [new_state]))
                    visited.add(tuple_state)
    return None
def depth_bounded_search(start, goal, depth_bound, visited):
    if start == goal:
        return [start]

    if depth_bound > 0:
        X, Y = Find_Empty(start)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(start, X, Y, new_x, new_y)
                state_tuple = tuple(tuple(row) for row in new_state)
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    solution = depth_bounded_search(new_state, goal, depth_bound - 1, visited)
                    if solution is not None:
                        return [start] + solution
    return None

def Iterative_Deepening_DFS(start, goal):
    depth = 0
    while True:
        visited = set()
        solution = depth_bounded_search(start, goal, depth, visited)
        if solution is not None:
            return solution
        depth += 1
    return None
def Greedy_Search(start, goal):
    visited = set()
    open = PriorityQueue()
    open.put((Manhattan_Heuristic(start, goal), start, [start]))
    while open:
        cost, current, path = open.get()
        if str(current) not in visited:
            visited.add(tuple(tuple(row) for row in current))
            if current == goal:
                return path
            X, Y = Find_Empty(current)
            for dx, dy in Moves:
                new_x, new_y = X + dx, Y + dy
                if Check(new_x, new_y):
                    new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                    tuple_state = tuple(tuple(row) for row in new_state)
                    if tuple_state not in visited:
                        open.put((Manhattan_Heuristic(current,goal), new_state, path + [new_state]))
    return None
def A_Star_Search(start, goal):
    visited = set()
    open = PriorityQueue()
    open.put((Manhattan_Heuristic(start, goal), start, [start]))
    g = 0
    while open:
        cost, current, path = open.get()
        g += 1
        if str(current) not in visited:
            visited.add(tuple(tuple(row) for row in current))
            if current == goal:
                return path
            X, Y = Find_Empty(current)
            for dx, dy in Moves:
                new_x, new_y = X + dx, Y + dy
                if Check(new_x, new_y):
                    new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                    tuple_state = tuple(tuple(row) for row in new_state)
                    if tuple_state not in visited:
                        open.put((g+1+Manhattan_Heuristic(current,goal), new_state, path + [new_state]))
    return None
def Manhattan_Heuristic(current, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if current[i][j] != 0:
                goal_x, goal_y = Find_X(current[i][j], goal)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance
def Count_Different(current, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if current[i][j] != goal[i][j]:
                count += 1
    return count
def Find_X(x, goal):
    for i in range(3):
        for j in range(3):
            if x == goal[i][j]:
                return i, j
    return None
def IDA_limit(Start, Goal, limit):
    qp = PriorityQueue()
    qp.put( (0,0,Start,[]) )

    visited = set()

    while not qp.empty():
        f_n,chiphi,current, path = qp.get()
        if current == Goal:
            path = path + [Goal]
            return path

        x,y = Find_Empty(current)

        for dx,dy in Moves:
            new_X = x + dx
            new_Y = y + dy

            if(Check(new_X,new_Y)):
                new_matran = Chinh_Sua_Ma_Tran(current, x, y, new_X, new_Y)
                if str(new_matran) not in visited:
                    visited.add(str(new_matran))
                    f_new = chiphi + Manhattan_Heuristic(new_matran, Goal)
                    if f_new <= limit:
                        qp.put((f_new,chiphi+1,new_matran,path+[current]))
    return None

def IDA(Start,goal,limit):
    check = None
    while check == None:
        limit = limit + limit/2
        check = IDA_limit(Start, goal ,limit)
    return check
def Simple_Hill_Climbing(start, goal):
    current = start
    path = [current]

    while True:
        neighbors = []
        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                neighbors.append(new_state)

        if not neighbors:
            break

        next_state = min(neighbors, key=lambda s: Manhattan_Heuristic(s, goal))
        for i in neighbors:
            next_state = i
            if Manhattan_Heuristic(next_state, goal) <= Manhattan_Heuristic(current, goal):
                current = next_state
            else:
                break
        if Manhattan_Heuristic(next_state, goal) > Manhattan_Heuristic(current, goal):
            break

        path.append(current)

    return path
def Stochastic_Hill_Climbing(start, goal):
    current = start
    path = [current]

    while True:
        neighbors = []
        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                neighbors.append(new_state)

        if not neighbors:
            break

        next_state = random.choice(neighbors)

        if Manhattan_Heuristic(next_state, goal) >= Manhattan_Heuristic(current, goal):
            break

        current = next_state
        path.append(current)

    return path
def Steepest_Ascent_Hill_Climbing(start, goal):
    current = start
    path = [current]

    while True:
        neighbors = []
        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                neighbors.append(new_state)

        if not neighbors:
            break

        next_state = min(neighbors, key=lambda s: Manhattan_Heuristic(s, goal))

        if Manhattan_Heuristic(next_state, goal) >= Manhattan_Heuristic(current, goal):
            break

        current = next_state
        path.append(current)

    return path
def Simulated_Annealing(start, goal, temperature=1000, cooling_rate=0.99):
    current = start
    path = [current]

    while temperature > 1:
        if current == goal:
            break

        neighbors = []
        X, Y = Find_Empty(current)
        for dx, dy in Moves:
            new_x, new_y = X + dx, Y + dy
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current, X, Y, new_x, new_y)
                neighbors.append(new_state)

        if not neighbors:
            break

        next_state = random.choice(neighbors)
        current_cost = Manhattan_Heuristic(current, goal)
        next_cost = Manhattan_Heuristic(next_state, goal)

        if next_cost < current_cost:
            current = next_state
            path.append(current)
        else:
            delta = current_cost - next_cost
            acceptance_probability = math.exp(delta / temperature)
            if random.random() < acceptance_probability:
                current = next_state
                path.append(current)

        temperature *= cooling_rate

    return path
def Beam_Search(Start, Goal, beam_width=3):
    current_level = [(Start, [])]
    visited = set()

    while current_level:
        next_level_candidates = PriorityQueue()

        for state, path in current_level:
            if state == Goal:
                return path + [Goal]

            x, y = Find_Empty(state)

            for dx, dy in Moves:
                nx, ny = x + dx, y + dy
                if Check(nx, ny):
                    new_state = Chinh_Sua_Ma_Tran(state, x, y, nx, ny)
                    if str(new_state) not in visited:
                        visited.add(str(new_state))
                        next_level_candidates.put((Manhattan_Heuristic(new_state, Goal), new_state, path + [state]))

        current_level = []
        for _ in range(min(beam_width, next_level_candidates.qsize())):
            _, new_state, new_path = next_level_candidates.get()
            current_level.append((new_state, new_path))

    return []

def flatten(board):
    return [tile for row in board for tile in row]

def unflatten(lst):
    return [lst[i:i+3] for i in range(0, 9, 3)]

def fitness(board, goal):
    return -Manhattan_Heuristic(board, goal)

def generate_random_board():
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):
            return unflatten(tiles)

def is_solvable(tiles):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if tiles[i] and tiles[j] and tiles[i] > tiles[j]:
                inv_count += 1
    return inv_count % 2 == 0

def crossover(parent1, parent2):
    p1 = flatten(parent1)
    p2 = flatten(parent2)
    cut = random.randint(1, 7)
    child = p1[:cut]
    for gene in p2:
        if gene not in child:
            child.append(gene)
    return unflatten(child)

def mutate(board, mutation_rate=0.1):
    if random.random() < mutation_rate:
        flat = flatten(board)
        i, j = random.sample(range(9), 2)
        flat[i], flat[j] = flat[j], flat[i]
        if is_solvable(flat):
            return unflatten(flat)
    return board

def Genetic_Algorithm(start, goal, population_size=100, generations=500, mutation_rate=0.1):
    path = []
    print("Các giống đang có:", end='\n')
    population = [generate_random_board() for _ in range(population_size)]
    for i in population:
        print(i, end='\n')
    best = None
    for gen in range(generations):
        population.sort(key=lambda b: fitness(b, goal), reverse=True)
        if fitness(population[0], goal) == 0:
            print(f"Thế hệ giống {gen}:", end='\n')
            path.append(population[0])
            print(population[0])
            return path
        next_gen = population[:5]  # elitism
        while len(next_gen) < population_size:
            p1, p2 = random.choices(population[:5], k=2)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            next_gen.append(child)
        population = next_gen
        best = population[0]
        path.append(best)
        print(f"Thế hệ giống {gen}:", end='\n')
        print(best)
def And_Or_Search(current_state, goal_state, visited = set(), depth = 0, max_depth = 30):
    def Or_Search(current, goal):
        result = []
        X,Y = Find_Empty(current)
        for dx, dy in Moves:
            x,y = X+dx,Y+dy
            if Check(x,y):
                result_state = Chinh_Sua_Ma_Tran(current,X,Y,x,y)
                result.append(And_Search(result_state,goal_state))
        return result
    def And_Search(current, goal):
        return BFS(current,goal)
    def And_Or(start, goal):
        for i in Or_Search(start, goal):
            print(i)
            print()
    And_Or(current_state,goal_state)
def Belief_State_Search(initial_belief, goal_state):
    """
    Thuật toán tìm kiếm trong môi trường niềm tin (belief state) cho bài toán 8-puzzle
    Giả định: Chỉ quan sát được vị trí của ô trống và 1 số khác (ví dụ số 1)
    """

    visited = set()  # Lưu các belief state đã thăm
    queue = deque()
    queue.append((initial_belief, []))  # (belief state, path)

    while queue:
        current_belief, path = queue.popleft()

        # Kiểm tra nếu tất cả các trạng thái trong belief đều là goal
        if all(state == goal_state for state in current_belief.possible_states):
            return path

        # Tạo key để kiểm tra belief state đã thăm
        belief_key = frozenset(tuple(tuple(row) for row in state) for state in current_belief.possible_states)
        if belief_key in visited:
            continue
        visited.add(belief_key)

        # Thử các action có thể
        for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            # Tạo belief state mới sau action
            new_belief = current_belief.update(action, get_observation_after_action(action))

            if new_belief.possible_states:  # Nếu action hợp lệ
                queue.append((new_belief, path + [action]))

    return None  # Không tìm thấy giải pháp

class BeliefState8Puzzle:
    def __init__(self, possible_states):
        self.possible_states = possible_states  # Danh sách các trạng thái có thể

    def update(self, action, observation):
        """Cập nhật belief state sau khi thực hiện action và nhận observation"""
        new_states = []
        for state in self.possible_states:
            new_state = self.apply_action(state, action)
            if new_state and self.observation_match(new_state, observation):
                new_states.append(new_state)
        return BeliefState8Puzzle(new_states)

    def apply_action(self, state, action):
        """Áp dụng action lên một trạng thái cụ thể"""
        x, y = self.find_blank(state)
        new_state = [row[:] for row in state]

        if action == 'UP' and x > 0:
            new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
            return new_state
        elif action == 'DOWN' and x < 2:
            new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
            return new_state
        elif action == 'LEFT' and y > 0:
            new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
            return new_state
        elif action == 'RIGHT' and y < 2:
            new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
            return new_state
        return None

    def observation_match(self, state, observation):
        """Kiểm tra trạng thái có phù hợp với observation không"""
        # Giả sử observation là vị trí của số 1 và ô trống
        (obs_1_x, obs_1_y), (obs_blank_x, obs_blank_y) = observation
        state_1_pos = self.find_number(state, 1)
        state_blank_pos = self.find_blank(state)
        return state_1_pos == (obs_1_x, obs_1_y) and state_blank_pos == (obs_blank_x, obs_blank_y)

    def find_blank(self, state):
        """Tìm vị trí ô trống (0)"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def find_number(self, state, num):
        """Tìm vị trí của một số cụ thể"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == num:
                    return (i, j)
        return (-1, -1)
def get_observation_after_action(action):
    """Hàm giả lập sensor - trả về observation sau khi thực hiện action"""
    # Trong thực tế, đây sẽ là thông tin từ sensor
    # Ở đây giả sử observation là vị trí của số 1 và ô trống
    # (Cần được triển khai cụ thể tùy bài toán)
    pass

def generate_all_possible_states(observation):
    """Tạo tất cả các trạng thái có thể phù hợp với observation ban đầu"""
    # Triển khai hàm này dựa trên observation đầu vào
    pass
def Backtracking_Search(start, goal, path=[], visited=set(), max_depth=100):
    if start == goal:
        return path + [start]
    if max_depth <= 0:
        return None
    x, y = Find_Empty(start)

    for dx, dy in Moves:
        new_x, new_y = x + dx, y + dy
        if Check(new_x, new_y):
            new_state = Chinh_Sua_Ma_Tran(start, x, y, new_x, new_y)
            if str(new_state) not in visited:
                visited.add(str(new_state))
                result = Backtracking_Search(new_state, goal, path + [start], visited, max_depth - 1)
                if result is not None:
                    return result
    return None
def get_stt(x,y):
    stt = 0
    for i in range(3):
        for j in range(3):
            if i == x and j == y:
                return stt
            else:
                stt += 1
def q_study(start, goal,epsilon=0.1, episodes=1):
    path = [start]
    q_table = {}
    for i in range(3):
        for j in range(3):
            q_table[(i,j)] = [0, 0, 0, 0]
    for episode in range(episodes):
        current_state = start
        while current_state != goal:
            x, y = Find_Empty(current_state)
            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                action = q_table[(x,y)].index(max(q_table[(x,y)]))

            new_x, new_y = x + Moves[action][0], y + Moves[action][1]
            if Check(new_x, new_y):
                new_state = Chinh_Sua_Ma_Tran(current_state, x, y, new_x, new_y)
                path.append(new_state)
                reward = -1 if new_state != goal else 100
                q_table[(x,y)][action] += reward + max(q_table[(new_x,new_y)])
                current_state = new_state
                print(q_table)


    return path
def Rangbuoc(state):
    #Ràng buộc chuyển động:
    x,y = Find_Empty(state)
    move = {(0,0): [(1, 0), (0, 1)],
            (0,1): [(1, 0), (0, -1), (0, 1)],
            (0,2): [(1, 0), (0, -1)],
            (1,0): [(-1, 0), (1, 0), (0, 1)],
            (1,1): [(-1, 0), (1, 0), (0, -1), (0, 1)],
            (1,2): [(-1, 0), (1, 0), (0, -1)],
            (2,0): [(-1, 0), (0, 1)],
            (2,1): [(-1, 0), (0, -1), (0, 1)],
            (2,2): [(-1, 0), (0, -1)]
            }
    return move[(x,y)]

def Backtracking(state, goal, path = [], visited = set(), depth = 900):
    if state == goal or depth == 0:
        return path

    visited.add(tuple(map(tuple, state)))
    move = Rangbuoc(state)
    X,Y = Find_Empty(state)
    for dx, dy in move:
        new_x, new_y = X + dx, Y + dy
        new_state = Chinh_Sua_Ma_Tran(state, X, Y, new_x, new_y)

        if tuple(map(tuple, new_state)) not in visited:
            result = Backtracking(new_state, goal, path + [new_state], visited, depth - 1)
            if result:
                return result

    visited.remove(tuple(map(tuple, state)))
    return None
def Forward_Check(new_state, visited):
    # Tránh lặp trạng thái
    if tuple(map(tuple, new_state)) in visited:
        return False
    # Trạng thái mới không nên bị "kẹt", nên kiểm tra nếu có ít nhất 1 hướng di chuyển
    empty_x, empty_y = Find_Empty(new_state)
    if len(Rangbuoc(new_state)) == 1:
        return False
    return True

def Forward_Checking(state, goal, path=[], visited=set(), depth=900):
    if state == goal or depth == 0:
        return path

    visited.add(tuple(map(tuple, state)))
    move = Rangbuoc(state)
    X, Y = Find_Empty(state)

    for dx, dy in move:
        new_x, new_y = X + dx, Y + dy
        new_state = Chinh_Sua_Ma_Tran(state, X, Y, new_x, new_y)

        if Forward_Check(new_state, visited):
            result = Forward_Checking(new_state, goal, path + [new_state], visited, depth - 1)
            if result:
                return result

    visited.remove(tuple(map(tuple, state)))
def DoiMotKhacNhau(board):
    seen = set()
    for row in board:
        for val in row:
            if val in seen:
                return False
            seen.add(val)
    return True
def GiaiDuoc(puzzle):
    flat_puzzle = [num for row in puzzle for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1
    return inversions % 2 == 0
def AC3():
    boards = []
    for i in range(10000):
        nums = list(range(9))
        random.shuffle(nums)
        board_random = [nums[0:3], nums[3:6], nums[6:9]]
        boards.append(board_random)
    print(boards[-1])
    # Lộc bảng khác nhau từng đôi một và giải được
    for board in boards:
        if DoiMotKhacNhau(board) and GiaiDuoc(board):
            continue
        else:
            boards.remove(board)
    if boards == None:
        return AC3()
    else:
        return random.choice(boards)