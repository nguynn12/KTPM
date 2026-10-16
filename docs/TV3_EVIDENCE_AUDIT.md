# BIÊN BẢN RÀ SOÁT & ĐỐI CHIẾU CHỨNG CỨ KIỂM THỬ — THÀNH VIÊN 3 (TV3)

**Thành viên thực hiện:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed Schemathesis: 303  
**Học phần:** Kiểm thử phần mềm — Đề tài: Paperless-ngx (R08) + Schemathesis (K05)  
**Ngày thực hiện kiểm toán:** 16/10/2026  
**Mục đích:** Đối chiếu chi tiết, phát hiện và giải quyết triệt để các điểm mâu thuẫn số liệu giữa mã nguồn runner, log thực thi gốc, tệp báo cáo JUnit XML / NDJSON và tài liệu thuyết minh đồ án; đảm bảo 100% số liệu bàn giao có bằng chứng kỹ thuật xác thực.

---

## 1. Đối chiếu & Chuẩn hóa Kiểm thử Thủ công (Phần E)

### 1.1 Mâu thuẫn phát hiện ban đầu
- Trong `docs/TEST_CASES_TV3.md`: Bảng tổng kết trước đây ghi nhận: Correspondents có 14 PASS + 1 REPRO-BUG-01 + 5 NOT RUN; Document Types có 5 PASS + 1 REPRO-BUG-01 + 14 NOT RUN (Tổng: 19 PASS, 2 lỗi, 19 NOT RUN).
- Trong `docs/TV3_SUMMARY_FOR_SLIDES.md`: Báo cáo ghi nhận: 18 ca chạy thật (16 PASS, 2 ca lỗi).
- Có sự lệch nhau 3 ca PASS giữa hai tài liệu.

### 1.2 Đối chiếu với mã nguồn runner [`scripts/run_manual_tests_TV3.py`](../scripts/run_manual_tests_TV3.py)
- Mảng kiểm thử `test_cases = [...]` trong hàm `run_manual_suite()` có đúng **18 test cases**:
  - **13 ca Correspondents:**
    1. `TV3-COR-01`: POST tên hợp lệ -> HTTP 201 (**PASS**)
    2. `TV3-COR-02`: POST thiếu trường `name` -> HTTP 400 (**PASS**)
    3. `TV3-COR-03`: POST `name=""` -> HTTP 400 (**PASS**)
    4. `TV3-COR-04`: POST `name=null` -> HTTP 400 (**PASS**)
    5. `TV3-COR-05`: POST trùng tên `TV2_Bank_202` -> HTTP 400 (**PASS**)
    6. `TV3-COR-06`: POST độ dài $L-1=127$ ký tự -> HTTP 201 (**PASS**)
    7. `TV3-COR-07`: POST độ dài $L=128$ ký tự -> HTTP 201 (**PASS**)
    8. `TV3-COR-08`: POST độ dài $L+1=129$ ký tự -> HTTP 400 (**PASS**)
    9. `TV3-COR-10`: POST tên Unicode có dấu và icon -> HTTP 201 (**PASS**)
    10. `TV3-COR-17`: GET không có Authorization header -> HTTP 401 (**PASS**)
    11. `TV3-COR-18`: GET với token giả -> HTTP 401 (**PASS**)
    12. `TV3-COR-19`: GET phân trang `?page=1&page_size=1` -> HTTP 200 (**PASS**)
    13. `TV3-COR-20`: POST `set_permissions.view=false` -> HTTP 500 (**REPRO-BUG-01**)
  - **5 ca Document Types:**
    14. `TV3-DT-01`: POST tên hợp lệ -> HTTP 201 (**PASS**)
    15. `TV3-DT-02`: POST thiếu trường `name` -> HTTP 400 (**PASS**)
    16. `TV3-DT-03`: POST `name=""` -> HTTP 400 (**PASS**)
    17. `TV3-DT-08`: POST độ dài $L+1=129$ ký tự -> HTTP 400 (**PASS**)
    18. `TV3-DT-20`: POST `set_permissions.view=false` -> HTTP 500 (**REPRO-BUG-01**)

### 1.3 Nguyên nhân gốc và Hành động chuẩn hóa
- **Nguyên nhân gốc:** Ở cuối script runner (dòng 339–347), có khối lệnh dọn dẹp môi trường (teardown/cleanup) gọi `requests.delete(f"{BASE_URL}/api/correspondents/{cid}/")` và `requests.delete(f"{BASE_URL}/api/document_types/{dtid}/")` để xóa các ID tạm sinh ra trong lúc test. Tác giả tài liệu trước đây đã tính nhầm thao tác cleanup này thành 2 test case `TV3-COR-15` và `TV3-DT-15`, đồng thời đánh dấu PASS cho `TV3-COR-11` (vốn chưa có assert độc lập trong mảng `results`).
- **Hành động chuẩn hóa:**
  - `TV3-COR-11`: Chuyển về trạng thái **NOT RUN** (Chưa đưa assert độc lập vào runner).
  - `TV3-COR-15`: Chuyển về trạng thái **NOT RUN** (Là bước teardown dọn dẹp, không tính ca kiểm thử độc lập).
  - `TV3-DT-15`: Chuyển về trạng thái **NOT RUN** (Là bước teardown dọn dẹp, không tính ca kiểm thử độc lập).
  - Các ca chưa chạy khác: Giữ nguyên trạng thái **NOT RUN**.
- **Số liệu thống nhất chính thức toàn bộ hồ sơ:**
  - Tổng số ca thiết kế: **40 test cases**.
  - Thực thi thực tế: **18 test cases** (16 PASS, 2 REPRO-BUG-01).
  - Chưa chạy: **22 test cases** (7 ca Correspondents + 15 ca Document Types).

---

## 2. Đối chiếu Ba Lượt Chạy Schemathesis Thực tế (Seed 303)

Các tệp bằng chứng gốc được kiểm tra tại `results/`:
- **Vòng 1:** `TV3_round1_seed303_20261016_093736.*`
- **Vòng 2:** `TV3_round2_seed303_20261016_093803.*`
- **Vòng 3:** `TV3_round3_seed303_20261016_093930.*`

### 2.1 Bảng đối chiếu số liệu theo đúng nguồn và đơn vị

| Chỉ số kỹ thuật | Vòng 1 (Read-only GET) | Vòng 2 (CRUD Thực thể) | Vòng 3 (Full CRUD + Docs) | Nguồn trích xuất bằng chứng |
|---|:---:|:---:|:---:|---|
| **Operations được chọn** | 19 / 163 | 18 / 163 | 53 / 163 | NDJSON `LoadingFinished.statistic.operations.selected` |
| **Thời gian chạy Engine** | 2.71 giây | 42.12 giây | 102.41 giây | NDJSON `EngineFinished.running_time` |
| **Thời gian tổng JUnit** | 2.52 giây | 40.36 giây | 99.58 giây | JUnit XML `<testsuites time="...">` |
| **Test cases sinh (Hypothesis)** | 74 generated | 744 generated (68 skipped) | 1734 generated (112 skipped) | CLI Log `SUMMARY -> Test cases: ... generated` |
| **Ca sinh tìm ra lỗi (CLI)** | 17 | 44 | 108 | CLI Log `... found ... unique failures` |
| **Ca sinh bị Exception (CLI)** | 0 | 0 | 1 errored | CLI Log `... 1 errored ...` |
| **Kết quả Phase: Coverage** | *(Disabled)* | 18 failed | 2 passed, 51 failed | CLI Log `Phase: Coverage` |
| **Kết quả Phase: Fuzzing** | 2 passed, 17 failed | 3 passed, 15 failed | 4 passed, 49 failed | CLI Log `Phase: Fuzzing` |
| **Kết quả Phase: Stateful** | *(Disabled)* | 102 passed, 36 failed | 193 passed, 63 failed | CLI Log `Phase: Stateful` (Chuỗi API kịch bản) |
| **Số testcase trong JUnit XML** | 19 | 19 (18 ops + 1 stateful) | 54 (53 ops + 1 stateful) | JUnit XML `<testsuite tests="...">` |
| **Failures trong JUnit XML** | 17 | 19 | 53 | JUnit XML `<testsuite failures="...">` |
| **Errors trong JUnit XML** | 0 | 0 | 0 | JUnit XML `<testsuite errors="...">` |
| **Passed trong JUnit XML** | 2 | 0 | 1 | JUnit XML `<testcase>` không có `<failure>` |
| **Tổng Unique Failures (Checks)** | **22 failures** | **51 failures** | **131 failures** | CLI Log `SUMMARY -> Failures:` |
| • Server error (500) | 5 | 1 | 14 | Failure check `not_a_server_error` |
| • Response violates schema | 4 | 14 | 19 | Failure check `response_schema_conformance` |
| • API rejected compliant | 0 | 10 | 24 | Failure check `status_code_conformance` (Negative) |
| • API accepted invalid | 0 | 0 | 3 | Failure check `status_code_conformance` (Positive) |
| • Undocumented Content-Type | 3 | 0 | 3 | Failure check `content_type_conformance` |
| • Undocumented HTTP code | 10 | 26 | 67 | Failure check `status_code_conformance` |
| • Unsupported methods | 0 | 0 | 1 | Failure check `unsupported_method` |
| **Warnings** | 1 (Missing test data) | 0 | 2 (Missing auth, test data) | CLI Log `SUMMARY -> Warnings:` |
| **Exit Code** | 1 | 1 | 1 | CLI Process Exit Code |

### 2.2 Giải trình Kỹ thuật Chuyên sâu về 2 Điểm Mâu thuẫn Báo cáo

#### Vấn đề 1: Vì sao Vòng 2 có JUnit 19 testcases / 19 failures nhưng CLI ghi nhận Fuzzing "3 passed / 15 failed"?
- **Cơ chế tổng hợp của Schemathesis:** JUnit XML được thiết kế để báo cáo tình trạng theo từng **API Operation** (18 operations) cộng với một mục cho **Stateful tests** (tổng cộng 19 testcases).
- Kết quả của một `<testcase>` trong JUnit XML là kết quả **tổng hợp (aggregate)** của toàn bộ các phase kiểm thử mà operation đó tham gia (Coverage, Fuzzing, Stateful).
- Trong Vòng 2, ở phase **Coverage**, toàn bộ 18 operations đều bị phát hiện vi phạm ít nhất một assertion check (chủ yếu là check `status_code_conformance` do mã lỗi 400/404 chưa được khai báo trong OpenAPI schema).
- Khi một operation đã bị vi phạm ở phase Coverage, Schemathesis sẽ gắn thẻ `<failure>` cho operation đó trong báo cáo JUnit XML cuối cùng, ngay cả khi operation đó vượt qua phase Fuzzing độc lập. Thêm vào đó, mục `Stateful tests` cũng bị failure vì phase Stateful có 36 scenarios thất bại.
- Do đó: Trong JUnit XML ghi nhận chính xác `tests="19" failures="19" passed="0" errors="0"`. Con số "3 passed / 15 failed" chỉ là kết quả cục bộ của riêng phase Fuzzing trong CLI log.

#### Vấn đề 2: Vì sao Vòng 3 CLI báo "1 errored" nhưng JUnit XML báo "errors=0"?
- **Khác biệt về đơn vị đo lường:**
  - Chỉ số `1 errored` trong CLI summary (`1734 generated, 108 found 131 unique failures, 1 errored, 112 skipped`) là đơn vị **Hypothesis test case**: Trong 1734 mẫu thử dữ liệu được sinh ra, có đúng 1 mẫu thử gặp lỗi ngoại lệ khi thực thi (client-side execution exception, ví dụ lỗi kết nối mạng hoặc lỗi định dạng dữ liệu phía client runner).
  - Trong khi đó, JUnit XML biểu diễn theo đơn vị **Operation**: Khi operation chứa mẫu thử gặp ngoại lệ đó đồng thời đã vi phạm các invariant checks khác, Schemathesis gộp toàn bộ sự cố của operation đó vào một thẻ `<failure>` duy nhất. Thẻ `<error>` trong JUnit chỉ xuất hiện khi có lỗi nghiêm trọng ở cấp độ toàn bộ operation suite không thể chạy được. Vì toàn bộ 53 operations đều hoàn tất việc gửi request và nhận response, JUnit XML báo `errors="0"`.

---

## 3. Rà soát & Chuẩn hóa Kỹ thuật Nội dung Thuyết trình & Vấn đáp

| Điểm cần chuẩn hóa | Nội dung chưa chuẩn trước đây | Nội dung chuẩn xác đã hiệu chỉnh | Căn cứ kỹ thuật |
|---|---|---|---|
| **Ý nghĩa Exit Code 1** | Cho rằng Exit code 1 chứng minh đã chạy quét đủ 100% phạm vi. | Exit code 1 chỉ chứng minh Schemathesis đã chạy hoàn tất và phát hiện vi phạm kiểm thử (failure/error). | Không chứng minh độ bao phủ; độ bao phủ phải chứng minh bằng danh sách operations được chọn (19, 18, 53) và các phase đã chạy. |
| **Generated Cases vs Requests** | Coi 1734 generated cases là 1734 HTTP requests. | Generated cases là số ca thử nghiệm logic do Hypothesis sinh ra. | Trong Stateful testing, 1 test case gồm chuỗi nhiều request liên hoàn; shrinking gửi thêm request phụ; 112 ca bị skipped không gửi request. |
| **Số lượng 131 Failures** | Coi 131 failures là 131 bug độc lập hoặc 131 lỗi schema. | 131 failures là tổng số lần các invariant checks bị vi phạm trên các ca thử nghiệm. | Nhiều test cases cùng vi phạm một nguyên nhân gốc (ví dụ thiếu mã 400 trong schema hoặc lỗi phân quyền BUG-01). |
| **Bản chất "14 lỗi 500"** | Coi 14 lỗi 500 là 14 dòng bug mã nguồn riêng biệt trong backend Django. | 14 lỗi 500 là số lượng failure checks của bất biến `not_a_server_error` trên 13 operations độc lập và 1 trong stateful tests. | Fuzzing các tham số đường dẫn và body kích hoạt unhandled server error ở tầng Django view/ORM. |
| **Cơ chế lỗi BUG-01** | Suy đoán do `TypeError`, lỗi ORM compiler, ép kiểu ID số nguyên âm. | Đối chiếu đặc tả OpenAPI (`docs/openapi_TV3.json`), `set_permissions.view` là object chứa `users` và `groups`. Khi client gửi boolean `false`, backend không bắt validation 400 mà văng HTTP 500 HTML. | Do chưa có log traceback server Django bên trong container, chỉ ghi nhận hiện tượng kiểm thử hộp đen: Unhandled Server Error. Không suy đoán chi tiết mã nguồn khi chưa có traceback. |
| **Phạm vi lỗi BUG-03** | Khẳng định BUG-03 xảy ra trên toàn bộ các tài nguyên Paperless-ngx. | Đối chiếu response 201 của `POST /api/correspondents/` thiếu 3 trường required theo schema (`document_count`, `last_correspondence`, `permissions`). | Trường `permissions` gắn với query `full_perms` trong GET nhưng bị schema đánh required vô điều kiện trong POST 201. Chỉ khẳng định BUG-03 trên `Correspondents` vì chưa có kết quả kiểm tra response 201 trên các tài nguyên khác. |
| **Kỹ thuật Shrinking** | Cho rằng Shrinking chỉ là thuật toán tìm kiếm nhị phân (binary search). | Shrinking của Hypothesis là tập hợp các chiến lược heuristic đa dạng (xóa phần tử, giảm số nguyên, đơn giản hóa ký tự chuỗi). | Tài liệu thiết kế Hypothesis & Schemathesis engine. |
| **So sánh với Postman** | Cho rằng Postman chỉ có thể kiểm thử dữ liệu tĩnh. | Postman hỗ trợ kiểm thử động với biến môi trường, pre-request script và data files (CSV/JSON). | Điểm khác biệt cốt lõi: Schemathesis tự động sinh dữ liệu từ OpenAPI Specification và tự động assert các invariants mà tester không cần phải viết tay từng test case và assert cụ thể. |

---

## 4. Rà soát Môi trường, Băm Cấu hình & Đường dẫn Tương đối

### 4.1 Mã băm SHA256 OpenAPI Schema Thực tế
Đã kiểm tra bằng lệnh `Get-FileHash -Algorithm SHA256` trên máy local:
- **`docs/openapi_TV3.json`:** `888b0f89ec0a9f65293f5320a86b1810d7904f93033178b567e313d951b12e3a`
- **`docs/openapi_TV3.yaml`:** `4b56422b2e5bc4190efdefab3444c46336062c06c5c1478a2f44c1d6082785e0`
*(Đã loại bỏ mã băm cũ chưa được kiểm chứng `9e1ed205...` trong toàn bộ tài liệu).*

### 4.2 Giữ nguyên Dữ liệu nền Nhóm (Group Baseline)
- Giữ nguyên vẹn 4 Tags, 3 Correspondents, 3 Document Types và 2 file TXT mang tiền tố `TV2` làm mốc kiểm chuẩn của nhóm.
- Toàn bộ dữ liệu của TV3 sử dụng định danh `TV3_*_303`, test cases mang mã `TV3-COR-*`, `TV3-DT-*`, và các file kết quả mang tiền tố `TV3_round*`.

### 4.3 Chuẩn hóa Đường dẫn Tương đối (Relative Links)
Toàn bộ các liên kết dạng `file:///d:/...` trong các tài liệu:
- `docs/TV3_SUMMARY_FOR_SLIDES.md`
- `docs/TEST_CASES_TV3.md`
- `docs/TEST_CASES.md`
- `docs/TV3_STATUS.md`
- `docs/BUSINESS_FLOWS_TV3.md`
- `docs/TV3_TEST_PLAN.md`

đã được chuyển đổi hoàn toàn sang đường dẫn tương đối (ví dụ `[TEST_CASES_TV3.md](TEST_CASES_TV3.md)`, `[XML](../results/...)`), đảm bảo liên kết hoạt động chính xác và portable trên mọi môi trường và Git repository.

---

## 5. Kết luận Kiểm toán
1. Toàn bộ mâu thuẫn số liệu kiểm thử thủ công đã được giải quyết: **16 PASS, 2 REPRO-BUG-01, 22 NOT RUN** trên tổng số 40 test cases thiết kế.
2. Số liệu 3 vòng Schemathesis được xác thực chính xác từng đơn vị đo lường từ log, XML và NDJSON gốc.
3. Nội dung thuyết minh, slide và câu hỏi vấn đáp đã được chuẩn hóa về mặt kỹ thuật, tránh suy đoán chủ quan và tuân thủ chặt chẽ đặc tả OpenAPI Paperless-ngx 3.1.3.
