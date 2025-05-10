from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string

Moves_Dir_Name_Bt = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


def backtracking_recursive(current_state, goal_state_matrix, path_states, visited_in_path_strs, max_depth):
    current_state_str = change_matran_string(current_state)

    if current_state_str == change_matran_string(goal_state_matrix):
        return path_states + [current_state]

    if len(path_states) >= max_depth:
        return None

    x0, y0 = Tim_0(current_state)
    if x0 == -1: return None

    for move_name, (dx, dy) in Moves_Dir_Name_Bt.items():
        new_x, new_y = x0 + dx, y0 + dy
        if Check(new_x, new_y):
            next_state_matrix = DiChuyen(current_state, x0, y0, new_x, new_y)
            if next_state_matrix:
                next_state_str = change_matran_string(next_state_matrix)
                if next_state_str not in visited_in_path_strs:
                    visited_in_path_strs.add(next_state_str)
                    result = backtracking_recursive(next_state_matrix, goal_state_matrix,
                                                    path_states + [current_state],
                                                    visited_in_path_strs, max_depth)
                    visited_in_path_strs.remove(next_state_str)
                    if result:
                        return result
    return None


def solve_with_backtracking(start_node_matrix, goal_state_matrix=Goal, max_depth_bt=30):
    start_node_str = change_matran_string(start_node_matrix)
    if not start_node_str: return []

    path_found = backtracking_recursive(start_node_matrix, goal_state_matrix,
                                        [], {start_node_str}, max_depth_bt)

    return path_found if path_found else []