# TV1 — Biên bản dựng hệ thống + 3 luồng nghiệp vụ (ngày 13/10/2026)

| Mục | Giá trị |
|---|---|
| Người chạy | TV1 (agent hỗ trợ, user chụp ảnh bổ sung) |
| OS / RAM | Windows 11, RAM 15.7 GB |
| Docker / Compose | 29.8.0 / v5.5.1, daemon running, RAM Docker 8 GB |
| Image | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (đúng pin nhóm) |
| Container | paperless-webserver (healthy), paperless-db, paperless-broker — 3/3 Up |
| Port | 8000, trống trước khi chạy |
| Admin | `admin` / `admin` (thống nhất nhóm theo hướng dẫn TV2) |
| Seed nạp | 3 tag (`hoa-don`, `can-xu-ly`, `luu-tru-lau-dai`), 2 correspondent, 2 document type, 2 PDF (`seed_01`, `seed_03`) |

## Kết quả 3 luồng (HTTP thật, đã chạy)

1. **Upload → OCR**: `POST /api/documents/post_document/` → 2 task UUID; sau ~75 s
   `GET /api/documents/` → `count=2`, `content` có chữ đúng nội dung file gốc. ĐẠT.
2. **Gắn tag/correspondent**: `PATCH /api/documents/1/` `{"tags":[1],"correspondent":1,"document_type":1}`
   → 200, `tags=1 corr=1 dtype=1`. ĐẠT.
3. **Search/lọc**: `GET /api/documents/?query=dien` → `count=1 ids=1`;
   `?tags__id__in=1` → `count=1 ids=1`. ĐẠT.
4. **Schema**: `GET /api/schema/` → 200, 340696 bytes. Swagger: `/api/schema/view/`.

## Ảnh user tự chụp (checklist)

- [ ] `docker compose ps` (3 Up, webserver healthy)
- [ ] Đăng nhập `http://localhost:8000` thành công
- [ ] Tài liệu + tab Content có chữ OCR
- [ ] Swagger UI `/api/schema/view/`
- [ ] Kết quả search `dien` + lọc tag `hoa-don`
