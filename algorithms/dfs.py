# -*- coding: utf-8 -*-
# algorithms/dfs.py
""" Thuật toán Depth-First Search (DFS) """

from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string

def dfs_search(start_node, max_depth=50): # Thêm giới hạn độ sâu mặc định
    """Thực hiện tìm kiếm DFS với giới hạn độ sâu."""
    print(f"Running DFS with max_depth={max_depth}")
    # Stack lưu: (state, path_list_of_states, current_depth)
    stack = [(start_node, [], 0)]
    visited = set() # Chỉ cần set cho DFS đơn giản để tránh lặp trong 1 nhánh
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("DFS Error: Invalid start node.")
        return []

    visited.add(start_node_str)
    nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while stack:
        matran_hientai, path, depth = stack.pop()
        nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai)
        if not matran_hientai_str: continue

        if matran_hientai_str == goal_str:
            print(f"DFS: Expanded {nodes_expanded} nodes.")
            return path + [matran_hientai]

        # Dừng nếu vượt quá giới hạn độ sâu
        if depth >= max_depth:
            continue

        x, y = Tim_0(matran_hientai)
        if x == -1: continue

        # Duyệt ngược thứ tự Moves để đưa Left/Right lên trước Up/Down trong stack
        # (Giúp khám phá theo thứ tự giống code gốc nếu cần)
        for dx, dy in reversed(Moves):
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                new_matran = DiChuyen(matran_hientai, x, y, new_X, new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    # Chỉ thêm vào stack nếu trạng thái mới hợp lệ và chưa được thăm
                    if new_matran_str and new_matran_str not in visited:
                        visited.add(new_matran_str) # Đánh dấu đã thăm
                        stack.append((new_matran, path + [matran_hientai], depth + 1))

    print(f"DFS: Expanded {nodes_expanded} nodes. Goal not found within depth {max_depth}.")
    return []