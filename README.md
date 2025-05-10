# Đồ Án AI: Giải Bài Toán 8-Puzzle Bằng Các Thuật Toán Tìm Kiếm và Học Máy (Có Visualization)

Dự án này cài đặt, so sánh và trực quan hóa (visualize) quá trình giải bài toán 8-puzzle cổ điển bằng cách sử dụng một loạt các thuật toán tìm kiếm khác nhau, từ tìm kiếm mù, tìm kiếm có thông tin, tìm kiếm cục bộ đến các thuật toán nâng cao hơn bao gồm cả học tăng cường và xử lý ràng buộc. Giao diện đồ họa được xây dựng bằng Pygame.

## Mục lục

* [Tính năng](#tính-năng)
* [Thuật toán được cài đặt](#thuật-toán-được-cài-đặt)
* [Heuristics](#heuristics)
* [Cấu trúc thư mục](#cấu-trúc-thư-mục)
* [Yêu cầu](#yêu-cầu)
* [Cài đặt](#cài-đặt)
* [Cách chạy](#cách-chạy)
* [Hướng dẫn sử dụng giao diện](#hướng-dẫn-sử-dụng-giao-diện)
* [Lưu ý về thuật toán](#lưu-ý-về-thuật-toán)
* [Tác giả](#tác-giả)

## Tính năng

* Giải bài toán 8-puzzle từ một trạng thái bắt đầu cho trước về trạng thái đích (đối với các thuật toán tìm đường đi).
* Cài đặt và so sánh nhiều thuật toán tìm kiếm và học máy khác nhau.
* Sử dụng các hàm heuristic phổ biến (Manhattan Distance) cho thuật toán tìm kiếm có thông tin.
* Giao diện đồ họa tương tác bằng Pygame cho phép:
    * Hiển thị trạng thái bắt đầu và trạng thái đích.
    * Chọn và chạy các thuật toán khác nhau.
    * Trực quan hóa từng bước di chuyển trong quá trình giải (đối với các thuật toán tìm đường đi trạng thái).
    * Điều hướng qua các bước của lời giải (Lùi/Tiến) cho các thuật toán tìm đường đi trạng thái.
    * Hiển thị thông báo trạng thái (đang giải, đã tìm thấy, không tìm thấy, lỗi, thời gian giải, số bước/kết quả...).
    * Hỗ trợ chạy thuật toán Conformant BFS trên một trạng thái niềm tin (belief state) mẫu.
    * Hỗ trợ huấn luyện và thử nghiệm cơ bản cho các tác nhân Học tăng cường (Q-Learning, TD-Learning/SARSA).
    * Hỗ trợ chạy và hiển thị kết quả cơ bản cho thuật toán xử lý ràng buộc AC-3.
    * Hỗ trợ chạy thuật toán AND-OR Search (hiển thị đường đi nếu tìm thấy).

## Thuật toán được cài đặt

Dự án cài đặt các thuật toán sau (nằm trong thư mục `algorithms/`):

* **Tìm kiếm không có thông tin (Uninformed Search):**
    * Breadth-First Search (BFS)
    * Uniform Cost Search (UCS)
    * Depth-First Search (DFS)
    * Iterative Deepening Depth-First Search (IDDFS)
    * **Tìm kiếm có thông tin (Informed Search):**
    * Greedy Best-First Search (Sử dụng Manhattan Distance)
    * A\* Search (Sử dụng Manhattan Distance)
    * Iterative Deepening A\* (IDA\*) (Sử dụng Manhattan Distance)
* **Tìm kiếm cục bộ (Local Search):**
    * Simple Hill Climbing 
    * Steepest Ascent Hill Climbing
    * Stochastic Hill Climbing
    * Simulated Annealing 
    * Genetic Algorithm 
    * Beam Search
* **tìm kiếm trong môi trường phức tạp**
    * Conformant BFS (Tìm kiếm trên không gian trạng thái niềm tin)
    * AND-OR Tree Search 
* **Tìm kiếm trong môi trường có ràng buộc**
    * Backtracking
    * AC-3
* **Học máy**
    * Q-Learning 
    * Temporal Difference (TD) Learning

## Heuristics

Các hàm heuristic được cài đặt trong `puzzle/heuristics.py`:

* **Khoảng cách Manhattan (`khoang_cach_mahathan`):** Được sử dụng chủ yếu cho các thuật toán Greedy, A\*, IDA\*, và các thuật toán Local Search.
* **Số ô sai vị trí (`Chiphi`):** Được cài đặt nhưng có thể không được sử dụng mặc định trong các thuật toán chính.

## Cấu trúc thư mục

Dự án được tổ chức theo cấu trúc module hóa:
```
BaiTapCaNhan_AI/
├── puzzle/
│   ├── init.py
│   ├── state.py
│   └── heuristics.py
│
├── algorithms/
│   ├── init.py
│   ├── a_star.py
│   ├── ac3_solver.py
│   ├── and_or_search.py
│   ├── backtracking_search.py
│   ├── beam_search.py
│   ├── bfs.py
│   ├── conformant_bfs.py
│   ├── dfs.py
│   ├── genetic_algorithm.py
│   ├── greedy.py
│   ├── hill_climbing.py
│   ├── ida_star.py
│   ├── iddfs.py
│   ├── q_learning_solver.py
│   ├── simulated_annealing.py
│   ├── td_learning_solver.py
│   └── ucs.py
│
├── ui/
│   ├── init.py
│   ├── constants.py
│   ├── button.py
│   ├── drawing.py
│   └── visualization.py
│
├── main.py
├── run_tests.py
├── README.md
└── requirements.txt
```

## Yêu cầu

* Python 3.x (Đã thử nghiệm trên Python 3.9+)
* Pygame (ví dụ: 2.5.x trở lên)
* NumPy (cho các thuật toán Học tăng cường và một số tính toán tiện ích)

## Cài đặt

1.  Clone repository này về máy (nếu bạn đặt nó trên Git). Nếu không, bỏ qua bước này.
2.  Mở Terminal (hoặc Command Prompt) trong thư mục gốc của dự án (`BaiTapCaNhan_AI`).
3.  Cài đặt các thư viện cần thiết bằng pip:
    ```bash
    pip install -r requirements.txt
    ```
    File `requirements.txt` nên có nội dung:
    ```
    pygame
    numpy
    ```

## Cách chạy

* **Chạy giao diện đồ họa:**
    Từ thư mục gốc `BaiTapCaNhan_AI`, chạy lệnh:
    ```bash
    python main.py
    ```
* **(Tùy chọn) Chạy thử nghiệm thuật toán trên dòng lệnh:**
    Từ thư mục gốc `BaiTapCaNhan_AI`, chạy lệnh:
    ```bash
    python run_tests.py
    ```

## Hướng dẫn sử dụng giao diện

1.  Chạy ứng dụng bằng lệnh `python main.py`.
2.  Cửa sổ ứng dụng sẽ hiện ra với các khu vực chính:
    * **Trái:** Hiển thị trạng thái Bắt đầu và Đích (dạng lưới 3x3 nhỏ).
    * **Giữa:** Hiển thị trạng thái hiện tại của puzzle (dạng lưới 3x3 lớn). Các nút "Lùi" và "Tiến" sẽ xuất hiện bên dưới sau khi tìm thấy lời giải (chỉ áp dụng cho các thuật toán trả về đường đi trạng thái).
    * **Phải:** Danh sách các nút bấm tương ứng với các thuật toán. Các thuật toán đặc biệt như "Conformant BFS", "Q-Learning", "TD (SARSA)", "AC-3 Solver", "AND-OR Search" có thể có màu khác để phân biệt.
3.  **Chọn thuật toán:** Click vào một nút thuật toán ở cột bên phải để bắt đầu.
    * Đối với các thuật toán tìm đường đi truyền thống, quá trình giải sẽ được trực quan hóa nếu tìm thấy lời giải.
    * Khi chọn "Conformant BFS", chương trình sẽ sử dụng một tập hợp trạng thái niềm tin (belief state) mẫu. Kết quả là một chuỗi các hành động.
    * Khi chọn "AC-3 Solver", chương trình sẽ áp dụng thuật toán nhất quán cung lên trạng thái bắt đầu và hiển thị trạng thái puzzle sau khi lọc miền giá trị (nếu có thể).
    * Khi chọn "AND-OR Search", chương trình sẽ cố gắng tìm một kế hoạch/đường đi.
    * Khi chọn "Q-Learning" hoặc "TD (SARSA)", quá trình "huấn luyện" sẽ diễn ra (thời gian phụ thuộc vào số episodes). Sau khi huấn luyện, giao diện sẽ hiển thị trạng thái bắt đầu; bạn có thể click vào ô puzzle lớn để xem nước đi đề xuất từ agent đã học (nếu tính năng này được kích hoạt đầy đủ trong code xử lý sự kiện).
4.  **Quan sát:**
    * Puzzle lớn ở giữa sẽ hiển thị các bước di chuyển cho thuật toán tìm đường đi.
    * Thanh trạng thái (Status Bar) ở dưới cùng sẽ hiển thị thông báo: đang tìm kiếm/huấn luyện, tìm thấy đường đi (số bước, thời gian), không tìm thấy, hoặc lỗi.
5.  **Điều hướng:** Sử dụng nút "Lùi" và "Tiến" để xem lại từng bước giải (chỉ hoạt động với các thuật toán trả về danh sách trạng thái và khi `found_path_type` là `states`).

## Lưu ý về thuật toán

* **Không đảm bảo tìm thấy lời giải tối ưu/bất kỳ lời giải nào:**
    * Các thuật toán Local Search (Hill Climbing, Simulated Annealing), Greedy Search, Beam Search, Genetic Algorithm không đảm bảo sẽ tìm thấy trạng thái đích hoặc lời giải tối ưu. Chúng có thể bị kẹt ở tối ưu cục bộ hoặc kết thúc mà không đạt được mục tiêu.
    * DFS, IDDFS, IDA\*, Backtracking có thể không tìm thấy lời giải nếu đường đi yêu cầu độ sâu hoặc chi phí vượt quá giới hạn (`max_depth`/`max_threshold`) được đặt trong code.
* **Các thuật toán tìm kiếm đầy đủ và tối ưu (trong điều kiện nhất định):**
    * BFS (tìm đường đi ngắn nhất về số bước), UCS (tìm đường đi có chi phí thấp nhất khi chi phí mỗi bước là 1), A\* (tìm đường đi tối ưu nếu heuristic là admissible và consistent).
* **Các thuật toán đặc biệt:**
    * **Conformant BFS:** Tìm kiếm một kế hoạch hành động áp dụng được cho một tập hợp trạng thái ban đầu.
    * **AC-3 Solver:** Dùng cho Bài toán Thỏa mãn Ràng buộc. Trong ngữ cảnh này, nó có thể được dùng để phân tích một trạng thái puzzle. Kết quả không phải là đường đi.
    * **AND-OR Search:** Tìm kiếm giải pháp bằng cách phân rã bài toán. Phiên bản hiện tại là cơ bản.
    * **Q-Learning & TD (SARSA) Learning:** Đây là các thuật toán Học tăng cường. Chúng "học" một chính sách tối ưu qua nhiều lần thử và sai (episodes). Kết quả là một "agent" đã được huấn luyện. Giao diện hiện tại hỗ trợ huấn luyện và có thể cho phép thử nghiệm chính sách sau đó. Chúng không trả về một "đường đi" theo cách các thuật toán tìm kiếm truyền thống thực hiện trong một lần chạy.

## Tác giả

* [Sử Thanh Lộc]
* [23110371]