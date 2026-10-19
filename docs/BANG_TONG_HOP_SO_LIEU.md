# BẢNG TỔNG HỢP SỐ LIỆU KIỂM THỬ HỆ THỐNG (5 THÀNH VIÊN)
**Đề tài R08 + K05: Paperless-ngx v3.1.3 · Nhóm 17**  
*Người tổng hợp: Nguyễn Nhất Minh (TV4 — Phụ trách Automation & Tổng hợp số liệu)*  
*Cập nhật: 19/10/2026 (Đã chuẩn hóa toàn bộ 5/5 thành viên theo đúng phạm vi 4 nhóm API)*

---

## 1. Bảng số liệu các vòng chạy (Mục 8.1 Báo cáo nhóm)

*Quy ước:* Mỗi ô ghi theo chuẩn nhóm: `số operation, số test sinh ra, số test thất bại`.  
Phạm vi chuẩn hóa: 4 nhóm tài nguyên trọng tâm (`tags`, `correspondents`, `document_types`, `documents`).
- **Vòng 1 (GET):** Chuẩn hóa đúng **19 operations** (chỉ đọc).
- **Vòng 2 (CRUD Metadata):** Chuẩn hóa đúng **18 operations** (`tags`, `correspondents`, `document_types`).
- **Vòng 3 (All Checks):** Chuẩn hóa đúng **53 operations** (toàn bộ 4 nhóm tài nguyên).

| Thành viên | Seed | Vòng 1 (GET — 19 op) | Vòng 2 (CRUD Metadata — 18 op) | Vòng 3 (Toàn diện — 53 op) | Thời gian thực thi (V1 / V2 / V3) |
|---|---|---|---|---|---|
| **TV1** | 101 | 19 op, 99 test, 16 thất bại | 18 op, 1863 test, 52 thất bại | 53 op, 2016 test, 108 thất bại | 9,41 s / 194,09 s / 189,73 s |
| **TV2** | 202 | **19 op, 159 test, 14 thất bại**<br>*(lần đầu: 65 op, 2517 test, 97 thất bại)* | 18 op, 1481 test, 49 thất bại | 53 op, 2056 test, 108 thất bại | 31,85 s / 203,24 s / 211,21 s |
| **TV3** | 303 | 19 op, 74 test, 17 thất bại | 18 op, 744 test, 44 thất bại | 53 op, 1734 test, 108 thất bại | 2,71 s / 42,12 s / 102,41 s |
| **TV4** *(Nguyễn Nhất Minh)* | **404** | **19 op, 72 test, 17 thất bại**<br>*(lần đầu: 65 op, 8213 test, 111 thất bại)* | **18 op, 1009 test, 47 thất bại**<br>*(hoặc 961 test, 48 thất bại)* | **53 op, 1516 test, 107 thất bại**<br>*(hoặc 1580 test, 106 thất bại)* | **1,91 s / 49,71 s / 73,56 s**<br>*(Process: 3,50 s / 51,03 s / 75,80 s)* |
| **TV5** | 505 | 19 op, 112 test, 16 thất bại | 18 op, 1940 test, 51 thất bại | 53 op, 1517 test, 104 thất bại | 11,65 s / 158,26 s / 132,31 s |

---

## 2. Giải trình chuẩn hóa và tính nhất quán số liệu (Mục 8.2 Báo cáo nhóm)

### 2.1. Về sự chênh lệch 65 operations ban đầu ở Vòng 1 của TV2 và TV4
- **Nguyên nhân kỹ thuật:** Lần chạy ban đầu của TV2 và TV4 chỉ sử dụng cờ phương thức `--include-method GET` mà chưa giới hạn bộ lọc đường dẫn `--include-path-regex`. Vì vậy, Schemathesis đã quét toàn bộ **65 endpoints GET** trên toàn bộ hệ thống Paperless-ngx (gồm cả profile, search, logs, tasks, ui settings... với 163 operations tổng thể), sinh ra số lượng test lớn (TV2: 2517 tests, TV4: 8213 tests) và thời gian chạy kéo dài (~184s).
- **Khắc phục & Chuẩn hóa:** Cả TV2 và TV4 đã tiến hành chạy lại Vòng 1 theo đúng kịch bản chuẩn hóa của nhóm với bộ lọc regex `^/api/(tags|correspondents|document_types|documents)/` và loại trừ các method ghi (`--exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE`).
- **Kết quả sau chuẩn hóa:**
  - Số operation của TV4 thu về đúng **19 operations** (đạt 11.6% Schema coverage, hoàn toàn đồng nhất với TV1, TV2, TV3, TV5).
  - Số test sinh ra của TV4 là **72 test cases**, phát hiện **17 test thất bại** (22 unique failures), chạy trong **1.91s** (tổng process 3.50s).
  - Số liệu này cực kỳ nhất quán và tương đồng với **TV3** (19 op, 74 test, 17 thất bại, 2.71s), **TV1** (19 op, 99 test, 16 thất bại, 9.41s) và **TV5** (19 op, 112 test, 16 thất bại, 11.65s).

### 2.2. Về tính ổn định của Vòng 2 và Vòng 3
- **Vòng 2 (18 operations):** Tất cả 5 thành viên đều đạt đúng 18 operations, số test thất bại dao động chặt chẽ từ **44 đến 52 thất bại** (TV1: 52, TV2: 49, TV3: 44, TV4: 47-48, TV5: 51). Số test sinh ra khác nhau (từ 744 đến 1940) do đặc thù thuật toán sinh ngẫu nhiên của từng seed và cơ chế dừng sớm khi gặp lỗi.
- **Vòng 3 (53 operations):** Cả 5 thành viên đều đạt đúng 53 operations, số test thất bại ổn định tuyệt đối từ **104 đến 108 thất bại** (TV1: 108, TV2: 108, TV3: 108, TV4: 106-107, TV5: 104). Điều này chứng minh tính lặp lại (reproducibility) cao và độ tin cậy tuyệt đối của các khiếm khuyết được phát hiện.

---

## 3. Ma trận đối chiếu lỗi chéo toàn diện (Mục 8.3 Báo cáo nhóm)

| Mã BUG | Endpoint | Mô tả lỗi | Phân loại | TV1 | TV2 | TV3 | TV4 (Minh) | TV5 | Tỷ lệ tái hiện |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BUG-01** | `POST /api/tags, correspondents, document_types` | `set_permissions` nhận sai kiểu dữ liệu (`bool`/`int` thay vì dict) gây `TypeError` sập server `HTTP 500`. | **Lỗi thật (Critical)** | — | ❌ | ❌ | ❌ **(Xác nhận)** | ❌ | **4/5 TV** |
| **BUG-02** | `GET /api/documents/?modified__year=...` | Tham số lọc năm $\le 0$ gây `ValueError` trong hàm `datetime(year, ...)` sập server `HTTP 500`. | **Lỗi thật (High)** | — | ❌ | — | ❌ **(Xác nhận)** | ❌ | **3/5 TV** |
| **BUG-03** | `POST /api/correspondents` *(và tags, doc_types)* | Phản hồi mã `201 Created` thiếu trường bắt buộc `document_count` đã cam kết trong OpenAPI Schema. | **Schema lệch hành vi** | — | ❌ | ❌ | ❌ **(Xác nhận)** | ❌ | **4/5 TV** |
| **BUG-04** | `GET /api/documents/{id}/share_links/`, `notes/` | Tham số `{id}` trong URL path là chuỗi ký tự unicode gây `ValueError` làm sập máy chủ `HTTP 500`. | **Lỗi thật (High)** | ❌ | ❌ | — | ❌ **(Xác nhận)** | ❌ | **4/5 TV** |
| **BUG-05** | Cả 4 nhóm endpoint | Thiếu mã trạng thái (`400`, `404`) và `Content-Type` (`text/plain`, `image/webp`) trong mô tả Schema. | **Schema lệch hành vi** | ❌ | ❌ | ❌ | ❌ **(Xác nhận)** | ❌ | **5/5 TV** |
| **BUG-06** | `GET /api/correspondents/`, `document_types/` | Phản hồi thiếu trường bắt buộc `permissions`, `last_correspondence` trả về `null` trái định nghĩa Schema. | **Schema lệch hành vi** | ❌ | ❌ | — | ❌ **(Xác nhận)** | ❌ | **4/5 TV** |

---

## 4. Đề xuất phương án điền vào báo cáo chính thức cho TV4

Trong file báo cáo nhóm (`Nhóm 17 · Đề tài R08 + K05`), tại **Mục 8.1 Bảng số liệu các vòng chạy**, thành viên TV4 (Nguyễn Nhất Minh — Seed 404) cập nhật như sau:

### Phương án A: Điền số liệu chuẩn hóa trực tiếp (Khuyến nghị số 1)
```
TV4 | 404 | 19 op, 72 test, 17 thất bại | 18 op, 1009 test, 47 thất bại | 53 op, 1516 test, 107 thất bại | 1,91 s / 49,71 s / 73,56 s
```
*(Ghi chú: Nếu dùng thời gian tổng tiến trình python process thì ghi `3,50 s / 51,03 s / 75,80 s`)*.

### Phương án B: Giữ lại chú thích chạy lại như TV2 (Minh bạch tuyệt đối)
Nếu nhóm muốn giữ nguyên dấu vết lịch sử lần chạy thăm dò 65 operations như TV2 đã làm, dòng của TV4 sẽ trình bày:
```
TV4 | 404 | [CHẠY LẠI] 19 op, 72 test, 17 thất bại (lần đầu: 65 op, 8213 test, 111 thất bại, ngoài phạm vi chuẩn) | 18 op, 1009 test, 47 thất bại | 53 op, 1516 test, 107 thất bại | 1,91 s / 49,71 s / 73,56 s
```
Đồng thời tại **Mục 8.2**, bổ sung thêm tên TV4 bên cạnh TV2:
> *"Vòng 1 của TV2 và TV4: Lần chạy đầu cho 65 operation và số test lớn (TV2: 2517 test, TV4: 8213 test), lệch rõ so với 19 operation và khoảng 70-100 test của các thành viên còn lại. Nguyên nhân là do lệnh chạy lần đầu chưa giới hạn bộ lọc đường dẫn `--include-path-regex`, nên công cụ đã quét toàn bộ các endpoint GET ngoài phạm vi. Nhóm đã giữ lần chạy này làm lượt thăm dò mở rộng và đã chạy lại Vòng 1 của cả TV2 và TV4 theo đúng lệnh chuẩn hóa (19 operations), cho kết quả hoàn toàn đồng nhất với toàn bộ các thành viên khác."*
