# BÍ KÍP VẤN ĐÁP BẢO VỆ ĐỀ TÀI KIỂM THỬ PHẦN MỀM (DEFENSE CHEAT SHEET)
**Đề tài:** Kiểm thử hệ thống Paperless-ngx bằng kỹ thuật Schema-based API Testing (Schemathesis)  
**Mã đề tài:** R08 (Paperless-ngx) + K05 (Schemathesis)  
**Thành viên:** TV2 — Tạ Nhật Nguyên (Seed: 202)

---

## PHẦN 1: BẢN CHẤT PHƯƠNG PHÁP KIỂM THỬ K05 (SCHEMATHESIS)

### Câu 1: Phương pháp K05 - Schema-based API Testing là gì? Khác gì kiểm thử thông thường?
- **Trả lời:**
  - *Kiểm thử thông thường (như Postman / viết tay):* Con người tự nghĩ ra từng test case (vài chục ca), tự nhập dữ liệu và tự kiểm tra kết quả. Nhược điểm là tốn công và dễ bỏ sót các trường hợp biên dị hợm.
  - *Schema-based API Testing (K05):* Là kỹ thuật kiểm thử tự động dựa trên **Hợp đồng giao tiếp (API Contract / OpenAPI Specification)**. Công cụ (Schemathesis) tự động đọc file đặc tả API (`/api/schema/`), hiểu cấu trúc dữ liệu của từng endpoint, rồi tự động sinh ra hàng ngàn test cases và tự động kiểm tra xem phản hồi của máy chủ có đúng chuẩn cam kết hay không.

### Câu 2: Dữ liệu kiểm thử (Test Data) lấy từ đâu ra? Tại sao nó sinh được chuỗi dị hợm, số âm, ký tự lạ?
- **Trả lời:**
  - Dữ liệu hoàn toàn **do Schemathesis tự động sinh ra** dựa trên thư viện kiểm thử theo thuộc tính **Hypothesis** (Property-based Testing) và kỹ thuật **Fuzzing**.
  - *Cơ chế:* 
    1. Đầu tiên, nó đọc schema để biết kiểu dữ liệu (ví dụ: trường `name` là `string`, `max_length: 128`).
    2. Sau đó nó sinh dữ liệu hợp lệ (Positive testing).
    3. Tiếp theo, engine Fuzzing cố tình "đột biến" dữ liệu (Negative testing): nhét các ký tự Unicode không in được, null byte `\x00`, số thực vô cực, số nguyên âm cực lớn, chuỗi rỗng... để kiểm tra độ bền (Robustness) và khả năng xử lý ngoại lệ của máy chủ backend.

### Câu 3: Tại sao bắt buộc phải dùng Seed (Seed 202)?
- **Trả lời:** 
  - Vì Schemathesis sinh dữ liệu ngẫu nhiên. Nếu không cố định seed, mỗi lần chạy sẽ ra một bộ dữ liệu khác nhau và khi phát hiện ra bug thì không ai có thể làm lại giống hệt để kiểm tra (mất tính **Tái lập - Reproducibility**).
  - Ghim **`--seed 202`** đảm bảo trình sinh số giả ngẫu nhiên hoạt động theo đúng một chuỗi cố định. Bất kỳ ai, ở bất kỳ máy tính nào, gõ lệnh với `--seed 202` đều sẽ nhận được kết quả và các lỗi y hệt 100%.

---

## PHẦN 2: Ý NGHĨA CÁC THAM SỐ TRONG LỆNH CHẠY SCHEMATHESIS

Lệnh chạy mẫu:
```bash
docker run --rm -it --network ktpm_default schemathesis/schemathesis:latest run http://webserver:8000/api/schema/ --include-path-regex "^/api/tags/" --seed 202 --max-examples 5 -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a"
```

| Tham số / Cờ | Ý nghĩa kỹ thuật |
|---|---|
| `docker run --rm -it` | Chạy Schemathesis bằng Docker container, tự động xóa container sau khi chạy xong để sạch máy. |
| `--network ktpm_default` | Cho Schemathesis kết nối vào cùng mạng nội bộ Docker với Paperless-ngx để gọi được tên miền nội bộ `http://webserver:8000/`. |
| `http://webserver:8000/api/schema/` | Đường dẫn endpoint trả về tài liệu đặc tả OpenAPI 3.0 của Paperless-ngx. |
| `--include-path-regex "^/api/tags/"` | Bộ lọc endpoint: Chỉ quét các API bắt đầu bằng `/api/tags/` (tài nguyên do TV2 phụ trách). |
| `--seed 202` | Ghim hạt giống ngẫu nhiên 202 để đảm bảo tính tái lập (Reproducibility). |
| `--max-examples 5` | Số lượng mẫu kiểm thử tối đa sinh ra cho mỗi API operation (Vòng 3 dùng 25 mẫu). |
| `-H "Authorization: Token ..."` | Gắn header xác thực tài khoản admin cho mọi request gửi đi. |
| `--checks all` *(dùng ở Vòng 3)* | Bật toàn bộ các bộ kiểm tra: kiểm tra sập server (500), kiểm tra vi phạm schema, kiểm tra status code, kiểm tra content-type. |

---

## PHẦN 3: ĐỘ BAO PHỦ (COVERAGE) TRONG SCHEMATHESIS

Khi thầy hỏi: *"Độ bao phủ (Coverage) đọc ở đâu? Nghĩa là gì?"*, bạn chỉ vào bảng `Schema Coverage` ở cuối màn hình terminal:

1. **Operations Coverage (Bao phủ Endpoint/Thao tác):**
   - Ví dụ: `6 / 163 (3.6%)` ➔ Hệ thống có tổng cộng 163 thao tác API, lệnh kiểm thử này nhóm chọn lọc và bao phủ 6 thao tác thuộc nhóm `/api/tags/` (GET danh sách, GET chi tiết, POST, PUT, PATCH, DELETE).
2. **Parameters Coverage (Bao phủ Tham số):**
   - Tỷ lệ các tham số (query params, path params, header params) đã được Schemathesis đưa dữ liệu vào kiểm thử.
3. **Responses Coverage (Bao phủ Mã phản hồi):**
   - Tỷ lệ các mã trạng thái HTTP (200, 201, 400, 404,...) nhận được trong thực tế so với các mã phản hồi được mô tả trong schema.

---

## PHẦN 4: KIẾN TRÚC DỰ ÁN PAPERLESS-NGX (PHẦN VIỆC TV2)

### Câu 1: Hệ thống gồm những container nào?
- **Trả lời:** Triển khai bằng Docker Compose gồm **3 container** trên mạng `ktpm_default`:
  1. `paperless-webserver`: Chứa backend Django 5.1, máy chủ web ASGI (Granian/Gunicorn), giao diện Angular và tích hợp sẵn tiến trình **Celery worker** xử lý ngầm và engine **Tesseract OCR**.
  2. `paperless-db`: Chạy PostgreSQL 16 Alpine, lưu trữ cơ sở dữ liệu có cấu trúc.
  3. `paperless-broker`: Chạy Redis 7 Alpine, đóng vai trò message broker hàng đợi tác vụ cho Celery.

### Câu 2: Luồng xử lý một tài liệu khi người dùng upload diễn ra thế nào?
- **Trả lời:** 
  1. Client gửi `POST /api/documents/post_document/` kèm file tới `webserver`.
  2. `webserver` kiểm tra hợp lệ, lưu tạm file vào thư mục media, tạo một Task ID và đẩy thông tin tác vụ vào **Redis**. Webserver trả về ngay mã `200/202` cho client mà không bắt client phải chờ (luồng đồng bộ).
  3. Tiến trình **Celery worker** bên trong webserver lắng nghe Redis, rút tác vụ ra để thực hiện tiền xử lý, gọi **Tesseract OCR** để nhận diện chữ, chạy thuật toán **Matching** để gán Tag tự động, lưu thông tin vào **PostgreSQL** và cập nhật chỉ mục tìm kiếm Whoosh (luồng bất đồng bộ).

---

## PHẦN 5: 3 BUG THỰC TẾ ĐÃ TÌM ĐƯỢC (TÓM TẮT DỄ NHỚ)

### 1. BUG-01: Server trả về HTTP 500 do lỗi `TypeError` ở quyền (`set_permissions`)
- **Vị trí:** File `src/documents/serialisers.py:241` trong hàm `validate_set_permissions`.
- **Nguyên nhân:** Lập trình viên viết `if "users" in set_permissions[action]:` với giả định `action` luôn là dictionary. Khi Schemathesis gửi giá trị boolean `false` hoặc số nguyên, toán tử `in` văng lỗi `TypeError: argument of type 'bool' is not a container` làm sập server với lỗi 500.
- **Khắc phục:** Thêm kiểm tra `isinstance(set_permissions[action], dict)` trước khi truy cập phần tử.

### 2. BUG-02: Server trả về HTTP 500 do lỗi `ValueError` khi lọc năm âm (`modified__year`)
- **Vị trí:** File `src/documents/filters.py` kết hợp `django/db/backends/base/operations.py:636`.
- **Nguyên nhân:** Khi người dùng truyền số âm hoặc số thực `-1.17e-38`, giá trị bị ép thành số `0`. Khi Django ORM gọi `datetime.datetime(0, 1, 1)` để tạo câu lệnh SQL, Python ném lỗi `ValueError: year must be in 1..9999, not 0` vì năm hợp lệ phải từ 1 đến 9999.
- **Khắc phục:** Thêm ràng buộc `min_value=1, max_value=9999` cho bộ lọc `modified__year`.

### 3. BUG-03: Vi phạm hợp đồng Schema (Response 201 thiếu trường `document_count`)
- **Vị trí:** Schema tại `#/components/schemas/Correspondent` vs mã nguồn `src/documents/views.py`.
- **Nguyên nhân:** Schema OpenAPI cam kết phản hồi của Correspondent bắt buộc phải có trường `document_count`. Nhưng trong code `views.py`, trường này chỉ được tính khi gọi GET (qua hàm `get_queryset()`), còn khi POST tạo mới thì đối tượng vừa lưu chưa được tính toán nên trả về thiếu trường `document_count`.

---

## PHẦN 6: PHÂN BIỆT HTTP 400 VS HTTP 500 — LỖI NÀO MỚI LÀ BUG?

- **HTTP 400 (Bad Request):** Là phản hồi **ĐÚNG** của máy chủ. Khi client gửi dữ liệu sai (thiếu trường, tên quá dài), máy chủ bẫy lỗi thành công và thông báo từ chối lịch sự.
- **HTTP 500 (Internal Server Error):** Là **BUG NGHIÊM TRỌNG**. Khi client gửi dữ liệu sai hoặc dị, mã nguồn máy chủ bị crash do gặp ngoại lệ chưa được xử lý (Unhandled Exception) và làm sập tiến trình request. Tiêu chuẩn REST API nghiêm cấm máy chủ trả về 500 khi client gửi dữ liệu sai.
