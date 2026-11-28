# KTPM — Nhánh TV1 (Trần Gia Huy): môi trường & tài liệu cài đặt

Đề tài: Kiểm thử phần mềm — Paperless-ngx (R08) + K05 Schemathesis (schema-based API testing).
Nhóm: 5 người, môn Kiểm thử phần mềm, Trường Đại học Đà Lạt. Mốc giữa kỳ: 20/10/2026.

> **README chuẩn ở gốc repo: [`README.md`](README.md).**
> File này giữ phần mô tả vai trò/cấu trúc cũ; nếu có khác biệt, làm theo `README.md`.
> Xác minh môi trường sạch 26/11/2026: [`results/TV1_cleanenv_verify.md`](results/TV1_cleanenv_verify.md).

## Vai trò TV1 — Phần C, H (môi trường & tài liệu cài đặt)

| Việc | Nằm ở đâu |
|---|---|
| Hướng dẫn cài Paperless-ngx từ máy sạch | `docs/ONBOARDING_TV1.md` |
| 3 luồng nghiệp vụ chạy được (kèm lệnh API) | `docs/BUSINESS_FLOWS_TV1.md` |
| Bộ seed chung 6 PDF + script tạo metadata | `docs/SEED_DATA_TV1.md`, `scripts/sample_docs/TV1_Sample_*.pdf` |
| Pin tag / commit SHA / phiên bản công cụ | `docs/PINNED_VERSION_TV1.md`, `docker/docker-compose.pinned.yml` |
| Kết quả chạy thật (3 vòng seed 101) + báo cáo lỗi | `results/TV1_ketqua_seed101.md`, `docs/bugs/BUG-04.md` → `BUG-06.md` |
| Biên bản dựng hệ thống | `results/TV1_deploy_13-10.md` |
| Kiểm tra môi trường trước khi cài | `scripts/check_env_TV1.ps1`, `scripts/check_env_TV1.sh` |
| Ảnh bằng chứng (tự chụp) | `docs/evidence/` |

## Phiên bản ghim (bắt buộc cả nhóm)

| Mục | Giá trị |
|---|---|
| Repo hệ thống | https://github.com/paperless-ngx/paperless-ngx |
| Tag đã chốt | `v3.1.3` |
| Annotated tag object | `cbd6b56c9f0eb7261c903cf5ccdbe124d433e995` |
| Commit SHA (tag trỏ tới) | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` |
| Image Docker | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (digest `sha256:aa810a36...`) |
| Schemathesis | `4.30.1` (PyPI) |
| Port | `8000` (http://localhost:8000) |

Xem chi tiết: `docs/PINNED_VERSION_TV1.md`.

## Cấu trúc thư mục

```
D:\KTPM/
├── README.md                      (TV1: README chuẩn ở gốc — cài/chạy/kiểm tra/reset)
├── README_TV1.md                  (file này — mô tả vai trò/cấu trúc cũ)
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
│   │   DEFENSE_CHEAT_SHEET.md, TODO_TV2.md                        (TV2)
│   ├── bugs/BUG-0{1,2,3}.md      (TV2: lỗi của nhóm, TV1 không sửa)
│   ├── bugs/BUG-0{4,5,6}.md      (TV1: lỗi do TV1 phát hiện, seed 101)
│   └── evidence/                  (TV1: ảnh bằng chứng TV1_*.png)
├── results/
│   ├── TV1_deploy_13-10.md        (TV1: biên bản dựng hệ thống 13/10)
│   ├── TV1_ketqua_seed101.md      (TV1: bảng kết quả thật 3 vòng + phân loại lỗi)
│   ├── TV1_round{1,2,3}_seed101.{log,xml,ndjson}  (TV1: log, JUnit, NDJSON thô)
│   ├── TV1_round{1,2,3}_seed101_summary.md        (TV1: tóm tắt tự động mỗi vòng)
│   ├── TV1_cleanenv_verify.md/.log                (TV1: xác minh môi trường sạch 26/11/2026)
│   ├── TV1_cleanenv_round{1,2,3}_seed101_summary.md
│   └── TV2_round{1,2,3}_seed202*  (TV2: log 3 vòng Schemathesis)
└── scripts/
    ├── check_env_TV1.ps1, check_env_TV1.sh          (TV1)
    ├── generate_sample_pdfs_TV1.py/.ps1             (TV1: sinh lại 6 PDF)
    ├── seed_and_verify_flows_TV1.py                 (TV1: tạo tag/corr/doctype)
    ├── prepare_baseline_TV1.py                      (TV1: reset + seed + xác nhận baseline)
    ├── run_round_TV1.py, run_round_TV1.ps1          (TV1: chạy từng vòng Schemathesis, seed 101)
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

> Hướng dẫn đầy đủ, có cảnh báo xóa dữ liệu: [`README.md`](README.md).

1. Cài Docker Desktop (≥ 4.30), bật WSL2 trên Windows.
2. `Copy-Item .env.example .env` → sửa `PAPERLESS_SECRET_KEY`, `PAPERLESS_ADMIN_PASSWORD`,
   `PAPERLESS_URL` (không commit `.env`).
3. `docker compose pull && docker compose up -d` → chờ 3 container `webserver/db/broker` Up,
   `webserver` healthy.
4. Tạo admin: để hệ thống tự tạo từ `.env`, hoặc
   `docker compose run --rm webserver createsuperuser`.
5. Kiểm tra http://localhost:8000 + Swagger http://localhost:8000/api/schema/view/;
   `GET /api/schema/` phải `200`, OpenAPI 3.0.3.
6. Cài Schemathesis: cần **Python 3.11–3.13** (Python 3.15 lỗi build `pyyaml`) →
   `py -3.13 -m venv .venv` rồi `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
7. Dựng dữ liệu seed (quy trình nhóm: reset → seed → xác nhận baseline):
   `.\.venv\Scripts\python.exe scripts\prepare_baseline_TV1.py`
   ⚠️ Bước này **xóa dữ liệu** documents/tags/correspondents/document_types — chỉ chạy trên máy test.
8. Chạy 3 vòng seed 101: `.\.venv\Scripts\python.exe scripts\run_round_TV1.py --round 1|2|3`
   (chạy lại bước 7 trước vòng 2 và vòng 3 vì fuzzing có tạo/xoá dữ liệu).
9. Kết quả: `results/TV1_round<N>_seed101.{xml,ndjson,log}` + `_summary.md`.

Chi tiết từng bước (kèm xử lý sự cố): `docs/ONBOARDING_TV1.md`.
Xác minh môi trường sạch: `results/TV1_cleanenv_verify.md`.