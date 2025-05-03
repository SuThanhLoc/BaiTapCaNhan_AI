# -*- coding: utf-8 -*-
# algorithms/iddfs.py
""" Thuật toán Iterative Deepening Depth-First Search (IDDFS) """

from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string

# --- Biến toàn cục (Không lý tưởng, nên được trả về hoặc dùng class) ---
# Khai báo biến global ở cấp module để hàm đệ quy có thể truy cập
nodes_expanded_dls = 0

def _dfs_limited_recursive(current_node, limit, path, visited):
    """Hàm đệ quy cho DLS (Depth Limited Search)."""
    global nodes_expanded_dls # Sử dụng biến global của module này
    nodes_expanded_dls += 1
    current_node_str = change_matran_string(current_node)
    goal_str = change_matran_string(Goal)
    if not current_node_str: return None # Trạng thái không hợp lệ

    # Tạo path mới bao gồm trạng thái hiện tại
    current_path = path + [current_node]

    # Kiểm tra đích
    if current_node_str == goal_str: return current_path
    # Kiểm tra giới hạn độ sâu
    if limit <= 0: return None

    x, y = Tim_0(current_node)
    if x == -1: return None # Trạng thái không hợp lệ

    # Duyệt các hàng xóm
    for dx, dy in Moves: # Thứ tự duyệt có thể ảnh hưởng kết quả nhưng không ảnh hưởng tính đúng đắn
        new_X, new_Y = x + dx, y + dy
        if Check(new_X, new_Y):
            neighbor_node = DiChuyen(current_node, x, y, new_X, new_Y)
            if neighbor_node:
                 neighbor_node_str = change_matran_string(neighbor_node)
                 # Chỉ gọi đệ quy nếu hàng xóm hợp lệ và chưa được thăm trong lần DLS này
                 if neighbor_node_str and neighbor_node_str not in visited:
                      visited.add(neighbor_node_str) # Đánh dấu đã thăm trong lần lặp DLS này
                      result = _dfs_limited_recursive(neighbor_node, limit - 1, current_path, visited)
                      if result is not None: return result # Tìm thấy Goal, trả về ngay
                      # Backtrack: visited sẽ được reset ở vòng lặp ngoài của IDDFS
                      # Không cần remove ở đây trừ khi muốn visited dùng chung mọi độ sâu (không đúng với IDDFS)
                      # visited.remove(neighbor_node_str) # Không cần thiết

    return None # Không tìm thấy trong nhánh này với giới hạn độ sâu hiện tại

def iddfs_search(start_node, max_depth=50):
    """Thực hiện tìm kiếm IDDFS."""
    global nodes_expanded_dls # Sử dụng biến global của module
    total_nodes_expanded = 0
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("IDDFS Error: Invalid start node.")
        return []
    print(f"Running IDDFS up to depth {max_depth}...")

    for depth in range(max_depth + 1):
        # print(f"  Trying depth limit: {depth}")
        # Visited set PHẢI được reset cho mỗi lần lặp độ sâu của DLS
        visited = {start_node_str}
        nodes_expanded_dls = 0 # Reset counter cho lần lặp DLS này
        # Bắt đầu DLS từ start_node với path rỗng ban đầu
        result = _dfs_limited_recursive(start_node, depth, [], visited)
        total_nodes_expanded += nodes_expanded_dls # Cộng dồn số node đã duyệt
        # print(f"    Expanded {nodes_expanded_dls} nodes at depth {depth}.")

        if result is not None:
            print(f"  Goal found at depth {depth}.")
            print(f"IDDFS: Total expanded nodes (sum over depths): {total_nodes_expanded}.")
            return result # Trả về path (list of states)

    print(f"  Goal not found within depth limit {max_depth}.")
    print(f"IDDFS: Total expanded nodes (sum over depths): {total_nodes_expanded}.")
    return []