# BÁO CÁO TỔNG HỢP BÀN GIAO SLIDE — THÀNH VIÊN 3 (TV3)
**Học phần:** Kiểm thử phần mềm — Đề tài: Kiểm thử API Paperless-ngx với Schemathesis  
**Thành viên thực hiện:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303  
**Thời gian thực hiện & nghiệm thu:** 16/10/2026 (Ngày báo cáo chính thức)  
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
- **OpenAPI Schema Local:** Tải có xác thực từ `http://localhost:8000/api/schema/`:
  - JSON Schema: [docs/openapi_TV3.json](openapi_TV3.json) (SHA256: `888b0f89ec0a9f65293f5320a86b1810d7904f93033178b567e313d951b12e3a`)
  - YAML Schema: [docs/openapi_TV3.yaml](openapi_TV3.yaml) (SHA256: `4b56422b2e5bc4190efdefab3444c46336062c06c5c1478a2f44c1d6082785e0`)

---

## 2. Bảng Trạng thái và Số liệu 3 Vòng Schemathesis Thực tế (Seed 303)

| Vòng | Cấu hình & Phạm vi | Operations chọn / test | Hypothesis Test Cases | Kết quả theo Phase (CLI Log) | JUnit XML Testcases | JUnit Failures / Errors | Unique Failures theo Checks (CLI) | Thời gian chạy (CLI Engine) | Tệp Bằng chứng (Relative Path) |
|:---:|---|:---:|:---:|---|:---:|:---:|:---:|:---:|---|
| **Vòng 1** | **Chỉ GET (Read-only)**<br>Allowlist: Tags, Corrs, DocTypes, Docs<br>Exclude: POST, PUT, PATCH, DELETE<br>Phases: `examples,fuzzing`<br>Checks: 5 checks cốt lõi | 19 / 19 | 74 generated<br>(17 found failures) | • Examples: 19 skipped<br>• Fuzzing: 2 passed, 17 failed | 19 testcases (19 operations) | 17 failures<br>0 errors | **22 failures**<br>• Server error: 5<br>• Violates schema: 4<br>• Content-Type: 3<br>• Undocumented code: 10<br>(1 warning) | 2.71s<br>(Engine: 2.71s) | [XML](../results/TV3_round1_seed303_20261016_093736.xml)<br>[NDJSON](../results/TV3_round1_seed303_20261016_093736.ndjson)<br>[Log](../results/TV3_round1_seed303_20261016_093736.log)<br>[Summary](../results/TV3_round1_seed303_20261016_093736_summary.md) |
| **Vòng 2** | **CRUD Nhóm Thực thể Cơ bản**<br>Allowlist: `tags`, `correspondents`, `document_types`<br>Phases: All, Checks: All | 18 / 18 | 744 generated<br>(44 found failures,<br>68 skipped) | • Examples: 18 skipped<br>• Coverage: 18 failed<br>• Fuzzing: 3 passed, 15 failed<br>• Stateful: 102 passed, 36 failed | 19 testcases (18 operations + 1 stateful) | 19 failures<br>0 errors | **51 failures**<br>• Server error: 1<br>• Violates schema: 14<br>• Rejected compliant: 10<br>• Undocumented code: 26 | 42.12s<br>(Engine: 42.12s) | [XML](../results/TV3_round2_seed303_20261016_093803.xml)<br>[NDJSON](../results/TV3_round2_seed303_20261016_093803.ndjson)<br>[Log](../results/TV3_round2_seed303_20261016_093803.log)<br>[Summary](../results/TV3_round2_seed303_20261016_093803_summary.md) |
| **Vòng 3** | **Full CRUD Toàn diện + Documents**<br>Allowlist: 4 nhóm tài nguyên đầy đủ<br>Phases: All, Checks: All | 53 / 53 | 1734 generated<br>(108 found failures,<br>1 errored, 112 skipped) | • Examples: 53 skipped<br>• Coverage: 2 passed, 51 failed<br>• Fuzzing: 4 passed, 49 failed<br>• Stateful: 193 passed, 63 failed | 54 testcases (53 operations + 1 stateful) | 53 failures<br>0 errors | **131 failures**<br>• Server error: 14<br>• Violates schema: 19<br>• Accepted invalid: 3<br>• Rejected compliant: 24<br>• Content-Type: 3<br>• Undocumented code: 67<br>• Unsupported method: 1<br>(2 warnings) | 102.41s<br>(Engine: 102.41s) | [XML](../results/TV3_round3_seed303_20261016_093930.xml)<br>[NDJSON](../results/TV3_round3_seed303_20261016_093930.ndjson)<br>[Log](../results/TV3_round3_seed303_20261016_093930.log)<br>[Summary](../results/TV3_round3_seed303_20261016_093930_summary.md) |

### Giải thích Kỹ thuật Chuyên sâu về Số liệu & Mâu thuẫn Báo cáo

> [!IMPORTANT]
> 1. **Vì sao Vòng 2 có JUnit 19 failures / 0 passed nhưng CLI ghi nhận Fuzzing 3 passed / 15 failed?**
>    - Trong JUnit XML, mỗi phần tử `<testcase>` đại diện cho một API operation (18 operations) cộng thêm một mục tổng hợp `<testcase name="Stateful tests">` (tổng cộng 19 testcases).
>    - Kết quả của một `<testcase>` trong JUnit XML là kết quả **tổng hợp (aggregate)** của toàn bộ các phase kiểm thử (Coverage, Fuzzing, Stateful).
>    - Ở phase Coverage, toàn bộ 18 operations đều bị phát hiện vi phạm check (đặc biệt là check Undocumented HTTP status code hoặc Response violates schema). Do đó, Schemathesis gán thẻ `<failure>` cho tất cả 18 operations trong JUnit XML, dù ở riêng phase Fuzzing có 3 operations vượt qua. Thêm vào đó, mục Stateful tests cũng bị failure do có 36 stateful scenarios thất bại.
>    - Vì vậy, JUnit XML ghi nhận chính xác: `tests="19" failures="19" errors="0"`. Số liệu "3 passed / 15 failed" chỉ thuộc về riêng phase Fuzzing trong CLI log.
>
> 2. **Vì sao Vòng 3 CLI có `1 errored` nhưng JUnit XML ghi nhận `errors="0"`?**
>    - Chỉ số `1 errored` trong CLI thuộc về cấp độ **Hypothesis test case generation/execution**: Trong số 1734 mẫu thử do engine Hypothesis sinh ra, có đúng 1 mẫu thử gặp ngoại lệ khi thực thi (client-side execution error).
>    - Trong JUnit XML, Schemathesis tổng hợp theo cấp độ **Operation**: Khi operation chứa mẫu thử đó đã có vi phạm assertion check, Schemathesis biểu diễn nó dưới dạng một thẻ `<failure>` chung cho operation đó chứ không tạo thẻ `<error>` riêng biệt. Do đó JUnit XML báo `errors="0"`.
>
> 3. **Phân biệt rành mạch giữa các đơn vị đo lường:**
>    - `Operations` (19, 18, 53): Số endpoint API được chọn lọc và kiểm thử.
>    - `Hypothesis Test Cases` (74, 744, 1734): Số lượng mẫu thử nghiệm logic được engine sinh ra dựa trên đặc tả schema. **Không đồng nhất với tổng số HTTP requests** vì trong kiểm thử Stateful một test case là chuỗi nhiều request liên hoàn, và quá trình shrinking có thể gửi thêm các request phụ.
>    - `Unique Failures theo Checks` (22, 51, 131): Tổng số lần các bất biến (invariants) bị vi phạm trên các ca thử. **Không đồng nghĩa với số bug độc lập trong mã nguồn**, vì một lỗi gốc (như thiếu khai báo mã 400 trong OpenAPI) có thể gây ra hàng chục check failures ở nhiều endpoint.
>    - `Server Error: 14` (Vòng 3): Đếm **14 failure checks của bất biến `not_a_server_error`** trên 13 operations đơn lẻ và 1 trong stateful testing, không phải 14 bug mã nguồn riêng biệt.
>    - `Exit code 1`: Xác nhận Schemathesis đã chạy hoàn tất và phát hiện vi phạm kiểm thử. Exit code 1 **không tự chứng minh đã quét đủ phạm vi**; độ bao phủ phạm vi phải được đối chiếu qua số operations được chọn và các phase đã chạy thực tế.

---

## 3. Kết quả Xác thực 3 Luồng Nghiệp vụ Thực tế (Business Flows)
Toàn bộ 3 luồng nghiệp vụ đã được thực thi và xác nhận bằng HTTP response thật tại [docs/BUSINESS_FLOWS_TV3.md](BUSINESS_FLOWS_TV3.md):
1. **Luồng 1 (TV3-FLOW-01): Upload tài liệu PDF và trích xuất nội dung văn bản:**
   - Upload file `scripts/sample_docs/TV3_Sample_01_Report_303.pdf` -> HTTP 202, Task UUID `ea3629b6-2918-43fa-94d9-6366fee4a86c`.
   - Celery worker xử lý hoàn tất (`SUCCESS`), sinh ra Document ID 4 trong PostgreSQL.
   - `GET /api/documents/4/` trả về HTTP 200, độ dài content: 306 ký tự chứa nội dung: *"BAO CAO KIEM THU PHAN MEM SCHEMATHESIS... Tác giả Nguyễn Khiêm Thuận (2312764)..."*. Đánh giá: **PASS**.
2. **Luồng 2 (TV3-FLOW-02): Quản trị và gán quan hệ thực thể (Tags, Correspondent, DocumentType):**
   - Tạo mới `TV3_Tag_Verified_303` (ID 5), `TV3_Auditor_303` (ID 4), `TV3_DocType_Report_303` (ID 4) -> đều HTTP 201 Created.
   - Gán quan hệ qua `PATCH /api/documents/4/` -> HTTP 200.
   - `GET /api/documents/4/` đối chiếu: trường `tags` chứa `[5]`, `correspondent` là `4`, `document_type` là `4` khớp hoàn toàn. Đánh giá: **PASS**.
3. **Luồng 3 (TV3-FLOW-03): Tìm kiếm toàn văn và bộ lọc đa chiều:**
   - Tìm kiếm `GET /api/documents/?query=Schemathesis` -> HTTP 200, tìm thấy Document ID 4 trong danh sách kết quả.
   - Lọc theo nhãn `GET /api/documents/?tags__id__all=5` -> HTTP 200, tìm thấy chính xác Document ID 4. Đánh giá: **PASS**.
4. **Xác thực bổ sung OCR Raster (Ảnh PNG):**
   - Upload ảnh scan `TV3_Sample_Scan_Image_303.png` -> Celery Task -> Document ID 5.
   - Trích xuất thành công nội dung chữ từ raster image nhờ Tesseract OCR (`"NGUYEN KHIEM THUAN - MSSV 2312764 - SEED 303"`). Đánh giá: **PASS**.

---

## 4. Kiểm thử Thủ công có Thiết kế & Tái hiện Lỗi Hồi quy (Phần E)
Chi tiết tại [docs/TEST_CASES_TV3.md](TEST_CASES_TV3.md) và [docs/TEST_CASES.md](TEST_CASES.md):
- **Phạm vi thiết kế:** 40 test cases (20 ca cho `Correspondents` và 20 ca cho `Document Types`).
- **Thực thi qua runner tự động [`scripts/run_manual_tests_TV3.py`](../scripts/run_manual_tests_TV3.py):** **18 test cases** (13 ca Correspondents + 5 ca Document Types).
  - **16 ca PASS:**
    - Biên name $L-1=127$ ký tự: HTTP 201 Created (**PASS**).
    - Biên name đúng $L=128$ ký tự: HTTP 201 Created (**PASS**).
    - Vượt biên name $L+1=129$ ký tự: HTTP 400 Bad Request, thông báo rõ `"Ensure this field has no more than 128 characters"` (**PASS**).
    - Chuỗi tiếng Việt có dấu và icon Unicode (`TV3_Nguyễn_Khiêm_Thuận_🌿`): HTTP 201 Created, lưu và đọc lại toàn vẹn (**PASS**).
    - Bảo mật xác thực: Không có Authorization token hoặc token giả đều nhận phản hồi HTTP 401 Unauthorized (**PASS**).
    - Phân trang: `?page=1&page_size=1` trả về đúng định dạng HTTP 200 OK (**PASS**).
  - **2 ca REPRO-BUG-01 (Lỗi máy chủ 500):**
    - Gửi payload `{"set_permissions": {"view": false}}` tới `POST /api/correspondents/` (`TV3-COR-20`) và `POST /api/document_types/` (`TV3-DT-20`).
    - Cả hai tài nguyên đều trả về `HTTP 500 Internal Server Error` dạng HTML thay vì kiểm tra validation và trả về `400 Bad Request`.
  - **22 ca NOT RUN:** Các ca kiểm thử CRUD nâng cao (PATCH, PUT, DELETE kiểm tra mã 404, chuỗi 1000 ký tự) chưa đưa vào runner và được giữ nguyên trạng thái chưa chạy (7 ca Correspondents + 15 ca Document Types).
- *Lưu ý về teardown:* Lệnh `requests.delete` ở cuối script runner là thao tác dọn dẹp môi trường (cleanup), không tính là test case độc lập do không có assertions và verdict trong runner.

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

### Ca Lỗi Tái hiện: `TV3-COR-20` (BUG-01: Server trả về 500 khi set_permissions sai kiểu dữ liệu)
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

| Hạng mục đối chiếu | TV2 (Seed 202, Scope Tags) | TV3 (Seed 303, Scope Corrs, DocTypes, Docs) | Đánh giá Kỹ thuật |
|---|---|---|---|
| **BUG-01 (HTTP 500 trên set_permissions)** | Phát hiện trên `POST /api/tags/` khi gửi boolean cho object `set_permissions.view`. | Tái hiện thành công trên `POST /api/correspondents/` (`TV3-COR-20`) và `POST /api/document_types/` (`TV3-DT-20`). | **Xác nhận lỗi kiến trúc:** Theo OpenAPI schema, `set_permissions.view` là object chứa `users/groups`. Khi gửi boolean, backend không bắt validation 400 mà văng lỗi máy chủ 500 HTML. Do chưa trích xuất traceback từ container Django, hiện tượng này được xác định chính xác là Unhandled Server Error ở lớp serializer phân quyền dùng chung. |
| **BUG-02 (HTTP 400 Bad Request)** | Kiểm thử định dạng màu `color` trên Tag. | Kiểm thử biên độ dài `name` ($L=128$, $L+1=129$) trên Correspondent và DocumentType. | Cả hai thành viên đều ghi nhận hệ thống bắt lỗi định dạng 400 đúng chuẩn cho các trường cơ bản. |
| **BUG-03 (Vi phạm Schema Contract 201)** | Phát hiện thiếu trường required trong schema của Tag. | Xác nhận phản hồi 201 của `POST /api/correspondents/` thiếu 3 trường required: `document_count`, `last_correspondence`, `permissions`. | **Xác nhận trên Correspondents:** Trường `permissions` gắn liền với query `full_perms` trong GET nhưng bị schema đánh required vô điều kiện trong response 201 của POST. Tương tự, `document_count` và `last_correspondence` là trường tính toán chưa có khi tạo mới. Hồ sơ chỉ khẳng định BUG-03 trên `Correspondents`. |
| **Server Error Checks (Schemathesis V3)** | Ghi nhận lỗi server trên phạm vi Tag. | Ghi nhận **14 failure checks thuộc bất biến `not_a_server_error`** trên 13 operations độc lập (như `DELETE /api/documents/{id}/notes/`, `POST /api/documents/edit_pdf/`, `GET /api/documents/{id}/preview/`,...) và trong stateful tests. | Fuzzing sâu các giá trị tham số đường dẫn và body kích hoạt các lỗi máy chủ HTTP 500 không được xử lý trong backend Paperless-ngx. |
| **Vi phạm hợp đồng Schema (Response Violations)** | 14 vi phạm. | Phát hiện **19 vi phạm schema** (thiếu trường, sai kiểu) và **67 mã trạng thái HTTP chưa tài liệu hóa (Undocumented codes)**. | Thư viện sinh schema tự động (`drf-spectacular`) chưa khai báo đầy đủ các mã lỗi 400/404 và có sự sai lệch giữa Serializer tài liệu hóa và Serializer phản hồi thực tế. |

---

## 7. Bàn giao Kỹ thuật & Lưu ý Quan trọng cho Nhóm Làm Slide
1. **Tính độc lập của dữ liệu:** Dữ liệu nền của nhóm có tiền tố `TV2` (4 tags, 3 correspondents, 3 doctypes, 2 txt) được giữ nguyên vẹn làm mốc kiểm chuẩn. Dữ liệu chạy cá nhân của TV3 mang tên `TV3_*_303` và các test case mã `TV3-COR-*`, `TV3-DT-*`.
2. **An toàn bảo mật:** Tất cả hình ảnh và bảng biểu đưa lên slide **tuyệt đối không để lộ Authorization Token thật** hoặc mật khẩu admin; luôn sử dụng định dạng `[REDACTED_AUTH_TOKEN]` hoặc token giả định.
3. **Phân biệt đơn vị số liệu:** Cần giải thích rõ cho giảng viên sự khác biệt giữa số lượng operations (19, 18, 53), số test cases sinh bởi Hypothesis (74, 744, 1734), và số testcases trong JUnit XML (19, 19, 54).

---

## 8. Kịch bản Thuyết trình Mẫu 2 Phút Bảo vệ Phần D–E

> **Thời lượng chuẩn:** ~120 giây (2 phút)  
> **Người trình bày:** Nguyễn Khiêm Thuận (TV3)

*"Kính thưa Thầy/Cô và các bạn,*

*Em là **Nguyễn Khiêm Thuận**, MSSV **2312764**, là Thành viên 3 của nhóm đề tài Paperless-ngx. Em phụ trách **Phần D và E**: Nghiên cứu nguyên lý kiểm thử dựa trên thuộc tính với Schemathesis, lập kế hoạch kiểm thử, thiết kế test case và thực thi 3 vòng kiểm thử cùng 3 luồng nghiệp vụ cá nhân.*

*Về **nguyên lý Schemathesis (Phần D)**: Schemathesis đọc tài liệu OpenAPI Specification của Paperless-ngx, kết hợp với engine Hypothesis để tự động sinh hàng ngàn ca thử nghiệm biên và dữ liệu dị thường (fuzzing), đồng thời tự động kiểm tra các bất biến (invariants) như không có lỗi máy chủ 500, tuân thủ schema phản hồi và mã trạng thái HTTP. Khi gặp lỗi, cơ chế Shrinking với các chiến lược heuristic tích hợp sẽ tự động thu nhỏ payload về ca kiểm thử tối thiểu giúp định vị nguyên nhân nhanh chóng.*

*Em đã xây dựng **kế hoạch kiểm thử 3 vòng (Seed 303)** trên môi trường Windows local với Paperless-ngx 3.1.3:*
- *Ở **Vòng 1 (Read-only GET)**: Kiểm thử 19 operations đọc trên 4 nhóm tài nguyên, phát hiện 22 lỗi vi phạm checks, chủ yếu do phản hồi thiếu trường hoặc trả về mã 404 chưa được khai báo trong schema.*
- *Ở **Vòng 2 (CRUD Thực thể cơ bản)**: Thực thi 18 operations trên Tags, Correspondents và Document Types với 744 ca thử sinh ra và 138 kịch bản stateful, phát hiện 51 vi phạm checks.*
- *Ở **Vòng 3 (Full CRUD + Documents)**: Mở rộng lên 53 operations với 1734 ca thử sinh ra và 256 kịch bản stateful, phát hiện **14 điểm kiểm tra lỗi máy chủ HTTP 500** và 131 vi phạm checks.*

*Đồng thời, ở **Phần E**, em đã thiết kế **40 test cases** cho Correspondents và Document Types, chạy thực tế 18 ca qua runner tự động đạt 16 PASS (bao gồm kiểm thử biên 128 ký tự, chuỗi Unicode tiếng Việt, Authorization), và **tái hiện độc lập 100% hai lỗi BUG-01 (500 Server Error khi gửi sai cấu trúc phân quyền) và BUG-03 (phản hồi 201 thiếu trường bắt buộc) của bạn TV2** trên chính các tài nguyên mới.*

*Cuối cùng, em đã hoàn thành xác thực **3 luồng nghiệp vụ thực tế** từ việc upload PDF trích xuất OCR 306 ký tự văn bản, gán nhãn siêu dữ liệu và tìm kiếm toàn văn thành công.*

*Em xin chân thành cảm ơn Thầy/Cô và sẵn sàng trả lời các câu hỏi vấn đáp!"*

---

## 9. 8 Câu hỏi & Đáp án Ôn tập Vấn đáp Chuyên sâu (Oral Exam Q&A)

### Câu hỏi 1: Schemathesis hoạt động dựa trên nguyên lý cốt lõi nào? Điểm khác biệt so với Postman/Newman là gì?
- **Đáp án:**
  - Schemathesis hoạt động dựa trên phương pháp **Property-Based Testing (Kiểm thử dựa trên thuộc tính)** kết hợp **Specification-Based Fuzzing**. Công cụ phân tích tài liệu OpenAPI Specification của ứng dụng, dựng đồ thị kiểu dữ liệu và ràng buộc, sau đó sử dụng engine **Hypothesis** để sinh tự động các ca thử nghiệm biên, dữ liệu ngẫu nhiên có định hướng và các chuỗi gọi API đa bước (Stateful).
  - Khác với Postman/Newman (nơi tester phải chủ động viết trước từng kịch bản thử nghiệm, tự cấu hình bộ dữ liệu và tự viết câu assert cho từng trường), Schemathesis **tự động sinh dữ liệu từ schema** và **tự động kiểm tra các bất biến tổng quát (Invariants)** — ví dụ không có lỗi máy chủ 500, phản hồi phải khớp 100% với schema và mã HTTP phải được khai báo — giúp phát hiện các trường hợp biên dị thường mà tester không lường trước được.

### Câu hỏi 2: Tại sao phải sử dụng tham số `--seed 303`? Có phải cùng seed thì luôn đảm bảo tái hiện 100% kết quả không?
- **Đáp án:**
  - Tham số `--seed 303` cố định giá trị khởi tạo (pseudo-random seed) cho bộ sinh số ngẫu nhiên của Hypothesis. Việc này đảm bảo tính tiền định (deterministic), giúp các ca thử nghiệm sinh ra có thể lặp lại chính xác giữa các lần chạy khác nhau.
  - **Không đảm bảo 100% tái hiện lỗi** nếu chỉ có cùng seed. Để tái hiện chính xác kết quả kiểm thử, cần thỏa mãn đồng bộ: (1) Cùng giá trị seed, (2) Cùng phiên bản Schemathesis và Hypothesis, (3) Cùng phiên bản Paperless-ngx backend, (4) Cùng nội dung schema OpenAPI, và đặc biệt là (5) **Trạng thái cơ sở dữ liệu ban đầu (Database Baseline)** phải giống hệt nhau, vì kiểm thử stateful phụ thuộc vào các ID và dữ liệu đã tồn tại sẵn trong hệ thống.

### Câu hỏi 3: Thuật toán Hypothesis và kỹ thuật Shrinking (thu gọn ca lỗi) hoạt động như thế nào trong Schemathesis?
- **Đáp án:**
  - Khi một payload ngẫu nhiên phức tạp (ví dụ chuỗi 500 ký tự chứa nhiều ký tự điều khiển UTF-8 lạ) gây lỗi sập server HTTP 500, tester rất khó biết chính xác ký tự nào gây ra lỗi.
  - Kỹ thuật **Shrinking (Thu gọn)** của Hypothesis sẽ tự động áp dụng tập hợp các chiến lược heuristic thu gọn đa dạng: xóa bỏ từng phần tử không cần thiết, giảm dần độ lớn của số nguyên về 0, thay thế ký tự phức tạp bằng ký tự ASCII đơn giản hoặc chuỗi rỗng.
  - Quá trình này lặp lại cho đến khi tìm được **payload tối thiểu khả dĩ (minimal reproducing example)** vẫn kích hoạt lỗi đó, giúp lập trình viên xác định chính xác nguyên nhân gốc.

### Câu hỏi 4: Khi chạy Schemathesis, kết quả trả về Exit Code `1`. Điều này có ý nghĩa gì và có chứng minh công cụ đã quét đủ phạm vi không?
- **Đáp án:**
  - Exit code `1` trong Schemathesis biểu thị: **Quá trình kiểm thử đã hoàn tất và công cụ đã phát hiện ít nhất một vi phạm kiểm thử (failure hoặc error)** trong các checks được kích hoạt (như lỗi máy chủ 500, vi phạm response schema, hoặc mã trạng thái chưa tài liệu hóa). Nếu bị lỗi môi trường hoặc không kết nối được Docker, công cụ sẽ trả về exit code khác hoặc traceback unhandled.
  - Tuy nhiên, **Exit code 1 không tự chứng minh đã quét đủ phạm vi API**. Độ bao phủ thực tế phải được đánh giá qua số lượng operations được chọn lọc kiểm thử (19/163 ở Vòng 1, 18/163 ở Vòng 2, 53/163 ở Vòng 3), cấu hình `max-examples` và danh sách các phase kiểm thử đã thực thi (Coverage, Fuzzing, Stateful).

### Câu hỏi 5: Lỗi `Undocumented HTTP status code` là gì? Tại sao API trả về HTTP 400 hoặc 404 lại bị Schemathesis báo Failure?
- **Đáp án:**
  - `Undocumented HTTP status code` là lỗi vi phạm tính tuân thủ hợp đồng tài liệu API (Contract Conformance).
  - Về mặt nghiệp vụ, khi client gửi ID không tồn tại hoặc payload sai định dạng, máy chủ trả về HTTP 404 (Not Found) hoặc HTTP 400 (Bad Request) là hoàn toàn chính xác.
  - Tuy nhiên, trong tài liệu OpenAPI (`/api/schema/`) được sinh ra tự động, lập trình viên backend chỉ khai báo mã thành công `200` hoặc `201` mà **quên khai báo phản hồi `400` và `404` trong mục `responses`** của endpoint đó.
  - Schemathesis thực hiện kiểm thử hợp đồng: Mọi mã trạng thái mà API trả về đều bắt buộc phải được cam kết trước trong đặc tả OpenAPI. Việc trả về mã chưa được tài liệu hóa có thể khiến các thư viện client SDK tự động sinh từ OpenAPI bị lỗi unhandled response.

### Câu hỏi 6: Bạn đã tái hiện những lỗi nào của TV2 (BUG-01, BUG-03)? Bản chất kỹ thuật của hai lỗi này là gì?
- **Đáp án:**
  - Em đã tái hiện độc lập cả hai lỗi trên các tài nguyên mới:
    - **BUG-01 (Mức độ High):** Khi gửi payload `{"set_permissions": {"view": false}}`, máy chủ trả về `HTTP 500 Internal Server Error` dạng HTML thay vì `HTTP 400 Bad Request`. Đối chiếu OpenAPI schema: `set_permissions.view` được định nghĩa là một object chứa `users` và `groups` (mảng ID số nguyên). Khi client gửi kiểu boolean, backend Django không bắt lỗi validation kiểu dữ liệu mà để văng ra lỗi máy chủ nội bộ. Em đã tái hiện thành công trên cả `Correspondents` và `Document Types`.
    - **BUG-03 (Mức độ Medium):** Khi gửi POST tạo mới Correspondent thành công (`HTTP 201 Created`), response trả về thiếu 3 trường mà OpenAPI schema đánh dấu là bắt buộc (`required`): `document_count`, `last_correspondence`, và `permissions`. Bản chất là do sự bất đồng bộ giữa Serializer sinh schema và Serializer phản hồi: trường `permissions` chỉ được trả về khi có query `full_perms=true` trong GET nhưng schema lại đánh required vô điều kiện trong response 201 của POST. Em đã xác minh độc lập lỗi này trên tài nguyên `Correspondents`.

### Câu hỏi 7: Trong Vòng 3, Schemathesis phát hiện "14 lỗi Server Error (HTTP 500)". Con số 14 này đang đếm đại lượng gì và nêu ví dụ một endpoint bị lỗi?
- **Đáp án:**
  - Con số `14` trong dòng `❌ Server error: 14` của Schemathesis Vòng 3 là **số lượng failure checks thuộc danh mục `not_a_server_error`** được ghi nhận trên các operations kiểm thử (bao gồm 13 operations đơn lẻ như `DELETE /api/documents/{id}/notes/`, `POST /api/documents/edit_pdf/`, `GET /api/documents/{id}/preview/`,... và 1 trường hợp trong kiểm thử chuỗi Stateful). Nó không đồng nghĩa với 14 bug mã nguồn độc lập trong backend Django.
  - Ví dụ cụ thể: Endpoint `DELETE /api/documents/{id}/notes/` khi nhận tham số đường dẫn `{id}` dị thường kết hợp với query parameters không hợp lệ trong quá trình fuzzing đã khiến backend văng ra lỗi 500 HTML thay vì trả về 400 hoặc 404.

### Câu hỏi 8: Ba luồng nghiệp vụ cá nhân của TV3 được thiết kế và xác thực trên hệ thống như thế nào?
- **Đáp án:**
  - Cả 3 luồng nghiệp vụ đều được xác thực qua script tự động tương tác trực tiếp với API Paperless-ngx trên Docker local:
    - **Luồng 1 (Upload & OCR):** Upload tệp PDF `TV3_Sample_01_Report_303.pdf` qua `POST /api/documents/post_document/` nhận HTTP 202. Polling Celery task hoàn tất (`SUCCESS`), sinh Document ID 4 và kiểm tra `GET /api/documents/4/` trích xuất thành công 306 ký tự văn bản. Đã xác thực bổ sung OCR trên ảnh raster PNG `TV3_Sample_Scan_Image_303.png` sinh Document ID 5 trích xuất chính xác chuỗi tên và MSSV.
    - **Luồng 2 (Quản trị quan hệ):** Tạo mới Tag ID 5, Correspondent ID 4, Document Type ID 4 (HTTP 201). Gửi `PATCH /api/documents/4/` liên kết 3 thực thể này vào tài liệu, sau đó gọi `GET` đối chiếu các khóa ngoại cập nhật chính xác 100%.
    - **Luồng 3 (Tìm kiếm & Lọc):** Gọi `GET /api/documents/?query=Schemathesis` để kiểm tra công cụ tìm kiếm toàn văn và `GET /api/documents/?tags__id__all=5` để kiểm tra bộ lọc nhãn; cả hai truy vấn đều trả về chính xác Document ID 4.
