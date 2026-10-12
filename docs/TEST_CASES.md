# BỘ TEST CASE THIẾT KẾ THỦ CÔNG (MANUAL TEST CASES)
**Học phần:** Kiểm thử phần mềm — Đề tài: Kiểm thử hệ thống Paperless-ngx bằng Schemathesis (R08 & K05)  
**Thành viên thực hiện:** TV2 — Tạ Nhật Nguyên  
**Tài nguyên phụ trách:** `Tag` (Endpoint: `/api/tags/`)  
**Môi trường thử nghiệm:** Docker Localhost (`http://localhost:8000/api/tags/`)

---

## 1. Tổng quan tài nguyên kiểm thử: `/api/tags/`
- **Mô tả:** Quản lý danh mục nhãn (Tag) dùng để phân loại tài liệu trong hệ thống Paperless-ngx.
- **Mã nguồn tương ứng:**
  - View: `TagViewSet` tại [src/documents/views.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/views.py)
  - Serializer: `TagSerializer` tại [src/documents/serialisers.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/serialisers.py)
  - Model: `Tag` tại [src/documents/models.py:102-140](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/models.py#L102-L140) (kế thừa `MatchingModel`, `TreeNodeModel`)
- **Các ràng buộc nghiệp vụ chính (Business Constraints):**
  - `name`: Kiểu chuỗi, độ dài tối đa **128 ký tự**, bắt buộc, không được để trống.
  - `name + owner`: Duy nhất theo người sở hữu (`UniqueConstraint`).
  - `color`: Mã màu HEX, độ dài tối đa **7 ký tự** (ví dụ `#a6cee3`), mặc định `#a6cee3`.
  - `match`: Độ dài tối đa 256 ký tự, có thể để trống.
  - `matching_algorithm`: Số nguyên dương từ `0` đến `6` (0: None, 1: Any, 2: All, 3: Exact, 4: Regex, 5: Fuzzy, 6: Auto). Mặc định là 1.
  - `is_insensitive`: Kiểu boolean, mặc định `true`.
  - `is_inbox_tag`: Kiểu boolean, mặc định `false`.
  - `parent`: Cấu trúc cây phân cấp nhãn, độ sâu tối đa `MAX_NESTING_DEPTH = 5`. Không được tự nhận mình làm cha.

---

## 2. Bảng tổng hợp Test Cases & Tiến độ thực nghiệm

> **Ghi chú báo cáo tiến độ:** Nhóm đã hoàn thành thiết kế toàn bộ **19/19 Test Case**. Trong đợt báo cáo tiến độ, TV2 đã thực thi thử nghiệm **8 ca đại diện** (phủ khắp các kỹ thuật: CRUD, Phân vùng tương đương, Giá trị biên, Ràng buộc DB, Bảo mật và Tái hiện Bug). **11 ca còn lại** nằm trong kế hoạch thực thi cho đợt báo cáo chính thức cuối kỳ.

| Mã Test Case | Phương thức | Endpoint | Kỹ thuật kiểm thử | Mục tiêu kiểm thử | Kỳ vọng | Thực tế (Tiến độ) | Đánh giá |
|---|---|---|---|---|---|---|---|
| **TC-TAG-01** | POST | `/api/tags/` | Phân vùng tương đương (Hợp lệ) | Tạo Tag chỉ với trường bắt buộc `name` | 201 Created | 201 Created | **PASS** |
| **TC-TAG-02** | POST | `/api/tags/` | Phân vùng tương đương (Hợp lệ) | Tạo Tag với đầy đủ tất cả các trường thuộc tính | 201 Created | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-03** | POST | `/api/tags/` | Phân vùng tương đương (Không hợp lệ) | Tạo Tag nhưng thiếu trường bắt buộc `name` | 400 Bad Request | 400 Bad Request | **PASS** |
| **TC-TAG-04** | POST | `/api/tags/` | Phân tích giá trị biên (BVA) | Tạo Tag với `name` là chuỗi rỗng `""` | 400 Bad Request | 400 Bad Request | **PASS** |
| **TC-TAG-05** | POST | `/api/tags/` | Phân tích giá trị biên (BVA) | Tạo Tag với `name` đúng 128 ký tự (biên trên hợp lệ) | 201 Created | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-06** | POST | `/api/tags/` | Phân tích giá trị biên (BVA) | Tạo Tag với `name` dài 129 ký tự (vượt biên max_length) | 400 Bad Request | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-07** | POST | `/api/tags/` | Kiểm thử tính duy nhất (Uniqueness) | Tạo Tag trùng tên với Tag đã tồn tại của cùng một chủ sở hữu | 400 Bad Request | 400 Bad Request | **PASS** |
| **TC-TAG-08** | POST | `/api/tags/` | Kiểm thử giá trị miền (Domain/Choices) | Tạo Tag với `matching_algorithm` không hợp lệ (`99`) | 400 Bad Request | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-09** | POST | `/api/tags/` | Phân tích giá trị biên (BVA - Color) | Tạo Tag với `color` vượt quá 7 ký tự (`#1234567`) | 400 Bad Request | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-10** | POST | `/api/tags/` | Ràng buộc phân cấp cây (Tree Model) | Tạo Tag con trỏ `parent` đến chính ID của nó | 400 Bad Request | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-11** | POST | `/api/tags/` | Error Guessing (Tái hiện lỗi mã nguồn) | Tạo Tag với `set_permissions` chứa `"view": false` | 400 Bad Request | 500 Server Error | **BUG-01 (500)** |
| **TC-TAG-12** | GET | `/api/tags/` | Kiểm thử truy vấn (Query/Listing) | Lấy danh sách Tag có phân trang và kiểm tra các trường trả về | 200 OK | 200 OK | **PASS** |
| **TC-TAG-13** | GET | `/api/tags/` | Kiểm thử lọc (Filter) | Lọc danh sách Tag theo tên (`?name__icontains=...`) | 200 OK | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-14** | GET | `/api/tags/{id}/` | Truy vấn chi tiết (Hợp lệ) | Xem thông tin chi tiết một Tag theo ID tồn tại | 200 OK | 200 OK | **PASS** |
| **TC-TAG-15** | GET | `/api/tags/{id}/` | Phân vùng tương đương (Không hợp lệ) | Xem thông tin Tag với ID không tồn tại (`999999`) | 404 Not Found | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-16** | PUT | `/api/tags/{id}/` | Cập nhật toàn phần (Full update) | Cập nhật lại toàn bộ thuộc tính của Tag đã có | 200 OK | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-17** | PATCH | `/api/tags/{id}/` | Cập nhật một phần (Partial update) | Chỉ cập nhật màu sắc (`color`) của Tag | 200 OK | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-18** | DELETE | `/api/tags/{id}/` | Xóa tài nguyên (Delete flow) | Xóa một Tag đang tồn tại và xác nhận không còn trong hệ thống | 204 No Content | *Chờ thực thi* | *Kế hoạch chính thức* |
| **TC-TAG-19** | GET | `/api/tags/` | Kiểm thử bảo mật & xác thực (Auth) | Gửi request không kèm Authorization header | 401 Unauthorized | 401 Unauthorized | **PASS** |

---

## 3. Chi tiết từng Test Case

### TC-TAG-01: Tạo Tag hợp lệ với các trường tối thiểu
- **Mục tiêu:** Kiểm tra hệ thống tự động gán các giá trị mặc định cho `color`, `matching_algorithm`, `is_insensitive`, `is_inbox_tag` khi người dùng chỉ cung cấp trường `name`.
- **Preconditions:** Đã có tài khoản admin và Authorization Token hợp lệ.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Headers: `Authorization: Token <TOKEN>`, `Content-Type: application/json`
  - Body:
    ```json
    {
      "name": "Manual_Test_Tag_Minimal"
    }
    ```
- **Expected Result:**
  - HTTP Status: `201 Created`
  - Response Body: Có trường `id`, `name`: `"Manual_Test_Tag_Minimal"`, `slug`: `"manual_test_tag_minimal"`, `color`: `"#a6cee3"`, `matching_algorithm`: `1`, `is_insensitive`: `true`, `is_inbox_tag`: `false`.

---

### TC-TAG-02: Tạo Tag với đầy đủ thuộc tính
- **Mục tiêu:** Kiểm tra tạo thành công một Tag khi điền đầy đủ tất cả các trường cấu hình nâng cao.
- **Preconditions:** Token xác thực hợp lệ.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body:
    ```json
    {
      "name": "Manual_Test_Tag_Full",
      "color": "#ff5733",
      "text_color": "#ffffff",
      "match": "hoá đơn",
      "matching_algorithm": 3,
      "is_insensitive": false,
      "is_inbox_tag": true
    }
    ```
- **Expected Result:**
  - HTTP Status: `201 Created`
  - Response Body chứa đúng các giá trị đã truyền: `color`: `"#ff5733"`, `match`: `"hoá đơn"`, `matching_algorithm`: `3`, `is_inbox_tag`: `true`.

---

### TC-TAG-03: Tạo Tag thiếu trường bắt buộc `name`
- **Mục tiêu:** Kiểm tra DRF validation từ chối request không chứa trường bắt buộc.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: `{"color": "#112233"}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"name": ["This field is required."]}`

---

### TC-TAG-04: Tạo Tag với `name` là chuỗi rỗng
- **Mục tiêu:** Kiểm tra hệ thống không cho phép lưu nhãn có tên rỗng.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: `{"name": ""}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"name": ["This field may not be blank."]}`

---

### TC-TAG-05: Tạo Tag với `name` đúng 128 ký tự (Biên hợp lệ)
- **Mục tiêu:** Kiểm tra giá trị biên trên (Boundary Value Analysis) của `models.CharField(max_length=128)`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body:
    ```json
    {
      "name": "A123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L12345678912345678"
    }
    ```
- **Expected Result:**
  - HTTP Status: `201 Created` (Tag được tạo thành công với chuỗi 128 ký tự).

---

### TC-TAG-06: Tạo Tag với `name` dài 129 ký tự (Vượt biên tối đa)
- **Mục tiêu:** Kiểm tra hệ thống từ chối chuỗi vượt quá `max_length=128`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: Chuỗi gồm 129 ký tự.
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"name": ["Ensure this field has no more than 128 characters."]}`

---

### TC-TAG-07: Tạo Tag trùng tên với Tag đã tồn tại
- **Mục tiêu:** Kiểm tra ràng buộc tính duy nhất `UniqueConstraint(fields=["name", "owner"])`.
- **Preconditions:** Đã có Tag mang tên `"TV2_Tag_Invoice_202"`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: `{"name": "TV2_Tag_Invoice_202"}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"name": ["Tag with this Name already exists."]}` hoặc thông báo vi phạm tính duy nhất tương tự.

---

### TC-TAG-08: Tạo Tag với `matching_algorithm` không hợp lệ
- **Mục tiêu:** Kiểm tra validation danh mục lựa chọn (choices: 0..6).
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: `{"name": "Tag_Invalid_Algo", "matching_algorithm": 99}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"matching_algorithm": ["\"99\" is not a valid choice."]}`

---

### TC-TAG-09: Tạo Tag với mã màu vượt quá độ dài 7 ký tự
- **Mục tiêu:** Kiểm tra ràng buộc `color = models.CharField(max_length=7)`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body: `{"name": "Tag_Color_Overflow", "color": "#12345678"}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"color": ["Ensure this field has no more than 7 characters."]}`

---

### TC-TAG-10: Tạo Tag vi phạm cấu trúc cây (Self-parenting)
- **Mục tiêu:** Kiểm tra phương thức `clean()` của `TreeNodeModel` ngăn chặn một tag chọn chính mình làm cha.
- **Preconditions:** Tag ID 95 đã tồn tại.
- **Request:**
  - Method: `PATCH`
  - URL: `http://localhost:8000/api/tags/95/`
  - Body: `{"parent": 95}`
- **Expected Result:**
  - HTTP Status: `400 Bad Request`
  - Response Body: `{"parent": ["Cannot set itself as parent."]}`

---

### TC-TAG-11: Tạo Tag với payload `set_permissions` lỗi (BUG-01)
- **Mục tiêu:** Kiểm tra xử lý ngoại lệ khi gửi dữ liệu quyền không đúng định dạng.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/tags/`
  - Body:
    ```json
    {
      "name": "Tag_Perm_Test",
      "set_permissions": {
        "view": false
      }
    }
    ```
- **Expected Result:**
  - Mong đợi: `400 Bad Request` (Báo lỗi kiểu dữ liệu quyền không hợp lệ).
  - *Thực tế ghi nhận:* Trả về `500 Internal Server Error` (do lỗi mã nguồn tại `serialisers.py:241` đã được phân tích ở BUG-01).

---

### TC-TAG-12: Lấy danh sách Tag (`GET /api/tags/`)
- **Mục tiêu:** Kiểm tra truy vấn danh sách, phân trang, và số lượng phần tử trả về.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/tags/?page=1&page_size=25`
- **Expected Result:**
  - HTTP Status: `200 OK`
  - Response Body chứa cấu trúc chuẩn DRF: `count`, `next`, `previous`, `results` (mảng chứa các đối tượng Tag).

---

### TC-TAG-13: Lọc Tag theo tên
- **Mục tiêu:** Kiểm tra bộ lọc `name__icontains` hoạt động chính xác.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/tags/?name__icontains=Invoice`
- **Expected Result:**
  - HTTP Status: `200 OK`
  - Mọi phần tử trong `results` đều có `name` chứa từ khóa `"Invoice"`.

---

### TC-TAG-14: Lấy chi tiết Tag theo ID tồn tại
- **Mục tiêu:** Kiểm tra truy vấn chi tiết thực thể theo khóa chính.
- **Preconditions:** Tag ID 95 (`TV2_Tag_Invoice_202`) đang tồn tại.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/tags/95/`
- **Expected Result:**
  - HTTP Status: `200 OK`
  - Response Body chứa đối tượng JSON của Tag ID 95.

---

### TC-TAG-15: Lấy chi tiết Tag với ID không tồn tại
- **Mục tiêu:** Kiểm tra xử lý ngoại lệ khi không tìm thấy thực thể (Not Found).
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/tags/999999/`
- **Expected Result:**
  - HTTP Status: `404 Not Found`
  - Response Body: `{"detail": "No Tag matches the given query."}`

---

### TC-TAG-16: Cập nhật toàn phần Tag (`PUT`)
- **Mục tiêu:** Kiểm tra cập nhật toàn bộ thuộc tính của một Tag.
- **Request:**
  - Method: `PUT`
  - URL: `http://localhost:8000/api/tags/95/`
  - Body:
    ```json
    {
      "name": "TV2_Tag_Invoice_Updated",
      "color": "#123456",
      "matching_algorithm": 2,
      "is_insensitive": false,
      "is_inbox_tag": false
    }
    ```
- **Expected Result:**
  - HTTP Status: `200 OK`
  - Response Body phản ánh tên mới `"TV2_Tag_Invoice_Updated"` và màu `"#123456"`.

---

### TC-TAG-17: Cập nhật một phần Tag (`PATCH`)
- **Mục tiêu:** Kiểm tra cập nhật một trường riêng lẻ mà không làm ảnh hưởng các trường khác.
- **Request:**
  - Method: `PATCH`
  - URL: `http://localhost:8000/api/tags/95/`
  - Body: `{"color": "#00ff00"}`
- **Expected Result:**
  - HTTP Status: `200 OK`
  - Trường `color` đổi thành `"#00ff00"`, các trường `name`, `matching_algorithm` giữ nguyên.

---

### TC-TAG-18: Xóa Tag (`DELETE`)
- **Mục tiêu:** Kiểm tra xóa một Tag thành công và phản hồi HTTP 204.
- **Request:**
  - Method: `DELETE`
  - URL: `http://localhost:8000/api/tags/95/`
- **Expected Result:**
  - HTTP Status: `204 No Content`
  - Response Body rỗng.
  - Khi thực hiện `GET /api/tags/95/` ngay sau đó, hệ thống trả về `404 Not Found`.

---

### TC-TAG-19: Truy cập không có xác thực (Unauthorized)
- **Mục tiêu:** Kiểm tra cơ chế bảo mật phân quyền token trên toàn bộ endpoint `/api/tags/`.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/tags/`
  - Headers: Không có `Authorization` header.
- **Expected Result:**
  - HTTP Status: `401 Unauthorized`
  - Response Body: `{"detail": "Authentication credentials were not provided."}`
