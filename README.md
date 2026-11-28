# KTPM — Paperless-ngx + Schemathesis 

## Bản nộp cuối kỳ

Bản này tập hợp cấu hình Docker Compose, README và các kết quả đã lưu của năm thành viên. Dùng Windows PowerShell và Docker Desktop với WSL2. Paperless-ngx dùng tag 3.1.3 (commit d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e). Môi trường Python tham chiếu là 3.13.15; dependencies trong requirements.txt ghim Schemathesis 4.30.1 và Requests 2.34.2.

Để kiểm tra vận hành cục bộ, sao chép .env.example thành .env, cấu hình tài khoản thử và chạy docker compose config --quiet, docker compose up -d, docker compose ps theo các mục cài đặt dưới đây. Đợi dịch vụ hoạt động trước khi mở giao diện và OpenAPI. Các ca đọc có thể kiểm tra trực tiếp từ giao diện API bằng dữ liệu mẫu. Xem [kết quả chức năng và giá trị biên đã xác minh](docs/FINAL_FUNCTIONAL_VERIFICATION.md).

Runner tham chiếu là scripts/run_round_TV1.py. Hồ sơ TV1 có bằng chứng chạy sạch với đúng phiên bản đã ghim. Cả hai bản run_round.py của TV2 và TV4 đều dùng tên tệp cố định theo vòng/seed và không phải điểm vào mặc định của bản nộp. Tệp tại đường dẫn cũ giữ bản TV2 để đối chiếu; bản TV4 còn ở commit 65ebf18. Khi thực thi lại, dùng checkout và stack thử nghiệm riêng để đầu ra mới không ghi đè nguồn lịch sử.

- [Đối chiếu seed 202](results/TV2_DOI_CHIEU_SEED202.md)
- [Đối chiếu seed 303](docs/TV3_DOI_CHIEU_SEED303.md)
- [Minh chứng vận hành seed 404](docs/TV4_MINH_CHUNG_VAN_HANH.md)
- [Đối chiếu seed 505](docs/TV5_DOI_CHIEU_SEED505_VA_PHAT_HIEN.md)
- [Hồ sơ cài sạch seed 101](results/TV1_cleanenv_verify.md)

## 1. Yêu cầu môi trường

| Hạng mục | Tối thiểu / khuyến nghị | Đã dùng khi xác minh 26/11/2026 |
|---|---|---|
| OS | Windows 10/11 + WSL2, Ubuntu 22.04+, hoặc macOS 13+ | Windows 11 Home Single Language |
| RAM | 8 GB (khuyến nghị 16 GB) | 15.7 GB |
| Dung lượng trống | 10 GB (image Paperless ~3.5 GB + volume) | C: 109.2 GB, D: 118.6 GB |
| Docker | Docker Engine/Desktop ≥ 24, có Compose v2 | Docker 29.8.0, Compose v5.5.1 |
| Python (chạy Schemathesis) | **3.11 – 3.13** (nhóm chốt 3.13) | Python 3.13.15 |
| Mạng | Cần Internet lần đầu để pull image + cài pip | Đã pull GHCR/Docker Hub và PyPI thành công |
| Cổng | `8000` trống, hoặc đổi port và `PAPERLESS_URL` | `8000` bị stack cũ chiếm → xác minh dùng `8013` |

Kiểm tra nhanh bằng script có sẵn:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_env_TV1.ps1   # Windows
bash scripts/check_env_TV1.sh                                        # WSL/Ubuntu/macOS
```

Script kiểm tra Docker/Compose/daemon, Python 3.13, venv, Schemathesis, RAM, dung lượng đĩa
và cổng 8000. Kết quả mẫu của lần xác minh:

```text
[OK]   Docker: Docker version 29.8.0, build 88096ef
[OK]   Docker Compose: Docker Compose version v5.5.1
[OK]   Docker daemon: RUNNING
[OK]   Python 3.13: Python 3.13.15
[WARN] Port 8000: DANG BI CHIEM -> doi ports + PAPERLESS_URL hoac dung port khac
```

> **Lưu ý Python 3.14/3.15:** PyPI có thể chưa có wheel `pyyaml` cho bản quá mới, khiến
> `pip install schemathesis` cố biên dịch và báo `Microsoft Visual C++ 14.0 or greater is required`.
> Dùng Python 3.13 (`winget install -e --id Python.Python.3.13`) rồi tạo venv bằng `py -3.13`.

---

## 2. Phiên bản ghim và nguồn cài đặt

### 2.1. Paperless-ngx

| Mục | Giá trị đã xác minh |
|---|---|
| Repo nguồn | https://github.com/paperless-ngx/paperless-ngx |
| Tag | **`v3.1.3`** (annotated tag object `cbd6b56c9f0eb7261c903cf5ccdbe124d433e995`) |
| Commit được tag trỏ tới | **`d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`** |
| Image Docker | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` |
| Image digest | `sha256:aa810a36942c63d4ee70d00eda7236cd3d6acfb7eb3f7987fb568ed14df8817a` |
| Label trong image | `org.opencontainers.image.version=3.1.3`, `org.opencontainers.image.revision=d48663e9...` |
| PostgreSQL | `postgres:16-alpine` |
| Redis | `redis:7-alpine` |
| Port mặc định | `8000` → http://localhost:8000 |

Lệnh kiểm chứng :

```bash
git ls-remote --tags https://github.com/paperless-ngx/paperless-ngx.git \
  refs/tags/v3.1.3 refs/tags/v3.1.3^{}
# cbd6b56c9f0eb7261c903cf5ccdbe124d433e995  refs/tags/v3.1.3        (tag object)
# d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e  refs/tags/v3.1.3^{}     (commit that tag points to)

docker image inspect ghcr.io/paperless-ngx/paperless-ngx:3.1.3 \
  --format '{{json .Config.Labels}}'
# ... "org.opencontainers.image.revision":"d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e"
# ... "org.opencontainers.image.version":"3.1.3"
```

> Vì `v3.1.3` là **annotated tag**, `git ls-remote` in ra 2 dòng: dòng `refs/tags/v3.1.3`
> là tag object, dòng `refs/tags/v3.1.3^{}` mới là commit thật. Cả hai khớp với label image;
> không dùng `latest`.

### 2.2. Schemathesis

| Mục | Giá trị đã xác minh |
|---|---|
| Phiên bản | **`4.30.1`** |
| Nguồn cài đặt | PyPI chính thức: https://pypi.org/project/schemathesis/4.30.1/ |
| Gói tải về | `schemathesis-4.30.1-py3-none-any.whl` |
| Python theo PyPI | `Requires-Python >=3.10`; nhóm chốt chạy bằng Python **3.13** |
| Cài đặt | `pip install "schemathesis==4.30.1"` |
| Kiểm tra | `schemathesis --version` → `schemathesis, version 4.30.1` |
| Thư viện kèm theo (lần xác minh) | Hypothesis `6.170.17`, requests `2.34.2` |

Danh sách dependency của repo: [`requirements.txt`](requirements.txt) (đã ghim `schemathesis==4.30.1`).
Cấu hình Docker: [`docker-compose.yml`](docker-compose.yml) và [`.env.example`](.env.example).

---

## 3. Lấy mã nguồn

```powershell
git clone https://github.com/nguynn12/KTPM.git
cd KTPM
git checkout TV1_TranGiaHuy
git log --oneline -5
```

Kiểm tra image trong compose phải là tag đã ghim, **không** phải `latest`:

```powershell
Select-String -Path docker-compose.yml -Pattern "image:"
# ghcr.io/paperless-ngx/paperless-ngx:3.1.3
```

---

## 4. Tạo `.env` từ `.env.example`

`.env.example` là file mẫu **không chứa secret thật**. Tạo `.env` rồi sửa các giá trị bắt buộc:

**PowerShell (Windows):**

```powershell
Copy-Item .env.example .env
notepad .env
```

**Bash / WSL / macOS:**

```bash
cp .env.example .env
nano .env
```

Các giá trị **bắt buộc đổi** trong `.env`:

| Biến | Ý nghĩa | Việc phải làm |
|---|---|---|
| `PAPERLESS_SECRET_KEY` | Khóa ký session/token | Sinh chuỗi ngẫu nhiên, không dùng giá trị mẫu |
| `PAPERLESS_ADMIN_USER` | Tên đăng nhập admin | Giữ `admin` hoặc đổi; các lệnh seed/token bên dưới phải dùng đúng tên này |
| `PAPERLESS_ADMIN_PASSWORD` | Mật khẩu admin tạo tự động lần đầu | Đổi khỏi `admin`, dùng mật khẩu mạnh |
| `PAPERLESS_URL` | URL công khai của hệ thống | Giữ `http://localhost:8000` nếu dùng port 8000; đổi nếu dùng port khác |
| `PAPERLESS_TIME_ZONE` | Múi giờ | `Asia/Ho_Chi_Minh` |
| `PAPERLESS_OCR_LANGUAGE` | Ngôn ngữ OCR | `eng` với bộ seed hiện tại; `vie` nếu thêm tài liệu tiếng Việt |

Sinh `PAPERLESS_SECRET_KEY`:

```powershell
py -3.13 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Sau khi sửa, kiểm tra nhanh (không in secret ra màn hình):

```powershell
Select-String -Path .env -Pattern '^PAPERLESS_(SECRET_KEY|ADMIN_PASSWORD)=' |
  ForEach-Object { ($_.Line -replace '=.*','=<REDACTED>') }
```

> `.env` đã nằm trong [`.gitignore`](.gitignore). **Không** commit `.env`, token, mật khẩu.
>
> **Nếu dùng bản compose pin tách cấu hình** (`docker/docker-compose.pinned.yml`): ngoài `.env`
> còn cần `docker-compose.env` từ `docker/docker-compose.env.example` (xem
> `docs/ONBOARDING_TV1.md`). README này xác minh theo hướng đơn giản hơn: compose gốc + `.env`.

---

## 5. Dựng Docker Compose

```powershell
docker compose pull
docker compose up -d
docker compose ps
```

Kỳ vọng: 3 container `paperless-webserver`, `paperless-db`, `paperless-broker` ở trạng thái
`Up`; `paperless-webserver` chuyển `healthy` sau khoảng 30–90 giây.

```powershell
# Chờ đến khi webserver healthy (PowerShell)
docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" paperless-webserver
```

Nếu cổng 8000 đã bị chiếm:

1. Sửa `ports` trong `docker-compose.yml`, ví dụ `"8013:8000"`.
2. Sửa `PAPERLESS_URL` trong `.env` thành `http://localhost:8013`.
3. Chạy lại `docker compose up -d`, và dùng port mới ở mọi lệnh bên dưới.

> Lần xác minh 26/11/2026 đã gặp đúng trường hợp này: stack Paperless cũ đang giữ port 8000.
> Môi trường sạch được dựng ở **port 8013** với project/volume riêng (`tv1verify`).

Nếu `.env` đã có `PAPERLESS_ADMIN_USER` / `PAPERLESS_ADMIN_PASSWORD`, admin được tạo tự động
ở lần khởi động đầu. Nếu cần tạo tay:

```powershell
docker compose run --rm webserver createsuperuser
```

Đổi mật khẩu về sau:

```powershell
docker compose exec webserver python3 manage.py changepassword admin
```

---

## 6. Kiểm tra dịch vụ và OpenAPI

### 6.1. Trang web và Swagger

Mở http://localhost:8000 (hoặc port đã đổi) → trang đăng nhập.
Swagger UI: http://localhost:8000/api/schema/view/.
Schema thô: http://localhost:8000/api/schema/.

### 6.2. Kiểm tra bằng lệnh

```powershell
# Schema tho: ky vong HTTP 200, ~340.696 byte, OpenAPI 3.0.3
curl.exe -s -o NUL -w "schema_http=%{http_code} bytes=%{size_download}`n" http://localhost:8000/api/schema/
curl.exe -s -o NUL -w "swagger_http=%{http_code}`n" http://localhost:8000/api/schema/view/
```

Kết quả đã xác minh trên môi trường sạch:

| Chỉ số | Giá trị |
|---|---|
| `GET /api/schema/` | `200`, `application/vnd.oai.openapi`, `340696` byte |
| `GET /api/schema/view/` | `200` |
| Phiên bản OpenAPI | `3.0.3` |
| `info.version` | `6.0.0 (10)` |
| Số path | `93` |
| Số operation | `163` |

Kiểm tra phiên bản Paperless **đúng cách** trong container:

```powershell
docker compose exec webserver cat /usr/src/paperless/src/paperless/version.py
# __version__ = (3, 1, 3)

# Hoac:
docker compose exec webserver python3 -c "from paperless.version import __full_version_str__; print(__full_version_str__)"
# 3.1.3
```

> **Đã sửa lỗi tài liệu cũ:** lệnh `python -c "import paperless; print(paperless.__version__)"`
> **không chạy** (module `paperless` không export `__version__`). Dùng một trong hai lệnh trên.

### 6.3. Lấy token API (không in ra log/commit)

```powershell
$body = @{ username = "admin"; password = "<MAT_KHAU>" } | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/token/ `
  -ContentType "application/json" -Body $body).token
# Dung: Authorization: Token $token
```

Không dán token/mật khẩu vào chat, file markdown hoặc commit. Runner của TV1 tự lấy token và
tự thay token bằng `[REDACTED]` trong mọi file kết quả.

---

## 7. Chuẩn bị dữ liệu mẫu

Bộ seed của TV1: **seed 101** — 6 PDF trong `scripts/sample_docs/`, 3 tag, 2 correspondent,
2 document type. Chi tiết: [`docs/SEED_DATA_TV1.md`](docs/SEED_DATA_TV1.md).

### Cách A — Baseline nhanh (đã dùng khi xác minh)

Tạo 2 tài liệu đã OCR + metadata + gắn tag/correspondent/document_type:

```powershell
$env:PAPERLESS_URL="http://localhost:8000"
$env:PAPERLESS_ADMIN_USER="admin"
$env:PAPERLESS_ADMIN_PASSWORD="<MAT_KHAU>"
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
```

Kết quả kỳ vọng:

```text
documents=2 tags=3 correspondents=2 document_types=2
search 'dien'      -> count=1 ids=[...]
lọc tag 'hoa-don'  -> count=1 ids=[...]
```

> `admin` ở trên phải trùng `PAPERLESS_ADMIN_USER` trong `.env` (mặc định `admin`).
> Nếu đã đổi username, dùng đúng giá trị đó cho mọi lệnh seed/token.
>
> ⚠️ **CẢNH BÁO XÓA DỮ LIỆU:** `prepare_baseline_TV1.py` **reset trước rồi mới seed**.
> Nó xóa toàn bộ documents / tags / correspondents / document_types qua API (giữ user admin).
> **Chỉ chạy trên môi trường thử nghiệm.** Không chạy trên dữ liệu thật.

### Cách B — Nạp đủ 6 PDF

```powershell
# Cach 1: keo-tha 6 file trong scripts/sample_docs/ vao giao dien web
# Cach 2: copy vao thu muc consume de he thong tu OCR
Copy-Item scripts\sample_docs\TV1_Sample_*.pdf .\consume\
docker compose logs --tail=30 webserver
```

Sau đó tạo metadata (script này **không** reset, chỉ tạo nếu chưa có):

```powershell
.\.venv\Scripts\python.exe scripts\seed_and_verify_flows_TV1.py `
  --base-url http://localhost:8000 --username admin --password "<MAT_KHAU>"
```

---

## 8. Cài Schemathesis

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\schemathesis.exe --version
```

Kỳ vọng:

```text
schemathesis, version 4.30.1
```

Nguồn cài đặt đúng phiên bản: PyPI `schemathesis==4.30.1`
(https://pypi.org/project/schemathesis/4.30.1/). Không cài từ bản `latest` hoặc fork.

> Nếu gọi trực tiếp `schemathesis` trong PowerShell và gặp `UnicodeEncodeError: 'charmap'`,
> đặt `$env:PYTHONUTF8="1"` trước khi chạy. Runner `scripts/run_round_TV1.py` đã tự ép UTF-8
> cho tiến trình con, nên không cần đặt tay khi dùng runner.

---

## 9. Chạy bộ kiểm thử 3 vòng

Quy trình nhóm: **reset → seed → xác nhận baseline → chạy vòng**.

| Vòng | Phạm vi | Operation | Ghi chú |
|---|---|---|---|
| 1 | Chỉ GET trên `tags`, `correspondents`, `document_types`, `documents` | 19 | Chỉ đọc, không làm thay đổi dữ liệu |
| 2 | Mọi method trên 3 nhóm metadata | 18 | Có POST/PUT/PATCH/DELETE → phải reset trước |
| 3 | Mọi method trên cả 4 nhóm tài nguyên | 53 | Có thay đổi dữ liệu → phải reset trước |

```powershell
# Truoc vong 1 (neu chua seed)
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 1

# Truoc vong 2: BAT BUOC reset + seed lai
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 2

# Truoc vong 3: BAT BUOC reset + seed lai
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 3
```

Hoặc dùng wrapper PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_round_TV1.ps1 -Round 1
powershell -ExecutionPolicy Bypass -File scripts\run_round_TV1.ps1 -Round 2
powershell -ExecutionPolicy Bypass -File scripts\run_round_TV1.ps1 -Round 3
```

Runner tự:

- lấy token từ `/api/token/` (không in token);
- đếm lại operation từ `/api/schema/` và đối chiếu với NDJSON;
- che token/mật khẩu trong log, JUnit XML, NDJSON, summary.

Exit code `1` là **bình thường** khi Schemathesis phát hiện vi phạm; exit code `2` thường là
lỗi cấu hình/kết nối.

---

## 10. Tìm file kết quả

Mỗi vòng ghi 4 file vào `results/`:

| File | Nội dung |
|---|---|
| `results/TV1_round<N>_seed101.log` | Log CLI (bị `.gitignore` chặn `*.log` — chỉ có trên máy chạy) |
| `results/TV1_round<N>_seed101.xml` | JUnit XML |
| `results/TV1_round<N>_seed101.ndjson` | Sự kiện thô của Schemathesis |
| `results/TV1_round<N>_seed101_summary.md` | Bảng số liệu đọc từ chính XML/NDJSON/log |

Lần xác minh môi trường sạch dùng tên riêng, không ghi đè kết quả 18/10:

| File | Nội dung |
|---|---|
| `results/TV1_cleanenv_verify.md` | Báo cáo xác minh + kết luận |
| `results/TV1_cleanenv_verify.log` | Log tổng hợp đã che thông tin đăng nhập (được `git add` nhờ ngoại lệ trong `.gitignore`) |
| `results/TV1_cleanenv_round<N>_seed101.{xml,ndjson}` | JUnit XML + sự kiện thô, đã thay `<ADMIN>` và `<VERIFY_DIR>` |
| `results/TV1_cleanenv_round<N>_seed101_summary.md` | Tóm tắt từng vòng |

Xem nhanh:

```powershell
Get-Content results\TV1_round1_seed101_summary.md -Encoding UTF8
Get-ChildItem results\TV1_round*_seed101*
```

Báo cáo tổng hợp cũ (18/10/2026): [`results/TV1_ketqua_seed101.md`](results/TV1_ketqua_seed101.md).
Báo cáo xác minh môi trường sạch (26/11/2026): [`results/TV1_cleanenv_verify.md`](results/TV1_cleanenv_verify.md).

Khi đọc số, nhớ:

- `--max-examples 25` là giới hạn dữ liệu mỗi operation, **không phải** số request.
- `<testcase>` trong JUnit là operation × nhóm check, **không phải** số request.
- “Lỗi khác nhau” (unique failures) **không phải** số bug; nhiều failure có thể cùng nguyên nhân.

---

## 11. Reset / xóa dữ liệu — CHỈ DÙNG CHO MÔI TRƯỜNG THỬ NGHIỆM

> 🛑 **Các lệnh dưới đây xóa dữ liệu thật.** Chỉ chạy trên máy test/volume test.
> Không chạy trên production, không chạy khi chưa sao lưu.

| Lệnh / script | Xóa gì | Giữ lại gì |
|---|---|---|
| `docker compose down -v` | **Toàn bộ volume**: DB PostgreSQL, media, data, Redis | Không giữ dữ liệu nào |
| `scripts/prepare_baseline_TV1.py` | Xóa documents, tags, correspondents, document_types qua API | User admin |
| `scripts/reset_data.py` (dùng chung) | Xóa documents/tags/correspondents/document_types qua API | User admin |
| `scripts/reset_system.ps1` (dùng chung) | `docker compose down -v` + dựng lại | Không giữ dữ liệu |
| `docker system prune -a --volumes` | Xóa **mọi** image/container/volume không dùng của Docker | Có thể ảnh hưởng project khác — tránh dùng nếu không cần |

Quy trình reset đầy đủ (test only):

```powershell
docker compose down -v
docker compose up -d
# chờ healthy, sau đó tạo/seed lại dữ liệu:
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
```

Nếu chỉ muốn xóa dữ liệu qua API mà giữ container/DB:

```powershell
.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py
```

> Lần xác minh 26/11/2026 đã chạy `docker compose -p tv1verify down -v` trên **project biệt lập**
> `tv1verify` (volume `tv1verify_*`), không đụng volume `paperless-*`/`ktpm-group_*` hiện có.

---

## 12. Kết quả xác minh môi trường sạch (26/11/2026)

Môi trường: Windows 11, Docker 29.8.0 / Compose v5.5.1, Python 3.13.15, Schemathesis 4.30.1,
Paperless-ngx `3.1.3` (commit `d48663e`). Dựng bằng project/volume riêng `tv1verify`, port `8013`
để không đụng stack cũ đang giữ port 8000.

| Vòng | Operation chọn / schema | Testcase sinh ra | Unique failures | JUnit tests/failures | Thời gian |
|---|---|---|---|---|---|
| 1 | 19 / 163 | 130 | 18 | 19 / 15 | 7.78 s |
| 2 | 18 / 163 | 1288 | 53 | 19 / 19 | 86.61 s |
| 3 | 53 / 163 | 3146 | 139 | 54 / 53 | 183.19 s |

- Cả 3 vòng đều **KHỚP** số operation mong đợi (19/18/53).
- Exit code `1` ở cả 3 vòng (có vi phạm) — đúng kỳ vọng.
- Không phát hiện token/mật khẩu trong artifact; username admin đã được thay bằng `<ADMIN>`
  trong log công bố.
- Chi tiết lệnh + output + điểm còn vướng: [`results/TV1_cleanenv_verify.md`](results/TV1_cleanenv_verify.md).

> Số unique failures lần này (18/53/139) khác báo cáo 18/10 (20/58/136) vì môi trường sạch
> dùng Hypothesis `6.170.17` (bản cũ `6.170.1`) và dữ liệu/ID khác nhau. Đây là dao động bình
> thường của fuzzing; số operation và kết luận lỗi không đổi.

---

## 13. Điểm còn vướng / lưu ý sau khi chạy lại

1. **PowerShell cp1252:** `run_round_TV1.py` từng chết `UnicodeEncodeError` khi in tiếng Việt.
   Đã sửa bằng cách ép UTF-8 cho stdout/stderr và cho tiến trình con Schemathesis.
   Nếu gọi `schemathesis` trực tiếp, đặt `$env:PYTHONUTF8="1"`.
2. **Lệnh kiểm tra phiên bản trong tài liệu cũ sai:** `paperless.__version__` không tồn tại.
   Dùng `cat .../paperless/version.py` hoặc `from paperless.version import __full_version_str__`.
3. **Trùng tên container:** compose đặt `container_name: paperless-*` cố định, nên dựng project
   thứ hai sẽ báo `Conflict`. Khi cần môi trường sạch song song, phải đổi `container_name`
   (như lần xác minh đã đổi thành `tv1verify-*`) hoặc dừng stack cũ.
4. **Port 8000 có thể bị chiếm:** kiểm tra bằng `scripts/check_env_TV1.ps1`; đổi cả `ports`
   và `PAPERLESS_URL`, ghi lại port thực tế vào báo cáo.
5. **File `.log` bị `.gitignore` chặn:** log CLI từng vòng chỉ nằm trên máy chạy; bằng chứng
   commit được là `.xml`, `.ndjson`, `_summary.md`. Riêng log xác minh đã làm sạch
   `results/TV1_cleanenv_verify.log` được mở ngoại lệ trong `.gitignore` để nộp kèm.
6. **Ảnh/video minh chứng vẫn phải tự chụp:** agent không thể tạo ảnh đăng nhập/OCR/Swagger
   thật. Checklist nằm trong `results/TV1_deploy_13-10.md` và `docs/BUSINESS_FLOWS_TV1.md`.
7. **`scripts/reset_data.py` của TV2 chỉ xóa trang đầu API** (phân trang) nên có thể sót bản ghi.
   TV1 dùng `prepare_baseline_TV1.py` có xử lý phân trang. Khi reset bằng script dùng chung,
   kiểm tra lại số lượng bản ghi còn lại.

---

## 14. Tài liệu liên quan

| Tài liệu | Nội dung |
|---|---|
| [`docs/ONBOARDING_TV1.md`](docs/ONBOARDING_TV1.md) | Hướng dẫn cài chi tiết + xử lý sự cố |
| [`docs/PINNED_VERSION_TV1.md`](docs/PINNED_VERSION_TV1.md) | Tag/commit/image/Schemathesis đã ghim |
| [`docs/SEED_DATA_TV1.md`](docs/SEED_DATA_TV1.md) | Bộ seed 101 (PDF + metadata) |
| [`docs/BUSINESS_FLOWS_TV1.md`](docs/BUSINESS_FLOWS_TV1.md) | 3 luồng nghiệp vụ + lệnh API |
| [`results/TV1_ketqua_seed101.md`](results/TV1_ketqua_seed101.md) | Kết quả 3 vòng ngày 18/10/2026 |
| [`results/TV1_cleanenv_verify.md`](results/TV1_cleanenv_verify.md) | Xác minh môi trường sạch 26/11/2026 |
| [`results/TV1_deploy_13-10.md`](results/TV1_deploy_13-10.md) | Biên bản dựng hệ thống 13/10/2026 |
| [`docs/bugs/BUG-04.md`](docs/bugs/BUG-04.md) → [`BUG-06.md`](docs/bugs/BUG-06.md) | Lỗi TV1 phát hiện |

---

## 15. Quy tắc Git & an toàn

- Không commit `.env`, token, mật khẩu, `paperless-ngx/`, `.venv/`.
- Không commit log có chứa thông tin đăng nhập; runner đã che token nhưng vẫn phải kiểm tra lại.
- Mỗi thành viên commit trên nhánh/tài khoản của mình.
- Chỉ test trên `localhost`/`127.0.0.1`; không gửi request fuzzing ra Internet.
- Các bước reset/xóa dữ liệu chỉ dùng cho môi trường thử nghiệm.
