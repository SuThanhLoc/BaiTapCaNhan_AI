# -*- coding: utf-8 -*-
# puzzle/state.py
"""
Module định nghĩa trạng thái và các thao tác cơ bản của bài toán 8-puzzle.
"""
import copy

# --- Trạng thái Bắt đầu và Đích ---
Start = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
Goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# --- Các Hằng số Di chuyển ---
Moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lên, Xuống, Trái, Phải (Tọa độ thay đổi của ô trống)
Moves_Dir_Name = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)} # Tên nước đi -> Thay đổi tọa độ

# --- Các hàm tiện ích thao tác trạng thái ---

def Tim_0(matran_hientai):
    """Tìm tọa độ (hàng, cột) của ô trống (số 0)."""
    if matran_hientai is None: return -1, -1
    # Thêm kiểm tra cấu trúc ma trận cơ bản
    if not isinstance(matran_hientai, (list, tuple)) or len(matran_hientai) != 3:
        # print("Warning: Invalid matrix structure in Tim_0")
        return -1, -1
    for i in range(3):
        # Check if row is valid before accessing
        if not isinstance(matran_hientai[i], (list, tuple)) or len(matran_hientai[i]) != 3:
             # print(f"Warning: Invalid row format in Tim_0 at index {i}")
             return -1, -1
        for j in range(3):
            try:
                 if matran_hientai[i][j] == 0: return i, j
            except IndexError:
                 # print(f"Warning: IndexError accessing [{i}][{j}] in Tim_0")
                 return -1,-1
    # print("Warning: Blank tile (0) not found in Tim_0")
    return -1, -1 # Không tìm thấy số 0

def Check(x, y):
    """Kiểm tra tọa độ có hợp lệ trong bảng 3x3 không."""
    return 0 <= x < 3 and 0 <= y < 3

def DiChuyen(matran_hientai, x, y, new_x, new_y):
    """
    Tạo bản sao của ma trận hiện tại và thực hiện di chuyển ô trống.
    Input là tọa độ CŨ (x,y) và tọa độ MỚI (new_x, new_y) của ô trống.
    Trả về ma trận mới hoặc None nếu lỗi.
    """
    if not isinstance(matran_hientai, list) or not matran_hientai:
        # print("Warning: Invalid input matrix in DiChuyen")
        return None
    # Deep copy để đảm bảo không ảnh hưởng bản gốc
    # Sử dụng list comprehension cho deep copy hiệu quả với list 2D chứa số
    try:
        new_state = [row[:] for row in matran_hientai]
        # Swap giá trị tại vị trí cũ của ô trống và vị trí mới của ô trống
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    except (IndexError, TypeError) as e:
        # print(f"Warning: Error during swap in DiChuyen ({x},{y}) <-> ({new_x},{new_y}): {e}")
        return None # Trả về None nếu có lỗi
    return new_state

def change_matran_string(matran):
    """Chuyển ma trận thành chuỗi để dùng làm key trong set/dict (visited)."""
    if matran is None: return ""
    # Đảm bảo là ma trận hợp lệ trước khi chuyển đổi
    if not isinstance(matran, (list, tuple)) or len(matran) != 3: return ""
    if not all(isinstance(row, (list, tuple)) and len(row) == 3 for row in matran): return ""
    try:
        # Nối các số thành một chuỗi duy nhất
        return ''.join(str(num) for row in matran for num in row)
    except TypeError:
        # print("Warning: TypeError during matrix to string conversion.")
        return "" # Trả về chuỗi rỗng nếu có lỗi type

def print_matrix(matran):
    """In ma trận ra màn hình cho dễ nhìn."""
    if matran and isinstance(matran, list) and all(isinstance(row, list) and len(row)==3 for row in matran):
        print("-" * 5);
        for row in matran:
            # Đảm bảo các phần tử là số trước khi join
            try:
                 print(" ".join(map(str, row)))
            except TypeError:
                 print("Invalid row content")
                 break
        print("-" * 5)
    else:
        print("Invalid matrix format for printing")

# Có thể thêm lớp PuzzleState ở đây sau nếu muốn refactor nâng cao
# class PuzzleState:
#     def __init__(self, board, g=0, parent=None, move=None):
#         self.board = board
#         self.g = g # cost from start
#         self.parent = parent
#         self.move = move # Move name ('U', 'D', 'L', 'R') that led to this state
#         self._str_rep = None
#         self._hash = None
#         # ... (thêm các phương thức find_blank, get_successors, is_goal, to_string...)