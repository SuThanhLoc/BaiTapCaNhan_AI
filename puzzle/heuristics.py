# -*- coding: utf-8 -*-
# puzzle/heuristics.py
"""
Module chứa các hàm tính heuristic cho bài toán 8-puzzle.
"""
from .state import Goal # Import Goal từ state.py cùng cấp

# Cache cho vị trí đích của các ô số (Manhattan)
# Sử dụng dictionary để cache động dựa trên trạng thái đích
_manhattan_goal_pos_cache = {}

def _get_goal_positions(goal_state=Goal):
    """Helper function to get (and cache) goal positions."""
    # Sử dụng tuple của tuple làm key vì list không hashable
    goal_tuple = tuple(tuple(row) for row in goal_state)
    if goal_tuple not in _manhattan_goal_pos_cache:
        # print(f"Creating Manhattan cache for goal: {goal_tuple}") # Debug cache creation
        cache = {goal_state[i][j]: (i, j) for i in range(3) for j in range(3) if goal_state[i][j] != 0}
        _manhattan_goal_pos_cache[goal_tuple] = cache
        # print(f"Cache created: {_manhattan_goal_pos_cache[goal_tuple]}")
    # else:
        # print(f"Using cached Manhattan positions for goal: {goal_tuple}")
    return _manhattan_goal_pos_cache[goal_tuple]

def khoang_cach_mahathan(matran_hientai, goal_state=Goal):
    """Tính tổng khoảng cách Manhattan từ vị trí hiện tại của các ô số đến vị trí đích."""
    sum_val = 0
    if matran_hientai is None: return float('inf')
    # Đảm bảo goal_state hợp lệ
    if not isinstance(goal_state, list) or len(goal_state)!=3: goal_state = Goal

    try:
        goal_pos_cache = _get_goal_positions(goal_state)
    except Exception as e:
        print(f"Error getting goal positions for {goal_state}: {e}")
        return float('inf') # Lỗi khi lấy vị trí đích

    for i in range(3):
        for j in range(3):
            try:
                tile = matran_hientai[i][j]
                if tile != 0:
                    # Lấy vị trí đích từ cache
                    pos_x, pos_y = goal_pos_cache.get(tile, (-1, -1))

                    if pos_x != -1: # Nếu ô số có trong trạng thái đích
                        sum_val += abs(i - pos_x) + abs(j - pos_y)
                    else:
                        # Ô số không tồn tại trong trạng thái đích -> trạng thái không hợp lệ so với đích
                        # print(f"Warning: Tile {tile} not found in goal cache for goal {goal_state}")
                        return float('inf')
            except (IndexError, TypeError):
                 # print(f"Error accessing tile at [{i}][{j}] or tile value issue.")
                 return float('inf') # Lỗi truy cập hoặc giá trị ô không hợp lệ

    return sum_val

def Chiphi(matran_hientai, goal_state=Goal):
    """Tính số ô sai vị trí (không kể ô trống) so với trạng thái đích."""
    dem = 0
    if matran_hientai is None: return float('inf')
    # Đảm bảo goal_state hợp lệ
    if not isinstance(goal_state, list) or len(goal_state)!=3: goal_state = Goal

    for i in range(3):
        for j in range(3):
            try:
                if matran_hientai[i][j] != 0 and matran_hientai[i][j] != goal_state[i][j]:
                    dem += 1
            except (IndexError, TypeError):
                 # print(f"Error comparing tile at [{i}][{j}] in Chiphi.")
                 return float('inf') # Lỗi thì trả về heuristic vô cùng
    return dem

# Hàm tim_X không còn thực sự cần thiết nếu dùng _get_goal_positions
# nhưng giữ lại nếu có code nào đó vẫn dùng trực tiếp
_tim_x_goal_pos_cache = None
def tim_X(x_value, goal_state=Goal):
    """Tìm tọa độ (hàng, cột) của giá trị x_value trong ma trận Đích (goal_state)."""
    global _tim_x_goal_pos_cache
    # Cache đơn giản cho hàm này, giả sử Goal không đổi thường xuyên trong 1 lần chạy
    if _tim_x_goal_pos_cache is None:
        try:
             _tim_x_goal_pos_cache = {goal_state[i][j]: (i, j) for i in range(3) for j in range(3)}
        except (IndexError, TypeError):
             print("Error creating tim_X cache. Using default Goal.")
             _tim_x_goal_pos_cache = {Goal[i][j]: (i, j) for i in range(3) for j in range(3)}

    return _tim_x_goal_pos_cache.get(x_value, (-1,-1))