# LỖI BUG-01: Server trả về HTTP 500 do unhandled TypeError trong validate_set_permissions

## 1. Thao tác thực hiện
Gửi request `POST /api/tags/` (hoặc `/api/correspondents/`, `/api/document_types/`) với payload chứa cấu trúc phân quyền `set_permissions` nhưng giá trị của hành động không phải là một dictionary (ví dụ: `"view": false`).

Payload gửi đi:
```json
{
  "name": "Test_Perm_Crash",
  "set_permissions": {
    "view": false
  }
}
```

## 2. Đoạn mã nguồn liên quan
Trong file `src/documents/serialisers.py:238-242`, hàm `validate_set_permissions` thuộc lớp `SerializerWithPerms`:
```python
if set_permissions is not None:
    for action in ["view", "change"]:
        if action in set_permissions:
            if "users" in set_permissions[action]:
                users = set_permissions[action]["users"]
```

## 3. Phân tích nguyên nhân kỹ thuật
- Áp dụng kỹ thuật Đoán lỗi (Error Guessing) và Fuzzing kiểu dữ liệu đầu vào.
- Tại dòng 240, mã nguồn chỉ kiểm tra sự tồn tại của khóa `if action in set_permissions:`.
- Tại dòng 241, lập trình viên truy cập trực tiếp bằng toán tử `in`: `if "users" in set_permissions[action]:` với giả định rằng giá trị của `action` luôn là kiểu dictionary.
- Khi người dùng hoặc công cụ kiểm thử gửi giá trị kiểu boolean (`false`), số nguyên hoặc null, toán tử `in` trên kiểu boolean trong Python lập tức ném ra ngoại lệ: `TypeError: argument of type 'bool' is not a container or iterable`.
- Đoạn mã không kiểm tra `isinstance(set_permissions[action], dict)` và không bọc trong khối `try...except` để ném `serializers.ValidationError`, dẫn đến ngoại lệ thoát ra ngoài làm sập tiến trình xử lý request và máy chủ trả về HTTP 500.

## 4. KẾT QUẢ MONG ĐỢI
- HTTP Status Code: `400 Bad Request`
- Response Body: Máy chủ phải bẫy lỗi hợp lệ và trả về thông báo lỗi kiểm tra dữ liệu theo chuẩn REST API:
```json
{
  "set_permissions": {
    "view": [
      "Expected a dictionary of permissions, but got boolean."
    ]
  }
}
```

## 5. KẾT QUẢ THỰC TẾ
- HTTP Status Code: `500 Internal Server Error`
- Response Body:
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
- Traceback từ log container (`paperless-webserver`):
```text
File "/usr/src/paperless/src/documents/serialisers.py", line 241, in validate_set_permissions
  if "users" in set_permissions[action]:
TypeError: argument of type 'bool' is not a container or iterable
```

## 6. Lệnh tái hiện (Curl)
```bash
curl -X POST http://localhost:8000/api/tags/ \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test_Perm_Crash", "set_permissions": {"view": false}}'
```

## 7. Đề xuất khắc phục
Bổ sung kiểm tra kiểu dữ liệu trước khi truy cập phần tử bên trong:
```python
if action in set_permissions:
    if not isinstance(set_permissions[action], dict):
        raise serializers.ValidationError({action: "Expected a dictionary object."})
    if "users" in set_permissions[action]:
        users = set_permissions[action]["users"]
```
