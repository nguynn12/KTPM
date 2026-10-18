# ONBOARDING_TV1 — Cài và chạy Paperless-ngx từ máy sạch (Phần C, H)

> Đối tượng: thành viên mới / máy mới hoàn toàn. Làm theo từ đầu đến cuối mất khoảng
> 30–60 phút (tùy tốc độ mạng khi pull image ~2–3 GB).
> Bản pin: xem `docs/PINNED_VERSION_TV1.md` (Paperless-ngx **v3.1.3**, Schemathesis **4.30.1**).
> Chỉ test trên `http://localhost:8000` — không gửi request ra Internet.
>
> Tài liệu này gộp bản TV1 viết ban đầu và phần hiệu đính ngày 12/10 (sửa 2 lệnh sai
> mà TV2 từng hướng dẫn: `manage.py set_password` / `manage.py create_api_token` — xem mục 6 và mục 12).

## 1. Yêu cầu máy

| Hạng mục | Tối thiểu | Máy của TV1 (đối chứng) |
|---|---|---|
| RAM | 8 GB | 15.7 GB |
| Ổ đĩa trống | 10 GB | 125.6 GB |
| OS | Win 10/11 + WSL2, hoặc Ubuntu 22.04+, hoặc macOS 13+ | Windows 11 + WSL2 (Ubuntu) |
| Docker Desktop | ≥ 4.30 (kèm Compose v2) | 29.8.0 / Compose v5.5.1 |
| Python (cho Schemathesis) | 3.11–3.13 | máy TV1 chưa có Python — dùng Docker để seed |

Kiểm tra nhanh bằng script có sẵn:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_env_TV1.ps1   # Windows
bash scripts/check_env_TV1.sh                                        # WSL/Ubuntu/macOS
```

## 2. Cài Docker Desktop (chỉ làm 1 lần)

1. Tải Docker Desktop tại https://www.docker.com/products/docker-desktop/ và cài đặt.
2. **Windows:** bật WSL2 + cài Ubuntu từ Microsoft Store. Trong Settings → Resources → WSL integration → bật Ubuntu.
3. Kiểm tra (mở terminal WSL / Ubuntu, **không** dùng PowerShell cho các bước sau):

```bash
docker --version          # kỳ vọng: Docker version 24+
docker compose version    # kỳ vọng: Docker Compose version v2+
```

> Lỗi thường gặp: `cannot connect to the Docker daemon` → mở Docker Desktop lên,
> đợi biểu tượng cá voi hết quay rồi chạy lại.

## 3. Lấy file compose đã pin (không dùng script install mặc định)

Script `install-paperless-ngx.sh` của hãng kéo `main`/`latest` nên nhóm **không** dùng.
Dùng bộ file đã pin sẵn trong repo này (`docker/docker-compose.pinned.yml` là bản sao
`docker-compose.yml` của nhóm, chỉ thêm dòng `env_file: docker-compose.env` để tách
phần cấu hình Paperless ra riêng):

```bash
git clone https://github.com/nguynn12/KTPM.git ktpm && cd ktpm
git checkout TV1_TranGiaHuy
cp docker/docker-compose.pinned.yml docker-compose.yml
cp docker/docker-compose.env.example docker-compose.env
cp docker/.env.example .env
# Sinh SECRET thật, thay dòng PAPERLESS_SECRET_KEY=change-me trong docker-compose.env:
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Kiểm tra dòng image trong `docker-compose.yml` phải là:

```yaml
image: ghcr.io/paperless-ngx/paperless-ngx:3.1.3
```

## 4. Biến môi trường quan trọng (giải thích ngắn)

| Biến (trong `docker-compose.env`) | Ý nghĩa | Giá trị nhóm dùng |
|---|---|---|
| `PAPERLESS_SECRET_KEY` | Khóa ký session/token, **bắt buộc đổi**, không commit lên Git | chuỗi ngẫu nhiên 64 ký tự |
| `PAPERLESS_ADMIN_PASSWORD` | Mật khẩu admin tạo tự động ở lần chạy đầu — **không để `admin`/`change-me` khi chạy thật** | mật khẩu mạnh của bạn |
| `PAPERLESS_URL` | URL công khai (để nguyên comment khi chạy local) | không đặt |
| `PAPERLESS_TIME_ZONE` | Múi giờ hiển thị | `Asia/Ho_Chi_Minh` |
| `PAPERLESS_OCR_LANGUAGE` | Ngôn ngữ OCR chính | `eng` (bộ seed là tiếng Anh; nếu thêm tài liệu tiếng Việt thì đặt `vie` + thêm `PAPERLESS_OCR_LANGUAGES=vie`) |
| `PAPERLESS_REDIS` / `PAPERLESS_DBHOST` / `PAPERLESS_DBENGINE` | Trỏ sang container broker/db (đã khai trong compose) | giữ nguyên |

`COMPOSE_PROJECT_NAME=paperless` (trong `.env`) để tên container/volume thống nhất cả nhóm.

## 5. Khởi động + tạo admin

```bash
docker compose pull            # kéo đúng image đã pin
docker compose up -d           # chạy nền 3 container: webserver, db, broker
docker compose ps              # cả 3 phải ở trạng thái running/healthy
docker compose run --rm webserver createsuperuser   # đặt username/password admin của BẠN
```

Nếu `.env` đã có `PAPERLESS_ADMIN_USER` / `PAPERLESS_ADMIN_PASSWORD` thì tài khoản admin
được tạo tự động ở lần khởi động đầu, không cần `createsuperuser`. Đổi mật khẩu về sau:

```bash
docker compose exec webserver python3 manage.py changepassword admin
```

## 6. Lấy token API (đúng cách duy nhất)

Paperless-ngx **không có** lệnh `manage.py create_api_token` và cũng **không có** `manage.py set_password`.
Lấy token qua endpoint (thay `ADMIN`/`MK` bằng của bạn, chạy trong WSL/Git Bash):

```bash
curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ADMIN","password":"MK"}'
```

Trả về `{"token":"abc..."}`. Dùng cho mọi lệnh sau qua header
`Authorization: Token <token>`. **Không dán token vào chat, file md hay commit.**

## 7. Kiểm tra sống (ai cũng phải chụp màn hình)

1. Mở http://localhost:8000 → trang login hiện ra.
2. Đăng nhập bằng admin vừa tạo.
3. Upload 1 file trong `scripts/sample_docs/` (kéo-thả vào Dashboard) → đợi 30–90 s → tài liệu xuất hiện, mở ra thấy **nội dung text OCR** được.
4. Mở http://localhost:8000/api/schema/view/ (Swagger UI mở được) và
   http://localhost:8000/api/schema/ (file schema thô tải được).
5. Chụp ảnh: login thành công, tài liệu sau OCR, Swagger UI, search/lọc → lưu vào `docs/evidence/` rồi nộp kèm báo cáo.

## 8. Nạp bộ seed chung (để 5 máy có dữ liệu giống nhau)

```bash
# Cách 1 (khuyên dùng): upload tay 6 file PDF mẫu qua giao diện web
# Cách 2: copy vào thư mục consume để hệ thống tự nuốt:
cp scripts/sample_docs/TV1_Sample_*.pdf consume/ && sleep 60 && docker compose logs --tail=20 webserver
# Tạo tag / correspondent / document_type mẫu giống nhau:
pip install requests
python3 scripts/seed_and_verify_flows_TV1.py --base-url http://localhost:8000 --username <ADMIN> --password <MK>
```

Chi tiết bộ seed: xem `docs/SEED_DATA_TV1.md`.
Bộ seed/script riêng của TV2 nằm ở `scripts/seed_data.py`, `scripts/reset_data.py`, `scripts/sample_docs/TV2_*`.

## 9. Reset về trạng thái ban đầu (trước mỗi vòng test Vòng 2, Vòng 3)

```bash
docker compose down -v        # XÓA SẠCH volume/db — cẩn thận, chỉ chạy khi được yêu cầu
docker compose up -d
docker compose run --rm webserver createsuperuser   # tạo lại admin
# upload lại scripts/sample_docs/TV1_Sample_*.pdf + chạy lại seed_and_verify_flows_TV1.py
```

Script dùng chung của nhóm: `scripts/reset_system.ps1` (script duy nhất được phép `down -v`),
`scripts/reset_data.py` (reset API nhẹ: xóa documents/tags/correspondents/document_types, giữ user).

## 10. Cài Schemathesis (bản nhóm dùng chung)

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows (WSL): vẫn lệnh này; PowerShell: .venv\Scripts\activate
pip install "schemathesis==4.30.1"
schemathesis --version         # phải ra 4.30.1 trên cả 5 máy
schemathesis run --help | head -50   # đọc kỹ: tên option khác nhau giữa bản 3 và 4 (TV3 chốt lệnh chuẩn)
```

## 11. Lệnh hay dùng

| Việc | Lệnh |
|---|---|
| Xem container | `docker compose ps` |
| Xem log | `docker compose logs -f webserver` |
| Tắt (giữ dữ liệu) | `docker compose down` |
| Xóa sạch làm lại | `docker compose down -v` |
| Lấy token API | `curl -s -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"ADMIN","password":"MK"}'` |
| Backup DB nhanh | `docker compose exec db pg_dump -U paperless paperless > backup_$(date +%F).sql` |

## 12. Xử lý sự cố (ghi lại để khỏi hỏi lại)

| Triệu chứng | Nguyên nhân hay gặp | Cách gỡ |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop chưa bật | Mở Docker Desktop, chờ trạng thái running |
| `port 8000 already in use` | Cổng bị app khác chiếm | Đổi `ports: "8001:8000"` trong compose, test ở `localhost:8001` và **ghi lại** vào file kết quả |
| Upload xong mãi không OCR | Consumer chưa chạy / thiếu RAM | `docker compose logs webserver \| grep -i consume`; cấp thêm RAM cho Docker Desktop (≥ 4 GB) |
| `/api/schema/` trắng / 404 | Webserver chưa healthy | `docker compose ps`, đợi 1–2 phút rồi F5 |
| `latest` bị kéo nhầm | Quên pin tag | Sửa image thành `:3.1.3`, chạy `docker compose pull && docker compose up -d` |
| Token 400/403, 401 khi gọi API | Sai username/password, thiếu header | Lấy lại token (mục 6), header đúng dạng `Authorization: Token <token>` |
| `webserver` restart liên tục | `.env` sai hoặc DB chưa sẵn sàng | `docker compose logs webserver`, chờ thêm 2 phút |
| Lệnh `set_password` / `create_api_token` báo `Unknown command` | Hai lệnh này không tồn tại trong Paperless-ngx | Dùng mục 5–6 ở trên |
| WSL hết dung lượng | Image + volume phình | `docker system prune -a --volumes` (xóa hết rồi làm lại từ bước 5) |

## 13. Checklist TV1

- [x] Chốt tag `v3.1.3` + SHA `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` (`docs/PINNED_VERSION_TV1.md`)
- [x] Viết tài liệu này (cài từ máy sạch, port, biến môi trường, token, reset, sự cố)
- [x] `docker/docker-compose.pinned.yml` + file env mẫu (không chứa secret thật)
- [x] Bộ seed `scripts/sample_docs/TV1_Sample_*.pdf` + `scripts/seed_and_verify_flows_TV1.py`
- [x] Hướng dẫn 3 luồng nghiệp vụ (`docs/BUSINESS_FLOWS_TV1.md`)
- [x] Dựng thành công trên máy TV1 (13/10/2026) + biên bản `results/TV1_deploy_13-10.md`
- [ ] Chụp ảnh bằng chứng và lưu vào `docs/evidence/`
- [ ] Chạy Vòng 1–3 với seed 101, điền `results/TV1_seed101_mau.md`
