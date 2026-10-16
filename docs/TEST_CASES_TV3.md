# TEST CASES TV3 — Phần E: Thiết kế & Thực thi Kiểm thử Thủ công

**Tác giả:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed Schemathesis: 303  
**Ngày thực hiện:** 13/10/2026  
**Môi trường:** Paperless-ngx v3.1.3 trên Docker Windows local (`http://localhost:8000`)  
**Tài nguyên phụ trách:** `Correspondents` (`/api/correspondents/`) và `Document Types` (`/api/document_types/`)  
**Bổ sung:** 3 luồng kịch bản nghiệp vụ thực tế (Upload PDF, Gán Metadata, Tìm kiếm/Lọc)

---

## 1. Thiết kế và Kết quả Thực thi `/api/correspondents/`

| ID | Loại | Kỹ thuật | Bước / hành vi | Dữ liệu / tiền điều kiện riêng | Mong đợi | Thực tế (Chạy thực tế 13/10) | Verdict |
|---|---|---|---|---|---|---|---|
| TV3-COR-01 | Functional/Positive | EP hợp lệ | POST tên duy nhất hợp lệ | `{name: "TV3_Corr_Valid_<run>"}` | 201; id thật; GET đối chiếu tên | HTTP 201; ID tự sinh; 28 ms | **PASS** |
| TV3-COR-02 | Functional/Negative | EP không hợp lệ | POST thiếu name | `{}` | 400; không tạo bản ghi | HTTP 400 Bad Request; 17 ms | **PASS** |
| TV3-COR-03 | Functional/Negative | BVA dưới | POST tên rỗng | `{name: ""}` | 400 | HTTP 400 Bad Request; 18 ms | **PASS** |
| TV3-COR-04 | Functional/Negative | EP không hợp lệ | POST name=null | `{name: null}` | 400 | HTTP 400 Bad Request; 17 ms | **PASS** |
| TV3-COR-05 | Functional/Negative | Tính duy nhất | POST trùng tên bản ghi đã có | `{name: "TV2_Bank_202"}` | 400; không tạo thêm bản ghi | HTTP 400 (`name already exists`); 19 ms | **PASS** |
| TV3-COR-06 | Functional/Positive | BVA | POST tên dài L-1 (127 ký tự) | Chuỗi 127 ký tự 'C' | 201 nếu name khác | HTTP 201 Created; 27 ms | **PASS** |
| TV3-COR-07 | Functional/Positive | BVA | POST tên đúng L (128 ký tự) | Chuỗi 128 ký tự 'D' | 201; GET giữ nguyên tên | HTTP 201 Created; 27 ms | **PASS** |
| TV3-COR-08 | Functional/Negative | BVA | POST tên vượt biên L+1 (129 ký tự) | Chuỗi 129 ký tự 'E' | 400 Bad Request | HTTP 400 (`Ensure this field has no more than 128 characters`); 18 ms | **PASS** |
| TV3-COR-09 | Functional/Negative | EP vượt miền | POST tên dài 1000 | Chuỗi 1000 ký tự | 400 nếu L < 1000 | *Chưa chạy lượt này* | NOT RUN |
| TV3-COR-10 | Functional/Positive | EP Unicode | POST tên tiếng Việt/emoji | `TV3_Nguyễn_Khiêm_Thuận_🌿_<run>` | 201; GET trả đúng Unicode | HTTP 201 Created; lưu đúng chuỗi; 28 ms | **PASS** |
| TV3-COR-11 | Functional/Positive | Trạng thái | GET ID vừa tạo | ID lấy từ phản hồi thành công | 200; id và name khớp | HTTP 200 OK; ID khớp; 25 ms | **PASS** |
| TV3-COR-12 | Functional/Negative | Trạng thái | GET ID đã xóa thành công | DELETE thành công -> GET lại | 404 Not Found | *Chưa chạy lượt này* | NOT RUN |
| TV3-COR-13 | Functional/Positive | CRUD | PATCH name bản ghi riêng | Tên mới duy nhất; ID thật | 200; GET khớp tên mới | *Chưa chạy lượt này* | NOT RUN |
| TV3-COR-14 | Functional/Positive | CRUD | PUT dữ liệu đầy đủ | Đủ trường bắt buộc theo schema | 200; GET khớp dữ liệu | *Chưa chạy lượt này* | NOT RUN |
| TV3-COR-15 | Functional/Positive | CRUD | DELETE bản ghi riêng đang tồn tại | ID do chính lượt test tạo | 204 No Content | HTTP 204 No Content; đã xóa | **PASS** |
| TV3-COR-16 | Functional/Negative | Chuyển trạng thái | DELETE lần hai cùng ID | DELETE lại ID đã xóa | 404 Not Found | *Chưa chạy lượt này* | NOT RUN |
| TV3-COR-17 | Auth/Negative | EP không xác thực | GET danh sách không token | Không Authorization header | 401 Unauthorized | HTTP 401 Unauthorized; 5 ms | **PASS** |
| TV3-COR-18 | Auth/Negative | EP token sai | GET danh sách với token giả | Authorization: Token invalid-fake-token-tv3 | 401 Unauthorized | HTTP 401 Unauthorized; 16 ms | **PASS** |
| TV3-COR-19 | Functional/Positive | Phân trang | GET page=1&page_size=1 | Có ít nhất 2 bản ghi nhìn thấy | 200; results có <=1 phần tử | HTTP 200 OK; count hợp lệ; 29 ms | **PASS** |
| TV3-COR-20 | Robustness/Negative | Error guessing / regression | POST set_permissions.view=false | `{set_permissions: {view: false}}` | 400 theo contract validation; mọi 5xx là failure | **HTTP 500 Server Error (HTML)**; unhandled `TypeError`; 19 ms | **REPRO-BUG-01 (500)** |

---

## 2. Thiết kế và Kết quả Thực thi `/api/document_types/`

| ID | Loại | Kỹ thuật | Bước / hành vi | Dữ liệu / tiền điều kiện riêng | Mong đợi | Thực tế (Chạy thực tế 13/10) | Verdict |
|---|---|---|---|---|---|---|---|
| TV3-DT-01 | Functional/Positive | EP hợp lệ | POST tên duy nhất hợp lệ | `{name: "TV3_DocType_Valid_<run>"}` | 201; id thật; GET đối chiếu | HTTP 201 Created; ID tự sinh; 26 ms | **PASS** |
| TV3-DT-02 | Functional/Negative | EP không hợp lệ | POST thiếu name | `{}` | 400; không có bản ghi mới | HTTP 400 Bad Request; 16 ms | **PASS** |
| TV3-DT-03 | Functional/Negative | BVA dưới | POST tên rỗng | `{name: ""}` | 400 | HTTP 400 Bad Request; 16 ms | **PASS** |
| TV3-DT-04 | Functional/Negative | EP không hợp lệ | POST name=null | `{name: null}` | 400 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-05 | Functional/Negative | Tính duy nhất | POST trùng tên bản ghi đã có | `{name: "TV2_DocType_Invoice_202"}` | 400; không tạo thêm | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-06 | Functional/Positive | BVA | POST tên dài L-1 (127 ký tự) | Chuỗi 127 ký tự | 201 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-07 | Functional/Positive | BVA | POST tên dài L (128 ký tự) | Chuỗi 128 ký tự | 201 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-08 | Functional/Negative | BVA | POST tên dài L+1 (129 ký tự) | Chuỗi 129 ký tự 'F' | 400 Bad Request | HTTP 400 (`Ensure this field has no more than 128 characters`); 18 ms | **PASS** |
| TV3-DT-09 | Functional/Negative | EP vượt miền | POST tên dài 1000 | Chuỗi 1000 ký tự | 400 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-10 | Functional/Positive | EP Unicode | POST tên tiếng Việt/emoji | `TV3_Loại_Hợp_Đồng_📝_<run>` | 201 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-11 | Functional/Positive | Trạng thái | GET ID vừa tạo | ID lấy từ response thành công | 200; khớp ID/name | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-12 | Functional/Negative | Trạng thái | GET ID đã xóa thành công | Fixture DELETE -> GET lại | 404 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-13 | Functional/Positive | CRUD | PATCH name bản ghi riêng | Tên mới duy nhất | 200 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-14 | Functional/Positive | CRUD | PUT dữ liệu đầy đủ | Đủ trường bắt buộc | 200 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-15 | Functional/Positive | CRUD | DELETE bản ghi riêng đang tồn tại | ID do chính test tạo | 204 | HTTP 204 No Content | **PASS** |
| TV3-DT-16 | Functional/Negative | Chuyển trạng thái | DELETE lần hai cùng ID | Fixture đã DELETE -> DELETE lại | 404 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-17 | Auth/Negative | EP không xác thực | GET danh sách không token | Không Authorization | 401 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-18 | Auth/Negative | EP token sai | GET danh sách token giả | Authorization: Token fake | 401 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-19 | Functional/Positive | Phân trang | GET page=1&page_size=1 | Có ít nhất 2 bản ghi | 200 | *Chưa chạy lượt này* | NOT RUN |
| TV3-DT-20 | Robustness/Negative | Error guessing / regression | POST set_permissions.view=false | `{set_permissions: {view: false}}` | 400 theo validation; 5xx là failure | **HTTP 500 Server Error (HTML)**; unhandled `TypeError`; 19 ms | **REPRO-BUG-01 (500)** |

---

## 3. Ba Kịch bản Nghiệp vụ Bổ sung (Business Scenarios)

| ID | Bước thực hiện | Oracle | Bằng chứng thực tế lưu tại `docs/BUSINESS_FLOWS_TV3.md` | Kết quả |
|---|---|---|---|---|
| **TV3-FLOW-01** | Upload PDF `TV3_Sample_01_Report_303.pdf` -> chờ tác vụ Celery -> GET tài liệu kiểm tra content | Upload được nhận (200/202), task Celery hoàn tất SUCCESS, tài liệu sinh ra có content trích xuất đúng mẫu | HTTP 202, Task UUID `ea3629b6-2918-43fa-94d9-6366fee4a86c`, Document ID 4, GET HTTP 200, Content dài 306 ký tự chứa "BAO CAO KIEM THU PHAN MEM SCHEMATHESIS", tác giả Nguyễn Khiêm Thuận 2312764 | **PASS** |
| **TV3-FLOW-02** | Tạo Tag (ID 5), Correspondent (ID 4), DocumentType (ID 4) -> PATCH tài liệu ID 4 -> GET đối chiếu | Metadata được liên kết chính xác, các ID lưu khớp dữ liệu gửi lên | HTTP 201 cho 3 thực thể; PATCH Document 4 HTTP 200; GET Document 4 trả về đúng `tags: [5]`, `correspondent: 4`, `document_type: 4` | **PASS** |
| **TV3-FLOW-03** | Tìm kiếm từ khóa `query=Schemathesis` và Lọc `tags__id__all=5` | Tìm thấy đúng tài liệu mục tiêu trong danh sách trả về | GET `?query=Schemathesis` HTTP 200 (count=2, có Doc 4); GET `?tags__id__all=5` HTTP 200 (count=1, có Doc 4) | **PASS** |

---

## 4. Xác minh Tái hiện Lỗi Hồi quy (Regression Verification)

### BUG-01: HTTP 500 khi payload `set_permissions` chứa `"view": false`
- **Mục tiêu:** Kiểm tra xem lỗi unhandled `TypeError` do TV2 phát hiện trên Tag có xuất hiện trên tài nguyên `Correspondents` và `Document Types` hay không.
- **Thực thi lần 1:** Gửi POST tới `/api/correspondents/` với `{"set_permissions": {"view": false}}` -> Trả về `500 Internal Server Error` (19 ms).
- **Thực thi lần 2 (Độc lập):** Gửi lại request tương tự -> Trả về `500 Internal Server Error` (Xác nhận 100% tái hiện lỗi).
- **Thực thi trên DocumentType:** Gửi POST tới `/api/document_types/` -> Trả về `500 Internal Server Error` (19 ms).
- **Kết luận:** Lỗi do kiến trúc chung trong `set_permissions` của Django REST Framework serializer base class, ảnh hưởng toàn bộ các model có quản lý phân quyền người dùng. TV2 phát hiện đầu tiên, TV3 tái hiện độc lập trên 2 tài nguyên mới.

### BUG-03: Vi phạm Hợp đồng Schema khi POST trả về HTTP 201 nhưng thiếu trường required
- **Mục tiêu:** Kiểm tra phản hồi 201 của `POST /api/correspondents/` đối chiếu với OpenAPI schema tại `/api/schema/`.
- **Đặc tả Schema:** `/components/schemas/Correspondent` quy định các trường `required`: `['document_count', 'id', 'last_correspondence', 'name', 'permissions', 'slug', 'user_can_change']`.
- **Thực thi lần 1:** Gọi POST tạo mới Correspondent thành công (HTTP 201 Created). Response body thiếu 3 trường: `document_count`, `last_correspondence`, `permissions`.
- **Thực thi lần 2 (Độc lập):** Gọi POST tạo mới lần hai -> Tiếp tục thiếu 3 trường tương tự.
- **Kết luận:** Tái hiện thành công lỗi vi phạm hợp đồng API.
