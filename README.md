# Dự án Giải Bài Toán 8-Puzzle Bằng Các Thuật Toán Tìm Kiếm

## 1. Mục tiêu

Dự án này được xây dựng nhằm mục đích triển khai và mô phỏng các thuật toán tìm kiếm khác nhau để giải quyết bài toán 8-Puzzle. Qua đó, người dùng có thể hiểu rõ hơn về cách hoạt động, ưu nhược điểm và so sánh hiệu suất của từng thuật toán trong việc tìm kiếm lời giải cho một bài toán cụ thể trong lĩnh vực Trí Tuệ Nhân Tạo. Dự án cung cấp một giao diện trực quan (`UI.py`) để người dùng tương tác và quan sát quá trình giải của các thuật toán được định nghĩa trong `AI.py`.

## 2. Nội dung

### 2.1. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search Algorithms)

Phần này tập trung vào các thuật toán tìm kiếm không sử dụng thông tin bổ sung về bài toán (heuristic) để hướng dẫn quá trình tìm kiếm.

* **Thành phần chính của bài toán tìm kiếm và solution:**
    * **Bài toán tìm kiếm** thường bao gồm các thành phần sau:
        * **Không gian trạng thái (State Space):** Tập hợp tất cả các trạng thái có thể đạt được của bài toán. Trong 8-Puzzle, mỗi cách sắp xếp các ô số là một trạng thái.
        * **Trạng thái ban đầu (Initial State):** Trạng thái xuất phát của bài toán.
        * **Trạng thái đích (Goal State):** Một hoặc nhiều trạng thái mà bài toán cần đạt tới.
        * **Hành động (Actions):** Các thao tác có thể thực hiện để chuyển từ trạng thái này sang trạng thái khác. Trong 8-Puzzle, đó là việc di chuyển ô trống lên, xuống, trái, hoặc phải.
        * **Hàm chuyển trạng thái (Transition Model):** Mô tả trạng thái kết quả khi thực hiện một hành động từ một trạng thái cụ thể.
        * **Chi phí đường đi (Path Cost):** Hàm gán một giá trị chi phí cho một đường đi. Trong trường hợp 8-Puzzle cơ bản, mỗi bước di chuyển có thể có chi phí là 1.
    * **Solution (Lời giải):** Là một dãy các hành động (một đường đi) từ trạng thái ban đầu đến trạng thái đích. Một lời giải tối ưu là lời giải có chi phí đường đi thấp nhất.

* **Các thuật toán được triển khai (trong `AI.py`):**
    * **Tìm kiếm theo chiều rộng (Breadth-First Search - BFS):**
        * *Nguyên tắc:* Duyệt tất cả các trạng thái ở độ sâu hiện tại trước khi chuyển sang các trạng thái ở độ sâu tiếp theo.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình BFS duyệt các trạng thái của 8-Puzzle tại đây.)*
    * **Tìm kiếm chi phí đồng nhất (Uniform Cost Search - UCS):**
        * *Nguyên tắc:* Mở rộng nút có chi phí đường đi `g(n)` nhỏ nhất từ trạng thái ban đầu.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình UCS tại đây, đặc biệt nếu chi phí bước đi khác nhau.)*
    * **Tìm kiếm theo chiều sâu (Depth-First Search - DFS):**
        * *Nguyên tắc:* Luôn ưu tiên mở rộng nút ở nhánh sâu nhất trong cây tìm kiếm.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình DFS duyệt các trạng thái tại đây.)*
    * **Tìm kiếm sâu lặp (Iterative Deepening Depth-First Search - IDDFS):**
        * *Nguyên tắc:* Kết hợp ưu điểm của DFS (ít tốn bộ nhớ) và BFS (tìm lời giải nông nhất, tính đầy đủ) bằng cách thực hiện DFS với giới hạn độ sâu tăng dần.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình IDDFS tại đây.)*
    * **Tìm kiếm Backtracking (Backtracking Search):**
        * *Nguyên tắc:* Một dạng của DFS, thử từng khả năng cho đến khi tìm thấy lời giải. Nếu một nhánh không dẫn đến lời giải, nó sẽ quay lui (backtrack) và thử nhánh khác.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình Backtracking tại đây.)*

* **So sánh hiệu suất:**
    * *(Đề xuất: Tại đây, bạn có thể trình bày bảng hoặc biểu đồ so sánh hiệu suất của các thuật toán trên dựa trên các tiêu chí như: Thời gian tìm kiếm, Số bước trong lời giải, Số trạng thái đã duyệt, Bộ nhớ sử dụng. Dữ liệu này có thể thu thập được từ việc chạy các thuật toán trong `UI.py` và `AI.py`.)*

* **Nhận xét về hiệu suất trên 8-Puzzle:**
    * **BFS:** Luôn tìm thấy lời giải ngắn nhất (nếu tồn tại) vì nó duyệt theo từng mức. Tuy nhiên, tốn nhiều bộ nhớ do phải lưu trữ tất cả các nút ở biên.
    * **UCS:** Tương tự BFS khi chi phí mỗi bước là như nhau; đảm bảo tìm ra lời giải có chi phí thấp nhất. Cũng gặp vấn đề về bộ nhớ.
    * **DFS:** Ít tốn bộ nhớ hơn BFS vì chỉ lưu trữ các nút trên đường đi hiện tại. Tuy nhiên, có thể bị lạc vào các nhánh rất sâu và không đảm bảo tìm ra lời giải ngắn nhất (hoặc có thể không tìm ra lời giải nếu không gian tìm kiếm vô hạn và không có giới hạn độ sâu).
    * **IDDFS:** Kết hợp được ưu điểm của BFS và DFS. Tìm ra lời giải ngắn nhất và ít tốn bộ nhớ hơn BFS. Tuy nhiên, có thể duyệt lại các trạng thái ở các mức trên nhiều lần.
    * **Backtracking Search:** Tương tự DFS về mặt không gian và có thể không tối ưu về lời giải. Hiệu quả phụ thuộc nhiều vào thứ tự thử các hành động.

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed Search Algorithms)

Các thuật toán này sử dụng hàm đánh giá heuristic `h(n)` để ước lượng chi phí từ trạng thái hiện tại đến trạng thái đích, giúp hướng dẫn tìm kiếm hiệu quả hơn.

* **Thành phần chính và solution:** Tương tự như mục 2.1. Điểm khác biệt chính là việc sử dụng hàm heuristic.

* **Các hàm Heuristic được sử dụng (trong `AI.py`):**
    * **Số ô sai vị trí (Misplaced Tiles / Hamming Distance):** Đếm số ô (không tính ô trống) đang không nằm ở vị trí đúng so với trạng thái đích. (Hàm `Count_Different` trong `AI.py`)
    * **Khoảng cách Manhattan (Manhattan Distance):** Tổng khoảng cách (theo chiều ngang và chiều dọc) của mỗi ô (không tính ô trống) từ vị trí hiện tại đến vị trí đúng của nó trong trạng thái đích. (Hàm `Manhattan_Heuristic` trong `AI.py`)

* **Các thuật toán được triển khai (trong `AI.py`):**
    * **Tìm kiếm Tham lam (Greedy Best-First Search):**
        * *Nguyên tắc:* Luôn mở rộng nút được đánh giá là gần đích nhất theo hàm heuristic `h(n)`.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình Greedy Search tại đây.)*
    * **A\* Search:**
        * *Nguyên tắc:* Mở rộng nút có tổng `f(n) = g(n) + h(n)` nhỏ nhất, trong đó `g(n)` là chi phí thực tế từ trạng thái đầu đến `n`, và `h(n)` là chi phí ước lượng từ `n` đến đích.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình A\* Search tại đây.)*
    * **IDA\* (Iterative Deepening A\*):**
        * *Nguyên tắc:* Tương tự IDDFS nhưng thay vì giới hạn độ sâu, nó giới hạn giá trị `f(n)`.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình IDA\* tại đây.)*
    * **Beam Search:**
        * *Nguyên tắc:* Tại mỗi bước, chỉ giữ lại một số lượng `k` (beam width) trạng thái tốt nhất để mở rộng tiếp.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình Beam Search tại đây.)*
    * **Tìm kiếm Leo đồi (Hill Climbing):**
        * *Các biến thể:*
            * **Simple Hill Climbing:** Chọn một hàng xóm tốt hơn trạng thái hiện tại.
            * **Stochastic Hill Climbing:** Chọn ngẫu nhiên một trong số các hàng xóm tốt hơn.
            * **Steepest Ascent Hill Climbing:** Chọn hàng xóm tốt nhất trong tất cả các hàng xóm.
        * *Nguyên tắc:* Di chuyển đến trạng thái lân cận tốt hơn cho đến khi không còn trạng thái lân cận nào tốt hơn (đạt local maximum).
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo ảnh GIF cho từng biến thể của Hill Climbing.)*
    * **Luyện kim mô phỏng (Simulated Annealing):**
        * *Nguyên tắc:* Tương tự Hill Climbing nhưng cho phép di chuyển đến trạng thái xấu hơn với một xác suất nhất định, giảm dần theo "nhiệt độ" để tránh bị kẹt ở local maximum.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình Simulated Annealing.)*
    * **Thuật toán Di truyền (Genetic Algorithm):**
        * *Nguyên tắc:* Mô phỏng quá trình tiến hóa tự nhiên, sử dụng các toán tử như lựa chọn, lai ghép (crossover), và đột biến (mutation) trên một quần thể các giải pháp tiềm năng.
        * *Hình ảnh gif minh họa:*
            * *(Đề xuất: Bạn có thể tạo một ảnh GIF minh họa quá trình Genetic Algorithm.)*
    * **Tìm kiếm AND-OR (AND-OR Search):**
        * *Nguyên tắc:* Dùng để giải các bài toán có thể được phân rã thành các bài toán con (AND nodes) hoặc các lựa chọn thay thế (OR nodes). Kết quả được in ra console.
        * *Minh họa:* Quá trình tìm kiếm và kết quả được hiển thị trên console.
    * **Tìm kiếm trong không gian niềm tin (Belief State Search):**
        * *Nguyên tắc:* Áp dụng cho các môi trường không quan sát được hoàn toàn, nơi agent duy trì một "niềm tin" về trạng thái hiện tại của nó. Kết quả được in ra console.
        * *Minh họa:* Quá trình tìm kiếm và kết quả được hiển thị trên console.
    * **Q-Learning:**
        * *Nguyên tắc:* Một thuật toán học tăng cường không cần mô hình, học một hàm giá trị hành động (Q-value) để chọn hành động tối ưu.
        * *Minh họa:* Quá trình học và đường đi tìm được (có thể in ra console hoặc trực quan hóa nếu được hỗ trợ).
    * **Forward Checking (trong CSP):**
        * *Nguyên tắc:* Một kỹ thuật được sử dụng trong các bài toán thỏa mãn ràng buộc (CSP). Khi một biến được gán một giá trị, nó kiểm tra và loại bỏ các giá trị không nhất quán khỏi các biến chưa được gán.
        * *Minh họa:* Quá trình tìm kiếm và đường đi.
    * **AC-3 (trong CSP):**
        * *Nguyên tắc:* Một thuật toán để đảm bảo tính nhất quán cung (arc consistency) trong các bài toán CSP. Nó tạo ra các bảng ngẫu nhiên và lọc để đảm bảo các ràng buộc.
        * *Minh họa:* Kết quả là một bảng (board) thỏa mãn các ràng buộc nhất định.

* **So sánh hiệu suất:**
    * *(Đề xuất: Tương tự mục 2.1, trình bày bảng hoặc biểu đồ so sánh hiệu suất của các thuật toán có thông tin, có thể so sánh thêm ảnh hưởng của các hàm heuristic khác nhau.)*

* **Nhận xét về hiệu suất trên 8-Puzzle:**
    * **Greedy Search:** Thường nhanh chóng tìm ra lời giải nhưng không đảm bảo tối ưu. Chất lượng lời giải phụ thuộc nhiều vào hàm heuristic.
    * **A\* Search:** Nếu hàm heuristic là chấp nhận được (admissible - không đánh giá quá cao chi phí thực tế), A\* đảm bảo tìm ra lời giải tối ưu và thường hiệu quả hơn nhiều so_với các thuật toán không có thông tin. Với heuristic Manhattan, A\* hoạt động tốt cho 8-Puzzle.
    * **IDA\*:** Giống A\* về tính tối ưu và sử dụng heuristic, nhưng tiết kiệm bộ nhớ hơn đáng kể, phù hợp cho các không gian tìm kiếm lớn.
    * **Beam Search:** Không đảm bảo tìm ra lời giải tối ưu hoặc thậm chí là bất kỳ lời giải nào, nhưng có thể hiệu quả về mặt thời gian và bộ nhớ khi beam width được chọn hợp lý.
    * **Hill Climbing:** Dễ bị kẹt ở local maximum (trạng thái tốt hơn tất cả hàng xóm nhưng không phải là trạng thái tốt nhất toàn cục). Các biến thể như Stochastic Hill Climbing hoặc khởi tạo lại ngẫu nhiên có thể giúp giảm thiểu vấn đề này.
    * **Simulated Annealing:** Có khả năng thoát khỏi local maximum tốt hơn Hill Climbing, nhưng cần điều chỉnh cẩn thận các tham số (nhiệt độ ban đầu, tốc độ làm nguội).
    * **Genetic Algorithm:** Có thể tìm ra các giải pháp tốt cho các bài toán phức tạp, nhưng thường đòi hỏi nhiều thời gian tính toán và điều chỉnh tham số (kích thước quần thể, tỷ lệ lai ghép/đột biến).
    * **AND-OR Search, Belief State Search:** Các thuật toán chuyên biệt cho các loại bài toán cụ thể hơn là tìm kiếm đường đi đơn giản. Hiệu suất phụ thuộc vào cấu trúc của bài toán.
    * **Q-Learning:** Hiệu suất phụ thuộc vào số lượng episodes huấn luyện, hàm phần thưởng, và các tham số như epsilon (exploration rate). Có thể tìm ra chính sách tối ưu sau khi học đủ.
    * **Forward Checking, AC-3:** Là các thuật toán/kỹ thuật cho Bài toán Thỏa mãn Ràng buộc (CSP), giúp giảm không gian tìm kiếm bằng cách loại bỏ sớm các giá trị không thể dẫn đến lời giải.

### 2.3. Giao diện người dùng (`UI.py`)

* **Mô tả chung:** File `UI.py` sử dụng thư viện Pygame để tạo giao diện đồ họa cho người dùng tương tác với bài toán 8-Puzzle.
* **Chức năng chính:**
    * Hiển thị trạng thái đầu, trạng thái hiện tại và trạng thái đích của puzzle.
    * Cho phép người dùng chọn thuật toán để giải.
    * Cho phép tạo puzzle ngẫu nhiên hoặc nhập puzzle thủ công.
    * Hiển thị quá trình giải từng bước một hoặc xem kết quả cuối cùng.
    * Hiển thị thông tin về số bước và thời gian tìm kiếm (nếu có).
    * Thông báo về khả năng giải được của puzzle.
* **(Đề xuất: Bạn có thể thêm ảnh chụp màn hình giao diện tại đây.)**

## 3. Kết luận

Dự án này đã thành công trong việc:

* **Triển khai đa dạng các thuật toán tìm kiếm:** Bao gồm cả các thuật toán tìm kiếm không có thông tin và có thông tin, cũng như một số thuật toán nâng cao và học tăng cường.
* **Xây dựng giao diện người dùng trực quan:** Giúp người dùng dễ dàng tương tác, thử nghiệm và quan sát cách các thuật toán hoạt động để giải bài toán 8-Puzzle.
* **Cung cấp nền tảng để so sánh và đánh giá thuật toán:** Người dùng có thể tự mình so sánh hiệu suất của các thuật toán khác nhau dựa trên thời gian giải, số bước, và các thông tin khác được cung cấp bởi giao diện.
* **Minh họa các khái niệm cơ bản của Trí Tuệ Nhân Tạo:** Giúp người học hiểu rõ hơn về các khái niệm như không gian trạng thái, heuristic, và các chiến lược tìm kiếm khác nhau.

**(Đề xuất: Bạn có thể bổ sung thêm các kết quả cụ thể đã đạt được, ví dụ như thuật toán nào hoạt động hiệu quả nhất cho các trường hợp thử nghiệm cụ thể, hoặc những thách thức gặp phải và cách giải quyết.)**

---

**Hướng dẫn sử dụng:**

1.  Đảm bảo bạn đã cài đặt thư viện Pygame (`pip install pygame`).
2.  Chạy file `UI.py` để khởi động chương trình.
3.  Sử dụng các nút trên giao diện để tạo puzzle, chọn thuật toán và bắt đầu quá trình giải.