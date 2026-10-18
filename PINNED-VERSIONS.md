# PINNED VERSIONS — Mục 2 (TV1 chốt, cả nhóm dùng chung)

> Quy tắc: KHÔNG dùng `latest`. Mọi người pin đúng tag + commit SHA dưới đây.
> Ngày chốt: 11/10/2026 (TV1). Cập nhật bảng này nếu cả nhóm thống nhất đổi bản.

| Mục | Giá trị |
|---|---|
| Repo | https://github.com/paperless-ngx/paperless-ngx |
| Tag/release đã chốt | **v3.1.3** (release ổn định 04/09/2026; đã chạy xong vòng 1–3 và dựng thật TV1 ngày 13/10) |
| Commit SHA (đầy đủ) | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` |
| Image Docker pin | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` |
| Phiên bản Schemathesis (cả nhóm đồng nhất) | `4.30.1` — cài bằng `pip install "schemathesis==4.30.1"`, kiểm tra bằng `schemathesis --version` |
| Python yêu cầu (cho Schemathesis) | 3.11 – 3.13 (theo docs Schemathesis; Paperless container tự mang Python riêng) |
| Phạm vi test | `/api/tags/`, `/api/correspondents/`, `/api/document_types/`, `/api/documents/` |
| Port mặc định | `8000` → mở http://localhost:8000 |
| DB / service kèm theo | PostgreSQL `docker.io/library/postgres:16-alpine`, Redis `docker.io/library/redis:7-alpine` (theo `docker-compose.yml` của nhóm) |
| Repo Git của nhóm | https://github.com/nguynn12/KTPM.git |
| Nhánh TV1 | `TV1_TranGiaHuy` |
| Công cụ quản lý | Trello / GitHub Projects (TV5 điền) |

## Vì sao chọn v3.1.3 mà không phải v3.2.1 / v3.3.0 hay main?

- `main` trôi liên tục → 5 máy sẽ chạy 5 bản khác nhau, số liệu không so sánh được.
- `v3.2.1` là đề xuất ban đầu của TV1, nhưng TV2 đã chạy xong vòng 1–3 và viết 3 bug report trên `v3.1.3`; đổi tag lúc này đồng nghĩa chạy lại toàn bộ. Nhóm thống nhất giữ `v3.1.3` cho mốc giữa kỳ 20/10.
- `v3.3.0` ra mới (06/10/2026) chưa đủ thời gian kiểm chứng, rủi ro lỗi hồi quy.
- `v3.1.3` đã tồn tại, ổn định để test giữa kỳ.

## Cách kiểm chứng pin (ai cũng chạy được)

```bash
docker images | grep paperless-ngx        # phải thấy :3.1.3, KHÔNG thấy :latest
docker compose exec webserver python -c "import paperless; print(paperless.__version__)" 2>/dev/null || \
docker compose exec webserver cat /usr/src/paperless/src/paperless/version.py
git -C paperless-ngx-src log --oneline -1  # nếu có clone repo để đọc code: phải ra d48663e
schemathesis --version                    # phải ra 4.30.1 trên cả 5 máy
```
