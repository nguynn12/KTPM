# TV1 — KẾT QUẢ CHẠY THẬT 3 VÒNG SCHEMATHESIS (seed 101)

> File này là bản **đã điền số liệu thật**, thay cho bản mẫu `results/TV1_seed101_mau.md`.
> Mọi con số dưới đây đọc trực tiếp từ các file kết quả trong `results/` (JUnit XML, NDJSON, log CLI)
> — không nhập tay và không suy đoán. Tóm tắt tự động của từng vòng:
> `results/TV1_round1_seed101_summary.md`, `TV1_round2_seed101_summary.md`, `TV1_round3_seed101_summary.md`.

## 1. Môi trường và phiên bản

| Mục | Giá trị |
|---|---|
| Người chạy, ngày chạy | Trần Gia Huy (TV1) — 18/10/2026 |
| Hệ điều hành | Windows 11, RAM 15.7 GB, Docker Desktop |
| Docker / Compose | Docker 29.8.0, Compose v5.5.1 |
| Paperless-ngx | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`) |
| Schemathesis | `4.30.1` (Python 3.13.15, Hypothesis 6.170.1) |
| Địa chỉ test | `http://localhost:8000` — chỉ máy cục bộ, không gửi request ra Internet |
| Tài khoản | `admin` / `admin` |
| Seed | **101** |

## 2. Quy trình đã thực hiện

1. `docker compose up -d` → 3 container Up (`paperless-webserver` healthy, `paperless-db`, `paperless-broker`), port 8000.
2. Dựng baseline đúng chuẩn nhóm bằng `scripts/prepare_baseline_TV1.py` (reset → seed → xác nhận):
   2 tài liệu đã OCR (`Hoa don dien T9/2026`, `Bao cao tuan 41`), 3 tag, 2 correspondent, 2 document type;
   kiểm tra lại 3 luồng nghiệp vụ: `?query=dien` → 1 kết quả, `?tags__id__in=<hoa-don>` → 1 kết quả.
3. Chạy từng vòng: `.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round N`
   (runner tự lấy token, tự che token trong mọi file kết quả, tự đếm lại số operation từ schema để đối chiếu).
4. Vì vòng 2 và vòng 3 có method thay đổi dữ liệu, **giữa các vòng phải chạy lại bước 2** rồi mới chạy vòng tiếp theo.

### Phát hiện khi chuẩn bị chạy (quan trọng cho cả nhóm)

Cách lọc của Schemathesis 4.30.1 khác với ghi chú trong `docs/CLI_STANDARD_TV3.md`, đã đo thực nghiệm:

| Cách lọc | Số operation được chọn |
|---|---|
| `--include-path-regex <4 nhóm>` (mọi method) | 53 |
| `--include-method GET` (toàn schema) | 65 |
| `--include-path-regex <4 nhóm>` **+** `--include-method GET` | **99** ← hai cờ `--include-*` bị ghép **OR** |
| `--exclude-method POST` (một giá trị, đứng cùng `--include-path-regex`) | 34 |
| `--exclude-method POST,PUT,PATCH,DELETE` (danh sách CSV trong 1 cờ) | 53 ← **không có tác dụng** |
| `--exclude-method` **lặp 4 lần** (mỗi lần 1 giá trị) | **19** ← cách đúng |

Hệ quả: lệnh "vòng 1 chỉ GET" nếu viết `--include-path-regex … --include-method GET` sẽ **không** giới hạn
được method (thực chất fuzz cả POST/PUT/PATCH/DELETE ra ngoài 4 nhóm tài nguyên). Vì vậy kết quả vòng 1 của
TV1 dùng cách lọc đúng (19 operation, chỉ GET) — xem chi tiết ở mục 3 và `docs/ONBOARDING_TV1.md` §10.

## 3. Bảng tổng hợp 3 vòng

| Mục | Vòng 1 | Vòng 2 | Vòng 3 |
|---|---|---|---|
| Phạm vi | chỉ đọc (GET), 4 nhóm tài nguyên | mọi method, 3 nhóm metadata | mọi method, 4 nhóm tài nguyên |
| Regex đường dẫn | `^/api/(tags\|correspondents\|document_types\|documents)/` | `^/api/(tags\|correspondents\|document_types)/` | `^/api/(tags\|correspondents\|document_types\|documents)/` |
| Method loại trừ | POST, PUT, PATCH, DELETE | không | không |
| Phases thực chạy | examples, fuzzing | examples, coverage, fuzzing, stateful | examples, coverage, fuzzing, stateful |
| Checks | 5 check quy ước | all | all |
| **Operation được chọn / tổng schema** | **19 / 163** | **18 / 163** | **53 / 163** |
| Test case sinh ra (CLI) | 99 | 1863 | 2016 |
| Test case phát hiện lỗi (CLI) | 16 | 52 | 108 |
| **Lỗi khác nhau (CLI)** | **20** | **58** | **136** |
| `<testcase>` trong JUnit | 19 | 19 | 54 |
| Failures trong JUnit | 16 | 19 | 53 |
| Errors trong JUnit | 0 | 0 | 0 |
| Thời gian chạy (NDJSON) | 9.41 s | 194.09 s | 189.73 s |
| Exit code | 1 | 1 | 1 |
| File log | `results/TV1_round1_seed101.log` | `results/TV1_round2_seed101.log` | `results/TV1_round3_seed101.log` |

Số operation ở cột "được chọn" do runner **đếm lại từ chính `/api/schema/`** rồi đối chiếu với NDJSON
(`LoadingFinished.statistic.operations.selected`) — cả 3 vòng đều KHỚP, không có operation nào lọt ngoài phạm vi.

## 4. Phân loại lỗi theo check (số của chính Schemathesis)

| Check bị vi phạm | Vòng 1 | Vòng 2 | Vòng 3 | Tổng |
|---|---|---|---|---|
| Server error | 4 | 0 | 17 | 21 |
| Response violates schema | 4 | 14 | 20 | 38 |
| Undocumented HTTP status code | 9 | 27 | 72 | 108 |
| Undocumented Content-Type | 3 | 0 | 3 | 6 |
| API accepted schema-violating request | 0 | 5 | 0 | 5 |
| API rejected schema-compliant request | 0 | 12 | 23 | 35 |
| Unsupported methods | 0 | 0 | 1 | 1 |
| **Tổng lỗi khác nhau** | **20** | **58** | **136** | **214** |

Cách đọc số cho đúng:

- `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho **mỗi operation**, không phải số request đã gửi.
- `<testcase>` trong JUnit là số operation (× nhóm check) được ánh xạ; JUnit chỉ ghi **1** `<failure>` đại diện cho mỗi testcase, nên số failure trong JUnit **nhỏ hơn** số "lỗi khác nhau" mà CLI đếm (ví dụ vòng 3: JUnit 53 testcase lỗi / CLI 136 lỗi khác nhau).
- **Lỗi khác nhau không phải số bug**: 214 lỗi khác nhau của cả 3 vòng chỉ quy về một số nguyên nhân gốc (mục 6). Phần lớn là lỗi **tài liệu OpenAPI** (schema ghi thiếu mã trạng thái/Content-Type), còn lỗi chức năng đã xác nhận là BUG-04.

## 5. Lỗi thật đã xác nhận thủ công ngoài công cụ

| Nhóm lỗi | Số testcase (JUnit) | Đã xác nhận lại bằng tay? |
|---|---|---|
| HTTP 500 khi `{id}` không phải số → **BUG-04** | 16 (vòng 1: 4, vòng 3: 12) | **Có** — server trả 500 và log có traceback `ValueError` |
| Mã trạng thái 404/400/403 không có trong tài liệu → **BUG-05** | 61 | Có — gọi lại bằng `curl`/HTTP thấy đúng mã đó |
| Response thiếu trường bắt buộc `permissions` / `last_correspondence` → **BUG-06** | 4 | Có — so response thật với `required` trong schema |
| Content-Type `application/pdf`, `image/webp` không có trong tài liệu | 3 | Có — đúng như docs ghi cho `download`/`preview`/`thumb` |
| "API rejected schema-compliant request" (dữ liệu công cụ sinh) | 35 | **Chưa** — cần kiểm tra lại, có thể là false positive do dữ liệu vô lý |

## 6. File bằng chứng

| Vòng | Log | JUnit XML | NDJSON | Tóm tắt |
|---|---|---|---|---|
| 1 | `results/TV1_round1_seed101.log` | `results/TV1_round1_seed101.xml` | `results/TV1_round1_seed101.ndjson` | `results/TV1_round1_seed101_summary.md` |
| 2 | `results/TV1_round2_seed101.log` | `results/TV1_round2_seed101.xml` | `results/TV1_round2_seed101.ndjson` | `results/TV1_round2_seed101_summary.md` |
| 3 | `results/TV1_round3_seed101.log` | `results/TV1_round3_seed101.xml` | `results/TV1_round3_seed101.ndjson` | `results/TV1_round3_seed101_summary.md` |

Báo cáo lỗi: `docs/bugs/BUG-04.md`, `docs/bugs/BUG-05.md`, `docs/bugs/BUG-06.md`
(BUG-01 → BUG-03 là lỗi của TV2, TV1 không sửa).

Đã kiểm tra: **không** có token hay mật khẩu trong bất kỳ file kết quả nào
(Schemathesis tự lọc header `Authorization: [Filtered]`; runner thay thêm chuỗi token bằng `[REDACTED]`).

> Lưu ý: các file `.log` (log CLI) bị `.gitignore` chặn (`*.log`) nên **chỉ có trên máy TV1**;
> bằng chứng nằm trong repo là `.xml` (JUnit), `.ndjson` (sự kiện thô) và `_summary.md` của từng vòng —
> giống cách TV2/TV3 lưu kết quả.

## 7. Việc nhóm cần thống nhất

1. `docs/CLI_STANDARD_TV3.md`: cặp cờ `--include-path-regex` + `--include-method` bị ghép OR nên phạm vi vòng 1
   ghi trong tài liệu (99 operation) thực chất không phải "chỉ GET trên 4 nhóm tài nguyên" (đúng ra là 19).
   TV1 đã chạy theo cách lọc đúng.
2. `scripts/reset_data.py` (bản của TV2): chỉ xoá trang đầu của API (API có phân trang) nên **còn sót bản ghi**
   (đã gặp thật: sót 2 correspondent sau reset). TV1 dùng `scripts/prepare_baseline_TV1.py` có xử lý phân trang.
3. Cần biểu quyết thống nhất danh sách lỗi chính thức của nhóm trước khi nộp.
