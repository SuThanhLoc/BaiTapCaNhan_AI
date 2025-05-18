import pygame
import random
import AI
import sys
import os

pygame.init()
pygame.font.init()

pygame.display.set_caption("8-puzzle")
screen = pygame.display.set_mode((1200, 850))

FONT_FILE_NAME = "Roboto-Regular.ttf"
FONT_SIZE_TITLE_MAIN = 36
FONT_SIZE_TITLE_SECTION = 22
FONT_SIZE_BUTTON_CONTROL = 20
FONT_SIZE_BUTTON_ALGO = 16
FONT_SIZE_STEP_INFO = 20
FONT_EXTRA_INFO_SIZE = 18
try:
    FONT_TITLE_MAIN = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_TITLE_MAIN)
    FONT_TITLE_SECTION = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_TITLE_SECTION)
    FONT_BUTTON_CONTROL = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_BUTTON_CONTROL)
    FONT_BUTTON_ALGO = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_BUTTON_ALGO)
    FONT_STEP_INFO = pygame.font.Font(FONT_FILE_NAME, FONT_SIZE_STEP_INFO)
    FONT_EXTRA_INFO = pygame.font.Font(FONT_FILE_NAME, FONT_EXTRA_INFO_SIZE)
    print(f"Đã tải font thành công từ: {FONT_FILE_NAME}")
except pygame.error as e:
    print(f"LỖI: Không thể tải font '{FONT_FILE_NAME}': {e}. Sử dụng font mặc định.")
    FONT_TITLE_MAIN = pygame.font.Font(None, FONT_SIZE_TITLE_MAIN + 6)
    FONT_TITLE_SECTION = pygame.font.Font(None, FONT_SIZE_TITLE_SECTION + 4)
    FONT_BUTTON_CONTROL = pygame.font.Font(None, FONT_SIZE_BUTTON_CONTROL + 4)
    FONT_BUTTON_ALGO = pygame.font.Font(None, FONT_SIZE_BUTTON_ALGO + 4)
    FONT_STEP_INFO = pygame.font.Font(None, FONT_SIZE_STEP_INFO + 4)
    FONT_EXTRA_INFO = pygame.font.Font(None, FONT_EXTRA_INFO_SIZE + 4)

BLUE_BG = (142, 30, 32)
WHITE_TEXT = (236, 236, 236)
MAIN_SCREEN_BACKGROUND = (215, 215, 215)
NUMBERED_CELL_BG = BLUE_BG
EMPTY_CELL_BG = (215, 215, 215)
PUZZLE_BORDER_COLOR = (215, 215, 215)
CELL_BORDER_RADIUS = 10
DARK_RED_BUTTON_BG = (27, 79, 147)
SELECTED_HIGHLIGHT_COLOR = (244, 244, 0)
HOVER_OFFSET = -2
SEARCHING_BG_COLOR = (100, 100, 100)
TEXT_INFO_COLOR = (50, 50, 50)

TITLE_TEXT = "8 PUZZLE GAME"
TITLE_BAR_Y_OFFSET = 10
TITLE_BG_PADDING_X = 40
TITLE_BG_PADDING_Y = 10
TITLE_BG_BORDER_RADIUS = 15

def is_solvable(puzzle_state):
    flat_puzzle = [num for row in puzzle_state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]: inversions += 1
    return inversions % 2 == 0

def random_puzzle():
    while True:
        nums = list(range(9))
        random.shuffle(nums)
        puzzle = [nums[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(puzzle): return puzzle

def create_blocks_for_input():
    new_blocks = []
    block_width_input, block_height_input = 80, 80
    for i in range(9):
        rect = pygame.Rect(0, 0, block_width_input, block_height_input)
        new_blocks.append((rect, i))
    return new_blocks

def button(x, y, width, height, text, base_color, text_color, font_obj=None, border_radius=5, is_hovered=False,
           is_selected=False):
    if font_obj is None: font_obj = FONT_BUTTON_CONTROL
    draw_x, draw_y = x, y
    current_bg_color = base_color
    if is_hovered and not is_selected:
        draw_x += HOVER_OFFSET
        draw_y += HOVER_OFFSET
    pygame.draw.rect(screen, current_bg_color, (draw_x, draw_y, width, height), 0, border_radius=border_radius)
    if is_selected:
        highlight_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(screen, SELECTED_HIGHLIGHT_COLOR, highlight_rect, 2, border_radius=border_radius + 2)
    text_surface = font_obj.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    if is_hovered and not is_selected:
        text_rect.center = (draw_x + width // 2, draw_y + height // 2)
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def draw_text_label(text, font_obj, color, center_x, y, background_color=None, padding_x=10, padding_y=5,
                    width_override=None, border_radius=3, text_align_center=True):
    text_surface = font_obj.render(text, True, color)
    text_rect_temp = text_surface.get_rect()
    if background_color:
        bg_width = width_override if width_override is not None else text_rect_temp.width + 2 * padding_x
        bg_height = text_rect_temp.height + 2 * padding_y
        bg_rect = pygame.Rect(0, 0, bg_width, bg_height)
        if text_align_center:
            bg_rect.centerx = center_x
        else:
            bg_rect.x = center_x - padding_x
        bg_rect.y = y
        pygame.draw.rect(screen, background_color, bg_rect, 0, border_radius=border_radius)
        text_final_rect = text_surface.get_rect(center=bg_rect.center)
        screen.blit(text_surface, text_final_rect)
        return bg_rect.bottom
    else:
        if text_align_center:
            text_final_rect = text_surface.get_rect(centerx=center_x, top=y)
        else:
            text_final_rect = text_surface.get_rect(left=center_x, top=y)
        screen.blit(text_surface, text_final_rect)
        return text_final_rect.bottom

def draw_puzzle(puzzle_state, pos, puzzle_total_size=300):
    cell_size = puzzle_total_size // 3
    font_size_dynamic = int(cell_size * 0.55)
    try:
        dynamic_puzzle_font = pygame.font.Font(FONT_FILE_NAME, font_size_dynamic)
    except:
        dynamic_puzzle_font = pygame.font.Font(None, font_size_dynamic + 6)

    for i in range(3):
        for j in range(3):
            number = puzzle_state[i][j]
            rect_x, rect_y = pos[0] + j * cell_size, pos[1] + i * cell_size
            cell_rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)

            cell_bg_color = NUMBERED_CELL_BG if number != 0 else EMPTY_CELL_BG
            pygame.draw.rect(screen, cell_bg_color, cell_rect, border_radius=CELL_BORDER_RADIUS)
            pygame.draw.rect(screen, PUZZLE_BORDER_COLOR, cell_rect, 2,
                             border_radius=CELL_BORDER_RADIUS)

            if number != 0:
                text_surface = dynamic_puzzle_font.render(str(number), True, WHITE_TEXT)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                screen.blit(text_surface, text_rect)

def add_number_to_input(current_puzzle_input, number_to_add):
    for i in range(3):
        for j in range(3):
            if puzzle_input_check[i][j] == 0:
                current_puzzle_input[i][j] = number_to_add
                puzzle_input_check[i][j] = 1
                return True
    return False

def reset_input_puzzle_state():
    global puzzle_input, puzzle_input_check, blocks
    puzzle_input = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    puzzle_input_check = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    blocks = create_blocks_for_input()

def reset_all_game_states():
    global begin, current, path, index, solving, done, selected, text_box_algorithm, algorithm_dict
    global is_calculating_path, search_time_sec, show_search_info, solvability_message

    begin = random_puzzle()
    current = begin
    path = []
    index = 0
    solving = False
    done = False
    selected = False
    text_box_algorithm = ''
    is_calculating_path = False
    search_time_sec = 0.0
    show_search_info = False
    if is_solvable(begin):
        solvability_message = "Trạng thái: Có thể giải"
    else:
        solvability_message = "Trạng thái: Không thể giải!"

    for key in algorithm_dict: algorithm_dict[key] = False
    reset_input_puzzle_state()

running = True
solving = False
inputting = False
selected = False
done = False
is_calculating_path = False
speed = 300
search_time_sec = 0.0
show_search_info = False
solvability_message = ""

begin = random_puzzle()
current = begin
path = []
if is_solvable(begin):
    solvability_message = "Trạng thái: Có thể giải"
else:
    solvability_message = "Trạng thái: Không thể giải!"

puzzle_input = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
puzzle_input_check = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
result = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
algorithm_dict_display_names = ['Breadth-First Search', 'Uniform Cost Search', 'Depth-First Search',
                                'Iterative Deepening DFS', 'Greedy Search', 'A* Search', 'IDA* Search',
                                'Simple Hill Climbing', 'Stochastic Hill Climbing', 'Steepest Ascent HC',
                                'Simulated Annealing', 'Beam Search', 'Genetic Algorithm', 'AND-OR (Console)',
                                'Belief State (Console)', 'Backtracking Search', 'Belief 1 Part (Console)',
                                'Q-Learning', 'Forward Checking']
algorithm_dict = {name: False for name in algorithm_dict_display_names}
blocks = create_blocks_for_input()
text_box_algorithm = ''
index = 0

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 850

LEFT_COL_X_START = 30
LEFT_COL_WIDTH = 202
STATIC_PUZZLE_SIZE = 200

algo_button_height = 35
algo_button_spacing = 8
algo_horizontal_spacing = 10
algo_padding_x = 10
uniform_algo_button_width = 200

btn_random = pygame.Rect(0, 0, 0, 0)
btn_input_main = pygame.Rect(0, 0, 0, 0)
btn_solve_main = pygame.Rect(0, 0, 0, 0)
btn_show_goal_main = pygame.Rect(0, 0, 0, 0)
btn_prev_main = pygame.Rect(0, 0, 0, 0)
btn_reset_main = pygame.Rect(0, 0, 0, 0)
btn_next_main = pygame.Rect(0, 0, 0, 0)
btn_back_input = pygame.Rect(0, 0, 0, 0)
btn_ok_input = pygame.Rect(0, 0, 0, 0)
btn_reset_puzzle_input = pygame.Rect(0, 0, 0, 0)
algo_buttons_list_cache = []

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not inputting:
                action_taken_this_click = False
                if btn_random.collidepoint(mouse_pos) and not solving and not is_calculating_path:
                    reset_all_game_states()
                    show_search_info = False
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_input_main.collidepoint(
                        mouse_pos) and not solving and not is_calculating_path:
                    inputting = True
                    reset_input_puzzle_state()
                    text_box_algorithm = ""
                    solvability_message = ""
                    show_search_info = False
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_solve_main.collidepoint(
                        mouse_pos) and not solving and selected and not is_calculating_path:
                    if begin == result:
                        path = [begin]
                        solving = True;
                        done = True;
                        index = 0;
                        current = begin
                        show_search_info = True;
                        search_time_sec = 0.0
                    elif text_box_algorithm:
                        is_calculating_path = True
                        start_time = pygame.time.get_ticks()
                        actual_algo_name = text_box_algorithm

                        if actual_algo_name == 'Breadth-First Search':
                            path = AI.BFS(begin, result)
                        elif actual_algo_name == 'Uniform Cost Search':
                            path = AI.Uniform_Cost_Search(begin, result)
                        elif actual_algo_name == 'Depth-First Search':
                            path = AI.DFS(begin, result)
                        elif actual_algo_name == 'Iterative Deepening DFS':
                            path = AI.Iterative_Deepening_DFS(begin, result)
                        elif actual_algo_name == 'Greedy Search':
                            path = AI.Greedy_Search(begin, result)
                        elif actual_algo_name == 'A* Search':
                            path = AI.A_Star_Search(begin, result)
                        elif actual_algo_name == 'IDA* Search':
                            path = AI.IDA(begin, result, 30)
                        elif actual_algo_name == 'Simple Hill Climbing':
                            path = AI.Simple_Hill_Climbing(begin, result)
                        elif actual_algo_name == 'Stochastic Hill Climbing':
                            path = AI.Stochastic_Hill_Climbing(begin, result)
                        elif actual_algo_name == 'Steepest Ascent HC':
                            path = AI.Steepest_Ascent_Hill_Climbing(begin, result)
                        elif actual_algo_name == 'Simulated Annealing':
                            path = AI.Simulated_Annealing(begin, result)
                        elif actual_algo_name == 'Beam Search':
                            path = AI.Beam_Search(begin, result, 5)
                        elif actual_algo_name == 'Genetic Algorithm':
                            ga_path = AI.Genetic_Algorithm(begin, result, 50, 100)
                            path = [s for s in ga_path if isinstance(s, list) and len(s) == 3] if ga_path else None
                            if path and path[-1] != result: path = None
                        elif actual_algo_name in ['AND-OR (Console)', 'Belief State (Console)',
                                                  'Belief 1 Part (Console)']:
                            print(f"{text_box_algorithm} chạy ở console.")
                            if actual_algo_name == 'AND-OR (Console)': AI.And_Or_Search(begin, result)
                            path = None
                        elif actual_algo_name == 'Backtracking Search':
                            path = AI.Backtracking(begin, result, depth=30)
                        elif actual_algo_name == 'Q-Learning':
                            path = AI.q_study(begin, result, episodes=10)
                        elif actual_algo_name == 'Forward Checking':
                            path = AI.Forward_Checking(begin, result, depth=30)
                        else:
                            path = None

                        end_time = pygame.time.get_ticks()
                        search_time_sec = (end_time - start_time) / 1000.0
                        show_search_info = True
                        is_calculating_path = False

                        if path is None or not path:
                            print(f"Không tìm thấy lời giải cho {text_box_algorithm}.")
                            done = True
                            solving = False
                        else:
                            print(f"Tìm thấy lời giải: {len(path)} bước.")
                            current = path[0] if path else begin
                            solving = True
                            done = False
                            index = 0
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_show_goal_main.collidepoint(mouse_pos):
                    if solving and not done and path:
                        if path:
                            index = len(path) - 1
                            current = path[index]
                            done = True
                            print(f"Bỏ qua animation của '{text_box_algorithm}', hiển thị kết quả cuối.")
                    else:
                        current = result
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_prev_main.collidepoint(mouse_pos) and path:
                    if index > 0: index -= 1; current = path[index]
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_reset_main.collidepoint(mouse_pos):
                    reset_all_game_states()
                    show_search_info = False
                    action_taken_this_click = True
                elif not action_taken_this_click and btn_next_main.collidepoint(mouse_pos) and path:
                    if index < len(path) - 1: index += 1; current = path[index]
                    action_taken_this_click = True

                if not action_taken_this_click and not solving and not is_calculating_path:
                    for btn_r, algo_name_disp, _, _ in algo_buttons_list_cache:
                        if btn_r.collidepoint(mouse_pos):
                            text_box_algorithm = algo_name_disp
                            selected = True
                            print(f"Đã chọn thuật toán: {text_box_algorithm}")
                            break
            else:
                if btn_back_input.collidepoint(mouse_pos):
                    inputting = False
                    text_box_algorithm = ""
                    if is_solvable(begin):
                        solvability_message = "Trạng thái: Có thể giải"
                    else:
                        solvability_message = "Trạng thái: Không thể giải!"

                elif btn_ok_input.collidepoint(mouse_pos):
                    flat_check = [item for sublist in puzzle_input_check for item in sublist]
                    if all(cell == 1 for cell in flat_check):
                        flat_puzzle = [item for sublist in puzzle_input for item in sublist]
                        if len(set(flat_puzzle)) == 9 and all(
                                0 <= x <= 8 for x in flat_puzzle):
                            if is_solvable(puzzle_input):
                                temp_begin = [row[:] for row in puzzle_input]
                                reset_all_game_states()
                                begin = temp_begin
                                current = begin
                                if is_solvable(begin):
                                    solvability_message = "Trạng thái: Có thể giải"
                                else:
                                    solvability_message = "Trạng thái: Không thể giải!"
                                inputting = False
                                show_search_info = False
                            else:
                                text_box_algorithm = "Puzzle bạn nhập không thể giải được!"
                        else:
                            text_box_algorithm = "Input không hợp lệ (số trùng hoặc ngoài phạm vi 0-8)!"
                    else:
                        text_box_algorithm = "Chưa nhập đủ 9 số!"
                elif btn_reset_puzzle_input.collidepoint(mouse_pos):
                    reset_input_puzzle_state()
                    text_box_algorithm = ""

                for r_rect, val_block_event in blocks:
                    if r_rect.collidepoint(mouse_pos):
                        is_val_used = False
                        temp_flat_input = [num for row in puzzle_input for num in row]
                        if val_block_event in temp_flat_input and val_block_event != 0:
                            found_in_filled_cell = False
                            for r_idx, row_val in enumerate(puzzle_input):
                                for c_idx, cell_val in enumerate(row_val):
                                    if cell_val == val_block_event and puzzle_input_check[r_idx][c_idx] == 1:
                                        found_in_filled_cell = True
                                        break
                                if found_in_filled_cell: break
                            if found_in_filled_cell: is_val_used = True

                        elif val_block_event == 0:
                            zero_already_placed = False
                            for r_idx, row_val in enumerate(puzzle_input):
                                for c_idx, cell_val in enumerate(row_val):
                                    if cell_val == 0 and puzzle_input_check[r_idx][c_idx] == 1:
                                        zero_already_placed = True
                                        break
                                if zero_already_placed: break
                            if zero_already_placed: is_val_used = True

                        if not is_val_used:
                            if not add_number_to_input(puzzle_input, val_block_event):
                                text_box_algorithm = "Puzzle input đã đầy!"
                        else:
                            text_box_algorithm = f"Số {val_block_event} đã được dùng!"
                        break

    screen.fill(MAIN_SCREEN_BACKGROUND)

    title_text_render_surface = FONT_TITLE_MAIN.render(TITLE_TEXT, True, WHITE_TEXT)
    title_text_render_rect = title_text_render_surface.get_rect()
    title_bg_actual_width = title_text_render_rect.width + 2 * TITLE_BG_PADDING_X
    title_bg_actual_height = title_text_render_rect.height + 2 * TITLE_BG_PADDING_Y
    title_bg_final_rect = pygame.Rect((SCREEN_WIDTH - title_bg_actual_width) // 2, TITLE_BAR_Y_OFFSET,
                                      title_bg_actual_width, title_bg_actual_height)
    pygame.draw.rect(screen, BLUE_BG, title_bg_final_rect, 0, border_radius=TITLE_BG_BORDER_RADIUS)
    title_text_final_rect = title_text_render_surface.get_rect(center=title_bg_final_rect.center)
    screen.blit(title_text_render_surface, title_text_final_rect)
    effective_title_bar_bottom = title_bg_final_rect.bottom

    if not inputting:
        font_h_section = FONT_TITLE_SECTION.get_height() if FONT_TITLE_SECTION else 22
        font_h_extra_info = FONT_EXTRA_INFO.get_height() if FONT_EXTRA_INFO else 18

        label_tt_dau_y_new = effective_title_bar_bottom + 20
        begin_puzzle_pos_y_new = label_tt_dau_y_new + font_h_section + 10
        solvability_text_y_new = begin_puzzle_pos_y_new + STATIC_PUZZLE_SIZE + 5
        label_tt_dich_y_new = solvability_text_y_new + font_h_extra_info + 15
        result_puzzle_pos_y_new = label_tt_dich_y_new + font_h_section + 10
        btn_left_y_start_new = result_puzzle_pos_y_new + STATIC_PUZZLE_SIZE + 30
        left_button_height_val = 40
        left_button_spacing_val = 10

        dynamic_status_header_y_new = effective_title_bar_bottom + 20

        MID_COL_X_START = LEFT_COL_X_START + LEFT_COL_WIDTH + 30
        est_right_col_width = 2 * uniform_algo_button_width + algo_horizontal_spacing + 30
        MID_COL_WIDTH_val = SCREEN_WIDTH - MID_COL_X_START - est_right_col_width - 30

        main_puzzle_display_y_new = label_tt_dau_y_new

        available_height_for_mid_puzzle = btn_left_y_start_new - main_puzzle_display_y_new - 80
        MAIN_PUZZLE_SIZE_val = min(MID_COL_WIDTH_val - 20, available_height_for_mid_puzzle)
        MAIN_PUZZLE_SIZE_val = max(MAIN_PUZZLE_SIZE_val, 150)

        mid_button_height_const = 40
        mid_button_width_val = (MAIN_PUZZLE_SIZE_val - 2 * 10) // 3
        mid_button_width_val = max(mid_button_width_val, 60)

        current_y_mid_buttons_draw_val = main_puzzle_display_y_new + MAIN_PUZZLE_SIZE_val + 20
        step_text_y_draw_val = current_y_mid_buttons_draw_val + mid_button_height_const + 15

    if not inputting:
        if (solving and not done and path) or (done and path):
            if path and 0 <= index < len(path):
                current = path[index]
            elif path:
                current = path[-1]
        elif not is_calculating_path:
            current = begin

        draw_text_label("TRẠNG THÁI ĐẦU", FONT_TITLE_SECTION, (0, 0, 0),
                        LEFT_COL_X_START + LEFT_COL_WIDTH // 2, label_tt_dau_y_new, text_align_center=True)
        draw_puzzle(begin, (LEFT_COL_X_START + (LEFT_COL_WIDTH - STATIC_PUZZLE_SIZE) // 2, begin_puzzle_pos_y_new),
                    STATIC_PUZZLE_SIZE)

        if solvability_message:
            draw_text_label(solvability_message, FONT_EXTRA_INFO, TEXT_INFO_COLOR,
                            LEFT_COL_X_START + LEFT_COL_WIDTH // 2, solvability_text_y_new, text_align_center=True)

        draw_text_label("TRẠNG THÁI ĐÍCH", FONT_TITLE_SECTION, (0, 0, 0),
                        LEFT_COL_X_START + LEFT_COL_WIDTH // 2, label_tt_dich_y_new, text_align_center=True)
        draw_puzzle(result, (LEFT_COL_X_START + (LEFT_COL_WIDTH - STATIC_PUZZLE_SIZE) // 2, result_puzzle_pos_y_new),
                    STATIC_PUZZLE_SIZE)

        current_y_btn_left = btn_left_y_start_new
        btn_random = button(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH, left_button_height_val, "NGẪU NHIÊN",
                            (255, 69, 0), WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH,
                                    left_button_height_val).collidepoint(
                            mouse_pos) and not solving and not is_calculating_path))
        current_y_btn_left += left_button_height_val + left_button_spacing_val
        btn_input_main = button(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH, left_button_height_val,
                                "NHẬP TAY", (255, 165, 0), WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH,
                                    left_button_height_val).collidepoint(
                            mouse_pos) and not solving and not is_calculating_path))
        current_y_btn_left += left_button_height_val + left_button_spacing_val
        btn_solve_main = button(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH, left_button_height_val, "GIẢI",
                                (60, 179, 113), WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH,
                                    left_button_height_val).collidepoint(
                            mouse_pos) and not solving and selected and not is_calculating_path))
        current_y_btn_left += left_button_height_val + left_button_spacing_val
        btn_show_goal_main = button(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH, left_button_height_val,
                                    "XEM KẾT QUẢ", (128, 0, 128), WHITE_TEXT, is_hovered=(
                        pygame.Rect(LEFT_COL_X_START, current_y_btn_left, LEFT_COL_WIDTH,
                                    left_button_height_val).collidepoint(mouse_pos) and not is_calculating_path))

        mid_puzzle_x_centered = MID_COL_X_START + (MID_COL_WIDTH_val - MAIN_PUZZLE_SIZE_val) // 2
        draw_puzzle(current, (mid_puzzle_x_centered, main_puzzle_display_y_new), MAIN_PUZZLE_SIZE_val)

        actual_mid_button_group_width = 3 * mid_button_width_val + 2 * 10
        btn_prev_main_x_draw = MID_COL_X_START + (MID_COL_WIDTH_val - actual_mid_button_group_width) // 2
        btn_reset_main_x_draw = btn_prev_main_x_draw + mid_button_width_val + 10
        btn_next_main_x_draw = btn_reset_main_x_draw + mid_button_width_val + 10

        btn_prev_main = button(btn_prev_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                               mid_button_height_const, "LÙI", BLUE_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(btn_prev_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                                    mid_button_height_const).collidepoint(
                            mouse_pos) and path and not is_calculating_path))
        btn_reset_main = button(btn_reset_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                                mid_button_height_const, "RESET", BLUE_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(btn_reset_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                                    mid_button_height_const).collidepoint(mouse_pos) and not is_calculating_path))
        btn_next_main = button(btn_next_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                               mid_button_height_const, "TIẾN", BLUE_BG, WHITE_TEXT, is_hovered=(
                        pygame.Rect(btn_next_main_x_draw, current_y_mid_buttons_draw_val, mid_button_width_val,
                                    mid_button_height_const).collidepoint(
                            mouse_pos) and path and not is_calculating_path))

        step_text_content = f"Số bước: {index}/{len(path) - 1 if path else '0'}"
        current_info_y = draw_text_label(step_text_content, FONT_STEP_INFO, TEXT_INFO_COLOR,
                                         MID_COL_X_START + MID_COL_WIDTH_val // 2, step_text_y_draw_val,
                                         text_align_center=True)

        if show_search_info:
            search_time_text = f"Thời gian tìm: {search_time_sec:.3f} s"
            current_info_y = draw_text_label(search_time_text, FONT_EXTRA_INFO, TEXT_INFO_COLOR,
                                             MID_COL_X_START + MID_COL_WIDTH_val // 2, current_info_y + 5,
                                             text_align_center=True)

        max_algo_text_w = 0
        if FONT_BUTTON_ALGO:
            for algo_name in algorithm_dict_display_names:
                text_s = FONT_BUTTON_ALGO.render(algo_name, True, (0, 0, 0))
                if text_s.get_width() > max_algo_text_w: max_algo_text_w = text_s.get_width()

        calculated_one_algo_btn_w = max_algo_text_w + 2 * algo_padding_x

        TOTAL_ALGO_BUTTONS_SPAN_WIDTH = (2 * uniform_algo_button_width) + algo_horizontal_spacing
        SCREEN_RIGHT_MARGIN_val = 30
        RIGHT_COL_X_START_val = SCREEN_WIDTH - TOTAL_ALGO_BUTTONS_SPAN_WIDTH - SCREEN_RIGHT_MARGIN_val
        CENTER_X_ALGO_AREA_val = RIGHT_COL_X_START_val + TOTAL_ALGO_BUTTONS_SPAN_WIDTH // 2

        dynamic_header_text_content = "CHỌN THUẬT TOÁN ĐỂ BẮT ĐẦU"
        dynamic_header_background = BLUE_BG
        dynamic_header_font_color = WHITE_TEXT
        if is_calculating_path:
            dynamic_header_text_content = f"ĐANG TÌM: {text_box_algorithm}..."
            dynamic_header_background = SEARCHING_BG_COLOR
        elif solving and not done and path:
            dynamic_header_text_content = f"ĐANG GIẢI: {text_box_algorithm}"
        elif done and path and (index == len(path) - 1 or (len(path) == 1 and index == 0)):
            dynamic_header_text_content = f"HOÀN THÀNH: {text_box_algorithm}!"
        elif done and (not path or (path and index >= len(path))):
            dynamic_header_text_content = f"LỖI/KTTLG: {text_box_algorithm}"
            dynamic_header_background = "red"
        elif selected:
            dynamic_header_text_content = f"Đã chọn: {text_box_algorithm}"

        header_actual_bottom_y = draw_text_label(dynamic_header_text_content, FONT_TITLE_SECTION,
                                                 dynamic_header_font_color,
                                                 CENTER_X_ALGO_AREA_val, dynamic_status_header_y_new,
                                                 background_color=dynamic_header_background, padding_x=10, padding_y=8,
                                                 width_override=TOTAL_ALGO_BUTTONS_SPAN_WIDTH, text_align_center=True)

        current_algo_button_y_draw = header_actual_bottom_y + 10
        algo_buttons_list_cache = []
        col_idx = 0
        for i, algo_name_disp in enumerate(algorithm_dict_display_names):
            btn_x = RIGHT_COL_X_START_val + (col_idx * (uniform_algo_button_width + algo_horizontal_spacing))
            btn_y = current_algo_button_y_draw

            is_hovered_algo = pygame.Rect(btn_x, btn_y, uniform_algo_button_width, algo_button_height).collidepoint(
                mouse_pos) and not (solving and not done) and not is_calculating_path
            is_selected_algo = selected and text_box_algorithm == algo_name_disp

            algo_rect = button(btn_x, btn_y, uniform_algo_button_width, algo_button_height, algo_name_disp,
                               DARK_RED_BUTTON_BG, WHITE_TEXT, FONT_BUTTON_ALGO, is_hovered=is_hovered_algo,
                               is_selected=is_selected_algo)
            algo_buttons_list_cache.append((algo_rect, algo_name_disp, algo_name_disp, 0))

            col_idx += 1
            if col_idx >= 2:
                col_idx = 0
                current_algo_button_y_draw += algo_button_height + algo_button_spacing

        if solving and not done and path and not is_calculating_path:
            if 0 <= index < len(path) - 1:
                pygame.time.delay(speed)
                index += 1
            elif index == len(path) - 1:
                done = True
            else:
                done = True

    else:
        padding_top_input_screen = effective_title_bar_bottom + 40
        padding_general = 20
        font_h_section = FONT_TITLE_SECTION.get_height() if FONT_TITLE_SECTION else 22
        font_h_step_info = FONT_STEP_INFO.get_height() if FONT_STEP_INFO else 20

        input_puzzle_label_y = padding_top_input_screen
        left_section_width = SCREEN_WIDTH // 2 - padding_general
        left_section_center_x = left_section_width // 2 + padding_general // 2

        draw_text_label("Puzzle Bạn Nhập:", FONT_TITLE_SECTION, (0, 0, 0),
                        left_section_center_x, input_puzzle_label_y, text_align_center=True)

        input_display_puzzle_size = 280
        puzzle_input_draw_x = left_section_center_x - (input_display_puzzle_size // 2)
        puzzle_input_draw_y = input_puzzle_label_y + font_h_section + 10
        draw_puzzle(puzzle_input, (puzzle_input_draw_x, puzzle_input_draw_y), input_display_puzzle_size)

        right_section_x_start = SCREEN_WIDTH // 2 + padding_general // 2
        right_section_width = SCREEN_WIDTH // 2 - padding_general
        right_section_center_x = right_section_x_start + right_section_width // 2

        select_number_label_y = padding_top_input_screen
        draw_text_label("Chọn số:", FONT_TITLE_SECTION, (0, 0, 0),
                        right_section_center_x, select_number_label_y, text_align_center=True)

        block_w_input, block_h_input, spacing_input_val = 80, 80, 15
        total_blocks_width = 3 * block_w_input + 2 * spacing_input_val
        blocks_area_start_x = right_section_center_x - (total_blocks_width // 2)
        blocks_area_start_y = select_number_label_y + font_h_section + 10

        for idx, (r_block, v_block) in enumerate(blocks):
            row_block, col_block = divmod(idx, 3)
            new_x_block = blocks_area_start_x + col_block * (block_w_input + spacing_input_val)
            new_y_block = blocks_area_start_y + row_block * (block_h_input + spacing_input_val)
            r_block.topleft = (new_x_block, new_y_block)
            r_block.size = (block_w_input, block_h_input)

            is_val_used_input = False
            for r_idx, row_val in enumerate(puzzle_input):
                for c_idx, cell_val in enumerate(row_val):
                    if cell_val == v_block and puzzle_input_check[r_idx][c_idx] == 1:
                        is_val_used_input = True
                        break
                if is_val_used_input: break

            block_fill_color_input = (180, 180, 180) if is_val_used_input else 'white'
            pygame.draw.rect(screen, block_fill_color_input, r_block, 0, 5)
            pygame.draw.rect(screen, 'black', r_block, 2, 5)

            label_font_input_block_path = FONT_FILE_NAME if FONT_FILE_NAME and os.path.exists(FONT_FILE_NAME) else None
            label_font_input_block = pygame.font.Font(label_font_input_block_path,
                                                      30 if label_font_input_block_path else 36)
            label_surf_input = label_font_input_block.render(str(v_block), True, 'black')
            label_rect_input = label_surf_input.get_rect(center=r_block.center)
            screen.blit(label_surf_input, label_rect_input)

        button_width_input = 190
        button_height_input = 50
        button_spacing_input = 20
        total_buttons_width_input = 3 * button_width_input + 2 * button_spacing_input

        y_offset_for_msg = 0
        if text_box_algorithm:
            y_offset_for_msg = font_h_step_info + 2 * 5 + 10

        buttons_y_start_input = SCREEN_HEIGHT - button_height_input - padding_general - y_offset_for_msg

        btn_back_x = (SCREEN_WIDTH - total_buttons_width_input) // 2
        btn_ok_x = btn_back_x + button_width_input + button_spacing_input
        btn_reset_x = btn_ok_x + button_width_input + button_spacing_input

        btn_back_input = button(btn_back_x, buttons_y_start_input, button_width_input, button_height_input, 'QUAY LẠI',
                                (205, 92, 92), WHITE_TEXT,
                                is_hovered=pygame.Rect(btn_back_x, buttons_y_start_input, button_width_input,
                                                       button_height_input).collidepoint(mouse_pos))
        btn_ok_input = button(btn_ok_x, buttons_y_start_input, button_width_input, button_height_input, 'XÁC NHẬN',
                              (60, 179, 113), WHITE_TEXT,
                              is_hovered=pygame.Rect(btn_ok_x, buttons_y_start_input, button_width_input,
                                                     button_height_input).collidepoint(mouse_pos))
        btn_reset_puzzle_input = button(btn_reset_x, buttons_y_start_input, button_width_input, button_height_input,
                                        'NHẬP LẠI', (30, 144, 255), WHITE_TEXT,
                                        is_hovered=pygame.Rect(btn_reset_x, buttons_y_start_input, button_width_input,
                                                               button_height_input).collidepoint(mouse_pos))

        if text_box_algorithm:
            input_msg_box_y = buttons_y_start_input - font_h_step_info - 10
            msg_color_bg = (255, 70,
                            70) if "lỗi" in text_box_algorithm.lower() or "không" in text_box_algorithm.lower() or "chưa" in text_box_algorithm.lower() else (
            100, 100, 100)
            msg_text_color = WHITE_TEXT
            draw_text_label(text_box_algorithm, FONT_STEP_INFO, msg_text_color,
                            SCREEN_WIDTH // 2, input_msg_box_y,
                            background_color=msg_color_bg, padding_x=20, padding_y=5,
                            width_override=SCREEN_WIDTH * 0.7, text_align_center=True)

    pygame.display.flip()

pygame.quit()
sys.exit()