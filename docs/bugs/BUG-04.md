# LỖI BUG-04: HTTP 500 (ValueError) khi `{id}` của tài liệu không phải là số

- **Mã lỗi:** BUG-04 (TV1) — nhóm đã có BUG-01 → BUG-03 của TV2, TV1 đánh số tiếp
- **Người phát hiện:** Trần Gia Huy (TV1)
- **Công cụ phát hiện:** Schemathesis 4.30.1 (seed 101). Vòng 1 — Test Case ID `lvjTJ0`; Vòng 3 — Test Case ID `qg4aZX`, `83XLMq`, `XW6OmH`, `Whb1ZK`, `tc6cCS`
- **Mức độ:** High (Internal Server Error, không kiểm soát được đầu vào)
- **Phương thức & endpoint:** `GET|DELETE|POST /api/documents/{id}/<tài nguyên con>/`

## 1. Mô tả lỗi

Các view con của tài liệu (`ai_suggestions`, `metadata`, `share_links`, `suggestions`, `thumb`, `history`,
`root`, `notes`, `preview`) nhận tham số đường dẫn `{id}` và đưa thẳng vào truy vấn cơ sở dữ liệu
mà **không kiểm tra** giá trị này có phải số. Khi `{id}` là chuỗi không phải số, Django ném
`ValueError: Field 'id' expected a number but got '…'` và Paperless-ngx trả về **HTTP 500**
(trang HTML `Server Error (500)`) thay vì `400 Bad Request` / `404 Not Found` như tài liệu OpenAPI ghi.

## 2. Các bước tái hiện

```bash
# Thay <TOKEN> bằng token lấy từ POST /api/token/ với admin/admin
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/true/metadata/
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/true/ai_suggestions/
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/true/history/
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/true/root/
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/abc/suggestions/
curl -i -H "Authorization: Token <TOKEN>" "http://localhost:8000/api/documents/null,null/ai_suggestions/"
```

## 3. Kết quả thực tế (đo ngày 18/10/2026 trên máy TV1)

| Request | Kết quả thật |
|---|---|
| `GET /api/documents/true/metadata/` | **HTTP 500** |
| `GET /api/documents/true/ai_suggestions/` | **HTTP 500** |
| `GET /api/documents/true/share_links/` | **HTTP 500** |
| `GET /api/documents/true/history/` | **HTTP 500** |
| `GET /api/documents/true/root/` | **HTTP 500** |
| `GET /api/documents/abc/suggestions/` | **HTTP 500** |
| `GET /api/documents/null,null/ai_suggestions/` | **HTTP 500** |
| `GET /api/documents/{id}/thumb/` với `{id}` không phải số | **HTTP 500** |
| `DELETE /api/documents/{id}/notes/` với `{id}` không phải số | **HTTP 500** |
| `TRACE /api/documents/{id}/notes/` | **HTTP 500** (đáng lẽ 405 Method Not Allowed) |
| `GET /api/documents/true/` (endpoint gốc) | 404 — **đúng**, cho thấy lỗi chỉ ở các view con |
| `GET /api/documents/999999/metadata/` (id số, không tồn tại) | 404 — **đúng** |

Thân phản hồi là trang HTML của Django:

```html
<!doctype html><html lang="en"><head><title>Server Error (500)</title></head>
<body><h1>Server Error (500)</h1><p></p></body></html>
```

## 4. Bằng chứng ở log máy chủ

```
paperless-webserver | [2026-10-18 16:28:54,479] [ERROR] [django.request] Internal Server Error: /api/documents/true/history/
paperless-webserver | Traceback (most recent call last):
paperless-webserver | ValueError: invalid literal for int() with base 10: 'true'
paperless-webserver | ValueError: Field 'id' expected a number but got 'true'.

paperless-webserver | [2026-10-18 16:26:52,779] [ERROR] [django.request] Internal Server Error: /api/documents/null,null/ai_suggestions/
paperless-webserver | ValueError: invalid literal for int() with base 10: 'null,null'
paperless-webserver | ValueError: Field 'id' expected a number but got 'null,null'.

paperless-webserver | [2026-10-18 16:28:54,580] [ERROR] [django.request] Internal Server Error: /api/documents/abc/suggestions/
paperless-webserver | ValueError: invalid literal for int() with base 10: 'abc'
```

Xem thêm trong file kết quả: `results/TV1_round1_seed101.xml` (Test Case ID `lvjTJ0`, `g910DV`, `ZKaq22`),
`results/TV1_round3_seed101.xml` (`qg4aZX`, `83XLMq`, `XW6OmH`, `Whb1ZK`, `tc6cCS`).

## 5. Kết quả mong đợi

- Với `{id}` không phải số: `400 Bad Request` (hoặc `404`), **không** được là `500`.
- Tài liệu OpenAPI của chính endpoint đó ghi các mã: `200, 400, 403, 404` — tức là `500` không có trong tài liệu.

## 6. Phân loại

| Trường | Nội dung |
|---|---|
| Loại lỗi | Lỗi chức năng thật (kiểm tra dữ liệu đầu vào) — không phải lỗi tài liệu |
| Tái hiện | Ổn định trên máy TV1, tái hiện 100% bằng `curl` |
| Tái hiện trên máy khác? | Chưa thử — nhờ TV2/TV3 xác nhận lại (rất dễ: 1 lệnh `curl`) |
| Phân loại | **đã xác nhận** trên máy TV1 (có traceback máy chủ), chờ xác nhận chéo ≥2 người |
| Gợi ý hướng sửa | Ép kiểu/validate `{id}` (dùng `get_object_or_404` với `pk` số) ở các view con trước khi truy vấn |
