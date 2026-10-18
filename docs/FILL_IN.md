# BẢNG TỔNG HỢP DỮ LIỆU THỰC TẾ HỆ THỐNG (FILL_IN.MD)

> **Ghi chú bảo đảm tính trung thực:** Toàn bộ thông tin dưới đây được trích xuất trực tiếp từ máy tính thực thi, cấu hình repo và các file log thực tế trong thư mục `results/`, `docs/`, `scripts/` của **TV1 (Trần Gia Huy)**. Không sử dụng số liệu giả định hay ước đoán. Những mục chưa thực hiện được ghi rõ "Chưa chạy" / "Chưa có dữ liệu".

---

## 1. Phiên bản & Môi trường thực thi (TV1)

| Thành phần | Thông tin / Phiên bản trích xuất thực tế | Lệnh kiểm tra thực tế |
|---|---|---|
| **Hệ điều hành (OS)** | Windows 11 (Docker Desktop dùng backend **WSL2**, nhưng máy chỉ có distro `docker-desktop`; lần chạy thật thực hiện trên **PowerShell** của Windows, không dùng WSL) | `winver`; `wsl -l -v` |
| **CPU / RAM** | Intel Core i5-12450H / 15.7 GB | `(Get-CimInstance Win32_Processor).Name`; `Get-CimInstance Win32_ComputerSystem` |
| **Docker Engine** | `Docker version 29.8.0, build 88096ef` | `docker --version` |
| **Docker Compose** | `Docker Compose version v5.5.1` | `docker compose version` |
| **Python (Host)** | `Python 3.15.0` (bản mặc định trên PATH) và `Python 3.13.15` (cài thêm qua winget) | `python --version`; `py --list` |
| **Môi trường ảo chạy kiểm thử** | `D:\KTPM\.venv` — Python **3.13.15** (đã bị `.gitignore` chặn, không commit). Lý do dùng 3.13: Python 3.15 trên máy không có wheel sẵn của `pyyaml` nên `pip` phải tự build và cần MSVC | `D:\KTPM\.venv\Scripts\python.exe --version` |
| **Schemathesis** | `schemathesis, version 4.30.1` (kèm `Hypothesis 6.170.1`), cài trong `.venv` Python 3.13.15 | `D:\KTPM\.venv\Scripts\schemathesis.exe --version` |
| **Tag Paperless-ngx (pin)** | `v3.1.3` | `docs/PINNED_VERSION_TV1.md` |
| **Commit SHA Paperless-ngx (pin)** | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` | `docs/PINNED_VERSION_TV1.md` |
| **Tag Image Docker (`docker-compose.pinned.yml`)** | • `broker`: `docker.io/library/redis:7-alpine`<br>• `db`: `docker.io/library/postgres:16-alpine`<br>• `webserver`: `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` | Đọc trực tiếp từ file `docker/docker-compose.pinned.yml` |
| **Tên các Container** | `paperless-webserver`, `paperless-db`, `paperless-broker` (project `ktpm-group`) | `docker compose ps` |
| **Port** | `8000` → http://localhost:8000 | `docker-compose.pinned.yml` |

> Cả 3 image đều ghim theo tag cụ thể, **không dùng `latest`**. Các image đang chạy thật đã được đối chiếu khớp với file `docker/docker-compose.pinned.yml` (commit `5b46419`).

---

## 2. Kết quả kiểm thử Schemathesis (TV1)

> **Trạng thái: ĐÃ CHẠY THẬT 3 vòng (ngày 18/10/2026), seed 101.** Báo cáo đầy đủ kèm phân tích: `results/TV1_ketqua_seed101.md`.

| Mục | Giá trị |
|---|---|
| **Vòng kiểm thử** | 3 vòng (1: chỉ đọc GET; 2: mọi method trên 3 nhóm metadata; 3: mọi method trên cả 4 nhóm tài nguyên) |
| **Seed của TV1** | `101` (theo quy ước nhóm: TV1=101, TV2=202, TV3=303, TV4=404, TV5=505) — giữ nguyên ở cả 3 vòng |
| **Cấu hình sinh** | `--seed 101 --max-examples 25 --workers 1 --mode all` |
| **Số endpoint/operation được test** | Vòng 1: **19**, Vòng 2: **18**, Vòng 3: **53** (đều khớp số đếm độc lập từ `/api/schema/`; schema có tổng 163 operation) |
| **Số test case sinh ra** | Vòng 1: **99**, Vòng 2: **1863**, Vòng 3: **2016** |
| **Số test case phát hiện lỗi (CLI)** | Vòng 1: **16**, Vòng 2: **52**, Vòng 3: **108** |
| **Số lỗi khác nhau (unique failures, CLI)** | Vòng 1: **20**, Vòng 2: **58**, Vòng 3: **136** |
| **JUnit (tests / failures / errors / skipped)** | Vòng 1: `19/16/0/0` · Vòng 2: `19/19/0/0` · Vòng 3: `54/53/0/0` |
| **Thời gian chạy** | Vòng 1: **9.41 s**, Vòng 2: **194.09 s**, Vòng 3: **189.73 s** |
| **Exit code CLI** | `1` ở cả 3 vòng (có vi phạm được phát hiện) |
| **File mẫu** | **Không còn dùng** — file mẫu `results/TV1_seed101_mau.md` đã được thay bằng file kết quả thật (đã xóa khỏi repo) |
| **File kết quả thật** | `results/TV1_ketqua_seed101.md` (báo cáo tổng hợp) + `results/TV1_round{1,2,3}_seed101.{xml,ndjson}` + `results/TV1_round{1,2,3}_seed101_summary.md` |
| **File triển khai thật** | `results/TV1_deploy_13-10.md` (biên bản dựng hệ thống + 3 luồng nghiệp vụ) |

**Lệnh đã chạy** (token đã bị Schemathesis tự lọc thành `[Filtered]`). Vòng 3 là lệnh đầy đủ nhất:

```bash
schemathesis run http://localhost:8000/api/schema/ --url http://localhost:8000 \
  --include-path-regex ^/api/(tags|correspondents|document_types|documents)/ \
  --seed 101 --max-examples 25 --workers 1 --mode all \
  --header Authorization: [Filtered] --checks all \
  --report junit,ndjson \
  --report-junit-path D:\KTPM\results\TV1_round3_seed101.xml \
  --report-ndjson-path D:\KTPM\results\TV1_round3_seed101.ndjson \
  --output-sanitize true --no-color
```

Hai vòng còn lại chỉ khác phần lọc phạm vi: Vòng 1 thêm 4 cờ `--exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE` và `--phases examples,fuzzing`; Vòng 2 dùng regex `^/api/(tags|correspondents|document_types)/`. Lệnh nguyên văn của từng vòng nằm trong mục "Lệnh đã chạy" của `results/TV1_round{1,2,3}_seed101_summary.md`.

> Lưu ý đọc số: `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho mỗi operation, **không phải** số request; `--include-path-regex` và các cờ `--include-method/--exclude-method` của Schemathesis 4.30.1 có hành vi **ghép OR** khi truyền nhiều cờ `--include-*`, nên phạm vi được chốt bằng 1 regex + lặp cờ `--exclude-method` (xem `docs/ONBOARDING_TV1.md` §10).

---

## 3. Danh sách BUG (TV1)

| ID | Endpoint | Loại lỗi | Mô tả 1 dòng | Tái hiện ≥ 2 lần | Bằng chứng tái hiện |
|---|---|---|---|---|---|
| **BUG-04** | `GET\|DELETE\|POST /api/documents/{id}/<view con>/` | Lỗi chức năng (thiếu kiểm tra đầu vào) | `{id}` không phải số → `ValueError` → **HTTP 500** thay vì `400/404` | Có — 100% bằng `curl` | `docs/bugs/BUG-04.md`; JUnit vòng 1 `lvjTJ0/g910DV/ZKaq22`, vòng 3 `qg4aZX/83XLMq/XW6OmH/Whb1ZK/tc6cCS` |
| **BUG-05** | `GET /api/tags/{id}/`, `POST /api/tags/`, `GET /api/documents/{id}/download/`, `thumb/`, … | Lỗi **tài liệu/đặc tả** (schema thiếu) | Schema không ghi các mã trạng thái / Content-Type mà API thực tế trả | Có — `curl` + JUnit | `docs/bugs/BUG-05.md`; JUnit `yTZzye`, `fkWPHj`, `ADm3zu`, `94SGhk`, `Gj3vp6`, `CNPN21`, `sGzLlM`, `A9mtyD` |
| **BUG-06** | `GET /api/correspondents/`, `/api/correspondents/{id}/`, `GET /api/document_types/`, `/api/document_types/{id}/` | Response vi phạm schema | Response thiếu trường `required`: `last_correspondence` / `permissions` | Có — `curl` + JUnit | `docs/bugs/BUG-06.md`; JUnit vòng 1 `HRip4b`, `Ymv9RX` |

**Phân loại lỗi theo check** (đọc từ bảng tổng kết CLI của 3 vòng):

| Check bị vi phạm | Vòng 1 | Vòng 2 | Vòng 3 | Tổng |
|---|---|---|---|---|
| Server error | 4 | 0 | 17 | **21** |
| Response violates schema | 4 | 14 | 20 | **38** |
| Undocumented HTTP status code | 9 | 27 | 72 | **108** |
| Undocumented Content-Type | 3 | 0 | 3 | **6** |
| API accepted schema-violating request | 0 | 5 | 0 | **5** |
| API rejected schema-compliant request | 0 | 12 | 23 | **35** |
| Unsupported methods | 0 | 0 | 1 | **1** |
| **Tổng lỗi khác nhau** | **20** | **58** | **136** | **214** |

> **BUG-01, BUG-02, BUG-03** là dữ liệu của **TV2** (seed 202) và **không thuộc** phân công TV1: 500 `TypeError` ở `set_permissions`, 500 `ValueError` khi lọc theo `year`, và 201 thiếu trường `document_count`. TV1 đánh số tiếp từ **BUG-04** để không ghi đè file của TV2.
>
> Lưu ý: **"lỗi khác nhau" không phải số bug** — nhiều mục có cùng một nguyên nhân gốc (ví dụ toàn bộ 108 mục "Undocumented HTTP status code" đều nằm trong BUG-05; các mục 500 đều nằm trong BUG-04).

---

## 4. Bảng Test Case thực thi thực tế (TV1)

> Bảng dưới đây là các ca kiểm thử **TV1 đã thực thi thật** (đo lại ngày 18/10/2026 trên `http://localhost:8000` bằng HTTP + `curl`). TV1 chưa có file `docs/TEST_CASES.md` riêng (theo kế hoạch là trách nhiệm của TV3); mã `TC-TV1-xx` do TV1 tự đặt để đối chiếu, không thay thế mã của TV3.

| Mã TC | Phương thức | Endpoint | Kết quả mong đợi | Kết quả thực tế | Đánh giá | Ghi chú thực tế |
|---|---|---|---|---|---|---|
| TC-TV1-01 | POST | `/api/documents/post_document/` | Tải lên PDF → tạo task OCR, sinh nội dung text | **200** + `task_id`; OCR chạy xong, `content` đọc được | **ĐẠT** | Luồng 1 — tài liệu OCR (`docs/BUSINESS_FLOWS_TV1.md`, `results/TV1_deploy_13-10.md`) |
| TC-TV1-02 | PATCH | `/api/documents/{id}/` | Gắn được tag / correspondent / document_type | **200**; bản ghi hiển thị đủ tag + corr + doctype | **ĐẠT** | Luồng 2 |
| TC-TV1-03 | GET | `/api/documents/?query=dien` | Tìm theo từ khóa trả đúng tài liệu | **200**, `count = 1` | **ĐẠT** | Luồng 3 (từ khóa) |
| TC-TV1-04 | GET | `/api/documents/?tags__id__in=108` | Lọc theo tag `hoa-don` trả đúng tài liệu | **200**, `count = 1` | **ĐẠT** | Luồng 3 (bộ lọc theo tag) |
| TC-TV1-05 | GET | `/api/schema/` | Trả đặc tả OpenAPI hợp lệ | **200**, `application/vnd.oai.openapi`, 340 696 byte, `openapi 3.0.3`, 93 path / **163 operation** | **ĐẠT** | Đầu vào cho Schemathesis |
| TC-TV1-06 | GET | `/api/documents/true/metadata/` | `{id}` không phải số → 400/404 | **500** (`ValueError: Field 'id' expected a number`) | **PHÁT HIỆN LỖI** | BUG-04 — tái hiện bằng `curl`, xem log máy chủ |
| TC-TV1-07 | GET | `/api/documents/999999/metadata/` | id số không tồn tại → 404 | **404** — đúng | **ĐẠT** | Đối chứng: lỗi 500 ở TC-06 chỉ do `{id}` sai kiểu, không phải thiếu bản ghi |
| TC-TV1-08 | GET | `/api/tags/999999/` | Trả đúng mã thực tế **và** schema phải ghi mã đó | **404** nhưng schema **không ghi** `404` | **PHÁT HIỆN LỖI** | BUG-05 (lỗi tài liệu/đặc tả) |
| TC-TV1-09 | GET | `/api/correspondents/` | Response chứa đủ trường `required` | Thiếu `last_correspondence` (và `permissions` ở bản `{id}/`) | **PHÁT HIỆN LỖI** | BUG-06 |
| TC-TV1-10 | GET | `/api/document_types/` | Response chứa đủ trường `required` | Thiếu `permissions` | **PHÁT HIỆN LỖI** | BUG-06 (cùng nguyên nhân) |

**Trạng thái dữ liệu nền lúc kiểm tra:** 2 tài liệu, 3 tag (`can-xu-ly`, `hoa-don`, `luu-tru-lau-dai`), 2 correspondent, 2 document type — khớp bộ seed của TV1 (`docs/SEED_DATA_TV1.md`).

---

## 5. Ánh xạ Endpoint → Mã nguồn (tham khảo từ Paperless-ngx v3.1.3)

*Căn cứ từ mã nguồn Paperless-ngx tag `v3.1.3` (commit `d48663e`), dùng làm tài liệu tham khảo cho TV1 khi đọc mã nguồn sau khi chạy thử:*

| Nhóm Endpoint | ViewSet / View | Serializer | Model | File và Số dòng cụ thể |
|---|---|---|---|---|
| `/api/tags/` | `TagViewSet` | `TagSerializer` | `Tag` | • View: `src/documents/views.py:599-677`<br>• Serializer: `src/documents/serialisers.py:617-746`<br>• Model: `src/documents/models.py:102-140` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/correspondents/` | `CorrespondentViewSet` | `CorrespondentSerializer` | `Correspondent` | • View: `src/documents/views.py:553-596`<br>• Serializer: `src/documents/serialisers.py:541-560`<br>• Model: `src/documents/models.py:96-101` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/document_types/` | `DocumentTypeViewSet` | `DocumentTypeSerializer` | `DocumentType` | • View: `src/documents/views.py:680-698`<br>• Serializer: `src/documents/serialisers.py:562-601`<br>• Model: `src/documents/models.py:141-156` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/documents/` | `UnifiedSearchViewSet` *(kế thừa `DocumentViewSet`)* | `DocumentSerializer` *(và `SearchResultSerializer`)* | `Document` | • View: `src/documents/views.py:2402-2460`<br>*(Lớp cha `DocumentViewSet`: dòng 980-2401)*<br>• Serializer: `src/documents/serialisers.py:1047-1334`<br>*(Lớp tìm kiếm `SearchResultSerializer`: dòng 1336-1377)*<br>• Model: `src/documents/models.py:157-550` |

---

## 6. Thống kê Git Log & Đóng góp TV1

- **Nhánh:** `TV1_TranGiaHuy` — nhánh riêng của TV1, **đã hợp nhất `master` (của TV2)** vào ngày 18/10/2026 (commit hợp nhất `7583021`).
- **Remote:** `https://github.com/nguynn12/KTPM.git`
- **Số commit trên nhánh:** **29** (bao gồm 16 commit kế thừa từ `master` của TV2 sau khi hợp nhất). Trong đó **12 commit do TV1 viết** + **1 commit hợp nhất** = **13 commit thuộc TV1**.
- **Commit đầu tiên của TV1:** `a19c309` (2026-10-18) — `chore(repo): khoi tao repo TV1 + .gitignore + README + requirements`
- **Commit gần nhất của TV1:** `92c45d4` (2026-10-18) — `feat(ketqua): chay that 3 vong Schemathesis seed 101 + bao cao BUG-04..06`
- **Trạng thái đẩy lên remote:** `origin/TV1_TranGiaHuy` đang ở `7583021`; nhánh local **ahead 3 commit** (`7b1574a`, `5b46419`, `92c45d4`) — **chưa push**, chờ nhóm xác nhận.
- **Danh sách 13 commit của TV1 (cũ → mới):**

| # | Commit | Ngày | Nội dung |
|---|---|---|---|
| 1 | `a19c309` | 2026-10-18 | chore(repo): khoi tao repo TV1 + .gitignore + README + requirements |
| 2 | `32e9c32` | 2026-10-18 | docs(pin): pin Paperless-ngx v3.1.3 + commit SHA + Schemathesis 4.30.1 |
| 3 | `2b0e7bb` | 2026-10-18 | feat(docker): compose pin 3.1.3 + file env mau |
| 4 | `4aedd5c` | 2026-10-18 | feat(seed): 6 PDF mau + seed_api.py + generator + README |
| 5 | `4aac7c3` | 2026-10-18 | docs(onboarding): huong dan cai Paperless-ngx tu may sach (Phan C) |
| 6 | `54879be` | 2026-10-18 | docs(flows): 3 luong nghiep vu chay duoc (Phan C) |
| 7 | `cfa36c5` | 2026-10-18 | test(results): bien ban duct thuc TV1 13/10 + mau seed 101 |
| 8 | `20fbca1` | 2026-10-18 | scripts(check): script kiem tra moi truong truoc khi cai |
| 9 | `3400a69` | 2026-10-18 | docs(fill_in): bo sung bang tong hop du lieu thuc te TV1 |
| 10 | `7583021` | 2026-10-18 | merge: hop nhat master (TV2) vao TV1_TranGiaHuy |
| 11 | `7b1574a` | 2026-10-18 | refactor(structure): sap xep lai thu muc nhanh TV1 theo quy uoc chung cua nhom |
| 12 | `5b46419` | 2026-10-18 | fix(compose): dong bo docker-compose.pinned.yml voi docker-compose.yml that cua nhom |
| 13 | `92c45d4` | 2026-10-18 | feat(ketqua): chay that 3 vong Schemathesis seed 101 + bao cao BUG-04..06 |

- **Các thành viên khác:** lịch sử của TV2 đã được hợp nhất vào nhánh qua `master`; TV3, TV4, TV5 **chưa có commit** trên nhánh `TV1_TranGiaHuy` (mỗi thành viên commit trên nhánh/ tài khoản riêng để peer-review cuối kỳ).

---

## 7. Các mục người dùng bắt buộc PHẢI TỰ LÀM

Agent không thể và không được phép tạo tự động các nội dung mang tính chất định danh cá nhân và minh chứng hình ảnh thực tế sau đây:

1. **Thông tin định danh hành chính của nhóm:**
   - [ ] Tên nhóm chính thức theo danh sách lớp học phần.
   - [ ] Họ tên và Mã số sinh viên (MSSV) của toàn bộ 5 thành viên (TV1, TV2, TV3, TV4, TV5).
   - [ ] Đường dẫn (Link) bảng quản lý tiến độ công việc trên **Trello** (hoặc Jira/Notion).

2. **Ảnh chụp màn hình thực tế (Screenshots) có gắn dấu hiệu nhận diện (để vào báo cáo Word/Slide):**
   - [ ] Ảnh chụp màn hình đăng nhập thành công vào Paperless-ngx UI (`http://localhost:8000`).
   - [ ] Ảnh chụp danh sách tài liệu (`/documents`) với dữ liệu đã seed.
   - [ ] Ảnh chụp giao diện Swagger UI tài liệu đặc tả API (`http://localhost:8000/api/schema/swagger-ui/`).
   - [ ] Ảnh chụp kết quả chạy Schemathesis trên Terminal / PowerShell (sau khi chạy vòng 1–3).
   - [ ] Ảnh chụp tái hiện BUG trên giao diện UI hoặc Postman/Swagger (sau khi tìm thấy lỗi).

   > Gợi ý tên file bằng chứng của TV1 (lưu vào `docs/evidence/`): `TV1_docker-ps.png`, `TV1_login.png`, `TV1_ocr.png`, `TV1_tag.png`, `TV1_swagger.png`, `TV1_search.png` (xem checklist trong `results/TV1_deploy_13-10.md`).

3. **Video minh chứng (Screen Recording):**
   - [ ] Quay video màn hình (độ dài 1-3 phút) thao tác kiểm thử 3 luồng nghiệp vụ trên hệ thống cục bộ:
     1. Luồng 1: Tải lên tài liệu mẫu (Upload document).
     2. Luồng 2: Gắn nhãn (Tag), người gửi (Correspondent), loại tài liệu (Document Type).
     3. Luồng 3: Tìm kiếm tài liệu bằng từ khóa và bộ lọc.

4. **Chạy thực tế Schemathesis (seed 101):** — ✅ **TV1 đã hoàn thành ngày 18/10/2026**
   - [x] Cài `pip install "schemathesis==4.30.1"` (trong `.venv` Python 3.13.15).
   - [x] Chạy Vòng 1, Vòng 2, Vòng 3 theo `docs/ONBOARDING_TV1.md` — cả 3 vòng chạy xong thật, exit code `1`.
   - [x] Điền số liệu thật vào báo cáo kết quả: `results/TV1_ketqua_seed101.md` (file mẫu `results/TV1_seed101_mau.md` đã được thay thế và xóa khỏi repo).
   - [x] Ghi file lỗi cho mỗi lỗi phát hiện: `docs/bugs/BUG-04.md`, `BUG-05.md`, `BUG-06.md`.
   - [ ] Chụp ảnh màn hình Terminal/PowerShell thể hiện kết quả chạy thật (bằng chứng cá nhân — xem mục 2).
