# ONBOARDING — Cài và chạy Paperless-ngx từ máy sạch (TV1 chủ trì, TV2 hiệu đính 12/10)

> Tài liệu chính xác duy nhất để dựng hệ thống. Phiên bản ghim: xem `docs/PINNED_VERSION.md`
> (Paperless-ngx `v3.1.3`, Schemathesis `4.30.1`). Chỉ test trên `http://localhost:8000`.

## 1. Yêu cầu máy

RAM ≥ 8 GB, đĩa trống ≥ 10 GB, Docker Desktop (Windows bật WSL2), Python 3.11–3.13.

```bash
git --version
docker --version
docker compose version
python3 --version
```

## 2. Kéo repo và tạo `.env` (không commit file này)

```bash
git pull origin master
cp .env.example .env
```

Mở `.env` và đặt lại 2 giá trị (không để `admin`/`change-me` khi chạy thật):

```
PAPERLESS_SECRET_KEY=<chuỗi ngẫu nhiên 50+ ký tự>
PAPERLESS_ADMIN_PASSWORD=<mật khẩu mạnh của BẠN>
```

## 3. Bật hệ thống

```bash
docker compose up -d
docker compose ps          # webserver, db, broker đều Up
docker compose logs -f webserver   # chờ xong migration, 1–3 phút
curl -s -o NUL -w "%{http_code}" http://localhost:8000   # 200 hoặc 302 là sống
```

Tài khoản admin được tự tạo từ `PAPERLESS_ADMIN_USER` / `PAPERLESS_ADMIN_PASSWORD`
trong `.env` ở lần khởi động đầu. Đổi mật khẩu sau này:

```bash
docker compose exec webserver python3 manage.py changepassword admin
```

## 4. Lấy token API (đúng cách duy nhất)

Paperless-ngx **không có** lệnh `manage.py create_api_token` / `set_password`.
Lấy token qua endpoint (thay `ADMIN`/`MK` bằng của bạn, chạy trong WSL/Git Bash):

```bash
curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ADMIN","password":"MK"}'
```

Trả về `{"token":"abc..."}`. Dùng cho mọi lệnh sau qua header
`Authorization: Token <token>`. **Không dán token vào chat, file md hay commit.**

## 5. Seed dữ liệu mẫu

```bash
pip install requests
set PAPERLESS_ADMIN_USER=admin & set PAPERLESS_ADMIN_PASSWORD=<MK>   # CMD Windows
python scripts/seed_data.py
```

Kiểm tra: http://localhost:8000 hiện 2 tài liệu mẫu; 4 tag, 3 correspondent, 3 doctype.

## 6. Cài Schemathesis đúng bản nhóm

```bash
python -m venv .venv
.venv\Scripts\activate
pip install "schemathesis==4.30.1"
schemathesis --version
schemathesis run --help   # đọc kỹ: tên option khác nhau giữa bản 3 và 4, không đoán
```

## 7. Reset về trạng thái ban đầu (trước vòng 2, vòng 3)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/reset_system.ps1
python scripts/seed_data.py
```

`reset_system.ps1` là script duy nhất được phép `down -v`. Reset API nhẹ
(`scripts/reset_data.py`) chỉ xóa documents/tags/correspondents/document_types, giữ user.

## 8. Sự cố đã gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `Cannot connect to the Docker daemon` | Mở Docker Desktop, chờ running |
| Port 8000 bị chiếm | Đổi `ports` trong compose, thống nhất cả nhóm |
| `webserver` restart liên tục | `docker compose logs webserver`, thường do `.env` sai hoặc DB chưa sẵn sàng — chờ thêm 2 phút |
| 401 khi gọi API | Lấy lại token (mục 4) |
| Lệnh `set_password` / `create_api_token` báo `Unknown command` | Đúng — 2 lệnh này không tồn tại, dùng mục 3–4 ở trên |
