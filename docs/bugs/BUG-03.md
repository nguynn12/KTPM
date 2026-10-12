# Báo cáo lỗi: BUG-03

## 1. Thông tin chung
- **Mã lỗi:** BUG-03
- **Tiêu đề:** Response trả về HTTP 201 vi phạm OpenAPI Schema (thiếu các trường bắt buộc `document_count`, `last_correspondence`, `permissions`)
- **Mức độ nghiêm trọng:** Medium (Schema Inconsistency / Contract Violation)
- **Phương thức & Endpoint:** `POST /api/correspondents/`, `POST /api/tags/`
- **Người phát hiện:** TV2 (Tạ Nhật Nguyên)
- **Công cụ phát hiện:** Schemathesis v4.30.1 (Vòng 2 & Vòng 3, Seed: 202, Test Case ID: `vNBfDm`)

---

## 2. Mô tả lỗi (Summary)
Theo tài liệu đặc tả OpenAPI sinh tự động (`/api/schema/`), schema của đối tượng `Correspondent` quy định danh sách các trường bắt buộc (`required`) trong phản hồi gồm có:
`['document_count', 'id', 'last_correspondence', 'name', 'permissions', 'slug', 'user_can_change']`.
Tuy nhiên, khi gọi API `POST /api/correspondents/` để tạo mới một đối tượng thành công, phản hồi trả về `HTTP 201 Created` nhưng payload JSON thực tế chỉ chứa 8 trường cơ bản và hoàn toàn **thiếu các trường `document_count`, `last_correspondence`, `permissions`**. Điều này vi phạm hợp đồng API (API Contract Violation), khiến các bộ client sinh tự động hoặc công cụ kiểm thử như Schemathesis báo lỗi không khớp schema.

---

## 3. Các bước tái hiện (Steps to Reproduce)
Gửi request HTTP POST để tạo mới một đối tượng Correspondent:

```bash
curl -X POST http://localhost:8000/api/correspondents/ \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test_Schema_Violation_Correspondent"}'
```

---

## 4. Kết quả thực tế (Actual Result)
- **HTTP Status Code:** `201 Created`
- **Response Body (JSON):**
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
*Lưu ý:* Các trường `document_count`, `last_correspondence`, và `permissions` hoàn toàn không có mặt trong response payload.

- **Thông báo lỗi từ Schemathesis:**
```text
- Response violates schema
    "document_count" is a required property
    Validated against the response schema for status code 201.
```

---

## 5. Kết quả mong đợi (Expected Result)
Phản hồi từ API phải tuân thủ nghiêm ngặt theo tài liệu đặc tả OpenAPI được công bố. Một trong hai cách giải quyết:
1. Hoặc API trả về đầy đủ các trường đã cam kết trong schema với giá trị mặc định khi tạo mới (ví dụ `"document_count": 0`, `"last_correspondence": null`, `"permissions": {"view": {"users": [], "groups": []}, ...}`).
2. Hoặc cấu hình OpenAPI Schema (thông qua decorator `@extend_schema`) để tách biệt rõ Response Schema khi tạo mới (Create Response) và Response Schema khi truy vấn chi tiết (Retrieve Response), đánh dấu các trường này là tùy chọn (`required: false`) hoặc `read_only=True` kèm `nullable`.

---

## 6. Liên kết mã nguồn và Nguyên nhân gốc (Root Cause Analysis - Phần C)
- **Tập tin liên quan:** [src/documents/serialisers.py:530-580](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/serialisers.py#L530-L580) và [src/documents/views.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/views.py)
- **Lớp / Hàm:** `CorrespondentSerializer` và `CorrespondentViewSet.create()`
- **Giải thích cơ chế gây lỗi:**
  1. Trong `views.py`, phương thức `get_queryset()` của ViewSet sử dụng ORM annotation (`annotate(document_count=Count('documents'), last_correspondence=Max('documents__created'))`) để bổ sung các trường tính toán này vào QuerySet khi thực hiện truy vấn `GET`.
  2. Tuy nhiên, khi một đối tượng được tạo mới qua `POST`, phương thức mặc định `CreateModelMixin.create()` của DRF chỉ đơn giản lưu instance (`serializer.save()`) và trả về `serializer.data` từ chính instance vừa lưu đó. Instance này chưa đi qua `get_queryset()` nên không mang các thuộc tính tính toán (`document_count`, `last_correspondence`).
  3. Đồng thời, thư viện sinh schema `drf-spectacular` khi phân tích `CorrespondentSerializer` đã dùng chung một schema cho cả phương thức `GET`, `POST`, `PUT`, và đánh dấu các trường này là bắt buộc trong response 201.
  4. Hậu quả là có sự không nhất quán giữa dữ liệu thực tế trả về sau khi tạo mới và schema mà hệ thống tự động công bố cho client.

- **Đề xuất khắc phục:**
  Trong `CorrespondentViewSet`, sau khi tạo thành công đối tượng, truy vấn lại instance thông qua `self.get_queryset().get(pk=instance.pk)` trước khi trả về dữ liệu serialize; hoặc sử dụng `@extend_schema_view(create=extend_schema(responses={201: ...}))` để định nghĩa schema phản hồi chính xác cho hành động tạo mới.
