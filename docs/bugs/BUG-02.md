# Báo cáo lỗi: BUG-02

## 1. Thông tin chung
- **Mã lỗi:** BUG-02
- **Tiêu đề:** Server trả về HTTP 500 do unhandled `ValueError` khi tham số lọc năm (`modified__year`) nằm ngoài giới hạn hợp lệ (1..9999)
- **Mức độ nghiêm trọng:** Medium
- **Phương thức & Endpoint:** `GET /api/documents/`
- **Người phát hiện:** TV2 (Tạ Nhật Nguyên)
- **Công cụ phát hiện:** Schemathesis v4.30.1 (Vòng 1 & Vòng 3, Seed: 202)

---

## 2. Mô tả lỗi (Summary)
Khi client gửi request tìm kiếm và lọc danh sách tài liệu với tham số query `modified__year` mang giá trị số thực âm rất nhỏ (ví dụ `-1.17e-38`) hoặc giá trị âm/vượt quá ngưỡng cho phép của kiểu ngày tháng năm, bộ lọc `django-filter` chuyển giá trị này xuống trình tạo câu truy vấn cơ sở dữ liệu của Django (`django.db.backends.base.operations`). Tại đây, hàm khởi tạo đối tượng `datetime.datetime(value, 1, 1)` ném ra ngoại lệ `ValueError: year must be in 1..9999, not 0`. Máy chủ không bẫy ngoại lệ này dẫn đến phản hồi lỗi `500 Internal Server Error` dạng HTML thay vì `400 Bad Request`.

---

## 3. Các bước tái hiện (Steps to Reproduce)
Gửi request HTTP GET đến endpoint `http://localhost:8000/api/documents/` với tham số query và Authorization Token:

```bash
curl -X GET "http://localhost:8000/api/documents/?modified__year=-1.17e-38" \
  -H "Authorization: Token 3716828bfd21075a2fb68f1b959d02d2756f8d7a"
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
File "/usr/local/lib/python3.14/site-packages/django/db/models/lookups.py", line 744, in as_sql
  start, finish = self.year_lookup_bounds(connection, self.rhs)
File "/usr/local/lib/python3.14/site-packages/django/db/models/lookups.py", line 724, in year_lookup_bounds
  bounds = connection.ops.year_lookup_bounds_for_datetime_field(year, iso_year=iso_year)
File "/usr/local/lib/python3.14/site-packages/django/db/backends/base/operations.py", line 636, in year_lookup_bounds_for_datetime_field
  first = datetime.datetime(value, 1, 1)
ValueError: year must be in 1..9999, not 0
```

---

## 5. Kết quả mong đợi (Expected Result)
- **HTTP Status Code:** `400 Bad Request`
- **Response Body (JSON):**
```json
{
  "modified__year": [
    "Select a valid year between 1 and 9999."
  ]
}
```
API cần xác thực giá trị tham số lọc đầu vào từ query parameter trước khi chuyển vào ORM QuerySet. Khi giá trị không hợp lệ, phải trả về lỗi `400 Bad Request`.

---

## 6. Liên kết mã nguồn và Nguyên nhân gốc (Root Cause Analysis - Phần C)
- **Tập tin liên quan:** [src/documents/filters.py:46-120](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/filters.py#L46-L120) và [src/documents/views.py](file:///c:/Users/storm/Downloads/KiemThuPhanMem/KTPM/paperless-ngx/src/documents/views.py)
- **Lớp / Cấu hình:** `DocumentFilterSet` (kế thừa từ `django_filters.rest_framework.FilterSet`)
- **Giải thích cơ chế gây lỗi:**
  1. Trong `src/documents/views.py`, lớp `DocumentViewSet` thiết lập `filterset_class = DocumentFilterSet`.
  2. Trong `DocumentFilterSet`, trường `modified` được cấu hình bộ lọc theo thuộc tính thời gian (bao gồm lookup `__year`).
  3. Mặc định `django-filter` coi lookup `year` là kiểu số nguyên thông thường mà không áp đặt ràng buộc giá trị tối thiểu (`min_value=1`) và tối đa (`max_value=9999`).
  4. Khi giá trị chuỗi số khoa học `-1.17e-38` được ép kiểu thành số nguyên `0`, ORM của Django cố gắng xây dựng giới hạn ngày truy vấn bằng `datetime.datetime(value, 1, 1)`. Vì chuẩn module `datetime` trong Python chỉ chấp nhận năm từ `1` đến `9999`, hàm này ném ra `ValueError`.
  5. Ngoại lệ này xảy ra ở tầng cơ sở dữ liệu (khi thực thi compile câu lệnh SQL `as_sql`), nằm ngoài tầm bắt lỗi mặc định của `django-filter`, khiến toàn bộ request sụp đổ với HTTP 500.

- **Đề xuất khắc phục:**
  Trong `DocumentFilterSet`, định nghĩa bộ lọc cho các trường ngày tháng năm có kiểm tra ràng buộc:
```python
modified__year = django_filters.NumberFilter(
    field_name="modified",
    lookup_expr="year",
    min_value=1,
    max_value=9999,
)
```
