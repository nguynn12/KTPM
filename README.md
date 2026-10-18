# KTPM — Phân công TV1 (Trần Gia Huy)

Đề tài: Kiểm thử phần mềm — Paperless-ngx (R08) + K05 Schemathesis (schema-based API testing).
Nhóm: 5 người, môn Kiểm thử phần mềm, Trường Đại học Đà Lạt. Mốc giữa kỳ: 20/10/2026.

## Vai trò TV1
Môi trường & tài liệu cài đặt (Phần C, H):
- Hướng dẫn cài Paperless-ngx từ máy sạch (`docs/TV1_Onboarding.md`).
- 3 luồng nghiệp vụ chạy được + bằng chứng (`docs/TV1_3_Luong_Nghiep_Vu.md`, `docs/img/`).
- Bộ seed chung 6 PDF mẫu + script tạo tag/correspondent/document_type giống nhau trên 5 máy (`seed/`).
- Pin tag/commit SHA + cách chạy lại (`PINNED-VERSIONS.md`, `docker/docker-compose.pinned.yml`).
- Kết quả chạy thật vòng 1–3, seed 101 (`results/TV1_101_*.md`, `results/TV1_deploy_13-10.md`).

## Phiên bản ghim (bắt buộc cả nhóm)
| Mục | Giá trị |
|---|---|
| Repo hệ thống | https://github.com/paperless-ngx/paperless-ngx |
| Tag đã chốt | `v3.1.3` |
| Commit SHA | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` |
| Image Docker | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` |
| Schemathesis | `4.30.1` |
| Port | `8000` (http://localhost:8000) |

Xem chi tiết: `PINNED-VERSIONS.md`.

## Cấu trúc thư mục
```
D:\KTPM/
├── README.md                 (file này)
├── PINNED-VERSIONS.md        (tag, commit SHA, phiên bản công cụ)
├── .gitignore
├── requirements.txt
├── docker/                   (compose pin 3.1.3 + file env mẫu)
│   ├── docker-compose.pinned.yml
│   ├── docker-compose.env.example
│   └── .env.example
├── seed/                     (6 PDF mẫu + seed_api.py + generator + README)
├── scripts/                  (check_env.ps1, check_env.sh)
├── docs/
│   ├── TV1_Onboarding.md     (hướng dẫn cài từ máy sạch — Phần C)
│   ├── TV1_3_Luong_Nghiep_Vu.md (3 luồng nghiệp vụ — Phần C)
│   ├── ONBOARDING.md         (biên bản dựng thật 13/10)
│   └── img/                  (ảnh minh chứng)
├── results/
│   ├── TV1_deploy_13-10.md   (biên bản chạy thật 13/10)
│   └── TV1_101_mau.md        (mẫu kết quả seed 101)
└── .github/ (nếu có)
```

## Cách chạy lại toàn bộ
1. Cài Docker Desktop (≥ 4.30), bật WSL2 trên Windows.
2. `cp docker/docker-compose.pinned.yml docker-compose.yml`
3. `cp docker/docker-compose.env.example docker-compose.env` → sửa `PAPERLESS_SECRET_KEY` (không commit).
4. `docker compose up -d` → chờ 3 container `webserver/db/broker` Up.
5. Tạo admin: `docker compose run --rm webserver createsuperuser`.
6. Kiểm tra http://localhost:8000 + Swagger http://localhost:8000/api/schema/view/.
7. Seed: `cp seed/*.pdf consume/` rồi `python seed/seed_api.py`.
8. Cài Schemathesis: `pip install "schemathesis==4.30.1"`.

## Quy tắc Git
- Mỗi thành viên commit trên tài khoản của mình (để peer-review cuối kỳ).
- Không commit `.env` thật, token, mật khẩu, `paperless-ngx/`, `.venv/`.
- Nhánh TV1 trên repo nhóm: `TV1_TranGiaHuy` (`https://github.com/nguynn12/KTPM.git`).
