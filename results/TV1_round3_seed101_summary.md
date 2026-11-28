# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV1 VÒNG 3 (seed 101)

- **Người chạy:** Trần Gia Huy (TV1) — Windows 11, Docker Desktop
- **Thời điểm chạy:** 2026-10-18 16:23:58
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** schemathesis, version 4.30.1 | Python 3.13.15 | Hypothesis 6.170.1
- **Ý nghĩa vòng 3:** mọi method, trên cả 4 nhóm tài nguyên
- **Phạm vi (regex đường dẫn):** `^/api/(tags|correspondents|document_types|documents)/`
- **Method loại trừ:** không loại trừ
- **Phases:** mặc định của Schemathesis 4.30.1 (không truyền cờ --phases)
- **Checks:** all
- **Cấu hình sinh:** `--seed 101`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm được phát hiện)

Lệnh đã chạy (token đã bị Schemathesis lọc thành `[Filtered]`):

```bash
st run http://localhost:8000/api/schema/ --url http://localhost:8000 --include-path-regex ^/api/(tags|correspondents|document_types|documents)/ --seed 101 --max-examples 25 --workers 1 --mode all --header Authorization: [Filtered] --report junit,ndjson --report-junit-path D:\KTPM\results\TV1_round3_seed101.xml --report-ndjson-path D:\KTPM\results\TV1_round3_seed101.ndjson --output-sanitize true --no-color --checks all
```

## 1. Số liệu đọc từ chính file kết quả

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Operation có trong schema | 163 | NDJSON `LoadingFinished` |
| **Operation theo phạm vi (mong đợi)** | **53** | đếm trực tiếp từ `/api/schema/` |
| **Operation được chọn (thực tế)** | **53** | NDJSON `LoadingFinished` |
| Đối chiếu mong đợi/thực tế | KHỚP | so sánh 2 dòng trên |
| Tổng thời gian chạy (giây) | 189.73 | NDJSON `EngineFinished` |
| Lý do dừng | completed | NDJSON `EngineFinished` |
| `<testcase>` trong JUnit | 54 | JUnit XML `tests=` |
| Failures trong JUnit | 53 | JUnit XML `failures=` |
| Errors trong JUnit | 0 | JUnit XML `errors=` |
| Skipped trong JUnit | 0 | JUnit XML `skipped=` |
| Testcase sinh ra (CLI) | 2016 | bảng tổng kết CLI |
| Testcase phát hiện lỗi (CLI) | 108 | bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **136** | bảng tổng kết CLI |
| Scenario đã chạy / bỏ qua / lỗi | 668 / 241 / 159 | NDJSON `Scenario*` |

> Ghi nhớ khi đọc số: `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho mỗi
> operation, **không phải** số request đã gửi; số `<testcase>` là số operation × check được ánh
> xạ, không phải số request; **unique failures không phải số bug** — nhiều failure có thể chung
> một nguyên nhân, và một nguyên nhân có thể sinh nhiều failure.

## 2. Phân loại lỗi theo check (đọc từ bảng tổng kết CLI)

| Check bị vi phạm | Số lỗi khác nhau |
|---|---|
| Server error | 17 |
| Response violates schema | 20 |
| API rejected schema-compliant request | 23 |
| Undocumented Content-Type | 3 |
| Undocumented HTTP status code | 72 |
| Unsupported methods | 1 |
| **Tổng** | **136** |

## 3. Lý do bỏ qua scenario (NDJSON)

- không ghi lý do: 188
- No examples in schema: 53

## 4. Phases đã chạy

- Thực chạy: probing, schema_analysis, auth_bootstrap, examples, coverage, fuzzing, stateful
- Không chạy: không có

## 5. File bằng chứng (đường dẫn tương đối trong repo)

- Log CLI đã làm sạch token: `results/TV1_round3_seed101.log`
- JUnit XML: `results/TV1_round3_seed101.xml`
- NDJSON (sự kiện thô): `results/TV1_round3_seed101.ndjson`

> Token đã bị thay bằng `[REDACTED]` trong mọi file kết quả (số vị trí đã thay ở XML/NDJSON: 8).
