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

## 2. Bảng tổng hợp Test Cases

| Mã Test Case | Phương thức | Endpoint | Kỹ thuật kiểm thử | Mục tiêu kiểm thử | Kỳ vọng | Thực tế | Đánh giá |
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


---

# PHẦN II: TÀI NGUYÊN KIỂM THỬ CORRESPONDENTS (`/api/correspondents/`)
**Học phần:** Kiểm thử phần mềm — Đề tài: Kiểm thử hệ thống Paperless-ngx bằng Schemathesis (R08 & K05)  
**Thành viên thực hiện:** TV4 — Tạ Nhật Nguyên (Automation & Tổng hợp số liệu)  
**Tài nguyên phụ trách:** `Correspondents` (Người gửi / Cơ quan phát hành tài liệu)  
**Môi trường thử nghiệm:** Docker Localhost (`http://localhost:8000/api/correspondents/`)

---

## 1. Tổng quan tài nguyên kiểm thử: `/api/correspondents/`
- **Mô tả:** Quản lý danh mục người gửi/cơ quan phát hành tài liệu (Correspondent) trong hệ thống Paperless-ngx.
- **Mã nguồn tương ứng:**
  - View: `CorrespondentViewSet` tại `src/documents/views.py`
  - Serializer: `CorrespondentSerializer` tại `src/documents/serialisers.py`
  - Model: `Correspondent` tại `src/documents/models.py` (kế thừa `MatchingModel`)
- **Các ràng buộc nghiệp vụ chính (Business Constraints):**
  - `name`: Kiểu chuỗi, độ dài tối đa **128 ký tự**, bắt buộc, không được để trống.
  - `name + owner`: Duy nhất theo người sở hữu (`UniqueConstraint`).
  - `match`: Độ dài tối đa 256 ký tự, có thể để trống.
  - `matching_algorithm`: Số nguyên dương từ `0` đến `6` (0: None, 1: Any, 2: All, 3: Exact, 4: Regex, 5: Fuzzy, 6: Auto). Mặc định là 1.
  - `is_insensitive`: Kiểu boolean, mặc định `true`.
  - `set_permissions`: Cấu hình phân quyền đọc (`view`) và sửa (`change`) cho người dùng/nhóm.

---

## 2. Bảng tổng hợp Test Cases (Correspondents)

| Mã Test Case | Phương thức | Endpoint | Kỹ thuật kiểm thử | Mục tiêu kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|---|---|
| **TC-CORR-01** | POST | `/api/correspondents/` | Phân vùng tương đương (Hợp lệ) | Tạo Correspondent chỉ với trường bắt buộc `name` | 201 Created | 201 Created | Pass |
| **TC-CORR-02** | POST | `/api/correspondents/` | Phân vùng tương đương (Hợp lệ) | Tạo Correspondent với đầy đủ các thuộc tính cấu hình | 201 Created | 201 Created | Pass |
| **TC-CORR-03** | POST | `/api/correspondents/` | Phân vùng tương đương (Không hợp lệ) | Tạo Correspondent nhưng thiếu trường bắt buộc `name` | 400 Bad Request | 400 Bad Request | Pass |
| **TC-CORR-04** | POST | `/api/correspondents/` | Phân tích giá trị biên (BVA) | Tạo Correspondent với `name` là chuỗi rỗng `""` | 400 Bad Request | 400 Bad Request | Pass |
| **TC-CORR-05** | POST | `/api/correspondents/` | Phân tích giá trị biên (BVA) | Tạo Correspondent với `name` đúng 128 ký tự (biên trên hợp lệ) | 201 Created | 201 Created | Pass |
| **TC-CORR-06** | POST | `/api/correspondents/` | Phân tích giá trị biên (BVA) | Tạo Correspondent với `name` dài 129 ký tự (vượt biên max_length) | 400 Bad Request | 400 Bad Request | Pass |
| **TC-CORR-07** | POST | `/api/correspondents/` | Kiểm thử tính duy nhất (Uniqueness) | Tạo Correspondent trùng tên với đối tượng đã có cùng owner | 400 Bad Request | 400 Bad Request | Pass |
| **TC-CORR-08** | POST | `/api/correspondents/` | Kiểm thử giá trị miền (Domain/Choices) | Tạo Correspondent với `matching_algorithm` không hợp lệ (`99`) | 400 Bad Request | 400 Bad Request | Pass |
| **TC-CORR-09** | POST | `/api/correspondents/` | Error Guessing (Lỗi hệ thống - BUG-01) | Gửi payload `set_permissions` chứa `"view": false` | 400 Bad Request | 500 Internal Server Error | **Fail (Bug)** |
| **TC-CORR-10** | POST | `/api/correspondents/` | Contract Testing (Lỗi Schema - BUG-03) | Kiểm tra response 201 có đủ trường `document_count`, `permissions` | Phù hợp OpenAPI Schema | Thiếu trường required | **Fail (Bug)** |
| **TC-CORR-11** | GET | `/api/correspondents/` | Truy vấn danh sách (Listing) | Lấy danh sách Correspondent có phân trang | 200 OK | 200 OK | Pass |
| **TC-CORR-12** | GET | `/api/correspondents/` | Kiểm thử lọc (Filter) | Lọc danh sách theo tên (`?name__icontains=...`) | 200 OK | 200 OK | Pass |
| **TC-CORR-13** | GET | `/api/correspondents/{id}/` | Truy vấn chi tiết (Hợp lệ) | Xem chi tiết Correspondent theo ID đang tồn tại | 200 OK | 200 OK | Pass |
| **TC-CORR-14** | GET | `/api/correspondents/{id}/` | Phân vùng tương đương (Không hợp lệ) | Xem chi tiết với ID không tồn tại (`999999`) | 404 Not Found | 404 Not Found | Pass |
| **TC-CORR-15** | PUT | `/api/correspondents/{id}/` | Cập nhật toàn phần (Full update) | Cập nhật lại toàn bộ thuộc tính Correspondent | 200 OK | 200 OK | Pass |
| **TC-CORR-16** | PATCH | `/api/correspondents/{id}/` | Cập nhật một phần (Partial update) | Chỉ cập nhật cấu hình thuật toán khớp `matching_algorithm` | 200 OK | 200 OK | Pass |
| **TC-CORR-17** | DELETE | `/api/correspondents/{id}/` | Xóa tài nguyên (Delete flow) | Xóa Correspondent tồn tại và xác nhận bị xóa khỏi DB | 204 No Content | 204 No Content | Pass |
| **TC-CORR-18** | GET | `/api/correspondents/` | Bảo mật & Xác thực (Auth) | Gửi request không kèm Authorization token | 401 Unauthorized | 401 Unauthorized | Pass |

---

## 3. Chi tiết từng Test Case (Correspondents)

### TC-CORR-01: Tạo Correspondent hợp lệ với trường tối thiểu
- **Mục tiêu:** Kiểm tra hệ thống tự động gán giá trị mặc định cho `matching_algorithm` (1), `is_insensitive` (true), `match` ("") khi chỉ gửi `name`.
- **Preconditions:** Token xác thực hợp lệ.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "TV4_Manual_Correspondent_Minimal"}`
- **Expected Result:** HTTP 201 Created, body có `id`, `name`: `"TV4_Manual_Correspondent_Minimal"`, `slug`: `"tv4_manual_correspondent_minimal"`.

---

### TC-CORR-02: Tạo Correspondent với đầy đủ thuộc tính
- **Mục tiêu:** Kiểm tra cấu hình bộ lọc khớp tự động tài liệu của người gửi.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body:
    ```json
    {
      "name": "TV4_Manual_Bank_Full",
      "match": "ngân hàng agribank",
      "matching_algorithm": 3,
      "is_insensitive": false
    }
    ```
- **Expected Result:** HTTP 201 Created phản ánh đúng cấu hình khớp chính xác (`matching_algorithm`: 3).

---

### TC-CORR-03: Tạo Correspondent thiếu trường bắt buộc `name`
- **Mục tiêu:** Kiểm tra DRF validation ngăn chặn request thiếu trường `name`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"match": "abc"}`
- **Expected Result:** HTTP 400 Bad Request, body: `{"name": ["This field is required."]}`.

---

### TC-CORR-04: Tạo Correspondent với `name` là chuỗi rỗng
- **Mục tiêu:** Kiểm tra không cho phép tên người gửi là chuỗi khoảng trắng hoặc rỗng.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": ""}`
- **Expected Result:** HTTP 400 Bad Request, body: `{"name": ["This field may not be blank."]}`.

---

### TC-CORR-05: Tạo Correspondent với `name` đúng 128 ký tự (Biên hợp lệ)
- **Mục tiêu:** Kiểm tra giá trị biên trên của `models.CharField(max_length=128)`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C12345678912345678"}`
- **Expected Result:** HTTP 201 Created thành công.

---

### TC-CORR-06: Tạo Correspondent với `name` dài 129 ký tự (Vượt biên tối đa)
- **Mục tiêu:** Kiểm tra DRF từ chối chuỗi dài 129 ký tự.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789C123456789123456789"}`
- **Expected Result:** HTTP 400 Bad Request, body: `{"name": ["Ensure this field has no more than 128 characters."]}`.

---

### TC-CORR-07: Tạo Correspondent trùng tên đã có
- **Mục tiêu:** Kiểm tra ràng buộc duy nhất `UniqueConstraint(fields=["name", "owner"])`.
- **Preconditions:** Đã có Correspondent `"TV2_Bank_202"`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "TV2_Bank_202"}`
- **Expected Result:** HTTP 400 Bad Request thông báo tên người gửi đã tồn tại.

---

### TC-CORR-08: Tạo Correspondent với `matching_algorithm` không hợp lệ
- **Mục tiêu:** Kiểm tra miền giá trị của `matching_algorithm` (chỉ nhận từ 0 đến 6).
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "Corr_Invalid_Algo", "matching_algorithm": 99}`
- **Expected Result:** HTTP 400 Bad Request, body: `{"matching_algorithm": ["\"99\" is not a valid choice."]}`.

---

### TC-CORR-09: Tạo Correspondent với `set_permissions` sai kiểu (Tái hiện BUG-01)
- **Mục tiêu:** Kiểm tra lỗ hổng ngoại lệ chưa bắt khi truyền boolean vào dictionary permissions.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "Corr_Crash_Test", "set_permissions": {"view": false}}`
- **Expected Result:** Mong đợi `400 Bad Request`.
- **Actual Result:** Server ném `TypeError` và trả về `500 Internal Server Error` (Xác nhận lỗi BUG-01).

---

### TC-CORR-10: Kiểm tra Response vi phạm OpenAPI Schema (Tái hiện BUG-03)
- **Mục tiêu:** Kiểm tra tính tuân thủ hợp đồng API (API Contract) theo file Swagger `/api/schema/`.
- **Request:**
  - Method: `POST`
  - URL: `http://localhost:8000/api/correspondents/`
  - Body: `{"name": "Corr_Schema_Contract_Test"}`
- **Expected Result:** Response 201 phải chứa các trường bắt buộc đã cam kết: `document_count`, `last_correspondence`, `permissions`.
- **Actual Result:** Response 201 thiếu các trường bắt buộc này (Xác nhận lỗi BUG-03).

---

### TC-CORR-11: Lấy danh sách Correspondent (`GET /api/correspondents/`)
- **Mục tiêu:** Kiểm tra truy vấn danh sách người gửi và cấu trúc phân trang.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/correspondents/?page=1&page_size=25`
- **Expected Result:** HTTP 200 OK kèm các trường phân trang `count`, `next`, `previous`, `results`.

---

### TC-CORR-12: Lọc Correspondent theo tên
- **Mục tiêu:** Kiểm tra bộ lọc tìm kiếm con `name__icontains`.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/correspondents/?name__icontains=Bank`
- **Expected Result:** HTTP 200 OK, tất cả kết quả trả về đều chứa chuỗi "Bank".

---

### TC-CORR-13: Lấy chi tiết Correspondent theo ID tồn tại
- **Mục tiêu:** Kiểm tra truy vấn thực thể đơn lẻ theo Primary Key.
- **Preconditions:** Correspondent ID 1 (`TV2_Bank_202`) đang tồn tại.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/correspondents/1/`
- **Expected Result:** HTTP 200 OK trả về thông tin chi tiết của Correspondent ID 1.

---

### TC-CORR-14: Lấy chi tiết với ID không tồn tại
- **Mục tiêu:** Kiểm tra xử lý đối tượng không tìm thấy.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/correspondents/999999/`
- **Expected Result:** HTTP 404 Not Found, body: `{"detail": "No Correspondent matches the given query."}`.

---

### TC-CORR-15: Cập nhật toàn phần Correspondent (`PUT`)
- **Mục tiêu:** Kiểm tra cập nhật toàn bộ thuộc tính người gửi.
- **Request:**
  - Method: `PUT`
  - URL: `http://localhost:8000/api/correspondents/1/`
  - Body: `{"name": "TV2_Bank_Updated", "match": "ngan hang", "matching_algorithm": 2, "is_insensitive": true}`
- **Expected Result:** HTTP 200 OK phản ánh thông tin mới.

---

### TC-CORR-16: Cập nhật một phần Correspondent (`PATCH`)
- **Mục tiêu:** Kiểm tra cập nhật riêng lẻ trường `matching_algorithm`.
- **Request:**
  - Method: `PATCH`
  - URL: `http://localhost:8000/api/correspondents/1/`
  - Body: `{"matching_algorithm": 4}`
- **Expected Result:** HTTP 200 OK, `matching_algorithm` đổi thành 4, các trường khác giữ nguyên.

---

### TC-CORR-17: Xóa Correspondent (`DELETE`)
- **Mục tiêu:** Kiểm tra xóa thành công người gửi.
- **Request:**
  - Method: `DELETE`
  - URL: `http://localhost:8000/api/correspondents/1/`
- **Expected Result:** HTTP 204 No Content, body rỗng. Truy vấn lại ngay sau đó trả về 404.

---

### TC-CORR-18: Truy cập không xác thực (Unauthorized)
- **Mục tiêu:** Kiểm tra bảo vệ quyền truy cập API.
- **Request:**
  - Method: `GET`
  - URL: `http://localhost:8000/api/correspondents/`
  - Headers: Không có `Authorization`.
- **Expected Result:** HTTP 401 Unauthorized, body: `{"detail": "Authentication credentials were not provided."}`.
