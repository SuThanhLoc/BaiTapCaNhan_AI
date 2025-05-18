# GIẢI BÀI TOÁN 8 PUZZLE BẰNG CÁC THUẬT TOÁN TÌM KIẾM

## 1. MỤC TIÊU

* Mô tả mục tiêu của dự án này. Ví dụ:
    * Nghiên cứu và triển khai các thuật toán tìm kiếm khác nhau để giải bài toán 8-puzzle.
    * Phân tích, so sánh hiệu suất (thời gian, số bước, bộ nhớ sử dụng) của các thuật toán.
    * Xây dựng một giao diện người dùng trực quan để minh họa quá trình giải và tương tác với các thuật toán.

## 2. NỘI DUNG

Trong bài toán 8-puzzle, các thành phần chính của một bài toán tìm kiếm bao gồm:

* **Không gian trạng thái (State Space):** Tập hợp tất cả các cấu hình (sắp xếp) có thể có của các ô số trên bảng 3x3.
* **Trạng thái ban đầu (Initial State):** Cấu hình xuất phát của bài toán.
* **Trạng thái đích (Goal State):** Cấu hình mong muốn mà thuật toán cần đạt tới (thường là các số được sắp xếp theo thứ tự từ 1 đến 8, với ô trống ở vị trí cuối cùng hoặc một vị trí xác định trước).
* **Hành động (Actions):** Các phép toán cho phép chuyển từ trạng thái này sang trạng thái khác. Trong bài toán 8-puzzle, hành động là di chuyển ô trống lên, xuống, trái, hoặc phải (nếu có thể).
* **Hàm chuyển đổi (Transition Model):** Mô tả trạng thái kết quả khi thực hiện một hành động từ một trạng thái nhất định.
* **Chi phí đường đi (Path Cost):** Thường là số bước di chuyển để đạt được trạng thái đích. Trong một số thuật toán (như Uniform Cost Search), mỗi bước có thể có chi phí khác nhau, nhưng trong bài toán 8-puzzle cơ bản, mỗi bước thường có chi phí là 1.

**Solution (Lời giải):** Là một chuỗi các hành động (hoặc một dãy các trạng thái) dẫn từ trạng thái ban đầu đến trạng thái đích. Một lời giải tối ưu là lời giải có chi phí đường đi nhỏ nhất.

---

### 2.1. Tìm kiếm không có thông tin (Uninformed Search)

* **Đặc điểm chung:** Các thuật toán trong nhóm này không sử dụng bất kỳ thông tin nào về "khoảng cách" hay "hướng" đến trạng thái đích. Chúng chỉ duyệt qua không gian trạng thái một cách có hệ thống.
* **Thành phần chính của bài toán:** Như đã mô tả ở trên.
* **Solution:** Một đường đi từ trạng thái đầu đến trạng thái đích.

#### a. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
* **Mô tả ngắn gọn:** Duyệt các nút theo từng mức, đảm bảo tìm ra lời giải nông nhất (ít bước nhất).
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh (chắc chắn tìm thấy lời giải nếu có), tối ưu (tìm ra lời giải ít bước nhất).
    * Nhược điểm: Tốn nhiều bộ nhớ (lưu trữ tất cả các nút ở biên), thời gian thực thi có thể lâu nếu lời giải ở sâu.

#### b. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
* **Mô tả ngắn gọn:** Ưu tiên duyệt sâu xuống một nhánh của cây tìm kiếm trước khi quay lui.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Ít tốn bộ nhớ hơn BFS (chỉ lưu trữ các nút trên đường đi hiện tại).
    * Nhược điểm: Không hoàn chỉnh nếu cây có nhánh vô hạn và không có kiểm tra lặp, không đảm bảo tìm ra lời giải tối ưu. Trong bài toán 8-puzzle với không gian trạng thái hữu hạn, DFS có thể tìm ra lời giải nhưng không chắc là ngắn nhất.

#### c. IDDFS (Iterative Deepening Depth-First Search - Tìm kiếm sâu dần lặp)
* **Mô tả ngắn gọn:** Kết hợp ưu điểm của BFS (tính tối ưu về số bước) và DFS (ít tốn bộ nhớ) bằng cách thực hiện DFS lặp đi lặp lại với giới hạn độ sâu tăng dần.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh, tối ưu (tìm ra lời giải ít bước nhất), ít tốn bộ nhớ hơn BFS.
    * Nhược điểm: Lặp lại việc duyệt các nút ở các mức trên, nhưng chi phí này thường không đáng kể so với lợi ích.

#### d. UCS (Uniform Cost Search - Tìm kiếm chi phí đồng nhất)
* **Mô tả ngắn gọn:** Mở rộng nút có chi phí đường đi $g(n)$ nhỏ nhất từ trạng thái bắt đầu. Tương tự BFS nếu chi phí mỗi bước là như nhau.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh, tối ưu (nếu chi phí đường đi là không âm).
    * Nhược điểm: Có thể khám phá các đường đi dài không cần thiết nếu chi phí thấp, tương tự BFS về bộ nhớ và thời gian trong trường hợp chi phí bước là 1.

---

### 2.2. Tìm kiếm có thông tin (Informed Search / Heuristic Search)

* **Đặc điểm chung:** Sử dụng hàm đánh giá heuristic $h(n)$ để ước lượng chi phí từ trạng thái hiện tại $n$ đến trạng thái đích.
* **Thành phần chính của bài toán:** Bổ sung hàm heuristic $h(n)$.
* **Solution:** Một đường đi từ trạng thái đầu đến trạng thái đích, thường được tối ưu hóa hơn nhờ heuristic.

#### a. Greedy Search (Best-First Search tham lam)
* **Mô tả ngắn gọn:** Luôn chọn mở rộng nút có vẻ "gần" đích nhất theo hàm heuristic $h(n)$.
* **Hình ảnh GIF minh họa:**
    ![Hình ảnh GIF minh họa](image/A_START.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Thường nhanh hơn các thuật toán không thông tin.
    * Nhược điểm: Không hoàn chỉnh, không đảm bảo tối ưu (có thể bị "mắc kẹt" ở các cực tiểu địa phương hoặc đi theo đường dài).

#### b. A* Search (A Sao)
* **Mô tả ngắn gọn:** Kết hợp chi phí đường đi thực tế $g(n)$ và chi phí ước lượng $h(n)$ để đánh giá nút: $f(n) = g(n) + h(n)$.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh và tối ưu nếu hàm heuristic $h(n)$ là chấp nhận được (admissible - không đánh giá quá cao chi phí thực tế) và nhất quán (consistent - monotonic). Thường hiệu quả hơn nhiều so với các thuật toán không thông tin.
    * Nhược điểm: Vẫn có thể tốn nhiều bộ nhớ để lưu trữ các nút trên biên.

#### c. IDA* Search (Iterative Deepening A* - A* sâu dần lặp)
* **Mô tả ngắn gọn:** Phiên bản A* sử dụng ít bộ nhớ hơn bằng cách áp dụng kỹ thuật sâu dần lặp dựa trên giá trị $f(n)$.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh và tối ưu (với heuristic chấp nhận được), sử dụng bộ nhớ hiệu quả như DFS.
    * Nhược điểm: Lặp lại việc duyệt các nút, có thể tốn thời gian hơn A* trong một số trường hợp.

---

### 2.3. Tìm kiếm cục bộ (Local Search)

* **Đặc điểm chung:** Duy trì một trạng thái hiện tại và cố gắng cải thiện nó bằng cách di chuyển đến các trạng thái lân cận. Không quan tâm đến đường đi đã qua.
* **Thành phần chính của bài toán:** Trạng thái hiện tại, hàm đánh giá (thường là heuristic để cực tiểu hóa).
* **Solution:** Trạng thái cuối cùng đạt được, hy vọng là trạng thái đích hoặc một trạng thái tốt.

#### a. Simple Hill Climbing (Leo đồi đơn giản)
* **Mô tả ngắn gọn:** Liên tục di chuyển đến trạng thái lân cận tốt hơn cho đến khi không còn trạng thái lân cận nào tốt hơn (đạt đỉnh cục bộ).
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Ít tốn bộ nhớ, nhanh.
    * Nhược điểm: Dễ bị mắc kẹt ở cực tiểu địa phương, không hoàn chỉnh, không tối ưu.

#### b. Steepest Ascent Hill Climbing (Leo đồi dốc nhất)
* **Mô tả ngắn gọn:** Tương tự Simple Hill Climbing, nhưng chọn trạng thái lân cận "tốt nhất" (dốc nhất) trong số tất cả các lân cận.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Tương tự Simple Hill Climbing.
    * Nhược điểm: Tương tự Simple Hill Climbing, vẫn có thể bị mắc kẹt.

#### c. Stochastic Hill Climbing (Leo đồi ngẫu nhiên)
* **Mô tả ngắn gọn:** Chọn một trạng thái lân cận tốt hơn một cách ngẫu nhiên, cho phép thoát khỏi một số đỉnh cục bộ.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng thoát khỏi cực tiểu địa phương tốt hơn Simple/Steepest Ascent.
    * Nhược điểm: Vẫn không đảm bảo hoàn chỉnh hay tối ưu.

#### d. Simulated Annealing (Luyện kim mô phỏng)
* **Mô tả ngắn gọn:** Cho phép di chuyển đến trạng thái "xấu hơn" với một xác suất nhất định, xác suất này giảm dần theo thời gian (nhiệt độ). Giúp thoát khỏi các cực tiểu địa phương.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng tìm ra lời giải tốt hơn Hill Climbing, hoàn chỉnh nếu nhiệt độ giảm đủ chậm.
    * Nhược điểm: Cần tinh chỉnh các tham số (lịch trình giảm nhiệt độ), có thể chậm.

#### e. Genetic Algorithm (Thuật toán di truyền)
* **Mô tả ngắn gọn:** Mô phỏng quá trình tiến hóa tự nhiên, duy trì một quần thể các lời giải, áp dụng các toán tử lai ghép (crossover) và đột biến (mutation) để tạo ra các thế hệ mới.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng tìm kiếm trong không gian lớn và phức tạp, thoát khỏi cực tiểu địa phương.
    * Nhược điểm: Cần nhiều tham số để tinh chỉnh, có thể hội tụ chậm, không đảm bảo tìm ra lời giải tối ưu tuyệt đối.

#### f. Beam Search (Tìm kiếm chùm)
* **Mô tả ngắn gọn:** Biến thể của Best-First Search, chỉ giữ lại một số lượng giới hạn (beam width - độ rộng chùm) các trạng thái tốt nhất ở mỗi bước để mở rộng, nhằm giảm bộ nhớ.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Giảm đáng kể bộ nhớ so với Best-First Search toàn cục.
    * Nhược điểm: Không hoàn chỉnh (có thể loại bỏ nhánh chứa lời giải tốt), không đảm bảo tối ưu.

---

### 2.4. Tìm kiếm trong môi trường phức tạp

#### a. And-Or Search (Tìm kiếm Và-Hoặc)
* **Mô tả ngắn gọn:** Dùng cho các bài toán có thể được phân rã thành các bài toán con (AND nodes - nút Và) hoặc có nhiều cách giải quyết khác nhau (OR nodes - nút Hoặc).
* **Thành phần chính của bài toán:** Các nút AND (cần giải quyết tất cả các bài toán con) và nút OR (chỉ cần giải quyết một trong các bài toán con).
* **Solution:** Một cây con lời giải, chứng minh rằng bài toán gốc có thể được giải quyết.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây, hoặc mô tả cách nó hoạt động với 8-puzzle nếu có cách tiếp cận cụ thể)
    ```
* **Nhận xét hiệu suất:**
    * Trong ngữ cảnh 8-puzzle tiêu chuẩn, And-Or Search không phải là cách tiếp cận trực tiếp phổ biến. Nó phù hợp hơn cho các bài toán lập kế hoạch hoặc suy luận logic. Nếu bạn có một cách áp dụng cụ thể, hãy mô tả nó.

---

### 2.5. Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Problems - CSPs)

* **Đặc điểm chung:** Tìm kiếm một trạng thái thỏa mãn một tập hợp các ràng buộc.
* **Thành phần chính của bài toán:** Các biến, miền giá trị cho mỗi biến, và các ràng buộc giữa các biến.
* **Solution:** Một phép gán giá trị cho tất cả các biến sao cho tất cả các ràng buộc đều được thỏa mãn.
* *Lưu ý:* Bài toán 8-puzzle có thể được coi là một bài toán tìm đường đi, không phải là một CSP điển hình. Tuy nhiên, các kỹ thuật CSP có thể được điều chỉnh hoặc truyền cảm hứng cho các thuật toán tìm kiếm.

#### a. Backtracking Search (Tìm kiếm quay lui)
* **Mô tả ngắn gọn:** Xây dựng lời giải từng phần, nếu một lựa chọn dẫn đến vi phạm ràng buộc hoặc không thể hoàn thành lời giải, thuật toán sẽ quay lui và thử lựa chọn khác. Đây là một dạng của DFS.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Tương tự DFS về bộ nhớ.
    * Nhược điểm: Có thể rất chậm nếu không có các heuristic hoặc kỹ thuật tối ưu hóa tốt.

#### b. Forward Checking (Kiểm tra ràng buộc phía trước)
* **Mô tả ngắn gọn:** Khi gán một giá trị cho một biến, thuật toán kiểm tra trước các ràng buộc liên quan đến các biến chưa được gán và loại bỏ các giá trị không tương thích khỏi miền của chúng. Giúp phát hiện bế tắc sớm hơn.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Thường hiệu quả hơn Backtracking đơn thuần bằng cách giảm không gian tìm kiếm.
    * Nhược điểm: Chi phí kiểm tra phía trước có thể đáng kể.

#### c. AC-3 (Arc Consistency Algorithm #3 - Thuật toán nhất quán cung AC-3)
* **Mô tả ngắn gọn:** Một thuật toán tiền xử lý (hoặc dùng trong quá trình tìm kiếm) để loại bỏ các giá trị không nhất quán khỏi miền của các biến trong một CSP. Đảm bảo rằng với mỗi giá trị của một biến, tồn tại ít nhất một giá trị tương thích cho mỗi biến khác có ràng buộc với nó.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây - Lưu ý: AC-3 thường không trực tiếp giải 8-puzzle mà dùng để xử lý ràng buộc. Trong code của bạn, nó được dùng để tạo puzzle hợp lệ.)
    ```
* **Nhận xét hiệu suất:**
    * AC-3 không phải là thuật toán tìm đường đi cho 8-puzzle. Trong project này, bạn đã sử dụng nó để tạo ra các trạng thái puzzle hợp lệ và có thể giải được. Điều này đảm bảo rằng các thuật toán tìm kiếm khác có một bài toán có ý nghĩa để giải.

---

### 2.6. Học máy (Machine Learning)

#### a. Q-Learning (Học Q)
* **Mô tả ngắn gọn:** Một thuật toán học tăng cường không cần mô hình (model-free). Tác tử học một hàm giá trị hành động (Q-value) cho mỗi cặp (trạng thái, hành động), cho biết "chất lượng" của việc thực hiện hành động đó tại trạng thái đó.
* **Thành phần chính của bài toán:** Tác tử (Agent), môi trường (Environment), trạng thái (State), hành động (Action), phần thưởng (Reward), hàm Q (Q-function).
* **Solution:** Một chính sách (policy) tối ưu, cho biết hành động tốt nhất cần thực hiện ở mỗi trạng thái để tối đa hóa tổng phần thưởng kỳ vọng.
* **Hình ảnh GIF minh họa:**
    ```
    (Thêm hình ảnh GIF của bạn ở đây, minh họa quá trình học hoặc quá trình giải sau khi học)
    ```
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có thể học để giải các bài toán phức tạp mà không cần biết trước mô hình của môi trường.
    * Nhược điểm: Cần nhiều lượt tương tác để học, việc thiết kế phần thưởng phù hợp là quan trọng, tốn nhiều thời gian và bộ nhớ để lưu trữ bảng Q_table cho các không gian trạng thái lớn.

---

### Hình ảnh so sánh hiệu suất của các thuật toán
### Một vài nhận xét chung về hiệu suất các nhóm thuật toán

* **Tìm kiếm không có thông tin:** Đảm bảo tính hoàn chỉnh và tối ưu (BFS, IDDFS, UCS) nhưng thường chậm và tốn bộ nhớ cho các bài toán phức tạp. DFS nhanh hơn về bộ nhớ nhưng không tối ưu.
* **Tìm kiếm có thông tin:** Hiệu quả hơn nhiều nếu có heuristic tốt (A*, IDA*). Greedy nhanh nhưng không đảm bảo tối ưu.
* **Tìm kiếm cục bộ:** Nhanh và ít tốn bộ nhớ, nhưng dễ bị mắc kẹt ở cực tiểu địa phương và không đảm bảo tìm ra lời giải (trừ Simulated Annealing và Genetic Algorithm có cơ chế thoát).
* **Tìm kiếm với ràng buộc:** Backtracking và Forward Checking là các kỹ thuật tổng quát cho CSPs, có thể áp dụng nhưng cần điều chỉnh cho bài toán tìm đường đi.
* **Học máy (Q-Learning):** Một cách tiếp cận khác, học từ kinh nghiệm, có thể mạnh mẽ nhưng đòi hỏi quá trình huấn luyện.

## 3. KẾT LUẬN
    * Đã triển khai thành công những thuật toán tìm kiếm khác nhau cho bài toán 8-puzzle.
    * Xây dựng được giao diện người dùng cho phép người dùng tương tác và quan sát quá trình giải.
    * Phân tích và so sánh cho thấy thuật toán một số thuật toán có vẻ hiệu quả nhất trong việc giải 8-puzzle.
    * Rút ra những bài học từ những lần vấp ngã (thuật toán chạy không như ý muốn).
    * Những điều học hỏi được qua dự án.

## 4. HƯỚNG DẪN THỰC THI

Để chạy chương trình và trải nghiệm trò chơi:

1.  **Cách sử dụng giao diện:**
    * Vào File "UI.py" để khởi chạy từ IDE mà bạn sử dụng.
    * Các nút bấm chính: "NGẪU NHIÊN", "NHẬP TAY", "GIẢI", "XEM KẾT QUẢ", "LÙI", "RESET", "TIẾN".
    * chọn thuật toán từ danh sách mà bạn muốn.
    * Nhấn nút "CHẠY" để khởi chạy thuật toán.
    * sau khi thuật toán đã chạy xong.
    * Nhấn nút "RESET" để có thể chọn thuật toán khác để chạychạy
    * Nhập puzzle bằng tay (nút NHẬP TAY).

## 5. SINH VIÊN THỰC HIỆN

* **Họ và tên:** Sử Thanh LộcLộc
* **Mã số sinh viên:** [Mã số sinh viên của bạn]
* **(Tùy chọn) Link GitHub (nếu có):** https://github.com/SuThanhLoc/BaiTapCaNhan_AI