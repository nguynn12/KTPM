# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV4 VÒNG 2 (Seed 404)

- **Người thực hiện:** Nguyễn Nhất Minh (TV4) — Windows, Python 3.12, Schemathesis v4.31.0
- **MSSV:** 2312690
- **Thời điểm chạy:** 2026-10-19 19:54:24
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (Commit SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** Schemathesis v4.31.0
- **Mục tiêu Vòng 2:** Kiểm thử các thao tác ghi dữ liệu (CRUD: POST, PUT, PATCH, DELETE, GET) trên 3 nhóm metadata cốt lõi (`tags`, `correspondents`, `document_types`)
- **Phạm vi Regex:** `^/api/(tags|correspondents|document_types)/`
- **Checks:** `--checks all`
- **Cấu hình sinh:** `--seed 404`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm kiểm thử được phát hiện hợp lệ)

### Lệnh chuẩn hóa đã chạy (Token đã được che):
```bash
schemathesis run http://localhost:8000/api/schema/ \
    --url http://localhost:8000 \
    --include-path-regex '^/api/(tags|correspondents|document_types)/' \
    --seed 404 --max-examples 25 --workers 1 --mode all \
    --header "Authorization: Token [REDACTED_TOKEN]" \
    --report junit,ndjson \
    --report-junit-path results/TV4_round2_seed404_junit.xml \
    --report-ndjson-path results/TV4_round2_seed404.ndjson \
    --output-sanitize true --no-color \
    --checks all
```

---

## 1. Số liệu đọc từ chính file kết quả thực tế

| Chỉ số | Giá trị | Nguồn trích xuất |
|---|---|---|
| Operation có trong Schema | 163 | NDJSON `LoadingFinished` / CLI log |
| **Operation theo phạm vi (mong đợi)** | **18** | Đếm trực tiếp từ `/api/schema/?format=json` |
| **Operation được chọn (thực tế)** | **18** | NDJSON `LoadingFinished` / CLI log (`18 selected / 163 total`) |
| Đối chiếu mong đợi/thực tế | **KHỚP 100% (18/18)** | Chuẩn hóa theo toàn nhóm |
| Tổng thời gian chạy (giây) | **49.71s** (CLI execution) / **51.03s** (Process) | NDJSON / CLI summary |
| `<testcase>` trong JUnit XML | 19 | JUnit XML `tests="19"` |
| Failures trong JUnit XML | 19 | JUnit XML `failures="19"` |
| Skipped trong JUnit XML | 0 | JUnit XML `skipped="0"` |
| Test case sinh ra (CLI) | **1009** (72 skipped) | Bảng tổng kết CLI |
| Test case phát hiện lỗi (CLI) | **47** | Bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **55** | Bảng tổng kết CLI |

---

## 2. Phân loại lỗi theo Check bị vi phạm

| Check bị vi phạm | Số lỗi khác nhau (Unique Failures) |
|---|---|
| Response violates schema | 14 |
| API accepted schema-violating request | 1 |
| API rejected schema-compliant request | 12 |
| Undocumented HTTP status code | 28 |
| **Tổng số lỗi khác nhau** | **55** |

---

## 3. Các lỗi trọng tâm được phát hiện trong Vòng 2

1. **BUG-01 (Tạo mới sập do permissions):**
   - Lỗi `TypeError` unhandled khi gửi payload sai cấu trúc ở `set_permissions` đối với `POST /api/tags/`, `correspondents/`, `document_types/`.
2. **BUG-03 (Vi phạm hợp đồng dữ liệu):**
   - Phản hồi mã `201 Created` khi tạo mới `correspondents` và `tags` bị thiếu trường bắt buộc `document_count`.
3. **Mã trạng thái ngoài tài liệu đặc tả (Undocumented Status Code):**
   - Phản hồi `404 Not Found` hoặc `403 Forbidden` khi thao tác xóa `DELETE /api/correspondents/{id}/` và `DELETE /api/document_types/{id}/` với ID không hợp lệ, trong khi schema chỉ ghi nhận mã `204 No Content`.

---

## 4. File bằng chứng
- Log CLI: `results/TV4_round2_seed404.log`
- JUnit XML: `results/TV4_round2_seed404_junit.xml`
- NDJSON: `results/TV4_round2_seed404.ndjson`
