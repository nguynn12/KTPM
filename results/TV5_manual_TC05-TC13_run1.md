# Kết quả kiểm thử thủ công TC05-TC13 (mục 5.2 báo cáo giữa kỳ)

- Người thực hiện: TV5 - Trần Quốc Khánh (2312646)
- Ngày chạy: 2026-10-18 14:06:07
- Môi trường: http://localhost:8000 - Paperless-ngx v3.1.3 (Docker, ghcr.io/paperless-ngx/paperless-ngx:3.1.3)
- Mã lượt chạy: 1018140604
- Dữ liệu seed: scripts/seed_data.py (4 tag, 3 correspondent, 3 document type, 2 tài liệu)
- Điều kiện trước: 4 tag trong hệ thống
- Sau khi chạy: 4 tag trong hệ thống

| ID | Loại | Tiêu đề | Dữ liệu | Kết quả mong đợi | Thực tế | Pass/Fail |
|---|---|---|---|---|---|---|
| TC05 | Biên | Tên đúng giới hạn độ dài tối đa | `name` = 128 ký tự (`TC05_<mã lượt>` + đệm `A`) | 201 | 201 Created | **PASS** |
| TC06 | Biên | Tên vượt giới hạn 1 ký tự | `name` = 129 ký tự (`TC06_<mã lượt>` + đệm `B`) | 400 | 400 Bad Request | **PASS** |
| TC07 | Positive | Tên tiếng Việt có dấu, emoji | `name` = `"Hóa đơn tháng 10 🧾 – Đà Lạt <mã lượt>"` | 201, không 500 | 201 Created | **PASS** |
| TC08 | Negative | Ký tự đặc biệt `<script>`, dấu nháy đơn | `name` = `"<script>alert('XSS')</script>_<mã lượt>"` | không 500 | 201 Created | **PASS** |
| TC09 | Negative | ID không tồn tại | `GET /api/tags/999999/` | 404 | 404 Not Found | **PASS** |
| TC10 | Negative | Xóa hai lần cùng ID | `DELETE /api/tags/{id}/` hai lần | lần 2: 404 | lần 1: 204 No Content; lần 2: 404 Not Found | **PASS** |
| TC12 | Bảo mật | Token sai | đổi 1 ký tự token (và thử thêm token rác) | 401 | 401 Unauthorized | **PASS** |
| TC13 | Biên | Tham số phân trang bất thường | `page_size` = 0, -1, rất lớn (thêm `page=0`) | không 500 | page_size=0→200; page_size=-1→200; page_size=100000→200; page_size=999999999→200; page_size=abc→200; page=0→404 | **PASS** |

## Chi tiết từng ca

### TC05 - Tên đúng giới hạn độ dài tối đa
- Dữ liệu: `name` = 128 ký tự (`TC05_<mã lượt>` + đệm `A`)
- Mong đợi: 201
- Thực tế: 201 Created
- Đánh giá: PASS
- Ghi chú: Tên đúng 128 ký tự được tạo thành công.

### TC06 - Tên vượt giới hạn 1 ký tự
- Dữ liệu: `name` = 129 ký tự (`TC06_<mã lượt>` + đệm `B`)
- Mong đợi: 400
- Thực tế: 400 Bad Request
- Đánh giá: PASS
- Ghi chú: Thông báo lỗi đúng như mong đợi (max 128).

### TC07 - Tên tiếng Việt có dấu, emoji
- Dữ liệu: `name` = `"Hóa đơn tháng 10 🧾 – Đà Lạt <mã lượt>"`
- Mong đợi: 201, không 500
- Thực tế: 201 Created
- Đánh giá: PASS
- Ghi chú: Tạo thành công, `slug` = 'hoa-on-thang-10-a-lat-1018140604'.

### TC08 - Ký tự đặc biệt `<script>`, dấu nháy đơn
- Dữ liệu: `name` = `"<script>alert('XSS')</script>_<mã lượt>"`
- Mong đợi: không 500
- Thực tế: 201 Created
- Đánh giá: PASS
- Ghi chú: Chuỗi được lưu nguyên văn (JSON escape), không có 5xx.

### TC09 - ID không tồn tại
- Dữ liệu: `GET /api/tags/999999/`
- Mong đợi: 404
- Thực tế: 404 Not Found
- Đánh giá: PASS

### TC10 - Xóa hai lần cùng ID
- Dữ liệu: `DELETE /api/tags/{id}/` hai lần
- Mong đợi: lần 2: 404
- Thực tế: lần 1: 204 No Content; lần 2: 404 Not Found
- Đánh giá: PASS
- Ghi chú: id dùng để thử: 41 (đã bị xóa ở lần 1)

### TC12 - Token sai
- Dữ liệu: đổi 1 ký tự token (và thử thêm token rác)
- Mong đợi: 401
- Thực tế: 401 Unauthorized
- Đánh giá: PASS
- Ghi chú: token rác cũng trả 401 Unauthorized

### TC13 - Tham số phân trang bất thường
- Dữ liệu: `page_size` = 0, -1, rất lớn (thêm `page=0`)
- Mong đợi: không 500
- Thực tế: page_size=0→200; page_size=-1→200; page_size=100000→200; page_size=999999999→200; page_size=abc→200; page=0→404
- Đánh giá: PASS
- Ghi chú: page_size bất thường bị bỏ qua, dùng kích thước trang mặc định; riêng page=0 bị từ chối 404 "Invalid page."

