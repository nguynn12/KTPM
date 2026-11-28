# TV5 – Vòng 2 (ghi dữ liệu trên tags, correspondents, document_types), seed 505

## 1. Thông tin chạy

| Mục | Giá trị |
|---|---|
| Thành viên | Trần Quốc Khánh (TV5, MSSV 2312646) |
| Ngày chạy | 2026-10-18 |
| Hệ điều hành / RAM | Microsoft Windows v10.0.26300.9711, RAM 8GB; chạy trong WSL2 |
| Docker / Docker Compose | Docker v29.8.0 / Docker Compose v5.5.1 |
| Paperless-ngx | v3.1.3 (commit d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e) |
| Schemathesis | 4.30.1 (image `schemathesis/schemathesis:4.30.1`) |
| Seed | 505 |
| Vòng | 2: GET, POST, PUT, PATCH, DELETE trên tags, correspondents, document_types |
| Điều kiện trước | Đã chạy `docker compose down -v`, `docker compose up -d` và `scripts/seed_data.py` trước vòng này |
| Dữ liệu seed | `scripts/seed_data.py` của TV2: 4 tag, 3 correspondent, 3 document type, 2 file txt |

Lệnh đã chạy (token đã được lọc):

```bash
docker run --rm -v "$PWD/results:/results" --network ktpm_default \
  schemathesis/schemathesis:4.30.1 run http://webserver:8000/api/schema/ \
  --wait-for-schema 120 \
  --include-path-regex "^/api/(tags|correspondents|document_types)/" \
  --seed 505 --max-examples 25 \
  -H "Authorization: Token [FILTERED]" --report junit,ndjson \
  --report-junit-path /results/TV5_round2_seed505_junit.xml \
  --report-ndjson-path /results/TV5_round2_seed505.ndjson --no-color
```

File kèm: `TV5_round2_seed505.log`, `TV5_round2_seed505.ndjson`, `TV5_round2_seed505_junit.xml`.

## 2. Số liệu (lấy từ log), đối chiếu với TV2

| Mục | TV5 (seed 505) | TV2 (seed 202) |
|---|---|---|
| Operations được test | 18/163 (11.0%) | 18/163 (11.0%) |
| Test case sinh ra | 1940 (72 skipped) | 1481 (72 skipped) |
| Test case thất bại / lỗi riêng biệt | 51 / 58 | 49 / 58 |
| Thời gian chạy | 158.26s | 203.24s |
| Server error | 1 | 1 |
| Response violates schema | 14 | 13 |
| API accepted schema-violating request | 3 | 4 |
| API rejected schema-compliant request | 12 | 12 |
| Undocumented HTTP status code | 28 | 28 |

Độ phủ schema: Operations 18/163 (11.0%), Parameters 41/597 (6.8%), Responses 18/207 (8.6%), Examples 0/72.

## 3. Lỗi 500 duy nhất: POST /api/correspondents/

Input trong log (ca `rlOU7h`): `set_permissions.change.users = 10060` (số nguyên thay vì danh sách). Trong ndjson Vòng 2 của TV2, lỗi 500 duy nhất cũng ở `POST /api/correspondents/`, với `set_permissions.change.users = true`. Hai seed cùng gặp nên đạt chuẩn "đã xác nhận".

Tái hiện bằng curl (độc lập với Schemathesis):

| Request (POST /api/correspondents/) | Kết quả |
|---|---|
| `set_permissions.change.users = 10060` (2 lần) | 500, 500 |
| `set_permissions.change.users = true` | 500 |
| `set_permissions.view = false` (trigger gốc trong BUG-01.md) | 500 |
| `set_permissions.change.users = []` (đối chứng hợp lệ) | 201 |

Traceback từ log webserver: `TypeError: argument of type 'bool' is not a container or iterable` tại `src/documents/serialisers.py`, dòng 241, hàm `validate_set_permissions`; và `TypeError: 'bool' object is not iterable`.

Đọc mã nguồn v3.1.3 (chưa chạy): `validate_set_permissions` (dòng 233) gán `users` từ dữ liệu vào rồi gọi `_validate_user_ids` (dòng 213–217), hàm này dùng `User.objects.filter(id__in=user_ids)` và `len(user_ids)` mà không kiểm tra kiểu. Đây là cùng hàm với BUG-01 nhưng trigger đi qua dòng mã khác (`users` không phải danh sách, thay vì giá trị của `view`/`change` không phải dictionary). Đề xuất bổ sung làm biến thể của BUG-01.

## 4. BUG-03: thiếu `document_count` trong phản hồi 201

Log Vòng 2 báo `"document_count" is a required property` ở cả ba `POST`: correspondents (log dòng 713), document_types (dòng 786) và tags (dòng 859). Tái hiện bằng curl `POST` với body `{"name": "..."}`, mỗi tài nguyên 2 lần: cả 6 phản hồi 201 đều không có `document_count`. Trong khi các phản hồi `GET` cùng tài nguyên có trường này. BUG-03 trong repo hiện chỉ mô tả correspondents, nên mô tả cần mở rộng sang document_types và tags.

Các lệnh curl chạy sau Vòng 3, trên DB hiện tại.

## 5. Phân loại các nhóm còn lại (sơ bộ)

Chi tiết từng ca: xem `TV5_round2_seed505.log`. Các nhóm điển hình:

| Nhóm | Ví dụ thấy trong log | Phân loại gợi ý |
|---|---|---|
| Undocumented HTTP status (28) | 400 khi `owner` là id không tồn tại hoặc bộ lọc chứa ký tự NULL; schema chỉ khai báo 200/201 | Schema lệch |
| Rejected schema-compliant (12) | `owner` là id không tồn tại (400 "Invalid pk"), ký tự NULL trong bộ lọc (400) | Schema lệch (ràng buộc không khai báo) |
| Accepted schema-violating (3) | `full_perms` truyền số/chuỗi vẫn trả 200; `set_permissions.view = null` được chấp nhận 201 | Hành vi dung thứ |
| Response violates schema (14) | `user_can_change` thiếu khi `full_perms=true` ở tags; `document_count` thiếu ở phản hồi 201 | Phần lớn schema lệch; `document_count` là BUG-03 |
| Server error (1) | POST /api/correspondents/ với `users` không phải danh sách | Lỗi thật (mục 3) |

## 6. Việc còn mở

- Đọc hết 58 lỗi riêng biệt trong log và gán nhãn từng ca (bảng mục 5 mới chỉ nêu nhóm điển hình).
