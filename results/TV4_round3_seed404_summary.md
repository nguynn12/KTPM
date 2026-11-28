# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV4 VÒNG 3 (Seed 404)

- **Người thực hiện:** Nguyễn Nhất Minh (TV4) — Windows, Python 3.12, Schemathesis v4.31.0
- **MSSV:** 2312690
- **Thời điểm chạy:** 2026-10-19 19:56:24
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (Commit SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** Schemathesis v4.31.0
- **Mục tiêu Vòng 3:** Kiểm thử toàn diện mở rộng toàn bộ 4 nhóm tài nguyên trọng tâm (`tags`, `correspondents`, `document_types`, `documents`) và kích hoạt toàn bộ các kiểm tra (`--checks all`)
- **Phạm vi Regex:** `^/api/(tags|correspondents|document_types|documents)/`
- **Checks:** `--checks all`
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
    --report-junit-path results/TV4_round3_seed404_junit.xml \
    --report-ndjson-path results/TV4_round3_seed404.ndjson \
    --output-sanitize true --no-color \
    --checks all
```

---

## 1. Số liệu đọc từ chính file kết quả thực tế

| Chỉ số | Giá trị | Nguồn trích xuất |
|---|---|---|
| Operation có trong Schema | 163 | NDJSON `LoadingFinished` / CLI log |
| **Operation theo phạm vi (mong đợi)** | **53** | Đếm trực tiếp từ `/api/schema/?format=json` |
| **Operation được chọn (thực tế)** | **53** | NDJSON `LoadingFinished` / CLI log (`53 selected / 163 total`) |
| Đối chiếu mong đợi/thực tế | **KHỚP 100% (53/53)** | Chuẩn hóa theo toàn nhóm |
| Tổng thời gian chạy (giây) | **73.56s** (CLI execution) / **75.80s** (Process) | NDJSON / CLI summary |
| `<testcase>` trong JUnit XML | 54 | JUnit XML `tests="54"` |
| Failures trong JUnit XML | 53 | JUnit XML `failures="53"` |
| Skipped trong JUnit XML | 0 | JUnit XML `skipped="0"` |
| Test case sinh ra (CLI) | **1516** (120 skipped) | Bảng tổng kết CLI |
| Test case phát hiện lỗi (CLI) | **107** | Bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **134** | Bảng tổng kết CLI |

---

## 2. Phân loại lỗi theo Check bị vi phạm

| Check bị vi phạm | Số lỗi khác nhau (Unique Failures) |
|---|---|
| Server error (HTTP 500) | 16 |
| Response violates schema | 21 |
| API accepted schema-violating request | 1 |
| API rejected schema-compliant request | 22 |
| Undocumented Content-Type | 4 |
| Undocumented HTTP status code | 69 |
| Unsupported methods | 1 |
| **Tổng số lỗi khác nhau** | **134** |

---

## 3. Các lỗi trọng tâm được phát hiện trong Vòng 3

1. **Server error 500 tại `GET /api/documents/?modified__year=...` (BUG-02):**
   - Lỗi unhandled `ValueError` khi lọc tham số năm `modified__year` nhận giá trị `<= 0` ngoài dải 1..9999 của hàm `datetime`.
2. **Server error 500 tại `GET /api/documents/{id}/share_links/`, `/notes/`, `/metadata/` (BUG-04):**
   - Tham số `{id}` nhận chuỗi ký tự unicode/text khiến `Document.objects.get(pk=...)` sập lỗi unhandled `ValueError`.
3. **Lỗi `BUG-01` và `BUG-03` tiếp tục được tái hiện ổn định:**
   - Tiếp tục khẳng định tính xác thực và khả năng tái lập 100% của các lỗi backend trên Paperless-ngx v3.1.3.

---

## 4. File bằng chứng
- Log CLI: `results/TV4_round3_seed404.log`
- JUnit XML: `results/TV4_round3_seed404_junit.xml`
- NDJSON: `results/TV4_round3_seed404.ndjson`
