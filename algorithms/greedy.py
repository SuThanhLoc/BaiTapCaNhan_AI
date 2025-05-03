# -*- coding: utf-8 -*-
# algorithms/greedy.py
""" Thuật toán Greedy Best-First Search """

from queue import PriorityQueue
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Sử dụng Manhattan làm heuristic

def greedy_search(start_node):
    """Thực hiện tìm kiếm Greedy Best-First Search."""
    qp = PriorityQueue()
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("Greedy Error: Invalid start node.")
        return []

    h_start = khoang_cach_mahathan(start_node, Goal)
    if h_start == float('inf'):
        print("Greedy Error: Start node invalid vs Goal or heuristic failed.")
        return []

    # Queue lưu: (heuristic_cost, state, path_list_of_states)
    qp.put( (h_start, start_node, []) )
    visited = set() # Chỉ cần set để tránh quay vòng vô hạn
    visited.add(start_node_str)
    nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while not qp.empty():
        h, matran_hientai, path = qp.get()
        nodes_expanded += 1
        matran_hientai_str = change_matran_string(matran_hientai)
        if not matran_hientai_str: continue

        if matran_hientai_str == goal_str:
            print(f"Greedy Search: Expanded {nodes_expanded} nodes.")
            return path + [matran_hientai]

        x, y = Tim_0(matran_hientai)
        if x == -1: continue

        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                new_matran = DiChuyen(matran_hientai, x, y, new_X, new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    # Chỉ thêm vào queue nếu hợp lệ và chưa thăm
                    if new_matran_str and new_matran_str not in visited:
                        visited.add(new_matran_str)
                        h_new = khoang_cach_mahathan(new_matran, Goal)
                        if h_new != float('inf'): # Chỉ thêm nếu heuristic hợp lệ
                            qp.put((h_new, new_matran, path + [matran_hientai]))

    print(f"Greedy Search: Expanded {nodes_expanded} nodes. Goal not found.")
    return []