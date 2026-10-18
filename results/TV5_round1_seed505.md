# TV5 – Vòng 1 (chỉ operation GET), seed 505

## 1. Thông tin chạy

| Mục | Giá trị |
|---|---|
| Thành viên | Trần Quốc Khánh (TV5, MSSV 2312646) |
| Ngày chạy | 2026-10-18 |
| Hệ điều hành / RAM | Microsoft Windows v10.0.26300.9711, RAM 8GB; chạy trong WSL2 (kernel Linux 6.18.33.2-microsoft-standard-WSL2, theo /api/status) |
| Docker / Docker Compose | Docker v29.8.0 / Docker Compose v5.5.1 |
| Paperless-ngx | v3.1.3 (commit d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e) |
| Schemathesis | 4.30.1 (image `schemathesis/schemathesis:4.30.1`) |
| Seed | 505 |
| Vòng | 1: chọn operation GET trên toàn bộ schema (không lọc đường dẫn) |
| Điều kiện trước | Hệ thống vừa dựng lại và seed bằng `scripts/seed_data.py` |
| Dữ liệu seed | `scripts/seed_data.py` của TV2: 4 tag, 3 correspondent, 3 document type, 2 file txt (2 tài liệu) |

Lệnh đã chạy (token đã được lọc):

```bash
docker run --rm -v "$PWD/results:/results" --network ktpm_default \
  schemathesis/schemathesis:4.30.1 run http://webserver:8000/api/schema/ \
  --wait-for-schema 120 --include-method GET --seed 505 --max-examples 25 \
  -H "Authorization: Token [FILTERED]" --report junit,ndjson \
  --report-junit-path /results/TV5_round1_seed505_junit.xml \
  --report-ndjson-path /results/TV5_round1_seed505.ndjson --no-color
```

File kèm: `TV5_round1_seed505.log`, `TV5_round1_seed505.ndjson`, `TV5_round1_seed505_junit.xml`.

## 2. Số liệu (lấy từ log), đối chiếu với TV2

| Mục | TV5 (seed 505) | TV2 (seed 202) |
|---|---|---|
| Operations được test | 65/163 (39.8%) | 65/163 (39.8%) |
| Test case sinh ra | 2851 (196 skipped, 2 errored) | 2517 (176 skipped) |
| Test case thất bại / lỗi riêng biệt | 100 / 122 | 97 / 121 |
| Thời gian chạy | 170.45s | 183.35s |
| Server error | 13 | 13 |
| Response violates schema | 16 | 10 |
| API accepted schema-violating request | 9 | 13 |
| API rejected schema-compliant request | 13 | 13 |
| Invalid Allow header | 1 | 1 |
| Undocumented Content-Type | 4 | 4 |
| Undocumented HTTP status code | 65 | 66 |
| Unsupported methods | 1 | 1 |

Các pha: Examples bỏ qua 65 operation (không có ví dụ trong schema); Coverage 8 đạt / 57 lỗi (42.48s); Fuzzing 12 đạt / 53 lỗi (54.92s); Stateful 320 kịch bản, 258 đạt / 62 lỗi (72.73s), 11/90 API link được phủ.

Độ phủ schema: Operations 65/163 (39.8%), Parameters 190/597 (31.8%), Responses 55/207 (26.5%), Examples 1/72.

Cảnh báo của công cụ: `GET /api/documents/{id}/share_links/` liên tục trả 404 nên không tới được logic chính (thiếu dữ liệu test).

## 3. Kiểm tra từ ndjson: Vòng 1 có sửa dữ liệu không?

Dù chọn `--include-method GET`, công cụ vẫn gửi thêm request với phương thức không được tài liệu hóa:

| Phương thức | Kết quả (số lần) |
|---|---|
| GET | 200: 1767; 400: 132; 401: 196; 404: 480; 500: 42 |
| DELETE | 405: 22 |
| PATCH | 405: 25 |
| POST | 405: 38 |
| PUT | 405: 26 |
| QUERY | 405: 40 |
| TRACE | 405: 40; 500: 1 |
| OPTIONS | 200: 39; 500: 1 |

Mọi request POST/PUT/PATCH/DELETE đều bị từ chối 405, nên Vòng 1 không làm thay đổi dữ liệu.

## 4. Lỗi 500 (13)

| # | Operation | Input kích hoạt | Phạm vi 4 nhóm |
|---|---|---|---|
| 1 | GET /api/documents/ | tham số `shared_by__id=false` (xem mục 6) | Trong |
| 2–9 | GET /api/documents/{id}/ai_suggestions, history, metadata, preview, root, share_links, suggestions, thumb | id không phải số (`null,null` hoặc ký tự lạ) | Trong |
| 10 | TRACE /api/documents/{id}/notes/ | phương thức TRACE | Trong |
| 11 | GET /api/share_link_bundles/ | `created__year` ngoài khoảng | Ngoài |
| 12 | GET /api/share_links/ (Stateful) | `created__month`, `expiration__year`... giá trị lạ | Ngoài |
| 13 | OPTIONS /api/profile/totp/ | phương thức OPTIONS | Ngoài |

Đối chiếu chéo: cả 13 operation này đều có 5xx trong ndjson Vòng 1 của TV2, nên được hai seed xác nhận. Đây là so khớp theo operation, chưa chứng minh cùng nguyên nhân.

## 5. Phân loại các nhóm còn lại (sơ bộ)

| Nhóm | Nhận xét | Phân loại gợi ý |
|---|---|---|
| Undocumented HTTP status (65) | Chủ yếu 404 "Invalid page" khi `page=0` hoặc âm, 404 khi id=0, và 400. Schema chỉ khai báo 200. | Schema lệch |
| Response violates schema (16) | `permissions`/`user_can_change` thiếu khi không có `full_perms=true`; `root_document` là null; `history` trả danh sách thay vì đối tượng phân trang; `/api/status` có `error: null`. | Phần lớn schema lệch, cần xem từng ca |
| Rejected schema-compliant (13) | Ràng buộc không khai báo: `query` phải ≥3 ký tự, `limit` phải dương, ký tự NULL, chỉ một trong `text`/`query`/`title_search`; `ai_suggestions` báo "AI is required" (chưa bật AI). | Schema lệch; ca AI là do môi trường |
| Accepted schema-violating (9) | `page_size=null` được bỏ qua và trả 200. | Hành vi dung thứ, gần false positive |
| Undocumented Content-Type (4) | `download`, `preview` trả text/plain; `thumb` trả image/webp; một ca trả HTML. | Schema lệch; ca HTML cần xem tay |

## 6. Tái hiện bằng curl (độc lập với Schemathesis)

| Request | Kết quả |
|---|---|
| GET /api/documents/null%2Cnull/{ai_suggestions, history, metadata, preview, root, suggestions, thumb}/ | 500 (cả 7) |
| GET /api/documents/1/metadata/ (đối chứng) | 200 |
| GET /api/documents/99999/metadata/ (đối chứng) | 404 |
| GET /api/documents/?modified__year=-1.1754943508222875e-38 (BUG-02 của TV2) | 500 |
| GET /api/share_link_bundles/?created__year=-107907925428658.0 | 500 |
| GET /api/share_links/?expiration__year=-0.3333333333333333 | 500 |
| TRACE /api/documents/0/notes/ | 500 |
| OPTIONS /api/profile/totp/ | 500 |
| GET /api/documents/ với 10 tham số của ca gây lỗi | 500; bỏ riêng `shared_by__id=false` thì 200, bỏ tham số khác vẫn 500 |

Các lệnh curl chạy sau Vòng 3, trên DB hiện tại.

## 7. Việc còn mở

- Phân tích 2 test case "errored" trong ndjson.
- Xác nhận `GET /api/documents/?shared_by__id=false` đứng một mình có gây 500 không, và lấy traceback.
- Lần đếm `count` của `/api/documents/` ngay sau khi seed trả 4, trong khi danh sách chỉ có 2 bản ghi (ID 1 và 2). Chưa giải thích được.
