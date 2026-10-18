# LỖI BUG-05: Tài liệu OpenAPI ghi thiếu mã trạng thái và Content-Type mà API thực tế trả về

- **Mã lỗi:** BUG-05 (TV1)
- **Người phát hiện:** Trần Gia Huy (TV1)
- **Công cụ phát hiện:** Schemathesis 4.30.1, seed 101 — check `status_code_conformance` / `content_type_conformance`
- **Mức độ:** Low–Medium (không làm hỏng chức năng, nhưng làm sai tài liệu API và làm client sinh mã sai)
- **Phạm vi:** `tags`, `correspondents`, `document_types`, `documents`

## 1. Mô tả

Schema OpenAPI do chính Paperless-ngx phát ở `/api/schema/` **không liệt kê đủ** các mã trạng thái và
kiểu nội dung mà API trả về trong thực tế. Schemathesis phát hiện 108 lỗi "Undocumented HTTP status code"
và 6 lỗi "Undocumented Content-Type" trong 3 vòng chạy (số lỗi khác nhau theo thống kê của công cụ).

## 2. Bằng chứng (Test Case ID đọc từ file JUnit của TV1)

| Endpoint | Tài liệu ghi | Thực tế trả | Test Case ID |
|---|---|---|---|
| `GET /api/tags/{id}/` (id không tồn tại) | không ghi 404 | `404` | Vòng 1 `yTZzye`, Vòng 2 `fkWPHj` |
| `DELETE /api/tags/{id}/` | không ghi 404 | `404` | `ADm3zu` |
| `PUT /api/tags/{id}/` | không ghi 404 | `404` | `94SGhk` |
| `POST /api/tags/` (payload thiếu trường) | không ghi 400 | `400` | `Gj3vp6` |
| `PATCH /api/documents/{id}/versions/{version_id}/` | không ghi 403 | `403` | `CNPN21` |
| `GET /api/documents/{id}/download/` | không ghi `application/pdf` | `Content-Type: application/pdf` | `sGzLlM` |
| `GET /api/documents/{id}/thumb/` | không ghi `image/webp` | `Content-Type: image/webp` | `A9mtyD` |

Lệnh tái hiện (đọc nguyên văn từ trường `Reproduce with` của JUnit):

```bash
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/tags/999999/
curl -i -X POST -H "Authorization: Token <TOKEN>" -H "Content-Type: application/json" -d '{}' http://localhost:8000/api/tags/
curl -i -H "Authorization: Token <TOKEN>" http://localhost:8000/api/documents/<id>/download/
```

Tổng hợp theo nhóm (đếm trên 3 file JUnit của TV1):

| Mã trạng thái gặp nhưng không có trong tài liệu | Số testcase |
|---|---|
| `404` | 39 |
| `400` | 20 |
| `403` | 2 |

## 3. Kết quả thực tế / mong đợi

- **Thực tế:** API trả 404/400/403 (đúng về mặt REST) nhưng schema không ghi.
- **Mong đợi:** schema ở `/api/schema/` phải liệt kê đủ các mã trạng thái và Content-Type mà API có thể trả.

## 4. Phân loại

| Trường | Nội dung |
|---|---|
| Loại lỗi | Lỗi **tài liệu/đặc tả** (schema sai thiếu), không phải lỗi chức năng của API |
| Vì sao vẫn phải báo | Client sinh từ schema (SDK, codegen) sẽ hiểu sai; các vòng kiểm thử tự động sẽ báo "lỗi" dù hành vi đúng |
| Tái hiện trên máy khác? | Có — cùng image `3.1.3` và cùng schema thì cùng kết quả |
| Phân loại | **đã xác nhận** (bằng chứng trong JUnit + gọi lại bằng HTTP thấy đúng mã đó) |
