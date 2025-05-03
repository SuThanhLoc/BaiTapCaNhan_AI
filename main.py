# -*- coding: utf-8 -*-
# main.py
"""
File chính để khởi chạy ứng dụng 8-Puzzle Solver Visualization.
"""
import sys
import pygame as pg
import os

# Đảm bảo có thể import từ các thư mục con (thường không cần nếu cấu trúc chuẩn)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)

# Import lớp ứng dụng chính từ package ui
try:
    from ui.visualization import VisualizationApp
except ImportError as e:
    print("--------------------------------------------------------------------")
    print(f"LỖI: Không thể import VisualizationApp từ ui.visualization.")
    print(f"Lỗi chi tiết: {e}")
    print("Hãy đảm bảo rằng:")
    print("1. Thư mục 'ui' và file 'visualization.py' tồn tại.")
    print("2. File 'ui/__init__.py' tồn tại (có thể trống).")
    print("3. Không có lỗi cú pháp trong file 'ui/visualization.py' hoặc các file nó import.")
    print("--------------------------------------------------------------------")
    sys.exit(1) # Thoát nếu không import được UI chính

if __name__ == "__main__":
    print("Starting 8-Puzzle Solver Visualization...")
    try:
        app = VisualizationApp()
        app.run()
    except Exception as e:
        print("\n--------------------------------------------------------------------")
        print(f"LỖI KHÔNG XÁC ĐỊNH KHI CHẠY ỨNG DỤNG:")
        print(f"Lỗi chi tiết: {e}")
        import traceback
        traceback.print_exc() # In traceback để debug
        print("--------------------------------------------------------------------")
        pg.quit() # Cố gắng đóng pygame nếu nó đã khởi tạo
        sys.exit(1)