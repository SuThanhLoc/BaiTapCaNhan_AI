import pygame as pg
import sys
import random
import threading
import time
import math
import copy

from .constants import *
from .button import Button  # <--- SỬA LỖI: Tách thành hai dòng import riêng biệt
from .drawing import draw_text, find_zero_pos, grid_to_pixel_large, lerp, draw_8_puzzle

from puzzle.state import Start, Goal
from puzzle.state import Tim_0, Check, DiChuyen, change_matran_string, print_matrix
import puzzle.state

if not hasattr(puzzle.state, 'Moves_Dir_Name'):
    puzzle.state.Moves_Dir_Name = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
if not hasattr(puzzle.state, 'Moves_List_Named'):
    puzzle.state.Moves_List_Named = [('U', (-1, 0)), ('D', (1, 0)), ('L', (0, -1)), ('R', (0, 1))]

try:
    from algorithms.bfs import bfs_search
    from algorithms.dfs import dfs_search
    from algorithms.ucs import ucs_search
    from algorithms.iddfs import iddfs_search
    from algorithms.greedy import greedy_search
    from algorithms.a_star import a_star_search
    from algorithms.ida_star import ida_star_search
    from algorithms.hill_climbing import (simple_hill_climbing_first_choice,
                                          steepest_ascent_hill_climbing,
                                          stochastic_hill_climbing)
    from algorithms.simulated_annealing import simulated_annealing_search
    from algorithms.beam_search import beam_search
    from algorithms.genetic_algorithm import genetic_algorithm_search
    from algorithms.conformant_bfs import conformant_bfs_search
    from algorithms.backtracking_search import solve_with_backtracking
    from algorithms.ac3_solver import ac3_for_8_puzzle
    from algorithms.and_or_search import solve_with_and_or_search
    from algorithms.q_learning_solver import run_q_learning_training
    from algorithms.td_learning_solver import run_sarsa_training

    ALGORITHMS_IMPORTED = True
except ImportError as e:
    ALGORITHMS_IMPORTED = False


    def bfs_search(s):
        time.sleep(0.1); return [s, [[2, 6, 5], [4, 0, 7], [8, 3, 1]], Goal]


    def dfs_search(s, md=50):
        time.sleep(0.1); return [s, Goal]


    def ucs_search(s):
        time.sleep(0.1); return [s, Goal]


    def iddfs_search(s, md=50):
        time.sleep(0.2); return []


    def greedy_search(s):
        time.sleep(0.1); return [s, Goal]


    def a_star_search(s):
        time.sleep(0.1); return [s, [[2, 6, 5], [4, 8, 7], [0, 3, 1]], Goal]


    def ida_star_search(s, mt=80):
        time.sleep(0.2); return [s, Goal]


    def simple_hill_climbing_first_choice(s, ms=1000):
        time.sleep(0.1); return [s]


    def steepest_ascent_hill_climbing(s, ms=1000):
        time.sleep(0.1); return [s]


    def stochastic_hill_climbing(s, ms=1000):
        time.sleep(0.1); return [s, Goal]


    def simulated_annealing_search(s, it=100, cr=0.95, mt=0.1, mi=5000):
        time.sleep(0.1); return [s]


    def beam_search(s, bw=5, mi=1000):
        time.sleep(0.1); return [s, Goal]


    def genetic_algorithm_search(s, g, ps=100, gen=100, mr=0.1):
        time.sleep(0.1); return [g] if random.random() < 0.5 else []


    def conformant_bfs_search(bl, g):
        time.sleep(0.2); return ['R', 'U'] if random.random() < 0.5 else None


    def solve_with_backtracking(s, g=Goal, md=30):
        time.sleep(0.1); return [s, g]


    def ac3_for_8_puzzle(s):
        time.sleep(0.1); return {"type": "ac3_result", "is_consistent": True, "final_puzzle_state": s}


    def solve_with_and_or_search(s):
        time.sleep(0.1); return {"type": "and_or_result", "path": [s, Goal]}


    def run_q_learning_training(s, g=Goal, ep=10, ms=10):
        time.sleep(0.1); return {"type": "q_learning_result", "agent": None, "rewards_log": []}


    def run_sarsa_training(s, g=Goal, ep=10, ms=10):
        time.sleep(0.1); return {"type": "sarsa_result", "agent": None, "rewards_log": []}

solver_thread = None
solver_result = None


def run_solver(algorithm_func, start_input, algo_name, result_container_ref, goal_input=Goal):
    global solver_result
    try:
        start_time = time.time()
        path_result = None

        if algo_name == "Conformant BFS":
            path_result = algorithm_func(start_input, goal_input)
        elif algo_name == "IDDFS":
            path_result = algorithm_func(start_input, max_depth=30)
        elif algo_name == "IDA*":
            path_result = algorithm_func(start_input, max_threshold=80)
        elif algo_name in ["Simple HC", "Steepest HC", "Stochastic HC"]:
            path_result = algorithm_func(start_input, max_steps=2000)
        elif algo_name == "Sim Anneal":
            path_result = algorithm_func(start_input, initial_temp=100, cooling_rate=0.97, min_temp=0.1,
                                         max_iterations=15000)
        elif algo_name == "Beam Search":
            path_result = algorithm_func(start_input, beam_width=5, max_iterations=1000)
        elif algo_name == "Genetic Algo":
            path_result = algorithm_func(start_input, goal_input, population_size=100, generations=200,
                                         mutation_rate=0.2)
        elif algo_name == "Backtracking":
            path_result = algorithm_func(start_input, goal_input, max_depth_bt=30)
        elif algo_name == "AC-3 Solver":
            path_result = algorithm_func(start_input)
        elif algo_name == "AND-OR Search":
            path_result = algorithm_func(start_input)
        elif algo_name == "Q-Learning":
            path_result = algorithm_func(start_input, goal_input, episodes=1000, max_steps_per_episode=100)
        elif algo_name == "TD (SARSA)":
            path_result = algorithm_func(start_input, goal_input, episodes=1000, max_steps_per_episode=100)
        else:
            path_result = algorithm_func(start_input)

        end_time = time.time()
        solve_time = end_time - start_time
        solver_result = {"result_data": path_result, "error": None, "time": solve_time, "algo": algo_name}

    except Exception as e:
        import traceback
        solver_result = {"result_data": None, "error": str(e), "time": 0, "algo": algo_name}


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

        self.trained_rl_agent = None
        self.ac3_display_state = None

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
            "Conformant BFS": conformant_bfs_search,
            "Backtracking": solve_with_backtracking,
            "AC-3 Solver": ac3_for_8_puzzle,
            "AND-OR Search": solve_with_and_or_search,
            "Q-Learning": run_q_learning_training,
            "TD (SARSA)": run_sarsa_training
        } if ALGORITHMS_IMPORTED else {}

    def _create_algo_buttons(self):
        buttons = []
        y_offset = 0
        max_buttons_per_col = 10 # Giữ nguyên từ code gốc của bạn
        # Điều chỉnh current_col_x và col_width_offset nếu bạn có nhiều hơn 2 cột
        # current_col_x = ALGO_BUTTON_X 
        # col_width_offset = ALGO_BUTTON_WIDTH + 15

        # Tính toán cho nhiều cột (ví dụ 2 cột nếu số lượng button > max_buttons_per_col)
        num_algo_buttons = len(ALGORITHMS_TO_DISPLAY)
        num_cols = (num_algo_buttons + max_buttons_per_col -1) // max_buttons_per_col

        # Tính toán X bắt đầu cho cột đầu tiên để căn giữa cụm button nếu có nhiều cột
        total_button_block_width = num_cols * ALGO_BUTTON_WIDTH + max(0, num_cols - 1) * 15 # 15 là khoảng cách giữa các cột
        # BUTTON_COLUMN_START_X_ANCHOR = RIGHT_PANEL_START_X + (RIGHT_PANEL_WIDTH - total_button_block_width) // 2
        
        # Sử dụng ALGO_BUTTON_X như cũ nếu bạn chỉ muốn căn giữa một cột đơn
        current_col_x_start = ALGO_BUTTON_X 


        col_idx = 0
        current_col_x = current_col_x_start

        for i, algo_name_display in enumerate(ALGORITHMS_TO_DISPLAY):
            if i > 0 and i % max_buttons_per_col == 0:
                y_offset = 0
                col_idx +=1
                current_col_x = current_col_x_start + col_idx * (ALGO_BUTTON_WIDTH + 15)


            btn_y = BUTTON_COLUMN_START_Y + y_offset * (ALGO_BUTTON_HEIGHT + BUTTON_GAP_Y)
            
            # Không cần gán button_color nữa nếu không dùng cho nền
            # is_belief = (algo_name_display == "Conformant BFS")
            # is_rl = algo_name_display in ["Q-Learning", "TD (SARSA)"]
            # is_other_special = algo_name_display in ["AC-3 Solver", "AND-OR Search"]

            # button_color = COLOR_BUTTON # Mặc định
            # if is_belief: button_color = COLOR_BUTTON_BELIEF
            # elif is_rl: button_color = pg.Color("#FFC107")
            # elif is_other_special: button_color = pg.Color("#607D8B")

            button = Button(current_col_x, btn_y, ALGO_BUTTON_WIDTH, ALGO_BUTTON_HEIGHT, algo_name_display,
                            callback=self.handle_algo_button_click)
                            # Loại bỏ: base_color=button_color
            buttons.append(button)
            y_offset += 1
        return buttons

    def _create_nav_buttons(self):
        buttons = {
            "prev": Button(POS_PREV_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Lùi",
                           callback=self.nav_button_click),
                           # Loại bỏ: base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER
            "next": Button(POS_NEXT_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Tiến",
                           callback=self.nav_button_click)
                           # Loại bỏ: base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER
        }
        return buttons
    
    def _update_nav_button_state(self):
        can_navigate_path = self.path_found and self.found_path_type == 'states' and isinstance(self.path,
                                                                                                list) and len(
            self.path) > 1
        self.nav_buttons["prev"].is_disabled = not can_navigate_path
        self.nav_buttons["next"].is_disabled = not can_navigate_path

        if self.found_path_type in ['q_learning_result', 'sarsa_result', 'ac3_result', 'and_or_result_no_path_vis']:
            self.nav_buttons["prev"].is_disabled = True
            self.nav_buttons["next"].is_disabled = True

    def handle_algo_button_click(self, algo_name_clicked):
        global solver_result
        if self.is_solving: return
        self.selected_algorithm_name = algo_name_clicked
        self.is_solving = True;
        solver_result = None;
        self.path = [];
        self.path_found = False;
        self.found_path_type = None
        self.current_step_index = 0;
        self.is_overall_animating = False;
        self.is_tile_animating = False
        self.trained_rl_agent = None;
        self.ac3_display_state = None
        self.status_message = f"Đang xử lý bằng {self.selected_algorithm_name}...";
        self.status_color = COLOR_TEXT_ACCENT
        for btn in self.algo_buttons: btn.is_selected = (
                    btn.text == self.selected_algorithm_name); btn.is_disabled = True
        self._update_nav_button_state()

        algo_func = self.algorithms_map.get(self.selected_algorithm_name)
        start_input_arg = None
        goal_input_arg = copy.deepcopy(self.goal_state)

        if self.selected_algorithm_name == "Conformant BFS":
            start_input_arg = copy.deepcopy(self.sample_initial_belief_state)
            if start_input_arg:
                self.path = [start_input_arg[0]]
            else:
                self.path = [copy.deepcopy(self.start_state)]
        else:
            start_input_arg = copy.deepcopy(self.start_state)
            self.path = [start_input_arg]

        if algo_func and start_input_arg is not None:
            self.solver_thread = threading.Thread(target=run_solver,
                                                  args=(algo_func, start_input_arg, self.selected_algorithm_name,
                                                        solver_result, goal_input_arg),
                                                  daemon=True)
            self.solver_thread.start()
        else:
            errmsg = "không tìm thấy hàm" if not algo_func else "đầu vào không hợp lệ"
            self.status_message = f"Lỗi: Không chạy được {self.selected_algorithm_name} ({errmsg})";
            self.status_color = COLOR_TEXT_ERROR
            self.is_solving = False;
            for btn in self.algo_buttons: btn.is_disabled = False; btn.is_selected = False
            self._update_nav_button_state()
            self.path = [copy.deepcopy(self.start_state)]

    def nav_button_click(self, direction):
        if not self.path_found or not isinstance(self.path,
                                                 list) or not self.path or self.is_tile_animating or self.found_path_type != 'states':
            return

        self.is_overall_animating = False
        prev_index = self.current_step_index
        if direction == "Lùi":
            self.current_step_index = max(0, self.current_step_index - 1)
        elif direction == "Tiến":
            self.current_step_index = min(len(self.path) - 1, self.current_step_index + 1)

        if prev_index != self.current_step_index:
            self.step_complete_time = pg.time.get_ticks()

    def _process_solver_result(self):
        global solver_result
        if not self.is_solving or not self.solver_thread or self.solver_thread.is_alive():
            return

        self.is_solving = False
        local_solver_result_dict = solver_result
        solver_result = None

        algo_name_from_result = "Unknown"
        self.path_found = False
        self.found_path_type = None
        self.path = [copy.deepcopy(self.start_state)]
        self.ac3_display_state = None
        self.trained_rl_agent = None

        if local_solver_result_dict:
            algo_name_from_result = local_solver_result_dict.get("algo", "Unknown")
            solve_time = local_solver_result_dict.get('time', 0)
            raw_result_data = local_solver_result_dict.get("result_data")
            error_msg = local_solver_result_dict.get("error")

            if error_msg:
                self.status_message = f"Lỗi ({algo_name_from_result}): {error_msg}"
                self.status_color = COLOR_TEXT_ERROR
            elif raw_result_data is not None:
                result_type = raw_result_data.get("type") if isinstance(raw_result_data, dict) else None

                if algo_name_from_result == "Conformant BFS":
                    if isinstance(raw_result_data, list):
                        if raw_result_data:
                            self.path = raw_result_data
                            self.path_found = True
                            self.found_path_type = 'names'
                            move_count = len(self.path)
                            self.status_message = f"Conformant BFS: Tìm thấy {move_count} nước đi trong {solve_time:.3f}s"
                            self.status_color = COLOR_TEXT_SUCCESS
                        else:
                            self.status_message = f"Conformant BFS: Không tìm thấy đường đi."
                            self.status_color = COLOR_TEXT_SECONDARY
                        self.path_for_display = [copy.deepcopy(
                            self.sample_initial_belief_state[0])] if self.sample_initial_belief_state else [
                            copy.deepcopy(self.start_state)]
                        self.path = self.path_for_display
                    else:
                        self.status_message = f"Conformant BFS: Kết quả không hợp lệ."
                        self.status_color = COLOR_TEXT_ERROR
                        self.path = [copy.deepcopy(
                            self.sample_initial_belief_state[0])] if self.sample_initial_belief_state else [
                            copy.deepcopy(self.start_state)]

                elif result_type == "ac3_result":
                    self.found_path_type = 'ac3_result'
                    self.path_found = True
                    is_consistent = raw_result_data.get("is_consistent")
                    self.ac3_display_state = raw_result_data.get("final_puzzle_state")
                    self.path = [self.ac3_display_state] if self.ac3_display_state else [self.start_state]
                    consistency_msg = "Nhất quán" if is_consistent else "Không nhất quán"
                    self.status_message = f"AC-3: {consistency_msg} trong {solve_time:.3f}s. Hiển thị kết quả."
                    self.status_color = COLOR_TEXT_SUCCESS if is_consistent else COLOR_TEXT_ERROR

                elif result_type == "and_or_result":
                    self.found_path_type = 'and_or_result'
                    ao_path = raw_result_data.get("path")
                    if ao_path and isinstance(ao_path, list) and len(ao_path) > 0:
                        self.path = ao_path
                        self.path_found = True
                        self.found_path_type = 'states'
                        self.is_overall_animating = len(self.path) > 1
                        self.step_complete_time = pg.time.get_ticks() if self.is_overall_animating else 0
                        self.status_message = f"AND-OR: Tìm thấy đường đi ({len(self.path)} bước) trong {solve_time:.3f}s."
                        self.status_color = COLOR_TEXT_SUCCESS
                    else:
                        self.status_message = f"AND-OR: Không tìm thấy đường đi trong {solve_time:.3f}s."
                        self.status_color = COLOR_TEXT_SECONDARY
                        self.path = [copy.deepcopy(self.start_state)]


                elif result_type in ["q_learning_result", "sarsa_result"]:
                    self.found_path_type = result_type
                    self.path_found = True
                    self.trained_rl_agent = raw_result_data.get("agent")
                    self.path = [copy.deepcopy(self.start_state)]
                    algo_display_name = "Q-Learning" if result_type == "q_learning_result" else "TD (SARSA)"
                    self.status_message = f"{algo_display_name}: Huấn luyện xong trong {solve_time:.3f}s. Sẵn sàng để thử nghiệm."
                    self.status_color = COLOR_TEXT_SUCCESS

                else:
                    temp_path = raw_result_data
                    is_list_of_states = isinstance(temp_path, list) and \
                                        (len(temp_path) == 0 or (len(temp_path) > 0 and isinstance(temp_path[0], list)))

                    is_valid_path_structure = False
                    if is_list_of_states and len(temp_path) > 0:
                        is_valid_path_structure = all(
                            len(step) == 3 and all(isinstance(row, list) and len(row) == 3 for row in step) for step in
                            temp_path)

                    if is_valid_path_structure:
                        self.path = temp_path
                        self.path_found = True
                        self.found_path_type = 'states'
                        self.current_step_index = 0
                        goal_str_check = change_matran_string(self.goal_state)
                        is_only_goal = len(self.path) == 1 and change_matran_string(self.path[0]) == goal_str_check

                        if is_only_goal:
                            self.is_overall_animating = False
                            self.status_message = f"{algo_name_from_result}: Tìm thấy Goal State trong {solve_time:.3f}s."
                            self.status_color = COLOR_TEXT_SUCCESS
                        elif len(self.path) > 1:
                            self.is_overall_animating = True
                            self.step_complete_time = pg.time.get_ticks()
                            self.status_message = f"{algo_name_from_result}: Tìm thấy ({len(self.path)} bước) trong {solve_time:.3f}s."
                            self.status_color = COLOR_TEXT_SUCCESS
                        else:
                            self.is_overall_animating = False
                            if len(self.path) == 1 and change_matran_string(self.path[0]) != goal_str_check:
                                self.status_message = f"{algo_name_from_result}: Dừng (không phải Goal) trong {solve_time:.3f}s."
                            elif len(self.path) == 1 and change_matran_string(self.path[0]) == goal_str_check:
                                self.status_message = f"{algo_name_from_result}: Tìm thấy Goal State trong {solve_time:.3f}s."
                                self.status_color = COLOR_TEXT_SUCCESS
                            else:
                                self.status_message = f"{algo_name_from_result}: Kết quả không rõ ràng."
                            self.status_color = COLOR_TEXT_SECONDARY
                    elif isinstance(temp_path, list) and len(temp_path) == 0:
                        self.status_message = f"{algo_name_from_result}: Không tìm thấy đường đi.";
                        if solve_time > 0: self.status_message += f" (Tìm kiếm {solve_time:.3f}s)"
                        self.status_color = COLOR_TEXT_SECONDARY
                        self.path = [copy.deepcopy(self.start_state)]
                    else:
                        self.status_message = f"Lỗi: Kết quả từ {algo_name_from_result} không hợp lệ.";
                        self.status_color = COLOR_TEXT_ERROR
                        self.path = [copy.deepcopy(self.start_state)]
            else:
                self.status_message = f"Lỗi Solver: Không nhận được kết quả từ {algo_name_from_result}."
                self.status_color = COLOR_TEXT_ERROR
                self.path = [copy.deepcopy(self.start_state)]
        else:
            self.status_message = "Lỗi Solver: Kết quả không xác định.";
            self.status_color = COLOR_TEXT_ERROR
            self.path = [copy.deepcopy(self.start_state)]

        for btn in self.algo_buttons:
            btn.is_disabled = False
            btn.is_selected = (btn.text == algo_name_from_result)
        self._update_nav_button_state()

    def _update_tile_animation(self, current_time):
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
        if (self.is_overall_animating and self.path_found and
                not self.is_tile_animating and self.found_path_type == 'states' and
                isinstance(self.path, list) and self.current_step_index < len(self.path) - 1):
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
                                self.is_overall_animating = False;
                                self.animating_tile_value = None;
                                return
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
                                self.current_step_index = target_step_index;
                                self.step_complete_time = current_time
                                if self.current_step_index >= len(self.path) - 1: self.is_overall_animating = False
                        else:
                            self.is_overall_animating = False
                    else:
                        self.is_overall_animating = False
                else:
                    self.is_overall_animating = False

    def _draw_frames(self):
        frame_border_thickness = 1;
        frame_border_radius = 5
        pg.draw.rect(self.screen, COLOR_BORDER, FRAME_LEFT_RECT, frame_border_thickness,
                     border_radius=frame_border_radius)
        pg.draw.rect(self.screen, COLOR_BORDER, FRAME_CENTER_RECT, frame_border_thickness,
                     border_radius=frame_border_radius)
        # pg.draw.rect(self.screen, COLOR_BORDER, FRAME_RIGHT_RECT, frame_border_thickness,
        #              border_radius=frame_border_radius)

        can_navigate_path = self.path_found and self.found_path_type == 'states' and isinstance(self.path,
                                                                                                list) and len(
            self.path) > 1
        if can_navigate_path:
            # pg.draw.rect(self.screen, COLOR_BORDER, FRAME_NAV_RECT, frame_border_thickness,
            #              border_radius=frame_border_radius)
            pass

    def _draw_static_elements(self):
        draw_text("8 PUZZLE SOLVER VISUALIZATION", FONT_LARGE, COLOR_TEXT_PRIMARY, self.screen,
                  (SCREEN_WIDTH // 2, TITLE_POS_Y), center_x=True, center_y=True)
        draw_text("Trạng Thái Đầu", FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen,
                  (POS_START_SMALL_X + GRID_SIZE_SMALL // 2, POS_START_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
        draw_8_puzzle(self.screen, self.start_state, POS_START_SMALL_X, POS_START_SMALL_Y, TILE_SIZE_SMALL,
                      TILE_MARGIN_SMALL, FONT_TILE_SMALL)
        draw_text("Trạng Thái Đích", FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen,
                  (POS_GOAL_SMALL_X + GRID_SIZE_SMALL // 2, POS_GOAL_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
        draw_8_puzzle(self.screen, self.goal_state, POS_GOAL_SMALL_X, POS_GOAL_SMALL_Y, TILE_SIZE_SMALL,
                      TILE_MARGIN_SMALL, FONT_TILE_SMALL)

    def _draw_dynamic_elements(self):
        path_label_text = "Chọn Thuật Toán"
        if self.is_solving:
            path_label_text = f"Đang xử lý ({self.selected_algorithm_name})..."
        elif self.path_found:
            if self.found_path_type == 'states':
                is_only_goal = len(self.path) == 1 and change_matran_string(self.path[0]) == change_matran_string(
                    self.goal_state)
                if is_only_goal:
                    path_label_text = f"{self.selected_algorithm_name}: Tìm thấy Goal!"
                elif len(self.path) > 1:
                    path_label_text = f"{self.selected_algorithm_name}: Bước {self.current_step_index + 1} / {len(self.path)}"
                else:
                    path_label_text = f"{self.selected_algorithm_name}: Dừng (Không phải Goal)"
            elif self.found_path_type == 'names':
                path_label_text = f"Conformant BFS: {len(self.path)} nước đi"
            elif self.found_path_type == 'ac3_result':
                path_label_text = f"AC-3: Kết quả xử lý ràng buộc"
            elif self.found_path_type in ['q_learning_result', 'sarsa_result']:
                path_label_text = f"{self.selected_algorithm_name}: Huấn luyện xong"
            elif self.found_path_type == 'and_or_result':
                path_label_text = f"AND-OR: Kết quả (kiểm tra console)"


        elif self.selected_algorithm_name and not self.is_solving:
            path_label_text = f"{self.selected_algorithm_name}: Không tìm thấy/Không có kết quả"
        draw_text(path_label_text, FONT_MEDIUM, COLOR_TEXT_SECONDARY, self.screen,
                  (POS_PATH_LARGE_X + GRID_SIZE_LARGE // 2, POS_PATH_LARGE_Y - LABEL_OFFSET_Y), center_x=True)

        current_display_state = self.start_state
        if self.path and len(self.path) > 0 and isinstance(self.path[0], list):
            if self.found_path_type == 'states' or (
                    self.found_path_type == 'and_or_result' and isinstance(self.path[0], list)):
                safe_index = max(0, min(self.current_step_index, len(self.path) - 1))
                if safe_index < len(self.path) and isinstance(self.path[safe_index], list):
                    current_display_state = self.path[safe_index]
            elif self.found_path_type == 'names' and isinstance(self.path[0], list):
                current_display_state = self.path[0]
            elif self.found_path_type == 'ac3_result' and self.ac3_display_state:
                current_display_state = self.ac3_display_state
            elif self.found_path_type in ['q_learning_result', 'sarsa_result'] and isinstance(self.path[0], list):
                current_display_state = self.path[0]

        tile_to_skip_drawing = self.animating_tile_value if self.is_tile_animating and self.found_path_type == 'states' else None
        draw_8_puzzle(self.screen, current_display_state, POS_PATH_LARGE_X, POS_PATH_LARGE_Y, TILE_SIZE_LARGE,
                      TILE_MARGIN_LARGE, FONT_TILE_LARGE, skip_tile_value=tile_to_skip_drawing)

        if self.is_tile_animating and self.found_path_type == 'states' and self.animating_tile_value is not None and self.animating_tile_value > 0:
            pg.draw.rect(self.screen, COLOR_TILE, self.animating_tile_rect, border_radius=PUZZLE_BORDER_RADIUS)
            pg.draw.rect(self.screen, COLOR_TILE_BORDER, self.animating_tile_rect, width=1,
                         border_radius=PUZZLE_BORDER_RADIUS)
            draw_text(str(self.animating_tile_value), FONT_TILE_LARGE, COLOR_TEXT_ON_TILE, self.screen,
                      self.animating_tile_rect.center, center_x=True, center_y=True)

        for button in self.algo_buttons: button.draw(self.screen)

        can_navigate_path = self.path_found and self.found_path_type == 'states' and isinstance(self.path,
                                                                                                list) and len(
            self.path) > 1
        if can_navigate_path:
            self.nav_buttons["prev"].draw(self.screen)
            self.nav_buttons["next"].draw(self.screen)

        status_rect = pg.Rect(0, STATUS_BAR_Y, SCREEN_WIDTH, STATUS_BAR_HEIGHT)
        pg.draw.rect(self.screen, COLOR_STATUS_BG, status_rect)
        pg.draw.line(self.screen, COLOR_BORDER, (0, STATUS_BAR_Y), (SCREEN_WIDTH, STATUS_BAR_Y), 1)
        display_status_msg = self.status_message
        draw_text(display_status_msg, FONT_MAIN_REGULAR, self.status_color, self.screen,
                  (15, STATUS_BAR_Y + STATUS_BAR_HEIGHT // 2), center_y=True)

    def handle_puzzle_click(self, mouse_pos):
        if self.found_path_type in ['q_learning_result', 'sarsa_result'] and self.trained_rl_agent:
            puzzle_rect = pg.Rect(POS_PATH_LARGE_X, POS_PATH_LARGE_Y, GRID_SIZE_LARGE, GRID_SIZE_LARGE)
            if puzzle_rect.collidepoint(mouse_pos):
                current_puzzle_state_for_rl = self.path[0]

                action_idx = self.trained_rl_agent.choose_action(current_puzzle_state_for_rl, use_exploration=False)

                if action_idx is not None:
                    _, (dx, dy) = self.trained_rl_agent.actions_map_idx_to_named_move[action_idx]
                    x0, y0 = Tim_0(current_puzzle_state_for_rl)
                    if x0 != -1:
                        next_s_matrix = DiChuyen(current_puzzle_state_for_rl, x0, y0, x0 + dx, y0 + dy)
                        if next_s_matrix:
                            self.path = [next_s_matrix]
                            self.status_message = f"RL Agent moved. New state shown."
                            self.status_color = COLOR_TEXT_ACCENT
                        else:
                            self.status_message = "RL Agent: Invalid move suggested by policy."
                            self.status_color = COLOR_TEXT_ERROR
                else:
                    self.status_message = "RL Agent: No action chosen."
                    self.status_color = COLOR_TEXT_SECONDARY

    def run(self):
        running = True
        while running:
            current_time = pg.time.get_ticks()
            mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT: running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_puzzle_click(mouse_pos)

                button_clicked_this_frame = False
                for button in self.algo_buttons:
                    if not button.is_disabled:
                        if button.handle_event(event): button_clicked_this_frame = True; break

                can_handle_nav = (not button_clicked_this_frame and
                                  self.path_found and
                                  self.found_path_type == 'states' and
                                  isinstance(self.path, list) and len(self.path) > 1)
                if can_handle_nav:
                    if not self.nav_buttons["prev"].is_disabled: self.nav_buttons["prev"].handle_event(event)
                    if not self.nav_buttons["next"].is_disabled: self.nav_buttons["next"].handle_event(event)

            self._process_solver_result()
            self._update_tile_animation(current_time)
            self._update_overall_animation(current_time)

            self.screen.fill(COLOR_BACKGROUND)
            self._draw_frames()
            self._draw_static_elements()
            self._draw_dynamic_elements()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
        sys.exit()