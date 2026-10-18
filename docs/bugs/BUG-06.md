# LỖI BUG-06: Response thiếu trường bắt buộc `permissions` (và `last_correspondence`) so với schema

- **Mã lỗi:** BUG-06 (TV1) — cùng họ với BUG-03 của TV2 (thiếu trường `document_count`), nhưng khác trường và khác phương thức
- **Người phát hiện:** Trần Gia Huy (TV1)
- **Công cụ phát hiện:** Schemathesis 4.30.1, seed 101 — check `response_schema_conformance`, Vòng 1
- **Mức độ:** Medium (response không khớp đặc tả; client tin vào schema sẽ lỗi khi đọc dữ liệu)
- **Phương thức & endpoint:** `GET /api/correspondents/`, `GET /api/correspondents/{id}/`, `GET /api/document_types/`, `GET /api/document_types/{id}/`

## 1. Mô tả

Schema khai báo các trường này là **bắt buộc** (`required`) trong response, nhưng API không trả về:

| Endpoint | Trường schema nói bắt buộc | Thực tế |
|---|---|---|
| `GET /api/correspondents/` | `last_correspondence` | không có trong response |
| `GET /api/correspondents/{id}/` | `permissions` | không có trong response |
| `GET /api/document_types/` | `permissions` | không có trong response |
| `GET /api/document_types/{id}/` | `permissions` | không có trong response |

Ngoài ra cùng nhóm nguyên nhân: `POST /api/correspondents/` và `POST /api/document_types/` trả `201 Created`
nhưng thiếu `document_count` — đây chính là BUG-03 do TV2 phát hiện trước đó, TV1 ghi lại để thấy cùng một
nguồn lỗi (schema/response lệch nhau) xuất hiện ở cả phương thức GET.

## 2. Các bước tái hiện

```bash
curl -s -H "Authorization: Token <TOKEN>" http://localhost:8000/api/correspondents/ | python -m json.tool
curl -s -H "Authorization: Token <TOKEN>" http://localhost:8000/api/correspondents/1/ | python -m json.tool
curl -s -H "Authorization: Token <TOKEN>" http://localhost:8000/api/document_types/ | python -m json.tool
```

Trích file JUnit `results/TV1_round1_seed101.xml`:

```
Test Case ID: HRip4b — GET /api/correspondents/   — "last_correspondence" is a required property
Test Case ID: (vòng 1)  — GET /api/correspondents/{id}/ — "permissions" is a required property
Test Case ID: Ymv9RX — GET /api/document_types/    — "permissions" is a required property
```

Nguyên văn công cụ:

```
- Response violates schema

    "permissions" is a required property

    Validated against the response schema for status code 200.

    Schema at /components/schemas/DocumentType:
        { "required": ["document_count", "id", "name", "permissions", "slug", "user_can_change"], ... }
```

## 3. Kết quả mong đợi

Response phải chứa đủ các trường `required` như schema khai báo, **hoặc** schema phải bỏ các trường
không thực sự được trả về khỏi danh sách `required`.

## 4. Phân loại

| Trường | Nội dung |
|---|---|
| Loại lỗi | Response vi phạm schema (lệch giữa đặc tả và triển khai) |
| Chiều gây lỗi | Không phải lỗi 500; client đọc `permissions`/`last_correspondence` theo schema sẽ nhận `None`/lỗi |
| Tái hiện trên máy khác? | Có — cùng image `3.1.3`, chỉ cần 1 lệnh `curl` |
| Phân loại | **đã xác nhận** (so trực tiếp response thật với `required` trong `/api/schema/`) |
