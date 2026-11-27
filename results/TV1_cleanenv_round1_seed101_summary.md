> **Bản sao từ môi trường sạch biệt lập ngày 26/11/2026.**
> Đường dẫn gốc đã thay bằng ``<VERIFY_DIR>``; port `8013` dùng để tránh trùng port `8000`.
> Tài khoản đã che thành ``<ADMIN>`` (nếu có). Token đã bị runner thay bằng `[REDACTED]`.
> File gốc tên `TV1_round1_seed101.*`; khi công bố đổi thành `TV1_cleanenv_round1_seed101.*`
> để không ghi đè kết quả 18/10.

# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV1 VÒNG 1 (seed 101)

- **Người chạy:** Trần Gia Huy (TV1) — Windows 11, Docker Desktop
- **Thời điểm chạy:** 2026-11-26 20:48:43
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8013`
- **Công cụ:** schemathesis, version 4.30.1 | Python 3.13.15 | Hypothesis 6.170.17
- **Ý nghĩa vòng 1:** chỉ đọc (GET), trên 4 nhóm tài nguyên
- **Phạm vi (regex đường dẫn):** `^/api/(tags|correspondents|document_types|documents)/`
- **Method loại trừ:** POST, PUT, PATCH, DELETE
- **Phases:** examples,fuzzing
- **Checks:** not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance
- **Cấu hình sinh:** `--seed 101`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm được phát hiện)

Lệnh đã chạy (token đã bị Schemathesis lọc thành `[Filtered]`):

```bash
st run http://localhost:8013/api/schema/ --url http://localhost:8013 --include-path-regex ^/api/(tags|correspondents|document_types|documents)/ --seed 101 --max-examples 25 --workers 1 --mode all --header Authorization: [Filtered] --report junit,ndjson --report-junit-path <VERIFY_DIR>\results\TV1_round1_seed101.xml --report-ndjson-path <VERIFY_DIR>\results\TV1_round1_seed101.ndjson --output-sanitize true --no-color --exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE --phases examples,fuzzing --checks not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance
```

## 1. Số liệu đọc từ chính file kết quả

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Operation có trong schema | 163 | NDJSON `LoadingFinished` |
| **Operation theo phạm vi (mong đợi)** | **19** | đếm trực tiếp từ `/api/schema/` |
| **Operation được chọn (thực tế)** | **19** | NDJSON `LoadingFinished` |
| Đối chiếu mong đợi/thực tế | KHỚP | so sánh 2 dòng trên |
| Tổng thời gian chạy (giây) | 7.78 | NDJSON `EngineFinished` |
| Lý do dừng | completed | NDJSON `EngineFinished` |
| `<testcase>` trong JUnit | 19 | JUnit XML `tests=` |
| Failures trong JUnit | 15 | JUnit XML `failures=` |
| Errors trong JUnit | 0 | JUnit XML `errors=` |
| Skipped trong JUnit | 0 | JUnit XML `skipped=` |
| Testcase sinh ra (CLI) | 130 | bảng tổng kết CLI |
| Testcase phát hiện lỗi (CLI) | 15 | bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **18** | bảng tổng kết CLI |
| Scenario đã chạy / bỏ qua / lỗi | 38 / 19 / 15 | NDJSON `Scenario*` |

> Ghi nhớ khi đọc số: `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho mỗi
> operation, **không phải** số request đã gửi; số `<testcase>` là số operation × check được ánh
> xạ, không phải số request; **unique failures không phải số bug** — nhiều failure có thể chung
> một nguyên nhân, và một nguyên nhân có thể sinh nhiều failure.

## 2. Phân loại lỗi theo check (đọc từ bảng tổng kết CLI)

| Check bị vi phạm | Số lỗi khác nhau |
|---|---|
| Server error | 2 |
| Response violates schema | 8 |
| Undocumented Content-Type | 3 |
| Undocumented HTTP status code | 5 |
| **Tổng** | **18** |

## 3. Lý do bỏ qua scenario (NDJSON)

- No examples in schema: 19

## 4. Phases đã chạy

- Thực chạy: probing, schema_analysis, auth_bootstrap, examples, fuzzing
- Không chạy: coverage (disabled), stateful (disabled)

## 5. File bằng chứng (đường dẫn tương đối trong repo)

- Log xác minh tổng hợp (đã che thông tin đăng nhập): `results/TV1_cleanenv_verify.log`
- JUnit XML: `results/TV1_cleanenv_round1_seed101.xml`
- NDJSON (sự kiện thô): `results/TV1_cleanenv_round1_seed101.ndjson`

> Token đã bị thay bằng `[REDACTED]` trong mọi file kết quả (số vị trí đã thay ở XML/NDJSON: 0).