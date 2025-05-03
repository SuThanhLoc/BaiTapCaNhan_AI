# -*- coding: utf-8 -*- # Thêm encoding để hỗ trợ tiếng Việt
import pygame as pg
import sys
import random
import threading
import time
import math # Thêm math để dùng ceil
import copy # Needed for deepcopy

# --- Import và Fallback ---
try:
    # Thêm conformant_bfs vào import
    from ThuatToan import (Start, Goal, BFS, DFS, UCS, IDDFS, Greedy,
                           A_Star, IDA, Simple_Hill_Climbing_First_Choice,
                           Steepest_Ascent_Hill_Climbing, Stochastic_Hill_Climbing,
                           Simulated_Annealing, Beam_Search, Genetic_Algorithm,
                           conformant_bfs) # <--- Thêm conformant_bfs
    print("ThuatToan.py loaded successfully with all algorithms including Conformant BFS.")
except ImportError:
    print("Lỗi: Không tìm thấy file ThuatToan.py hoặc các hàm/biến cần thiết.")
    print("Sử dụng các hàm và trạng thái giả lập.")
    # Trạng thái giả lập
    Start = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    Goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    # Các hàm fallback (Thêm fallback cho conformant_bfs)
    def DFS(s): time.sleep(0.1); return [s, [[2,6,5],[4,0,7],[8,3,1]], Goal]
    def BFS(s): time.sleep(0.1); return [s, [[2,6,5],[4,0,7],[8,3,1]], Goal]
    def UCS(s): time.sleep(0.1); return [s, Goal]
    def IDDFS(s, md=50): time.sleep(0.2); return []
    def Greedy(s): time.sleep(0.1); return [s, Goal]
    def A_Star(s): time.sleep(0.1); return [s, [[2,6,5],[4,8,7],[0,3,1]], [[2,6,5],[4,8,7],[3,0,1]], Goal]
    def IDA(s, d=15): time.sleep(0.2); return [s, Goal]
    def Simple_Hill_Climbing_First_Choice(s, max_steps=1000): time.sleep(0.1); return [s, [[2,6,5],[4,0,7],[8,3,1]]]
    def Steepest_Ascent_Hill_Climbing(s, max_steps=1000): time.sleep(0.1); return [s]
    def Stochastic_Hill_Climbing(s, max_steps=1000): time.sleep(0.1); return [s, [[2,0,5],[6,8,7],[4,3,1]], Goal]
    def Simulated_Annealing(s, initial_temp=100, cooling_rate=0.95, min_temp=0.1, max_iterations=5000):
        print("Fallback: Simulated Annealing"); time.sleep(0.1)
        if random.random() < 0.7: return [s, [[2,6,5],[4,0,7],[8,3,1]], [[2,0,5],[4,6,7],[8,3,1]], Goal]
        else: return [s, [[2,6,5],[4,0,7],[8,3,1]]]
    def Beam_Search(s, beam_width=5, max_iterations=1000):
        print("Fallback: Beam Search"); time.sleep(0.1)
        return [s, [[2,6,5],[4,0,7],[8,3,1]], Goal]
    def Genetic_Algorithm(s, g, population_size=100, generations=100, mutation_rate=0.1):
         print("Fallback: Genetic Algorithm"); time.sleep(0.1)
         if random.random() < 0.5: return [g] # Trả về [Goal] nếu "thành công"
         else: return [] # Trả về [] nếu "thất bại"
    # Fallback cho Conformant BFS
    def conformant_bfs(belief_list, g):
         print("Fallback: Conformant BFS"); time.sleep(0.2)
         # Trả về list tên nước đi hoặc None
         if random.random() < 0.6: return ['R', 'U', 'L', 'L', 'D']
         else: return None


# --- Constants ---
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800 # Tăng chiều cao để chứa nút mới
WINDOW_TITLE = "8 Puzzle Solver Visualization - 23110371"

# --- Colors ---
# (Giữ nguyên Colors)
COLOR_BACKGROUND = pg.Color("#343A40")
COLOR_TILE = pg.Color("#007BFF")
COLOR_TILE_BORDER = pg.Color("#6C757D")
COLOR_EMPTY_TILE = pg.Color("#495057")
COLOR_TEXT_ON_TILE = pg.Color("#FFFFFF")
COLOR_TEXT_PRIMARY = pg.Color("#F8F9FA")
COLOR_TEXT_SECONDARY = pg.Color("#ADB5BD")
COLOR_TEXT_ACCENT = pg.Color("#0D6EFD")
COLOR_TEXT_ERROR = pg.Color("#DC3545")
COLOR_TEXT_SUCCESS = pg.Color("#198754")
COLOR_BUTTON = pg.Color("#495057")
COLOR_BUTTON_HOVER = pg.Color("#6C757D")
COLOR_BUTTON_SELECTED = pg.Color("#0D6EFD") # Giữ màu xanh cho selected
COLOR_BUTTON_BELIEF = pg.Color("#FD7E14") # Màu cam cho nút Belief
COLOR_BUTTON_BELIEF_HOVER = pg.Color("#FF9A3C")
COLOR_BUTTON_BELIEF_SELECTED = pg.Color("#E8590C") # Màu cam đậm hơn cho selected
COLOR_BUTTON_DISABLED = pg.Color("#212529")
COLOR_BUTTON_TEXT = pg.Color("#F8F9FA")
COLOR_NAV_BUTTON = pg.Color("#198754")
COLOR_NAV_BUTTON_HOVER = pg.Color("#20A060")
COLOR_BORDER = pg.Color("#6C757D")
COLOR_STATUS_BG = pg.Color("#212529")

# --- Fonts ---
# (Giữ nguyên Fonts)
pg.font.init()
try:
    FONT_MAIN_REGULAR = pg.font.SysFont("Segoe UI", 14)
    FONT_MAIN_BOLD = pg.font.SysFont("Segoe UI", 14, bold=True)
    FONT_MEDIUM = pg.font.SysFont("Segoe UI Semibold", 20)
    FONT_LARGE = pg.font.SysFont("Segoe UI", 36, bold=True)
    FONT_TILE_SMALL = pg.font.SysFont("Arial", 24, bold=True)
    FONT_TILE_LARGE = pg.font.SysFont("Arial", 50, bold=True)
except Exception as e:
    print(f"Font loading error: {e}. Using fallback.")
    FONT_MAIN_REGULAR = pg.font.Font(None, 20)
    FONT_MAIN_BOLD = pg.font.Font(None, 20)
    FONT_MEDIUM = pg.font.Font(None, 24)
    FONT_LARGE = pg.font.Font(None, 48)
    FONT_TILE_SMALL = pg.font.Font(None, 30)
    FONT_TILE_LARGE = pg.font.Font(None, 70)

# --- Layout & Size Constants ---
# (Giữ nguyên Layout & Size Constants)
TILE_SIZE_SMALL = 55; TILE_MARGIN_SMALL = 4
GRID_SIZE_SMALL = 3 * TILE_SIZE_SMALL + 2 * TILE_MARGIN_SMALL
TILE_SIZE_LARGE = 120; TILE_MARGIN_LARGE = 8
GRID_SIZE_LARGE = 3 * TILE_SIZE_LARGE + 2 * TILE_MARGIN_LARGE
PUZZLE_BORDER_RADIUS = 8; BUTTON_BORDER_RADIUS = 8
TOP_MARGIN = 20; TITLE_GAP_Y = 15; SECTION_GAP_Y = 30; LABEL_OFFSET_Y = 35
FRAME_PADDING = 10

# --- Vị trí các thành phần ---
# (Giữ nguyên cách tính toán vị trí)
TITLE_POS_Y = TOP_MARGIN + FONT_LARGE.get_height() // 2
LEFT_PANEL_MARGIN = 40
RIGHT_PANEL_MARGIN = 40
POS_START_SMALL_X = LEFT_PANEL_MARGIN; POS_GOAL_SMALL_X = LEFT_PANEL_MARGIN
LEFT_PANEL_START_Y = TITLE_POS_Y + FONT_LARGE.get_height() // 2 + TITLE_GAP_Y
POS_START_SMALL_Y = LEFT_PANEL_START_Y + LABEL_OFFSET_Y
POS_GOAL_SMALL_Y = POS_START_SMALL_Y + GRID_SIZE_SMALL + SECTION_GAP_Y + LABEL_OFFSET_Y
POS_PATH_LARGE_X = LEFT_PANEL_MARGIN + GRID_SIZE_SMALL + SECTION_GAP_Y
POS_PATH_LARGE_Y = LEFT_PANEL_START_Y + LABEL_OFFSET_Y
ALGO_BUTTON_WIDTH = 110
ALGO_BUTTON_HEIGHT = 35
BUTTON_GAP_Y = 10
RIGHT_PANEL_START_X = POS_PATH_LARGE_X + GRID_SIZE_LARGE + SECTION_GAP_Y
RIGHT_PANEL_WIDTH = SCREEN_WIDTH - RIGHT_PANEL_START_X - RIGHT_PANEL_MARGIN
BUTTON_COLUMN_CENTER_X = RIGHT_PANEL_START_X + RIGHT_PANEL_WIDTH // 2
ALGO_BUTTON_X = BUTTON_COLUMN_CENTER_X - ALGO_BUTTON_WIDTH // 2
BUTTON_COLUMN_START_Y = POS_PATH_LARGE_Y
NAV_BUTTON_WIDTH = 100
NAV_BUTTON_HEIGHT = 40
NAV_BUTTON_GAP_X = 30
PUZZLE_CENTER_X = POS_PATH_LARGE_X + GRID_SIZE_LARGE // 2
TOTAL_NAV_WIDTH = NAV_BUTTON_WIDTH * 2 + NAV_BUTTON_GAP_X
POS_PREV_X = PUZZLE_CENTER_X - TOTAL_NAV_WIDTH // 2
POS_NEXT_X = POS_PREV_X + NAV_BUTTON_WIDTH + NAV_BUTTON_GAP_X
NAV_BUTTON_Y = POS_PATH_LARGE_Y + GRID_SIZE_LARGE + SECTION_GAP_Y
STATUS_BAR_HEIGHT = 40
STATUS_BAR_Y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT

# --- Danh sách thuật toán cho UI ---
# *** Thêm "Conformant BFS" vào danh sách hiển thị ***
algorithms_to_display = [
    "DFS", "BFS", "UCS", "Greedy", "A*", "IDDFS",
    "IDA*", "Simple HC", "Steepest HC", "Stochastic HC",
    "Sim Anneal", "Beam Search", "Genetic Algo",
    "Conformant BFS" # <--- Thêm vào đây
]
num_algo_buttons = len(algorithms_to_display) # Tự động cập nhật số lượng nút

# --- Tính toán Rect cho các Khung ---
# (Các tính toán khung sẽ tự động điều chỉnh theo num_algo_buttons mới)
frame_left_top = POS_START_SMALL_Y - LABEL_OFFSET_Y - FRAME_PADDING
frame_left_bottom = POS_GOAL_SMALL_Y + GRID_SIZE_SMALL + FRAME_PADDING
frame_left_height = frame_left_bottom - frame_left_top
frame_left_rect = pg.Rect(LEFT_PANEL_MARGIN - FRAME_PADDING, frame_left_top, GRID_SIZE_SMALL + 2 * FRAME_PADDING, frame_left_height)
frame_center_top = POS_PATH_LARGE_Y - LABEL_OFFSET_Y - FRAME_PADDING
frame_center_bottom = POS_PATH_LARGE_Y + GRID_SIZE_LARGE + FRAME_PADDING
frame_center_height = frame_center_bottom - frame_center_top
frame_center_rect = pg.Rect(POS_PATH_LARGE_X - FRAME_PADDING, frame_center_top, GRID_SIZE_LARGE + 2 * FRAME_PADDING, frame_center_height)
frame_right_top = BUTTON_COLUMN_START_Y - FRAME_PADDING
# Tính lại bottom dựa trên num_algo_buttons mới
bottom_y_last_algo = BUTTON_COLUMN_START_Y + num_algo_buttons * ALGO_BUTTON_HEIGHT + max(0, num_algo_buttons - 1) * BUTTON_GAP_Y
frame_right_bottom = bottom_y_last_algo + FRAME_PADDING
frame_right_height = frame_right_bottom - frame_right_top # Chiều cao khung phải sẽ tăng lên
frame_right_rect = pg.Rect(ALGO_BUTTON_X - FRAME_PADDING, frame_right_top, ALGO_BUTTON_WIDTH + 2 * FRAME_PADDING, frame_right_height)
frame_nav_top = NAV_BUTTON_Y - FRAME_PADDING
frame_nav_bottom = NAV_BUTTON_Y + NAV_BUTTON_HEIGHT + FRAME_PADDING
frame_nav_height = frame_nav_bottom - frame_nav_top
frame_nav_rect = pg.Rect(POS_PREV_X - FRAME_PADDING, frame_nav_top, TOTAL_NAV_WIDTH + 2 * FRAME_PADDING, frame_nav_height)

# --- Animation Timing ---
STEP_DELAY = 100
TILE_ANIMATION_DURATION = 150

# --- Helper Functions ---
# (Giữ nguyên các hàm draw_text, find_zero_pos, grid_to_pixel_large, lerp, draw_8_puzzle)
def draw_text(text, font, color, surface, position, center_x=False, center_y=False, top_left=False):
    if not isinstance(text, str): text = str(text)
    try:
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if top_left: text_rect.topleft = position
        elif center_x and center_y: text_rect.center = position
        elif center_x: text_rect.centerx = position[0]; text_rect.top = position[1]
        elif center_y: text_rect.left = position[0]; text_rect.centery = position[1]
        else: text_rect.topleft = position
        surface.blit(text_obj, text_rect)
        return text_rect
    except Exception as e:
        print(f"Error rendering text '{text}': {e}")
        return pg.Rect(position, (0,0))

def find_zero_pos(board):
    if not isinstance(board, list) or len(board) != 3: return None
    for r in range(len(board)):
        if not isinstance(board[r], list) or len(board[r]) != 3: return None
        for c in range(len(board[r])):
            if isinstance(board[r][c], int) and board[r][c] == 0: return r, c
    return None

def grid_to_pixel_large(row, col):
    x = POS_PATH_LARGE_X + col * (TILE_SIZE_LARGE + TILE_MARGIN_LARGE)
    y = POS_PATH_LARGE_Y + row * (TILE_SIZE_LARGE + TILE_MARGIN_LARGE)
    return x, y

def lerp(start, end, t): return start + (end - start) * t

def draw_8_puzzle(matran, posx_bd, posy_bd, tile_size, tile_margin, font, skip_tile_value=None):
    current_grid_size = 3 * tile_size + 2 * tile_margin
    is_valid_matran = isinstance(matran, list) and len(matran) == 3 and \
                      all(isinstance(row, list) and len(row) == 3 for row in matran)
    if not is_valid_matran:
        rect = pg.Rect(posx_bd, posy_bd, current_grid_size, current_grid_size)
        pg.draw.rect(screen, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
        draw_text("N/A", FONT_MEDIUM, COLOR_TEXT_SECONDARY, screen, rect.center, True, True)
        return
    for r in range(3):
        for c in range(3):
            try: tile_val = matran[r][c];
            except IndexError: tile_val = -1
            if not isinstance(tile_val, int): tile_val = -1
            if skip_tile_value is not None and tile_val == skip_tile_value:
                left = posx_bd + c * (tile_size + tile_margin)
                top = posy_bd + r * (tile_size + tile_margin)
                rect = pg.Rect(left, top, tile_size, tile_size)
                pg.draw.rect(screen, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
                continue
            left = posx_bd + c * (tile_size + tile_margin)
            top = posy_bd + r * (tile_size + tile_margin)
            rect = pg.Rect(left, top, tile_size, tile_size)
            if tile_val == 0: pg.draw.rect(screen, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
            elif tile_val > 0:
                pg.draw.rect(screen, COLOR_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
                pg.draw.rect(screen, COLOR_TILE_BORDER, rect, width=1, border_radius=PUZZLE_BORDER_RADIUS)
                draw_text(str(tile_val), font, COLOR_TEXT_ON_TILE, screen, rect.center, center_x=True, center_y=True)

# --- Button Class ---
# (Giữ nguyên Button Class)
class Button:
    def __init__(self, x, y, w, h, text, callback=None, font=FONT_MAIN_BOLD,
                 base_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER,
                 selected_color=COLOR_BUTTON_SELECTED, disabled_color=COLOR_BUTTON_DISABLED,
                 text_color=COLOR_BUTTON_TEXT,
                 is_belief_button=False): # Thêm cờ nhận diện nút Belief
        self.rect = pg.Rect(x, y, w, h); self.text = text; self.callback = callback; self.font = font
        self.is_hovered = False; self.is_selected = False; self.is_disabled = False
        # Gán màu dựa trên loại nút
        self.is_belief_button = is_belief_button
        if is_belief_button:
            self.base_color = COLOR_BUTTON_BELIEF
            self.hover_color = COLOR_BUTTON_BELIEF_HOVER
            self.selected_color = COLOR_BUTTON_BELIEF_SELECTED
        else:
            self.base_color = base_color
            self.hover_color = hover_color
            self.selected_color = selected_color
        self.disabled_color = disabled_color
        self.text_color = text_color

    def _adjust_font(self): pass

    def handle_event(self, event):
        if self.is_disabled: self.is_hovered = False; return False
        action = False; mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: action = True
        if action and self.callback: self.callback(self.text)
        return action

    def draw(self, surface):
        self._adjust_font()
        current_color = self.base_color # Bắt đầu với màu base (thường hoặc belief)
        if self.is_disabled: current_color = self.disabled_color
        elif self.is_selected: current_color = self.selected_color # Màu selected (thường hoặc belief)
        elif self.is_hovered: current_color = self.hover_color # Màu hover (thường hoặc belief)

        pg.draw.rect(surface, current_color, self.rect, border_radius=BUTTON_BORDER_RADIUS)
        border_thickness = 1
        pg.draw.rect(surface, COLOR_BORDER, self.rect, width=border_thickness, border_radius=BUTTON_BORDER_RADIUS)
        draw_text(self.text, self.font, self.text_color, surface, self.rect.center, center_x=True, center_y=True)


# --- Trạng thái niềm tin mẫu (cho Conformant BFS) ---
# Bạn có thể thay đổi trạng thái này nếu muốn test với belief set khác
sample_initial_belief_state = [
    [[2, 6, 5], [0, 8, 7], [4, 3, 1]], # Trạng thái Start gốc
    [[2, 6, 5], [8, 0, 7], [4, 3, 1]], # Trạng thái Start, 0 và 8 đổi chỗ
    [[2, 0, 5], [6, 8, 7], [4, 3, 1]]  # Trạng thái Start, 0 và 6 đổi chỗ
]

# --- Solver Thread Function ---
solver_thread = None; solver_result = None; is_solving = False; path = []
# *** Cập nhật run_solver để xử lý Conformant BFS ***
def run_solver(algorithm_func, start_input, algo_name, result_container):
    """Hàm chạy thuật toán trong thread riêng.
       start_input: Có thể là start_node (cho alg thường) hoặc belief_list (cho Conf BFS).
    """
    global solver_result, Goal

    try:
        print(f"Thread started for {algo_name}..."); start_time = time.time()
        path_result = None # Kết quả cuối cùng (path states, path names, [Goal], [], None)

        # --- Xử lý gọi hàm thuật toán với các tham số đặc biệt ---
        if algo_name == "Conformant BFS": # *** Xử lý riêng cho Conformant BFS ***
            try:
                # Đảm bảo start_input là belief list
                if isinstance(start_input, list) and len(start_input) > 0 and isinstance(start_input[0], list):
                    path_result = conformant_bfs(start_input, Goal) # Gọi hàm conf_bfs
                    # path_result bây giờ là list các tên nước đi ['U', 'D', ...] hoặc None
                else:
                     raise ValueError("Input for Conformant BFS must be a list of states (belief state).")
            except ImportError:
                print("Error: Conformant BFS function not found (ImportError). Using fallback.")
                # Gọi fallback nếu import lỗi
                try: from __main__ import conformant_bfs as fallback_conf_bfs # Thử import fallback từ main
                except ImportError: fallback_conf_bfs = lambda bl, g: None # Fallback cuối cùng
                if isinstance(start_input, list) and len(start_input) > 0: path_result = fallback_conf_bfs(start_input, Goal)
                else: path_result = None
            except Exception as e_conf:
                print(f"Error running Conformant BFS: {e_conf}")
                path_result = None # Lỗi thì kết quả là None

        # --- Các thuật toán khác (giữ nguyên logic gọi) ---
        elif algo_name == "IDA*":
             try: from ThuatToan import IDA; path_result = IDA(start_input, max_threshold=80)
             except Exception as e: print(f"Error IDA*: {e}"); path_result = []
        elif algo_name in ["Simple HC", "Steepest HC", "Stochastic HC"]:
             try: path_result = algorithm_func(start_input, max_steps=2000)
             except TypeError: path_result = algorithm_func(start_input) # Fallback if no max_steps
             except Exception as e: print(f"Error HC {algo_name}: {e}"); path_result = []
        elif algo_name == "IDDFS":
             try: from ThuatToan import IDDFS; path_result = IDDFS(start_input, max_depth=30)
             except Exception as e: print(f"Error IDDFS: {e}"); path_result = []
        elif algo_name == "Sim Anneal":
             try: from ThuatToan import Simulated_Annealing; path_result = Simulated_Annealing(start_input, initial_temp=100, cooling_rate=0.97, min_temp=0.1, max_iterations=15000)
             except Exception as e: print(f"Error Sim Anneal: {e}"); path_result = []
        elif algo_name == "Beam Search":
             try: from ThuatToan import Beam_Search; path_result = Beam_Search(start_input, beam_width=5, max_iterations=1000)
             except Exception as e: print(f"Error Beam Search: {e}"); path_result = []
        elif algo_name == "Genetic Algo":
             try: from ThuatToan import Genetic_Algorithm, Goal; path_result = Genetic_Algorithm(start_input, Goal, population_size=100, generations=200, mutation_rate=0.2)
             except NameError: print("Error GA: Goal not defined."); path_result = []
             except Exception as e: print(f"Error Genetic Algo: {e}"); path_result = []
        else: # BFS, DFS, UCS, Greedy, A*
             try: path_result = algorithm_func(start_input)
             except Exception as e: print(f"Error standard algo {algo_name}: {e}"); path_result = []
        # --- Kết thúc xử lý gọi hàm ---

        end_time = time.time(); solve_time = end_time - start_time
        print(f"Thread for {algo_name} finished in {solve_time:.4f} seconds.")

        # Gán kết quả
        solver_result = {"path": path_result, "error": None, "time": solve_time, "algo": algo_name}

    except Exception as e:
        import traceback
        print(f"!!! Solver Thread critical error for {algo_name}: {e}")
        traceback.print_exc()
        solver_result = {"path": None, "error": str(e), "time": 0, "algo": algo_name}

# --- Game Initialization ---
pg.init(); screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)); pg.display.set_caption(WINDOW_TITLE); clock = pg.time.Clock()

# --- Game State & Animation Variables ---
# (Giữ nguyên)
current_step_index = 0; selected_algorithm_name = None
is_overall_animating = False
step_complete_time = 0
path_found = False # Cờ chung báo có kết quả hợp lệ (path state hoặc path name)
found_path_type = None # Lưu loại path: 'states' hoặc 'names'
status_message = "Chọn Thuật Toán Để Bắt Đầu !"; status_color = COLOR_TEXT_SECONDARY
is_tile_animating = False
animating_tile_value = None
animating_tile_rect = pg.Rect(0, 0, TILE_SIZE_LARGE, TILE_SIZE_LARGE)
animating_tile_start_pixel_pos = (0, 0)
animating_tile_end_pixel_pos = (0, 0)
tile_animation_start_time = 0

# --- Algorithms Dictionary & UI Elements ---
# *** Cập nhật dictionary để bao gồm conformant_bfs ***
algorithms = {
    "DFS": DFS, "BFS": BFS, "UCS": UCS, "IDDFS": IDDFS, "Greedy": Greedy, "A*": A_Star, "IDA*": IDA,
    "Simple HC": Simple_Hill_Climbing_First_Choice,
    "Steepest HC": Steepest_Ascent_Hill_Climbing,
    "Stochastic HC": Stochastic_Hill_Climbing,
    "Sim Anneal": Simulated_Annealing,
    "Beam Search": Beam_Search,
    "Genetic Algo": Genetic_Algorithm,
    "Conformant BFS": conformant_bfs # <--- Thêm ánh xạ
}
algo_keys = algorithms_to_display # Danh sách tên nút (đã thêm Conformant BFS)
algo_buttons = []
nav_buttons = {}

# --- Callback Functions ---
def handle_algo_button_click(algo_name_clicked):
    global selected_algorithm_name, is_solving, solver_result, path, path_found, found_path_type
    global current_step_index, is_overall_animating, status_message, status_color, is_tile_animating
    global solver_thread, Start, sample_initial_belief_state # Thêm sample_initial_belief_state

    if is_solving: print("Already solving, please wait."); return

    selected_algorithm_name = algo_name_clicked
    print(f"Algorithm Button '{selected_algorithm_name}' clicked.")
    is_solving = True; solver_result = None; path = []; path_found = False; found_path_type = None
    current_step_index = 0; is_overall_animating = False; is_tile_animating = False
    status_message = f"Đang giải bằng {selected_algorithm_name}..."; status_color = COLOR_TEXT_ACCENT

    # Disable buttons
    for btn in algo_buttons:
        btn.is_selected = (btn.text == selected_algorithm_name)
        btn.is_disabled = True
    nav_buttons["prev"].is_disabled = True
    nav_buttons["next"].is_disabled = True

    # --- Xác định đầu vào và hàm cho thuật toán ---
    algo_func = algorithms.get(selected_algorithm_name)
    start_input_arg = None

    if selected_algorithm_name == "Conformant BFS":
        # Sử dụng trạng thái niềm tin mẫu làm đầu vào
        start_input_arg = copy.deepcopy(sample_initial_belief_state)
        print(f"Using sample belief state for {selected_algorithm_name}: {len(start_input_arg)} initial states.")
        # Hiển thị trạng thái đầu tiên của belief set lên puzzle lớn
        if start_input_arg: path = [start_input_arg[0]] # Đặt path tạm thời để vẽ
    else:
        # Các thuật toán khác dùng trạng thái Start đơn
        start_input_arg = copy.deepcopy(Start)
        path = [start_input_arg] # Đặt path tạm thời để vẽ Start

    # --- Chạy thread ---
    if algo_func and start_input_arg is not None:
        solver_thread = threading.Thread(target=run_solver,
                                         args=(algo_func, start_input_arg, selected_algorithm_name, solver_result),
                                         daemon=True)
        solver_thread.start()
    else:
        # Lỗi không tìm thấy hàm hoặc không có đầu vào hợp lệ
        errmsg = "không tìm thấy hàm" if not algo_func else "đầu vào không hợp lệ"
        print(f"Error: Cannot run '{selected_algorithm_name}' ({errmsg}).")
        status_message = f"Lỗi: Không chạy được {selected_algorithm_name}"; status_color = COLOR_TEXT_ERROR
        is_solving = False;
        # Re-enable buttons
        for btn in algo_buttons: btn.is_disabled = False; btn.is_selected = False
        nav_buttons["prev"].is_disabled = True
        nav_buttons["next"].is_disabled = True
        path = [copy.deepcopy(Start)] # Reset path về Start

# (Giữ nguyên nav_button_click)
def nav_button_click(direction):
    global current_step_index, is_overall_animating, path, path_found, found_path_type, is_tile_animating, step_complete_time
    # *** Chỉ cho phép điều hướng nếu path là 'states' ***
    if not path_found or not path or is_tile_animating or found_path_type != 'states':
        return
    was_animating = is_overall_animating
    is_overall_animating = False
    prev_index = current_step_index
    if direction == "prev":
        current_step_index = max(0, current_step_index - 1)
    elif direction == "next":
        if not is_tile_animating:
             current_step_index = min(len(path) - 1, current_step_index + 1)
    if prev_index != current_step_index:
         print(f"Navigate {direction}: Step index set to {current_step_index}")
         step_complete_time = pg.time.get_ticks()

# --- Tạo các đối tượng Button UI ---
# (Phải tạo sau khi định nghĩa callback)
for i, algo_name_display in enumerate(algo_keys):
    btn_y = BUTTON_COLUMN_START_Y + i * (ALGO_BUTTON_HEIGHT + BUTTON_GAP_Y)
    # *** Đặt cờ is_belief_button cho nút Conformant BFS ***
    is_belief = (algo_name_display == "Conformant BFS")
    button = Button(ALGO_BUTTON_X, btn_y, ALGO_BUTTON_WIDTH, ALGO_BUTTON_HEIGHT, algo_name_display,
                    callback=handle_algo_button_click,
                    is_belief_button=is_belief) # <-- Truyền cờ
    algo_buttons.append(button)

nav_buttons = {
    "prev": Button(POS_PREV_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Lùi",
                   callback=nav_button_click,
                   base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER),
    "next": Button(POS_NEXT_X, NAV_BUTTON_Y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT, "Tiến",
                   callback=nav_button_click,
                   base_color=COLOR_NAV_BUTTON, hover_color=COLOR_NAV_BUTTON_HOVER)
}
nav_buttons["prev"].is_disabled = True
nav_buttons["next"].is_disabled = True

# --- Main Game Loop ---
running = True
while running:
    current_time = pg.time.get_ticks(); mouse_pos = pg.mouse.get_pos(); dt = clock.tick(60) / 1000.0

    # --- Event Handling ---
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        button_clicked_this_frame = False
        for button in algo_buttons:
             if not button.is_disabled:
                 if button.handle_event(event): button_clicked_this_frame = True; break
        # *** Chỉ xử lý nav button nếu path là 'states' ***
        if not button_clicked_this_frame and path_found and len(path) > 1 and found_path_type == 'states':
             if not nav_buttons["prev"].is_disabled: nav_buttons["prev"].handle_event(event)
             if not nav_buttons["next"].is_disabled: nav_buttons["next"].handle_event(event)

    # --- Update State ---

    # 1. Kiểm tra và xử lý kết quả từ Solver Thread
    if is_solving and solver_thread and not solver_thread.is_alive():
        is_solving = False
        local_solver_result = solver_result
        algo_name_from_result = "Unknown"
        path_found = False
        found_path_type = None # Reset loại path
        # Mặc định hiển thị Start nếu có lỗi hoặc không có path
        path = [copy.deepcopy(Start)]
        # Mặc định vô hiệu hóa nav buttons
        can_navigate = False

        if local_solver_result:
            algo_name_from_result = local_solver_result.get("algo", "Unknown")
            solve_time = local_solver_result.get('time', 0)
            raw_path_result = local_solver_result.get("path") # Đây có thể là list states, list names, [Goal], [], None
            error_msg = local_solver_result.get("error")

            if error_msg: # Nếu có lỗi từ thread
                status_message = f"Lỗi ({algo_name_from_result}): {error_msg}"
                status_color = COLOR_TEXT_ERROR
                print(f"Solver error reported: {error_msg}")

            elif raw_path_result is not None: # Nếu có kết quả (không phải None)
                # *** Xử lý riêng cho Conformant BFS ***
                if algo_name_from_result == "Conformant BFS":
                    if isinstance(raw_path_result, list): # Kết quả là list tên nước đi
                        path = raw_path_result # Lưu lại list tên nước đi
                        path_found = True
                        found_path_type = 'names' # Đánh dấu loại path
                        move_count = len(path)
                        status_message = f"Conformant BFS: Tìm thấy {move_count} nước đi trong {solve_time:.3f}s"
                        status_color = COLOR_TEXT_SUCCESS
                        print(f"Conformant BFS path found: {move_count} moves - {path}")
                        # Hiển thị trạng thái đầu tiên của belief state lên puzzle lớn
                        if sample_initial_belief_state:
                            path_for_display = [copy.deepcopy(sample_initial_belief_state[0])]
                        else:
                            path_for_display = [copy.deepcopy(Start)] # Fallback nếu sample belief state lỗi
                        path = path_for_display # Ghi đè path để vẽ (chỉ vẽ state đầu)

                    else: # Kết quả conformant BFS không phải list (có thể là None hoặc lỗi khác)
                         status_message = f"Conformant BFS: Không tìm thấy đường đi."
                         if solve_time > 0: status_message += f" (Tìm kiếm trong {solve_time:.3f}s)"
                         status_color = COLOR_TEXT_SECONDARY
                         print("Conformant BFS did not find a path.")
                         path = [copy.deepcopy(sample_initial_belief_state[0])] if sample_initial_belief_state else [copy.deepcopy(Start)]


                # *** Xử lý cho các thuật toán khác ***
                else:
                    temp_path = raw_path_result # Kết quả là list states, [Goal], hoặc []
                    is_list_of_states = isinstance(temp_path, list) and \
                                        len(temp_path) > 0 and \
                                        all(isinstance(step, list) for step in temp_path)
                    is_only_goal = is_list_of_states and len(temp_path) == 1 and temp_path[0] == Goal

                    if is_list_of_states:
                        is_valid_path_structure = all(len(step) == 3 and all(isinstance(row, list) and len(row)==3 for row in step) for step in temp_path)
                        if is_valid_path_structure:
                            path = temp_path # Lưu path trạng thái
                            path_found = True
                            found_path_type = 'states' # Đánh dấu loại path
                            current_step_index = 0
                            if is_only_goal: # GA/HC/SA tìm thấy Goal
                                is_overall_animating = False
                                can_navigate = False # Không navigate nếu chỉ có Goal
                                status_message = f"{algo_name_from_result}: Tìm thấy Goal State trong {solve_time:.3f}s."
                                status_color = COLOR_TEXT_SUCCESS
                                print("Goal state found directly.")
                            elif len(temp_path) > 1: # Path chuẩn
                                is_overall_animating = True
                                can_navigate = True # Có thể navigate
                                step_complete_time = current_time
                                status_message = f"{algo_name_from_result}: Tìm thấy đường đi ({len(path)} bước) trong {solve_time:.3f}s."
                                status_color = COLOR_TEXT_SUCCESS
                                print(f"Path processed: {len(path)} steps. Ready to animate.")
                            else: # Path có 1 bước nhưng không phải Goal
                                is_overall_animating = False
                                can_navigate = False
                                path_found = False # Coi như không tìm thấy Goal
                                status_message = f"{algo_name_from_result}: Dừng ở bước {len(path)} (không phải Goal) trong {solve_time:.3f}s."
                                status_color = COLOR_TEXT_SECONDARY
                                print("Path found but not Goal state.")
                        else: # Cấu trúc path không hợp lệ
                             status_message = f"Lỗi: Kết quả từ {algo_name_from_result} có cấu trúc không hợp lệ."; status_color = COLOR_TEXT_ERROR
                             print("Invalid path structure received.")
                    elif isinstance(temp_path, list) and len(temp_path) == 0: # Không tìm thấy (list rỗng)
                        status_message = f"{algo_name_from_result}: Không tìm thấy đường đi.";
                        if solve_time > 0: status_message += f" (Tìm kiếm trong {solve_time:.3f}s)"
                        status_color = COLOR_TEXT_SECONDARY
                        print("No path found by solver (empty list).")
                    else: # Cấu trúc kết quả không xác định
                         status_message = f"Lỗi: Kết quả từ {algo_name_from_result} không xác định."; status_color = COLOR_TEXT_ERROR
                         print(f"Unknown result structure: {temp_path}")

            else: # raw_path_result là None
                status_message = f"Lỗi Solver: Không nhận được kết quả từ {algo_name_from_result}."
                status_color = COLOR_TEXT_ERROR
                print("Solver path result was None.")

            # --- Kích hoạt lại các nút ---
            for btn in algo_buttons:
                btn.is_disabled = False
                btn.is_selected = (btn.text == algo_name_from_result)

            # Kích hoạt/Vô hiệu hóa nút điều hướng
            # Chỉ kích hoạt nếu path là 'states' và có nhiều hơn 1 state
            can_navigate = path_found and found_path_type == 'states' and len(path) > 1
            nav_buttons["prev"].is_disabled = not can_navigate
            nav_buttons["next"].is_disabled = not can_navigate

            solver_result = None # Reset kết quả global

        else: # Lỗi: solver_thread xong nhưng solver_result là None
             print("Solver finished but global solver_result is None.")
             status_message = "Lỗi Solver: Kết quả không xác định."; status_color = COLOR_TEXT_ERROR
             path = [copy.deepcopy(Start)]; path_found = False; found_path_type = None
             for btn in algo_buttons: btn.is_disabled = False; btn.is_selected = False
             nav_buttons["prev"].is_disabled = True
             nav_buttons["next"].is_disabled = True

    # 2. Xử lý Animation Di chuyển Ô (Tile Sliding)
    # *** Chỉ chạy nếu path type là 'states' ***
    if is_tile_animating and found_path_type == 'states':
        elapsed = current_time - tile_animation_start_time
        progress = min(1.0, elapsed / TILE_ANIMATION_DURATION)
        current_x = lerp(animating_tile_start_pixel_pos[0], animating_tile_end_pixel_pos[0], progress)
        current_y = lerp(animating_tile_start_pixel_pos[1], animating_tile_end_pixel_pos[1], progress)
        animating_tile_rect.topleft = (int(current_x), int(current_y))
        if progress >= 1.0:
            is_tile_animating = False
            step_complete_time = current_time
            if current_step_index >= len(path) - 1:
                is_overall_animating = False

    # 3. Xử lý Animation Tổng thể (Chuyển bước tự động)
    # *** Chỉ chạy nếu path type là 'states' ***
    if is_overall_animating and path_found and not is_tile_animating and found_path_type == 'states' and current_step_index < len(path) - 1:
        if current_time - step_complete_time >= STEP_DELAY:
            target_step_index = current_step_index + 1
            if 0 <= current_step_index < len(path) and 0 <= target_step_index < len(path):
                prev_state = path[current_step_index]
                next_state = path[target_step_index]
                if isinstance(prev_state, list) and isinstance(next_state, list):
                    prev_zero_pos = find_zero_pos(prev_state)
                    next_zero_pos = find_zero_pos(next_state)
                    if prev_zero_pos and next_zero_pos:
                        moving_tile_r, moving_tile_c = prev_zero_pos
                        try: animating_tile_value = next_state[moving_tile_r][moving_tile_c]
                        except IndexError: is_overall_animating = False; animating_tile_value = None; print("Anim Error: Index out of bounds")
                        if animating_tile_value is not None and animating_tile_value != 0:
                            start_r, start_c = next_zero_pos
                            animating_tile_start_pixel_pos = grid_to_pixel_large(start_r, start_c)
                            end_r, end_c = prev_zero_pos
                            animating_tile_end_pixel_pos = grid_to_pixel_large(end_r, end_c)
                            is_tile_animating = True
                            animating_tile_rect.topleft = animating_tile_start_pixel_pos
                            tile_animation_start_time = current_time
                            current_step_index = target_step_index # Cập nhật index ngay
                        else:
                            current_step_index = target_step_index; step_complete_time = current_time
                            if current_step_index >= len(path) - 1: is_overall_animating = False
                    else: is_overall_animating = False; print("Anim Error: Zero pos not found")
                else: is_overall_animating = False; print("Anim Error: Invalid state in path")
            else: is_overall_animating = False; print("Anim Error: Invalid index")

    # --- Drawing ---
    screen.fill(COLOR_BACKGROUND)
    frame_border_thickness = 1; frame_border_radius = 5
    pg.draw.rect(screen, COLOR_BORDER, frame_left_rect, frame_border_thickness, border_radius=frame_border_radius)
    pg.draw.rect(screen, COLOR_BORDER, frame_center_rect, frame_border_thickness, border_radius=frame_border_radius)
    pg.draw.rect(screen, COLOR_BORDER, frame_right_rect, frame_border_thickness, border_radius=frame_border_radius)
    # *** Chỉ vẽ khung nav nếu path type là 'states' ***
    if path_found and len(path) > 1 and found_path_type == 'states':
        pg.draw.rect(screen, COLOR_BORDER, frame_nav_rect, frame_border_thickness, border_radius=frame_border_radius)

    draw_text("8 PUZZLE SOLVER VISUALIZATION", FONT_LARGE, COLOR_TEXT_PRIMARY, screen, (SCREEN_WIDTH // 2, TITLE_POS_Y), center_x=True, center_y=True)
    draw_text("Trạng Thái Đầu", FONT_MEDIUM, COLOR_TEXT_SECONDARY, screen, (POS_START_SMALL_X + GRID_SIZE_SMALL // 2, POS_START_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
    draw_8_puzzle(Start, POS_START_SMALL_X, POS_START_SMALL_Y, TILE_SIZE_SMALL, TILE_MARGIN_SMALL, FONT_TILE_SMALL)
    draw_text("Trạng Thái Đích", FONT_MEDIUM, COLOR_TEXT_SECONDARY, screen, (POS_GOAL_SMALL_X + GRID_SIZE_SMALL // 2, POS_GOAL_SMALL_Y - LABEL_OFFSET_Y), center_x=True)
    draw_8_puzzle(Goal, POS_GOAL_SMALL_X, POS_GOAL_SMALL_Y, TILE_SIZE_SMALL, TILE_MARGIN_SMALL, FONT_TILE_SMALL)

    path_label_text = "Chọn Thuật Toán"
    if is_solving: path_label_text = f"Đang tìm kiếm ({selected_algorithm_name})..."
    elif path_found:
        if found_path_type == 'states': # Path là list states
            if len(path) == 1 and path[0] == Goal: path_label_text = f"{selected_algorithm_name}: Tìm thấy Goal!"
            elif len(path) > 1: path_label_text = f"{selected_algorithm_name}: Bước {current_step_index + 1} / {len(path)}"
            else: path_label_text = f"{selected_algorithm_name}: Dừng (Không phải Goal)"
        elif found_path_type == 'names': # Path là list tên nước đi (Conformant BFS)
             path_label_text = f"Conformant BFS: {len(path)} nước đi"
             # Có thể hiển thị một phần path tên ở status bar thay vì ở đây
    elif selected_algorithm_name and not is_solving: # Đã chạy xong nhưng không tìm thấy
         path_label_text = f"{selected_algorithm_name}: Không tìm thấy Goal"

    draw_text(path_label_text, FONT_MEDIUM, COLOR_TEXT_SECONDARY, screen, (POS_PATH_LARGE_X + GRID_SIZE_LARGE // 2, POS_PATH_LARGE_Y - LABEL_OFFSET_Y), center_x=True)

    current_display_state = Start
    if path and len(path) > 0:
        # Chỉ hiển thị state nếu path là 'states'
        if found_path_type == 'states' and isinstance(path[0], list):
             safe_index = max(0, min(current_step_index, len(path) - 1))
             if safe_index < len(path) and isinstance(path[safe_index], list):
                  current_display_state = path[safe_index]
        elif found_path_type == 'names': # Nếu là conformant, chỉ hiển thị state đầu của belief set mẫu
             current_display_state = copy.deepcopy(sample_initial_belief_state[0]) if sample_initial_belief_state else Start

    tile_to_skip_drawing = animating_tile_value if is_tile_animating and found_path_type == 'states' else None
    draw_8_puzzle(current_display_state, POS_PATH_LARGE_X, POS_PATH_LARGE_Y, TILE_SIZE_LARGE, TILE_MARGIN_LARGE, FONT_TILE_LARGE, skip_tile_value=tile_to_skip_drawing)

    # Vẽ tile đang di chuyển (chỉ khi path type là 'states')
    if is_tile_animating and found_path_type == 'states' and animating_tile_value is not None and animating_tile_value > 0:
        pg.draw.rect(screen, COLOR_TILE, animating_tile_rect, border_radius=PUZZLE_BORDER_RADIUS)
        pg.draw.rect(screen, COLOR_TILE_BORDER, animating_tile_rect, width=1, border_radius=PUZZLE_BORDER_RADIUS)
        draw_text(str(animating_tile_value), FONT_TILE_LARGE, COLOR_TEXT_ON_TILE, screen, animating_tile_rect.center, center_x=True, center_y=True)

    for button in algo_buttons: button.draw(screen)
    # Chỉ vẽ nút nav nếu path là 'states'
    if path_found and len(path) > 1 and found_path_type == 'states':
        nav_buttons["prev"].draw(screen)
        nav_buttons["next"].draw(screen)

    status_rect = pg.Rect(0, STATUS_BAR_Y, SCREEN_WIDTH, STATUS_BAR_HEIGHT)
    pg.draw.rect(screen, COLOR_STATUS_BG, status_rect)
    pg.draw.line(screen, COLOR_BORDER, (0, STATUS_BAR_Y), (SCREEN_WIDTH, STATUS_BAR_Y), 1)
    # Hiển thị thêm path tên nếu là conformant bfs
    display_status_msg = status_message
    if path_found and found_path_type == 'names':
        display_status_msg += f" Path: {' -> '.join(path[:10])}{'...' if len(path)>10 else ''}" # Hiển thị 10 bước đầu

    draw_text(display_status_msg, FONT_MAIN_REGULAR, status_color, screen, (15, STATUS_BAR_Y + STATUS_BAR_HEIGHT // 2), center_y=True)

    pg.display.flip()

pg.quit()
sys.exit()