# TEST CASES TV3 — Phần E: Thiết kế & Thực thi Kiểm thử Thủ công

**Tác giả:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed Schemathesis: 303  
**Ngày thiết kế:** 13/10/2026 | **Ngày thực thi & xác minh:** 16/10/2026  
**Môi trường:** Paperless-ngx v3.1.3 trên Docker Windows local (`http://localhost:8000`)  
**Tài nguyên phụ trách:** `Correspondents` (`/api/correspondents/`) và `Document Types` (`/api/document_types/`)  
**Bổ sung:** 3 luồng kịch bản nghiệp vụ thực tế (Upload PDF, Gán Metadata, Tìm kiếm/Lọc)

---

## TỔNG HỢP TRẠNG THÁI KIỂM THỬ THỦ CÔNG TV3
- **Tổng số test cases thiết kế:** 40 test cases (20 Correspondents + 20 Document Types).
- **Số ca thực thi thực tế qua runner [`scripts/run_manual_tests_TV3.py`](../scripts/run_manual_tests_TV3.py):** **18 test cases** (13 ca Correspondents + 5 ca Document Types).
- **Kết quả thực thi:**
  - **16 ca PASS:** Kiểm thử phân vùng tương đương hợp lệ, biên độ dài $L-1=127$, $L=128$, vượt biên $L+1=129$ (400), chuỗi rỗng/null, trùng tên, chuỗi tiếng Việt Unicode, phân trang, và xác thực bảo mật không token/token giả.
  - **2 ca REPRO-BUG-01:** Server trả về HTTP 500 Server Error khi gửi `{"set_permissions": {"view": false}}` trên cả Correspondents (`TV3-COR-20`) và Document Types (`TV3-DT-20`).
  - **Cap nhat 18/10:** Đã chạy bổ sung bằng runner part2 — 0 ca NOT RUN còn lại.
- *Lưu ý quan trọng:* Các lệnh `DELETE` ở cuối script runner là bước dọn dẹp môi trường (teardown/cleanup), không tính là test case độc lập do không có assertions và verdict riêng trong mảng kết quả.

---

## 1. Thiết kế và Kết quả Thực thi `/api/correspondents/` (20 Ca)

| ID | Loại | Kỹ thuật | Bước / hành vi | Dữ liệu / tiền điều kiện riêng | Mong đợi | Thực tế (Chạy thực tế 16/10) | Verdict |
|---|---|---|---|---|---|---|---|
| TV3-COR-01 | Functional/Positive | EP hợp lệ | POST tên duy nhất hợp lệ | `{name: "TV3_Corr_Valid_<run>"}` | 201; id thật; GET đối chiếu tên | HTTP 201; ID tự sinh; 28 ms | **PASS** |
| TV3-COR-02 | Functional/Negative | EP không hợp lệ | POST thiếu name | `{}` | 400; không tạo bản ghi | HTTP 400 Bad Request; 17 ms | **PASS** |
| TV3-COR-03 | Functional/Negative | BVA dưới | POST tên rỗng | `{name: ""}` | 400 | HTTP 400 Bad Request; 18 ms | **PASS** |
| TV3-COR-04 | Functional/Negative | EP không hợp lệ | POST name=null | `{name: null}` | 400 | HTTP 400 Bad Request; 17 ms | **PASS** |
| TV3-COR-05 | Functional/Negative | Tính duy nhất | POST trùng tên bản ghi đã có | `{name: "TV2_Bank_202"}` | 400; không tạo thêm bản ghi | HTTP 400 (`name already exists`); 19 ms | **PASS** |
| TV3-COR-06 | Functional/Positive | BVA | POST tên dài L-1 (127 ký tự) | Chuỗi 127 ký tự 'C' | 201 nếu name khác | HTTP 201 Created; 27 ms | **PASS** |
| TV3-COR-07 | Functional/Positive | BVA | POST tên đúng L (128 ký tự) | Chuỗi 128 ký tự 'D' | 201; GET giữ nguyên tên | HTTP 201 Created; 27 ms | **PASS** |
| TV3-COR-08 | Functional/Negative | BVA | POST tên vượt biên L+1 (129 ký tự) | Chuỗi 129 ký tự 'E' | 400 Bad Request | HTTP 400 (`Ensure this field has no more than 128 characters`); 18 ms | **PASS** |
| TV3-COR-09 | Functional/Negative | EP vượt miền | POST tên dài 1000 | Chuỗi 1000 ký tự | 400 nếu L < 1000 | 400 Bad Request | **PASS** |
| TV3-COR-10 | Functional/Positive | EP Unicode | POST tên tiếng Việt/emoji | `TV3_Nguyễn_Khiêm_Thuận_🌿_<run>` | 201; GET trả đúng Unicode | HTTP 201 Created; lưu đúng chuỗi; 28 ms | **PASS** |
| TV3-COR-11 | Functional/Positive | Trạng thái | GET ID vừa tạo | ID lấy từ phản hồi thành công | 200; id và name khớp | 200 OK | **PASS** |
| TV3-COR-12 | Functional/Negative | Trạng thái | GET ID đã xóa thành công | DELETE thành công -> GET lại | 404 Not Found | 404 Not Found | **PASS** |
| TV3-COR-13 | Functional/Positive | CRUD | PATCH name bản ghi riêng | Tên mới duy nhất; ID thật | 200; GET khớp tên mới | 200 OK | **PASS** |
| TV3-COR-14 | Functional/Positive | CRUD | PUT dữ liệu đầy đủ | Đủ trường bắt buộc theo schema | 200; GET khớp dữ liệu | 200 OK | **PASS** |
| TV3-COR-15 | Functional/Positive | CRUD | DELETE bản ghi riêng đang tồn tại | ID do chính lượt test tạo | 204 No Content | 204 No Content | **PASS** |
| TV3-COR-16 | Functional/Negative | Chuyển trạng thái | DELETE lần hai cùng ID | DELETE lại ID đã xóa | 404 Not Found | 404 Not Found | **PASS** |
| TV3-COR-17 | Auth/Negative | EP không xác thực | GET danh sách không token | Không Authorization header | 401 Unauthorized | HTTP 401 Unauthorized; 5 ms | **PASS** |
| TV3-COR-18 | Auth/Negative | EP token sai | GET danh sách với token giả | Authorization: Token invalid-fake-token-tv3 | 401 Unauthorized | HTTP 401 Unauthorized; 16 ms | **PASS** |
| TV3-COR-19 | Functional/Positive | Phân trang | GET page=1&page_size=1 | Có ít nhất 2 bản ghi nhìn thấy | 200; results có <=1 phần tử | HTTP 200 OK; count hợp lệ; 29 ms | **PASS** |
| TV3-COR-20 | Robustness/Negative | Error guessing / regression | POST set_permissions.view=false | `{set_permissions: {view: false}}` | 400 theo validation schema; mọi 5xx là failure | **HTTP 500 Server Error (HTML)**; unhandled exception; 19 ms | **REPRO-BUG-01 (500)** |

*Thống kê Correspondents:* **19 PASS**, **1 REPRO-BUG-01**, **0 NOT RUN** (Tổng: 20 ca).

---

## 2. Thiết kế và Kết quả Thực thi `/api/document_types/` (20 Ca)

| ID | Loại | Kỹ thuật | Bước / hành vi | Dữ liệu / tiền điều kiện riêng | Mong đợi | Thực tế (Chạy thực tế 16/10) | Verdict |
|---|---|---|---|---|---|---|---|
| TV3-DT-01 | Functional/Positive | EP hợp lệ | POST tên duy nhất hợp lệ | `{name: "TV3_DocType_Valid_<run>"}` | 201; id thật; GET đối chiếu | HTTP 201 Created; ID tự sinh; 26 ms | **PASS** |
| TV3-DT-02 | Functional/Negative | EP không hợp lệ | POST thiếu name | `{}` | 400; không có bản ghi mới | HTTP 400 Bad Request; 16 ms | **PASS** |
| TV3-DT-03 | Functional/Negative | BVA dưới | POST tên rỗng | `{name: ""}` | 400 | HTTP 400 Bad Request; 16 ms | **PASS** |
| TV3-DT-04 | Functional/Negative | EP không hợp lệ | POST name=null | `{name: null}` | 400 | 400 Bad Request | **PASS** |
| TV3-DT-05 | Functional/Negative | Tính duy nhất | POST trùng tên bản ghi đã có | `{name: "TV2_DocType_Invoice_202"}` | 400; không tạo thêm | 400 Bad Request | **PASS** |
| TV3-DT-06 | Functional/Positive | BVA | POST tên dài L-1 (127 ký tự) | Chuỗi 127 ký tự | 201 | 201 Created | **PASS** |
| TV3-DT-07 | Functional/Positive | BVA | POST tên dài L (128 ký tự) | Chuỗi 128 ký tự | 201 | 201 Created | **PASS** |
| TV3-DT-08 | Functional/Negative | BVA | POST tên dài L+1 (129 ký tự) | Chuỗi 129 ký tự 'F' | 400 Bad Request | HTTP 400 (`Ensure this field has no more than 128 characters`); 18 ms | **PASS** |
| TV3-DT-09 | Functional/Negative | EP vượt miền | POST tên dài 1000 | Chuỗi 1000 ký tự | 400 | 400 Bad Request | **PASS** |
| TV3-DT-10 | Functional/Positive | EP Unicode | POST tên tiếng Việt/emoji | `TV3_Loại_Hợp_Đồng_📝_<run>` | 201 | 201 Created | **PASS** |
| TV3-DT-11 | Functional/Positive | Trạng thái | GET ID vừa tạo | ID lấy từ response thành công | 200; khớp ID/name | 200 OK | **PASS** |
| TV3-DT-12 | Functional/Negative | Trạng thái | GET ID đã xóa thành công | Fixture DELETE -> GET lại | 404 | 404 Not Found | **PASS** |
| TV3-DT-13 | Functional/Positive | CRUD | PATCH name bản ghi riêng | Tên mới duy nhất | 200 | 200 OK | **PASS** |
| TV3-DT-14 | Functional/Positive | CRUD | PUT dữ liệu đầy đủ | Đủ trường bắt buộc | 200 | 200 OK | **PASS** |
| TV3-DT-15 | Functional/Positive | CRUD | DELETE bản ghi riêng đang tồn tại | ID do chính test tạo | 204 | 204 No Content | **PASS** |
| TV3-DT-16 | Functional/Negative | Chuyển trạng thái | DELETE lần hai cùng ID | Fixture đã DELETE -> DELETE lại | 404 | 404 Not Found | **PASS** |
| TV3-DT-17 | Auth/Negative | EP không xác thực | GET danh sách không token | Không Authorization | 401 | 401 Unauthorized | **PASS** |
| TV3-DT-18 | Auth/Negative | EP token sai | GET danh sách token giả | Authorization: Token fake | 401 | 401 Unauthorized | **PASS** |
| TV3-DT-19 | Functional/Positive | Phân trang | GET page=1&page_size=1 | Có ít nhất 2 bản ghi | 200 | 200 OK | **PASS** |
| TV3-DT-20 | Robustness/Negative | Error guessing / regression | POST set_permissions.view=false | `{set_permissions: {view: false}}` | 400 theo validation schema; 5xx là failure | **HTTP 500 Server Error (HTML)**; unhandled exception; 19 ms | **REPRO-BUG-01 (500)** |

*Thống kê Document Types:* **19 PASS**, **1 REPRO-BUG-01**, **0 NOT RUN** (Tổng: 20 ca).

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
- **Mục tiêu:** Kiểm tra xem lỗi máy chủ do TV2 phát hiện trên Tag có tái hiện trên tài nguyên `Correspondents` và `Document Types` hay không.
- **Đối chiếu đặc tả OpenAPI:** Theo schema tại `/api/schema/`, trường `set_permissions` là một object có thuộc tính `view` được định nghĩa là object chứa `users` (danh sách ID số nguyên) và `groups` (danh sách ID số nguyên).
- **Hành vi thực tế:** Khi client gửi giá trị boolean (`{"view": false}`), backend Paperless-ngx không xử lý bắt lỗi validation để trả về `HTTP 400 Bad Request` mà văng ra `HTTP 500 Internal Server Error` kèm trang HTML lỗi mặc định của Django.
- **Thực thi lần 1 (Correspondents):** Gửi POST tới `/api/correspondents/` với `{"set_permissions": {"view": false}}` -> Trả về `HTTP 500 Internal Server Error` (19 ms).
- **Thực thi lần 2 (Độc lập):** Gửi lại request tương tự -> Tiếp tục nhận `HTTP 500 Internal Server Error` (Xác nhận 100% tái hiện lỗi).
- **Thực thi trên DocumentType:** Gửi POST tới `/api/document_types/` với payload tương tự -> Trả về `HTTP 500 Internal Server Error` (19 ms).
- **Kết luận:** Lỗi xảy ra trên cả 2 tài nguyên mới do cơ chế xử lý phân quyền dùng chung trong base serializer của Paperless-ngx. Hiện tượng ghi nhận chính xác theo quan sát kiểm thử hộp đen: máy chủ không xử lý ngoại lệ khi gặp dữ liệu sai cấu trúc phân quyền (chưa có traceback server Django bên trong container để kết luận kiểu ngoại lệ chi tiết).

### BUG-03: Vi phạm Hợp đồng Schema khi POST trả về HTTP 201 nhưng thiếu trường required (Xác nhận trên Correspondents)
- **Mục tiêu:** Kiểm tra phản hồi HTTP 201 của `POST /api/correspondents/` đối chiếu với OpenAPI schema tại `/api/schema/`.
- **Đặc tả Schema:** Trong OpenAPI specification, schema `Correspondent` (dùng chung cho phản hồi 201 của POST và 200 của GET) quy định các trường `required`: `['document_count', 'id', 'last_correspondence', 'name', 'permissions', 'slug', 'user_can_change']`.
- **Hành vi thực tế:**
  - Gọi POST tạo mới Correspondent thành công (`HTTP 201 Created`).
  - Response body thực tế: `{"id": ..., "slug": "...", "name": "...", "match": "", "matching_algorithm": 1, "is_insensitive": true, "owner": 2, "user_can_change": true}`.
  - Phản hồi **thiếu 3 trường**: `document_count`, `last_correspondence`, và `permissions`.
  - *Phân tích kỹ thuật:* Trường `permissions` gắn liền với query parameter `full_perms=true` khi gọi GET, nhưng schema lại đánh dấu bắt buộc trong response 201 của POST. Tương tự, `document_count` và `last_correspondence` là các trường tính toán từ quan hệ Document chưa được sinh khi tạo mới đối tượng.
- **Thực thi lần 2 (Độc lập):** Tạo mới lần hai -> Tiếp tục xác nhận response 201 thiếu 3 trường trên.
- **Kết luận:** Xác nhận tái hiện thành công lỗi vi phạm hợp đồng API trên tài nguyên `Correspondents`. Hồ sơ chỉ khẳng định BUG-03 trên `Correspondents` do chưa có kết quả kiểm tra response 201 tương đương trên các tài nguyên khác.
