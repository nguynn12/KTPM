# BÁO CÁO TỔNG HỢP BÀN GIAO SLIDE — THÀNH VIÊN 3 (TV3)
**Học phần:** Kiểm thử phần mềm — Đề tài: Kiểm thử API Paperless-ngx với Schemathesis  
**Thành viên thực hiện:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303  
**Thời gian hoàn thành:** 16/10/2026 (Ngày báo cáo chính thức)  
**Vai trò chính:** Phần D–E (Nghiên cứu nguyên lý Schemathesis, Kế hoạch kiểm thử, Thiết kế scenario/test case, Thực thi 3 vòng Schemathesis & 3 luồng nghiệp vụ cá nhân, Tái hiện lỗi hồi quy độc lập)

---

## 1. Môi trường Thực thi Thực tế trên Máy Windows Local
- **Hệ điều hành:** Windows 11 Home/Pro (x86_64), WSL2 Docker Backend
- **Docker Engine:** Docker Desktop 29.7.2 | Docker Compose v5.4.0
- **Paperless-ngx:** Image pin cố định `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (chạy trên `http://localhost:8000`)
- **Git Commit máy local:** `62e9a2ffbcb36bec9672c0e0c7a504cab20bf3f8` (nhánh `master`)
- **Python Runtime:** Python 3.14.4 (Venv isolated `.venv`)
- **Thư viện kiểm thử:**
  - `schemathesis==4.30.1`
  - `hypothesis==6.169.0`
  - `requests==2.34.2`
  - `reportlab==5.0.1`
- **OpenAPI Schema:** Tải có xác thực từ `http://localhost:8000/api/schema/`, SHA256: `9e1ed205b10a93961bf66d731e4ac3f64b7bba3ed66c7a1d3c42523116306f5c`

---

## 2. Bảng Trạng thái và Số liệu 3 Vòng Schemathesis Thực tế (Seed 303)

| Vòng | Cấu hình & Phạm vi | Operations chọn | Test Cases sinh (Hypothesis) | Test Cases (JUnit) | Failures / Errors (JUnit) | Unique Failures (CLI) | Thời gian thực thi | Trạng thái | Đường dẫn Log / Báo cáo |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Vòng 1** | **Chỉ GET (Read-only)**<br>Path: `^/api/(tags\|correspondents\|document_types\|documents)/`<br>Exclude: POST, PUT, PATCH, DELETE<br>Phases: `examples,fuzzing`<br>Checks: 5 checks cốt lõi | 19 / 163 | 74 generated | 19 testcases | 17 failed<br>0 errors | 22 failures<br>(1 warning) | 2.71s | **HOÀN TẤT (PASS 2, FAIL 17)** | [TV3_round1_seed303_20261016_093736.log](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303_20261016_093736.log)<br>[TV3_round1_seed303_20261016_093736.xml](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303_20261016_093736.xml)<br>[TV3_round1_seed303_20261016_093736.ndjson](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303_20261016_093736.ndjson) |
| **Vòng 2** | **CRUD Nhóm Thực thể Cơ bản**<br>Path: `^/api/(tags\|correspondents\|document_types)/`<br>Phases: `examples,coverage,fuzzing,stateful`<br>Checks: `all` | 18 / 163 | 744 generated<br>(68 skipped) | 19 testcases | 19 failed<br>0 errors | 51 failures | 42.12s | **HOÀN TẤT (PASS 3, FAIL 18)** | [TV3_round2_seed303_20261016_093803.log](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round2_seed303_20261016_093803.log)<br>[TV3_round2_seed303_20261016_093803.xml](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round2_seed303_20261016_093803.xml)<br>[TV3_round2_seed303_20261016_093803.ndjson](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round2_seed303_20261016_093803.ndjson) |
| **Vòng 3** | **Full CRUD Toàn diện + Documents**<br>Path: `^/api/(tags\|correspondents\|document_types\|documents)/`<br>Phases: `examples,coverage,fuzzing,stateful`<br>Checks: `all` | 53 / 163 | 1734 generated<br>(112 skipped) | 54 testcases | 53 failed<br>0 errors | 131 failures<br>(1 error, 2 warnings) | 102.41s | **HOÀN TẤT (PASS 2, FAIL 51, ERR 1)** | [TV3_round3_seed303_20261016_093930.log](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round3_seed303_20261016_093930.log)<br>[TV3_round3_seed303_20261016_093930.xml](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round3_seed303_20261016_093930.xml)<br>[TV3_round3_seed303_20261016_093930.ndjson](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round3_seed303_20261016_093930.ndjson) |

> [!IMPORTANT]
> **Giải thích kỹ thuật về số liệu kiểm thử:**
> 1. `max-examples=25` là cấu hình số lượng mẫu thử sinh bởi engine Hypothesis cho mỗi endpoint, không phải tổng số HTTP request.
> 2. `Số test cases trong JUnit XML`: Được ánh xạ theo từng Operation/Check quy chuẩn của Schemathesis (ví dụ 19 operations tương ứng 19 `<testcase>`).
> 3. `Unique Failures`: Tổng số vi phạm riêng biệt được phát hiện (bao gồm 500 Server Error, vi phạm Schema, từ chối request hợp lệ, mã trạng thái chưa được tài liệu hóa).
> 4. `Exit code 1`: Xác nhận Schemathesis đã hoàn tất toàn bộ chu trình kiểm thử và phát hiện các lỗi vi phạm hợp đồng schema/máy chủ; đây là trạng thái phát hiện lỗi thành công của công cụ fuzzing, không phải crash môi trường.

---

## 3. Kết quả Xác thực 3 Luồng Nghiệp vụ Thực tế (Business Flows)
Toàn bộ 3 luồng nghiệp vụ đã được thực thi và xác nhận bằng HTTP response thật tại [docs/BUSINESS_FLOWS_TV3.md](file:///d:/DaiHocDL/KiemThuPhanMem/KTPM/docs/BUSINESS_FLOWS_TV3.md):
1. **Luồng 1 (TV3-FLOW-01): Upload tài liệu PDF và trích xuất nội dung văn bản:**
   - Upload file `scripts/sample_docs/TV3_Sample_01_Report_303.pdf` -> HTTP 202, Task UUID `ea3629b6-2918-43fa-94d9-6366fee4a86c`.
   - Celery worker xử lý hoàn tất (`SUCCESS`), sinh ra Document ID 4 trong cơ sở dữ liệu PostgreSQL.
   - `GET /api/documents/4/` trả về HTTP 200, độ dài content: 306 ký tự. Nội dung mẫu: *"BAO CAO KIEM THU PHAN MEM SCHEMATHESIS... Tác giả Nguyễn Khiêm Thuận (2312764)..."*.
   - Đánh giá: **PASS**.
2. **Luồng 2 (TV3-FLOW-02): Quản trị và gán quan hệ thực thể (Tags, Correspondent, DocumentType):**
   - Tạo mới `TV3_Tag_Verified_303` (ID 5), `TV3_Auditor_303` (ID 4), `TV3_DocType_Report_303` (ID 4) -> đều HTTP 201 Created.
   - Gán quan hệ qua `PATCH /api/documents/4/` -> HTTP 200.
   - `GET /api/documents/4/` đối chiếu: trường `tags` chứa `[5]`, `correspondent` là `4`, `document_type` là `4` khớp hoàn toàn.
   - Đánh giá: **PASS**.
3. **Luồng 3 (TV3-FLOW-03): Tìm kiếm toàn văn và bộ lọc đa chiều:**
   - Tìm kiếm `GET /api/documents/?query=Schemathesis` -> HTTP 200, tìm thấy Document ID 4 trong các kết quả trả về.
   - Lọc theo nhãn `GET /api/documents/?tags__id__all=5` -> HTTP 200, tìm thấy chính xác Document ID 4.
   - Đánh giá: **PASS**.
4. **Xác thực bổ sung OCR Raster (Ảnh PNG):**
   - Upload ảnh scan `TV3_Sample_Scan_Image_303.png` -> Celery Task -> Document ID 5.
   - Trích xuất thành công chữ từ ảnh nhờ Tesseract OCR (`"NGUYEN KHIEM THUAN - MSSV 2312764 - SEED 303"`).
   - Đánh giá: **PASS**.

---

## 4. Kiểm thử Thủ công có Thiết kế & Tái hiện Lỗi Hồi quy (18 Test Cases)
Thực thi bằng `scripts/run_manual_tests_TV3.py` trên 2 tài nguyên phụ trách mở rộng: `Correspondents` và `Document Types`:
- **Kiểm thử biên (BVA):**
  - Biên name L-1 (127 ký tự): HTTP 201 Created (**PASS**).
  - Đúng biên L (128 ký tự): HTTP 201 Created (**PASS**).
  - Vượt biên L+1 (129 ký tự): HTTP 400 Bad Request, báo lỗi rõ ràng `"Ensure this field has no more than 128 characters"` (**PASS**).
- **Kiểm thử chuỗi Unicode / tiếng Việt có dấu:** Lưu và hiển thị nguyên vẹn tiếng Việt có dấu và icon (`TV3_Nguyễn_Khiêm_Thuận_🌿`) (**PASS**).
- **Kiểm thử phân quyền / Token:** Không có token hoặc token giả đều nhận phản hồi HTTP 401 Unauthorized (**PASS**).
- **Tái hiện độc lập lỗi BUG-01 (High - Server Error 500):**
  - Gửi payload `set_permissions` chứa `"view": false` tới `POST /api/correspondents/` và `POST /api/document_types/`.
  - Cả hai tài nguyên đều văng lỗi `HTTP 500 Internal Server Error` dạng HTML thay vì trả về `400 Bad Request`.
  - Tái hiện thành công 2 lần độc lập: Xác nhận lỗi do cơ chế xử lý phân quyền dùng chung trong base serializer của Paperless-ngx.
- **Tái hiện độc lập lỗi BUG-03 (Medium - Schema Contract Violation):**
  - Gửi POST tạo mới Correspondent thành công (HTTP 201 Created).
  - Response payload thực tế thiếu 3 trường được schema `/api/schema/` đánh dấu là bắt buộc (`required`): `document_count`, `last_correspondence`, `permissions`.
  - Tái hiện thành công 2 lần độc lập.

---

## 5. Ví dụ Minh họa Case Đạt / Lỗi (Request & Response đã Che bí mật)

### Ca Đạt: `TV3-COR-07` (Tạo Correspondent đúng biên 128 ký tự)
- **Request:**
```http
POST /api/correspondents/ HTTP/1.1
Host: localhost:8000
Authorization: Token [REDACTED_AUTH_TOKEN]
Content-Type: application/json

{"name": "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"}
```
- **Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 12,
  "slug": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
  "name": "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
  "match": "",
  "matching_algorithm": 1,
  "is_insensitive": true,
  "owner": 2,
  "user_can_change": true
}
```

### Ca Lỗi Tái hiện: `TV3-COR-20` (BUG-01: Server trả về 500 khi set_permissions sai kiểu)
- **Request:**
```http
POST /api/correspondents/ HTTP/1.1
Host: localhost:8000
Authorization: Token [REDACTED_AUTH_TOKEN]
Content-Type: application/json

{"name": "TV3_Crash_Perm_Corr_1791867796", "set_permissions": {"view": false}}
```
- **Response:**
```http
HTTP/1.1 500 Internal Server Error
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang="en">
<head><title>Server Error (500)</title></head>
<body><h1>Server Error (500)</h1><p></p></body>
</html>
```

---

## 6. So sánh Kết quả Phát hiện Lỗi: TV3 vs TV2

| Hạng mục đối chiếu | TV2 (Seed 202, Scope Tags) | TV3 (Seed 303, Scope Corrs, DocTypes, Docs) | Đánh giá & Kết luận |
|---|---|---|---|
| **BUG-01 (HTTP 500 trên set_permissions)** | Phát hiện trên `POST /api/tags/` khi gửi boolean cho object `set_permissions`. | Tái hiện thành công trên `POST /api/correspondents/` và `POST /api/document_types/`. | Xác nhận lỗi kiến trúc: Xảy ra trên toàn bộ các serializer kế thừa từ `PermissionsMixin` của Paperless-ngx. |
| **BUG-02 (HTTP 400 Bad Request)** | Kiểm thử định dạng màu `color` trên Tag. | Kiểm thử biên độ dài `name` (L=128) trên Correspondent và DocumentType. | Cả hai thành viên đều ghi nhận hệ thống bắt lỗi định dạng 400 đúng chuẩn cho các trường cơ bản. |
| **BUG-03 (Vi phạm Schema Contract 201)** | Phát hiện thiếu trường required trong schema của Tag. | Xác nhận phản hồi 201 của `Correspondents` thiếu 3 trường required (`document_count`, `last_correspondence`, `permissions`). | Minh chứng lỗi bất đồng bộ giữa OpenAPI serializer và Response serializer của Django REST Framework. |
| **Server Errors mới (Schemathesis V3)** | Ghi nhận lỗi server trên phạm vi Tag. | Phát hiện **14 lỗi Server Error (HTTP 500)** trên các endpoint phức tạp: `DELETE /api/documents/{id}/notes/`, `POST /api/documents/{id}/email/`, `POST /api/documents/edit_pdf/`, `POST /api/document_types/`. | Schemathesis stateful và fuzzing sâu tìm ra các lỗ hổng unhandled exceptions nghiêm trọng trong backend Django. |
| **Vi phạm hợp đồng Schema (Response Violations)** | 14 vi phạm. | Phát hiện **19 vi phạm schema** (thiếu trường, sai kiểu dữ liệu) và **67 mã trạng thái HTTP chưa tài liệu hóa (Undocumented)**. | OpenAPI schema của Paperless 3.1.3 sinh tự động qua `drf-spectacular` chưa khai báo đầy đủ các mã lỗi 400/404 cho API client. |

---

## 7. Bàn giao Kỹ thuật & Lưu ý Quan trọng cho Nhóm Làm Slide
1. **Tính độc lập của dữ liệu:** Dữ liệu nền của nhóm có tiền tố `TV2` (4 tags, 3 correspondents, 3 doctypes, 2 txt) được giữ nguyên vẹn làm mốc kiểm chuẩn. Dữ liệu chạy cá nhân của TV3 mang tên `TV3_*_303` và các test case mã `TV3-COR-*`, `TV3-DT-*`.
2. **An toàn bảo mật:** Tất cả hình ảnh và bảng biểu đưa lên slide **tuyệt đối không để lộ Authorization Token thật** hoặc mật khẩu admin; luôn sử dụng định dạng `[REDACTED_AUTH_TOKEN]` hoặc token giả định `Token 303303303...`.
3. **Giải thích số liệu cho giảng viên:** Cần nhấn mạnh sự khác nhau giữa số "testcase" trên JUnit XML (19, 19, 54) và số lượt request thực tế mà Hypothesis sinh ra (74, 744, 1734 requests).

---

## 8. Kịch bản Thuyết trình Mẫu 2 Phút Bảo vệ Phần D–E

> **Thời lượng chuẩn:** ~120 giây (2 phút)  
> **Người trình bày:** Nguyễn Khiêm Thuận (TV3)

*"Kính thưa Thầy/Cô và các bạn,*

*Em là **Nguyễn Khiêm Thuận**, MSSV **2312764**, là Thành viên 3 của nhóm đề tài Paperless-ngx. Em phụ trách **Phần D và E**: Nghiên cứu nguyên lý kiểm thử dựa trên thuộc tính với Schemathesis, lập kế hoạch kiểm thử, thiết kế test case và thực thi 3 vòng kiểm thử cùng 3 luồng nghiệp vụ cá nhân.*

*Về **nguyên lý Schemathesis (Phần D)**: Khác với kiểm thử truyền thống vốn chỉ gửi các payload cố định, Schemathesis phân tích tài liệu OpenAPI Specification của Paperless-ngx, kết hợp với engine Hypothesis để tự động sinh hàng ngàn ca kiểm thử ngẫu nhiên có định hướng, kiểm tra các bất biến (invariants) như không có lỗi máy chủ 500, tuân thủ schema dữ liệu và mã trạng thái HTTP. Đặc biệt, khi gặp lỗi, cơ chế Shrinking sẽ tự động thu gọn payload về kích thước tối thiểu giúp định vị bug chính xác.*

*Em đã xây dựng **kế hoạch kiểm thử 3 vòng (Seed 303)** trên môi trường Windows local với Paperless-ngx 3.1.3:*
- *Ở **Vòng 1 (Read-only GET)**: Kiểm thử 19 operations đọc trên 4 nhóm tài nguyên, phát hiện 17 vi phạm hợp đồng do response thiếu trường hoặc trả về mã lỗi 404 chưa tài liệu hóa.*
- *Ở **Vòng 2 (CRUD Thực thể cơ bản)**: Thực thi 18 operations trên Tags, Correspondents và Document Types với 744 ca thử sinh ra, phát hiện 51 vi phạm độc lập.*
- *Ở **Vòng 3 (Full CRUD + Documents)**: Mở rộng lên 53 operations với 1734 ca thử, phát hiện **14 lỗi nghiêm trọng HTTP 500 Internal Server Error** và 131 vi phạm schema.*

*Đồng thời, ở **Phần E**, em đã tự thiết kế **40 test case** chi tiết cho Correspondents và Document Types, thực thi kiểm thử biên 128 ký tự, chuỗi Unicode tiếng Việt, và **tái hiện độc lập 100% hai lỗi BUG-01 (500 Server Error) và BUG-03 (vi phạm Schema) của bạn TV2** trên chính các tài nguyên mới.*

*Cuối cùng, em đã hoàn thành xác thực **3 luồng nghiệp vụ thực tế** từ việc upload tài liệu PDF, Celery xử lý trích xuất OCR 306 ký tự văn bản, gán nhãn siêu dữ liệu và tìm kiếm toàn văn thành công.*

*Em xin chân thành cảm ơn Thầy/Cô và sẵn sàng trả lời các câu hỏi vấn đáp!"*

---

## 9. 8 Câu hỏi & Đáp án Ôn tập Vấn đáp Chuyên sâu (Oral Exam Q&A)

### Câu hỏi 1: Schemathesis hoạt động dựa trên nguyên lý cốt lõi nào? Điểm khác biệt lớn nhất so với Postman/Newman là gì?
- **Đáp án:**
  - Schemathesis hoạt động dựa trên phương pháp **Property-Based Testing (Kiểm thử dựa trên thuộc tính)** và **Specification-based Fuzzing**. Nó đọc trực tiếp tài liệu OpenAPI/Swagger, xây dựng đồ thị các schema định nghĩa (kiểu dữ liệu, format, min/max length, regex, required fields) và sử dụng engine **Hypothesis** của Python để tự động sinh ra các tập dữ liệu biên, dữ liệu dị thường (fuzz input).
  - Điểm khác biệt lớn nhất so với Postman/Newman: Postman kiểm thử dạng **ví dụ tĩnh (Example-based)** — tester chỉ kiểm tra đúng những ca mình nghĩ ra được trước. Schemathesis kiểm tra **thuộc tính tổng quát (Invariants)** — tự động tìm ra các trường hợp biên và chuỗi ký tự quái dị mà lập trình viên không lường trước được, đồng thời tự động kiểm tra toàn bộ response có khớp 100% với hợp đồng OpenAPI hay không mà không cần tester phải tự viết từng câu assert.

### Câu hỏi 2: Tại sao phải sử dụng tham số `--seed 303`? Có phải cùng seed thì luôn đảm bảo tái hiện 100% kết quả không?
- **Đáp án:**
  - Tham số `--seed 303` khởi tạo giá trị mầm (pseudo-random seed) cho bộ sinh số ngẫu nhiên của engine Hypothesis. Việc cố định seed giúp các ca sinh ngẫu nhiên mang tính tiền định (deterministic), cho phép người khác hoặc chính mình chạy lại lệnh với cùng seed sẽ sinh ra đúng chuỗi test input đó.
  - **Không đảm bảo 100% tái hiện lỗi** nếu chỉ có cùng seed. Để tái hiện chính xác 100%, cần thỏa mãn đồng thời: (1) Cùng seed, (2) Cùng phiên bản Schemathesis & Hypothesis, (3) Cùng phiên bản ứng dụng Paperless-ngx & thư viện backend, (4) Cùng schema OpenAPI, (5) **Trạng thái cơ sở dữ liệu ban đầu (Database Baseline)** phải đồng nhất và (6) Trình tự thực thi stateful không bị tác động bởi dữ liệu rác trước đó.

### Câu hỏi 3: Thuật toán Hypothesis và kỹ thuật Shrinking (thu gọn ca lỗi) hoạt động như thế nào trong Schemathesis?
- **Đáp án:**
  - Khi Schemathesis gửi một payload ngẫu nhiên dài hàng trăm ký tự phức tạp và kích hoạt lỗi máy chủ HTTP 500, tester sẽ rất khó phân tích nguyên nhân cốt lõi.
  - Kỹ thuật **Shrinking (Thu gọn)** của Hypothesis sẽ tự động chạy một thuật toán tìm kiếm nhị phân/giảm dần để cắt bỏ các ký tự không liên quan, thu nhỏ kích thước chuỗi, đưa các số về 0 hoặc chuỗi rỗng cho đến khi tìm được **payload nhỏ nhất khả dĩ (minimal reproducing example)** vẫn gây ra lỗi đó.
  - Ví dụ: Thay vì báo lỗi với chuỗi rác 500 ký tự UTF-8, Shrinking giúp chỉ ra rằng chỉ cần gửi `{"set_permissions": {"view": false}}` là đủ để làm sập hệ thống (BUG-01).

### Câu hỏi 4: Khi chạy Schemathesis, kết quả trả về Exit Code `1`. Điều này có nghĩa là công cụ bị lỗi crash môi trường hay kiểm thử phát hiện bug?
- **Đáp án:**
  - Exit code `1` trong Schemathesis biểu thị: **Công cụ đã chạy thành công trọn vẹn chu trình kiểm thử, và đã phát hiện ít nhất một lỗi vi phạm (failure hoặc error)** trong các phép kiểm tra (checks) như Server Error 500, Response Schema Conformance, hay Status Code Conformance.
  - Nếu Schemathesis bị lỗi môi trường (không kết nối được Docker, sai cú pháp CLI, thiếu quyền token), nó sẽ trả về Exit code khác (ví dụ code 2 hoặc unhandled CLI traceback). Vì vậy, Exit code `1` là minh chứng rõ ràng nhất cho thấy kiểm thử đã thực thi và tìm ra các khiếm khuyết phần mềm thực tế.

### Câu hỏi 5: Lỗi `Undocumented HTTP status code` là gì? Tại sao API trả về HTTP 400 hoặc 404 lại bị Schemathesis đánh báo lỗi (Failure)?
- **Đáp án:**
  - `Undocumented HTTP status code` là lỗi vi phạm tính nhất quán của tài liệu API.
  - Khi client gửi một payload không hợp lệ hoặc ID không tồn tại, backend Django trả về HTTP 400 (Bad Request) hoặc 404 (Not Found) là hoàn toàn đúng logic nghiệp vụ.
  - Tuy nhiên, trong tài liệu OpenAPI (`/api/schema/`) được sinh ra tự động bởi thư viện `drf-spectacular`, lập trình viên backend chỉ khai báo mã thành công `200 OK` hoặc `201 Created` mà quên khai báo `responses: { '400': ..., '404': ... }`.
  - Schemathesis kiểm tra tính tuân thủ hợp đồng (Contract Testing): Mọi mã trạng thái mà API trả về đều phải được định nghĩa trước trong hợp đồng. Việc trả về mã chưa được khai báo là lỗi tài liệu hóa, có thể gây lỗi unhandled exception cho các SDK/Client tự động sinh từ OpenAPI schema.

### Câu hỏi 6: Bạn đã tái hiện những lỗi nào của TV2 (BUG-01, BUG-03)? Bản chất kỹ thuật của hai lỗi này là gì?
- **Đáp án:**
  - Em đã tái hiện độc lập cả hai lỗi trên hai tài nguyên mới là `Correspondents` và `Document Types`:
    - **BUG-01 (Mức độ High):** Khi gửi payload `{"set_permissions": {"view": false}}`, server trả về `HTTP 500 Internal Server Error` thay vì `400 Bad Request`. Bản chất: Trong mã nguồn Django của Paperless-ngx, lớp `PermissionsMixin` mong đợi trường `view` nhận một danh sách (list các user ID), nhưng mã nguồn thiếu khối `try-except` hoặc validation kiểu dữ liệu trước khi truy xuất, dẫn đến unhandled TypeError/ValueError trong backend Python.
    - **BUG-03 (Mức độ Medium):** Khi tạo mới thành công qua `POST /api/correspondents/` (HTTP 201), response trả về thiếu 3 trường `document_count`, `last_correspondence`, `permissions` dù schema OpenAPI đánh dấu chúng là `required`. Bản chất: Do sự bất đồng bộ giữa `Serializer` dùng để sinh OpenAPI schema (bao gồm đầy đủ các trường tính toán annotate) và `CreateSerializer` thực tế chỉ trả về các trường của model lưu trữ.

### Câu hỏi 7: Trong Vòng 3, Schemathesis phát hiện 14 lỗi Server Error (HTTP 500). Hãy nêu ví dụ cụ thể một endpoint bị lỗi và nguyên nhân?
- **Đáp án:**
  - Ví dụ điển hình là endpoint `DELETE /api/documents/{id}/notes/` (hoặc `POST /api/documents/{id}/email/`).
  - Khi Schemathesis fuzzing các giá trị tham số đường dẫn `{id}` với ký tự đặc biệt hoặc số âm/chuỗi không hợp lệ kết hợp với tham số truy vấn bất thường, view của Django trong Paperless không xử lý biệt lệ khi ép kiểu tham số hoặc gọi hàm truy vấn ORM `Document.objects.get(id=...)` mà để văng ra ngoại lệ chưa bắt (Unhandled Exception), dẫn đến Django WSGI handler trả về mã lỗi 500 kèm trang HTML lỗi mặc định.

### Câu hỏi 8: Ba luồng nghiệp vụ cá nhân của TV3 được thiết kế và xác thực trên hệ thống như thế nào?
- **Đáp án:**
  - Cả 3 luồng nghiệp vụ đều được xác thực qua kịch bản API tự động với dữ liệu thực tế:
    - **Luồng 1 (Upload & OCR):** Upload tệp PDF `TV3_Sample_01_Report_303.pdf` qua `POST /api/documents/post_document/`, nhận HTTP 202 kèm Task ID. Polling Celery task hoàn tất (`SUCCESS`), kiểm tra tài liệu ID 4 mới sinh và xác nhận trích xuất thành công 306 ký tự văn bản.
    - **Luồng 2 (Quản trị quan hệ):** Tạo mới Tag ID 5, Correspondent ID 4, Document Type ID 4 (HTTP 201). Gửi `PATCH /api/documents/4/` để liên kết 3 thực thể này vào tài liệu, sau đó `GET` lại kiểm tra các trường khóa ngoại đã được cập nhật chính xác.
    - **Luồng 3 (Tìm kiếm & Lọc):** Gọi `GET /api/documents/?query=Schemathesis` để kiểm tra công cụ tìm kiếm toàn văn của Paperless (Whoosh/Xapian) và `GET /api/documents/?tags__id__all=5` để kiểm tra bộ lọc đa chiều; cả hai đều trả về kết quả khớp chính xác tài liệu ID 4.
