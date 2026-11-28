# TV5 – Vòng 3 (mở rộng thêm documents, bật --checks all), seed 505

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
| Vòng | 3: tags, correspondents, document_types, documents; `--checks all` |
| Điều kiện trước | Đã chạy `docker compose down -v`, `docker compose up -d` và `scripts/seed_data.py` trước vòng này. Bằng chứng: tag Schemathesis tạo đầu tiên có id=5 và correspondent id=4, tức DB có sẵn 4 tag và 3 correspondent từ seed |
| Dữ liệu seed | 4 tag, 3 correspondent, 3 document type, 2 file txt (2 tài liệu) |

Lệnh đã chạy (token đã được lọc):

```bash
docker run --rm -v "$PWD/results:/results" --network ktpm_default \
  schemathesis/schemathesis:4.30.1 run http://webserver:8000/api/schema/ \
  --wait-for-schema 120 \
  --include-path-regex "^/api/(tags|correspondents|document_types|documents)/" \
  --seed 505 --max-examples 25 --checks all \
  -H "Authorization: Token [FILTERED]" --report junit,ndjson \
  --report-junit-path /results/TV5_round3_seed505_junit.xml \
  --report-ndjson-path /results/TV5_round3_seed505.ndjson --no-color
```

File kèm: `TV5_round3_seed505.log`, `TV5_round3_seed505.ndjson`, `TV5_round3_seed505_junit.xml`.

## 2. Số liệu (lấy từ log), đối chiếu với TV2

| Mục | TV5 (seed 505) | TV2 (seed 202) |
|---|---|---|
| Operations được test | 53/163 (32.5%) | 53/163 (32.5%) |
| Test case sinh ra | 1517 (148 skipped) | 2056 (120 skipped) |
| Test case thất bại / lỗi riêng biệt | 104 / 130 | 108 / 136 |
| Thời gian chạy | 132.31s | 211.21s |
| Server error | 14 | 16 |
| Response violates schema | 22 | 17 |
| API accepted schema-violating request | 0 | 5 |
| API rejected schema-compliant request | 25 | 23 |
| Undocumented Content-Type | 3 | 5 |
| Undocumented HTTP status code | 65 | 69 |
| Unsupported methods | 1 | 1 |

Các pha: Examples bỏ qua 53 operation; Coverage 2 đạt / 51 lỗi (15.52s); Fuzzing 7 đạt / 46 lỗi (50.70s); Stateful 204 kịch bản, 154 đạt / 50 lỗi (65.67s), 48/181 API link được phủ.

Độ phủ schema: Operations 53/163 (32.5%), Parameters 95/597 (15.9%), Examples 6/72 (8.3%), Responses 47/207 (22.7%).

Cảnh báo của công cụ:
- `DELETE` và `PATCH` `/api/documents/{id}/versions/{version_id}/` trả 403 dạng trang HTML (không phải JSON của DRF). TV2 cũng gặp ở hai operation này. Chưa giải thích được, cần kiểm tra thủ công; không kết luận là lỗi xác thực.
- `GET /api/documents/{id}/share_links/` liên tục trả 404 nên không tới được logic chính.

## 3. Lỗi 500 (14 lỗi do công cụ đếm, cộng thêm POST notes)

| # | Operation | Input kích hoạt |
|---|---|---|
| 1 | GET /api/documents/ | tham số `shared_by__id=false` (xem mục 5) |
| 2–10 | GET /api/documents/{id}/ai_suggestions, history, metadata, notes, preview, root, share_links, suggestions, thumb | id không phải số (`null,null` hoặc ký tự lạ) |
| 11 | DELETE /api/documents/{id}/notes/ | id không phải số |
| 12 | POST /api/documents/edit_pdf/ | `{"documents": [], "operations": []}` |
| 13 | POST /api/documents/{id}/email/ | id=0, không có body |
| 14 | TRACE /api/documents/{id}/notes/ | phương thức TRACE (công cụ cũng tính vào "Unsupported methods") |
| (phụ) | POST /api/documents/{id}/notes/ | id không phải số; công cụ chỉ tính là "Undocumented status 500" |

Đối chiếu chéo: tất cả các operation trên đều có 5xx trong ndjson Vòng 3 của TV2, nên được hai seed xác nhận (so khớp theo operation). TV2 còn có 500 trong phần Stateful (GET, POST, PUT) mà log của TV5 Vòng 3 không có, đó là lỗi phụ thuộc seed (BUG-01 được TV5 xác nhận ở Vòng 2 và bằng curl).

Lỗi mới so với Vòng 1 và 2: `edit_pdf`, `{id}/email`, và `notes` (GET/POST/DELETE).

## 4. BUG-03 trong Vòng 3

Cả ba `POST` (correspondents, document_types, tags) trả 201 nhưng thiếu `document_count`, đều bị công cụ báo "Response violates schema".

## 5. Tái hiện bằng curl (độc lập với Schemathesis)

| Request | Kết quả |
|---|---|
| POST /api/documents/edit_pdf/ `{"documents":[],"operations":[]}` (2 lần) | 500, 500 |
| POST /api/documents/edit_pdf/ không body (đối chứng) | 400 |
| POST /api/documents/0/email/ không body (2 lần) | 500, 500 |
| GET, DELETE, POST /api/documents/null%2Cnull/notes/ | 500 (cả 3); log: `ValueError: Field 'id' expected a number but got 'null,null'` |
| GET /api/documents/99999/notes/ (đối chứng) | 404 |
| TRACE /api/documents/0/notes/ | 500; log: `KeyError: 'TRACE'` |
| GET /api/documents/?modified__year=-1.1754943508222875e-38 (BUG-02, 2 lần) | 500, 500; log: `ValueError: year must be in 1..9999, not 0` |
| POST correspondents / document_types / tags, body `{"name": "..."}` (mỗi loại 2 lần) | cả 6 phản hồi 201 đều thiếu `document_count` (BUG-03) |
| GET /api/documents/ với 10 tham số của ca gây lỗi | 500; bỏ riêng `shared_by__id=false` thì 200, bỏ tham số khác vẫn 500 |

Đọc mã nguồn v3.1.3 (chưa chạy):
- `history` (dòng 1903), `share_links` (1872) và `notes` (1754) trong `src/documents/views.py` gọi `Document.objects.get(pk=pk)` và chỉ bắt `Document.DoesNotExist`; id không phải số gây ngoại lệ khác nên ra 500. Log của `notes` khớp với nhận định này. Các action còn lại (metadata, root, suggestions, ai_suggestions, preview, thumb) đi qua hàm trợ giúp mà tôi chưa đọc nên chưa kết luận chung.
- Lớp `SharedByUser` (`src/documents/filters.py`, dòng 212) đưa giá trị tham số thẳng vào `qs.filter(owner_id=value)` mà không ép kiểu. Đây là dự đoán cho lỗi `shared_by__id=false`, chưa xác nhận bằng traceback.

## 6. Phân loại các nhóm còn lại (sơ bộ)

| Nhóm | Nhận xét | Phân loại gợi ý |
|---|---|---|
| Undocumented HTTP status (65) | 404 và 400 chưa được mô tả; schema chỉ khai báo 200/201/204 | Schema lệch |
| Rejected schema-compliant (25) | Quy tắc nghiệp vụ không khai báo ("documents is required unless all is true", `version_label` bắt buộc), `owner`/`parent` là id không tồn tại, ký tự NULL, ràng buộc trùng owner/name; "AI is required for this feature" | Schema lệch; ca AI là do môi trường |
| Response violates schema (22) | `last_correspondence`, `permissions`, `is_shared_by_requester` thiếu hoặc null, `root_document` là null, `history` trả danh sách | Phần lớn schema lệch |
| Undocumented Content-Type (3) | `download`, `preview` trả text/plain; `thumb` trả image/webp | Schema lệch |

## 7. Việc còn mở

- Lấy traceback của `POST /api/documents/edit_pdf/` và `POST /api/documents/{id}/email/` ngay sau khi gọi (lần trước log bị cắt).
- Xác nhận `GET /api/documents/?shared_by__id=false` đứng một mình có gây 500 không, và kiểm tra khai báo kiểu của `shared_by__id` trong `/api/schema/`.
- Đọc hết 130 lỗi riêng biệt trong log và gán nhãn từng ca.
