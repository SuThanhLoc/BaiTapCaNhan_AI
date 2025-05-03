# -*- coding: utf-8 -*-
# algorithms/a_star.py
""" Thuật toán A* Search """

from queue import PriorityQueue
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Sử dụng Manhattan làm heuristic mặc định

def a_star_search(start_node):
    """Thực hiện tìm kiếm A*."""
    qp = PriorityQueue()
    start_node_str = change_matran_string(start_node)
    if not start_node_str:
        print("A* Error: Invalid start node.")
        return []

    g_cost = 0
    h_cost = khoang_cach_mahathan(start_node, Goal) # Tính h cho trạng thái đầu
    if h_cost == float('inf'):
        print("A* Error: Start node invalid vs Goal or heuristic failed.")
        return []

    f_cost = g_cost + h_cost
    # Store: (f_cost, g_cost, state, path_list_of_states)
    qp.put( (f_cost, g_cost, start_node, []) )
    # visited stores state_string -> min_g_cost to reach that state
    visited = {start_node_str: 0}
    nodes_expanded = 0
    goal_str = change_matran_string(Goal)

    while not qp.empty():
        f_n, g_n, matran_hientai, path = qp.get()
        nodes_expanded += 1
        matran_str = change_matran_string(matran_hientai)
        if not matran_str:
            # print("A* Warning: Invalid state retrieved from queue.")
            continue

        # Optimization: If we found a shorter path already, skip
        # Dùng visited.get để tránh KeyError nếu matran_str không có trong visited
        # (mặc dù logic hiện tại đảm bảo nó phải có)
        if g_n > visited.get(matran_str, float('inf')):
             continue

        if matran_str == goal_str:
            print(f"A*: Expanded {nodes_expanded} nodes.")
            return path + [matran_hientai]

        x, y = Tim_0(matran_hientai)
        if x == -1:
            # print(f"A* Warning: Invalid state encountered (no blank tile): {matran_hientai}")
            continue

        for dx, dy in Moves:
            new_X, new_Y = x + dx, y + dy
            if Check(new_X, new_Y):
                new_matran = DiChuyen(matran_hientai, x, y, new_X, new_Y)
                if new_matran:
                    new_matran_str = change_matran_string(new_matran)
                    if new_matran_str:
                        g_new = g_n + 1 # Chi phí mỗi bước là 1
                        # Chỉ xem xét nếu đường đi mới này tốt hơn đường đã biết (hoặc chưa biết)
                        if g_new < visited.get(new_matran_str, float('inf')):
                            h_new = khoang_cach_mahathan(new_matran, Goal)
                            if h_new != float('inf'): # Đảm bảo trạng thái hợp lệ so với Goal
                                visited[new_matran_str] = g_new # Cập nhật chi phí tốt nhất
                                f_new = g_new + h_new
                                qp.put((f_new, g_new, new_matran, path + [matran_hientai]))

    print(f"A*: Expanded {nodes_expanded} nodes. Goal not found.")
    return []