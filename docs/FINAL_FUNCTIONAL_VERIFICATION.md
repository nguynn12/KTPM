# Kết quả kiểm tra chức năng trên Paperless-ngx cục bộ

## Điều kiện thực thi

Docker Desktop ban đầu chưa chạy. Sau khi khởi động Docker Desktop, `docker compose start --wait --wait-timeout 45` khởi động ba container hiện có nhưng webserver chưa sẵn sàng trước hạn chờ. Redis và PostgreSQL đã sẵn sàng. Nhật ký webserver cho thấy migration không còn việc cần áp dụng và Granian đã khởi chạy. Lần thử lại sau đó xác thực và đọc được API. Kiểm tra này dùng stack cục bộ hiện có, không phải lượt cài sạch mới. Hồ sơ cài sạch của TV1 nằm trong results/TV1_cleanenv_verify.md.

### Ba ca chức năng

| Mã | Điều kiện, thao tác và dữ liệu | Mong đợi | Thực tế | Kết quả |
|---|---|---|---|---|
| TC-TAG-12 | Tài khoản cục bộ có quyền xem. GET /api/tags/. | HTTP 200 và results là danh sách. | HTTP 200, count=1, results là danh sách. | PASS |
| MC-03 | Chọn tài liệu đang hiển thị ở danh sách cục bộ. GET /api/documents/14/. | HTTP 200, định danh và tiêu đề trùng tài liệu đã chọn. | HTTP 200, ID 14, tiêu đề khớp dữ liệu ở danh sách. | PASS |
| MC-05 | Tạo nhãn tạm ID 140 và tải tài liệu mẫu ID 15 có nhãn đó. Tài liệu 14 làm đối chứng. GET danh sách tài liệu với tham số lọc theo nhãn được OpenAPI công bố. | HTTP 200, có tài liệu 15, không có tài liệu 14. | HTTP 200, trả đúng tài liệu 15, không có tài liệu 14, count=1, không có trang kế tiếp. | PASS |

Bản ghi quan sát đã lược thông tin xác thực, lưu riêng với kết quả lịch sử ngay trong hồ sơ này:

```text
Authentication: 200
TC-TAG-12 200 count 1 has_results_list True
Document list 200 count 4
MC-03 200 expected_id 14 returned_id 14 title_matches True
MC-05 200 filter tags__id__all tag 140 target 15 control 14 target_present True control_present False count 1 next_page False
Temporary document cleanup HTTP 204
Temporary tag cleanup HTTP 204
```

Ba ca được gọi trực tiếp từ terminal qua HTTP trên localhost. Khi đưa vào báo cáo, có thể ghi đã xác nhận qua API. Ảnh chụp trên Swagger UI vẫn do nhóm bổ sung nếu cần chứng minh giao diện thực thi.

### Phân vùng tương đương và giá trị biên của Tags

Đọc trực tiếp từ OpenAPI đang chạy: **3.0.3**, **163 operation**, giới hạn độ dài tên nhãn là **128**. Dùng tên ngẫu nhiên riêng cho từng ca chấp nhận dữ liệu hợp lệ. Chỉ xóa các nhãn tạm do lượt kiểm tra tạo.

| Ca đối chiếu | Dữ liệu mô tả | Mong đợi | HTTP thực tế | Kết quả |
|---|---|---:|---:|---|
| TC-TAG-03 | Thiếu trường tên | 400 | 400 | PASS |
| TC-TAG-04 | Tên rỗng | 400 | 400 | PASS |
| Biên dưới | Tên dài 127 ký tự | 201 | 201 | PASS |
| Đúng biên | Tên dài 128 ký tự | 201 | 201 | PASS |
| Vượt biên | Tên dài 129 ký tự | 400 | 400 | PASS |

```text
Schema 3.0.3 operations 163 name_max 128
Tags name missing expected 400 observed 400 PASS
Tags name empty expected 400 observed 400 PASS
Tags name 127 expected 201 observed 201 PASS
Temporary tag cleanup HTTP 204
Tags name 128 expected 201 observed 201 PASS
Temporary tag cleanup HTTP 204
Tags name 129 expected 400 observed 400 PASS
```

Các nhãn được API chấp nhận đã được dọn với HTTP 204. Ca tên trùng và xác thực trong hồ sơ lịch sử giữ nguồn lịch sử, chưa gắn nhãn là đã chạy lại.
