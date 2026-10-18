# TV5 – Vòng 2 (ghi dữ liệu tags/correspondents/document_types), seed 505

| Mục | Giá trị |
|---|---|
| Thành viên / ngày chạy | Trần Quốc Khánh (TV5) / 2026-10-18 |
| Hệ điều hành, RAM / Docker | [copy từ file Vòng 1] |
| Paperless-ngx / Schemathesis | v3.1.3 / 4.30.1 |
| Seed | 505 |
| Vòng | 2: --include-path-regex "^/api/(tags|correspondents|document_types)/" |
| Điều kiện trước | [ĐIỀN: đã reset_sys + seed lại chưa? documents=2?] |
| Operations | 18/163 (11.0%) |
| Test case sinh ra | 1940 (72 skipped) |
| Test thất bại | 51 test case, 58 lỗi riêng biệt |
| Thời gian | 158.26s |
| Phân loại (công cụ in) | Server error 1, Response violates schema 14, Accepted schema-violating 3, Rejected schema-compliant 12, Undocumented HTTP status 28 |
| Lỗi 500 | POST /api/correspondents/, set_permissions.change.users = 10060 (không phải danh sách); cùng hàm với BUG-01 (validate_set_permissions, serialisers.py:233). TV2 seed 202 cũng gặp (users = true) |
