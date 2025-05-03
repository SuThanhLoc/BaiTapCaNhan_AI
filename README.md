# Giải Bài Toán 8-Puzzle Bằng Thuật Toán Tìm Kiếm

Dự án này cài đặt và so sánh một số thuật toán tìm kiếm phổ biến để giải quyết bài toán 8-puzzle cổ điển.

## Mục lục

* [Giới thiệu](#giới-thiệu)
* [Bài toán 8-Puzzle](#bài-toán-8-puzzle)
* [Các thuật toán được sử dụng](#các-thuật-toán-được-sử-dụng)
* [Heuristics (Nếu có)](#heuristics-nếu-có)
* [Cấu trúc thư mục](#cấu-trúc-thư-mục)
* [Yêu cầu cài đặt](#yêu-cầu-cài-đặt)
* [Cách chạy chương trình](#cách-chạy-chương-trình)
* [Định dạng Input/Output](#định-dạng-inputoutput)
* [Ví dụ](#ví-dụ)
* [Kết quả & Phân tích (Tùy chọn)](#kết-quả--phân-tích-tùy-chọn)
* [Tác giả](#tác-giả)

## Giới thiệu

Dự án này là bài tập nhằm mục đích tìm hiểu, cài đặt và đánh giá hiệu quả của các thuật toán tìm kiếm mù (Uninformed Search) và/hoặc tìm kiếm có thông tin (Informed Search) thông qua việc áp dụng chúng để giải bài toán 8-puzzle.

## Bài toán 8-Puzzle

Bài toán 8-puzzle bao gồm một bảng 3x3 với 8 ô vuông được đánh số từ 1 đến 8 và một ô trống. Mục tiêu là sắp xếp lại các ô từ một trạng thái ban đầu cho trước về trạng thái đích (thường là `1 2 3 / 4 5 6 / 7 8 0`) bằng cách di chuyển ô trống lên, xuống, trái, hoặc phải.

**Trạng thái đích mặc định:**

```  <-- Dòng mở đầu bằng ba dấu huyền
1 2 3
4 5 6
7 8 0
```  <-- Dòng kết thúc bằng ba dấu huyền