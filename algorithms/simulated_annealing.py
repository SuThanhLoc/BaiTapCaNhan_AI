# -*- coding: utf-8 -*-
# algorithms/simulated_annealing.py
""" Thuật toán Simulated Annealing (SA) """

import random
import math
import copy
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Heuristic

def simulated_annealing_search(start_node, initial_temp=100.0, cooling_rate=0.95, min_temp=0.1, max_iterations=10000, goal_state=Goal):
    """Thực hiện tìm kiếm Simulated Annealing."""
    print(f"Running Simulated Annealing (T_init={initial_temp}, alpha={cooling_rate}, T_min={min_temp}, max_iter={max_iterations})")
    current_state = start_node
    current_h = khoang_cach_mahathan(current_state, goal_state)
    if current_h == float('inf'):
        print("SA Error: Invalid start state or heuristic failed.")
        return []

    T = initial_temp
    iterations = 0
    nodes_evaluated = 1 # Đếm cả state ban đầu
    path = [current_state] # Theo dõi chuỗi các trạng thái ĐÃ CHẤP NHẬN

    # Theo dõi trạng thái tốt nhất toàn cục (có h nhỏ nhất) đã gặp
    best_state_so_far = copy.deepcopy(current_state)
    best_h_so_far = current_h

    goal_str = change_matran_string(goal_state)

    while T > min_temp and iterations < max_iterations:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SA Error: Invalid current state during run."); return []

        # Kiểm tra nếu trạng thái hiện tại là đích (có thể xảy ra nếu may mắn)
        if current_state_str == goal_str:
            print(f"  Goal found after {iterations} iterations (T={T:.2f}). Evaluated {nodes_evaluated} states.")
            return path # Trả về path dẫn đến goal

        x, y = Tim_0(current_state)
        if x == -1: print("  Error: Cannot find blank tile in SA."); return []

        # --- Chọn hàng xóm ngẫu nhiên ---
        possible_moves_coords = [] # List các tọa độ MỚI của ô trống
        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                possible_moves_coords.append((new_X, new_Y))

        if not possible_moves_coords:
            # print("  SA: No possible moves from current state.")
            break # Dừng nếu không có nước đi nào

        # Chọn ngẫu nhiên một vị trí mới cho ô trống từ các vị trí hợp lệ
        chosen_new_blank_pos = random.choice(possible_moves_coords)
        # Tạo trạng thái hàng xóm bằng cách di chuyển ô trống đến vị trí mới
        next_state = DiChuyen(current_state, x, y, chosen_new_blank_pos[0], chosen_new_blank_pos[1])

        if next_state:
            nodes_evaluated += 1
            next_h = khoang_cach_mahathan(next_state, goal_state)

            # Chỉ xem xét nếu hàng xóm hợp lệ
            if next_h != float('inf'):
                # Cập nhật trạng thái tốt nhất toàn cục nếu cần
                if next_h < best_h_so_far:
                    best_h_so_far = next_h
                    best_state_so_far = copy.deepcopy(next_state) # Lưu lại bản sao

                # --- Quyết định chấp nhận nước đi ---
                delta_e = next_h - current_h # Thay đổi "năng lượng" (heuristic)
                accept = False
                if delta_e < 0: # Luôn chấp nhận nước đi tốt hơn
                    accept = True
                else:
                    # Chấp nhận nước đi tệ hơn với xác suất P = exp(-delta_e / T)
                    # Kiểm tra T > epsilon nhỏ để tránh chia cho 0
                    if T > 1e-9:
                        probability = math.exp(-delta_e / T)
                        if random.random() < probability:
                            accept = True

                if accept:
                    current_state = next_state
                    current_h = next_h
                    path.append(current_state) # Chỉ thêm trạng thái ĐÃ CHẤP NHẬN vào path

        # Giảm nhiệt độ
        T *= cooling_rate
        iterations += 1

    # --- Kết thúc vòng lặp ---
    # Kiểm tra lần cuối xem trạng thái hiện tại hoặc trạng thái tốt nhất có phải là Goal không
    final_state_str = change_matran_string(current_state)
    best_state_str = change_matran_string(best_state_so_far)

    if final_state_str == goal_str:
        print(f"  Goal found at the end (Iter {iterations}, T={T:.2f}). Evaluated {nodes_evaluated} states.")
        return path # Path dẫn đến goal
    elif best_state_str == goal_str:
        print(f"  Goal state was visited (best state) but algorithm ended elsewhere.")
        print(f"  Reporting Goal Found. Total states evaluated: {nodes_evaluated}.")
        # Khó trả về path chính xác đến best_state trừ khi lưu trữ đặc biệt.
        # Trả về [goal_state] để báo hiệu thành công như các local search khác.
        return [goal_state]
    else:
        reason = f"Reached max iterations ({iterations})" if iterations >= max_iterations else f"Temperature dropped below minimum ({T:.2f})"
        print(f"  Simulated Annealing finished without finding goal ({reason}). Evaluated {nodes_evaluated} states.")
        print(f"  Ended at state with h={current_h}. Best state found had h={best_h_so_far}.")
        # Trả về path các trạng thái đã chấp nhận, dù không phải goal
        return path