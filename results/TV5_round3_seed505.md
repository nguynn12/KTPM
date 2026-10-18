# TV5 – Vòng 3 (mở rộng + documents, --checks all), seed 505

| Mục | Giá trị |
|---|---|
| Thành viên / ngày chạy | Trần Quốc Khánh (TV5) / 2026-10-18 |
| Hệ điều hành, RAM / Docker | [copy từ file Vòng 1] |
| Paperless-ngx / Schemathesis | v3.1.3 / 4.30.1 |
| Seed | 505 |
| Vòng | 3: --include-path-regex "^/api/(tags|correspondents|document_types|documents)/" --checks all |
| Điều kiện trước | Đã reset (down -v) và seed lại bằng scripts/seed_data.py (tag mới id=5, correspondent mới id=4 cho thấy DB sạch) |
| Operations | 53/163 (32.5%) |
| Test case sinh ra | 1517 (148 skipped) |
| Test thất bại | 104 test case, 130 lỗi riêng biệt |
| Thời gian | 132.31s |
| Phân loại (công cụ in) | Server error 14, Response violates schema 22, Rejected schema-compliant 25, Undocumented Content-Type 3, Undocumented HTTP status 65, Unsupported methods 1 |
| Lỗi 500 mới (so với V1, V2) | POST /documents/edit_pdf/ (documents=[], operations=[]); POST /documents/{id}/email/ (id=0, không body); GET/POST/DELETE /documents/{id}/notes/ (id không phải số) |
| Cảnh báo | 403 dạng HTML ở DELETE/PATCH /documents/{id}/versions/{version_id}/ (TV2 cũng gặp); 1 operation thiếu test data (GET /documents/{id}/share_links/) |

## Tái hiện bằng curl (độc lập với Schemathesis)
| Request | Kết quả |
|---|---|
| POST /api/documents/edit_pdf/ {"documents":[],"operations":[]} (2 lần) | 500, 500 (đối chứng không body: 400) |
| POST /api/documents/0/email/ không body (2 lần) | 500, 500 |
| GET, DELETE, POST /api/documents/null%2Cnull/notes/ | 500 (cả 3); log: ValueError: Field 'id' expected a number but got 'null,null' |
| GET /api/documents/99999/notes/ (đối chứng) | 404 |
| TRACE /api/documents/0/notes/ | 500; log: KeyError: 'TRACE' |
| GET /api/documents/?modified__year=-1.1754943508222875e-38 (BUG-02, 2 lần) | 500, 500; log: ValueError: year must be in 1..9999, not 0 |
| POST correspondents / document_types / tags (mỗi loại 2 lần) | cả 6 lần 201 thiếu document_count (BUG-03) |
| GET /api/documents/?<10 tham số của ca F5Y4gz> | 500; bỏ shared_by__id=false thì 200 |
