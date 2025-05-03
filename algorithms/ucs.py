# -*- coding: utf-8 -*-
# algorithms/ucs.py
""" Thuật toán Uniform Cost Search (UCS) """

# heapq thường nhanh hơn PriorityQueue một chút cho các tác vụ đơn giản
# Bạn có thể chọn dùng 1 trong 2
# from queue import PriorityQueue
import heapq
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string

def ucs_search(start_node):
    """Thực hiện tìm kiếm UCS."""
    # Sử dụng heapq: lưu (cost, state, path)
    # heapq là min-heap nên hoạt động tương tự PriorityQueue cho UCS
    pq = [(0, start_node, [])] # List dùng như heap
    heapq.heapify(pq)

    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("UCS Error: Invalid start node.")
        return []

    # visited stores state_string -> min_g_cost to reach that state
    visited = {start_node_str: 0}
    nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while pq: # Khi heap không rỗng
        # Lấy phần tử có cost nhỏ nhất
        cost, matran_hientai, path = heapq.heappop(pq)
        nodes_expanded += 1
        matran_str = change_matran_string(matran_hientai)
        if not matran_str: continue # Bỏ qua trạng thái không hợp lệ

        if matran_str == goal_str:
            print(f"UCS: Expanded {nodes_expanded} nodes.")
            return path + [matran_hientai]

        # Optimization: Nếu chi phí lấy ra lớn hơn chi phí đã biết, bỏ qua
        # (Điều này xảy ra khi một trạng thái được thêm vào heap nhiều lần với chi phí khác nhau)
        if cost > visited.get(matran_str, float('inf')):
            continue

        x, y = Tim_0(matran_hientai)
        if x == -1: continue

        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                new_matran = DiChuyen(matran_hientai, x, y, new_X, new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str:
                         new_cost = cost + 1 # Chi phí mỗi bước là 1
                         # Nếu tìm thấy đường đi tốt hơn đến trạng thái này
                         if new_cost < visited.get(new_matran_str, float('inf')):
                             visited[new_matran_str] = new_cost
                             # Thêm vào heap
                             heapq.heappush(pq, (new_cost, new_matran, path + [matran_hientai]))

    print(f"UCS: Expanded {nodes_expanded} nodes. Goal not found.")
    return []