# BẢNG TỔNG HỢP DỮ LIỆU THỰC TẾ HỆ THỐNG (FILL_IN.MD)

> **Ghi chú bảo đảm tính trung thực:** Toàn bộ thông tin dưới đây được trích xuất trực tiếp từ máy tính thực thi, cấu hình repo và các file log thực tế trong thư mục `results/`, `docs/bugs/`, `docs/TEST_CASES.md`. Không sử dụng số liệu giả định hay ước đoán.

---

## 1. Phiên bản & Môi trường thực thi

| Thành phần | Thông tin / Phiên bản trích xuất thực tế | Lệnh kiểm tra thực tế |
|---|---|---|
| **Hệ điều hành (OS)** | `Microsoft Windows [Version 10.0.26200.8037]` | `cmd.exe /c ver` |
| **Docker Engine** | `Docker version 29.7.2, build a7dcaa6` | `docker --version` |
| **Docker Compose** | `Docker Compose version v5.5.1` | `docker compose version` |
| **Python (Host)** | `Python 3.14.8` | `python --version` |
| **Schemathesis** | `schemathesis, version 4.30.1` *(chạy qua container Docker `schemathesis/schemathesis:latest`)* | `docker run --rm schemathesis/schemathesis:latest --version` |
| **Tag Paperless-ngx** | `v3.1.3` | `git describe --tags` (trong thư mục `paperless-ngx`) |
| **Commit SHA Paperless-ngx** | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` | `git rev-parse HEAD` (trong thư mục `paperless-ngx`) |
| **Tag Image Docker (docker-compose.yml)** | • `broker`: `redis:7-alpine`<br>• `db`: `postgres:16-alpine`<br>• `webserver`: `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` | Đọc trực tiếp từ file `docker-compose.yml` |
| **Tên các Container** | • `paperless-broker`<br>• `paperless-db`<br>• `paperless-webserver` | `docker compose ps` |

---

## 2. Kết quả kiểm thử Schemathesis (trích xuất từ `results/`)

### Vòng 1: Chỉ kiểm tra phương thức GET (`TV2_round1_seed202.*`)
- **Vòng kiểm thử:** Vòng 1 (GET-only baseline test)
- **Seed:** `202`
- **Lệnh đã chạy (đã lọc Token):**
  - *Lệnh ghi nhận trong ndjson:*
    ```bash
    st run http://webserver:8000/api/schema/ --include-method GET --seed 202 --max-examples 25 -H Authorization: [Filtered] --report junit,ndjson --report-junit-path /results/TV2_round1_seed202_junit.xml --report-ndjson-path /results/TV2_round1_seed202.ndjson --no-color
    ```
  - *Lệnh Docker run thực tế:*
    ```bash
    docker run --rm -v ${PWD}/results:/results --network ktpm_default schemathesis/schemathesis:latest run http://webserver:8000/api/schema/ --include-method GET --seed 202 --max-examples 25 -H "Authorization: Token [FILTERED]" --report junit,ndjson --report-junit-path /results/TV2_round1_seed202_junit.xml --report-ndjson-path /results/TV2_round1_seed202.ndjson --no-color
    ```
- **Số endpoint/operation được test:** `65/163` operations được chọn và kiểm thử (Đạt 39.8% Schema Operation Coverage).
- **Số test case sinh ra:** `2517` test cases sinh ra (`176` skipped).
- **Số test thất bại:** `97` test cases phát hiện `121` lỗi riêng biệt (unique failures).
  - *Chi tiết lỗi do công cụ in ra:* Server error: 13, Response violates schema: 10, API accepted schema-violating request: 13, API rejected schema-compliant request: 13, Invalid Allow header: 1, Undocumented Content-Type: 4, Undocumented HTTP status code: 66, Unsupported methods: 1.
- **Thời gian chạy:** `183.35s` (xấp xỉ 3 phút 3 giây).

---

### Vòng 2: Ghi dữ liệu trên metadata (`TV2_round2_seed202.*`)
- **Vòng kiểm thử:** Vòng 2 (Write operations trên `tags`, `correspondents`, `document_types`)
- **Seed:** `202`
- **Lệnh đã chạy (đã lọc Token):**
  - *Lệnh ghi nhận trong ndjson:*
    ```bash
    st run http://webserver:8000/api/schema/ --include-path-regex ^/api/(tags|correspondents|document_types)/ --seed 202 --max-examples 25 -H Authorization: [Filtered] --report junit,ndjson --report-junit-path /results/TV2_round2_seed202_junit.xml --report-ndjson-path /results/TV2_round2_seed202.ndjson --no-color
    ```
  - *Lệnh Docker run thực tế:*
    ```bash
    docker run --rm -v ${PWD}/results:/results --network ktpm_default schemathesis/schemathesis:latest run http://webserver:8000/api/schema/ --include-path-regex "^/api/(tags|correspondents|document_types)/" --seed 202 --max-examples 25 -H "Authorization: Token [FILTERED]" --report junit,ndjson --report-junit-path /results/TV2_round2_seed202_junit.xml --report-ndjson-path /results/TV2_round2_seed202.ndjson --no-color
    ```
- **Số endpoint/operation được test:** `18/163` operations được chọn và kiểm thử (Đạt 11.0% Schema Operation Coverage).
- **Số test case sinh ra:** `1481` test cases sinh ra (`72` skipped).
- **Số test thất bại:** `49` test cases phát hiện `58` lỗi riêng biệt (unique failures).
  - *Chi tiết lỗi do công cụ in ra:* Server error: 1, Response violates schema: 13, API accepted schema-violating request: 4, API rejected schema-compliant request: 12, Undocumented HTTP status code: 28.
- **Thời gian chạy:** `203.24s` (xấp xỉ 3 phút 23 giây).

---

### Vòng 3: Kiểm thử toàn diện mở rộng (`TV2_round3_seed202.*`)
- **Vòng kiểm thử:** Vòng 3 (Bao gồm `/api/documents/` và kích hoạt `--checks all`)
- **Seed:** `202`
- **Lệnh đã chạy (đã lọc Token):**
  - *Lệnh ghi nhận trong ndjson:*
    ```bash
    st run http://webserver:8000/api/schema/ --include-path-regex ^/api/(tags|correspondents|document_types|documents)/ --seed 202 --max-examples 25 --checks all -H Authorization: [Filtered] --report junit,ndjson --report-junit-path /results/TV2_round3_seed202_junit.xml --report-ndjson-path /results/TV2_round3_seed202.ndjson --no-color
    ```
  - *Lệnh Docker run thực tế:*
    ```bash
    docker run --rm -v ${PWD}/results:/results --network ktpm_default schemathesis/schemathesis:latest run http://webserver:8000/api/schema/ --include-path-regex "^/api/(tags|correspondents|document_types|documents)/" --seed 202 --max-examples 25 --checks all -H "Authorization: Token [FILTERED]" --report junit,ndjson --report-junit-path /results/TV2_round3_seed202_junit.xml --report-ndjson-path /results/TV2_round3_seed202.ndjson --no-color
    ```
- **Số endpoint/operation được test:** `53/163` operations được chọn và kiểm thử (Đạt 32.5% Schema Operation Coverage).
- **Số test case sinh ra:** `2056` test cases sinh ra (`120` skipped).
- **Số test thất bại:** `108` test cases phát hiện `136` lỗi riêng biệt (unique failures).
  - *Chi tiết lỗi do công cụ in ra:* Server error: 16, Response violates schema: 17, API accepted schema-violating request: 5, API rejected schema-compliant request: 23, Undocumented Content-Type: 5, Undocumented HTTP status code: 69, Unsupported methods: 1.
- **Thời gian chạy:** `211.21s` (xấp xỉ 3 phút 31 giây).

---

## 3. Danh sách BUG trong `docs/bugs/`

| ID | Endpoint | Loại lỗi | Mô tả 1 dòng | Tái hiện ≥ 2 lần | Bằng chứng tái hiện |
|---|---|---|---|---|---|
| **BUG-01** | `POST /api/tags/` *(và correspondents, document_types)* | Server Error (HTTP 500) | Unhandled `TypeError` khi `set_permissions[action]` nhận giá trị không phải dictionary (`bool`/`int`) làm sập máy chủ. | **ĐÃ TÁI HIỆN** (3 lần) | • Lần 1: Schemathesis Round 2 & 3<br>• Lần 2: Lệnh `curl` độc lập<br>• Lần 3: Script `run_manual_tests.py` (case `TC-TAG-11`) |
| **BUG-02** | `GET /api/documents/` | Server Error (HTTP 500) | Unhandled `ValueError` khi lọc `modified__year=-1.17e-38` (năm ≤ 0) vượt ngoài khoảng cho phép 1..9999 của hàm `datetime`. | **ĐÃ TÁI HIỆN** (2 lần) | • Lần 1: Schemathesis Round 1 & 3<br>• Lần 2: Lệnh `curl` độc lập |
| **BUG-03** | `POST /api/correspondents/` | Vi phạm Schema (Contract Inconsistency) | Phản hồi mã 201 Created khi tạo mới Correspondent thiếu trường bắt buộc `document_count` đã cam kết trong OpenAPI Schema. | **ĐÃ TÁI HIỆN** (3 lần) | • Lần 1: Schemathesis Round 2 (Test ID `vNBfDm`)<br>• Lần 2: Lệnh `curl` tạo mới Correspondent<br>• Lần 3: Kiểm tra trực tiếp trên Swagger UI |

---

## 4. Bảng Test Case thực thi thực tế (từ `docs/TEST_CASES.md`)

*Chỉ liệt kê các Test Case đã được chạy thực tế qua kịch bản tự động `scripts/run_manual_tests.py` và kiểm thử độc lập:*

| Mã TC | Phương thức | Endpoint | Kết quả mong đợi | Kết quả thực tế | Đánh giá | Ghi chú thực tế |
|---|---|---|---|---|---|---|
| **TC-TAG-01** | POST | `/api/tags/` | `201 Created` | `201 Created` | **PASS** | Tạo tag hợp lệ với trường tối thiểu `name` thành công. |
| **TC-TAG-03** | POST | `/api/tags/` | `400 Bad Request` | `400 Bad Request` | **PASS** | Thiếu trường bắt buộc `name` bị DRF validation từ chối. |
| **TC-TAG-04** | POST | `/api/tags/` | `400 Bad Request` | `400 Bad Request` | **PASS** | Truyền `name=""` (rỗng) bị từ chối hợp lệ. |
| **TC-TAG-07** | POST | `/api/tags/` | `400 Bad Request` | `400 Bad Request` *(nếu đã có tag)*<br>`201 Created` *(nếu DB chưa có tag)* | **PASS** *(khi đúng tiền điều kiện)* | Đạt khi cơ sở dữ liệu đã tồn tại sẵn tag trùng tên của cùng user (`UniqueConstraint`). |
| **TC-TAG-11** | POST | `/api/tags/` | `400 Bad Request` | `500 Server Error` | **FAIL (BUG-01)** | Phát hiện lỗi mã nguồn: payload `{"set_permissions": {"view": false}}` làm sập tiến trình backend. |
| **TC-TAG-12** | GET | `/api/tags/` | `200 OK` | `200 OK` | **PASS** | Lấy danh sách tag có phân trang thành công. |
| **TC-TAG-14** | GET | `/api/tags/{id}/` | `200 OK` | `200 OK` *(nếu tồn tại ID)*<br>`404 Not Found` *(nếu DB rỗng)* | **PASS** *(khi đúng tiền điều kiện)* | Truy vấn chi tiết theo ID tồn tại trong hệ thống. |
| **TC-TAG-19** | GET | `/api/tags/` | `401 Unauthorized` | `401 Unauthorized` | **PASS** | Gửi request không có token xác thực bị từ chối đúng chuẩn bảo mật. |

> **Các Test Case còn lại trong kế hoạch (`TC-TAG-02`, `05`, `06`, `08`, `09`, `10`, `13`, `15`, `16`, `17`, `18`):**
> Trạng thái hiện tại: **CHƯA CÓ KẾT QUẢ CHẠY**.
> **Lý do:** Đây là các ca kiểm thử thuộc kế hoạch mở rộng (vượt biên độ dài 129 ký tự, cập nhật PUT/PATCH, xóa DELETE, thuật toán phân loại nâng cao) đã được thiết kế sẵn cấu trúc trong `docs/TEST_CASES.md` nhưng chưa đưa vào kịch bản chạy tự động của mốc giữa kỳ.

---

## 5. Ánh xạ Endpoint → Mã nguồn (Đọc trực tiếp từ file repo `paperless-ngx`)

*Căn cứ trực tiếp từ mã nguồn Paperless-ngx tag `v3.1.3` (Commit `d48663e`):*

| Nhóm Endpoint | ViewSet / View | Serializer | Model | File và Số dòng cụ thể |
|---|---|---|---|---|
| `/api/tags/` | `TagViewSet` | `TagSerializer` | `Tag` | • View: `src/documents/views.py:599-677`<br>• Serializer: `src/documents/serialisers.py:617-746`<br>• Model: `src/documents/models.py:102-140` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/correspondents/` | `CorrespondentViewSet` | `CorrespondentSerializer` | `Correspondent` | • View: `src/documents/views.py:553-596`<br>• Serializer: `src/documents/serialisers.py:541-560`<br>• Model: `src/documents/models.py:96-101` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/document_types/` | `DocumentTypeViewSet` | `DocumentTypeSerializer` | `DocumentType` | • View: `src/documents/views.py:680-698`<br>• Serializer: `src/documents/serialisers.py:562-601`<br>• Model: `src/documents/models.py:141-156` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/documents/` | `UnifiedSearchViewSet` *(kế thừa `DocumentViewSet`)* | `DocumentSerializer` *(và `SearchResultSerializer`)* | `Document` | • View: `src/documents/views.py:2402-2460`<br>*(Lớp cha `DocumentViewSet`: dòng 980-2401)*<br>• Serializer: `src/documents/serialisers.py:1047-1334`<br>*(Lớp tìm kiếm `SearchResultSerializer`: dòng 1336-1377)*<br>• Model: `src/documents/models.py:157-550` |

---

## 6. Thống kê Git Log & Đóng góp thành viên

- **Thống kê số lượng commit (`git shortlog -sn --all`):**
  - `Tạ Nhật Nguyên (TV2)`: **17 commits**
  - *Các thành viên khác (TV1, TV3, TV4, TV5):* **CHƯA CÓ**
    - **Lý do:** Kho lưu trữ cục bộ trên máy tính này là workspace phát triển độc lập của TV2 trên nhánh `TV2_TaNhatNguyen`. Nhóm chưa thực hiện gộp (merge) commit từ nhánh của các thành viên khác vào nhánh này.
- **Mốc thời gian commit trong Git Log:**
  - **Commit đầu tiên:** `2026-10-12 10:38:53 +0700` (SHA: `7cf838e` — *init: khoi tao workspace TV2 va them docs/TODO_TV2.md*)
  - **Commit gần nhất:** `2026-10-17 22:49:55 +0700` (SHA: `8a7df47` — *docs: go bo file DEFENSE_CHEAT_SHEET*)

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
   - [ ] Ảnh chụp kết quả chạy Schemathesis trên Terminal / PowerShell.
   - [ ] Ảnh chụp tái hiện BUG-01, BUG-02, BUG-03 trên giao diện UI hoặc Postman/Swagger.

3. **Video minh chứng (Screen Recording):**
   - [ ] Quay video màn hình (độ dài 1-3 phút) thao tác kiểm thử 3 luồng nghiệp vụ trên hệ thống cục bộ:
     1. Luồng 1: Tải lên tài liệu mẫu (Upload document).
     2. Luồng 2: Gắn nhãn (Tag), người gửi (Correspondent), loại tài liệu (Document Type).
     3. Luồng 3: Tìm kiếm tài liệu bằng từ khóa và bộ lọc.
