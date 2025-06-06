# GIẢI BÀI TOÁN 8 PUZZLE BẰNG CÁC THUẬT TOÁN TÌM KIẾM

## 1. MỤC TIÊU

* Mô tả mục tiêu của dự án này. Ví dụ:
    * Nghiên cứu và triển khai các thuật toán tìm kiếm khác nhau để giải bài toán 8-puzzle.
    * Phân tích, so sánh hiệu suất (thời gian, số bước) của các thuật toán.
    * Xây dựng một giao diện người dùng trực quan để minh họa quá trình giải và tương tác với các thuật toán.

## 2. NỘI DUNG

Trong bài toán 8-puzzle, các thành phần chính của một bài toán tìm kiếm bao gồm:

* **Không gian trạng thái (State Space):** Tập hợp tất cả các trạng thái có thể có của các ô số trên bảng 3x3.
* **Trạng thái ban đầu (Initial State):** Trạng thái bắt đầu của bài toán.
* **Trạng thái đích (Goal State):** Là trạng thái mà thuật toán cần đạt tới (các số được sắp xếp theo thứ tự từ 1 đến 8, với ô trống ở vị trí cuối cùng).
* **Hành động (Actions):** Hành động là di chuyển ô trống lên, xuống, trái, hoặc phải.
* **Hàm chuyển đổi (Transition Model):** Mô tả trạng thái kết quả khi thực hiện một hành động từ một trạng thái nhất định.
* **Chi phí đường đi (Path Cost):** Là số bước di chuyển để đạt được trạng thái đích. mỗi bước có chi phí là 1.

**Solution (Lời giải):** Là một chuỗi các hành động dẫn từ trạng thái đầu đến trạng thái đích. Một lời giải tối ưu là lời giải có chi phí đường đi nhỏ nhất.

---

### 2.1. Tìm kiếm không có thông tin

* **Đặc điểm chung:** Các thuật toán trong nhóm này không sử dụng bất kỳ thông tin nào về "khoảng cách" hay "hướng" đến trạng thái đích. Chúng chỉ duyệt qua không gian trạng thái một cách có hệ thống.
* **Thành phần chính của bài toán:** Như đã mô tả ở trên.
* **Solution:** Một đường đi từ trạng thái đầu đến trạng thái đích.

#### a. BFS
* **Mô tả ngắn gọn:** Duyệt các nút theo từng mức, đảm bảo tìm ra lời giải nông nhất (ít bước nhất).
* ![alt text](BFS.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh (chắc chắn tìm thấy lời giải nếu có), tối ưu (tìm ra lời giải ít bước nhất).
    * Nhược điểm: Tốn nhiều bộ nhớ (lưu trữ tất cả các nút ở biên), thời gian thực thi có thể lâu nếu lời giải ở sâu.

#### b. DFS
* **Mô tả ngắn gọn:** Ưu tiên duyệt sâu xuống một nhánh của cây tìm kiếm trước khi quay lui.
*   ![alt text](DFS.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Ít tốn bộ nhớ hơn BFS (chỉ lưu trữ các nút trên đường đi hiện tại).
    * Nhược điểm: Không hoàn chỉnh nếu cây có nhánh vô hạn và không có kiểm tra lặp, không đảm bảo tìm ra lời giải tối ưu. Trong bài toán 8-puzzle với không gian trạng thái hữu hạn, DFS có thể tìm ra lời giải nhưng không chắc là ngắn nhất.

#### c. IDDFS
* **Mô tả ngắn gọn:** Kết hợp ưu điểm của BFS (tính tối ưu về số bước) và DFS (ít tốn bộ nhớ) bằng cách thực hiện DFS lặp đi lặp lại với giới hạn độ sâu tăng dần.
*   ![alt text](IDDFS.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh, tối ưu (tìm ra lời giải ít bước nhất), ít tốn bộ nhớ hơn BFS.
    * Nhược điểm: Lặp lại việc duyệt các nút ở các mức trên, nhưng chi phí này thường không đáng kể so với lợi ích.

#### d. UCS
* **Mô tả ngắn gọn:** Mở rộng nút có chi phí đường đi $g(n)$ nhỏ nhất từ trạng thái bắt đầu. Tương tự BFS nếu chi phí mỗi bước là như nhau.
*   ![alt text](UCS.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh, tối ưu (nếu chi phí đường đi là không âm).
    * Nhược điểm: Có thể khám phá các đường đi dài không cần thiết nếu chi phí thấp, tương tự BFS về bộ nhớ và thời gian trong trường hợp chi phí bước là 1.

---

### 2.2. Tìm kiếm có thông tin

* **Đặc điểm chung:** Sử dụng hàm đánh giá heuristic $h(n)$ để ước lượng chi phí từ trạng thái hiện tại $n$ đến trạng thái đích.
* **Thành phần chính của bài toán:** Bổ sung hàm heuristic $h(n)$.
* **Solution:** Một đường đi từ trạng thái đầu đến trạng thái đích, thường được tối ưu hóa hơn nhờ heuristic.

#### a. Greedy Search
* **Mô tả ngắn gọn:** Luôn chọn mở rộng nút có vẻ "gần" đích nhất theo hàm heuristic $h(n)$.
*   ![alt text](GREEDY.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Thường nhanh hơn các thuật toán không thông tin.
    * Nhược điểm: Không hoàn chỉnh, không đảm bảo tối ưu (có thể bị "mắc kẹt" ở các cực tiểu địa phương hoặc đi theo đường dài).

#### b. A* Searchh
* **Mô tả ngắn gọn:** Kết hợp chi phí đường đi thực tế $g(n)$ và chi phí ước lượng $h(n)$ để đánh giá nút: $f(n) = g(n) + h(n)$.

    ![alt text](A_START.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh và tối ưu nếu hàm heuristic $h(n)$ là chấp nhận được (không đánh giá quá cao chi phí thực tế) và nhất quán. Thường hiệu quả hơn nhiều so với các thuật toán không thông tin.
    * Nhược điểm: Vẫn tốn nhiều bộ nhớ để lưu trữ các nút trên biên.

#### c. IDA* Search
* **Mô tả ngắn gọn:** Phiên bản A* sử dụng ít bộ nhớ hơn bằng cách áp dụng kỹ thuật sâu dần lặp dựa trên giá trị $f(n)$.
*   ![alt text](IDA_START.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Hoàn chỉnh và tối ưu (heuristic chấp nhận được), sử dụng bộ nhớ hiệu quả như DFS.
    * Nhược điểm: Lặp lại việc duyệt các nút, có thể tốn thời gian hơn A* trong một số trường hợp.

---

### 2.3. Tìm kiếm cục bộ

* **Đặc điểm chung:** Duy trì một trạng thái hiện tại và cố gắng cải thiện nó bằng cách di chuyển đến các trạng thái lân cận. Không quan tâm đến đường đi đã qua.
* **Thành phần chính của bài toán:** Trạng thái hiện tại, hàm đánh giá (heuristic để cực tiểu hóa).
* **Solution:** Trạng thái cuối cùng đạt được, hy vọng là trạng thái đích hoặc một trạng thái tốt.

#### a. Simple Hill Climbing
* **Mô tả ngắn gọn:** Liên tục di chuyển đến trạng thái lân cận tốt hơn cho đến khi không còn trạng thái lân cận nào tốt hơn (đạt đỉnh cục bộ).
* **Nhận xét hiệu suất:**
    * Ưu điểm: Ít tốn bộ nhớ, nhanh.
    * Nhược điểm: Dễ bị mắc kẹt ở cực tiểu địa phương, không hoàn chỉnh, không tối ưu.

#### b. Steepest Ascent Hill Climbing
* **Mô tả ngắn gọn:** Tương tự Simple Hill Climbing, nhưng chọn trạng thái lân cận "tốt nhất" (dốc nhất) trong số tất cả các lân cận.
* **Nhận xét hiệu suất:**
    * Ưu điểm: Tương tự Simple Hill Climbing.
    * Nhược điểm: Tương tự Simple Hill Climbing, vẫn có thể bị mắc kẹt.

#### c. Stochastic Hill Climbingng
* **Mô tả ngắn gọn:** Chọn một trạng thái lân cận tốt hơn một cách ngẫu nhiên, cho phép thoát khỏi một số đỉnh cục bộ.
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng thoát khỏi cực tiểu địa phương tốt hơn Simple/Steepest Ascent.
    * Nhược điểm: Vẫn không đảm bảo hoàn chỉnh hay tối ưu.

#### d. Simulated Annealing
* **Mô tả ngắn gọn:** Cho phép di chuyển đến trạng thái "xấu hơn" với một xác suất nhất định, xác suất này giảm dần theo thời gian. Giúp thoát khỏi các cực tiểu địa phương.
*   
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng tìm ra lời giải tốt hơn Hill Climbing, hoàn chỉnh nếu nhiệt độ giảm đủ chậm.
    * Nhược điểm: Cần tinh chỉnh các tham số, có thể chậm.

#### e. Genetic Algorithm
* **Mô tả ngắn gọn:** Mô phỏng quá trình tiến hóa tự nhiên, duy trì một tập các lời giải, áp dụng các toán tử lai ghép (crossover) và đột biến (mutation) để tạo ra các thế hệ mới.
*   ![alt text](GENETIC.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có khả năng tìm kiếm trong không gian lớn và phức tạp, thoát khỏi cực tiểu địa phương.
    * Nhược điểm: Cần nhiều tham số để tinh chỉnh, không đảm bảo tìm ra lời giải tối ưu tuyệt đối.

#### f. Beam Search
* **Mô tả ngắn gọn:** Biến thể của Best-First Search, chỉ giữ lại một số lượng giới hạn (beam width) các trạng thái tốt nhất ở mỗi bước để mở rộng, nhằm giảm bộ nhớ.
*   ![alt text](BEAM.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Giảm đáng kể bộ nhớ so với Best-First Search toàn cục.
    * Nhược điểm: Không hoàn chỉnh (có thể loại bỏ nhánh chứa lời giải tốt), không đảm bảo tối ưu.

---

### 2.4. Tìm kiếm trong môi trường phức tạp

#### a. And-Or Search
* **Mô tả ngắn gọn:** Dùng cho các bài toán có thể được phân rã thành các bài toán con hoặc có nhiều cách giải quyết khác nhau.
* **Thành phần chính của bài toán:** Các nút AND (cần giải quyết tất cả các bài toán con) và nút OR (chỉ cần giải quyết một trong các bài toán con).
* **Solution:** Một cây con lời giải, chứng minh rằng bài toán gốc có thể được giải quyết.
* **Nhận xét hiệu suất:**
    * And-Or Search không phải là cách tiếp cận trực tiếp phổ biến. Nó phù hợp hơn cho các bài toán lập kế hoạch hoặc suy luận logic.

---

### 2.5. Tìm kiếm trong môi trường có ràng buộc

* **Đặc điểm chung:** Tìm kiếm một trạng thái thỏa mãn một tập hợp các ràng buộc.
* **Thành phần chính của bài toán:** Các biến, miền giá trị cho mỗi biến, và các ràng buộc giữa các biến.
* **Solution:** Một phép gán giá trị cho tất cả các biến sao cho tất cả các ràng buộc đều được thỏa mãn.

#### a. Backtracking Search
* **Mô tả ngắn gọn:** Xây dựng lời giải từng phần, nếu một lựa chọn dẫn đến vi phạm ràng buộc hoặc không thể hoàn thành lời giải, thuật toán sẽ quay lui và thử lựa chọn khác. Đây là một dạng của DFS.
*   ![alt text](BACKTRACKING.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Tương tự DFS về bộ nhớ.
    * Nhược điểm: Có thể rất chậm nếu không có các heuristic hoặc kỹ thuật tối ưu hóa tốt.

#### b. Forward Checking
* **Mô tả ngắn gọn:** Khi gán một giá trị cho một biến, thuật toán kiểm tra trước các ràng buộc liên quan đến các biến chưa được gán và loại bỏ các giá trị không tương thích khỏi miền của chúng. Giúp phát hiện bế tắc sớm hơn.
*   ![alt text](FORWARD.gif)
* **Nhận xét hiệu suất:**
    * Ưu điểm: Thường hiệu quả hơn Backtracking đơn thuần bằng cách giảm không gian tìm kiếm.
    * Nhược điểm: Chi phí kiểm tra phía trước có thể đáng kể.

#### c. AC-3
* **Mô tả ngắn gọn:** Một thuật toán dùng trong quá trình tìm kiếm để loại bỏ các giá trị không nhất quán khỏi miền của các biến trong một CSP. Đảm bảo rằng với mỗi giá trị của một biến, tồn tại ít nhất một giá trị tương thích cho mỗi biến khác có ràng buộc với nó.
* **Nhận xét hiệu suất:**
    * AC-3 không phải là thuật toán tìm đường đi cho 8-puzzle. Trong ứng dụng của em, em sử dụng nó để tạo ra các trạng thái puzzle hợp lệ và có thể giải được. Điều này đảm bảo rằng các thuật toán tìm kiếm khác có một bài toán có ý nghĩa để giải.

---

### 2.6. Học máy

#### a. Q-Learningg
* **Mô tả ngắn gọn:** Một thuật toán học tăng cường không cần mô hình (model-free). Tác tử học một hàm giá trị hành động (Q-value) cho mỗi cặp (trạng thái, hành động), cho biết "chất lượng" của việc thực hiện hành động đó tại trạng thái đó.
* **Thành phần chính của bài toán:** Tác tử (Agent), môi trường (Environment), trạng thái (State), hành động (Action), phần thưởng (Reward), hàm Q (Q-function).
* **Solution:** Một chính sách (policy) tối ưu, cho biết hành động tốt nhất cần thực hiện ở mỗi trạng thái để tối đa hóa tổng phần thưởng kỳ vọng.
* **Nhận xét hiệu suất:**
    * Ưu điểm: Có thể học để giải các bài toán phức tạp mà không cần biết trước mô hình của môi trường.
    * Nhược điểm: Cần nhiều lượt tương tác để học, việc thiết kế phần thưởng phù hợp là quan trọng, tốn nhiều thời gian và bộ nhớ để lưu trữ bảng Q_table cho các không gian trạng thái lớn.

---
### Một số so sánh chung về các nhóm thuật toán
* **Tìm kiếm không có thông tin:** Các thuật toán trong nhóm này thường đảm bảo tìm ra lời giải nếu tồn tại. Tuy nhiên, chúng có thể không hiệu quả với không gian trạng thái lớn, đặc biệt là DFS không tối ưu.
* **Tìm kiếm có thông tin:** Các thuật toán trong nhóm này thường nhanh hơn nhờ sử dụng thông tin từ hàm heuristic
*   ![alt text](DFS.gif)
*   ![alt text](A_START.gif)

### Một vài nhận xét chung về hiệu suất các nhóm thuật toán

* **Tìm kiếm không có thông tin:** Đảm bảo tính hoàn chỉnh và tối ưu (BFS, IDDFS, UCS) nhưng thường chậm và tốn bộ nhớ cho các bài toán phức tạp.
* **Tìm kiếm có thông tin:** Hiệu quả hơn nhiều vì có hàm đánh giá tốt (A*, IDA*).Greedy nhanh nhưng không đảm bảo tối ưu.
* **Tìm kiếm cục bộ:** Nhanh và ít tốn bộ nhớ, nhưng dễ bị mắc kẹt ở cực tiểu địa phương và không đảm bảo tìm ra lời giải (trừ Simulated Annealing và Genetic Algorithm có cơ chế thoát).
* **Tìm kiếm với ràng buộc:** Backtracking và Forward Checking là các kỹ thuật tổng quát cho CSPs, có thể áp dụng nhưng cần điều chỉnh cho bài toán tìm đường đi.
* **Học máy (Q-Learning):** Tiếp cận bằng cách học từ kinh nghiệm, có thể mạnh mẽ nhưng đòi hỏi quá trình huấn luyện, học tập dài.

## 3. KẾT LUẬN
* Đã triển khai thành công những thuật toán tìm kiếm khác nhau cho bài toán 8-puzzle.
* Xây dựng được giao diện người dùng cho phép người dùng tương tác và quan sát quá trình giải.
 * Phân tích và so sánh cho thấy thuật toán một số thuật toán có vẻ hiệu quả hơn các thuật toán còn lại trong việc giải 8-puzzle.
 * Hiểu xâu hơn về những thuật toán đã được cô giảng dạy.
 * Học được cách làm việc với AI (có sử dụng một số AI để hỗ trợ, tham khảo để giải quyết bài toán (Gemini, ChatGPT).
 * Rút ra những bài học từ những lần vấp ngã (thuật toán chạy không như ý muốn).

## 4. HƯỚNG DẪN THỰC THI

Để chạy chương trình và trải nghiệm trò chơi:

1.  **Cách sử dụng giao diện:**
    * Vào File "UI.py" để khởi chạy.
    * Các nút bấm chính: "NGẪU NHIÊN", "NHẬP TAY", "GIẢI", "XEM KẾT QUẢ", "LÙI", "RESET", "TIẾN".
    * chọn thuật toán từ danh sách mà bạn muốn.
    * Nhấn nút "CHẠY" để khởi chạy thuật toán.
    * sau khi thuật toán đang chạy, các thông số như (số bước, thời gian tìm) sẽ hiển thị.
    * Nhấn nút "RESET" để có thể thiết lặp lại trạng thái ban đầu và chọn thuật toán khác để chạy.
    * Nhập puzzle bằng tay cho phép bạn đưa trạng thái ban đầu (nút "NHẬP TAY").

## 5. SINH VIÊN THỰC HIỆN

* **Họ và tên:** Sử Thanh Lộc
* **Mã số sinh viên:** 23110371
* **Link GitHub:** https://github.com/SuThanhLoc/BaiTapCaNhan_AI