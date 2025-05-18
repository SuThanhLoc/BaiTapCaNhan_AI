import pygame
import random
import AI  # Đảm bảo AI được import
import sys
import os
import copy
pygame.init()
pygame.font.init()

pygame.display.set_caption("8-puzzle")
screen = pygame.display.set_mode((1200, 850))

# --- Font Setup ---
FONT_FILE_NAME = "Roboto-Regular.ttf"  # Thử một font khác nếu Roboto không có sẵn
# FONT_FILE_NAME = None # Để sử dụng font mặc định của Pygame
FONT_SIZE_TITLE_MAIN = 36
FONT_SIZE_TITLE_SECTION = 22
FONT_SIZE_BUTTON_CONTROL = 20
FONT_SIZE_BUTTON_ALGO = 15  # Giảm nhẹ kích thước font nút algo
FONT_SIZE_STEP_INFO = 20
FONT_EXTRA_INFO_SIZE = 18
try:
    if FONT_FILE_NAME and os.path.exists(FONT_FILE_NAME):
        FONT_TITLE_MAIN = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_TITLE_MAIN)
        FONT_TITLE_SECTION = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_TITLE_SECTION)
        FONT_BUTTON_CONTROL = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_BUTTON_CONTROL)
        FONT_BUTTON_ALGO = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_BUTTON_ALGO)
        FONT_STEP_INFO = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_STEP_INFO)
        FONT_EXTRA_INFO = pygame.font.Font(FONT_FILE_NAME, FONT_EXTRA_INFO_SIZE)
        print(f"Đã tải font thành công từ: {FONT_FILE_NAME}")
    else:
        raise pygame.error("Font file not found or not specified.")
except pygame.error as e:
    print(f"LỖI: Không thể tải font '{FONT_FILE_NAME}': {e}. Sử dụng font mặc định của Pygame.")
    FONT_TITLE_MAIN = pygame.font.Font(None, FONT_SIZE_TITLE_MAIN + 6)
    FONT_TITLE_SECTION = pygame.font.Font(None, FONT_SIZE_TITLE_SECTION + 4)
    FONT_BUTTON_CONTROL = pygame.font.Font(None, FONT_SIZE_BUTTON_CONTROL + 4)
    FONT_BUTTON_ALGO = pygame.font.Font(None, FONT_SIZE_BUTTON_ALGO + 4)
    FONT_STEP_INFO = pygame.font.Font(None, FONT_SIZE_STEP_INFO + 4)
    FONT_EXTRA_INFO = pygame.font.Font(None, FONT_EXTRA_INFO_SIZE + 4)

# --- Color Definitions ---
BLUE_BG = (142, 30, 32)  # Màu xanh dương cho title bar và các nút chính
DARK_BLUE_BUTTON_BG = (30, 60, 120)  # Màu xanh dương đậm hơn cho nút thuật toán
ORANGE_BUTTON_BG = (255, 140, 0)  # DarkOrange
GREEN_BUTTON_BG = (60, 179, 113)  # MediumSeaGreen
PURPLE_BUTTON_BG = (138, 43, 226)  # BlueViolet
RED_BUTTON_BG = (205, 92, 92)  # IndianRed
LIGHT_BLUE_BUTTON_BG = (30, 144, 255)  # DodgerBlue

WHITE_TEXT = (240, 240, 240)
MAIN_SCREEN_BACKGROUND = (225, 225, 225)  # Xám nhạt hơn một chút
NUMBERED_CELL_BG = BLUE_BG
EMPTY_CELL_BG = (205, 205, 205)
PUZZLE_BORDER_COLOR = (60, 60, 60)
CELL_BORDER_RADIUS = 8
SELECTED_HIGHLIGHT_COLOR = (255, 215, 0)  # Gold
HOVER_BRIGHTEN_AMOUNT = 50  # Lượng làm sáng màu khi hover
SEARCHING_BG_COLOR = (120, 120, 120)  # Xám đậm hơn cho trạng thái "Đang tìm"
TEXT_INFO_COLOR = (40, 40, 40)  # Màu chữ thông tin (tối hơn)
ERROR_TEXT_COLOR = (200, 0, 0)  # Màu đỏ cho lỗi
SUCCESS_BG_COLOR = (0, 160, 0)  # Xanh lá đậm cho thành công

# --- UI Text Constants ---
TITLE_TEXT = "8 PUZZLE GAME"
TITLE_BAR_Y_OFFSET = 15
TITLE_BG_PADDING_X = 30
TITLE_BG_PADDING_Y = 12
TITLE_BG_BORDER_RADIUS = 12


# --- Utility Functions ---
def is_solvable_ui(puzzle_state_list_of_lists):
    return AI.is_solvable(puzzle_state_list_of_lists)


def random_puzzle_ui():
    return AI.generate_random_board()  # Nên dùng hàm đã có sẵn và kiểm tra solvability trong AI.py


def create_blocks_for_input_ui():
    new_blocks = []
    block_width_input, block_height_input = 75, 75  # Kích thước khối số nhập
    for i in range(9):
        rect = pygame.Rect(0, 0, block_width_input, block_height_input)
        new_blocks.append((rect, i))
    return new_blocks


def button_ui(x, y, width, height, text, base_color, text_color, font_obj=None, border_radius=8, is_hovered=False,
              is_selected=False):
    if font_obj is None: font_obj = FONT_BUTTON_CONTROL

    current_bg_color = base_color
    if is_hovered and not is_selected:
        try:
            current_bg_color = tuple(min(255, c + HOVER_BRIGHTEN_AMOUNT) for c in base_color)
        except TypeError:
            pass

    pygame.draw.rect(screen, current_bg_color, (x, y, width, height), 0, border_radius=border_radius)

    if is_selected:
        pygame.draw.rect(screen, SELECTED_HIGHLIGHT_COLOR, (x - 3, y - 3, width + 6, height + 6), 3,
                         border_radius=border_radius + 2)

    text_surface = font_obj.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)


def draw_text_label_ui(text, font_obj, color, center_x, y, background_color=None, padding_x=10, padding_y=5,
                       width_override=None, border_radius=5, text_align_center=True):
    text_surface = font_obj.render(text, True, color)
    text_rect_temp = text_surface.get_rect()

    bg_width = width_override if width_override is not None else text_rect_temp.width + 2 * padding_x
    bg_height = text_rect_temp.height + 2 * padding_y

    if text_align_center:
        bg_rect_x = center_x - bg_width // 2
    else:  # Căn lề trái
        bg_rect_x = center_x

    bg_rect = pygame.Rect(bg_rect_x, y, bg_width, bg_height)

    if background_color:
        pygame.draw.rect(screen, background_color, bg_rect, 0, border_radius=border_radius)

    text_final_rect = text_surface.get_rect(center=bg_rect.center)  # Luôn căn giữa text trong background
    screen.blit(text_surface, text_final_rect)
    return bg_rect.bottom


def draw_puzzle_ui(puzzle_state, pos, puzzle_total_size=300, cell_gap=3):
    cell_size = (puzzle_total_size - (2 * cell_gap)) // 3  # Tính kích thước ô dựa trên gap
    font_size_dynamic = int(cell_size * 0.6)
    try:
        dynamic_puzzle_font = pygame.font.Font(
            FONT_FILE_NAME if FONT_FILE_NAME and os.path.exists(FONT_FILE_NAME) else None, font_size_dynamic)
    except:
        dynamic_puzzle_font = pygame.font.Font(None, int(font_size_dynamic * 1.1))

    for i in range(3):
        for j in range(3):
            number = puzzle_state[i][j]
            rect_x = pos[0] + j * (cell_size + cell_gap)
            rect_y = pos[1] + i * (cell_size + cell_gap)
            cell_rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)

            cell_bg_color = NUMBERED_CELL_BG if number != 0 else EMPTY_CELL_BG
            pygame.draw.rect(screen, cell_bg_color, cell_rect, border_radius=CELL_BORDER_RADIUS)

            if number != 0:
                text_surface = dynamic_puzzle_font.render(str(number), True, WHITE_TEXT)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                screen.blit(text_surface, text_rect)


def add_number_to_input_ui(current_puzzle_input_list, number_to_add):
    for r_idx in range(3):
        for c_idx in range(3):
            if puzzle_input_check[r_idx][c_idx] == 0:
                current_puzzle_input_list[r_idx][c_idx] = number_to_add
                puzzle_input_check[r_idx][c_idx] = 1
                return True
    return False


def reset_input_puzzle_state_ui():
    global puzzle_input, puzzle_input_check, blocks_input_ui
    puzzle_input = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    puzzle_input_check = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    blocks_input_ui = create_blocks_for_input_ui()


def reset_all_game_states_ui():
    global begin, current, path, index, solving, done, selected_algo_name, is_calculating_path
    global search_time_sec, show_search_info, solvability_message_ui, last_update_time_anim

    begin = random_puzzle_ui()
    current = copy.deepcopy(begin)
    path = []
    index = 0
    solving = False
    done = False
    selected_algo_name = ''
    is_calculating_path = False
    search_time_sec = 0.0
    show_search_info = False
    last_update_time_anim = pygame.time.get_ticks()  # Reset timer animation

    if AI.is_solvable(begin):
        solvability_message_ui = "Trạng thái: Có thể giải"
    else:
        solvability_message_ui = "Trạng thái: Không thể giải!"
    reset_input_puzzle_state_ui()


# --- Game State Variables ---
running = True
solving = False
inputting = False
selected_algo_name = ''  # Tên thuật toán đang được chọn
done = False
is_calculating_path = False
animation_speed_ms = 250
search_time_sec = 0.0
show_search_info = False
solvability_message_ui = ""

begin = random_puzzle_ui()
current = copy.deepcopy(begin)
path = []
if AI.is_solvable(begin):
    solvability_message_ui = "Trạng thái: Có thể giải"
else:
    solvability_message_ui = "Trạng thái: Không thể giải!"

puzzle_input = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
puzzle_input_check = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
result_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Khôi phục danh sách thuật toán gốc và thêm AC-3
algorithm_display_names_list = [
    'Breadth-First Search', 'Uniform Cost Search', 'Depth-First Search',
    'Iterative Deepening DFS', 'Greedy Search', 'A* Search', 'IDA* Search',
    'Simple Hill Climbing', 'Stochastic Hill Climbing', 'Steepest Ascent HC',
    'Simulated Annealing', 'Beam Search', 'Genetic Algorithm',
    'Backtracking Search', 'Forward Checking',
    'AC-3 Algorithm',  # AC-3 đã thêm
    'AND-OR (Console)', 'Belief State (Console)', 'Belief 1 Part (Console)',  # Khôi phục Belief 1 Part
    'Q-Learning'  # Q-Learning không có (Console) nếu nó trả về path
]

index = 0
blocks_input_ui = create_blocks_for_input_ui()
last_update_time_anim = pygame.time.get_ticks()

# --- UI Layout Constants (có thể cần điều chỉnh lại sau khi thêm/bớt nút) ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 850
LEFT_COL_X_START_UI = 25
LEFT_COL_WIDTH_UI = 220
STATIC_PUZZLE_SIZE_UI = 180

algo_button_height_ui = 33
algo_button_spacing_ui = 7
algo_horizontal_spacing_ui = 10
algo_padding_x_ui = 8
uniform_algo_button_width_ui = 210  # Tăng nhẹ để vừa tên dài hơn

# Khởi tạo Rects cho các nút (quan trọng)
btn_random_rect = pygame.Rect(0, 0, 0, 0)
btn_input_main_rect = pygame.Rect(0, 0, 0, 0)
btn_solve_main_rect = pygame.Rect(0, 0, 0, 0)
btn_show_goal_main_rect = pygame.Rect(0, 0, 0, 0)
btn_prev_main_rect = pygame.Rect(0, 0, 0, 0)
btn_reset_main_rect = pygame.Rect(0, 0, 0, 0)
btn_next_main_rect = pygame.Rect(0, 0, 0, 0)
btn_back_input_rect = pygame.Rect(0, 0, 0, 0)
btn_ok_input_rect = pygame.Rect(0, 0, 0, 0)
btn_reset_puzzle_input_rect = pygame.Rect(0, 0, 0, 0)
algo_buttons_rect_cache_ui = []

# --- Main Game Loop ---
while running:
    current_time_ticks_main = pygame.time.get_ticks()
    mouse_pos_main = pygame.mouse.get_pos()

    for event_main in pygame.event.get():
        if event_main.type == pygame.QUIT:
            running = False

        elif event_main.type == pygame.MOUSEBUTTONDOWN:
            if not inputting:
                action_taken_main_click = False

                if btn_random_rect.collidepoint(mouse_pos_main) and not solving and not is_calculating_path:
                    reset_all_game_states_ui()
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_input_main_rect.collidepoint(
                        mouse_pos_main) and not solving and not is_calculating_path:
                    inputting = True
                    reset_input_puzzle_state_ui()
                    selected_algo_name = ""  # Xóa thông báo khi chuyển màn hình
                    solvability_message_ui = ""
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_solve_main_rect.collidepoint(
                        mouse_pos_main) and not solving and selected_algo_name and not is_calculating_path:
                    if not AI.is_solvable(begin):
                        selected_algo_name = "Puzzle hiện tại không thể giải!"
                        show_search_info = True
                        search_time_sec = 0.0
                    elif begin == result_goal_state:
                        path = [begin]
                        solving = True;
                        done = True;
                        index = 0;
                        current = copy.deepcopy(begin)
                        show_search_info = True;
                        search_time_sec = 0.0
                    elif selected_algo_name:
                        is_calculating_path = True
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_show_goal_main_rect.collidepoint(
                        mouse_pos_main) and not is_calculating_path:
                    if solving and not done and path:
                        index = len(path) - 1 if path else 0
                        current = copy.deepcopy(path[index] if path else result_goal_state)
                        done = True
                    else:
                        current = copy.deepcopy(result_goal_state)
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_prev_main_rect.collidepoint(
                        mouse_pos_main) and path and not is_calculating_path:
                    if index > 0: index -= 1; current = copy.deepcopy(path[index])
                    done = False
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_reset_main_rect.collidepoint(
                        mouse_pos_main) and not is_calculating_path:
                    reset_all_game_states_ui()
                    action_taken_main_click = True
                elif not action_taken_main_click and btn_next_main_rect.collidepoint(
                        mouse_pos_main) and path and not is_calculating_path:
                    if index < len(path) - 1: index += 1; current = copy.deepcopy(path[index])
                    if index == len(path) - 1: done = True
                    action_taken_main_click = True

                if not action_taken_main_click and not solving and not is_calculating_path:
                    for btn_r_algo, algo_name_iter, _, _ in algo_buttons_rect_cache_ui:
                        if btn_r_algo.collidepoint(mouse_pos_main):
                            selected_algo_name = algo_name_iter
                            print(f"Đã chọn thuật toán: {selected_algo_name}")
                            show_search_info = False;
                            search_time_sec = 0.0
                            if AI.is_solvable(begin):
                                solvability_message_ui = "Trạng thái: Có thể giải"
                            else:
                                solvability_message_ui = "Trạng thái: Không thể giải!"
                            break

            else:  # Đang ở màn hình inputting
                if btn_back_input_rect.collidepoint(mouse_pos_main):
                    inputting = False;
                    selected_algo_name = ""
                    if AI.is_solvable(begin):
                        solvability_message_ui = "Trạng thái: Có thể giải"
                    else:
                        solvability_message_ui = "Trạng thái: Không thể giải!"
                elif btn_ok_input_rect.collidepoint(mouse_pos_main):
                    flat_check_input = [item for sublist in puzzle_input_check for item in sublist]
                    if all(cell == 1 for cell in flat_check_input):
                        flat_puzzle_vals_input = [item for sublist in puzzle_input for item in sublist]
                        if len(set(flat_puzzle_vals_input)) == 9 and all(
                                0 <= x_val <= 8 for x_val in flat_puzzle_vals_input):
                            if AI.is_solvable(puzzle_input):
                                temp_begin_copy_input = [row[:] for row in puzzle_input]
                                reset_all_game_states_ui()
                                begin = temp_begin_copy_input
                                current = copy.deepcopy(begin)
                                if AI.is_solvable(begin):
                                    solvability_message_ui = "Trạng thái: Có thể giải"
                                else:
                                    solvability_message_ui = "Trạng thái: Không thể giải!"
                                inputting = False
                            else:
                                selected_algo_name = "Puzzle bạn nhập không thể giải được!"
                        else:
                            selected_algo_name = "Input không hợp lệ (số trùng / ngoài phạm vi)!"
                    else:
                        selected_algo_name = "Chưa nhập đủ 9 số!"
                elif btn_reset_puzzle_input_rect.collidepoint(mouse_pos_main):
                    reset_input_puzzle_state_ui();
                    selected_algo_name = ""

                for r_rect_input_block, val_block_event_block in blocks_input_ui:
                    if r_rect_input_block.collidepoint(mouse_pos_main):
                        is_val_used_input_block = False
                        for r_check_block, row_val_block in enumerate(puzzle_input):
                            for c_check_block, cell_val_block in enumerate(row_val_block):
                                if cell_val_block == val_block_event_block and puzzle_input_check[r_check_block][
                                    c_check_block] == 1:
                                    is_val_used_input_block = True;
                                    break
                            if is_val_used_input_block: break
                        if not is_val_used_input_block:
                            if not add_number_to_input_ui(puzzle_input, val_block_event_block):
                                selected_algo_name = "Puzzle input đã đầy!"
                        else:
                            selected_algo_name = f"Số {val_block_event_block} đã được dùng!"
                        break

                        # --- Logic cập nhật trạng thái (ngoài vòng event) ---
    if is_calculating_path:
        screen.fill(MAIN_SCREEN_BACKGROUND)
        loading_text_calc = f"Đang tìm lời giải: {selected_algo_name}..."
        draw_text_label_ui(loading_text_calc, FONT_TITLE_SECTION, TEXT_INFO_COLOR, SCREEN_WIDTH // 2,
                           SCREEN_HEIGHT // 2 - 30, text_align_center=True)
        pygame.display.flip()

        start_time_calc = pygame.time.get_ticks()
        algo_to_run_calc = selected_algo_name

        if algo_to_run_calc == 'Breadth-First Search':
            path = AI.BFS(begin, result_goal_state)
        elif algo_to_run_calc == 'Uniform Cost Search':
            path = AI.Uniform_Cost_Search(begin, result_goal_state)
        elif algo_to_run_calc == 'Depth-First Search':
            path = AI.DFS(begin, result_goal_state)
        elif algo_to_run_calc == 'Iterative Deepening DFS':
            path = AI.Iterative_Deepening_DFS(begin, result_goal_state)
        elif algo_to_run_calc == 'Greedy Search':
            path = AI.Greedy_Search(begin, result_goal_state)
        elif algo_to_run_calc == 'A* Search':
            path = AI.A_Star_Search(begin, result_goal_state)
        elif algo_to_run_calc == 'IDA* Search':
            path = AI.IDA(begin, result_goal_state)
        elif algo_to_run_calc == 'Simple Hill Climbing':
            path = AI.Simple_Hill_Climbing(begin, result_goal_state)
        elif algo_to_run_calc == 'Stochastic Hill Climbing':
            path = AI.Stochastic_Hill_Climbing(begin, result_goal_state)
        elif algo_to_run_calc == 'Steepest Ascent HC':
            path = AI.Steepest_Ascent_Hill_Climbing(begin, result_goal_state)
        elif algo_to_run_calc == 'Simulated Annealing':
            path = AI.Simulated_Annealing(begin, result_goal_state)
        elif algo_to_run_calc == 'Beam Search':
            path = AI.Beam_Search(begin, result_goal_state, beam_width=5)
        elif algo_to_run_calc == 'Genetic Algorithm':
            path = AI.Genetic_Algorithm(begin, result_goal_state)
        elif algo_to_run_calc == 'Backtracking Search':
            path = AI.Backtracking_Search(begin, result_goal_state)
        elif algo_to_run_calc == 'Forward Checking':
            path = AI.Forward_Checking(begin, result_goal_state)
        elif algo_to_run_calc == 'AC-3 Algorithm':
            path = AI.AC3_Algorithm(begin, result_goal_state)
        elif algo_to_run_calc == 'Q-Learning':  # Q-Learning không phải "(Console)"
            path = AI.q_study(begin, result_goal_state, episodes=100)  # episodes có thể điều chỉnh

        elif algo_to_run_calc == 'AND-OR (Console)':
            print(f"\n--- Chạy {algo_to_run_calc} trên Console ---")
            AI.And_Or_Search(begin, result_goal_state)  # AI.And_Or_Search trả về None
            print(f"--- Kết thúc {algo_to_run_calc} ---")
            path = None
        elif algo_to_run_calc == 'Belief State (Console)':
            print(f"\n--- Chạy {algo_to_run_calc} trên Console ---")
            path = AI.Belief_State_Search(begin, result_goal_state)  # Belief_State_Search có thể trả path
            if path:
                print(f"Belief State Search tìm thấy path {len(path) - 1} bước.")
            else:
                print("Belief State Search không tìm thấy path.")
            print(f"--- Kết thúc {algo_to_run_calc} ---")
            # UI sẽ xử lý path này bình thường
        elif algo_to_run_calc == 'Belief 1 Part (Console)':
            print(f"\n--- Chạy {algo_to_run_calc} trên Console ---")
            # Hiện tại không có hàm AI.Belief_1_Part_Function() tương ứng
            print("     (Thuật toán này chưa có hàm thực thi trong AI.py)")
            print(f"--- Kết thúc {algo_to_run_calc} ---")
            path = None
        else:
            print(f"Thuật toán không xác định: {algo_to_run_calc}")
            path = None

        end_time_calc = pygame.time.get_ticks()
        search_time_sec = (end_time_calc - start_time_calc) / 1000.0
        show_search_info = True;
        is_calculating_path = False

        if path is None or not path:
            print(f"Không tìm thấy lời giải cho {algo_to_run_calc}.")
            done = True;
            solving = False
        else:
            print(f"Tìm thấy lời giải: {len(path) - 1 if len(path) > 0 else 0} bước cho {algo_to_run_calc}.")
            current = copy.deepcopy(path[0] if path else begin)
            solving = True;
            done = False;
            index = 0
            if len(path) == 1: done = True

            # --- Vẽ màn hình ---
    screen.fill(MAIN_SCREEN_BACKGROUND)
    title_y_bottom = draw_text_label_ui(TITLE_TEXT, FONT_TITLE_MAIN, WHITE_TEXT, SCREEN_WIDTH // 2, TITLE_BAR_Y_OFFSET,
                                        BLUE_BG, TITLE_BG_PADDING_X, TITLE_BG_PADDING_Y,
                                        border_radius=TITLE_BG_BORDER_RADIUS) + 20

    if not inputting:
        # --- Cột Trái ---
        y_draw_left = title_y_bottom
        draw_text_label_ui("TRẠNG THÁI ĐẦU", FONT_TITLE_SECTION, TEXT_INFO_COLOR,
                           LEFT_COL_X_START_UI + LEFT_COL_WIDTH_UI // 2, y_draw_left)
        y_draw_left += FONT_TITLE_SECTION.get_height() + 8
        draw_puzzle_ui(begin, (LEFT_COL_X_START_UI + (LEFT_COL_WIDTH_UI - STATIC_PUZZLE_SIZE_UI) // 2, y_draw_left),
                       STATIC_PUZZLE_SIZE_UI)
        y_draw_left += STATIC_PUZZLE_SIZE_UI + 8
        if solvability_message_ui:
            draw_text_label_ui(solvability_message_ui, FONT_EXTRA_INFO,
                               TEXT_INFO_COLOR if "Có thể giải" in solvability_message_ui else ERROR_TEXT_COLOR,
                               LEFT_COL_X_START_UI + LEFT_COL_WIDTH_UI // 2, y_draw_left)
            y_draw_left += FONT_EXTRA_INFO.get_height() + 12
        draw_text_label_ui("TRẠNG THÁI ĐÍCH", FONT_TITLE_SECTION, TEXT_INFO_COLOR,
                           LEFT_COL_X_START_UI + LEFT_COL_WIDTH_UI // 2, y_draw_left)
        y_draw_left += FONT_TITLE_SECTION.get_height() + 8
        draw_puzzle_ui(result_goal_state,
                       (LEFT_COL_X_START_UI + (LEFT_COL_WIDTH_UI - STATIC_PUZZLE_SIZE_UI) // 2, y_draw_left),
                       STATIC_PUZZLE_SIZE_UI)
        y_draw_left += STATIC_PUZZLE_SIZE_UI + 25

        btn_h_control = 40;
        btn_spacing_control = 10
        btn_random_rect = button_ui(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control, "NGẪU NHIÊN",
                                    ORANGE_BUTTON_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control).collidepoint(
                            mouse_pos_main) and not solving and not is_calculating_path))
        y_draw_left += btn_h_control + btn_spacing_control
        btn_input_main_rect = button_ui(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control, "NHẬP TAY",
                                        ORANGE_BUTTON_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control).collidepoint(
                            mouse_pos_main) and not solving and not is_calculating_path))
        y_draw_left += btn_h_control + btn_spacing_control
        btn_solve_main_rect = button_ui(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control, "GIẢI",
                                        GREEN_BUTTON_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control).collidepoint(
                            mouse_pos_main) and selected_algo_name and not solving and not is_calculating_path and AI.is_solvable(
                    begin)))
        y_draw_left += btn_h_control + btn_spacing_control
        btn_show_goal_main_rect = button_ui(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control,
                                            "XEM KẾT QUẢ", PURPLE_BUTTON_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START_UI, y_draw_left, LEFT_COL_WIDTH_UI, btn_h_control).collidepoint(
                            mouse_pos_main) and not is_calculating_path))

        # --- Cột Giữa ---
        mid_col_x_start = LEFT_COL_X_START_UI + LEFT_COL_WIDTH_UI + 25
        right_col_total_w = (2 * uniform_algo_button_width_ui) + algo_horizontal_spacing_ui
        right_col_x_start = SCREEN_WIDTH - right_col_total_w - 25
        mid_col_width = right_col_x_start - mid_col_x_start - 25

        main_puzzle_h_avail = SCREEN_HEIGHT - title_y_bottom - 130  # Chừa chỗ cho nút điều khiển và text
        main_puzzle_size = min(mid_col_width - 20, main_puzzle_h_avail)
        main_puzzle_size = max(main_puzzle_size, 280)

        main_puzzle_x_draw = mid_col_x_start + (mid_col_width - main_puzzle_size) // 2
        main_puzzle_y_draw = title_y_bottom
        draw_puzzle_ui(current, (main_puzzle_x_draw, main_puzzle_y_draw), main_puzzle_size)

        y_mid_controls = main_puzzle_y_draw + main_puzzle_size + 20
        mid_btn_w = (main_puzzle_size - 2 * 10) // 3;
        mid_btn_w = max(mid_btn_w, 70)
        mid_btn_h = 40

        mid_btn_group_w = 3 * mid_btn_w + 2 * 10
        prev_x = main_puzzle_x_draw + (main_puzzle_size - mid_btn_group_w) // 2
        reset_x = prev_x + mid_btn_w + 10
        next_x = reset_x + mid_btn_w + 10

        btn_prev_main_rect = button_ui(prev_x, y_mid_controls, mid_btn_w, mid_btn_h, "LÙI", BLUE_BG, WHITE_TEXT,
                                       is_hovered=(pygame.Rect(prev_x, y_mid_controls, mid_btn_w,
                                                               mid_btn_h).collidepoint(
                                           mouse_pos_main) and path and not is_calculating_path))
        btn_reset_main_rect = button_ui(reset_x, y_mid_controls, mid_btn_w, mid_btn_h, "RESET", BLUE_BG, WHITE_TEXT,
                                        is_hovered=(pygame.Rect(reset_x, y_mid_controls, mid_btn_w,
                                                                mid_btn_h).collidepoint(
                                            mouse_pos_main) and not is_calculating_path))
        btn_next_main_rect = button_ui(next_x, y_mid_controls, mid_btn_w, mid_btn_h, "TIẾN", BLUE_BG, WHITE_TEXT,
                                       is_hovered=(pygame.Rect(next_x, y_mid_controls, mid_btn_w,
                                                               mid_btn_h).collidepoint(
                                           mouse_pos_main) and path and not is_calculating_path))

        y_info_text = y_mid_controls + mid_btn_h + 15
        steps_display_text = f"Số bước: {index}/{len(path) - 1 if path and len(path) > 0 else '0'}"
        y_info_text = draw_text_label_ui(steps_display_text, FONT_STEP_INFO, TEXT_INFO_COLOR,
                                         mid_col_x_start + mid_col_width // 2, y_info_text) + 5
        if show_search_info:
            time_text = f"Thời gian tìm: {search_time_sec:.3f} s"
            y_info_text = draw_text_label_ui(time_text, FONT_EXTRA_INFO, TEXT_INFO_COLOR,
                                             mid_col_x_start + mid_col_width // 2, y_info_text) + 5
            if not path and selected_algo_name and not is_calculating_path:
                no_sol_msg = f"{selected_algo_name}: Không tìm thấy lời giải."
                if "AC-3" in selected_algo_name and begin != result_goal_state:
                    no_sol_msg = f"{selected_algo_name}: Trạng thái không nhất quán."
                elif "không thể giải" in selected_algo_name:
                    no_sol_msg = selected_algo_name  # Giữ nguyên thông báo từ nút Solve
                draw_text_label_ui(no_sol_msg, FONT_EXTRA_INFO, ERROR_TEXT_COLOR, mid_col_x_start + mid_col_width // 2,
                                   y_info_text)

        # --- Cột Phải ---
        algo_header_text = "CHỌN THUẬT TOÁN"
        algo_header_bg = DARK_BLUE_BUTTON_BG
        if is_calculating_path:
            algo_header_text = f"ĐANG TÌM: {selected_algo_name}..."; algo_header_bg = SEARCHING_BG_COLOR
        elif solving and not done and path:
            algo_header_text = f"ĐANG GIẢI: {selected_algo_name}"
        elif done and path and (index == len(path) - 1 or (len(path) == 1 and index == 0)):
            algo_header_text = f"HOÀN THÀNH: {selected_algo_name}!"; algo_header_bg = SUCCESS_BG_COLOR
        elif done and not path:
            algo_header_text = f"KTTLG / LỖI: {selected_algo_name}"; algo_header_bg = RED_BUTTON_BG
        elif selected_algo_name:
            algo_header_text = f"Đã chọn: {selected_algo_name}"; algo_header_bg = (80, 80, 80)

        y_algo_buttons_start = draw_text_label_ui(algo_header_text, FONT_TITLE_SECTION, WHITE_TEXT,
                                                  right_col_x_start + right_col_total_w // 2, title_y_bottom,
                                                  algo_header_bg, 15, 8, right_col_total_w, 10) + 15

        algo_buttons_rect_cache_ui = []
        algo_col = 0
        y_curr_algo_btn = y_algo_buttons_start
        for i, name_algo_disp in enumerate(algorithm_display_names_list):
            x_algo_btn = right_col_x_start + (algo_col * (uniform_algo_button_width_ui + algo_horizontal_spacing_ui))

            is_hover = pygame.Rect(x_algo_btn, y_curr_algo_btn, uniform_algo_button_width_ui,
                                   algo_button_height_ui).collidepoint(
                mouse_pos_main) and not solving and not is_calculating_path
            is_sel = selected_algo_name == name_algo_disp

            btn_rect_cache = button_ui(x_algo_btn, y_curr_algo_btn, uniform_algo_button_width_ui, algo_button_height_ui,
                                       name_algo_disp, DARK_BLUE_BUTTON_BG, WHITE_TEXT, FONT_BUTTON_ALGO, 8, is_hover,
                                       is_sel)
            algo_buttons_rect_cache_ui.append((btn_rect_cache, name_algo_disp, name_algo_disp, 0))

            algo_col += 1
            if algo_col >= 2: algo_col = 0; y_curr_algo_btn += algo_button_height_ui + algo_button_spacing_ui

        # Animation
        if solving and not done and path and not is_calculating_path:
            if current_time_ticks_main - last_update_time_anim > animation_speed_ms:
                last_update_time_anim = current_time_ticks_main
                if 0 <= index < len(path) - 1:
                    index += 1; current = copy.deepcopy(path[index])
                elif index >= len(path) - 1:
                    done = True; current = copy.deepcopy(path[-1])

    else:  # --- Màn hình Nhập Tay UI ---
        y_draw_input_scr = title_y_bottom
        input_scr_padding_x = 40

        # Phần Puzzle đang nhập (bên trái)
        input_puzzle_area_w = SCREEN_WIDTH // 2 - input_scr_padding_x
        input_puzzle_center_x = input_scr_padding_x + input_puzzle_area_w // 2
        draw_text_label_ui("Puzzle Bạn Nhập:", FONT_TITLE_SECTION, TEXT_INFO_COLOR, input_puzzle_center_x,
                           y_draw_input_scr)
        y_draw_input_scr += FONT_TITLE_SECTION.get_height() + 15
        input_puzzle_disp_size = 300
        draw_puzzle_ui(puzzle_input, (input_puzzle_center_x - input_puzzle_disp_size // 2, y_draw_input_scr),
                       input_puzzle_disp_size)

        # Phần chọn số (bên phải)
        num_select_area_x_start = SCREEN_WIDTH // 2 + input_scr_padding_x // 2
        num_select_area_w = SCREEN_WIDTH // 2 - input_scr_padding_x * 1.5
        num_select_center_x = num_select_area_x_start + num_select_area_w // 2

        y_draw_input_scr_right = title_y_bottom
        draw_text_label_ui("Chọn số (0-8):", FONT_TITLE_SECTION, TEXT_INFO_COLOR, num_select_center_x,
                           y_draw_input_scr_right)
        y_draw_input_scr_right += FONT_TITLE_SECTION.get_height() + 20

        block_w_in, block_h_in, spacing_in = 75, 75, 12
        blocks_total_w_in = 3 * block_w_in + 2 * spacing_in
        blocks_start_x_in = num_select_center_x - blocks_total_w_in // 2

        for idx_b, (r_b, v_b) in enumerate(blocks_input_ui):  # Sử dụng blocks_input_ui đã khởi tạo
            r_idx_b, c_idx_b = divmod(idx_b, 3)
            x_b = blocks_start_x_in + c_idx_b * (block_w_in + spacing_in)
            y_b = y_draw_input_scr_right + r_idx_b * (block_h_in + spacing_in)
            r_b.topleft = (x_b, y_b);
            r_b.size = (block_w_in, block_h_in)  # Cập nhật rect

            is_used_b = any(cell_val == v_b and puzzle_input_check[r_check][c_check] == 1
                            for r_check, row_c in enumerate(puzzle_input) for c_check, cell_val in enumerate(row_c))

            bg_b = (210, 210, 210) if is_used_b else WHITE_TEXT
            txt_b_color = (160, 160, 160) if is_used_b else TEXT_INFO_COLOR
            pygame.draw.rect(screen, bg_b, r_b, 0, 8)
            pygame.draw.rect(screen, PUZZLE_BORDER_COLOR, r_b, 2, 8)
            font_b = pygame.font.Font(FONT_FILE_NAME if FONT_FILE_NAME and os.path.exists(FONT_FILE_NAME) else None,
                                      int(block_h_in * 0.6))
            surf_b = font_b.render(str(v_b), True, txt_b_color)
            rect_b = surf_b.get_rect(center=r_b.center)
            screen.blit(surf_b, rect_b)

        # Nút điều khiển màn hình nhập
        btn_w_in_scr, btn_h_in_scr, btn_spacing_in_scr = 180, 45, 20
        y_btns_in_scr = SCREEN_HEIGHT - btn_h_in_scr - 30
        total_w_3btns_in_scr = 3 * btn_w_in_scr + 2 * btn_spacing_in_scr
        start_x_3btns_in_scr = (SCREEN_WIDTH - total_w_3btns_in_scr) // 2

        btn_back_x_is = start_x_3btns_in_scr
        btn_reset_x_is = btn_back_x_is + btn_w_in_scr + btn_spacing_in_scr
        btn_ok_x_is = btn_reset_x_is + btn_w_in_scr + btn_spacing_in_scr

        btn_back_input_rect = button_ui(btn_back_x_is, y_btns_in_scr, btn_w_in_scr, btn_h_in_scr, 'QUAY LẠI',
                                        RED_BUTTON_BG, WHITE_TEXT,
                                        is_hovered=pygame.Rect(btn_back_x_is, y_btns_in_scr, btn_w_in_scr,
                                                               btn_h_in_scr).collidepoint(mouse_pos_main))
        btn_reset_puzzle_input_rect = button_ui(btn_reset_x_is, y_btns_in_scr, btn_w_in_scr, btn_h_in_scr, 'NHẬP LẠI',
                                                LIGHT_BLUE_BUTTON_BG, WHITE_TEXT,
                                                is_hovered=pygame.Rect(btn_reset_x_is, y_btns_in_scr, btn_w_in_scr,
                                                                       btn_h_in_scr).collidepoint(mouse_pos_main))
        btn_ok_input_rect = button_ui(btn_ok_x_is, y_btns_in_scr, btn_w_in_scr, btn_h_in_scr, 'XÁC NHẬN',
                                      GREEN_BUTTON_BG, WHITE_TEXT,
                                      is_hovered=pygame.Rect(btn_ok_x_is, y_btns_in_scr, btn_w_in_scr,
                                                             btn_h_in_scr).collidepoint(mouse_pos_main))

        if selected_algo_name:  # Hiển thị thông báo lỗi/trạng thái (tái sử dụng biến selected_algo_name)
            y_msg_in_scr = y_btns_in_scr - FONT_STEP_INFO.get_height() - 20
            msg_bg_in_scr = ERROR_TEXT_COLOR if "lỗi" in selected_algo_name.lower() or "không" in selected_algo_name.lower() or "chưa" in selected_algo_name.lower() else (
            180, 180, 180)
            msg_txt_color_in_scr = WHITE_TEXT if "lỗi" in selected_algo_name.lower() else TEXT_INFO_COLOR
            draw_text_label_ui(selected_algo_name, FONT_STEP_INFO, msg_txt_color_in_scr, SCREEN_WIDTH // 2,
                               y_msg_in_scr, msg_bg_in_scr, 15, 8, SCREEN_WIDTH * 0.75, 8)

    pygame.display.flip()

pygame.quit()
sys.exit()