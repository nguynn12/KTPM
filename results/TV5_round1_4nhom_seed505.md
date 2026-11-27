# TV5 – Vòng 1 (4 nhóm endpoint, chỉ GET), seed 505

> Đây là bản **chạy lại** vòng 1 để khớp đúng phạm vi với vòng 1 của **TV1 (seed 101)** và
> **TV3 (seed 303)**: 4 nhóm tài nguyên + loại bỏ các method ghi = **19/163 operation**.
> Bộ vòng 1 cũ của TV5 (`--include-method GET`, không lọc đường dẫn → **65 operation**) vẫn
> được giữ nguyên ở `TV5_round1_seed505.*` để đối chiếu lịch sử, **không bị ghi đè**.

## 1. Thông tin chạy

| Mục | Giá trị |
|---|---|
| Thành viên | Trần Quốc Khánh (TV5, MSSV 2312646) |
| Ngày chạy | 2026-10-18 |
| Hệ điều hành / RAM | Microsoft Windows v10.0.26300.9711, RAM 8GB; chạy trong WSL2 (kernel Linux 6.18.33.2-microsoft-standard-WSL2) |
| Docker / Docker Compose | Docker v29.8.0 / Docker Compose v5.5.1 |
| Paperless-ngx | v3.1.3 (commit d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e) |
| Schemathesis | 4.30.1 (image `schemathesis/schemathesis:4.30.1`) |
| Seed | 505 |
| Vòng | 1: **chỉ operation GET** trên **4 nhóm tài nguyên** (tags, correspondents, document_types, documents) |
| Phạm vi regex | `^/api/(tags\|correspondents\|document_types\|documents)/` |
| Method loại trừ | POST, PUT, PATCH, DELETE (viết lặp 4 lần cờ `--exclude-method`) |
| Phases | `examples,fuzzing` |
| Checks | 5 check cốt lõi: `not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance` |
| Cấu hình sinh | `--seed 505`, `--max-examples 25`, `--workers 1` |
| Điều kiện trước | `docker compose down -v` → `docker compose up -d` → chờ webserver `healthy` → `scripts/seed_data.py` |
| Dữ liệu seed | 4 tag, 3 correspondent, 3 document type, 2 tài liệu `.txt` (đã xác nhận lại bằng API trước khi chạy: 4/3/3/2) |
| Exit code CLI | `1` (1 = chạy xong và có vi phạm được phát hiện) |

Lệnh đã chạy (token đã được Schemathesis lọc thành `[Filtered]`):

```bash
docker run --rm -v "$PWD/results:/results" --network ktpm_default \
  schemathesis/schemathesis:4.30.1 run http://webserver:8000/api/schema/ \
  --wait-for-schema 120 \
  --include-path-regex "^/api/(tags|correspondents|document_types|documents)/" \
  --exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE \
  --phases examples,fuzzing \
  --checks not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance \
  --seed 505 --max-examples 25 --workers 1 \
  -H "Authorization: Token [FILTERED]" --report junit,ndjson \
  --report-junit-path /results/TV5_round1_4nhom_seed505_junit.xml \
  --report-ndjson-path /results/TV5_round1_4nhom_seed505.ndjson --no-color
```

File kèm: `TV5_round1_4nhom_seed505.log`, `TV5_round1_4nhom_seed505.ndjson`, `TV5_round1_4nhom_seed505_junit.xml`.

## 2. Số liệu (lấy từ log), đối chiếu với TV1 và TV3

| Mục | TV5 (seed 505) | TV1 (seed 101) | TV3 (seed 303) |
|---|---|---|---|
| Operations được test | 19/163 (11.6%) | 19/163 | 19/163 |
| Test case sinh ra (CLI) | 112 | 99 | 74 |
| Test case thất bại (CLI) | 16 | 16 | 17 |
| Lỗi khác nhau (unique failures) | 20 | 20 | 22 |
| JUnit: `<testcase>` / failures | 19 / 16 | 19 / 16 | 19 / 17 |
| Thời gian chạy | 11.65s | 9.41s | 1.17s |
| Server error | 3 | 4 | — |
| Response violates schema | 8 | 4 | — |
| Undocumented Content-Type | 3 | 3 | — |
| Undocumented HTTP status code | 6 | 9 | — |

Nguồn đối chiếu: `TV1_round1_seed101_summary.md` (nhánh `TV1_TranGiaHuy`) và
`TV3_round1_seed303_20261016_093736_summary.md` (nhánh `TV3_KhiemThuan`).

Chi tiết pha: `Examples` bỏ qua 19 operation (không có ví dụ trong schema, 0.07s);
`Fuzzing` 3 đạt / 16 thất bại (11.43s). `Coverage` và `Stateful` **không bật** (đúng cấu hình vòng 1).

> Ghi nhớ khi đọc số: `--max-examples 25` là giới hạn sinh của Hypothesis cho mỗi operation,
> không phải tổng số request; số `<testcase>` là số operation × check được ánh xạ, không phải số
> request HTTP; **unique failures không phải số bug**.

## 3. 16 operation thất bại (tổng 20 lỗi khác nhau)

| # | Operation | Test Case ID | Loại vi phạm |
|---|---|---|---|
| 1 | `GET /api/correspondents/` | `jOJusG` | Response violates schema (`last_correspondence` là required) |
| 2 | `GET /api/correspondents/{id}/` | `UZCYSo` | Response violates schema (`permissions` là required) |
| 3 | `GET /api/document_types/` | `fjoU5j` | Response violates schema (`permissions` là required) |
| 4 | `GET /api/document_types/{id}/` | `qzwBSU` | Response violates schema (`permissions` là required) |
| 5 | `GET /api/documents/` | `eUkF20` | Undocumented HTTP status code (nhận 400, tài liệu ghi 200) — `custom_field_query` không phải JSON |
| 6 | `GET /api/documents/{id}/` | `tkK0ZV` | Response violates schema ×2 (`permissions` required; `root_document = null` không phải integer) |
| 7 | `GET /api/documents/{id}/ai_suggestions/` | `2sxbe9` | **Server error 500** + Undocumented HTTP status code |
| 8 | `GET /api/documents/{id}/download/` | `y8XdMH` | Undocumented Content-Type (`text/plain` thay vì `application/json`) |
| 9 | `GET /api/documents/{id}/history/` | `ejfqvb` | Response violates schema (trả mảng thay vì object `PaginatedLogEntryList`) |
| 10 | `GET /api/documents/{id}/preview/` | `F6djAf` | Undocumented Content-Type |
| 11 | `GET /api/documents/{id}/root/` | `CiYsNP` | Undocumented HTTP status code (nhận 404, tài liệu ghi 200) |
| 12 | `GET /api/documents/{id}/share_links/` | `DC47i7` | **Server error 500** + Undocumented HTTP status code |
| 13 | `GET /api/documents/{id}/suggestions/` | `s8XG0j` | **Server error 500** + Undocumented HTTP status code |
| 14 | `GET /api/documents/{id}/thumb/` | `bBSU0S` | Undocumented Content-Type (`image/webp`) |
| 15 | `GET /api/tags/` | `b8OhaF` | Undocumented HTTP status code (nhận 404 `Invalid page.`) |
| 16 | `GET /api/tags/{id}/` | `IBobeo` | Response violates schema (`user_can_change` là required) |

Ba lỗi 500 đáng chú ý (đều ở nhóm `documents`, đều là GET nên vẫn thuộc vòng đọc an toàn):

- `GET /api/documents/false/ai_suggestions/` → 500 (id không phải số).
- `GET /api/documents/{id}/share_links/` → 500.
- `GET /api/documents/true/suggestions/` → 500 (id không phải số).

## 4. Độ phủ schema

| Chỉ số | Giá trị |
|---|---|
| Operations | 19/163 (11.6%) |
| Parameters | 10/597 (1.6%), 22 partial |
| Keywords | 13/9285 (0.1%), 22 partial |
| Examples | 0/72 (0.0%) |
| Responses | 22/207 (10.6%) |
| Response Keywords | 265/6235 (4.2%) |

## 5. Vòng 1 có sửa dữ liệu không?

Có — kiểm tra theo hai cách, kết luận **không sửa gì**:

1. **Theo cấu hình**: 19 operation được chọn đều là GET; 4 method ghi đã bị loại bằng
   `--exclude-method` (lặp 4 lần) và bộ checks chỉ gồm 5 check cốt lõi — **không bật** check
   `unsupported_method` (khác với bộ vòng 1 cũ dùng toàn bộ checks, vốn có gửi thêm request
   method không được tài liệu hóa).
2. **Theo trạng thái dữ liệu**: đo bằng API **trước** và **sau** khi chạy, đều là
   `tags = 4`, `correspondents = 3`, `document_types = 3`, `documents = 2`.

## 6. Ghi chú về vòng 1 cũ (65 operation)

Vòng 1 cũ (`results/TV5_round1_seed505.*`, chạy 2026-10-18 07:39) dùng lệnh:

```bash
... run ... --include-method GET --seed 505 --max-examples 25 ...
```

Lệnh này **không lọc đường dẫn** nên Schemathesis chọn **GET trên toàn bộ schema = 65/163
operation** (gồm cả các endpoint không thuộc 4 nhóm tài nguyên), và chạy pha mặc định
(examples/coverage/fuzzing/stateful) → 2851 test / 100 thất bại / 122 lỗi khác nhau.
Vì phạm vi và phases khác nên số liệu đó **không so sánh trực tiếp được** với vòng 1 của
TV1/TV3 — đó là lý do có bản chạy lại này.

Nguyên nhân cần lặp cờ `--exclude-method` 4 lần: trong Schemathesis 4.30.1, nhiều cờ `--include-*`
bị ghép **OR** (nên `--include-path-regex X` + `--include-method GET` không cho ra "chỉ GET trong
X"), và `--exclude-method` chỉ nhận **một** giá trị mỗi lần — viết `POST,PUT,PATCH,DELETE` trong
một cờ sẽ bị bỏ qua và phạm vi trở lại thành 53 operation.
