# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV1 VÒNG 2 (seed 101)

- **Người chạy:** Trần Gia Huy (TV1) — Windows 11, Docker Desktop
- **Thời điểm chạy:** 2026-10-18 16:15:42
- **Hệ thống được test:** `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`), chạy local tại `http://localhost:8000`
- **Công cụ:** schemathesis, version 4.30.1 | Python 3.13.15 | Hypothesis 6.170.1
- **Ý nghĩa vòng 2:** mọi method, chỉ trên 3 nhóm metadata
- **Phạm vi (regex đường dẫn):** `^/api/(tags|correspondents|document_types)/`
- **Method loại trừ:** không loại trừ
- **Phases:** mặc định của Schemathesis 4.30.1 (không truyền cờ --phases)
- **Checks:** all
- **Cấu hình sinh:** `--seed 101`, `--max-examples 25`, `--workers 1`, `--mode all`
- **Exit code CLI:** `1` (1 = có vi phạm được phát hiện)

Lệnh đã chạy (token đã bị Schemathesis lọc thành `[Filtered]`):

```bash
st run http://localhost:8000/api/schema/ --url http://localhost:8000 --include-path-regex ^/api/(tags|correspondents|document_types)/ --seed 101 --max-examples 25 --workers 1 --mode all --header Authorization: [Filtered] --report junit,ndjson --report-junit-path D:\KTPM\results\TV1_round2_seed101.xml --report-ndjson-path D:\KTPM\results\TV1_round2_seed101.ndjson --output-sanitize true --no-color --checks all
```

## 1. Số liệu đọc từ chính file kết quả

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Operation có trong schema | 163 | NDJSON `LoadingFinished` |
| **Operation theo phạm vi (mong đợi)** | **18** | đếm trực tiếp từ `/api/schema/` |
| **Operation được chọn (thực tế)** | **18** | NDJSON `LoadingFinished` |
| Đối chiếu mong đợi/thực tế | KHỚP | so sánh 2 dòng trên |
| Tổng thời gian chạy (giây) | 194.09 | NDJSON `EngineFinished` |
| Lý do dừng | completed | NDJSON `EngineFinished` |
| `<testcase>` trong JUnit | 19 | JUnit XML `tests=` |
| Failures trong JUnit | 19 | JUnit XML `failures=` |
| Errors trong JUnit | 0 | JUnit XML `errors=` |
| Skipped trong JUnit | 0 | JUnit XML `skipped=` |
| Testcase sinh ra (CLI) | 1863 | bảng tổng kết CLI |
| Testcase phát hiện lỗi (CLI) | 52 | bảng tổng kết CLI |
| **Lỗi khác nhau (unique failures, CLI)** | **58** | bảng tổng kết CLI |
| Scenario đã chạy / bỏ qua / lỗi | 582 / 181 / 81 | NDJSON `Scenario*` |

> Ghi nhớ khi đọc số: `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho mỗi
> operation, **không phải** số request đã gửi; số `<testcase>` là số operation × check được ánh
> xạ, không phải số request; **unique failures không phải số bug** — nhiều failure có thể chung
> một nguyên nhân, và một nguyên nhân có thể sinh nhiều failure.

## 2. Phân loại lỗi theo check (đọc từ bảng tổng kết CLI)

| Check bị vi phạm | Số lỗi khác nhau |
|---|---|
| Response violates schema | 14 |
| API accepted schema-violating request | 5 |
| API rejected schema-compliant request | 12 |
| Undocumented HTTP status code | 27 |
| **Tổng** | **58** |

## 3. Lý do bỏ qua scenario (NDJSON)

- không ghi lý do: 163
- No examples in schema: 18

## 4. Phases đã chạy

- Thực chạy: probing, schema_analysis, auth_bootstrap, examples, coverage, fuzzing, stateful
- Không chạy: không có

## 5. File bằng chứng (đường dẫn tương đối trong repo)

- Log CLI đã làm sạch token: `results/TV1_round2_seed101.log`
- JUnit XML: `results/TV1_round2_seed101.xml`
- NDJSON (sự kiện thô): `results/TV1_round2_seed101.ndjson`

> Token đã bị thay bằng `[REDACTED]` trong mọi file kết quả (số vị trí đã thay ở XML/NDJSON: 0).
