# -*- coding: utf-8 -*-
# ui/button.py
""" Lớp Button cho giao diện Pygame """

import pygame as pg
# Import có chọn lọc từ constants và drawing cùng cấp
from .constants import (COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_SELECTED,
                        COLOR_BUTTON_DISABLED, COLOR_BORDER, BUTTON_BORDER_RADIUS,
                        COLOR_BUTTON_TEXT, FONT_MAIN_BOLD,
                        COLOR_BUTTON_BELIEF, COLOR_BUTTON_BELIEF_HOVER,
                        COLOR_BUTTON_BELIEF_SELECTED)
# Cần import hàm draw_text từ drawing.py
# Tạm thời comment out nếu chưa có drawing.py hoặc import sau
from .drawing import draw_text

class Button:
    """ Lớp đại diện cho một nút bấm trong Pygame """
    def __init__(self, x, y, w, h, text, callback=None, font=FONT_MAIN_BOLD,
                 text_color=COLOR_BUTTON_TEXT,
                 is_belief_button=False, # Cờ nhận diện nút Belief
                 # Các màu có thể override nếu cần, nhưng thường lấy từ constants
                 base_color=None,
                 hover_color=None,
                 selected_color=None,
                 disabled_color=COLOR_BUTTON_DISABLED
                 ):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.text_color = text_color

        self.is_hovered = False
        self.is_selected = False
        self.is_disabled = False
        self.is_belief_button = is_belief_button # Lưu lại loại nút

        # Gán màu dựa trên loại nút và tham số override
        if is_belief_button:
            self.base_color = base_color if base_color else COLOR_BUTTON_BELIEF
            self.hover_color = hover_color if hover_color else COLOR_BUTTON_BELIEF_HOVER
            self.selected_color = selected_color if selected_color else COLOR_BUTTON_BELIEF_SELECTED
        else: # Nút thường hoặc Nav
            self.base_color = base_color if base_color else COLOR_BUTTON
            self.hover_color = hover_color if hover_color else COLOR_BUTTON_HOVER
            self.selected_color = selected_color if selected_color else COLOR_BUTTON_SELECTED

        self.disabled_color = disabled_color # Màu disabled là chung

    def handle_event(self, event):
        """ Xử lý input event cho nút. Trả về True nếu nút được click. """
        if self.is_disabled:
            self.is_hovered = False
            return False

        action = False
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Click chuột trái
                action = True
                # Gọi callback nếu có khi nút được click
                if self.callback:
                    try:
                        # Truyền text của nút làm đối số cho callback
                        self.callback(self.text)
                    except Exception as e:
                        print(f"Error executing callback for button '{self.text}': {e}")
        return action

    def draw(self, surface):
        """ Vẽ nút lên surface được cung cấp. """
        current_color = self.base_color # Bắt đầu với màu base (thường hoặc belief)
        if self.is_disabled:
            current_color = self.disabled_color
        elif self.is_selected:
            current_color = self.selected_color # Màu selected (thường hoặc belief)
        elif self.is_hovered:
            current_color = self.hover_color # Màu hover (thường hoặc belief)

        # Vẽ thân nút
        pg.draw.rect(surface, current_color, self.rect, border_radius=BUTTON_BORDER_RADIUS)
        # Vẽ viền nút
        border_thickness = 1
        pg.draw.rect(surface, COLOR_BORDER, self.rect, width=border_thickness, border_radius=BUTTON_BORDER_RADIUS)
        # Vẽ chữ lên nút
        draw_text(self.text, self.font, self.text_color, surface, self.rect.center, center_x=True, center_y=True)