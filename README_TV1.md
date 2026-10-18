# KTPM — Nhánh TV1 (Trần Gia Huy): môi trường & tài liệu cài đặt

Đề tài: Kiểm thử phần mềm — Paperless-ngx (R08) + K05 Schemathesis (schema-based API testing).
Nhóm: 5 người, môn Kiểm thử phần mềm, Trường Đại học Đà Lạt. Mốc giữa kỳ: 20/10/2026.

## Vai trò TV1 — Phần C, H (môi trường & tài liệu cài đặt)

| Việc | Nằm ở đâu |
|---|---|
| Hướng dẫn cài Paperless-ngx từ máy sạch | `docs/ONBOARDING_TV1.md` |
| 3 luồng nghiệp vụ chạy được (kèm lệnh API) | `docs/BUSINESS_FLOWS_TV1.md` |
| Bộ seed chung 6 PDF + script tạo metadata | `docs/SEED_DATA_TV1.md`, `scripts/sample_docs/TV1_Sample_*.pdf` |
| Pin tag / commit SHA / phiên bản công cụ | `docs/PINNED_VERSION_TV1.md`, `docker/docker-compose.pinned.yml` |
| Kết quả chạy thật + biên bản dựng hệ thống | `results/TV1_deploy_13-10.md`, `results/TV1_seed101_mau.md` |
| Kiểm tra môi trường trước khi cài | `scripts/check_env_TV1.ps1`, `scripts/check_env_TV1.sh` |
| Ảnh bằng chứng (tự chụp) | `docs/evidence/` |

## Phiên bản ghim (bắt buộc cả nhóm)

| Mục | Giá trị |
|---|---|
| Repo hệ thống | https://github.com/paperless-ngx/paperless-ngx |
| Tag đã chốt | `v3.1.3` |
| Commit SHA | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` |
| Image Docker | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` |
| Schemathesis | `4.30.1` |
| Port | `8000` (http://localhost:8000) |

Xem chi tiết: `docs/PINNED_VERSION_TV1.md`.

## Cấu trúc thư mục

```
D:\KTPM/
├── README_TV1.md                  (file này — TV1)
├── .gitignore, .env.example, docker-compose.yml, requirements.txt   (dùng chung cả nhóm)
├── docker/                        (TV1: compose pin 3.1.3 + env mẫu)
│   ├── docker-compose.pinned.yml
│   ├── docker-compose.env.example
│   └── .env.example
├── docs/
│   ├── ONBOARDING_TV1.md          (TV1: hướng dẫn cài từ máy sạch — Phần C)
│   ├── BUSINESS_FLOWS_TV1.md      (TV1: 3 luồng nghiệp vụ — Phần C)
│   ├── PINNED_VERSION_TV1.md      (TV1: tag, SHA, phiên bản công cụ)
│   ├── SEED_DATA_TV1.md           (TV1: mô tả bộ seed chung)
│   ├── FILL_IN.md                 (TV2: file tổng hợp số liệu thực tế)
│   ├── ARCHITECTURE_NOTES.md, TEST_CASES.md, PRESENTATION_NOTES.md,
│   │   DEFENSE_CHEAT_SHEET.md, TODO_TV2.md, bugs/BUG-0{1,2,3}.md   (TV2)
│   └── evidence/                  (TV1: ảnh bằng chứng TV1_*.png)
├── results/
│   ├── TV1_deploy_13-10.md        (TV1: biên bản dựng hệ thống 13/10)
│   ├── TV1_seed101_mau.md         (TV1: mẫu bảng kết quả seed 101)
│   └── TV2_round{1,2,3}_seed202*  (TV2: log 3 vòng Schemathesis)
└── scripts/
    ├── check_env_TV1.ps1, check_env_TV1.sh          (TV1)
    ├── generate_sample_pdfs_TV1.py/.ps1             (TV1: sinh lại 6 PDF)
    ├── seed_and_verify_flows_TV1.py                 (TV1: tạo tag/corr/doctype)
    ├── sample_docs/TV1_Sample_0*.pdf                (TV1: 6 PDF mẫu, seed 101)
    ├── sample_docs/TV2_Sample_*.txt                 (TV2)
    └── seed_data.py, reset_data.py, reset_system.ps1, run_manual_tests.py   (TV2)
```

## Quy ước đặt tên (thống nhất với nhánh TV2, TV3)

- Tài liệu của ai thì mang mã người đó: `*_TV1.md` (TV3 dùng `*_TV3.md`, TV2 dùng `TODO_TV2.md`).
- Kết quả test: `results/<MÃ>_seed<Số>_<mô tả>.<ext>` — TV1 dùng seed **101**, TV2 seed **202**, TV3 seed **303**.
- PDF/tài liệu mẫu để trong `scripts/sample_docs/` và có tiền tố mã người + số seed: `TV1_Sample_01_HoaDon_101.pdf`.
- Ảnh bằng chứng để trong `docs/evidence/`, tên bắt đầu bằng mã người: `TV1_*.png`.
- Script riêng của ai thì có hậu tố mã người: `check_env_TV1.ps1`.
- Không ghi đè file của thành viên khác; file kết quả đặt tên theo tên mình.

## Cách chạy lại toàn bộ

1. Cài Docker Desktop (≥ 4.30), bật WSL2 trên Windows.
2. `cp docker/docker-compose.pinned.yml docker-compose.yml`
3. `cp docker/docker-compose.env.example docker-compose.env` → sửa `PAPERLESS_SECRET_KEY` (không commit).
4. `docker compose up -d` → chờ 3 container `webserver/db/broker` Up.
5. Tạo admin: `docker compose run --rm webserver createsuperuser` (hoặc để hệ thống tự tạo từ `.env`).
6. Kiểm tra http://localhost:8000 + Swagger http://localhost:8000/api/schema/view/.
7. Seed: `cp scripts/sample_docs/TV1_Sample_*.pdf consume/` rồi `python3 scripts/seed_and_verify_flows_TV1.py`.
8. Cài Schemathesis: `pip install "schemathesis==4.30.1"`.

Chi tiết từng bước (kèm xử lý sự cố): `docs/ONBOARDING_TV1.md`.

## Quy tắc Git

- Mỗi thành viên commit trên tài khoản của mình (để peer-review cuối kỳ).
- Không commit `.env` thật, token, mật khẩu, `paperless-ngx/`, `.venv/`.
- Nhánh TV1 trên repo nhóm: `TV1_TranGiaHuy` (`https://github.com/nguynn12/KTPM.git`).
