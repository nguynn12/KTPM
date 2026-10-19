# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV2 VÒNG 1 (seed 202)

- **Người chạy:** Tạ Nhật Nguyên (TV2) — Windows 11, Docker Desktop
- **Thời điểm chạy:** 2026-10-19 13:49:46
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** schemathesis, version 4.30.1 | Python 3.14.8
- **Ý nghĩa vòng 1:** chỉ đọc (GET), trên 4 nhóm tài nguyên (`tags`, `correspondents`, `document_types`, `documents`)
- **Phạm vi (regex đường dẫn):** `^/api/(tags|correspondents|document_types|documents)/`
- **Method loại trừ:** POST, PUT, PATCH, DELETE (hoặc `--include-method GET`)
- **Phases:** examples, fuzzing (coverage và stateful tắt)
- **Checks:** not_a_server_error, status_code_conformance, content_type_conformance, response_headers_conformance, response_schema_conformance
- **Cấu hình sinh:** `--seed 202`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm kiểm thử được phát hiện)

Lệnh đã chạy (token đã được che bằng `[Filtered]`):

```bash
st run http://webserver:8000/api/schema/ --url http://webserver:8000 --include-path-regex ^/api/(tags|correspondents|document_types|documents)/ --seed 202 --max-examples 25 --workers 1 --mode all -H "Authorization: Token [Filtered]" --report junit,ndjson --report-junit-path /results/TV2_round1_seed202_junit.xml --report-ndjson-path /results/TV2_round1_seed202.ndjson --output-sanitize true --no-color --exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE --phases examples,fuzzing --checks not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance
```

## 1. Số liệu đọc từ chính file kết quả

| Chỉ số | Giá trị | Nguồn trích xuất |
|---|---|---|
| Operation có trong schema | 163 | NDJSON `LoadingFinished` / CLI |
| **Operation theo phạm vi (mong đợi)** | **19** | đếm trực tiếp từ `/api/schema/?format=json` |
| **Operation được chọn (thực tế)** | **19** | NDJSON `LoadingFinished` / CLI |
| Đối chiếu mong đợi/thực tế | **KHỚP (19/19)** | so sánh 2 dòng trên |
| Tổng thời gian chạy (giây) | 31.85s | NDJSON `EngineFinished` / CLI |
| `<testcase>` trong JUnit | 19 | JUnit XML `tests="19"` |
| Failures trong JUnit | 14 | JUnit XML `failures="14"` |
| Errors trong JUnit | 0 | JUnit XML `errors="0"` |
| Skipped trong JUnit | 0 | JUnit XML `skipped="0"` |
| Testcase sinh ra (CLI) | 159 | Bảng tổng kết CLI |
| Testcase phát hiện lỗi (CLI) | 14 | Bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **16** | Bảng tổng kết CLI |

## 2. Phân loại lỗi theo check (đọc từ bảng tổng kết CLI)

| Check bị vi phạm | Số lỗi khác nhau |
|---|---|
| Server error (HTTP 500) | 2 |
| Response violates schema | 4 |
| Undocumented Content-Type | 4 |
| Undocumented HTTP status code | 6 |
| **Tổng** | **16** |

## 3. Các lỗi nghiêm trọng được xác nhận tái hiện trong phạm vi 4 nhóm API

1. **Server error 500 tại `GET /api/documents/`:**
   - Test Case ID: `IrS0Ww`
   - URL: `GET /api/documents/?content__iendswith=%F1%BB%95%8B%00y%F3%8A%85%B6%C3%A8wZ&correspondent__id=131&document_type__id=108`
   - Nhận mã: `HTTP 500 Internal Server Error` (liên quan tới xử lý lọc chuỗi/ký tự unicode bất thường).

2. **Server error 500 tại `GET /api/documents/{id}/share_links/` (BUG-04):**
   - Test Case ID: `ECom8f`
   - URL: `GET /api/documents/3uZ3%C3%86%C2%B2r/share_links/`
   - Nhận mã: `HTTP 500 Internal Server Error` do tham số `{id}` trong URL path không phải là số nguyên, backend không bẫy ngoại lệ chuyển thành 400/404 mà để sập unhandled exception.

3. **Response vi phạm Schema tại `GET /api/document_types/{id}/` (BUG-06):**
   - Test Case ID: `LosEQ3`
   - URL: `GET /api/document_types/108/`
   - Thiếu trường bắt buộc `permissions` theo định nghĩa của OpenAPI Schema.

## 4. File bằng chứng
- Log CLI: `results/TV2_round1_seed202.log`
- JUnit XML: `results/TV2_round1_seed202_junit.xml`
- NDJSON: `results/TV2_round1_seed202.ndjson`
- Lần chạy thăm dò trước đó (toàn bộ 65 GET operation): `results/TV2_round1_seed202_thamdo.*`
