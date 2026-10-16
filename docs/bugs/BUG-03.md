# LỖI BUG-03: Response 201 vi phạm OpenAPI Schema do thiếu trường document_count

## 1. Thao tác thực hiện
Gửi request `POST /api/correspondents/` để tạo mới một đối tượng người gửi thư (Correspondent) với các trường hợp lệ tối thiểu.

Payload gửi đi:
```json
{
  "name": "Test_Schema_Violation_Correspondent"
}
```

## 2. Đoạn mã nguồn và Schema liên quan
- Trong OpenAPI Schema (`http://localhost:8000/api/schema/?format=json`):
  Tại mục `#/components/schemas/Correspondent`, danh sách các trường bắt buộc (`required`) được định nghĩa gồm:
  ```json
  "required": [
    "document_count",
    "id",
    "last_correspondence",
    "name",
    "permissions",
    "slug",
    "user_can_change"
  ]
  ```
- Trong file `src/documents/serialisers.py:544-559`, lớp `CorrespondentSerializer`:
  Trường `document_count` được liệt kê trong danh sách `fields` của Meta.
- Trong file `src/documents/views.py`, lớp `CorrespondentViewSet`:
  Trường `document_count` chỉ được tính toán bằng `annotate(document_count=Count('documents'))` trong hàm `get_queryset()`.

## 3. Phân tích nguyên nhân kỹ thuật
- Áp dụng kỹ thuật Kiểm thử dựa trên lược đồ (Schema-based Testing / API Contract Testing).
- Trong tài liệu OpenAPI Schema, hệ thống cam kết rằng mọi phản hồi trả về đối tượng `Correspondent` (bao gồm cả mã 201 khi POST tạo mới) đều bắt buộc phải có trường `document_count`.
- Tuy nhiên trong thực tế mã nguồn, khi client gọi `POST /api/correspondents/`, phương thức mặc định `create()` của Django REST Framework chỉ lưu instance vào cơ sở dữ liệu và trả về `serializer.data` từ chính instance đó.
- Instance vừa tạo chưa được nạp qua hàm `get_queryset()`, do đó không mang thuộc tính tính toán `document_count`.
- Kết quả là phản hồi thực tế trả về không chứa trường `document_count`, dẫn đến vi phạm hợp đồng giao tiếp API (API Contract Inconsistency) đã công bố với client. Lỗi này được công cụ Schemathesis phát hiện tự động tại Test Case ID `vNBfDm`.

## 4. KẾT QUẢ MONG ĐỢI
- HTTP Status Code: `201 Created`
- Response Body: Phản hồi phải tuân thủ đúng cam kết của Schema:
  1. Hoặc trả về đầy đủ trường `document_count` với giá trị ban đầu là `0`:
  ```json
  {
    "id": 130,
    "name": "Test_Schema_Violation_Correspondent",
    "document_count": 0,
    ...
  }
  ```
  2. Hoặc cấu hình lại Schema để tách biệt Response của hành động tạo mới (Create Response), đánh dấu `document_count` là không bắt buộc (`required: false`).

## 5. KẾT QUẢ THỰC TẾ
- HTTP Status Code: `201 Created`
- Response Body:
```json
{
  "id": 130,
  "slug": "test_schema_violation_correspondent",
  "name": "Test_Schema_Violation_Correspondent",
  "match": "",
  "matching_algorithm": 1,
  "is_insensitive": true,
  "owner": 2,
  "user_can_change": true
}
```
*(Hoàn toàn thiếu trường `document_count`, `last_correspondence`, `permissions`).*

- Thông báo vi phạm ghi nhận từ Schemathesis (`results/TV2_round2_seed202_junit.xml`):
```text
- Response violates schema
    "document_count" is a required property
    Validated against the response schema for status code 201.
```

## 6. Lệnh tái hiện (Curl)
```bash
curl -X POST http://localhost:8000/api/correspondents/ \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test_Schema_Violation_Correspondent"}'
```

## 7. Đề xuất khắc phục
Trong `CorrespondentViewSet`, nạp lại đối tượng thông qua `get_queryset()` sau khi lưu để bổ sung các trường tính toán trước khi serialize trả về client:
```python
def perform_create(self, serializer):
    instance = serializer.save()
    return self.get_queryset().get(pk=instance.pk)
```
Hoặc cấu hình decorator `@extend_schema_view` để định nghĩa schema phản hồi cho phương thức `create` không yêu cầu trường `document_count`.
