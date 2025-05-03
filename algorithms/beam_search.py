# -*- coding: utf-8 -*-
# algorithms/beam_search.py
""" Thuật toán Beam Search """

import heapq # Có thể dùng heapq để chọn top K hiệu quả hơn sort
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Heuristic

def beam_search(start_node, beam_width, max_iterations=1000, goal_state=Goal):
    """Thực hiện tìm kiếm Beam Search."""
    print(f"Running Beam Search (beam_width={beam_width}, max_iter={max_iterations})")
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("Beam Search Error: Invalid start node.")
        return []

    h_start = khoang_cach_mahathan(start_node, goal_state)
    if h_start == float('inf'):
        print("Beam Search Error: Start node invalid vs Goal or heuristic failed.")
        return []

    goal_str = change_matran_string(goal_state)

    # Beam lưu các tuple: (heuristic_cost, state, path_list_of_states)
    # Khởi tạo beam ban đầu chỉ chứa trạng thái bắt đầu
    # Dùng list thay vì heap ở đây cho đơn giản, nhưng heap sẽ tối ưu hơn
    beam = [(h_start, start_node, [start_node])]
    # Visited để tránh duyệt lại cùng một trạng thái vật lý qua các vòng lặp beam
    visited = {start_node_str}
    iterations = 0
    total_nodes_evaluated = 1 # Đếm state ban đầu

    while iterations < max_iterations and beam:
        candidates = [] # List các ứng viên cho beam tiếp theo (từ tất cả các state trong beam hiện tại)
        all_neighbors_generated = 0 # Đếm số neighbor được tạo ra ở mỗi iteration

        # Kiểm tra goal trong beam hiện tại trước khi mở rộng
        for h, current_state, path in beam:
             current_state_str = change_matran_string(current_state)
             if current_state_str == goal_str:
                  print(f"  Goal found within beam after {iterations} iterations. Total evaluated states (approx): {total_nodes_evaluated}.")
                  return path # Trả về path dẫn đến goal

        # Tạo tất cả các trạng thái kế tiếp từ các trạng thái trong beam hiện tại
        for h, current_state, path in beam:
             # Bỏ qua nếu đã tìm thấy goal ở trên (không cần thiết lắm)
             current_state_str = change_matran_string(current_state)
             if current_state_str == goal_str: continue

             x, y = Tim_0(current_state)
             if x == -1: continue # Bỏ qua state không hợp lệ trong beam

             # Sinh các trạng thái hàng xóm
             for dx, dy in Moves:
                 new_X, new_Y = x + dx, y + dy
                 if Check(new_X, new_Y):
                     neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                     if neighbor_state:
                         all_neighbors_generated += 1
                         neighbor_str = change_matran_string(neighbor_state)
                         # Chỉ thêm vào candidates nếu hợp lệ và chưa từng được visit tổng thể
                         if neighbor_str and neighbor_str not in visited:
                              visited.add(neighbor_str) # Đánh dấu visited toàn cục
                              total_nodes_evaluated += 1
                              h_neighbor = khoang_cach_mahathan(neighbor_state, goal_state)
                              if h_neighbor != float('inf'):
                                  # Thêm (heuristic, state, path_mới) vào candidates
                                  candidates.append((h_neighbor, neighbor_state, path + [neighbor_state]))

        # Nếu không sinh ra được ứng viên hợp lệ nào, dừng lại
        if not candidates:
            print(f"  Beam Search stopped after {iterations} iterations: No new valid candidates generated.")
            break

        # --- Chọn lọc beam tiếp theo ---
        # Sắp xếp các ứng viên theo heuristic (tốt nhất trước)
        # Dùng heapq.nsmallest hiệu quả hơn sort() rồi cắt list
        # beam = sorted(candidates, key=lambda item: item[0])[:beam_width]
        beam = heapq.nsmallest(beam_width, candidates, key=lambda item: item[0])

        # print(f"Iter {iterations+1}: Generated {all_neighbors_generated} neighbors, Kept {len(beam)} in beam.") # Debug
        iterations += 1

        # Nếu beam rỗng sau khi chọn lọc, dừng lại
        if not beam:
             print(f"  Beam became empty after selection at iteration {iterations}.")
             break

    # --- Kết thúc vòng lặp ---
    # Kiểm tra lần cuối trong beam cuối cùng
    for h, state, path in beam:
        state_str = change_matran_string(state)
        if state_str == goal_str:
            print(f"  Goal found in the final beam after {iterations} iterations. Total evaluated states (approx): {total_nodes_evaluated}.")
            return path

    # Báo cáo thất bại
    reason = f"Reached max iterations ({iterations})" if iterations >= max_iterations else "Beam became empty"
    print(f"  Beam Search finished without finding goal ({reason}). Total evaluated states (approx): {total_nodes_evaluated}.")
    # Trả về path tốt nhất trong beam cuối cùng? Hay list rỗng?
    # Thống nhất trả về list rỗng nếu không tìm thấy Goal state.
    return []