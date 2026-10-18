# TV5 – Vòng 1 (GET), seed 505

| Mục | Giá trị |
|---|---|
| Thành viên / ngày chạy | Trần Quốc Khánh (TV5) / 2026-10-18 |
| Hệ điều hành, RAM | Microsoft Windows [Version 10.0.26300.9711] |
| Docker / Paperless-ngx / Schemathesis | [ĐIỀN docker --version] / v3.1.3 / 4.30.1 |
| Seed | 505 |
| Vòng | 1: --include-method GET, toàn bộ schema (không có --include-path-regex) |
| Lệnh đã chạy | docker run ... schemathesis/schemathesis:4.30.1 run http://webserver:8000/api/schema/ --wait-for-schema 120 --include-method GET --seed 505 --max-examples 25 -H "Authorization: Token [FILTERED]" --report junit,ndjson ... |
| Operations | 65/163 (39.8%) |
| Test case sinh ra | 2851 (196 skipped, 2 errored chưa phân tích) |
| Test thất bại | 100 test case, 122 lỗi riêng biệt |
| Thời gian | 170.45s |
| Phân loại (công cụ in) | Server error 13, Response violates schema 16, Accepted schema-violating 9, Rejected schema-compliant 13, Invalid Allow header 1, Undocumented Content-Type 4, Undocumented HTTP status 65, Unsupported methods 1 |
| Dữ liệu seed | scripts/seed_data.py của TV2 (4 tag, 3 correspondent, 3 document type, 2 file txt) |

## Kiểm tra từ ndjson
Phương thức khác GET đều nhận 405 (DELETE 22, PATCH 25, POST 38, PUT 26, QUERY 40, TRACE 40), trừ TRACE 500 x1 và OPTIONS 500 x1. Vòng 1 không sửa dữ liệu.

## Tái hiện bằng curl (lần 2, độc lập với Schemathesis)
| Request | Kết quả |
|---|---|
| GET /api/documents/null%2Cnull/{ai_suggestions,history,metadata,preview,root,suggestions,thumb}/ | 500 (cả 7) |
| GET /api/documents/1/metadata/ (đối chứng) | 200 |
| GET /api/documents/99999/metadata/ (đối chứng) | 404 |
| GET /api/documents/?modified__year=-1.1754943508222875e-38 (BUG-02) | 500 |
| GET /api/share_link_bundles/?created__year=-107907925428658.0 | 500 |
| GET /api/share_links/?expiration__year=-0.3333333333333333 | 500 |
| TRACE /api/documents/0/notes/ | 500 |
| OPTIONS /api/profile/totp/ | 500 |
| GET /api/documents/?fields=... (curl nguyên bản trong log) | 500 (2/2 lần) |
