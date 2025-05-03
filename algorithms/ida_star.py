# -*- coding: utf-8 -*-
# algorithms/ida_star.py
""" Thuật toán Iterative Deepening A* (IDA*) """

from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Heuristic

# --- Biến toàn cục (Không lý tưởng) ---
nodes_expanded_ida = 0

def _ida_search_recursive(node, g_cost, threshold, path, visited_in_path):
    """Hàm đệ quy cho IDA*, trả về (path_nếu_tìm_thấy, min_f_cost_vượt_ngưỡng)."""
    global nodes_expanded_ida # Sử dụng biến global của module
    nodes_expanded_ida += 1
    node_str = change_matran_string(node)
    goal_str = change_matran_string(Goal)
    if not node_str: return None, float('inf') # Trạng thái không hợp lệ

    current_path = path + [node] # Path hiện tại bao gồm node này
    h_cost = khoang_cach_mahathan(node, Goal)
    if h_cost == float('inf'): return None, float('inf') # Trạng thái không hợp lệ so với đích

    f_cost = g_cost + h_cost

    # Nếu f_cost vượt ngưỡng, cắt tỉa nhánh này và trả về chính f_cost đó
    if f_cost > threshold:
        return None, f_cost

    # Kiểm tra đích
    if node_str == goal_str:
        return current_path, f_cost # Tìm thấy Goal, trả về path và f_cost cuối cùng

    min_f_cost_above_threshold = float('inf') # Theo dõi f_cost nhỏ nhất vượt ngưỡng trong các nhánh con

    x, y = Tim_0(node)
    if x == -1: return None, float('inf') # Trạng thái không hợp lệ

    # Duyệt các hàng xóm
    for dx, dy in Moves:
        new_X, new_Y = x + dx, y + dy
        if Check(new_X, new_Y):
            neighbor_node = DiChuyen(node, x, y, new_X, new_Y)
            if neighbor_node:
                neighbor_str = change_matran_string(neighbor_node)
                # Tránh chu trình trong đường đi hiện tại (quan trọng!)
                if neighbor_str and neighbor_str not in visited_in_path:
                     # Thêm vào visited trước khi gọi đệ quy
                     visited_in_path.add(neighbor_str)
                     # Gọi đệ quy cho hàng xóm
                     result_path, new_threshold_component = _ida_search_recursive(
                         neighbor_node, g_cost + 1, threshold, current_path, visited_in_path
                     )
                     # Xóa khỏi visited sau khi quay lui (backtrack)
                     visited_in_path.remove(neighbor_str)

                     # Nếu tìm thấy Goal trong nhánh con, trả về ngay
                     if result_path is not None:
                         return result_path, threshold # threshold không đổi khi tìm thấy goal

                     # Cập nhật ngưỡng f_cost nhỏ nhất vượt quá threshold hiện tại
                     min_f_cost_above_threshold = min(min_f_cost_above_threshold, new_threshold_component)

    # Nếu không tìm thấy Goal trong nhánh này, trả về None và min_f vượt ngưỡng
    return None, min_f_cost_above_threshold

def ida_star_search(start_node, initial_threshold=None, max_threshold=100):
    """Thực hiện tìm kiếm IDA*."""
    global nodes_expanded_ida # Sử dụng biến global của module
    total_nodes_expanded = 0
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("IDA* Error: Invalid start node.")
        return []

    h_start = khoang_cach_mahathan(start_node, Goal)
    if h_start == float('inf'):
        print("IDA* Error: Start node invalid vs Goal or heuristic failed.")
        return []

    # Ngưỡng ban đầu là h(start) nếu không được cung cấp
    threshold = h_start if initial_threshold is None else initial_threshold
    print(f"Running IDA* starting with threshold={threshold}...")
    ida_step_limit = 100 # Giới hạn số lần tăng threshold để tránh vòng lặp vô hạn nếu có lỗi
    steps = 0

    while steps < ida_step_limit and threshold <= max_threshold:
        # print(f"  Trying threshold: {threshold}")
        # visited_in_path được reset cho mỗi lần lặp threshold
        # Nó chỉ theo dõi các node đã thăm trong đường đi ĐỆ QUY hiện tại để tránh vòng lặp
        visited_in_path = {start_node_str}
        nodes_expanded_ida = 0 # Reset counter cho lần lặp này
        # Bắt đầu tìm kiếm đệ quy từ start_node
        result_path, new_threshold = _ida_search_recursive(start_node, 0, threshold, [], visited_in_path)
        total_nodes_expanded += nodes_expanded_ida
        # print(f"    Expanded {nodes_expanded_ida} nodes with threshold {threshold}.")

        # Nếu tìm thấy đường đi (result_path không phải None)
        if result_path is not None:
            print(f"  Goal found with threshold {threshold}.")
            print(f"IDA*: Total expanded nodes (sum over thresholds): {total_nodes_expanded}.")
            return result_path # Trả về path (list of states)

        # Nếu không tìm thấy, cập nhật ngưỡng cho lần lặp tiếp theo
        if new_threshold == float('inf'):
            # Không có nút nào có f-cost > threshold => Đã duyệt hết không gian trạng thái?
            print("  IDA*: No solution found (explored all reachable states or heuristic inconsistent?).")
            break
        if new_threshold <= threshold:
             # Nên tăng threshold lên, ngay cả khi giá trị trả về không lớn hơn
             print(f"  Warning: New threshold {new_threshold} <= current {threshold}. Incrementing threshold.")
             threshold += 1 # Tăng ít nhất 1 để đảm bảo tiến triển
        else:
             threshold = new_threshold # Cập nhật ngưỡng bằng f-cost nhỏ nhất vượt ngưỡng cũ

        steps += 1

    # Kiểm tra lý do dừng vòng lặp
    if threshold > max_threshold:
        print(f"  IDA*: Threshold limit ({max_threshold}) reached, stopping.")
    elif steps >= ida_step_limit:
        print(f"  IDA*: Reached step limit ({ida_step_limit}) without finding solution.")

    print(f"IDA*: Total expanded nodes (sum over thresholds): {total_nodes_expanded}. Goal not found.")
    return []