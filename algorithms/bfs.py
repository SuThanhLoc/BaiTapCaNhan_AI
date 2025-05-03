# -*- coding: utf-8 -*-
# algorithms/bfs.py
""" Thuật toán Breadth-First Search (BFS) """

from collections import deque
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string

def bfs_search(start_node):
    """Thực hiện tìm kiếm BFS."""
    queue = deque([(start_node, [])]) # (state, path_list_of_states)
    visited = set()
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("BFS Error: Invalid start node.")
        return [] # Check valid start

    visited.add(start_node_str)
    nodes_expanded = 0
    goal_str = change_matran_string(Goal) # So sánh chuỗi cho nhanh

    while queue:
        matran_hientai, path = queue.popleft()
        nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai) # Lấy chuỗi của trạng thái hiện tại

        if matran_hientai_str == goal_str:
            print(f"BFS: Expanded {nodes_expanded} nodes.")
            # Trả về đường đi bao gồm cả trạng thái cuối cùng
            return path + [matran_hientai]

        x, y = Tim_0(matran_hientai)
        if x == -1:
            # print(f"BFS Warning: Invalid state encountered (no blank tile): {matran_hientai}")
            continue # Trạng thái không hợp lệ

        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy # Tọa độ MỚI của ô trống
            if Check(new_X, new_Y):
                # Truyền tọa độ cũ và mới của ô trống
                new_matran = DiChuyen(matran_hientai, x, y, new_X, new_Y)
                if new_matran: # Check if DiChuyen succeeded
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str and new_matran_str not in visited:
                        visited.add(new_matran_str)
                        # Thêm trạng thái *trước đó* vào path khi thêm neighbor
                        queue.append((new_matran, path + [matran_hientai]))

    print(f"BFS: Expanded {nodes_expanded} nodes. Goal not found.")
    return [] # Trả về list rỗng nếu không tìm thấy