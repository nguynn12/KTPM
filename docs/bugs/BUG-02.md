# LỖI BUG-02: Server trả về HTTP 500 do unhandled ValueError khi lọc năm ngoài khoảng 1..9999

## 1. Thao tác thực hiện
Gửi request `GET /api/documents/` với tham số query lọc năm sửa đổi `modified__year` mang giá trị số thực âm rất nhỏ `-1.17e-38` (hoặc số nguyên âm `<= 0`).

URL gửi đi:
```text
http://localhost:8000/api/documents/?modified__year=-1.17e-38
```

## 2. Đoạn mã nguồn liên quan
Trong file `src/documents/filters.py`, lớp `DocumentFilterSet` kế thừa `django_filters.rest_framework.FilterSet`, và thư viện nội bộ của Django tại `django/db/backends/base/operations.py:636`:
```python
bounds = connection.ops.year_lookup_bounds_for_datetime_field(year, iso_year=iso_year)
first = datetime.datetime(value, 1, 1)
```

## 3. Phân tích nguyên nhân kỹ thuật
- Áp dụng kỹ thuật Phân tích giá trị biên (Boundary Value Analysis - BVA) trên tham số query thời gian.
- Trong `src/documents/views.py`, `DocumentViewSet` sử dụng `filterset_class = DocumentFilterSet`.
- Mặc định `django-filter` cho phép tra cứu `modified__year` dưới dạng số nguyên nhưng không cấu hình ràng buộc khoảng giá trị tối thiểu và tối đa (`min_value`, `max_value`).
- Khi chuỗi `-1.17e-38` được chuyển đổi thành số nguyên `0`, ORM của Django cố gắng xây dựng câu lệnh SQL bằng cách gọi `datetime.datetime(value, 1, 1)`.
- Module `datetime` của Python bắt buộc năm phải nằm trong khoảng từ `1` đến `9999`. Khi `value = 0`, Python ném ra ngoại lệ: `ValueError: year must be in 1..9999, not 0`.
- Ngoại lệ này phát sinh trong quá trình biên dịch câu truy vấn SQL (`compile`), không được bẫy ở tầng bộ lọc và không chuyển đổi thành lỗi 400, dẫn đến sập toàn bộ request với HTTP 500.

## 4. KẾT QUẢ MONG ĐỢI
- HTTP Status Code: `400 Bad Request`
- Response Body: Bộ lọc phải kiểm tra tính hợp lệ của tham số query và trả về thông báo lỗi:
```json
{
  "modified__year": [
    "Select a valid year between 1 and 9999."
  ]
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
File "/usr/local/lib/python3.14/site-packages/django/db/backends/base/operations.py", line 636, in year_lookup_bounds_for_datetime_field
  first = datetime.datetime(value, 1, 1)
ValueError: year must be in 1..9999, not 0
```

## 6. Lệnh tái hiện (Curl)
```bash
curl -X GET "http://localhost:8000/api/documents/?modified__year=-1.17e-38" \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a"
```

## 7. Đề xuất khắc phục
Trong `DocumentFilterSet`, khai báo tường minh ràng buộc khoảng giá trị cho trường lọc năm:
```python
modified__year = django_filters.NumberFilter(
    field_name="modified",
    lookup_expr="year",
    min_value=1,
    max_value=9999,
)
```
