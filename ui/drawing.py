# -*- coding: utf-8 -*-
# ui/drawing.py
""" Các hàm tiện ích để vẽ lên màn hình Pygame """

import pygame as pg
# Import các hằng số cần thiết
from .constants import (COLOR_EMPTY_TILE, PUZZLE_BORDER_RADIUS, FONT_MEDIUM,
                        COLOR_TEXT_SECONDARY, COLOR_TILE, COLOR_TILE_BORDER,
                        COLOR_TEXT_ON_TILE, TILE_SIZE_LARGE, TILE_MARGIN_LARGE,
                        POS_PATH_LARGE_X, POS_PATH_LARGE_Y)


def draw_text(text, font, color, surface, position, center_x=False, center_y=False, top_left=False):
    """Hàm tiện ích để vẽ text lên surface."""
    if not isinstance(text, str): text = str(text) # Đảm bảo text là string
    try:
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()

        # Xác định vị trí dựa trên các flag căn chỉnh
        if top_left:
            text_rect.topleft = position
        elif center_x and center_y:
            text_rect.center = position
        elif center_x:
            text_rect.centerx = position[0]
            text_rect.top = position[1]
        elif center_y:
            text_rect.left = position[0]
            text_rect.centery = position[1]
        else: # Mặc định là topleft nếu không có flag nào
            text_rect.topleft = position

        surface.blit(text_obj, text_rect)
        return text_rect # Trả về rect để kiểm tra va chạm nếu cần
    except Exception as e:
        print(f"Error rendering text '{text}': {e}")
        # Trả về rect 0x0 nếu lỗi
        return pg.Rect(position[0], position[1], 0, 0)

def find_zero_pos(board):
    """Tìm vị trí (row, col) của ô trống (0) trong board."""
    # Thêm kiểm tra board hợp lệ
    if not isinstance(board, list) or len(board) != 3:
        # print("find_zero_pos: Invalid board structure (not a list or length != 3)")
        return None
    for r in range(len(board)):
        if not isinstance(board[r], list) or len(board[r]) != 3:
            # print(f"find_zero_pos: Invalid row structure at index {r}")
            return None
        for c in range(len(board[r])):
            try:
                if board[r][c] == 0:
                    return r, c
            except IndexError:
                 # print(f"find_zero_pos: IndexError accessing board[{r}][{c}]")
                 return None # Lỗi index
            except TypeError:
                 # print(f"find_zero_pos: TypeError checking value at board[{r}][{c}]")
                 return None # Phần tử không phải số?
    # print("find_zero_pos: Blank tile (0) not found in board.")
    return None # Không tìm thấy ô 0

def grid_to_pixel_large(row, col):
    """Chuyển đổi tọa độ grid (row, col) sang tọa độ pixel (top-left) cho puzzle lớn."""
    x = POS_PATH_LARGE_X + col * (TILE_SIZE_LARGE + TILE_MARGIN_LARGE)
    y = POS_PATH_LARGE_Y + row * (TILE_SIZE_LARGE + TILE_MARGIN_LARGE)
    return x, y

def lerp(start, end, t):
    """Linear interpolation."""
    return start + (end - start) * t

def draw_8_puzzle(surface, matran, posx_bd, posy_bd, tile_size, tile_margin, font, skip_tile_value=None):
    """Vẽ trạng thái 8-puzzle lên surface."""
    current_grid_size = 3 * tile_size + 2 * tile_margin

    # Kiểm tra ma trận đầu vào
    is_valid_matran = isinstance(matran, list) and len(matran) == 3 and \
                      all(isinstance(row, list) and len(row) == 3 for row in matran)

    if not is_valid_matran:
        # Vẽ placeholder nếu ma trận không hợp lệ
        rect = pg.Rect(posx_bd, posy_bd, current_grid_size, current_grid_size)
        pg.draw.rect(surface, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
        draw_text("N/A", FONT_MEDIUM, COLOR_TEXT_SECONDARY, surface, rect.center, True, True)
        return

    for r in range(3):
        for c in range(3):
            try:
                tile_val = matran[r][c]
                # Đảm bảo giá trị là số nguyên
                if not isinstance(tile_val, int): tile_val = -1 # Coi như không hợp lệ
            except IndexError:
                tile_val = -1 # Lỗi index, coi như không hợp lệ

            # --- Tính toán vị trí ô ---
            left = posx_bd + c * (tile_size + tile_margin)
            top = posy_bd + r * (tile_size + tile_margin)
            rect = pg.Rect(left, top, tile_size, tile_size)

            # --- Vẽ ô ---
            # Bỏ qua nếu giá trị cần skip (dùng cho animation)
            if skip_tile_value is not None and tile_val == skip_tile_value:
                pg.draw.rect(surface, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
                continue

            # Vẽ ô trống
            if tile_val == 0:
                pg.draw.rect(surface, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
            # Vẽ ô có số
            elif tile_val > 0:
                pg.draw.rect(surface, COLOR_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
                pg.draw.rect(surface, COLOR_TILE_BORDER, rect, width=1, border_radius=PUZZLE_BORDER_RADIUS)
                # Vẽ số lên ô
                draw_text(str(tile_val), font, COLOR_TEXT_ON_TILE, surface, rect.center, center_x=True, center_y=True)
            # Vẽ ô không hợp lệ (nếu tile_val < 0) - có thể vẽ khác đi nếu muốn
            else:
                 pg.draw.rect(surface, COLOR_EMPTY_TILE, rect, border_radius=PUZZLE_BORDER_RADIUS)
                 draw_text("?", FONT_MEDIUM, COLOR_TEXT_SECONDARY, surface, rect.center, True, True)