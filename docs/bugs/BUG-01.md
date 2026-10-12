# Báo cáo lỗi: BUG-01

## 1. Thông tin chung
- **Mã lỗi:** BUG-01
- **Tiêu đề:** Server trả về HTTP 500 do unhandled `TypeError` khi payload `set_permissions` chứa giá trị không phải dictionary
- **Mức độ nghiêm trọng:** High (Internal Server Error)
- **Phương thức & Endpoint:** `POST /api/tags/`, `POST /api/correspondents/`, `POST /api/document_types/`
- **Người phát hiện:** TV2 (Tạ Nhật Nguyên)
- **Công cụ phát hiện:** Schemathesis v4.30.1 (Vòng 3, Seed: 202, Test Case ID: `uGoMNK`)

---

## 2. Mô tả lỗi (Summary)
Khi client gửi request tạo mới một đối tượng (Tag, Correspondent hoặc DocumentType) với trường `set_permissions` chứa cấu trúc lồng nhau nhưng giá trị của hành động (`view` hoặc `change`) không phải là một `dict` (ví dụ gửi giá trị kiểu boolean: `"view": false`), máy chủ Paperless-ngx gặp lỗi ngoại lệ chưa được xử lý (`TypeError: argument of type 'bool' is not a container or iterable`) và trả về mã phản hồi `500 Internal Server Error` dạng trang HTML thay vì trả về `400 Bad Request` kèm thông báo lỗi kiểm tra hợp lệ dữ liệu (validation error).

---

## 3. Các bước tái hiện (Steps to Reproduce)
Gửi request HTTP POST đến endpoint `http://localhost:8000/api/tags/` với Authorization Token và payload JSON sau:

```bash
curl -X POST http://localhost:8000/api/tags/ \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test_Perm_Crash", "set_permissions": {"view": false}}'
```

---

## 4. Kết quả thực tế (Actual Result)
- **HTTP Status Code:** `500 Internal Server Error`
- **Response Body:**
```html
<!doctype html>
<html lang="en">
<head>
  <title>Server Error (500)</title>
</head>
<body>
  <h1>Server Error (500)</h1><p></p>
</body>
</html>
```

- **Traceback từ Docker Container Log (`paperless-webserver`):**
```python
File "/usr/local/lib/python3.14/site-packages/rest_framework/views.py", line 512, in dispatch
  response = handler(request, *args, **kwargs)
File "/usr/local/lib/python3.14/site-packages/rest_framework/mixins.py", line 18, in create
  serializer.is_valid(raise_exception=True)
File "/usr/local/lib/python3.14/site-packages/rest_framework/serializers.py", line 225, in is_valid
  self._validated_data = self.run_validation(self.initial_data)
File "/usr/local/lib/python3.14/site-packages/rest_framework/serializers.py", line 515, in to_internal_value
  validated_value = validate_method(validated_value)
File "/usr/src/paperless/src/documents/serialisers.py", line 241, in validate_set_permissions
  if "users" in set_permissions[action]:
TypeError: argument of type 'bool' is not a container or iterable
```

---

## 5. Kết quả mong đợi (Expected Result)
- **HTTP Status Code:** `400 Bad Request`
- **Response Body (JSON):**
```json
{
  "set_permissions": {
    "view": ["Expected a dictionary of permissions, but got boolean."]
  }
}
```
Máy chủ phải bẫy lỗi kiểm tra kiểu dữ liệu đầu vào và trả về lỗi `400 Bad Request` theo chuẩn RESTful API, không được để crash ứng dụng bằng lỗi `500`.

---

## 6. Liên kết mã nguồn và Nguyên nhân gốc (Root Cause Analysis - Phần C)
- **Tập tin liên quan:** [src/documents/serialisers.py:233-253](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/serialisers.py#L233-L253)
- **Lớp / Hàm:** `SerializerWithPerms.validate_set_permissions(self, set_permissions=None)`
- **Vị trí dòng:** Dòng 240-241:
```python
238:         if set_permissions is not None:
239:             for action in ["view", "change"]:
240:                 if action in set_permissions:
241:                     if "users" in set_permissions[action]:
242:                         users = set_permissions[action]["users"]
```

- **Giải thích cơ chế gây lỗi:**
  1. Khi nhận dữ liệu từ request, Django REST Framework gọi phương thức xác thực `validate_set_permissions()`.
  2. Vòng lặp duyệt qua các khóa `"view"` và `"change"`. Tại dòng 240, mã nguồn chỉ kiểm tra sự tồn tại của khóa (`if action in set_permissions:`).
  3. Tại dòng 241, lập trình viên truy cập trực tiếp `set_permissions[action]` bằng toán tử `in` (`if "users" in set_permissions[action]:`) với giả định rằng giá trị tương ứng luôn là một dictionary.
  4. Khi client gửi giá trị là boolean (`false`), số nguyên, hoặc chuỗi không tương thích, toán tử `in` trên kiểu boolean trong Python lập tức ném ra ngoại lệ `TypeError: argument of type 'bool' is not a container or iterable`.
  5. Ngoại lệ này không được bọc trong khối `try...except` và không raise `serializers.ValidationError`, dẫn đến việc Django không xử lý được và trả về lỗi `500`.

- **Đề xuất khắc phục:**
  Bổ sung kiểm tra kiểu dữ liệu trước khi truy cập phần tử:
```python
if action in set_permissions:
    if not isinstance(set_permissions[action], dict):
        raise serializers.ValidationError({action: "Expected a dictionary object."})
    if "users" in set_permissions[action]:
        ...
```
