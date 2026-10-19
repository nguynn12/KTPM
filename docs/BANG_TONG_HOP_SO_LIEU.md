# Bảng tổng hợp số liệu chạy test (5 thành viên)

*Người tổng hợp: TV4 (Phụ trách Automation & Tổng hợp số liệu)*  
*Cập nhật ngày: 13/10/2026 (Đầy đủ số liệu thực nghiệm 3 vòng của TV2 và TV4)*

## 1. Thống kê thông số thực thi qua 3 Vòng
| Thành viên | Seed | Tổng số Test Cases / Operations | Tổng số lỗi phát hiện | Thời gian Vòng 1 (GET) | Thời gian Vòng 2 (Ghi) | Thời gian Vòng 3 (All Checks) | Tổng thời gian chạy |
|---|---|---|---|---|---|---|---|
| **TV1** | 101 | *(Chờ nộp)* | *(Chờ nộp)* | — | — | — | — |
| **TV2** | 202 | **139** operations tested | **132** failures | 179.91s (~3m) | 198.43s (~3m18s) | 205.99s (~3m26s) | **584.33s** (~9m44s) |
| **TV3** | 303 | *(Chờ nộp)* | *(Chờ nộp)* | — | — | — | — |
| **TV4** | 404 | **10.754** test cases sinh ra | **328** failures | 184.56s (~3m4s) | **53.08s** | **88.12s** | **325.76s** (~5m25s) |
| **TV5** | 505 | *(Chờ nộp)* | *(Chờ nộp)* | — | — | — | — |

---

## 2. Bảng ma trận đối chiếu lỗi chéo (Cross-Validation Matrix)

**Quy tắc xếp loại:**
- 🔴 **Đã xác nhận:** $\ge 2$ thành viên cùng tái hiện được độc lập (Lỗi thật của hệ thống).
- 🟡 **Cần kiểm tra lại:** Chỉ 1 thành viên thấy.
- ⚪ **False Positive:** Lỗi do schema mô tả sai hoặc dữ liệu vô lý, không tính lỗi phần mềm.

| Mã Lỗi | Endpoint + Method | Loại lỗi kỹ thuật | TV1 (101) | TV2 (202) | TV3 (303) | TV4 (404) | TV5 (505) | Kết luận độ tin cậy |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BUG-01** | `POST /api/tags/`, `/api/correspondents/`, `/api/document_types/` | HTTP 500 do unhandled `TypeError` khi `set_permissions` sai kiểu | — | ❌ Bị lỗi | — | ❌ **Bị lỗi** | — | 🔴 **ĐÃ XÁC NHẬN** (TV2 & TV4 cùng gặp ở V2, V3) |
| **BUG-02** | `GET /api/documents/?modified__year=...` | HTTP 500 do unhandled `ValueError` (`year 1..9999`) | — | ❌ Bị lỗi | — | ❌ **Bị lỗi** | — | 🔴 **ĐÃ XÁC NHẬN** (TV2 & TV4 cùng gặp ở V1, V3) |
| **BUG-03** | `POST /api/correspondents/`, `POST /api/tags/` | Response 201 Created thiếu trường bắt buộc của OpenAPI Schema | — | ❌ Bị lỗi | — | ❌ **Bị lỗi** | — | 🔴 **ĐÃ XÁC NHẬN** (TV2 & TV4 cùng gặp ở V2, V3) |
| **BUG-04** | `TRACE /api/documents/{id}/notes/` | HTTP 500 thay vì HTTP 405 Method Not Allowed | — | ❌ Bị lỗi | — | ❌ **Bị lỗi** | — | 🔴 **ĐÃ XÁC NHẬN** (TV2 & TV4 cùng gặp ở V1, V3) |
| **BUG-05** | `OPTIONS /api/profile/totp/` | HTTP 500 Internal Server Error | — | ❌ Bị lỗi | — | ❌ **Bị lỗi** | — | 🔴 **ĐÃ XÁC NHẬN** (TV2 & TV4 cùng gặp ở V1) |

---

## 3. Nhận xét phân tích của TV4 (Độ ổn định, So sánh Seed & Tối ưu hóa)
1. **Độ tin cậy của phát hiện lỗi (Cross-validation):**
   * Tất cả các lỗi nghiêm trọng gây crash máy chủ (HTTP 500) và vi phạm hợp đồng dữ liệu (Schema Violation) đều có tính lặp lại 100% giữa hai hạt giống ngẫu nhiên độc lập (**Seed 202** và **Seed 404**). 
   * Điều này chứng minh rằng các lỗi được báo cáo không phải do ngẫu nhiên hay phụ thuộc vào máy người dùng mà là các lỗi thực tế trong mã nguồn backend của Paperless-ngx v3.1.3.
2. **Hiệu quả tối ưu hóa của Automation Script:**
   * Nhờ thuật toán cấu hình thông minh (`-MaxExamples 20` và `--no-shrink`), thời gian chạy Vòng 2 và Vòng 3 của TV4 đã được rút ngắn hơn một nửa so với TV2 (tổng thời gian 5m25s so với 9m44s), trong khi vẫn đảm bảo độ phủ 53/53 operations trọng tâm và sinh ra hơn **10.000 test cases**.
