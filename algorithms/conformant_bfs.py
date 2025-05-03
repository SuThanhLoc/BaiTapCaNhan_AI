# -*- coding: utf-8 -*-
# algorithms/conformant_bfs.py
""" Thuật toán Conformant Breadth-First Search """

from collections import deque
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves_Dir_Name, Tim_0, Check, DiChuyen, change_matran_string

def conformant_bfs_search(initial_belief_state_list, goal_state=Goal):
    """
    Thực hiện tìm kiếm Conformant BFS trên không gian trạng thái niềm tin.
    Trả về một list các TÊN nước đi ('U', 'D', 'L', 'R') nếu tìm thấy, hoặc None nếu không.
    """
    print(f"Running Conformant BFS...")
    nodes_expanded_conf = 0 # Đếm số belief state đã được mở rộng

    # --- Kiểm tra đầu vào ---
    if not initial_belief_state_list:
        print("Conformant BFS Error: Initial belief state list is empty.")
        return None
    try:
        goal_str = change_matran_string(goal_state)
        if not goal_str: raise ValueError("Goal state is invalid")
    except Exception as e:
        print(f"Conformant BFS Error: Invalid goal state provided: {e}")
        return None

    # --- Thiết lập Trạng thái Niềm tin Ban đầu ---
    # Chuyển list các ma trận thành một frozenset các chuỗi (để hash được)
    initial_belief_set_str = set()
    for state_matrix in initial_belief_state_list:
        state_str = change_matran_string(state_matrix)
        if state_str:
            initial_belief_set_str.add(state_str)
        else:
            # Bỏ qua state không hợp lệ trong belief set ban đầu
            print(f"Conformant BFS Warning: Invalid state removed from initial belief set: {state_matrix}")
    if not initial_belief_set_str:
        print("Conformant BFS Error: Initial belief state contains no valid states.")
        return None
    # Dùng frozenset vì nó hashable và có thể dùng làm key trong set/dict
    initial_belief_frozenset = frozenset(initial_belief_set_str)

    # --- Kiểm tra nếu trạng thái niềm tin ban đầu đã là đích ---
    # Đích đạt được nếu TẤT CẢ các state trong belief set đều là goal state
    is_initial_goal = all(state_str == goal_str for state_str in initial_belief_frozenset)
    if is_initial_goal:
        print("  Conformant BFS: Initial belief state is already the goal state.")
        return [] # Trả về path rỗng (không cần nước đi nào)

    # --- Khởi tạo BFS ---
    # Queue lưu: (belief_state_frozenset, path_list_of_move_NAMES)
    queue = deque([(initial_belief_frozenset, [])])
    # Visited lưu các belief state (frozenset) đã thăm
    visited = {initial_belief_frozenset}
    MAX_BFS_NODES = 50000 # Giới hạn an toàn để tránh hết bộ nhớ

    while queue:
        nodes_expanded_conf += 1
        if nodes_expanded_conf > MAX_BFS_NODES:
            print(f"  Conformant BFS: Node limit ({MAX_BFS_NODES}) reached. Aborting.")
            return None # Không tìm thấy do giới hạn

        current_belief_fset_str, path_names = queue.popleft()

        # --- Thử từng nước đi có thể ('U', 'D', 'L', 'R') ---
        for move_name, move_dir in Moves_Dir_Name.items():
            next_belief_set_str = set() # Tập hợp các state string trong belief state tiếp theo
            possible_to_form_next_belief = True # Cờ kiểm tra tính hợp lệ khi tạo belief state mới

            # Áp dụng nước đi cho TỪNG state trong belief state hiện tại
            for state_str in current_belief_fset_str:
                # Chuyển string về ma trận để dùng các hàm helper hiện có
                # (Cách này không hiệu quả lắm, tốt hơn là sửa helper để làm việc với string)
                try:
                    # Cẩn thận khi chuyển đổi string -> matrix
                    state_list = [list(map(int, list(state_str[i*3:(i+1)*3]))) for i in range(3)]
                except (ValueError, IndexError):
                    # print(f"Conformant BFS Warning: Failed to convert state string '{state_str}' back to matrix.")
                    possible_to_form_next_belief = False; break # Lỗi chuyển đổi -> không thể tạo belief mới

                x, y = Tim_0(state_list)
                if x == -1:
                    # print(f"Conformant BFS Warning: Could not find blank in state {state_str} within belief set.")
                    # Nếu một state trong belief không có ô trống, có thể coi nước đi không thể thực hiện?
                    # Hoặc state đó vẫn giữ nguyên? Giả sử giữ nguyên.
                    next_belief_set_str.add(state_str) # Thêm state gốc lại
                    continue # Chuyển sang state khác trong belief

                new_x, new_y = x + move_dir[0], y + move_dir[1]

                # Nếu nước đi hợp lệ TẠI state này
                if Check(new_x, new_y):
                    next_state_list = DiChuyen(state_list, x, y, new_x, new_y)
                    if next_state_list:
                        next_state_str = change_matran_string(next_state_list)
                        if next_state_str:
                            next_belief_set_str.add(next_state_str) # Thêm kết quả vào belief mới
                        else:
                            # print(f"Conformant BFS Warning: DiChuyen resulted in invalid state string for move {move_name} from {state_str}")
                            # Lỗi sinh state mới -> nước đi này không an toàn cho belief state?
                            possible_to_form_next_belief = False; break
                    else:
                        # print(f"Conformant BFS Warning: DiChuyen failed for move {move_name} from {state_str}")
                        possible_to_form_next_belief = False; break
                # Nếu nước đi KHÔNG hợp lệ tại state này (ví dụ: ô trống ở góc trên cùng, đi 'U')
                else:
                    # Trạng thái vật lý không thay đổi, nên state này vẫn nằm trong belief set tiếp theo
                    next_belief_set_str.add(state_str)

            # Nếu có lỗi xảy ra khi tạo belief state tiếp theo, bỏ qua nước đi này
            if not possible_to_form_next_belief:
                continue

            # Nếu belief state tiếp theo rỗng (không nên xảy ra với logic trên), bỏ qua
            if not next_belief_set_str:
                continue

            # --- Xử lý Belief State Tiếp theo ---
            next_belief_frozenset = frozenset(next_belief_set_str)

            # Bỏ qua nếu belief state này đã được thăm
            if next_belief_frozenset in visited:
                continue

            # --- Kiểm tra Đích ---
            # Đích đạt được nếu TẤT CẢ các state trong belief set mới đều là goal state
            is_goal = all(s_str == goal_str for s_str in next_belief_frozenset)
            if is_goal:
                print(f"  Conformant BFS: Goal reached! Expanded {nodes_expanded_conf} belief states.")
                # Trả về danh sách các TÊN nước đi đã thực hiện
                return path_names + [move_name]

            # --- Thêm vào Queue và Visited ---
            visited.add(next_belief_frozenset)
            queue.append((next_belief_frozenset, path_names + [move_name]))

    # Nếu vòng lặp kết thúc mà không tìm thấy đích
    print(f"Conformant BFS: Goal not found after expanding {nodes_expanded_conf} belief states.");
    return None # Trả về None nếu không tìm thấy lời giải