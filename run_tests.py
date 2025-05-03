# -*- coding: utf-8 -*-
# run_tests.py
"""
Script để chạy thử nghiệm các thuật toán trên dòng lệnh.
(Tách ra từ khối if __name__ == '__main__' của file ThuatToan.py gốc)
"""
import time
import copy

# Import các thành phần cần thiết từ cấu trúc mới
try:
    from puzzle.state import Start, Goal, print_matrix, change_matran_string
    # Import tất cả các hàm thuật toán đã được tách ra
    from algorithms.bfs import bfs_search
    from algorithms.dfs import dfs_search
    from algorithms.ucs import ucs_search
    from algorithms.iddfs import iddfs_search # Cần import cả biến global nếu giữ nguyên
    from algorithms.greedy import greedy_search
    from algorithms.a_star import a_star_search
    from algorithms.ida_star import ida_star_search # Cần import cả biến global nếu giữ nguyên
    from algorithms.hill_climbing import (simple_hill_climbing_first_choice,
                                         steepest_ascent_hill_climbing,
                                         stochastic_hill_climbing)
    from algorithms.simulated_annealing import simulated_annealing_search
    from algorithms.beam_search import beam_search
    from algorithms.genetic_algorithm import genetic_algorithm_search
    from algorithms.conformant_bfs import conformant_bfs_search
    print("Imports for run_tests.py successful.")
except ImportError as e:
    print("-----------------------------------------------------")
    print(f"LỖI IMPORT trong run_tests.py: {e}")
    print("Không thể chạy thử nghiệm thuật toán.")
    print("Hãy kiểm tra lại cấu trúc thư mục và các file thuật toán.")
    print("-----------------------------------------------------")
    exit() # Thoát nếu không import được

# --- Phần chạy thử nghiệm ---
if __name__ == "__main__":
    print("="*30); print("Running run_tests.py script"); print("Trạng thái bắt đầu (Start):"); print_matrix(Start)
    print("\nTrạng thái đích (Goal):"); print_matrix(Goal); print("="*30 + "\n")

    # --- Reset global counters nếu cần ---
    # Việc sử dụng global trong các module riêng lẻ không được khuyến khích.
    # Cách tốt hơn là để hàm thuật toán trả về số node đã duyệt.
    # Tạm thời giữ lại nếu logic gốc dùng global, nhưng cần refactor sau.
    try:
        # Cần import các biến global này nếu module thuật toán định nghĩa chúng
        # Ví dụ, trong algorithms/iddfs.py, bạn phải có dòng:
        # nodes_expanded_iddfs = 0
        # Để lệnh import dưới đây hoạt động. Điều này khá rắc rối.
        # from algorithms.iddfs import nodes_expanded_iddfs # Thử import
        # from algorithms.ida_star import nodes_expanded_ida # Thử import
        pass # Bỏ qua việc reset global ở đây, vì nó không đáng tin cậy
    except ImportError:
         print("Warning: Could not import global node counters from algorithm modules.")
         pass


    # Define algorithms to test (ánh xạ tên -> hàm)
    # Sử dụng các hàm đã import
    algorithms_to_test = {
        "BFS": bfs_search,
        "UCS": ucs_search,
        "DFS (Depth=50)": lambda s: dfs_search(s, max_depth=50), # DFS gốc có giới hạn
        "IDDFS (Depth=25)": lambda s: iddfs_search(s, max_depth=25), # Limit depth
        "Greedy": greedy_search,
        "A*": a_star_search,
        "IDA* (Thresh=80)": lambda s: ida_star_search(s, max_threshold=80), # Limit threshold
        "Simple HC (First Choice)": lambda s: simple_hill_climbing_first_choice(s, max_steps=2000),
        "Steepest Ascent HC": lambda s: steepest_ascent_hill_climbing(s, max_steps=2000),
        "Stochastic HC": lambda s: stochastic_hill_climbing(s, max_steps=2000),
        "Simulated Annealing": lambda s: simulated_annealing_search(s, initial_temp=50, cooling_rate=0.98, min_temp=0.01, max_iterations=15000),
        "Beam Search (k=5)": lambda s: beam_search(s, beam_width=5, max_iterations=1000),
        #"Beam Search (k=20)": lambda s: beam_search(s, beam_width=20, max_iterations=1000), # Test thêm k lớn hơn
        "Genetic Algorithm": lambda s: genetic_algorithm_search(s, Goal, population_size=100, generations=200, mutation_rate=0.2),
        # Conformant BFS cần input là list of states
        # "Conformant BFS": lambda belief_list: conformant_bfs_search(belief_list, Goal)
    }

    # --- Run Standard Tests ---
    results = {}
    print("\n--- Running Standard Algorithm Tests (Non-Conformant) ---")
    for name, func in algorithms_to_test.items():
        # Bỏ qua Conformant BFS trong vòng lặp này
        if name == "Conformant BFS": continue

        print(f"\n--- Testing {name} ---")
        start_time = time.time()
        # Luôn truyền bản sao của Start để tránh bị thay đổi
        start_state_copy = copy.deepcopy(Start)

        try:
             # Gọi hàm thuật toán
             result = func(start_state_copy) # Algs chuẩn nhận 1 start state
        except Exception as e:
             print(f"!!! EXCEPTION during {name} execution: {e}")
             import traceback
             traceback.print_exc()
             result = "EXECUTION ERROR" # Đánh dấu lỗi

        end_time = time.time()
        elapsed = end_time - start_time

        # Phân tích kết quả trả về
        if isinstance(result, str) and "ERROR" in result:
            print(f"{name} failed with an execution error in {elapsed:.4f}s")
            results[name] = ("Exec Error", elapsed)
        elif result: # Nếu có kết quả (không phải None, không phải list rỗng)
            # Kiểm tra nếu là path (list các state)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0 and isinstance(result[0][0], list):
                 path_len = len(result) # Số state trong path
                 print(f"{name} found path length: {path_len} states ({max(0, path_len-1)} moves) in {elapsed:.4f}s")
                 # Optional: Kiểm tra state cuối có phải Goal không
                 final_state_str = change_matran_string(result[-1])
                 goal_state_str = change_matran_string(Goal)
                 # if final_state_str == goal_state_str: print("  Path ends at Goal.")
                 # else: print(f"  Warning: Path does not end at Goal state! Ends at:\n{result[-1]}")
                 results[name] = (path_len, elapsed)
            # Kiểm tra nếu là [Goal] trả về từ GA/Local Search
            elif isinstance(result, list) and len(result) == 1:
                 goal_state_str = change_matran_string(Goal)
                 res_state_str = change_matran_string(result[0])
                 if res_state_str == goal_state_str:
                      print(f"{name} found the goal state in {elapsed:.4f}s")
                      results[name] = ("Goal Found", elapsed)
                 else:
                      print(f"{name} returned a single state path, but not Goal, in {elapsed:.4f}s")
                      results[name] = ("Non-Goal Path", elapsed)

            else: # Format kết quả không xác định
                 print(f"{name} returned an unexpected result format in {elapsed:.4f}s: {type(result)}")
                 results[name] = ("Unknown Format", elapsed)
        else: # Kết quả là [] hoặc None -> Không tìm thấy
             print(f"{name} did not find the goal in {elapsed:.4f}s")
             results[name] = (None, elapsed) # Dùng None cho path length nếu không tìm thấy

        print("-"*(len(name) + 12))


    # --- Run Conformant BFS Test Separately ---
    print("\n--- Running Conformant BFS Test ---")
    # Define an example initial belief state (list of states)
    initial_belief_state = [
        [[2, 6, 5], [0, 8, 7], [4, 3, 1]], # The original Start state
        [[2, 6, 5], [8, 0, 7], [4, 3, 1]], # Blank swapped with 8
        [[2, 0, 5], [6, 8, 7], [4, 3, 1]]  # Blank swapped with 6
    ]
    print("Initial Belief State:")
    for i, state in enumerate(initial_belief_state): print(f" State {i+1}:"); print_matrix(state)

    start_time = time.time()
    conf_bfs_result_path_names = None
    try:
        # Gọi hàm conformant BFS
        conf_bfs_result_path_names = conformant_bfs_search(initial_belief_state, Goal)
    except Exception as e:
         print(f"!!! EXCEPTION during Conformant BFS execution: {e}")
         import traceback
         traceback.print_exc()
         conf_bfs_result_path_names = "EXECUTION ERROR"

    end_time = time.time()
    elapsed = end_time - start_time

    if isinstance(conf_bfs_result_path_names, str) and "ERROR" in conf_bfs_result_path_names:
         print(f"Conformant BFS failed with an execution error in {elapsed:.4f}s")
         results["Conformant BFS"] = ("Exec Error", elapsed)
    elif conf_bfs_result_path_names is not None: # Trả về list tên nước đi
        path_len = len(conf_bfs_result_path_names)
        print(f"Conformant BFS found path length: {path_len} moves in {elapsed:.4f}s")
        print(f"  Path (Move Names): {conf_bfs_result_path_names}")
        results["Conformant BFS"] = (path_len, elapsed)
    else: # Trả về None -> Không tìm thấy
        print(f"Conformant BFS did not find the goal in {elapsed:.4f}s")
        results["Conformant BFS"] = (None, elapsed)
    print("---------------------------------")


    # --- Print Summary ---
    print("\n" + "="*30); print("Summary of Test Results:"); print("-" * 30)
    for name, data in results.items():
         res, duration = data # Unpack tuple
         if res == "Exec Error":
              print(f"{name:<25}: EXECUTION ERROR{'':<11}, Time = {duration:.4f}s")
         elif res is not None:
             if isinstance(res, int): # Path length (states or moves)
                if name == "Conformant BFS":
                     print(f"{name:<25}: Path Length = {res:<5} moves, Time = {duration:.4f}s")
                else: # Standard algs return num states
                     print(f"{name:<25}: Path Length = {res:<5} states ({max(0, res-1)} moves), Time = {duration:.4f}s")
             elif res == "Goal Found": # GA/Local Search thành công
                 print(f"{name:<25}: Goal Found{'':<16}, Time = {duration:.4f}s")
             elif res == "Non-Goal Path":
                 print(f"{name:<25}: Non-Goal Path{'':<12}, Time = {duration:.4f}s")
             else: # Unknown Format
                 print(f"{name:<25}: Unknown Result{'':<12}, Time = {duration:.4f}s")
         else: # Goal not found (result is None)
             print(f"{name:<25}: Goal Not Found{'':<16}, Time = {duration:.4f}s")
    print("="*30)