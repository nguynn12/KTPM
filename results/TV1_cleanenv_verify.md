# TV1 — XÁC MINH CÀI ĐẶT LẠI TRÊN MÔI TRƯỜNG SẠCH (26/11/2026)

> **Mục đích:** thử lại toàn bộ quy trình cài đặt/chạy lại trong README trên một môi trường
> **sạch, biệt lập**, ghi lại lệnh đã chạy, kết quả thực tế và các điểm còn vướng.
>
> **Người chạy:** Trần Gia Huy — TV1.
> **Máy:** Windows 11 Home Single Language, RAM 15.7 GB.
> **Log chi tiết (đã che thông tin đăng nhập):** [`TV1_cleanenv_verify.log`](TV1_cleanenv_verify.log).
> **Tóm tắt từng vòng:** [`TV1_cleanenv_round1_seed101_summary.md`](TV1_cleanenv_round1_seed101_summary.md),
> [`TV1_cleanenv_round2_seed101_summary.md`](TV1_cleanenv_round2_seed101_summary.md),
> [`TV1_cleanenv_round3_seed101_summary.md`](TV1_cleanenv_round3_seed101_summary.md).

---

## 1. Môi trường và phạm vi xác minh

| Hạng mục | Giá trị thực tế |
|---|---|
| OS | Windows 11 Home Single Language |
| Docker Engine | `Docker version 29.8.0, build 88096ef` |
| Docker Compose | `Docker Compose version v5.5.1` |
| Python | `Python 3.13.15` |
| Schemathesis | `schemathesis, version 4.30.1` (PyPI) |
| Hypothesis (kèm theo) | `6.170.17` |
| requests | `2.34.2` |
| Paperless-ngx | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` |
| Commit Paperless-ngx | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` |
| Project/volume | `tv1verify` (biệt lập, xóa sau khi xác minh) |
| Port dùng để test | `8013` (vì port 8000 đang bị stack Paperless cũ chiếm) |
| Seed | 101 |

### Vì sao dùng port 8013?

Khi bật Docker Desktop, stack `paperless-*` cũ (từ lần chạy trước) tự khởi động lại vì
`restart: unless-stopped` và giữ port 8000. Để **không xóa/không đụng dữ liệu cũ**, môi trường
sạch được dựng thành một project riêng:

- `--project-name tv1verify` → volume `tv1verify_data`, `tv1verify_media`, `tv1verify_pgdata`,
  `tv1verify_redisdata`.
- Đổi `ports: "8000:8000"` → `"8013:8000"` và `PAPERLESS_URL=http://localhost:8013`.
- Đổi `container_name: paperless-*` → `tv1verify-*` để tránh lỗi trùng tên container.

Đây cũng là một **điểm còn vướng** khi dựng song song: compose gốc dùng `container_name` cố định.

---

## 2. Các lệnh đã kiểm tra và kết quả thực tế

### 2.1. Kiểm tra môi trường trước khi cài

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_env_TV1.ps1
```

Kết quả thực tế:

```text
=== TV1 env check ===
OS: Microsoft Windows 11 Home Single Language
[OK]   Docker: Docker version 29.8.0, build 88096ef
[OK]   Docker Compose: Docker Compose version v5.5.1
[OK]   Docker daemon: RUNNING
[OK]   Python 3.13: Python 3.13.15
INFO  Python mac dinh: Python 3.13.15
[WARN] venv: CHUA CO -> py -3.13 -m venv .venv
[WARN] Schemathesis: CHUA CAI -> pip install "schemathesis==4.30.1"
[OK]   O dia C trong: 109.2 GB (can >= 10 GB)
[OK]   O dia D trong: 118.6 GB (can >= 10 GB)
[OK]   RAM: 15.7 GB (can >= 8 GB)
[WARN] Port 8000: DANG BI CHIEM -> doi ports + PAPERLESS_URL hoac dung port khac
```

> `venv`/`Schemathesis` báo chưa có vì lần kiểm tra này chạy trước khi tạo `.venv` trong thư mục
> xác minh; đây là kết quả đúng tại thời điểm chạy.

### 2.2. Xác minh tag/commit/image Paperless-ngx

```bash
git ls-remote --tags https://github.com/paperless-ngx/paperless-ngx.git \
  refs/tags/v3.1.3 refs/tags/v3.1.3^{}
```

Kết quả:

```text
cbd6b56c9f0eb7261c903cf5ccdbe124d433e995  refs/tags/v3.1.3        (tag object)
d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e  refs/tags/v3.1.3^{}     (commit được tag trỏ tới)
```

```powershell
docker image inspect ghcr.io/paperless-ngx/paperless-ngx:3.1.3 --format '{{json .Config.Labels}}'
docker image inspect ghcr.io/paperless-ngx/paperless-ngx:3.1.3 --format '{{json .RepoDigests}}'
```

Kết quả rút gọn:

```text
org.opencontainers.image.version  = 3.1.3
org.opencontainers.image.revision = d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e
RepoDigest = ghcr.io/paperless-ngx/paperless-ngx@sha256:aa810a36942c63d4ee70d00eda7236cd3d6acfb7eb3f7987fb568ed14df8817a
```

→ Tag, commit và label image **khớp nhau**. `v3.1.3` là annotated tag, nên phải đọc thêm dòng
`refs/tags/v3.1.3^{}` mới thấy commit thật.

### 2.3. Pull và dựng Docker Compose

```powershell
docker compose --project-name tv1verify pull
docker compose --project-name tv1verify up -d
docker compose --project-name tv1verify ps
```

Kết quả: pull thành công 3 image; 3 container lên và `webserver` chuyển `healthy` sau khoảng 60 giây.

```text
tv1verify-broker      redis:7-alpine                              Up ... 6379/tcp
tv1verify-db          postgres:16-alpine                          Up ... 5432/tcp
tv1verify-webserver   ghcr.io/paperless-ngx/paperless-ngx:3.1.3   Up ... (healthy) 0.0.0.0:8013->8000/tcp
```

### 2.4. Kiểm tra OpenAPI và phiên bản

```powershell
curl.exe -s -o NUL -w "schema_http=%{http_code} bytes=%{size_download}`n" http://localhost:8013/api/schema/
curl.exe -s -o NUL -w "swagger_http=%{http_code}`n" http://localhost:8013/api/schema/view/
```

Kết quả thực tế:

| Chỉ số | Giá trị |
|---|---|
| `GET /api/schema/` | `200`, `340696` byte, `application/vnd.oai.openapi; charset=utf-8` |
| `GET /api/schema/view/` | `200` |
| OpenAPI | `3.0.3` |
| `info.version` | `6.0.0 (10)` |
| Số path | `93` |
| Số operation | `163` |
| Operation vòng 1 (GET 4 resource) | `19` |
| Operation vòng 2 (3 metadata) | `18` |
| Operation vòng 3 (4 resource) | `53` |

Kiểm tra phiên bản trong container:

```powershell
docker compose --project-name tv1verify exec -T webserver cat /usr/src/paperless/src/paperless/version.py
```

Kết quả:

```text
__version__: Final[tuple[int, int, int]] = (3, 1, 3)
```

> Lệnh cũ `python -c "import paperless; print(paperless.__version__)"` **không chạy**
> (`AttributeError: module 'paperless' has no attribute '__version__'`). Đã sửa trong README và
> `docs/ONBOARDING_TV1.md` / `docs/PINNED_VERSION_TV1.md`.

### 2.5. Cài Schemathesis

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install requests "schemathesis==4.30.1"
.\.venv\Scripts\python.exe -m pip show schemathesis
.\.venv\Scripts\schemathesis.exe --version
```

Kết quả:

```text
Name: schemathesis
Version: 4.30.1
...
schemathesis, version 4.30.1
```

Nguồn: PyPI chính thức `https://pypi.org/project/schemathesis/4.30.1/`
(gói `schemathesis-4.30.1-py3-none-any.whl`, `Requires-Python >=3.10`).
Các gói kèm theo trong lần cài sạch: `requests 2.34.2`, `hypothesis 6.170.17`.

### 2.6. Nạp baseline seed 101

```powershell
$env:PAPERLESS_URL="http://localhost:8013"
$env:PAPERLESS_ADMIN_USER="<ADMIN>"
$env:PAPERLESS_ADMIN_PASSWORD="<PASSWORD>"
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
```

Kết quả thực tế:

```text
documents=2 tags=3 correspondents=2 document_types=2
search 'dien'      -> count=1 ids=[1]
lọc tag 'hoa-don'  -> count=1 ids=[1]
```

> `prepare_baseline_TV1.py` **xóa dữ liệu trước khi seed**. Chỉ dùng trên môi trường thử nghiệm.

### 2.7. Chạy 3 vòng Schemathesis

```powershell
# Vòng 1
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 1

# Vòng 2 (reset trước vì có method thay đổi dữ liệu)
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 2

# Vòng 3 (reset trước)
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 3
```

Kết quả tổng hợp:

| Vòng | Operation chọn / schema | Testcase sinh ra | Testcase phát hiện lỗi | Unique failures | JUnit tests / failures | Thời gian |
|---|---|---|---|---|---|---|
| 1 | **19 / 163** | 130 | 15 | **18** | 19 / 15 | 7.78 s |
| 2 | **18 / 163** | 1288 | 44 | **53** | 19 / 19 | 86.61 s |
| 3 | **53 / 163** | 3146 | 113 | **139** | 54 / 53 | 183.19 s |

Phân loại theo check:

| Check bị vi phạm | Vòng 1 | Vòng 2 | Vòng 3 |
|---|---|---|---|
| Server error | 2 | 0 | 17 |
| Response violates schema | 8 | 13 | 18 |
| Undocumented Content-Type | 3 | 0 | 3 |
| Undocumented HTTP status code | 5 | 27 | 72 |
| API accepted schema-violating request | 0 | 1 | 4 |
| API rejected schema-compliant request | 0 | 12 | 24 |
| Unsupported methods | 0 | 0 | 1 |
| **Tổng unique failures** | **18** | **53** | **139** |

- Cả 3 vòng đều **KHỚP** số operation mong đợi (19/18/53) — runner tự đếm lại từ `/api/schema/`
  và đối chiếu với NDJSON.
- Exit code `1` ở cả 3 vòng (có vi phạm) — đúng kỳ vọng.
- Scenario started / skipped / failed: vòng 1 `38 / 19 / 15`; vòng 2 `388 / 115 / 75`;
  vòng 3 `1027 / 410 / 166`.

> **Vì sao số khác báo cáo 18/10?** Báo cáo cũ ghi 20/58/136 unique failures với Hypothesis
> `6.170.1`. Lần này môi trường sạch cài Hypothesis `6.170.17` và dữ liệu/ID khác, nên số liệu
> dao động (18/53/139). Số operation, phạm vi và kết luận lỗi không đổi. Đây là đặc điểm bình
> thường của fuzzing, không phải lỗi cài đặt.

### 2.8. File kết quả

| File | Trạng thái |
|---|---|
| `results/TV1_cleanenv_verify.md` | Báo cáo này |
| `results/TV1_cleanenv_verify.log` | Log xác minh đã che thông tin đăng nhập |
| `results/TV1_cleanenv_round{1,2,3}_seed101_summary.md` | Tóm tắt máy sinh cho từng vòng |
| `results/TV1_cleanenv_round{1,2,3}_seed101.{xml,ndjson}` | Bằng chứng gốc của lần chạy 26/11 (đã che `<ADMIN>` + `<VERIFY_DIR>`) |
| `results/TV1_round{1,2,3}_seed101.{xml,ndjson}` | Bằng chứng gốc của lần chạy 18/10 (giữ nguyên) |
| `results/TV1_ketqua_seed101.md` | Báo cáo tổng hợp 18/10 |

> Trong thư mục tạm, runner ghi tên `TV1_round<N>_seed101.*`. Khi công bố, các file của lần
> 26/11 được đổi thành `TV1_cleanenv_round<N>_seed101.*` để **không ghi đè** kết quả 18/10.
> XML/NDJSON đã được thay username bằng ``<ADMIN>`` và đường dẫn tạm bằng ``<VERIFY_DIR>``
> trước khi đưa vào repo (trong XML, dấu `<` `>` được escape thành `&lt;` `&gt;` để XML hợp lệ).

### 2.9. Dọn môi trường thử nghiệm

```powershell
docker compose --project-name tv1verify down -v
```

Kết quả: toàn bộ container/network và 4 volume `tv1verify_*` đã bị xóa; không còn volume
`tv1verify_*`. Volume của stack cũ (`ktpm-group_*`, `paperless-*`) **không bị đụng tới**.

> Đây là bước **xóa dữ liệu test**. Chỉ chạy với project/volume test. Không chạy
> `docker compose down -v` trên môi trường có dữ liệu thật.

---

## 3. Kiểm tra rò rỉ thông tin đăng nhập

Đã quét toàn bộ file log/XML/NDJSON/Markdown được công bố:

| Loại thông tin | Kết quả |
|---|---|
| Mật khẩu admin | `0` hit trong file công bố (chỉ có trong file credential tạm, không đưa vào repo) |
| `PAPERLESS_SECRET_KEY` | `0` hit trong file công bố |
| Token dạng `Token <chuỗi dài>` | `0` hit |
| Tên đăng nhập admin | Đã thay bằng `<ADMIN>` trong log công bố |
| Đường dẫn tạm/userprofile | Đã thay bằng `<VERIFY_DIR>` / `<USERPROFILE>` |

Runner `run_round_TV1.py` cũng tự thay token/mật khẩu bằng `[REDACTED]` trong log, JUnit XML,
NDJSON và summary.

---

## 4. Điểm còn vướng / đã sửa trong lần chạy lại

| # | Vấn đề gặp thật | Xử lý |
|---|---|---|
| 1 | `run_round_TV1.py` chết `UnicodeEncodeError: 'charmap'` khi in tiếng Việt trên PowerShell cp437/cp1252 | Đã ép UTF-8 cho `stdout`/`stderr` và truyền `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` cho tiến trình con Schemathesis |
| 2 | Schemathesis CLI cũng chết `UnicodeEncodeError` khi in header Unicode | Cùng cách xử lý ở trên; nếu gọi trực tiếp, đặt `$env:PYTHONUTF8="1"` |
| 3 | Lệnh `paperless.__version__` trong tài liệu cũ không tồn tại | Đã sửa sang `cat version.py` hoặc `from paperless.version import __full_version_str__` |
| 4 | Trùng `container_name: paperless-*` khi dựng project thứ hai | Đã ghi chú; khi xác minh đã đổi thành `tv1verify-*` và dùng `--project-name` riêng |
| 5 | Port 8000 bị stack cũ chiếm | Đã dùng port 8013 + đổi `PAPERLESS_URL`; `check_env_TV1.ps1` nay cảnh báo port bận |
| 6 | `scripts/check_env_TV1.ps1` cũ không thấy Python 3.13/venv | Đã viết lại: kiểm tra `py -3.13`, venv, Schemathesis trong venv, dung lượng C/D, RAM, port 8000 |
| 7 | Số unique failures khác báo cáo cũ | Không phải lỗi cài đặt; do Hypothesis patch version và dữ liệu/ID khác. Đã ghi rõ trong báo cáo |
| 8 | File `.log` bị `.gitignore` chặn | Bằng chứng commit là `.xml`, `.ndjson`, `_summary.md`; riêng `TV1_cleanenv_verify.log` đã được mở ngoại lệ trong `.gitignore` vì đã che thông tin đăng nhập |
| 9 | `scripts/reset_data.py` của TV2 chỉ xóa trang đầu API | TV1 dùng `prepare_baseline_TV1.py` có xử lý phân trang; đã ghi chú khi dùng script chung |

---

## 5. Việc vẫn phải làm thủ công

- [ ] Chụp ảnh màn hình thật: `docker compose ps`, đăng nhập UI, tài liệu OCR, Swagger UI,
      kết quả search/lọc — lưu vào `docs/evidence/` (agent không tạo được ảnh thật).
- [ ] Quay video 1–3 phút chạy 3 luồng nghiệp vụ.
- [ ] Điền tên nhóm/MSSV/link Trello theo yêu cầu hành chính (nếu báo cáo cần).
- [ ] Nhóm thống nhất danh sách bug chính thức trước khi nộp.

---

## 6. Kết luận

- Quy trình trong `README.md` **chạy được từ đầu đến cuối** trên môi trường sạch biệt lập.
- Các mốc quan trọng đều đạt: 3/3 container healthy, OpenAPI `200` (340 696 byte, 93 path,
  163 operation), baseline đúng 2 tài liệu + metadata, 3 vòng Schemathesis đúng phạm vi
  19/18/53 operation.
- Không phát hiện token/mật khẩu trong artifact công bố.
- Các điểm còn vướng đã được sửa hoặc ghi rõ ở mục 4; phần ảnh/video vẫn cần người thật thực hiện.
