# -*- coding: utf-8 -*-
# algorithms/genetic_algorithm.py
""" Thuật toán di truyền (Genetic Algorithm - GA) """

import random
import copy
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Fitness function

# Biến đếm số lần đánh giá fitness (có thể cần global hoặc cách khác)
nodes_evaluated_ga = 0

def genetic_algorithm_search(start_node_ignored, goal_state, population_size=100, generations=100, mutation_rate=0.1, elite_percent=0.1):
    """
    Thực hiện tìm kiếm bằng thuật toán di truyền.
    Lưu ý: GA thường không dùng trạng thái bắt đầu trực tiếp,
           mà tạo quần thể ban đầu (có thể ngẫu nhiên hoặc gần đích).
           Tham số start_node_ignored chỉ để giữ signature giống các thuật toán khác.
    """
    global nodes_evaluated_ga
    nodes_evaluated_ga = 0 # Reset counter mỗi lần chạy
    print(f"Running Genetic Algorithm (pop_size={population_size}, gens={generations}, mutation_rate={mutation_rate}, elite%={elite_percent*100})")

    # --- Hàm Fitness ---
    # Fitness càng nhỏ càng tốt (gần Goal hơn)
    def fitness(individual):
        global nodes_evaluated_ga
        nodes_evaluated_ga += 1
        # Sử dụng Manhattan distance làm độ đo fitness đảo ngược
        # Trả về giá trị heuristic, giá trị nhỏ là tốt
        return khoang_cach_mahathan(individual, goal_state)

    # --- Hàm Crossover (Lai ghép) ---
    # Sử dụng Partially Mapped Crossover (PMX) là một lựa chọn phổ biến cho permutation
    def crossover_pmx(parent1_list, parent2_list):
        size = len(parent1_list)
        child1_list, child2_list = [-1] * size, [-1] * size
        # Chọn 2 điểm cắt ngẫu nhiên
        cut1, cut2 = random.sample(range(size + 1), 2) # Sample từ 0 đến size
        start, end = min(cut1, cut2), max(cut1, cut2)

        # Sao chép đoạn giữa từ cha mẹ tương ứng
        mapping1, mapping2 = {}, {}
        for i in range(start, end):
            gene1 = parent1_list[i]
            gene2 = parent2_list[i]
            child1_list[i] = gene2
            child2_list[i] = gene1
            # Lưu lại ánh xạ để xử lý xung đột
            mapping1[gene2] = gene1
            mapping2[gene1] = gene2

        # Điền các phần còn lại
        for i in list(range(start)) + list(range(end, size)):
            # Child 1
            gene_p1 = parent1_list[i]
            while gene_p1 in mapping1: # Nếu gene từ parent1 đã có trong đoạn giữa của child1 (do lấy từ p2)
                gene_p1 = mapping1[gene_p1] # Tìm gene tương ứng từ parent1 mà parent2 map tới
            child1_list[i] = gene_p1

            # Child 2
            gene_p2 = parent2_list[i]
            while gene_p2 in mapping2:
                gene_p2 = mapping2[gene_p2]
            child2_list[i] = gene_p2

        return child1_list, child2_list

    # --- Hàm Mutation (Đột biến) ---
    # Đột biến bằng cách swap 2 ô ngẫu nhiên (không nhất thiết là ô trống)
    def mutate_swap(individual_list):
         size = len(individual_list)
         idx1, idx2 = random.sample(range(size), 2)
         # Swap giá trị tại 2 vị trí ngẫu nhiên
         individual_list[idx1], individual_list[idx2] = individual_list[idx2], individual_list[idx1]
         return individual_list

    # --- Helper: Chuyển list 1D thành ma trận 3x3 ---
    def reshape_to_matrix(flat_list):
        if len(flat_list) != 9: return None
        return [flat_list[i*3:(i+1)*3] for i in range(3)]

    # --- Helper: Chuyển ma trận 3x3 thành list 1D ---
    def flatten_matrix(matrix):
         if not matrix or len(matrix)!=3: return None
         return [num for row in matrix for num in row]

    # --- Khởi tạo quần thể ---
    print("  Initializing population...")
    population_matrices = [] # List các ma trận 3x3
    visited_init_strings = set()
    max_init_attempts = population_size * 10 # Tăng giới hạn thử
    attempts = 0
    goal_flat = flatten_matrix(goal_state)
    if not goal_flat: print("GA Error: Cannot flatten goal state."); return []

    # Thêm trạng thái đích vào quần thể ban đầu
    population_matrices.append(copy.deepcopy(goal_state))
    visited_init_strings.add(change_matran_string(goal_state))
    nodes_evaluated_ga += 1 # Đếm cả Goal state

    # Tạo các cá thể còn lại bằng cách đi lùi ngẫu nhiên từ Goal
    while len(population_matrices) < population_size and attempts < max_init_attempts:
        attempts += 1
        current = copy.deepcopy(goal_state)
        steps = random.randint(20, 60) # Số bước đi lùi ngẫu nhiên
        for _ in range(steps):
            x, y = Tim_0(current)
            if x == -1: current = copy.deepcopy(goal_state); break # Lỗi thì reset về Goal

            possible_moves_coords = []
            for dx, dy in Moves:
                nx, ny = x + dx, y + dy
                if Check(nx, ny): possible_moves_coords.append((nx, ny))

            if not possible_moves_coords: break
            nx, ny = random.choice(possible_moves_coords)
            next_state = DiChuyen(current, x, y, nx, ny)
            if next_state is None: current = copy.deepcopy(goal_state); break
            current = next_state

        current_str = change_matran_string(current)
        if current_str and current_str not in visited_init_strings:
            population_matrices.append(current)
            visited_init_strings.add(current_str)
            nodes_evaluated_ga += 1 # Đếm các state khởi tạo

    if len(population_matrices) < population_size // 2: # Cần ít nhất 1 nửa quần thể
         print(f"Error: Failed to initialize sufficient population ({len(population_matrices)}/{population_size}).")
         return []
    elif len(population_matrices) < population_size:
         print(f"Warning: Could only initialize {len(population_matrices)} unique states.")
         # Có thể bổ sung bằng các cá thể ngẫu nhiên hoàn toàn nếu cần

    # --- Vòng lặp Tiến hóa ---
    best_overall_individual = None
    best_overall_fitness = float('inf')

    for generation in range(generations):
        # 1. Đánh giá Fitness và Sắp xếp
        # Tính fitness cho từng cá thể (ma trận) trong quần thể
        pop_with_fitness = [(matrix, fitness(matrix)) for matrix in population_matrices]
        # Sắp xếp theo fitness (thấp tốt hơn)
        pop_with_fitness.sort(key=lambda item: item[1])

        current_best_fitness = pop_with_fitness[0][1]

        # 2. Kiểm tra điều kiện dừng (tìm thấy Goal)
        if current_best_fitness == 0:
            print(f"  Goal found in generation {generation+1}. Total states evaluated (approx): {nodes_evaluated_ga}.")
            # Trả về Goal state trong list để thống nhất format
            return [pop_with_fitness[0][0]] # Trả về ma trận Goal

        # 3. Cập nhật cá thể tốt nhất toàn cục
        if current_best_fitness < best_overall_fitness:
            best_overall_fitness = current_best_fitness
            # Lưu bản sao của ma trận tốt nhất
            best_overall_individual = copy.deepcopy(pop_with_fitness[0][0])

        # 4. Chọn lọc (Selection)
        next_generation_matrices = []

        # Elitism: Giữ lại % cá thể tốt nhất
        elite_count = max(1, int(population_size * elite_percent))
        elites = [item[0] for item in pop_with_fitness[:elite_count]]
        next_generation_matrices.extend(copy.deepcopy(e) for e in elites) # Thêm bản sao vào thế hệ mới

        # Tournament Selection (hoặc phương pháp khác như Roulette Wheel) để chọn cha mẹ
        def tournament_selection(population_fitness_list, k=3):
             # Chọn k cá thể ngẫu nhiên
             tournament_contenders = random.sample(population_fitness_list, k)
             # Trả về cá thể có fitness tốt nhất (nhỏ nhất) trong nhóm đó
             winner = min(tournament_contenders, key=lambda item: item[1])
             return winner[0] # Trả về ma trận của cá thể thắng

        # 5. Lai ghép (Crossover) và Đột biến (Mutation)
        while len(next_generation_matrices) < population_size:
            # Chọn cha mẹ bằng Tournament Selection
            parent1_matrix = tournament_selection(pop_with_fitness)
            parent2_matrix = tournament_selection(pop_with_fitness)

            # Chuyển sang list 1D để lai ghép
            parent1_flat = flatten_matrix(parent1_matrix)
            parent2_flat = flatten_matrix(parent2_matrix)

            if parent1_flat and parent2_flat:
                 # Thực hiện lai ghép PMX
                 child1_flat, child2_flat = crossover_pmx(parent1_flat, parent2_flat)

                 # Áp dụng đột biến cho con cái với xác suất mutation_rate
                 if random.random() < mutation_rate:
                      child1_flat = mutate_swap(child1_flat)
                 if random.random() < mutation_rate:
                      child2_flat = mutate_swap(child2_flat)

                 # Chuyển lại thành ma trận và thêm vào thế hệ mới nếu hợp lệ
                 child1_matrix = reshape_to_matrix(child1_flat)
                 if child1_matrix and len(next_generation_matrices) < population_size:
                      next_generation_matrices.append(child1_matrix)

                 child2_matrix = reshape_to_matrix(child2_flat)
                 if child2_matrix and len(next_generation_matrices) < population_size:
                      next_generation_matrices.append(child2_matrix)
            else:
                 # Nếu flatten lỗi, có thể thêm lại elite hoặc parent để đủ quần thể
                 if len(next_generation_matrices) < population_size:
                      next_generation_matrices.append(copy.deepcopy(elites[0]))


        # Cập nhật quần thể cho thế hệ tiếp theo
        population_matrices = next_generation_matrices

        # In tiến độ (tùy chọn)
        # if (generation + 1) % 20 == 0:
        #      print(f"  Generation {generation+1}/{generations}, Best Fitness: {best_overall_fitness}")


    # --- Kết thúc GA ---
    print(f"  Genetic Algorithm finished after {generations} generations without finding exact goal.")
    print(f"  Best fitness found: {best_overall_fitness}. Total states evaluated (approx): {nodes_evaluated_ga}.")
    # Trả về cá thể tốt nhất tìm được (dù không phải goal) hay list rỗng?
    # Trả về list rỗng để báo hiệu không đạt được Goal state.
    # print("Best individual found:")
    # if best_overall_individual: print_matrix(best_overall_individual)
    return []