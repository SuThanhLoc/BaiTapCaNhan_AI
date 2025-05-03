# -*- coding: utf-8 -*-
# ui/visualization.py
""" Module chính quản lý giao diện và vòng lặp Pygame """

import pygame as pg
import sys
import random
import threading
import time
import math # Needed for ceil and exp (Sim Anneal)
import copy # Needed for deepcopy

# --- Import các thành phần UI cùng cấp ---
from .constants import * # Import tất cả hằng số
from .button import Button
from .drawing import draw_text, find_zero_pos, grid_to_pixel_large, lerp, draw_8_puzzle

# --- Import Logic Puzzle ---
from puzzle.state import Start, Goal # Import trạng thái mặc định
# (Không cần import các hàm state khác nếu dùng PuzzleState class sau này)
# Tạm thời import các hàm cần thiết trực tiếp
from puzzle.state import Tim_0, Check, DiChuyen, change_matran_string, print_matrix
# Import các hàm heuristic
from puzzle.heuristics import khoang_cach_mahathan, Chiphi

# --- Import các Thuật toán ---
# Import từng hàm thuật toán từ module tương ứng
# (LƯU Ý: Đảm bảo bạn đã tạo và di chuyển code vào các file này)
try:
    from algorithms.bfs import bfs_search
    from algorithms.dfs import dfs_search # Đổi tên hàm nếu cần
    from algorithms.ucs import ucs_search
    from algorithms.iddfs import iddfs_search
    from algorithms.greedy import greedy_search
    from algorithms.a_star import a_star_search
    from algorithms.ida_star import ida_star_search
    # Gộp hill climbing từ hill_climbing.py
    from algorithms.hill_climbing import (simple_hill_climbing_first_choice,
                                         steepest_ascent_hill_climbing,
                                         stochastic_hill_climbing)
    from algorithms.simulated_annealing import simulated_annealing_search
    from algorithms.beam_search import beam_search
    from algorithms.genetic_algorithm import genetic_algorithm_search
    from algorithms.conformant_bfs import conformant_bfs_search

    print("Algorithm functions loaded successfully.")
    ALGORITHMS_IMPORTED = True
except ImportError as e:
    print(f"---------------------------------------------------------")
    print(f"LỖI IMPORT THUẬT TOÁN: {e}")
    print(f"Không thể import một hoặc nhiều hàm thuật toán từ thư mục 'algorithms/'.")
    print(f"Đảm bảo bạn đã tạo các file .py và di chuyển code thuật toán vào đó.")
    print(f"Sử dụng các hàm FALLBACK để chạy giao diện.")
    print(f"---------------------------------------------------------")
    ALGORITHMS_IMPORTED = False
    # Định nghĩa các hàm fallback nếu import lỗi
    def bfs_search(s): time.sleep(0.1); print("Fallback BFS"); return [s, [[2,6,5],[4,0,7],[8,3,1]], Goal]
    def dfs_search(s, md=50): time.sleep(0.1); print("Fallback DFS"); return [s, Goal] # Sửa fallback DFS
    def ucs_search(s): time.sleep(0.1); print("Fallback UCS"); return [s, Goal]
    def iddfs_search(s, md=50): time.sleep(0.2); print("Fallback IDDFS"); return []
    def greedy_search(s): time.sleep(0.1); print("Fallback Greedy"); return [s, Goal]
    def a_star_search(s): time.sleep(0.1); print("Fallback A*"); return [s, [[2,6,5],[4,8,7],[0,3,1]], Goal]
    def ida_star_search(s, mt=80): time.sleep(0.2); print("Fallback IDA*"); return [s, Goal]
    def simple_hill_climbing_first_choice(s, ms=1000): time.sleep(0.1); print("Fallback Simple HC"); return [s]
    def steepest_ascent_hill_climbing(s, ms=1000): time.sleep(0.1); print("Fallback Steepest HC"); return [s]
    def stochastic_hill_climbing(s, ms=1000): time.sleep(0.1); print("Fallback Stochastic HC"); return [s, Goal]
    def simulated_annealing_search(s, it=100, cr=0.95, mt=0.1, mi=5000): time.sleep(0.1); print("Fallback SA"); return [s]
    def beam_search(s, bw=5, mi=1000): time.sleep(0.1); print("Fallback Beam"); return [s, Goal]
    def genetic_algorithm_search(s, g, ps=100, gen=100, mr=0.1): time.sleep(0.1); print("Fallback GA"); return [g] if random.random()<0.5 else []
    def conformant_bfs_search(bl, g): time.sleep(0.2); print("Fallback Conformant"); return ['R','U'] if random.random()<0.5 else None


# --- Solver Thread Function ---
# (Giữ nguyên logic cơ bản, nhưng gọi hàm đã import)
solver_thread = None
solver_result = None # Dùng dict để chứa kết quả và thông tin khác

def run_solver(algorithm_func, start_input, algo_name, result_container_ref):
    """Hàm chạy thuật toán trong thread riêng."""
    global solver_result
    try:
        print(f"Thread started for {algo_name}...")
        start_time = time.time()
        path_result = None # Kết quả cuối cùng

        # Gọi hàm thuật toán tương ứng
        if algo_name == "Conformant BFS":
            path_result = algorithm_func(start_input, Goal)
        elif algo_name == "IDDFS":
            path_result = algorithm_func(start_input, max_depth=30)
        elif algo_name == "IDA*":
             path_result = algorithm_func(start_input, max_threshold=80)
        elif algo_name in ["Simple HC", "Steepest HC", "Stochastic HC"]:
             path_result = algorithm_func(start_input, max_steps=2000)
        elif algo_name == "Sim Anneal":
             path_result = algorithm_func(start_input, initial_temp=100, cooling_rate=0.97, min_temp=0.1, max_iterations=15000)
        elif algo_name == "Beam Search":
             path_result = algorithm_func(start_input, beam_width=5, max_iterations=1000)
        elif algo_name == "Genetic Algo":
             path_result = algorithm_func(start_input, Goal, population_size=100, generations=200, mutation_rate=0.2)
        else:
            path_result = algorithm_func(start_input)

        end_time = time.time()
        solve_time = end_time - start_time
        print(f"Thread for {algo_name} finished in {solve_time:.4f} seconds.")
        solver_result = {"path": path_result, "error": None, "time": solve_time, "algo": algo_name}

    except Exception as e:
        import traceback
        print(f"!!! Solver Thread critical error for {algo_name}: {e}")
        traceback.print_exc()
        solver_result = {"path": None, "error": str(e), "time": 0, "algo": algo_name}


# --- Lớp chính quản lý ứng dụng Visualization ---
class VisualizationApp:
    def __init__(self):
        pg.init()
        if 'FONT_MAIN_REGULAR' not in globals(): pg.font.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.start_state = copy.deepcopy(Start)
        self.goal_state = copy.deepcopy(Goal)
        self.sample_initial_belief_state = [
            [[2, 6, 5], [0, 8, 7], [4, 3, 1]],
            [[2, 6, 5], [8, 0, 7], [4, 3, 1]],
            [[2, 0, 5], [6, 8, 7], [4, 3, 1]]
        ]
        self.current_step_index = 0
        self.selected_algorithm_name = None
        self.is_solving = False
        self.solver_thread = None
        self.path = [self.start_state]
        self.path_found = False
        self.found_path_type = None
        self.status_message = "Chọn Thuật Toán Để Bắt Đầu !"
        self.status_color = COLOR_TEXT_SECONDARY
        self.is_overall_animating = False
        self.step_complete_time = 0
        self.is_tile_animating = False
        self.animating_tile_value = None
        self.animating_tile_rect = pg.Rect(0, 0, TILE_SIZE_LARGE, TILE_SIZE_LARGE)
        self.animating_tile_start_pixel_pos = (0, 0)
        self.animating_tile_end_pixel_pos = (0, 0)
        self.tile_animation_start_time = 0
        self.algo_buttons = self._create_algo_buttons()
        self.nav_buttons = self._create_nav_buttons()
        self._update_nav_button_state()
        self.algorithms_map = {
            "DFS": dfs_search, "BFS": bfs_search, "UCS": ucs_search,
            "IDDFS": iddfs_search, "Greedy": greedy_search, "A*": a_star_search,
            "IDA*": ida_star_search,
            "Simple HC": simple_hill_climbing_first_choice,
            "Steepest HC": steepest_ascent_hill_climbing,
            "Stochastic HC": stochastic_hill_climbing,
            "Sim Anneal": simulated_annealing_search,
            "Beam Search": beam_search,
            "Genetic Algo": genetic_algorithm_search,
            "Conformant BFS": conformant_bfs_search
        } if ALGORITHMS_IMPORTED else {
            "DFS": dfs_search, "BFS": bfs_search, "UCS": ucs_search,
            "IDDFS": iddfs_search, "Greedy": greedy_search, "A*": a_star_search,
            "IDA*": ida_star_search,
            "Simple HC": simple_hill_climbing_first_choice,
            "Steepest HC": steepest_ascent_hill_climbing,
            "Stochastic HC": stochastic_hill_climbing,
            "Sim Anneal": simulated_annealing_search,
            "Beam Search": beam_search,
            "Genetic Algo": genetic_algorithm_search,
            "Conformant BFS": conformant_bfs_search
        }

    def _create_algo_buttons(self):
        buttons = []
        for i, algo_name_display in enumerate(ALGORITHMS_TO_DISPLAY):
            btn_y = BUTTON_COLUMN_START_Y + i * (ALGO_BUTTON_HEIGHT + BUTTON_GAP_Y)
            is_belief = (algo_name_display == "Conformant BFS")
            button = Button(ALGO_BUTTON_X, btn_y, ALGO_BUTTON_WIDTH, ALGO_BUTTON_HEIGHT, algo_name_display,
                            callback=self.handle_algo_button_click,
                            is_belief_button=is_belief)
            buttons.append(button)
        return buttons

    def _create_nav_buttons(self):
        buttons = {
            "prev": Button(POS_PREV_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Lùi",
                           callback=self.nav_button_click,
                           base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER),
            "next": Button(POS_NEXT_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Tiến",
                           callback=self.nav_button_click,
                           base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER)
        }
        return buttons

    def _update_nav_button_state(self):
        can_navigate = self.path_found and self.found_path_type == 'states' and len(self.path) > 1
        # print(f"DEBUG: _update_nav_button_state: can_navigate = {can_navigate}") # Optional print
        self.nav_buttons["prev"].is_disabled = not can_navigate
        self.nav_buttons["next"].is_disabled = not can_navigate

    def handle_algo_button_click(self, algo_name_clicked):
        global solver_result
        if self.is_solving: print("Already solving, please wait."); return
        self.selected_algorithm_name = algo_name_clicked
        print(f"Algorithm Button '{self.selected_algorithm_name}' clicked.")
        self.is_solving = True; solver_result = None; self.path = []; self.path_found = False; self.found_path_type = None
        self.current_step_index = 0; self.is_overall_animating = False; self.is_tile_animating = False
        self.status_message = f"Đang giải bằng {self.selected_algorithm_name}..."; self.status_color = COLOR_TEXT_ACCENT
        for btn in self.algo_buttons: btn.is_selected = (btn.text == self.selected_algorithm_name); btn.is_disabled = True
        self._update_nav_button_state()
        algo_func = self.algorithms_map.get(self.selected_algorithm_name)
        start_input_arg = None
        if self.selected_algorithm_name == "Conformant BFS":
            start_input_arg = copy.deepcopy(self.sample_initial_belief_state)
            print(f"Using sample belief state for {self.selected_algorithm_name}: {len(start_input_arg)} initial states.")
            if start_input_arg: self.path = [start_input_arg[0]]
            else: self.path = [copy.deepcopy(self.start_state)]
        else:
            start_input_arg = copy.deepcopy(self.start_state)
            self.path = [start_input_arg]
        if algo_func and start_input_arg is not None:
            self.solver_thread = threading.Thread(target=run_solver,
                                             args=(algo_func, start_input_arg, self.selected_algorithm_name, solver_result),
                                             daemon=True)
            self.solver_thread.start()
        else:
            errmsg = "không tìm thấy hàm" if not algo_func else "đầu vào không hợp lệ"
            print(f"Error: Cannot run '{self.selected_algorithm_name}' ({errmsg}).")
            self.status_message = f"Lỗi: Không chạy được {self.selected_algorithm_name}"; self.status_color = COLOR_TEXT_ERROR
            self.is_solving = False;
            for btn in self.algo_buttons: btn.is_disabled = False; btn.is_selected = False
            self._update_nav_button_state()
            self.path = [copy.deepcopy(self.start_state)]

    def nav_button_click(self, direction):
        """Xử lý khi nút Lùi/Tiến được click."""
        # THÊM PRINT 1: Kiểm tra hàm có được gọi không
        print(f"DEBUG: nav_button_click('{direction}') được gọi. Index hiện tại: {self.current_step_index}")

        if not self.path_found or not self.path or self.is_tile_animating or self.found_path_type != 'states':
            print(f"DEBUG: Điều kiện nav không thỏa mãn: found={self.path_found}, path_empty={not self.path}, animating={self.is_tile_animating}, type={self.found_path_type}")
            return

        self.is_overall_animating = False
        prev_index = self.current_step_index
        if direction == "Lùi":  # So sánh với text của nút "Lùi"
            self.current_step_index = max(0, self.current_step_index - 1)
        elif direction == "Tiến":  # So sánh với text của nút "Tiến"
            self.current_step_index = min(len(self.path) - 1, self.current_step_index + 1)

        # THÊM PRINT 2: Kiểm tra index có thay đổi không
        print(f"DEBUG: Index thay đổi từ {prev_index} thành {self.current_step_index}")

        if prev_index != self.current_step_index:
             self.step_complete_time = pg.time.get_ticks()


    def _process_solver_result(self):
        """Kiểm tra và xử lý kết quả từ thread giải."""
        global solver_result

        if self.is_solving and self.solver_thread and not self.solver_thread.is_alive():
            self.is_solving = False
            local_solver_result_dict = solver_result
            solver_result = None

            algo_name_from_result = "Unknown"
            self.path_found = False
            self.found_path_type = None
            self.path = [copy.deepcopy(self.start_state)]

            if local_solver_result_dict:
                algo_name_from_result = local_solver_result_dict.get("algo", "Unknown")
                solve_time = local_solver_result_dict.get('time', 0)
                raw_path_result = local_solver_result_dict.get("path")
                error_msg = local_solver_result_dict.get("error")

                if error_msg:
                    self.status_message = f"Lỗi ({algo_name_from_result}): {error_msg}"
                    self.status_color = COLOR_TEXT_ERROR
                    print(f"Solver error reported: {error_msg}")
                elif raw_path_result is not None:
                    if algo_name_from_result == "Conformant BFS":
                        if isinstance(raw_path_result, list):
                            # Kiểm tra list không rỗng trước khi gán path
                            if raw_path_result:
                                self.path = raw_path_result # Lưu list tên
                                self.path_found = True
                                self.found_path_type = 'names'
                                move_count = len(self.path)
                                self.status_message = f"Conformant BFS: Tìm thấy {move_count} nước đi trong {solve_time:.3f}s"
                                self.status_color = COLOR_TEXT_SUCCESS
                                print(f"Conformant BFS path found: {move_count} moves - {self.path}")
                            else: # List rỗng cũng coi như không tìm thấy
                                self.path_found = False
                                self.found_path_type = None
                                self.status_message = f"Conformant BFS: Không tìm thấy đường đi (empty list)."
                                self.status_color = COLOR_TEXT_SECONDARY
                                print("Conformant BFS returned empty list.")

                            # Luôn hiển thị state đầu belief set (ngay cả khi path rỗng)
                            self.path_for_display = [copy.deepcopy(self.sample_initial_belief_state[0])] if self.sample_initial_belief_state else [copy.deepcopy(self.start_state)]
                            self.path = self.path_for_display # Ghi đè self.path để vẽ
                        else:
                             self.status_message = f"Conformant BFS: Kết quả không hợp lệ."
                             self.status_color = COLOR_TEXT_ERROR
                             print("Conformant BFS did not return a list.")
                             self.path = [copy.deepcopy(self.sample_initial_belief_state[0])] if self.sample_initial_belief_state else [copy.deepcopy(self.start_state)]
                    else: # Xử lý các thuật toán khác
                        temp_path = raw_path_result
                        # THÊM PRINT 1: In ra kết quả thô nhận được
                        print(f"DEBUG: Received raw_path_result for {algo_name_from_result}: Type={type(temp_path)}, Len={len(temp_path) if isinstance(temp_path, list) else 'N/A'}")
                        # print(f"DEBUG: Raw path data: {temp_path}") # Bỏ comment dòng này nếu cần xem chi tiết path

                        is_list_of_states = isinstance(temp_path, list) and \
                                            len(temp_path) > 0 and \
                                            all(isinstance(step, list) for step in temp_path)
                        # THÊM PRINT 2: Kiểm tra có phải list các state không
                        print(f"DEBUG: is_list_of_states = {is_list_of_states}")

                        is_valid_path_structure = False
                        if is_list_of_states:
                            is_valid_path_structure = all(len(step) == 3 and all(isinstance(row, list) and len(row)==3 for row in step) for step in temp_path)
                        # THÊM PRINT 3: Kiểm tra cấu trúc path có hợp lệ không
                        print(f"DEBUG: is_valid_path_structure = {is_valid_path_structure}")

                        if is_valid_path_structure:
                            self.path = temp_path
                            self.path_found = True
                            self.found_path_type = 'states'
                            self.current_step_index = 0
                            goal_str = change_matran_string(self.goal_state)
                            is_only_goal = len(self.path) == 1 and change_matran_string(self.path[0]) == goal_str

                            if is_only_goal:
                                self.is_overall_animating = False
                                self.status_message = f"{algo_name_from_result}: Tìm thấy Goal State trong {solve_time:.3f}s."
                                self.status_color = COLOR_TEXT_SUCCESS
                                print("Goal state found directly.")
                            elif len(self.path) > 1:
                                self.is_overall_animating = True
                                self.step_complete_time = pg.time.get_ticks()
                                self.status_message = f"{algo_name_from_result}: Tìm thấy đường đi ({len(self.path)} bước) trong {solve_time:.3f}s."
                                self.status_color = COLOR_TEXT_SUCCESS
                                print(f"Path processed: {len(self.path)} steps. Ready to animate.")
                            else:
                                self.is_overall_animating = False
                                self.path_found = False # Coi như không tìm thấy Goal
                                self.status_message = f"{algo_name_from_result}: Dừng ở bước {len(self.path)} (không phải Goal) trong {solve_time:.3f}s."
                                self.status_color = COLOR_TEXT_SECONDARY
                                print("Path found but not Goal state.")
                        elif isinstance(temp_path, list) and len(temp_path) == 0:
                            self.status_message = f"{algo_name_from_result}: Không tìm thấy đường đi.";
                            if solve_time > 0: self.status_message += f" (Tìm kiếm trong {solve_time:.3f}s)"
                            self.status_color = COLOR_TEXT_SECONDARY
                            print("No path found by solver (empty list).")
                            self.path = [copy.deepcopy(self.start_state)]
                            self.path_found = False # Đảm bảo reset
                            self.found_path_type = None
                        else:
                             self.status_message = f"Lỗi: Kết quả từ {algo_name_from_result} không hợp lệ."; self.status_color = COLOR_TEXT_ERROR
                             print(f"Invalid/Unknown result structure: {temp_path}")
                             self.path = [copy.deepcopy(self.start_state)]
                             self.path_found = False # Đảm bảo reset
                             self.found_path_type = None
                else: # raw_path_result là None
                    self.status_message = f"Lỗi Solver: Không nhận được kết quả từ {algo_name_from_result}."
                    self.status_color = COLOR_TEXT_ERROR
                    print("Solver path result was None.")
                    self.path = [copy.deepcopy(self.start_state)]
                    self.path_found = False # Đảm bảo reset
                    self.found_path_type = None
            else: # Lỗi solver_result dict rỗng
                 print("Solver finished but local_solver_result_dict is None or invalid.")
                 self.status_message = "Lỗi Solver: Kết quả không xác định."; self.status_color = COLOR_TEXT_ERROR
                 self.path = [copy.deepcopy(self.start_state)]
                 self.path_found = False # Đảm bảo reset
                 self.found_path_type = None

            # Kích hoạt lại các nút thuật toán
            for btn in self.algo_buttons:
                btn.is_disabled = False
                btn.is_selected = (btn.text == algo_name_from_result)

            # THÊM PRINT 4: In trạng thái ngay trước khi cập nhật nút nav
            print(f"DEBUG: BEFORE calling _update_nav_button_state: path_found={self.path_found}, type={self.found_path_type}, len={len(self.path) if self.path else 0}")

            # Cập nhật trạng thái nút điều hướng
            self._update_nav_button_state()


    def _update_tile_animation(self, current_time):
        """Cập nhật logic animation trượt ô."""
        if self.is_tile_animating and self.found_path_type == 'states':
            elapsed = current_time - self.tile_animation_start_time
            progress = min(1.0, elapsed / TILE_ANIMATION_DURATION)
            current_x = lerp(self.animating_tile_start_pixel_pos[0], self.animating_tile_end_pixel_pos[0], progress)
            current_y = lerp(self.animating_tile_start_pixel_pos[1], self.animating_tile_end_pixel_pos[1], progress)
            self.animating_tile_rect.topleft = (int(current_x), int(current_y))
            if progress >= 1.0:
                self.is_tile_animating = False
                self.step_complete_time = current_time
                if self.current_step_index >= len(self.path) - 1:
                    self.is_overall_animating = False

    def _update_overall_animation(self, current_time):
        """Cập nhật logic tự động chuyển bước."""
        if (self.is_overall_animating and self.path_found and
                not self.is_tile_animating and self.found_path_type == 'states' and
                self.current_step_index < len(self.path) - 1):
            if current_time - self.step_complete_time >= STEP_DELAY:
                target_step_index = self.current_step_index + 1
                if 0 <= self.current_step_index < len(self.path) and 0 <= target_step_index < len(self.path):
                    prev_state = self.path[self.current_step_index]
                    next_state = self.path[target_step_index]
                    if isinstance(prev_state, list) and isinstance(next_state, list):
                        prev_zero_pos = find_zero_pos(prev_state)
                        next_zero_pos = find_zero_pos(next_state)
                        if prev_zero_pos and next_zero_pos:
                            moving_tile_r, moving_tile_c = prev_zero_pos
                            try:
                                self.animating_tile_value = next_state[moving_tile_r][moving_tile_c]
                            except IndexError:
                                self.is_overall_animating = False; self.animating_tile_value = None; print("Anim Error: Index out of bounds accessing next_state"); return
                            if self.animating_tile_value is not None and self.animating_tile_value != 0:
                                start_r, start_c = next_zero_pos
                                self.animating_tile_start_pixel_pos = grid_to_pixel_large(start_r, start_c)
                                end_r, end_c = prev_zero_pos
                                self.animating_tile_end_pixel_pos = grid_to_pixel_large(end_r, end_c)
                                self.is_tile_animating = True
                                self.animating_tile_rect.topleft = self.animating_tile_start_pixel_pos
                                self.tile_animation_start_time = current_time
                                self.current_step_index = target_step_index
                            else:
                                self.current_step_index = target_step_index; self.step_complete_time = current_time
                                if self.current_step_index >= len(self.path) - 1: self.is_overall_animating = False
                        else: self.is_overall_animating = False; print("Anim Error: Zero pos not found")
                    else: self.is_overall_animating = False; print("Anim Error: Invalid state in path")
                else: self.is_overall_animating = False; print("Anim Error: Invalid index")

    def _draw_frames(self):
        """Vẽ các khung bao quanh."""
        frame_border_thickness = 1; frame_border_radius = 5
        pg.draw.rect(self.screen, COLOR_BORDER, FRAME_LEFT_RECT, frame_border_thickness, border_radius=frame_border_radius)
        pg.draw.rect(self.screen, COLOR_BORDER, FRAME_CENTER_RECT, frame_border_thickness, border_radius=frame_border_radius)
        pg.draw.rect(self.screen, COLOR_BORDER, FRAME_RIGHT_RECT, frame_border_thickness, border_radius=frame_border_radius)
        if self.path_found and len(self.path) > 1 and self.found_path_type == 'states':
            pg.draw.rect(self.screen, COLOR_BORDER, FRAME_NAV_RECT, frame_border_thickness, border_radius=frame_border_radius)

    def _draw_static_elements(self):
        """Vẽ các thành phần tĩnh."""
        draw_text("8 PUZZLE SOLVER VISUALIZATION", FONT_LARGE, COLOR_TEXT_PRIMARY, self.screen, (SCREEN_WIDTH // 2, TITLE_POS_Y), center_x=True, center_y=True)
        draw_text("Trạng Thái Đầu", FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen, (POS_START_SMALL_X + GRID_SIZE_SMALL // 2, POS_START_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
        draw_8_puzzle(self.screen, self.start_state, POS_START_SMALL_X, POS_START_SMALL_Y, TILE_SIZE_SMALL, TILE_MARGIN_SMALL, FONT_TILE_SMALL)
        draw_text("Trạng Thái Đích", FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen, (POS_GOAL_SMALL_X + GRID_SIZE_SMALL // 2, POS_GOAL_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
        draw_8_puzzle(self.screen, self.goal_state, POS_GOAL_SMALL_X, POS_GOAL_SMALL_Y, TILE_SIZE_SMALL, TILE_MARGIN_SMALL, FONT_TILE_SMALL)

    def _draw_dynamic_elements(self):
        """Vẽ các thành phần động (puzzle lớn, nút, status bar)."""
        path_label_text = "Chọn Thuật Toán"
        if self.is_solving: path_label_text = f"Đang tìm kiếm ({self.selected_algorithm_name})..."
        elif self.path_found:
            if self.found_path_type == 'states':
                is_only_goal = len(self.path) == 1 and change_matran_string(self.path[0]) == change_matran_string(self.goal_state)
                if is_only_goal: path_label_text = f"{self.selected_algorithm_name}: Tìm thấy Goal!"
                elif len(self.path) > 1: path_label_text = f"{self.selected_algorithm_name}: Bước {self.current_step_index + 1} / {len(self.path)}"
                else: path_label_text = f"{self.selected_algorithm_name}: Dừng (Không phải Goal)"
            elif self.found_path_type == 'names': path_label_text = f"Conformant BFS: {len(self.path)} nước đi" # self.path giờ là list tên
        elif self.selected_algorithm_name and not self.is_solving: path_label_text = f"{self.selected_algorithm_name}: Không tìm thấy Goal"
        draw_text(path_label_text, FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen, (POS_PATH_LARGE_X + GRID_SIZE_LARGE // 2, POS_PATH_LARGE_Y - LABEL_OFFSET_Y), center_x=True)

        current_display_state = self.start_state
        if self.path and len(self.path) > 0:
            # Chỉ lấy state từ path nếu type là 'states'
            if self.found_path_type == 'states' and isinstance(self.path[0], list):
                 safe_index = max(0, min(self.current_step_index, len(self.path) - 1))
                 if safe_index < len(self.path) and isinstance(self.path[safe_index], list):
                      current_display_state = self.path[safe_index]
            # Nếu type là 'names', current_display_state đã được đặt là state đầu belief khi xử lý kết quả
            elif self.found_path_type == 'names' and isinstance(self.path[0], list):
                 current_display_state = self.path[0] # Vẫn là state đầu belief set đã lưu

        tile_to_skip_drawing = self.animating_tile_value if self.is_tile_animating and self.found_path_type == 'states' else None
        draw_8_puzzle(self.screen, current_display_state, POS_PATH_LARGE_X, POS_PATH_LARGE_Y, TILE_SIZE_LARGE, TILE_MARGIN_LARGE, FONT_TILE_LARGE, skip_tile_value=tile_to_skip_drawing)

        if self.is_tile_animating and self.found_path_type == 'states' and self.animating_tile_value is not None and self.animating_tile_value > 0:
            pg.draw.rect(self.screen, COLOR_TILE, self.animating_tile_rect, border_radius=PUZZLE_BORDER_RADIUS)
            pg.draw.rect(self.screen, COLOR_TILE_BORDER, self.animating_tile_rect, width=1, border_radius=PUZZLE_BORDER_RADIUS)
            draw_text(str(self.animating_tile_value), FONT_TILE_LARGE, COLOR_TEXT_ON_TILE, self.screen, self.animating_tile_rect.center, center_x=True, center_y=True)

        for button in self.algo_buttons: button.draw(self.screen)
        if self.path_found and len(self.path) > 1 and self.found_path_type == 'states':
            self.nav_buttons["prev"].draw(self.screen)
            self.nav_buttons["next"].draw(self.screen)

        status_rect = pg.Rect(0, STATUS_BAR_Y, SCREEN_WIDTH, STATUS_BAR_HEIGHT)
        pg.draw.rect(self.screen, COLOR_STATUS_BG, status_rect)
        pg.draw.line(self.screen, COLOR_BORDER, (0, STATUS_BAR_Y), (SCREEN_WIDTH, STATUS_BAR_Y), 1)
        display_status_msg = self.status_message
        # Tạm thời bỏ qua hiển thị path tên của Conformant trên status bar
        draw_text(display_status_msg, FONT_MAIN_REGULAR, self.status_color, self.screen, (15, STATUS_BAR_Y + STATUS_BAR_HEIGHT // 2), center_y=True)

    def run(self):
        """Chạy vòng lặp chính của ứng dụng."""
        running = True
        while running:
            current_time = pg.time.get_ticks()
            # --- Xử lý Input ---
            for event in pg.event.get():
                if event.type == pg.QUIT: running = False
                button_clicked_this_frame = False
                for button in self.algo_buttons:
                     if not button.is_disabled:
                         if button.handle_event(event): button_clicked_this_frame = True; break
                # Điều kiện xử lý nav button
                can_handle_nav = (not button_clicked_this_frame and
                                  self.path_found and
                                  self.found_path_type == 'states' and
                                  len(self.path) > 1)
                if can_handle_nav:
                    if not self.nav_buttons["prev"].is_disabled: self.nav_buttons["prev"].handle_event(event)
                    if not self.nav_buttons["next"].is_disabled: self.nav_buttons["next"].handle_event(event)

            # --- Cập nhật Trạng thái ---
            self._process_solver_result()
            self._update_tile_animation(current_time)
            self._update_overall_animation(current_time)

            # --- Vẽ ---
            self.screen.fill(COLOR_BACKGROUND)
            self._draw_frames()
            self._draw_static_elements()
            self._draw_dynamic_elements()
            pg.display.flip()

        pg.quit()
        sys.exit()

# if __name__ == '__main__':
#     app = VisualizationApp()
#     app.run()