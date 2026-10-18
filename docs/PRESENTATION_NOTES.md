# TÀI LIỆU CHUẨN BỊ BÁO CÁO BẢO VỆ GIỮA KỲ (PRESENTATION NOTES)
**Đề tài:** Kiểm thử hệ thống Paperless-ngx bằng kỹ thuật Schema-based API Testing (Schemathesis)  
**Phân công TV2:** Tạ Nhật Nguyên (Phụ trách Phần A & B: Mục tiêu, Actor, Kiến trúc hệ thống, Module và Luồng dữ liệu)  
**Tài liệu liên kết:** [docs/ARCHITECTURE_NOTES.md](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/docs/ARCHITECTURE_NOTES.md) | [docs/TEST_CASES.md](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/docs/TEST_CASES.md) | [docs/bugs/](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/docs/bugs/)

---

## PHẦN D1: KỊCH BẢN TRÌNH BÀY SLIDE (3-4 SLIDES PHẦN TV2)

> **Mẹo thuyết trình:** Không đọc nguyên văn từng chữ trên slide. Nhìn thẳng vào thầy cô, nói rõ ràng, tự tin, nhấn mạnh vào các từ khóa kỹ thuật (*Docker, Celery, Redis, DRF Serializer, OpenAPI Contract, Schemathesis*).

---

### Slide 1: Mục tiêu hệ thống Paperless-ngx & Các Actor
- **Mục tiêu slide:** Giúp hội đồng hiểu ngay hệ thống đang kiểm thử là gì và ai tương tác với nó.
- **Sơ đồ sử dụng:** Sơ đồ Use Case hoặc Bảng phân loại Actor (trong mục B1 của `ARCHITECTURE_NOTES.md`).
- **Ý chính trên slide:**
  - Paperless-ngx: Hệ thống quản lý tài liệu điện tử mã nguồn mở (DMS), số hóa tài liệu giấy, tự động OCR và tìm kiếm toàn văn.
  - 5 Actor cốt lõi:
    1. *Người dùng thường (End User):* Tải tài liệu, gắn nhãn, tra cứu qua Web UI.
    2. *Quản trị viên (Admin):* Cấu hình phân quyền, người dùng, quy trình tự động.
    3. *Tác vụ nền (Celery Worker & Consumer):* Xử lý OCR, trích xuất metadata bất đồng bộ.
    4. *Hệ thống bên ngoài (External Services):* Mail server (IMAP) tự động gửi tài liệu vào hệ thống.
    5. *QA Client (Schemathesis):* Đóng vai trò client tự động đọc OpenAPI spec và bắn payload kiểm thử.
- **2-3 câu nói mẫu (Dành cho TV2):**
  > *"Kính thưa thầy cô, Paperless-ngx là một hệ thống quản lý tài liệu phức tạp kết hợp giữa Web Application truyền thống và hệ thống xử lý bất đồng bộ nặng về OCR. Trong đề tài này, nhóm em không chỉ nhìn hệ thống từ góc độ người dùng giao diện, mà đặc biệt quan tâm tới Actor kiểm thử là công cụ Schemathesis – một API client tự động khai thác schema OpenAPI để kiểm tra tính toàn vẹn của hệ thống backend."*

---

### Slide 2: Kiến trúc Container & Hạ tầng dịch vụ (Container Architecture)
- **Mục tiêu slide:** Chứng minh nhóm đã dựng thành công hệ thống đúng chuẩn kiến trúc containerized và nắm rõ tương tác giữa các service.
- **Sơ đồ sử dụng:** Sơ đồ Container Architecture Mermaid (Mục B5.1 trong `ARCHITECTURE_NOTES.md`).
- **Ý chính trên slide:**
  - 3 Service container chính chạy trên Docker network `ktpm_default`:
    - `paperless-webserver` (Port 8000): Django 5.1 + Gunicorn + Celery Worker nội bộ.
    - `paperless-db` (Port 5432): PostgreSQL 16 Alpine lưu trữ dữ liệu thực thể có cấu trúc.
    - `paperless-broker` (Port 6379): Redis 7 Alpine làm message broker hàng đợi tác vụ.
  - Chia tách ranh giới rõ ràng: Webserver phục vụ REST API tức thời (Sync), tác vụ nặng được đẩy sang Celery qua Redis để xử lý nền (Async).
- **2-3 câu nói mẫu (Dành cho TV2):**
  > *"Để đảm bảo môi trường kiểm thử cô lập và có thể tái lập, nhóm em dựng toàn bộ hệ thống bằng Docker Compose với phiên bản ghim cố định v3.1.3. Kiến trúc này tách biệt rõ ràng giữa luồng xử lý HTTP đồng bộ qua Django REST Framework và luồng tác vụ nền qua Redis Broker. Điều này giúp hệ thống không bị nghẽn (blocking) khi người dùng tải lên nhiều tài liệu cùng lúc để OCR."*

---

### Slide 3: 4 Module kiểm thử trọng tâm & Ánh xạ API sang mã nguồn
- **Mục tiêu slide:** Chỉ ra cấu trúc mã nguồn nội bộ nơi trực tiếp đón nhận các request của Schemathesis.
- **Sơ đồ sử dụng:** Bảng ánh xạ Endpoint sang Code (Mục B4 trong `ARCHITECTURE_NOTES.md`).
- **Ý chính trên slide:**
  - 4 Module cốt lõi tại `src/documents/`:
    - `views.py` (`TagViewSet`, `CorrespondentViewSet`, `DocumentViewSet`): Điều hướng request, phân quyền, lọc dữ liệu.
    - `serialisers.py` (`TagSerializer`, `CorrespondentSerializer`): Xác thực dữ liệu đầu vào (Input Validation), chuyển đổi JSON (Serialization).
    - `models.py` (`Tag`, `Correspondent`, `Document`): Định nghĩa lược đồ dữ liệu DB, ràng buộc toàn vẹn (`max_length`, `unique`).
    - `filters.py` (`DocumentFilterSet`): Xử lý các query parameter tìm kiếm và lọc nâng cao.
- **2-3 câu nói mẫu (Dành cho TV2):**
  > *"Khi Schemathesis gửi các request fuzzing, chúng sẽ đi xuyên qua 4 tầng mã nguồn chính của ứng dụng Django: Tầng View điều hướng, tầng Serializer kiểm tra hợp lệ kiểu dữ liệu, tầng Filter xử lý các tham số tìm kiếm và tầng Model ghi xuống cơ sở dữ liệu. Bất kỳ sự thiếu sót nào trong việc validate dữ liệu ở tầng Serializer hay Filter đều sẽ dẫn đến việc request đi thẳng vào ORM và làm sập máy chủ bằng lỗi 500."*

---

### Slide 4: Luồng dữ liệu (Data Flow) & Kiểm thử Schemathesis
- **Mục tiêu slide:** Trình bày trực quan luồng đi của dữ liệu qua các thành phần hệ thống và cách Schemathesis phát hiện lỗi.
- **Sơ đồ sử dụng:** Sơ đồ tuần tự Schemathesis Test Flow (Mục B6.4 trong `ARCHITECTURE_NOTES.md`) hoặc Luồng Upload tài liệu (B6.1).
- **Ý chính trên slide:**
  - Luồng 1: Schemathesis fetch `/api/schema/` → Phân tích JSON Schema → Sinh payload fuzzing.
  - Luồng 2: Client gửi request → Serializer validate:
    - Nếu hợp lệ: Lưu DB, trả về 201/200.
    - Nếu vi phạm logic: Ném `ValidationError`, trả về 400 Bad Request (Hành vi đúng).
    - Nếu mã nguồn thiếu kiểm tra kiểu (Type check missing): Ném unhandled exception (`TypeError`, `ValueError`), trả về 500 Internal Server Error (Lỗi hệ thống!).
- **2-3 câu nói mẫu (Dành cho TV2):**
  > *"Trên sơ đồ tuần tự này, thầy cô có thể thấy rõ quy trình Schemathesis phát hiện ra 2 lỗi nghiêm trọng mức HTTP 500 của hệ thống: Tại hàm `validate_set_permissions`, do thiếu kiểm tra kiểu dữ liệu dictionary trước khi duyệt mảng, máy chủ đã bị crash bởi ngoại lệ `TypeError`. Tương tự, tại bộ lọc năm, việc thiếu chặn khoảng giá trị đã khiến Django ORM văng `ValueError` khi biên dịch câu lệnh SQL. Cả hai trường hợp đều minh chứng cho sức mạnh của Schema-based testing trong việc tìm ra các ca kiểm thử biên mà lập trình viên bỏ sót."*

---

## PHẦN D2: HƯỚNG DẪN XUẤT SƠ ĐỒ MERMAID THÀNH HÌNH ẢNH

Để đưa sơ đồ vào slide PowerPoint hoặc báo cáo Word, TV2 thực hiện theo các bước sau:

1. **Cách 1: Sử dụng công cụ trực tuyến Mermaid Live Editor (Khuyên dùng - Nhanh nhất)**
   - Mở trình duyệt và truy cập: [https://mermaid.live](https://mermaid.live)
   - Mở file [docs/ARCHITECTURE_NOTES.md](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/docs/ARCHITECTURE_NOTES.md).
   - Sao chép toàn bộ khối mã sơ đồ Mermaid (bỏ qua 3 dấu backticks ` ```mermaid ` ở đầu và cuối):
     - *Sơ đồ 1:* Kiến trúc Container (Mục B5.1)
     - *Sơ đồ 2:* Thực thể quan hệ ER Diagram (Mục B5.2)
     - *Sơ đồ 3:* Luồng Upload & OCR tài liệu (Mục B6.1)
     - *Sơ đồ 4:* Luồng kiểm thử Schemathesis (Mục B6.4)
   - Dán vào khung soạn thảo bên trái của `mermaid.live`.
   - Bấm nút **Actions** → Chọn **Download PNG** (hoặc **SVG** để có độ nét cao nhất khi phóng to trên slide).
   - Lưu các file ảnh vào thư mục `docs/img/` với tên:
     - `docs/img/container_architecture.png`
     - `docs/img/er_diagram.png`
     - `docs/img/dataflow_upload.png`
     - `docs/img/dataflow_schemathesis.png`

2. **Cách 2: Sử dụng Mermaid CLI (Dành cho môi trường lập trình)**
   - Cài đặt mermaid-cli qua npm: `npm install -g @mermaid-js/mermaid-cli`
   - Chạy lệnh xuất ảnh: `mmdc -i input.mmd -o docs/img/output.png`

---

## PHẦN D3: 15 CÂU HỎI TỰ KIỂM TRA PHẢN BIỆN (DEFENSE Q&A)

Dưới đây là 15 câu hỏi trọng tâm mà Thầy/Cô hội đồng chấm thi thường vấn đáp sinh viên về kiến trúc, Docker, và luồng dữ liệu, kèm câu trả lời chuẩn xác kỹ thuật:

### 1. Paperless-ngx được triển khai bằng những container nào? Nhiệm vụ của từng container là gì?
- **Trả lời:** Hệ thống triển khai trên 3 container chính:
  1. `paperless-webserver`: Chứa backend Django 5.1, Gunicorn, REST API, Web UI, và tích hợp luôn Celery worker/consumer nội bộ để thực hiện tiền xử lý và OCR.
  2. `paperless-db`: Chạy PostgreSQL 16 Alpine, chịu trách nhiệm lưu trữ toàn bộ dữ liệu có cấu trúc (bảng Documents, Tags, Correspondents, Permissions...).
  3. `paperless-broker`: Chạy Redis 7 Alpine, đóng vai trò message broker lưu trữ hàng đợi công việc (task queue) của Celery.

### 2. Tại sao hệ thống cần đến Redis? Nếu không có Redis thì hệ thống có chạy được không?
- **Trả lời:** Redis là thành phần bắt buộc vì các tác vụ số hóa tài liệu (chuyển đổi PDF, render ảnh thu nhỏ, nhận diện chữ OCR qua Tesseract) tiêu tốn rất nhiều CPU và thời gian (vài giây đến vài chục giây). Nếu thực hiện đồng bộ trên Webserver, kết nối HTTP của người dùng sẽ bị timeout và làm treo toàn bộ ứng dụng. Redis đóng vai trò hàng đợi trung gian: Webserver nhận file xong trả về HTTP 200/202 ngay kèm Task ID, còn Redis giữ công việc để Celery worker lấy ra xử lý lần lượt ở tiến trình nền. Không có Redis, hệ thống Paperless-ngx không thể khởi động được.

### 3. Quá trình OCR (Optical Character Recognition) diễn ra ở container nào?
- **Trả lời:** Quá trình OCR diễn ra bên trong container `paperless-webserver`. Trong container này đã được cài sẵn engine `tesseract-ocr` cùng các gói ngôn ngữ và thư viện xử lý ảnh (`pdf2image`, `pikepdf`). Tiến trình Celery worker chạy bên trong container này sẽ gọi trực tiếp binary Tesseract để trích xuất văn bản từ tài liệu.

### 4. Schemathesis đọc thông tin gì từ hệ thống Paperless-ngx trước khi chạy kiểm thử?
- **Trả lời:** Schemathesis gọi HTTP GET tới endpoint công bố schema của hệ thống tại `http://webserver:8000/api/schema/`. Endpoint này trả về tài liệu đặc tả OpenAPI 3.0 (sinh tự động bởi thư viện `drf-spectacular`), chứa toàn bộ thông tin về danh sách các đường dẫn (paths), phương thức HTTP (GET, POST, PUT, DELETE), tham số truy vấn (parameters), cấu trúc dữ liệu yêu cầu (request body) và kiểu dữ liệu mong đợi của phản hồi (response schemas).

### 5. Endpoint `/api/tags/` và `/api/correspondents/` được điều hướng và xử lý bởi những lớp mã nguồn nào?
- **Trả lời:** Được điều hướng tại [src/documents/urls.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/urls.py) thông qua `DefaultRouter`. Xử lý nghiệp vụ chính là `TagViewSet` và `CorrespondentViewSet` tại [src/documents/views.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/views.py). Việc chuyển đổi và xác thực dữ liệu JSON do `TagSerializer` và `CorrespondentSerializer` tại [src/documents/serialisers.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/serialisers.py) đảm nhiệm.

### 6. Sự khác nhau giữa HTTP 400 và HTTP 500 trong kết quả kiểm thử API là gì? Lỗi nào mới là bug của hệ thống?
- **Trả lời:** 
  - `HTTP 400 (Bad Request)`: Là phản hồi **hợp lệ và đúng đắn** của máy chủ khi client gửi dữ liệu sai định dạng (ví dụ thiếu trường bắt buộc, tên quá dài). Máy chủ đã bẫy lỗi thành công và từ chối request một cách lịch sự.
  - `HTTP 500 (Internal Server Error)`: Là **bug nghiêm trọng của hệ thống**. Nó xảy ra khi code máy chủ gặp một ngoại lệ chưa được bẫy (`Unhandled Exception` như `TypeError`, `ValueError`, `IndexError`), làm crash tiến trình xử lý và trả về trang lỗi sập nguồn. Tiêu chuẩn API RESTful nghiêm cấm việc để lộ lỗi 500 khi client gửi payload không hợp lệ.

### 7. Bạn hãy giải thích nguyên nhân gốc rễ của lỗi `BUG-01` (Lỗi 500 trên trường `set_permissions`)?
- **Trả lời:** Lỗi xảy ra tại file [src/documents/serialisers.py:241](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/serialisers.py#L241) trong hàm `validate_set_permissions()`. Lập trình viên viết dòng lệnh: `if "users" in set_permissions[action]:` mà giả định rằng `set_permissions[action]` luôn là một `dict`. Khi Schemathesis gửi payload chứa giá trị kiểu boolean như `{"view": false}`, toán tử `in` trong Python ném ra ngoại lệ `TypeError: argument of type 'bool' is not a container or iterable`. Do không có khối `try...except` hoặc kiểm tra `isinstance(..., dict)`, lỗi này thoát ra ngoài tầng view và biến thành HTTP 500.

### 8. Lỗi `BUG-02` (Lỗi 500 trên tham số `modified__year`) xảy ra ở tầng nào trong kiến trúc?
- **Trả lời:** Lỗi xảy ra ở tầng cơ sở dữ liệu / ORM compiler ([src/documents/filters.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/filters.py) kết hợp với `django.db.backends.base.operations`). Khi client truyền số thực âm `-1.17e-38`, giá trị bị ép về số nguyên `0`. Khi Django ORM gọi `datetime.datetime(value, 1, 1)` để xây dựng câu lệnh SQL tìm kiếm mốc thời gian, module datetime của Python ném lỗi `ValueError: year must be in 1..9999, not 0`. Vì bộ lọc `django-filter` không khai báo ràng buộc `min_value=1, max_value=9999`, ngoại lệ này không được bẫy ở tầng HTTP request.

### 9. Lỗi `BUG-03` vi phạm schema (Schema Violation) nghĩa là gì? Tại sao API trả về 201 Created mà vẫn bị coi là lỗi?
- **Trả lời:** Trong Schema-based testing, kiểm thử dựa trên nguyên tắc "hợp đồng giao tiếp" (API Contract). Trong tài liệu OpenAPI `/api/schema/`, hệ thống cam kết với client rằng mọi phản hồi `201 Created` của đối tượng Correspondent đều sẽ có đủ các trường bắt buộc gồm: `document_count`, `last_correspondence`, `permissions`. Tuy nhiên thực tế khi tạo mới, Django REST Framework chỉ trả về đối tượng cơ bản vừa lưu trong DB và bỏ quên các trường tính toán này. Đây là lỗi **không nhất quán giữa tài liệu đặc tả và mã nguồn thực tế** (Contract Inconsistency).

### 10. Tại sao nhóm phải sử dụng một seed ngẫu nhiên cố định (Seed 202) khi chạy Schemathesis?
- **Trả lời:** Trong kiểm thử phần mềm, tính **tái lập (Reproducibility)** là yếu tố sống còn. Schemathesis sử dụng các thuật toán sinh dữ liệu ngẫu nhiên dựa trên thư viện Hypothesis. Nếu không cố định seed, mỗi lần chạy sẽ sinh ra các bộ dữ liệu khác nhau và khi phát hiện lỗi, ta không thể tái hiện lại chính xác chuỗi thao tác dẫn đến lỗi. Việc ghim `seed 202` (mã số của TV2) đảm bảo rằng bất kỳ ai chạy lại lệnh test với seed 202 cũng sẽ sinh ra đúng 100% các ca kiểm thử và bắt được đúng các lỗi như báo cáo.

### 11. Các ràng buộc toàn vẹn của Model `Tag` được định nghĩa ở đâu và gồm những gì?
- **Trả lời:** Được định nghĩa tại [src/documents/models.py:102-140](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/models.py#L102-L140). Bao gồm:
  - Trường `name`: Tối đa 128 ký tự, bắt buộc.
  - Ràng buộc duy nhất `UniqueConstraint(fields=["name", "owner"])`: Hai tag cùng một chủ sở hữu không được trùng tên.
  - Trường `color`: Mã màu HEX, tối đa 7 ký tự (mặc định `#a6cee3`).
  - Phân cấp cây `TreeNodeModel`: Giới hạn độ sâu tối đa 5 tầng (`MAX_NESTING_DEPTH = 5`) và hàm `clean()` cấm tag tự nhận mình làm cha (Self-parenting).

### 12. Khi nào thì một tài liệu được tự động gắn Tag (Matching Algorithm)?
- **Trả lời:** Khi tài liệu được Celery consumer xử lý xong bước OCR, hệ thống sẽ chạy logic matching tại `src/documents/matching.py`. Nếu một Tag có cấu hình `matching_algorithm`:
  - `1 (Any word)`: Văn bản chứa bất kỳ từ nào trong chuỗi match.
  - `2 (All words)`: Văn bản phải chứa tất cả các từ trong chuỗi match.
  - `3 (Exact match)`: Khớp chính xác cụm từ.
  - `4 (Regex)`: Khớp theo biểu thức chính quy.
  - `6 (Auto)`: Khớp tự động bằng thuật toán học máy (Naive Bayes classifier) dựa trên các tài liệu đã gắn nhãn trước đó.
  Nếu thỏa mãn, ID của Tag sẽ được tự động thêm vào quan hệ Many-to-Many `document.tags`.

### 13. Phân biệt sự khác nhau giữa Vòng 1, Vòng 2 và Vòng 3 trong chiến lược kiểm thử của nhóm?
- **Trả lời:**
  - *Vòng 1 (Read-only / Sanity check):* Chỉ kiểm thử phương thức an toàn `GET` (`--include-method GET`), đảm bảo toàn bộ hệ thống đọc dữ liệu và tìm kiếm ổn định, không làm biến đổi trạng thái DB.
  - *Vòng 2 (Write operations trên metadata):* Kiểm thử các phương thức ghi (`POST`, `PUT`, `PATCH`, `DELETE`) trên 3 tài nguyên danh mục nhẹ: `tags`, `correspondents`, `document_types`.
  - *Vòng 3 (Comprehensive / Stress testing):* Mở rộng kiểm thử sang toàn bộ tài nguyên cốt lõi bao gồm cả `documents` và bật tất cả các cơ chế kiểm tra nâng cao (`--checks all`), kiểm tra sâu về tính xác thực, tính tương thích header và vi phạm schema.

### 14. Tại sao trước mỗi vòng kiểm thử (hoặc sau khi Schemathesis chạy xong), nhóm bắt buộc phải chạy script reset và seed dữ liệu?
- **Trả lời:** Các bài kiểm thử ghi (`POST`, `DELETE`, `PUT`) của Schemathesis sẽ tạo ra hàng trăm bản ghi rác hoặc xóa mất các dữ liệu mẫu đã có sẵn trong cơ sở dữ liệu. Nếu không dọn dẹp và nạp lại dữ liệu chuẩn (seed 202), các ca kiểm thử sau sẽ bị ảnh hưởng bởi trạng thái ô nhiễm của dữ liệu trước đó (State Pollution), dẫn đến các lỗi giả (Flaky tests). Script `reset_data.py` và `seed_data.py` đưa hệ thống về đúng trạng thái ban đầu để đảm bảo tính độc lập giữa các vòng test.

### 15. Nếu được giao nhiệm vụ vá lỗi (Fix bug) cho Paperless-ngx dựa trên kết quả kiểm thử, bạn sẽ sửa những chỗ nào đầu tiên?
- **Trả lời:** Em sẽ ưu tiên vá 2 lỗi mức độ nghiêm trọng nhất (HTTP 500):
  1. Trong file `src/documents/serialisers.py:240`: Thêm câu lệnh kiểm tra kiểu `if not isinstance(set_permissions[action], dict): raise serializers.ValidationError(...)` để chặn đứng lỗi sập server `TypeError`.
  2. Trong file `src/documents/filters.py`: Đặt giới hạn `min_value=1, max_value=9999` cho bộ lọc `modified__year` để ngăn chặn số âm hoặc số quá lớn truyền vào hàm `datetime.datetime` của Django ORM.
  3. Cập nhật lại decorator `@extend_schema` cho `create()` của ViewSet để schema phản ánh đúng các trường có mặt trong response 201.
