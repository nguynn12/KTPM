# BẢNG ĐỐI CHIẾU SEED 303 VÀ GHI CHÚ KỸ THUẬT CHƯƠNG 3 — TV3

**Thành viên thực hiện:** TV3 — Nguyễn Khiêm Thuận (MSSV: `2312764`)  
**Seed kiểm thử:** `303`  
**Nhánh TV3 gốc:** `TV3_KhiemThuan` (HEAD trước PR: `1b95e106729c5e36b65f2fba51d227b4ae592d53`; commit chứa kết quả XML/NDJSON/summary: `f3233e7fc984d52201158ab32c58291bff8aa26b`)  
**Commit bổ sung CLI log gốc đã làm sạch trong PR này:** `52cb0fe136e59fffffccb88a3ae8dfcc16068040`  
**Môi trường xác minh:** Paperless-ngx `v3.1.3` (`ghcr.io/paperless-ngx/paperless-ngx:3.1.3`), Schemathesis `4.30.1`, Hypothesis `6.169.0`, Python `3.14.4`, Docker Desktop `29.7.2` (Windows 11, `http://localhost:8000`)  
**Đặc tả OpenAPI cục bộ:** OpenAPI `3.0.3` (`Paperless-ngx REST API 6.0.0 (10)`, tổng `163` operations) — [`docs/openapi_TV3.json`](https://github.com/nguynn12/KTPM/blob/dcf2c91fe67278bab6d8535807430dcd03641502/docs/openapi_TV3.json) (SHA256: `888b0f89ec0a9f65293f5320a86b1810d7904f93033178b567e313d951b12e3a`)  
**Mục đích:** Đối chiếu toàn bộ tệp log CLI, JUnit XML, NDJSON và bản tóm tắt của seed `303`; lập bảng chuẩn 3 dòng cho 3 vòng chạy phục vụ tổng hợp báo cáo cuối kỳ; tách riêng lượt chạy ngày 13/10 khác phạm vi; rà soát mô tả K05, các phép kiểm tra đã dùng và giới hạn của đánh giá dựa trên OpenAPI để chuyển cho người sửa Chương 3.

---

## 1. Bảng đối chiếu chính thức 3 vòng chạy (Seed 303)

> **Quy ước ghi nhận:** Mỗi dòng dưới đây tương ứng với **đúng một lượt chạy chuẩn** trên máy TV3 (ngày `16/10/2026`), đã kiểm tra chéo khớp hoàn toàn giữa `.log`, `.xml` và `.ndjson`. Không trộn lẫn đơn vị `operations`, `JUnit <testcase>`, `CLI generated cases`, `JUnit <failure>` và `CLI unique failures`. Lượt chạy ngày `13/10/2026` (`99` operations, khác phạm vi) được tách riêng ở Mục 2.

| Vòng | Phạm vi (Đường dẫn & Phương thức) | Operation được chọn | Ca sinh ra (CLI) | Failure (JUnit) | Unique failure (CLI) | Thời gian (giây) | Nguồn đối chiếu tại commit cụ thể |
|:---:|---|---:|---:|---:|---:|---:|---|
| **1** | **Chỉ đọc `GET` trên 4 nhóm API** (`tags`, `correspondents`, `document_types`, `documents`): `19 GET` (0 phương thức ghi, 0 endpoint ngoài 4 nhóm); `--phases examples,fuzzing`; 5 checks response cốt lõi | **19 / 163** *(11,66%)* | **74** *(0 skipped, 0 errored; 17 ca phát hiện lỗi)* | **17 / 19** *(`errors=0`, `skipped=0`; 17 thẻ `<failure>`; không có `Stateful tests`)* | **22** *(1 warning)* | **2,71** *(NDJSON: `2,714` \| JUnit: `2,519`)* | [log (`52cb0fe`)](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round1_seed303_20261016_093736.log) · [xml (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_20261016_093736.xml) · [ndjson (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_20261016_093736.ndjson) |
| **2** | **Đọc/ghi CRUD trên 3 nhóm danh mục** (`tags`, `correspondents`, `document_types`): `6 GET`, `3 POST`, `3 PUT`, `3 PATCH`, `3 DELETE` (0 endpoint ngoài 3 nhóm); 4 pha mặc định; `--checks all` | **18 / 163** *(11,04%)* | **744** *(68 skipped, 0 errored; 44 ca phát hiện lỗi)* | **19 / 19** *(18 ops + 1 `Stateful tests`; `errors=0`; 44 thẻ `<failure>`)* | **51** *(0 warning)* | **42,12** *(NDJSON: `42,120` \| JUnit: `40,363`)* | [log (`52cb0fe`)](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round2_seed303_20261016_093803.log) · [xml (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round2_seed303_20261016_093803.xml) · [ndjson (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round2_seed303_20261016_093803.ndjson) |
| **3** | **Toàn diện 4 nhóm API + `documents`**: `19 GET`, `19 POST`, `4 PUT`, `5 PATCH`, `6 DELETE` (0 endpoint ngoài 4 nhóm; pha `Coverage` gửi thêm probe `TRACE`/`QUERY`/`OPTIONS`); 4 pha mặc định; `--checks all` | **53 / 163** *(32,52%)* | **1.734** *(112 skipped, **1 errored**; 108 ca phát hiện lỗi)* | **53 / 54** *(53 ops + 1 `Stateful tests`; chỉ `GET /api/documents/next_asn/` đạt; `errors=0`; 108 thẻ `<failure>`)* | **131** *(2 warnings)* | **102,41** *(NDJSON: `102,407` \| JUnit: `99,581`)* | [log (`52cb0fe`)](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round3_seed303_20261016_093930.log) · [xml (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round3_seed303_20261016_093930.xml) · [ndjson (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round3_seed303_20261016_093930.ndjson) |

### 1.1 Đối chiếu chi tiết theo pha, tương tác HTTP và phân loại lỗi (Seed 303)

| Hạng mục đối chiếu | Vòng 1 chuẩn *(19 ops)* | Vòng 2 *(18 ops)* | Vòng 3 *(53 ops)* | Lượt tách riêng 13/10 *(99 ops)* |
|---|---:|---:|---:|---:|
| **Thời gian chạy (`UTC+7`, theo NDJSON)** | `2026-10-16 09:37:37 → 09:37:41` | `2026-10-16 09:38:03 → 09:38:47` | `2026-10-16 09:39:31 → 09:41:15` | `2026-10-13 11:58:34 → 11:59:01` |
| **Thời gian tải schema (`CLI` \| `NDJSON`)** | `1,17 s` \| `1,185 s` | `1,06 s` \| `1,072 s` | `0,91 s` \| `0,922 s` | `1,03 s` \| `1,046 s` |
| **Số `interactions` HTTP lưu trong NDJSON** | **74** (`74 GET`) | **744** (`330 GET`, `209 POST`, `113 DELETE`, `51 PUT`, `41 PATCH`) | **1.733** (`701 GET`, `684 POST`, `113 PATCH`, `106 DELETE`, `86 PUT`, `15 TRACE`, `14 QUERY`, `14 OPTIONS`) | **489** (`396 GET`, `72 POST`, `10 DELETE`, `6 PATCH`, `5 PUT`) |
| **Pha `Examples`** | 19 skipped (`0,03 s`) | 18 skipped (`0,04 s`) | 53 skipped (`0,06 s`) | 99 skipped (`0,07 s`) |
| **Pha `Coverage`** | *Disabled* | 0 passed / 18 failed (`1,72 s`) | 2 passed / 51 failed (`9,86 s`) | *Disabled* |
| **Pha `Fuzzing`** | 2 passed / 17 failed (`2,58 s`) | 3 passed / 15 failed (`6,21 s`) | 4 passed / 49 failed (`10,33 s`) | 17 passed / 82 failed (`26,03 s`) |
| **Pha `Stateful`** | *Disabled* | 138 kịch bản (`102 passed / 36 failed`, `36/63` inferred links, `34,03 s`) | 256 kịch bản (`193 passed / 63 failed`, `53/181` inferred links, `82,02 s`) | *Disabled* |
| **• `Server error` (`not_a_server_error`)** | **5** | **1** *(Stateful `POST /api/tags/`)* | **14** *(12 ops + `TRACE .../notes/` + Stateful `POST /api/document_types/`)* | **8** |
| **• `Response violates schema` (`response_schema_conformance`)** | **4** | **14** | **19** | **24** |
| **• `API accepted schema-violating request` (`negative_data_rejection`)** | *Không bật* | **0** | **3** | *Không bật* |
| **• `API rejected schema-compliant request` (`positive_data_acceptance`)** | *Không bật* | **10** | **24** | *Không bật* |
| **• `Undocumented Content-Type` (`content_type_conformance`)** | **3** | **0** | **3** | **3** |
| **• `Undocumented HTTP status code` (`status_code_conformance`)** | **10** | **26** | **67** | **60** |
| **• `Unsupported methods` (`unsupported_method`)** | *Không bật* | **0** | **1** *(`TRACE /api/documents/{id}/notes/`)* | *Không bật* |
| **Tổng CLI Unique Failures** | **22** | **51** | **131** | **95** |
| **Warnings (CLI)** | `1` *(404 lặp ở `GET /api/documents/{id}/metadata/`)* | `0` | `2` *(403 ở `DELETE`/`PATCH .../versions/{version_id}/`; 404 lặp ở `GET .../share_links/`)* | `1` *(Schema validation mismatch ở `POST /api/documents/email/`)* |

> **Cách đọc mối quan hệ giữa 3 con số thất bại:**
> 1. **`Failure (JUnit)` = thuộc tính `failures` của `<testsuite>`** (`17`, `19`, `53`): đếm số mục `<testcase>` có ít nhất một lỗi. Ở Vòng 2 và Vòng 3, Schemathesis thêm 1 mục tổng hợp `<testcase name="Stateful tests">`, nên tổng `<testcase>` là `18 + 1 = 19` và `53 + 1 = 54`. Một operation có thể đạt ở pha Fuzzing (ví dụ 3 operation ở Vòng 2) nhưng vẫn bị đánh fail trong JUnit XML vì đã vi phạm ở pha Coverage.
> 2. **Tổng số phần tử `<failure>` trong JUnit XML = số ca sinh phát hiện lỗi (`found`) trên CLI** (`17`, `44`, `108`): mỗi `<testcase>` có thể chứa nhiều thẻ `<failure>` tương ứng các Test Case ID khác nhau.
> 3. **`Unique failure (CLI)`** (`22`, `51`, `131`): đếm số cặp vi phạm check phân biệt (vì 1 Test Case ID có thể đồng thời vi phạm 2–3 check, ví dụ `TRACE /api/documents/{id}/notes/` ở case `ze8mSA` đồng thời vi phạm cả `Server error` lẫn `Unsupported methods`). Không đồng nhất con số này với số lỗi phần mềm độc lập.

---

## 2. Tách riêng lượt chạy khác phạm vi ngày 13/10/2026 (`TV3_round1_seed303.*`)

| Lượt tách riêng | Phạm vi thực tế quan sát được | Operation được chọn | Ca sinh ra (CLI) | Failure (JUnit) | Unique failure (CLI) | Thời gian (giây) | Nguồn đối chiếu |
|---|---|---:|---:|---:|---:|---:|---|
| **Lượt 13/10 (khác phạm vi Vòng 1)** | **Lệnh bị mở rộng ngoài ý muốn do phép HỢP (`OR`) giữa 2 cờ `--include-*`:** gồm toàn bộ `53` ops của 4 nhóm (`19 GET`, `19 POST`, `4 PUT`, `5 PATCH`, `6 DELETE`) **hợp với** `46` ops `GET` ngoài phạm vi (`/api/config/`, `/api/users/`, `/api/groups/`, `/api/mail_*`, `/api/profile/`, `/api/tasks/`, `/api/share_links/`, `/api/workflows/`…) | **99 / 163** *(60,74%)* | **489** *(0 skipped, 0 errored; 82 ca phát hiện lỗi)* | **82 / 99** *(`errors=0`, `skipped=0`; 82 thẻ `<failure>`)* | **95** *(1 warning)* | **26,23** *(NDJSON: `26,232` \| JUnit: `25,681`)* | [log (`52cb0fe`)](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round1_seed303.log) · [xml (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303.xml) · [ndjson (`f3233e7`)](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303.ndjson) |

- **Nguyên nhân kỹ thuật đã xác minh trực tiếp trên Schemathesis `4.30.1`:** Lượt ngày 13/10 truyền đồng thời `--include-path-regex ^/api/(tags|correspondents|document_types|documents)/` và `--include-method GET` (ghi trong sự kiện `Initialize` của `TV3_round1_seed303.ndjson`). Trong Schemathesis `4.30.1`, các cờ `--include-*` tách rời kết hợp theo phép **HỢP (`OR`)**: `53` ops thuộc 4 nhóm $\cup$ `65` ops `GET` trên toàn schema (`19` ops giao nhau) $= 53 + 65 - 19 = \mathbf{99}$ operations.
- **Lý do tách khỏi bảng 3 vòng chính:** Lượt này vừa chứa `34` thao tác ghi (`POST`/`PUT`/`PATCH`/`DELETE`, phá vỡ yêu cầu read-only của Vòng 1), vừa quét `46` endpoint `GET` ngoài 4 nhóm API trọng tâm. Ngày 16/10, TV3 đã đổi sang dùng `--include-path-regex` kết hợp `--exclude-method POST/PUT/PATCH/DELETE` ở lượt `TV3_round1_seed303_20261016_093736` để đạt chuẩn đúng **19/163 operations `GET`**.

---

## 3. Kiểm tra ghép lượt tệp nguồn & cảnh báo sai lệch trong 4 tệp `*_summary.md` cũ

### 3.1 Xác nhận ghép cặp tệp cùng một lượt

Cả 4 bộ tệp trong `results/` đều đã được đối chiếu theo 4 tiêu chí: (i) trường `Initialize.command` và khối `Reports:` trong `.log` trỏ đúng tên `.xml` và `.ndjson`; (ii) tập operations trong JUnit XML trùng khớp `100%` với tập `recorder.label` (không tính `Stateful tests`) trong NDJSON (`19==19`, `18==18`, `53==53`, `99==99`); (iii) tổng số phần tử `<failure>` trong JUnit XML trùng khớp tuyệt đối với số `found` trên CLI log (`17`, `44`, `108`, `82`); (iv) thời gian chạy trên CLI trùng khớp `EngineFinished.running_time` trong NDJSON tới phần trăm giây.

| Lượt chạy | Tệp `.xml` & `.ndjson` (commit `f3233e7`) | Tệp `.log` CLI gốc (commit `52cb0fe`) | Tệp `*_summary.md` (commit `f3233e7`) | Kết luận ghép lượt |
|---|---|---|---|---|
| **Vòng 1 chuẩn** | `TV3_round1_seed303_20261016_093736.{xml,ndjson}` | `TV3_round1_seed303_20261016_093736.log` | `TV3_round1_seed303_20261016_093736_summary.md` | **Cùng 1 lượt** (`2026-10-16 09:37:37–09:37:41`) |
| **Vòng 2 chuẩn** | `TV3_round2_seed303_20261016_093803.{xml,ndjson}` | `TV3_round2_seed303_20261016_093803.log` | `TV3_round2_seed303_20261016_093803_summary.md` | **Cùng 1 lượt** (`2026-10-16 09:38:03–09:38:47`) |
| **Vòng 3 chuẩn** | `TV3_round3_seed303_20261016_093930.{xml,ndjson}` | `TV3_round3_seed303_20261016_093930.log` | `TV3_round3_seed303_20261016_093930_summary.md` | **Cùng 1 lượt** (`2026-10-16 09:39:31–09:41:15`) |
| **Lượt 13/10 (tách riêng)** | `TV3_round1_seed303.{xml,ndjson}` | `TV3_round1_seed303.log` | `TV3_round1_seed303_summary.md` | **Cùng 1 lượt** (`2026-10-13 11:58:34–11:59:01`) |

### 3.2 Lỗi parser cần lưu ý ở 4 tệp `*_summary.md` (tại commit `f3233e7`) và trạng thái tệp `.log`

1. **Nguyên nhân sai số trong `*_summary.md`:** Trong [`scripts/run_round_TV3.py`](https://github.com/nguynn12/KTPM/blob/d3af55bf16370cb70b8e23f319f2ccf071bc5218/scripts/run_round_TV3.py#L55-L135), hàm `parse_ndjson()` đọc khóa `ev.get("type")` vốn không tồn tại trong định dạng NDJSON của Schemathesis `4.30.1` (tên sự kiện là khóa cấp 1 như `{"EngineFinished": {...}}`), nên rơi xuống fallback `parse_cli_summary()`. Hàm này dùng `re.search(r"in\s+([\d\.]+)s", log_text)` lấy **khớp đầu tiên** trong log — chính là thời gian **tải schema** (`1,17 s` / `1,06 s` / `0,91 s` / `1,03 s`) thay vì thời gian toàn lượt (`2,71 s` / `42,12 s` / `102,41 s` / `26,23 s`). Tương tự, `Passed/Failed reported (CLI)` ở Vòng 2 (`3`/`18`) trộn số `passed` của pha Fuzzing với số `failed` của pha Coverage, còn ở Vòng 3 (`2`/`51`) chỉ lấy số liệu của pha Coverage. **Không trích dẫn trực tiếp thời gian và cột Passed/Failed từ 4 tệp `*_summary.md` cũ vào báo cáo; chỉ sử dụng số liệu đã đối chiếu từ `.log`, `.ndjson`, `.xml` tại Mục 1.**
2. **Trạng thái 4 tệp `.log`:** Tại commit `f3233e7` và `1b95e10`, 4 tệp `.log` chưa được Git theo dõi do mẫu `*.log` trong `.gitignore`. Trong PR này, cả 4 tệp `.log` nguyên bản (đã quét kiểm tra xác nhận 0 lộ token, 0 lộ cookie/password — toàn bộ giá trị `Authorization` và `Cookie` đều là `[Filtered]`) được bổ sung ở commit `52cb0fe` để mọi chỉ số CLI trong bảng đều có nguồn kiểm chứng trực tiếp trên GitHub.

---

## 4. Các chỉ số và hiện tượng đánh dấu `Chưa xác minh`

Không điền giá trị suy đoán hoặc tự gán `0` cho các mục thiếu nguồn đối chứng trên nhánh TV3:

| Hạng mục | Trạng thái | Bằng chứng đã có và lý do chưa xác minh |
|---|---|---|
| **Thông điệp ngoại lệ cụ thể của `1 errored` test case ở Vòng 3** | **Chưa xác minh nguyên nhân chi tiết** | Đã xác minh nguồn phát sinh trong `TV3_round3_seed303_20261016_093930.ndjson` (dòng `876`): trong `1.734` `cases` chỉ có `1.733` `interactions`; duy nhất case `BaKhiX` (pha `stateful`, `POST /api/documents/chat/`, `media_type: application/x-www-form-urlencoded`, `is_transition_applied: false`, `request_body.value: {"$unresolvable": true}`) không có HTTP interaction/check. Tuy nhiên cả CLI log (không có khối `=== ERRORS ===`) lẫn NDJSON đều không lưu stack trace hoặc thông điệp lỗi cụ thể phía client; JUnit XML ghi `errors="0"`. |
| **Tổng số HTTP requests thô (bao gồm các request shrinking nội bộ của Hypothesis)** | **Chưa xác minh** | NDJSON chỉ ghi các `interactions` trong recorder (`74`, `744`, `1.733` ở 3 vòng chuẩn; `489` ở lượt 13/10). Nhánh TV3 không lưu access log phía container `paperless-webserver` nên không có tổng đếm mọi request phụ phát sinh trong quá trình shrinking/probing nền. |
| **Traceback máy chủ Django trên máy TV3 cho các lỗi HTTP 500** | **Chưa xác minh trên log máy TV3** | Các bằng chứng 500 trên nhánh TV3 (14 failure checks `Server error` ở Vòng 3, 5 ở Vòng 1, 1 ở Vòng 2 và 2 ca tái hiện thủ công BUG-01) chỉ ghi phản hồi HTTP 500 HTML theo hướng kiểm thử hộp đen; chưa xuất `docker compose logs webserver` từ máy TV3. Nếu báo cáo chung trích dẫn traceback nội bộ cho BUG-01/BUG-02/BUG-04/`TRACE`, cần dẫn đúng nguồn từ nhánh TV2 hoặc TV5. |
| **Tái hiện thủ công độc lập BUG-03 trên `POST /api/tags/` và `POST /api/document_types/` (máy TV3)** | **Chưa xác minh bằng ảnh tái hiện tay riêng của TV3** | Ảnh chụp thực tế `TV3_REAL_BUG03_response_201.png` và hồ sơ TV3 chỉ xác minh thủ công BUG-03 trên `POST /api/correspondents/`. Trên seed 303, Schemathesis Vòng 2/3 có báo `Response violates schema` trên cả 3 nhóm nhưng TV3 chưa tách ảnh tái hiện `curl` riêng cho `tags` và `document_types`. |
| **Nguyên nhân `403 Forbidden` trên `DELETE`/`PATCH /api/documents/{id}/versions/{version_id}/` (Warning Vòng 3)** | **Chưa xác minh** | CLI log Vòng 3 (dòng `2928–2932`) ghi cảnh báo 2 operation này chỉ trả `403 Forbidden`; chưa kiểm tra thủ công điều kiện tồn tại `version_id` hay cơ chế phân quyền versioning trên Paperless-ngx `3.1.3`. |
| **Wall-clock process time tổng (gồm khởi chạy Python/CLI) của 3 vòng** | **Chưa xác minh từ tệp nguồn** | `run_round_TV3.py` chỉ in `elapsed_total` ra màn hình console lúc chạy, không ghi vào tệp kết quả; bảng đối chiếu chỉ sử dụng thời gian có nguồn trực tiếp trong CLI summary, NDJSON `EngineFinished.running_time` và JUnit `<testsuites time>`. |

---

## 5. Ghi chú kỹ thuật chuyển cho người sửa Chương 3 (K05, Checks và Giới hạn OpenAPI)

### 5.1 Rà soát và chuẩn hóa mô tả công cụ K05 (Schemathesis `4.30.1` + Hypothesis `6.169.0`)

1. **Nguyên lý và kiến trúc thực thi thực tế của Schemathesis `4.30.1`:**
   - Schemathesis thực hiện kiểm thử API dựa trên đặc tả (*Specification-based / Contract-based API Testing*) kết hợp sinh dữ liệu dựa trên thuộc tính (*Property-based Testing* qua Hypothesis), sử dụng tài liệu **OpenAPI `3.0.3`** (`/api/schema/`, sinh tự động bởi `drf-spectacular`) làm đồng thời hai vai trò: **nguồn sinh đầu vào** và **oracle kiểm chứng phản hồi**.
   - Quy trình chạy thật quan sát được trong NDJSON gồm **3 pha chuẩn bị nội bộ** (`probing` kiểm tra năng lực máy chủ với NULL byte/backslash, `schema_analysis`, `auth_bootstrap`) và **4 pha kiểm thử chính (`--phases`)**:
     - `examples`: chạy các ví dụ tĩnh trong schema. Trên Paperless-ngx `3.1.3`, **100% bị `skipped`** (`19`/`18`/`53` skipped) vì schema `/api/schema/` không khai báo trường `example`/`examples`.
     - `coverage`: sinh có hệ thống các ca biên/kiểu sai/thiếu trường và **gửi thêm phương thức HTTP không khai báo** (`TRACE`, `QUERY`, `OPTIONS`) để kiểm tra `unsupported_method`.
     - `fuzzing`: sinh dữ liệu ngẫu nhiên có định hướng bằng Hypothesis (`--mode all` sinh cả dữ liệu hợp lệ `positive` lẫn vi phạm schema `negative`, giới hạn `--max-examples 25` mỗi operation), kèm **Shrinking** (tập hợp chiến lược heuristic rút gọn payload lỗi, **không mô tả giản lược là tìm kiếm nhị phân**).
     - `stateful`: sinh chuỗi gọi API đa bước dựa trên quan hệ producer–consumer. Do OpenAPI của Paperless-ngx không khai báo `links` tường minh (`LoadingFinished.statistic.transitions.total = 0`), toàn bộ liên kết đều do Schemathesis **tự suy luận (*inferred links*)** — Vòng 2: `63` liên kết suy luận (bao phủ `36/63`), Vòng 3: `181` liên kết suy luận (bao phủ `53/181`).
2. **Các điểm cần đính chính so với tài liệu cũ trước khi đưa vào Chương 3:**
   - **Vai trò của `--seed` (đính chính câu *"cùng seed luôn ra kết quả y hệt 100%"*):** `--seed 303` chỉ cố định bộ sinh số giả ngẫu nhiên của Hypothesis. Để tái lập kết quả còn phải giữ đồng bộ phiên bản Schemathesis/Hypothesis, nội dung OpenAPI schema, trạng thái dữ liệu nền CSDL (đặc biệt ảnh hưởng pha Stateful), và bộ cờ `--phases`/`--checks`/`--workers`. Tái hiện lỗi đáng tin cậy nhất phải dùng request tối thiểu độc lập (`curl`).
   - **Hành vi lọc CLI trong `4.30.1`:** Hai cờ `--include-path-regex` và `--include-method` khi đứng độc lập kết hợp theo phép **HỢP (`OR`)** (nguyên nhân trực tiếp tạo ra lượt `99` operations ngày 13/10). Để giao điều kiện `GET` trong 4 nhóm API phải dùng `--include-path-regex` kết hợp `--exclude-method POST/PUT/PATCH/DELETE` (hoặc `--include-by`), đồng thời tắt `coverage` và `stateful` ở Vòng 1 để đảm bảo không phát sinh probe phương thức ghi/không khai báo.
   - **So sánh với Postman/Newman:** Không viết *"Postman chỉ chạy dữ liệu tĩnh"*. Postman hỗ trợ biến động, pre-request script và chạy theo tập dữ liệu CSV/JSON. Điểm khác biệt bản chất của Schemathesis là tự động sinh dữ liệu biên/âm tính từ đặc tả OpenAPI, tự động áp dụng bộ bất biến (*invariants*) làm oracle và tự thu gọn ca lỗi (shrinking) mà không cần viết tay từng test case và assertion.
   - **Không đồng nhất đơn vị và mã thoát:** Exit code `1` chỉ cho biết lượt chạy đã hoàn tất và phát hiện ít nhất một failure/error, **không chứng minh đã bao phủ đủ phạm vi**. Tương tự, `1.734 generated cases` không bằng tổng mọi HTTP requests; `131 unique failures` không bằng `131` lỗi mã nguồn; `14 Server error` là 14 failure checks của `not_a_server_error` (trên 12 operations khai báo + `TRACE /api/documents/{id}/notes/` + 1 ca Stateful `POST /api/document_types/`).
   - **Đính chính số trường `required` của `Correspondent`:** Trong `docs/openapi_TV3.json`, `Correspondent` có đúng **7 trường `required`** (`document_count`, `id`, `last_correspondence`, `name`, `permissions`, `slug`, `user_can_change`), trong đó phản hồi `201` thực tế thiếu 3 trường (`document_count`, `last_correspondence`, `permissions`). *(Lưu ý: dòng chú thích dưới ảnh cũ `TV3_BUG03_schema_required.png` ghi nhầm là 9 trường — không chép con số 9 vào báo cáo).*
   - **Đính chính tên check trong `docs/TV3_EVIDENCE_AUDIT.md` cũ (dòng 81–82):** Hai nhãn CLI `API rejected schema-compliant request` và `API accepted schema-violating request` thuộc về hai check **`positive_data_acceptance`** và **`negative_data_rejection`**, không phải `status_code_conformance` như bảng cũ từng chú thích nhầm.

### 5.2 Danh mục đầy đủ các phép kiểm tra (Checks) đã dùng trong Schemathesis `4.30.1`

Đã đối chiếu trực tiếp từ registry `schemathesis.checks.CHECKS.get_all()`, đầu ra `schemathesis run --help` (`docs/SCHEMATHESIS_4.30.1_HELP.txt`) và toàn bộ sự kiện `checks` trong 3 tệp NDJSON seed 303:

| STT | Tên check (`--checks` / NDJSON) | Nhãn hiển thị trên CLI | Mục đích kiểm chứng (Oracle) | Vòng 1 | Vòng 2 & 3 (`--checks all`) | Unique failures (V1 / V2 / V3) |
|:---:|---|---|---|:---:|:---:|:---:|
| 1 | `not_a_server_error` | `Server error` | Phản hồi không được rơi vào mã `5xx` (lỗi máy chủ chưa xử lý) | Bật | Bật | **5 / 1 / 14** |
| 2 | `status_code_conformance` | `Undocumented HTTP status code` | Mã HTTP trả về phải được khai báo trong mục `responses` của OpenAPI | Bật | Bật | **10 / 26 / 67** |
| 3 | `content_type_conformance` | `Undocumented Content-Type` | Header `Content-Type` thực tế phải khớp định dạng công bố trong schema | Bật | Bật | **3 / 0 / 3** |
| 4 | `response_headers_conformance` | *(Response headers)* | Đầy đủ và đúng kiểu các header phản hồi bắt buộc theo schema | Bật | Bật | **0 / 0 / 0** |
| 5 | `response_schema_conformance` | `Response violates schema` | Cấu trúc JSON body trả về phải thỏa mãn JSON Schema (kiểu, `required`, `nullable`…) | Bật | Bật | **4 / 14 / 19** |
| 6 | `negative_data_rejection` | `API accepted schema-violating request` | Input cố tình vi phạm schema (`negative` mode) không được API chấp nhận `2xx` | Tắt | Bật | **— / 0 / 3** |
| 7 | `positive_data_acceptance` | `API rejected schema-compliant request` | Input tuân thủ schema (`positive` mode) không bị từ chối bất ngờ bằng `400` | Tắt | Bật | **— / 10 / 24** |
| 8 | `missing_required_header` | *(Missing required header)* | Thiếu header bắt buộc theo schema phải bị API từ chối (`4xx`) | Tắt | Bật | **— / 0 / 0** |
| 9 | `unsupported_method` | `Unsupported methods` | Phương thức HTTP không khai báo (`TRACE`, `QUERY`, `OPTIONS`…) phải trả `405` thay vì `5xx`/`2xx` | Tắt | Bật | **— / 0 / 1** |
| 10 | `allow_header_conformance` | *(Invalid `Allow` header)* | Khi trả `405`, header `Allow` phải liệt kê đúng các phương thức được hỗ trợ | Tắt | Bật | **— / 0 / 0** |
| 11 | `use_after_free` | *(Use after free)* | Tài nguyên sau khi `DELETE` thành công không được truy cập lại thành công | Tắt | Bật | **— / 0 / 0** |
| 12 | `ensure_resource_availability` | *(Resource availability)* | Tài nguyên vừa tạo (`POST`) thành công phải truy xuất được ngay sau đó | Tắt | Bật | **— / 0 / 0** |
| 13 | `ignored_auth` | *(Ignored auth)* | Endpoint yêu cầu xác thực không được chấp nhận request thiếu/sai chứng thực | Tắt | Bật | **— / 0 / 0** |
| *(phụ)* | `max_response_time` | *(Max response time)* | Kiểm tra thời gian phản hồi vượt ngưỡng `--max-response-time` | Chưa đặt ngưỡng | Chưa đặt ngưỡng *(ghi `success` mặc định trong NDJSON)* | **Không đánh giá SLA** |

### 5.3 Giới hạn của việc đánh giá dựa trên OpenAPI (cần nhấn mạnh ở Chương 3)

1. **Bài toán Oracle phụ thuộc chất lượng đặc tả (nhiều sai lệch hợp đồng không phải bug chức năng):**
   - OpenAPI của Paperless-ngx `3.1.3` sinh tự động bởi `drf-spectacular` thiếu khai báo các mã `400`/`403`/`404`, thiếu `Content-Type` nhị phân (`image/webp`, `application/pdf`, `text/plain`), thiếu `additionalProperties: false`, thiếu `nullable: true` và gắn `required` vô điều kiện cho trường phụ thuộc query (`permissions` chỉ xuất hiện khi `?full_perms=true`) hoặc trường annotate (`document_count`, `last_correspondence`).
   - Hệ quả trên seed 303 Vòng 3: riêng `Undocumented HTTP status code` (`67`) và `API rejected schema-compliant request` (`24` — phần lớn do server từ chối hợp lệ các trùng tên unique constraint hoặc `owner` không tồn tại bằng `400`) đã chiếm **`91/131` (~69,5%)** tổng số CLI unique failures. Do đó **không thể dùng thẳng số failure của Schemathesis để đo số lượng lỗi phần mềm** nếu thiếu bước lọc, phân loại và tái hiện thủ công.
2. **Không diễn tả được nghiệp vụ sâu và luồng xử lý bất đồng bộ (Async Pipeline & Side-effects):**
   - OpenAPI chỉ mô tả giao diện đồng bộ request/response, không mô tả được pipeline nền `POST /api/documents/post_document/` → Redis → Celery worker → Tesseract OCR → PostgreSQL → chỉ mục tìm kiếm. Schemathesis chỉ thấy mã HTTP `200`/`202` mà không xác minh được chất lượng nhận dạng OCR, tính đúng đắn của liên kết quan hệ sau `PATCH`, hay ngữ nghĩa truy vấn tìm kiếm toàn văn (`?query=`). Đây là lý do bắt buộc phải bổ sung **40 ca kiểm thử thiết kế tay** (`docs/TEST_CASES_TV3.md`, đã thực thi 40/40 gồm 38 PASS + 2 REPRO-BUG-01 ở commit `1b95e10`) và **3 luồng nghiệp vụ đầu-cuối** (`docs/BUSINESS_FLOWS_TV3.md`).
3. **Phụ thuộc trạng thái dữ liệu nền và liên kết suy luận (Stateful & Test Data Dependency):**
   - Vì schema không có OpenAPI `links` tường minh (`transitions.total = 0`) và không có `examples` tĩnh (toàn bộ pha `Examples` bị skip), độ sâu kiểm thử Stateful phụ thuộc hoàn toàn vào liên kết suy luận (`36/63` ở Vòng 2, `53/181` ở Vòng 3) và dữ liệu mồi hiện có. Các endpoint cần ID/trạng thái đặc thù dễ rơi vào cảnh báo `404` lặp lại (`GET .../metadata/`, `GET .../share_links/`) hoặc `403 Forbidden` (`versions/{version_id}`) khiến công cụ không chạm tới nhánh xử lý lõi.
4. **Giới hạn về phạm vi endpoint và kiểm thử phi chức năng:**
   - Phạm vi chính thức của đề tài dừng ở **4 nhóm tài nguyên (`53/163` operations = `32,52%`)**; `110` operations còn lại (`users`, `groups`, `mail_*`, `workflows`, `share_links`…) không thuộc tập kiểm thử chuẩn 3 vòng.
   - Đánh giá dựa trên OpenAPI cũng không thay thế kiểm thử giao diện Angular UI, kiểm thử tải/hiệu năng (chưa cấu hình `--max-response-time` và chạy `--workers 1`), đánh giá bảo mật chuyên sâu đa vai trò (IDOR/RBAC/CSRF/XSS), hay phân tích nguyên nhân gốc mức mã nguồn (Schemathesis chỉ báo triệu chứng hộp đen, vẫn cần kiểm tra traceback và mã nguồn để kết luận nguyên nhân).

---

## 6. Danh mục liên kết tệp nguồn tại commit cụ thể

| Nhóm tệp | Tệp nguồn | Commit cụ thể | Đường dẫn đầy đủ trên GitHub |
|---|---|---|---|
| **Vòng 1 chuẩn (19 ops)** | CLI Log | `52cb0fe` | [TV3_round1_seed303_20261016_093736.log](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round1_seed303_20261016_093736.log) |
| **Vòng 1 chuẩn (19 ops)** | JUnit XML | `f3233e7` | [TV3_round1_seed303_20261016_093736.xml](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_20261016_093736.xml) |
| **Vòng 1 chuẩn (19 ops)** | NDJSON | `f3233e7` | [TV3_round1_seed303_20261016_093736.ndjson](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_20261016_093736.ndjson) |
| **Vòng 1 chuẩn (19 ops)** | Summary *(có lỗi parser, xem Mục 3.2)* | `f3233e7` | [TV3_round1_seed303_20261016_093736_summary.md](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_20261016_093736_summary.md) |
| **Vòng 2 chuẩn (18 ops)** | CLI Log | `52cb0fe` | [TV3_round2_seed303_20261016_093803.log](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round2_seed303_20261016_093803.log) |
| **Vòng 2 chuẩn (18 ops)** | JUnit XML | `f3233e7` | [TV3_round2_seed303_20261016_093803.xml](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round2_seed303_20261016_093803.xml) |
| **Vòng 2 chuẩn (18 ops)** | NDJSON | `f3233e7` | [TV3_round2_seed303_20261016_093803.ndjson](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round2_seed303_20261016_093803.ndjson) |
| **Vòng 2 chuẩn (18 ops)** | Summary *(có lỗi parser, xem Mục 3.2)* | `f3233e7` | [TV3_round2_seed303_20261016_093803_summary.md](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round2_seed303_20261016_093803_summary.md) |
| **Vòng 3 chuẩn (53 ops)** | CLI Log | `52cb0fe` | [TV3_round3_seed303_20261016_093930.log](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round3_seed303_20261016_093930.log) |
| **Vòng 3 chuẩn (53 ops)** | JUnit XML | `f3233e7` | [TV3_round3_seed303_20261016_093930.xml](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round3_seed303_20261016_093930.xml) |
| **Vòng 3 chuẩn (53 ops)** | NDJSON | `f3233e7` | [TV3_round3_seed303_20261016_093930.ndjson](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round3_seed303_20261016_093930.ndjson) |
| **Vòng 3 chuẩn (53 ops)** | Summary *(có lỗi parser, xem Mục 3.2)* | `f3233e7` | [TV3_round3_seed303_20261016_093930_summary.md](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round3_seed303_20261016_093930_summary.md) |
| **Lượt 13/10 (99 ops, tách riêng)** | CLI Log | `52cb0fe` | [TV3_round1_seed303.log](https://github.com/nguynn12/KTPM/blob/52cb0fe136e59fffffccb88a3ae8dfcc16068040/results/TV3_round1_seed303.log) |
| **Lượt 13/10 (99 ops, tách riêng)** | JUnit XML / NDJSON / Summary | `f3233e7` | [xml](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303.xml) · [ndjson](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303.ndjson) · [summary](https://github.com/nguynn12/KTPM/blob/f3233e7fc984d52201158ab32c58291bff8aa26b/results/TV3_round1_seed303_summary.md) |
| **Schema & Runner & Tài liệu TV3** | OpenAPI / Help / Runner / Test Plan / Manual 40/40 | `dcf2c91` · `d3af55b` · `0fdca04` · `1b95e10` | [openapi_TV3.json (`dcf2c91`)](https://github.com/nguynn12/KTPM/blob/dcf2c91fe67278bab6d8535807430dcd03641502/docs/openapi_TV3.json) · [SCHEMATHESIS_4.30.1_HELP.txt (`dcf2c91`)](https://github.com/nguynn12/KTPM/blob/dcf2c91fe67278bab6d8535807430dcd03641502/docs/SCHEMATHESIS_4.30.1_HELP.txt) · [run_round_TV3.py (`d3af55b`)](https://github.com/nguynn12/KTPM/blob/d3af55bf16370cb70b8e23f319f2ccf071bc5218/scripts/run_round_TV3.py) · [TV3_EVIDENCE_AUDIT.md (`0fdca04`)](https://github.com/nguynn12/KTPM/blob/0fdca043d4f9516a60ed71535bbb5b1a2fc45de7/docs/TV3_EVIDENCE_AUDIT.md) · [TEST_CASES_TV3.md (`1b95e10`)](https://github.com/nguynn12/KTPM/blob/1b95e106729c5e36b65f2fba51d227b4ae592d53/docs/TEST_CASES_TV3.md) |
