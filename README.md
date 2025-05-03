# Đồ Án AI: Giải Bài Toán 8-Puzzle Bằng Các Thuật Toán Tìm Kiếm (Có Visualization)

Dự án này cài đặt, so sánh và trực quan hóa (visualize) quá trình giải bài toán 8-puzzle cổ điển bằng cách sử dụng một loạt các thuật toán tìm kiếm khác nhau, từ tìm kiếm mù, tìm kiếm có thông tin, tìm kiếm cục bộ đến các thuật toán nâng cao hơn. Giao diện đồ họa được xây dựng bằng Pygame.

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

* Giải bài toán 8-puzzle từ một trạng thái bắt đầu cho trước về trạng thái đích.
* Cài đặt và so sánh nhiều thuật toán tìm kiếm khác nhau.
* Sử dụng các hàm heuristic phổ biến (Manhattan Distance) cho thuật toán tìm kiếm có thông tin.
* Giao diện đồ họa tương tác bằng Pygame cho phép:
    * Hiển thị trạng thái bắt đầu và trạng thái đích.
    * Chọn và chạy các thuật toán tìm kiếm khác nhau.
    * Trực quan hóa từng bước di chuyển trong quá trình giải.
    * Điều hướng qua các bước của lời giải (Lùi/Tiến).
    * Hiển thị thông báo trạng thái (đang giải, đã tìm thấy, không tìm thấy, lỗi, thời gian giải, số bước...).
    * Hỗ trợ chạy thuật toán Conformant BFS trên một trạng thái niềm tin (belief state) mẫu.

## Thuật toán được cài đặt

Dự án cài đặt các thuật toán sau (nằm trong thư mục `algorithms/`):

* **Tìm kiếm mù (Uninformed Search):**
    * Breadth-First Search (BFS)
    * Uniform Cost Search (UCS)
    * Depth-First Search (DFS) - Có giới hạn độ sâu
    * Iterative Deepening Depth-First Search (IDDFS)
* **Tìm kiếm có thông tin (Informed Search):**
    * Greedy Best-First Search (Sử dụng Manhattan Distance)
    * A\* Search (Sử dụng Manhattan Distance)
    * Iterative Deepening A\* (IDA\*) (Sử dụng Manhattan Distance)
* **Tìm kiếm cục bộ (Local Search):**
    * Simple Hill Climbing (First Choice)
    * Steepest Ascent Hill Climbing
    * Stochastic Hill Climbing
    * Simulated Annealing (SA)
* **Thuật toán khác:**
    * Beam Search
    * Genetic Algorithm (GA)
    * Conformant BFS (Tìm kiếm trên không gian trạng thái niềm tin)

## Heuristics

Các hàm heuristic được cài đặt trong `puzzle/heuristics.py`:

* **Khoảng cách Manhattan (`khoang_cach_mahathan`):** Được sử dụng chủ yếu cho các thuật toán Greedy, A\*, IDA\*, và các thuật toán Local Search.
* **Số ô sai vị trí (`Chiphi`):** Được cài đặt nhưng có thể không được sử dụng mặc định trong các thuật toán chính (Manhattan thường hiệu quả hơn).

## Cấu trúc thư mục

Dự án được tổ chức theo cấu trúc module hóa:
```
BaiTapCaNhan_AI/              <-- Thư mục gốc của dự án
├── puzzle/                     # Logic cốt lõi của bài toán 8-puzzle
│   ├── init.py
│   ├── state.py              # Định nghĩa trạng thái, hằng số, di chuyển...
│   └── heuristics.py         # Các hàm heuristic
│
├── algorithms/                 # Các thuật toán tìm kiếm
│   ├── init.py
│   ├── bfs.py, a_star.py, ... # Mỗi file chứa một hoặc một nhóm thuật toán
│
├── ui/                         # Code giao diện người dùng Pygame
│   ├── init.py
│   ├── constants.py          # Hằng số UI (màu sắc, font, kích thước...)
│   ├── button.py             # Lớp Button
│   ├── drawing.py            # Các hàm vẽ vời
│   └── visualization.py      # Module chính quản lý giao diện và vòng lặp game
│
├── main.py                     # File chính để chạy ứng dụng có giao diện
├── run_tests.py                # (Tùy chọn) Chạy test thuật toán trên dòng lệnh
├── README.md                   # File này
└── requirements.txt            # Các thư viện cần thiết
```

## Yêu cầu

* Python 3.x (Đã thử nghiệm trên Python 3.9)
* Pygame

## Cài đặt

1.  Clone repository này về máy (nếu bạn đặt nó trên Git). Nếu không, bỏ qua bước này.
2.  Mở Terminal (hoặc Command Prompt) trong thư mục gốc của dự án.
3.  Cài đặt các thư viện cần thiết bằng pip:
    ```bash
    pip install -r requirements.txt
    ```
    Hoặc nếu chưa có file `requirements.txt`, chỉ cần cài đặt Pygame:
    ```bash
    pip install pygame
    ```

## Cách chạy

* **Chạy giao diện đồ họa:**
    ```bash
    python main.py
    ```
* **(Tùy chọn) Chạy thử nghiệm thuật toán trên dòng lệnh:**
    ```bash
    python run_tests.py
    ```
    *(Lưu ý: `run_tests.py` có thể cần được tạo và cập nhật từ code test gốc nếu bạn muốn sử dụng)*

## Hướng dẫn sử dụng giao diện

1.  Chạy ứng dụng bằng lệnh `python main.py`.
2.  Cửa sổ ứng dụng sẽ hiện ra với 3 khu vực chính:
    * **Trái:** Hiển thị trạng thái Bắt đầu và Đích (dạng lưới 3x3 nhỏ).
    * **Giữa:** Hiển thị trạng thái hiện tại của puzzle trong quá trình giải (dạng lưới 3x3 lớn). Các nút "Lùi" và "Tiến" sẽ xuất hiện bên dưới sau khi tìm thấy lời giải (chỉ áp dụng cho các thuật toán trả về đường đi trạng thái).
    * **Phải:** Danh sách các nút bấm tương ứng với các thuật toán tìm kiếm. Nút "Conformant BFS" có màu khác để phân biệt.
3.  **Chọn thuật toán:** Click vào một nút thuật toán ở cột bên phải để bắt đầu quá trình giải bằng thuật toán đó. Các nút sẽ bị vô hiệu hóa trong khi giải.
    * *Lưu ý:* Khi chọn "Conformant BFS", chương trình sẽ sử dụng một tập hợp trạng thái niềm tin (belief state) mẫu được định nghĩa sẵn trong code thay vì trạng thái `Start` đơn lẻ.
4.  **Quan sát:**
    * Puzzle lớn ở giữa sẽ hiển thị các bước di chuyển (nếu thuật toán tìm thấy đường đi và không phải là Conformant BFS). Quá trình có thể tự động chạy hoặc bạn có thể dùng nút "Lùi"/"Tiến".
    * Thanh trạng thái (Status Bar) ở dưới cùng sẽ hiển thị thông báo: đang tìm kiếm, tìm thấy đường đi (số bước, thời gian), không tìm thấy, hoặc lỗi. Đối với Conformant BFS, nó sẽ hiển thị chuỗi các nước đi tìm được.
5.  **Điều hướng:** Sử dụng nút "Lùi" và "Tiến" để xem lại từng bước giải (chỉ hoạt động với các thuật toán như BFS, A*, DFS,... trả về danh sách trạng thái).

## Lưu ý về thuật toán

* **Không đảm bảo tìm thấy lời giải:** Các thuật toán Local Search (Hill Climbing, Simulated Annealing), Greedy Search, Beam Search, Genetic Algorithm không đảm bảo sẽ tìm thấy trạng thái đích. Chúng có thể bị kẹt ở tối ưu cục bộ hoặc kết thúc mà không đạt được mục tiêu.
* **Có thể thất bại do giới hạn:** DFS, IDDFS, IDA\* có thể không tìm thấy lời giải nếu đường đi yêu cầu độ sâu hoặc chi phí vượt quá giới hạn `max_depth`/`max_threshold` được đặt trong code.
* **Đáng tin cậy (thường lệ):** BFS, UCS, A\* (với heuristic tốt) thường sẽ tìm thấy lời giải tối ưu nếu tồn tại và đủ tài nguyên (thời gian, bộ nhớ).
* **Conformant BFS:** Tìm kiếm một kế hoạch hành động áp dụng được cho một tập hợp trạng thái ban đầu, không phải tìm đường đi cho một trạng thái đơn lẻ.

## Tác giả

* [Sử Thanh Lộc]
* [23110371]