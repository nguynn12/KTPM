# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV4 VÒNG 1 (Seed 404)

- **Người thực hiện:** Nguyễn Nhất Minh (TV4) — Windows, Python 3.12, Schemathesis v4.31.0
- **MSSV:** 2312690
- **Thời điểm chạy:** 2026-10-19 19:53:03
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (Commit SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** Schemathesis v4.31.0
- **Mục tiêu Vòng 1:** Chỉ đọc (GET) trên 4 nhóm tài nguyên trọng tâm (`tags`, `correspondents`, `document_types`, `documents`)
- **Phạm vi Regex:** `^/api/(tags|correspondents|document_types|documents)/`
- **Method loại trừ:** POST, PUT, PATCH, DELETE (`--exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE`)
- **Phases:** `examples,fuzzing`
- **Checks:** `not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance`
- **Cấu hình sinh:** `--seed 404`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm kiểm thử được phát hiện hợp lệ)

### Lệnh chuẩn hóa đã chạy (Token đã được che):
```bash
schemathesis run http://localhost:8000/api/schema/ \
    --url http://localhost:8000 \
    --include-path-regex '^/api/(tags|correspondents|document_types|documents)/' \
    --seed 404 --max-examples 25 --workers 1 --mode all \
    --header "Authorization: Token [REDACTED_TOKEN]" \
    --report junit,ndjson \
    --report-junit-path results/TV4_round1_seed404_junit.xml \
    --report-ndjson-path results/TV4_round1_seed404.ndjson \
    --output-sanitize true --no-color \
    --exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE \
    --phases examples,fuzzing \
    --checks not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance
```

---

## 1. Số liệu đọc từ chính file kết quả thực tế

| Chỉ số | Giá trị | Nguồn trích xuất |
|---|---|---|
| Operation có trong Schema | 163 | NDJSON `LoadingFinished` / CLI log |
| **Operation theo phạm vi (mong đợi)** | **19** | Đếm trực tiếp từ `/api/schema/?format=json` |
| **Operation được chọn (thực tế)** | **19** | NDJSON `LoadingFinished` / CLI log (`19 selected / 163 total`) |
| Đối chiếu mong đợi/thực tế | **KHỚP 100% (19/19)** | Chuẩn hóa theo toàn nhóm |
| Tổng thời gian chạy (giây) | **1.91s** (CLI execution) / **3.50s** (Process) | NDJSON / CLI summary |
| `<testcase>` trong JUnit XML | 19 | JUnit XML `tests="19"` |
| Failures trong JUnit XML | 17 | JUnit XML `failures="17"` |
| Errors trong JUnit XML | 0 | JUnit XML `errors="0"` |
| Skipped trong JUnit XML | 0 | JUnit XML `skipped="0"` |
| Test case sinh ra (CLI) | **72** | Bảng tổng kết CLI |
| Test case phát hiện lỗi (CLI) | **17** | Bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **22** | Bảng tổng kết CLI |

---

## 2. Phân loại lỗi theo Check bị vi phạm

| Check bị vi phạm | Số lỗi khác nhau (Unique Failures) |
|---|---|
| Server error (HTTP 500) | 4 |
| Response violates schema | 5 |
| Undocumented Content-Type | 4 |
| Undocumented HTTP status code | 9 |
| **Tổng số lỗi khác nhau** | **22** |

---

## 3. Các lỗi trọng tâm được phát hiện trong Vòng 1

1. **Server Error 500 tại `GET /api/documents/{id}/share_links/` (BUG-04):**
   - URL: `GET /api/documents/%F1%8D%96%91%C2%A9/share_links/`
   - Mã lỗi trả về: `500 Internal Server Error`
   - Nguyên nhân: `{id}` truyền chuỗi ký tự unicode không phải số nguyên, backend không validate kiểu số mà query trực tiếp gây unhandled `ValueError`.

2. **Server Error 500 tại `GET /api/documents/{id}/suggestions/` và `/ai_suggestions/`:**
   - Mã lỗi: `500 Internal Server Error` khi `{id}` nhận chuỗi bất thường (`false`, ký tự rác).

3. **Response vi phạm Schema tại `GET /api/correspondents/` và `GET /api/correspondents/{id}/` (BUG-06):**
   - Phản hồi thiếu trường bắt buộc `permissions`, trường `last_correspondence` trả về `null` trong khi OpenAPI schema khai báo dạng string date bắt buộc.

4. **Response vi phạm Schema tại `GET /api/document_types/` và `GET /api/document_types/{id}/`:**
   - Phản hồi thiếu trường bắt buộc `permissions`.

5. **Undocumented Content-Type tại `GET /api/documents/{id}/download/` và `/preview/` (BUG-05):**
   - API trả về `text/plain; charset=utf-8` hoặc `image/webp` (file binary/text thực tế), nhưng OpenAPI schema chỉ định nghĩa `application/json`.

---

## 4. File bằng chứng
- Log CLI: `results/TV4_round1_seed404.log`
- JUnit XML: `results/TV4_round1_seed404_junit.xml`
- NDJSON: `results/TV4_round1_seed404.ndjson`
- Lần chạy khảo sát mở rộng ban đầu: `results/TV4_round1_seed404_thamdo.*` (toàn bộ 65 operation GET trên toàn hệ thống).
