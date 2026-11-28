# HỒ SƠ MINH CHỨNG VẬN HÀNH BA LUỒNG NGHIỆP VỤ VÀ ĐỐI CHIẾU KIẾN TRÚC COMPOSE — TV4

**Thành viên thực hiện:** TV4 — Nguyễn Nhất Minh (MSSV: `2312690`)  
**Nhánh làm việc:** `TV4_NguyenNhatMinh`  
**Phiên bản hệ thống xác minh:** Paperless-ngx `v3.1.3` (`ghcr.io/paperless-ngx/paperless-ngx:3.1.3`, commit `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`)  
**Môi trường thực nghiệm:** Windows 11 + WSL2, Docker Engine `29.8.0`, Docker Compose `v5.5.1`, PostgreSQL `16-alpine`, Redis `7-alpine`  
**Mục đích bàn giao:** Cung cấp danh mục minh chứng vận hành thực tế cho **Chương 4** báo cáo cuối kỳ (gồm trạng thái dịch vụ, xác thực API, ba luồng nghiệp vụ trọng tâm với tách biệt thời điểm tiếp nhận/xử lý hoàn tất và kiểm chứng lưu quan hệ), đối chiếu sơ đồ container & luồng dữ liệu với [`docker-compose.yml`](../docker-compose.yml), bàn giao hình ảnh 300 DPI kèm chú thích chèn Word và hướng dẫn chạy demo.

---

## 1. Danh mục tổng hợp minh chứng bàn giao (Evidence Catalog)

Toàn bộ tệp log và ảnh chụp giao diện dưới đây được thu thập từ cùng một lượt chạy thực nghiệm sạch vào lúc `2026-11-28 11:36:24 UTC+7` bằng script [`scripts/demo_system.py`](../scripts/demo_system.py) và trình duyệt cục bộ tại `http://localhost:8000`. Mọi token, mật khẩu và định danh tài khoản trên giao diện đã được rà soát và che (`<REDACTED_TOKEN>`, `<REDACTED_PASSWORD>`, `[REDACTED]`).

| Mã MC | Hạng mục cần chứng minh (theo Chương 4 báo cáo) | Tệp log minh chứng (đã che nhạy cảm) | Tệp ảnh giao diện / Sơ đồ đối ứng | Kết quả đánh giá |
|:---:|---|---|---|:---:|
| **MC-01** | **Các dịch vụ Docker Compose đã khởi chạy** & đúng phiên bản cố định (`v3.1.3`, commit `d48663e9`) | [`docs/evidence/logs/01_environment_and_compose_status.txt`](evidence/logs/01_environment_and_compose_status.txt) | [`docs/images/so_do_kien_truc_container.png`](images/so_do_kien_truc_container.png) | **ĐẠT** (`3/3 Up`, `webserver healthy`) |
| **MC-02** | **Giao diện Web và API xác thực hoạt động**, OpenAPI Schema truy cập được (`163` operations) | [`docs/evidence/logs/02_auth_and_openapi_check.txt`](evidence/logs/02_auth_and_openapi_check.txt) | [`01_webui_login_screen.png`](evidence/images/01_webui_login_screen.png) · [`02_openapi_schema_view.png`](evidence/images/02_openapi_schema_view.png) | **ĐẠT** (`401` khi thiếu token; `200` khi có token) |
| **MC-03** | **Luồng 1 — Tải lên và xử lý tài liệu:** Tách rõ thời điểm tiếp nhận (`Task UUID`), trạng thái xử lý hoàn tất (`success`) và truy xuất tài liệu sau xử lý | [`docs/evidence/logs/03_flow1_upload_and_processing.txt`](evidence/logs/03_flow1_upload_and_processing.txt) | [`03_flow1_tasks_completed.png`](evidence/images/03_flow1_tasks_completed.png) | **ĐẠT** (`HTTP 200` $\rightarrow$ `success` sau `2,24s` $\rightarrow$ `doc_id=8`) |
| **MC-04** | **Luồng 2 — Gán thông tin phân loại:** Tạo `Tag`, `Correspondent`, `DocumentType`; cập nhật tài liệu và truy vấn lại độc lập xác nhận quan hệ đã lưu | [`docs/evidence/logs/04_flow2_classification_assignment.txt`](evidence/logs/04_flow2_classification_assignment.txt) | [`04_flow2_document_metadata_assigned.png`](evidence/images/04_flow2_document_metadata_assigned.png) | **ĐẠT** (`201 Created` $\rightarrow$ `PATCH 200` $\rightarrow$ `GET 200` khớp) |
| **MC-05** | **Luồng 3 — Tìm kiếm và lọc tài liệu:** Tìm toàn văn (Tantivy) và lọc đa tiêu chí trên tập dữ liệu đối chứng có quan hệ biết trước | [`docs/evidence/logs/05_flow3_search_and_filtering.txt`](evidence/logs/05_flow3_search_and_filtering.txt) | [`05_flow3_search_and_filter_result.png`](evidence/images/05_flow3_search_and_filter_result.png) | **ĐẠT** (thu nhận đúng `ID=8`, loại trừ đối chứng `ID=9`) |
| **MC-06** | **Bản tổng hợp JSON tự động & Sơ đồ luồng dữ liệu + File Word chèn báo cáo** | [`docs/evidence/logs/TV4_demo_execution_summary.json`](evidence/logs/TV4_demo_execution_summary.json) | [`so_do_luong_du_lieu.png`](images/so_do_luong_du_lieu.png) · [`TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx`](TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx) | **ĐẠT** (`3/3` luồng `PASS`) |

---

## 2. Hồ sơ thực nghiệm chi tiết ba luồng vận hành trên Paperless-ngx cục bộ

### 2.0. Xác nhận điều kiện nền (Dịch vụ, Giao diện và Xác thực API)

* **Điều kiện ban đầu:** Tệp `.env` cục bộ đã cấu hình từ `.env.example` (bị chặn bởi `.gitignore`); lệnh `docker compose up -d` đã khởi chạy 3 dịch vụ trong [`docker-compose.yml`](../docker-compose.yml); dữ liệu cũ được dọn sạch có phân trang và làm rỗng thùng rác qua [`scripts/reset_data.py`](../scripts/reset_data.py).
* **Thao tác kiểm tra:**
  1. Chạy `docker compose ps`, `docker image inspect` và `docker compose exec -T webserver s6-rc -a list`.
  2. Gửi `GET /api/documents/` không kèm header xác thực để kiểm tra cơ chế chặn truy cập trái phép.
  3. Gửi `POST /api/token/` lấy token xác thực, sau đó gọi `GET /api/schema/` và mở giao diện `http://localhost:8000` cùng `http://localhost:8000/api/schema/view/`.
* **Kết quả mong đợi:** Cả 3 container hoạt động ổn định (`webserver` đạt `healthy`, commit image khớp `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e`); yêu cầu không token bị từ chối với `HTTP 401`; yêu cầu có token trả `HTTP 200` và đặc tả OpenAPI `3.0.3` gồm `163` operations.
* **Kết quả quan sát thực tế:** Khớp hoàn toàn kỳ vọng — `GET /api/documents/` không token trả `HTTP 401 {"detail":"Authentication credentials were not provided."}`; `POST /api/token/` trả `HTTP 200`; `GET /api/schema/` trả `Paperless-ngx REST API v6.0.0 (10)` với đúng `163` operations (xem [`01_environment_and_compose_status.txt`](evidence/logs/01_environment_and_compose_status.txt) và [`02_auth_and_openapi_check.txt`](evidence/logs/02_auth_and_openapi_check.txt)).

---

### 2.1. Luồng 1 — Tải lên và xử lý tài liệu bất đồng bộ (Upload, Processing Completion & Retrieval)

> **Nguyên tắc kiểm chứng (theo mục 2.4 & 4.1 báo cáo):** Phản hồi tiếp nhận tải lên mới chỉ xác nhận tệp đã được đưa vào hàng đợi nền. Minh chứng phải ghi nhận tách bạch **thời điểm tiếp nhận (`Task UUID`)**, **trạng thái xử lý nền hoàn tất (`status = success`)**, và **khả năng truy xuất tài liệu sau xử lý (`GET /api/documents/{id}/` & `/download/`)**.

| Hạng mục | Nội dung ghi nhận thực tế |
|---|---|
| **Điều kiện ban đầu** | • 3 dịch vụ `paperless-webserver`, `paperless-db`, `paperless-broker` ở trạng thái `Up` / `healthy`.<br>• Header xác thực `Authorization: Token <REDACTED_TOKEN>` hợp lệ; tổng số tài liệu trước khi tải lên: `0`.<br>• Chuẩn bị 2 tệp văn bản đầu vào giả lập tại `scripts/sample_docs/` (không chứa thông tin cá nhân):<br>  1. Tệp chính `Flow1_Invoice_ACME_Q4_2026.txt` (`247 bytes`, chứa mã đối soát riêng `KTPM-R08-FLOW-ALPHA` và kỳ cước `Q4-2026`).<br>  2. Tệp đối chứng `Flow3_Control_Report_Q4_2026.txt` (chứa mã `KTPM-R08-FLOW-BETA` và kỳ báo cáo `Q4-2026` để phục vụ đối chứng lọc ở Luồng 3). |
| **Thao tác thực hiện** | **Bước 1.1 (Tải lên):** Gửi `POST /api/documents/post_document/` (`multipart/form-data`) kèm `title="Hoa Don Dich Vu Luu Tru Dam May Q4-2026"` và tệp `Flow1_Invoice_ACME_Q4_2026.txt` (tương tự cho tệp đối chứng B).<br>**Bước 1.2 (Theo dõi xử lý hoàn tất):** Truy vấn lặp `GET /api/tasks/?task_id=57b4f69e-d598-47fe-b525-9c72370a823b` cho tới khi tác vụ kết thúc.<br>**Bước 1.3 (Truy xuất tài liệu sau xử lý):** Gọi `GET /api/documents/8/` để đọc bản ghi tài liệu + văn bản trích xuất, gọi `GET /api/documents/8/download/` để kiểm tra tệp vật lý và đối chiếu màn hình `Tasks` trên Web UI. |
| **Kết quả mong đợi** | • Bước 1.1 trả về `HTTP 200 OK` ngay lập tức kèm chuỗi `Task UUID` hợp lệ.<br>• Bước 1.2 ghi nhận `status = "success"` và trả về định danh tài liệu đã tạo (`document_id`).<br>• Bước 1.3 trả về `HTTP 200 OK` tại cả `/api/documents/{id}/` và `/download/`, trường `content` chứa đầy đủ nội dung văn bản trích xuất, `checksum` được tính toán và lưu trữ đầy đủ. |
| **Kết quả quan sát** | • **Tại thời điểm tiếp nhận:** `POST /api/documents/post_document/` trả `HTTP 200 OK` với Task UUID `"57b4f69e-d598-47fe-b525-9c72370a823b"`.<br>• **Tại thời điểm xử lý hoàn tất:** Sau `2,53 giây` (thời gian worker xử lý thực tế `duration_seconds = 2,2417 giây`), `GET /api/tasks/` ghi nhận `status: "success"`, `task_type: "consume_file"`, `result_data: {"document_id": 8}` (tệp đối chứng B hoàn tất với `document_id: 9`). Log Celery trong `paperless-webserver` xác nhận `ConsumeTaskPlugin completed with: {'document_id': 8}`.<br>• **Kết quả truy xuất tài liệu:** `GET /api/documents/8/` trả `HTTP 200 OK` với `title = "Hoa Don Dich Vu Luu Tru Dam May Q4-2026"`, `original_file_name = "Flow1_Invoice_ACME_Q4_2026.txt"`, `mime_type = "text/plain"`, trường `content` chứa nguyên vẹn chuỗi `MA DOI SOAT DUY NHAT: KTPM-R08-FLOW-ALPHA`; endpoint `GET /api/documents/8/download/` trả `HTTP 200 OK` (`247 bytes`). |
| **Minh chứng đính kèm** | • Log chi tiết: [`docs/evidence/logs/03_flow1_upload_and_processing.txt`](evidence/logs/03_flow1_upload_and_processing.txt)<br>• Ảnh giao diện: [`docs/evidence/images/03_flow1_tasks_completed.png`](evidence/images/03_flow1_tasks_completed.png) |

---

### 2.2. Luồng 2 — Tạo thông tin phân loại và gán cho tài liệu (Metadata Creation, Assignment & Re-query)

> **Nguyên tắc kiểm chứng (theo mục 2.4 báo cáo):** Không chỉ dừng ở kiểm tra mã phản hồi `PATCH 200 OK`, kịch bản thực hiện thêm bước **truy vấn lại độc lập** (`GET /api/documents/{id}/` và `GET /api/correspondents/{id}/`) để chứng minh mối quan hệ khóa ngoại và bảng trung gian N:M đã thực sự được lưu bền vững trong PostgreSQL.

| Hạng mục | Nội dung ghi nhận thực tế |
|---|---|
| **Điều kiện ban đầu** | • Tài liệu chính `ID = 8` và tài liệu đối chứng `ID = 9` đã được xử lý hoàn tất từ Luồng 1.<br>• Trạng thái phân loại ban đầu của tài liệu `ID = 8`: `correspondent = null`, `document_type = null`, `tags = []`. |
| **Thao tác thực hiện** | **Bước 2.1 (Tạo đối tượng phân loại):**<br>  1. `POST /api/tags/` với `{"name": "Demo_Tag_HoaDon_Q4", "color": "#1d4ed8", "is_inbox_tag": false}` (và tạo tag đối chứng `Demo_Tag_BienBan_Q4`).<br>  2. `POST /api/correspondents/` với `{"name": "Demo_DoiTac_ACME_Cloud", "matching_algorithm": 0, "match": "", "is_insensitive": true}` (và đối tác đối chứng `Demo_BoPhan_VanHanhNoiBo`).<br>  3. `POST /api/document_types/` với `{"name": "Demo_Loai_HoaDonDichVu", "matching_algorithm": 0, "match": "", "is_insensitive": true}` (và loại đối chứng `Demo_Loai_BienBanNghiemThu`).<br>**Bước 2.2 (Gán phân loại cho tài liệu):** Gửi `PATCH /api/documents/8/` với payload `{"tags": [74], "correspondent": 117, "document_type": 103}` (đồng thời gán bộ phân loại đối chứng cho tài liệu `ID = 9`).<br>**Bước 2.3 (Truy vấn lại độc lập):** Gửi `GET /api/documents/8/` và `GET /api/correspondents/117/`, đồng thời mở màn hình chi tiết `/documents/8/details` trên Web UI. |
| **Kết quả mong đợi** | • Cả 3 yêu cầu `POST` tạo đối tượng phân loại trả `HTTP 201 Created` kèm `id` số nguyên.<br>• Yêu cầu `PATCH /api/documents/8/` trả `HTTP 200 OK`.<br>• Truy vấn lại `GET /api/documents/8/` trả `tags = [74]`, `correspondent = 117`, `document_type = 103`; truy vấn `GET /api/correspondents/117/` ghi nhận `document_count = 1`. |
| **Kết quả quan sát** | • Tạo thành công `Tag` `ID = 74`, `Correspondent` `ID = 117`, `DocumentType` `ID = 103` (cả 3 đều nhận `HTTP 201 Created`). *(Ghi chú liên hệ K05: JSON phản hồi `201 Created` của cả 3 thao tác tạo mới thực tế không có trường `document_count`, khớp với hiện tượng sai lệch schema `BUG-03` được nhóm phân tích tại Chương 5).*<br>• `PATCH /api/documents/8/` trả `HTTP 200 OK`.<br>• Truy vấn lại độc lập `GET /api/documents/8/` trả `HTTP 200 OK` xác nhận chính xác `"correspondent": 117`, `"document_type": 103`, `"tags": [74]`; truy vấn `GET /api/correspondents/117/` xác nhận `"document_count": 1`. Trên giao diện Web UI (`/documents/8/details`), cả 3 thông tin phân loại và nội dung văn bản bên phải hiển thị đồng bộ. |
| **Minh chứng đính kèm** | • Log chi tiết: [`docs/evidence/logs/04_flow2_classification_assignment.txt`](evidence/logs/04_flow2_classification_assignment.txt)<br>• Ảnh giao diện: [`docs/evidence/images/04_flow2_document_metadata_assigned.png`](evidence/images/04_flow2_document_metadata_assigned.png) |

---

### 2.3. Luồng 3 — Tìm kiếm toàn văn và lọc tài liệu (Full-Text Search & Multi-Criteria Filtering)

> **Nguyên tắc kiểm chứng (theo mục 2.4 trang 16 báo cáo):** Để chứng minh tính đúng đắn của kết quả tìm kiếm và lọc thay vì chỉ kiểm tra cấu trúc JSON, thực nghiệm đối chiếu trực tiếp trên tập dữ liệu mẫu 2 tài liệu (`ID = 8` và đối chứng `ID = 9`) vừa có từ khóa riêng biệt vừa có từ khóa chung (`Q4-2026`).

| Hạng mục | Nội dung ghi nhận thực tế |
|---|---|
| **Điều kiện ban đầu** | • Tài liệu mục tiêu A (`ID = 8`): chứa mã riêng `KTPM-R08-FLOW-ALPHA`, từ khóa chung `Q4-2026`, gắn `tag = 74`, `correspondent = 117`, `document_type = 103`.<br>• Tài liệu đối chứng B (`ID = 9`): chứa mã riêng `KTPM-R08-FLOW-BETA`, từ khóa chung `Q4-2026`, gắn `tag = 75`, `correspondent = 118`, `document_type = 104`. |
| **Thao tác thực hiện** | **Bước 3.1 (Tìm kiếm toàn văn Tantivy):** `GET /api/documents/?query=KTPM-R08-FLOW-ALPHA`.<br>**Bước 3.2 (Lọc đa tiêu chí theo phân loại):** `GET /api/documents/?tags__id__all=74&correspondent__id=117&document_type__id=103`.<br>**Bước 3.3 (Đối chứng kết hợp từ khóa chung + lọc phân loại + phân trang):** So sánh kết quả giữa `GET /api/documents/?query=Q4-2026` (không lọc) và `GET /api/documents/?query=Q4-2026&correspondent__id=117&ordering=-created&page=1&page_size=10` (có lọc). |
| **Kết quả mong đợi** | • Bước 3.1 trả `HTTP 200 OK`, `count = 1`, chỉ chứa tài liệu `ID = 8`, kèm thông tin xếp hạng tìm kiếm `__search_hit__`.<br>• Bước 3.2 trả `HTTP 200 OK`, `count = 1`, chỉ chứa tài liệu `ID = 8` (loại trừ `ID = 9`).<br>• Bước 3.3: Truy vấn từ khóa chung `Q4-2026` trả về cả 2 tài liệu (`count = 2`); khi kết hợp thêm `correspondent__id=117`, tập kết quả thu hẹp còn đúng `count = 1` (`ID = 8`). |
| **Kết quả quan sát** | • **Bước 3.1:** `HTTP 200 OK`, `count = 1`, `results = [ID 8]`, đối tượng `__search_hit__` ghi nhận `score = 1.9041` và `highlights` đánh dấu đúng chuỗi `<span class="match">KTPM-R08-FLOW-ALPHA</span>`.<br>• **Bước 3.2:** `HTTP 200 OK`, `count = 1`, `results = [ID 8]`, loại trừ hoàn toàn tài liệu đối chứng `ID = 9`.<br>• **Bước 3.3:** Truy vấn `?query=Q4-2026` trả `count = 2` (`IDs = [9, 8]`); khi bổ sung `&correspondent__id=117&ordering=-created&page=1&page_size=10`, kết quả thu hẹp chính xác còn `count = 1` (`IDs = [8]`). Giao diện Web UI hiển thị `One document (filtered)` khớp hoàn toàn với phản hồi API. |
| **Minh chứng đính kèm** | • Log chi tiết: [`docs/evidence/logs/05_flow3_search_and_filtering.txt`](evidence/logs/05_flow3_search_and_filtering.txt)<br>• Ảnh giao diện: [`docs/evidence/images/05_flow3_search_and_filter_result.png`](evidence/images/05_flow3_search_and_filter_result.png) |

---

## 3. Đối chiếu sơ đồ Container và Luồng dữ liệu với cấu hình `docker-compose.yml`

### 3.1. Bảng đối chiếu trực tiếp giữa cấu hình Compose thực tế và Sơ đồ kiến trúc / Luồng dữ liệu

Thực hiện rà soát từng mục trong [`docker-compose.yml`](../docker-compose.yml) và kiểm tra tiến trình thực tế trong container để đảm bảo sơ đồ tại Chương 4 không vẽ thừa dịch vụ và không sai lệch công nghệ:

| Thành phần trong `docker-compose.yml` | Khai báo cấu hình cụ thể | Tiến trình / Vai trò thực tế xác minh trên container | Cách thể hiện trên Sơ đồ Container & Luồng dữ liệu (Đã chuẩn hóa) |
|---|---|---|---|
| **Service `webserver`**<br>(`paperless-webserver`) | `image: ghcr.io/paperless-ngx/paperless-ngx:3.1.3`<br>`ports: ["8000:8000"]`<br>`depends_on: [db, broker]`<br>`env_file: [.env]` | Tiến trình `/init` (`s6-overlay`) quản lý đồng thời: `svc-webserver` (Granian HTTP/ASGI `:8000` chạy Django/DRF + giao diện Angular SPA), `svc-worker` (Celery Worker + OCRmyPDF/Tesseract), `svc-scheduler` (Celery Beat) và `svc-consumer`. | Gom đúng các thành phần Web/API, Celery Worker, OCR và chỉ mục tìm kiếm **Tantivy** vào bên trong **cùng một container `paperless-webserver`** (giải thích rõ nhận xét tại Hình 2.1 trang 11 báo cáo là mỗi thành phần logic không nhất thiết tách thành container riêng). |
| **Service `db`**<br>(`paperless-db`) | `image: postgres:16-alpine`<br>`volumes: [pgdata:/var/lib/postgresql/data]`<br>*(Không khai báo `ports:` ra Host)* | Lắng nghe cổng `5432/tcp` nội bộ trong mạng bridge `ktpm_default` (`PAPERLESS_DBHOST=db`). Trình duyệt và Schemathesis không kết nối trực tiếp tới PostgreSQL. | Đặt trong khung mạng nội bộ `ktpm_default`, chỉ nối hai chiều `SQL :5432` với `webserver` và gắn sang `Named Volume: pgdata`. |
| **Service `broker`**<br>(`paperless-broker`) | `image: redis:7-alpine`<br>`volumes: [redisdata:/data]`<br>*(Không khai báo `ports:` ra Host)* | Lắng nghe cổng `6379/tcp` nội bộ (`PAPERLESS_REDIS=redis://broker:6379`). Làm hàng đợi phân phối tác vụ `consume_file` giữa `svc-webserver` và `svc-worker`. | Đặt trong khung mạng nội bộ `ktpm_default`, nối với `webserver` qua `Redis :6379` và gắn sang `Named Volume: redisdata`. |
| **4 Named Volumes** | `data`, `media`, `pgdata`, `redisdata` | • `media` (`/usr/src/paperless/media`): lưu tệp gốc, tệp lưu trữ sau OCR, ảnh thu nhỏ.<br>• `data` (`/usr/src/paperless/data`): lưu chỉ mục tìm kiếm toàn văn **Tantivy** (Paperless-ngx `v3.1.3` dùng `tantivy~=0.26.0`, đã hiệu chỉnh lại so với bản nháp cũ ghi Whoosh).<br>• `pgdata`, `redisdata`: lưu dữ liệu bền vững cho DB và Broker. | Tách rõ 4 hộp Named Volume riêng biệt với đường dẫn mount chính xác từ `docker-compose.yml`, không có đường mũi tên cắt đè qua container khác. |
| **Bind Mounts & Biến môi trường** | `./export:/usr/src/paperless/export`<br>`./consume:/usr/src/paperless/consume`<br>`env_file: .env` (`PAPERLESS_TIKA_ENABLED=0`) | Thư mục `./consume` và `./export` ánh xạ trực tiếp từ máy chủ Host vào `webserver`. Biến `PAPERLESS_TIKA_ENABLED=0` xác nhận hệ thống **không** chạy thêm container Apache Tika hay Gotenberg. | Biểu diễn khối `Bind Mounts & env_file` nối vào `webserver` và bổ sung ô ghi chú rõ chỉ có đúng **3 containers** thực tế (`PAPERLESS_TIKA_ENABLED=0`). |

### 3.2. Danh sách tệp ảnh / sơ đồ chèn Word và Chú thích chuẩn (Captions)

Các tệp ảnh dưới đây đã được xuất ở độ phân giải **300 DPI** (kèm bản vector `.svg`, tệp `.drawio` và bản Word chèn sẵn tại [`docs/TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx`](TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx)) để TV2 đưa thẳng vào **Chương 4**:

1. **Sơ đồ kiến trúc triển khai Container:**
   * Tệp ảnh: [`docs/images/so_do_kien_truc_container.png`](images/so_do_kien_truc_container.png) (Vector: [`.svg`](images/so_do_kien_truc_container.svg) · Draw.io: [`.drawio`](diagrams/so_do_kien_truc_container.drawio))
   * **Chú thích chèn Word:**  
     > *Hình 4.1. Kiến trúc triển khai thực tế của Paperless-ngx v3.1.3 trên Docker Compose gồm ba container (`paperless-webserver`, `paperless-db`, `paperless-broker`), các tiến trình nội bộ dưới `s6-overlay` và các vùng lưu trữ dữ liệu.*

2. **Sơ đồ luồng dữ liệu 3 nghiệp vụ vận hành trên cấu hình Compose:**
   * Tệp ảnh: [`docs/images/so_do_luong_du_lieu.png`](images/so_do_luong_du_lieu.png) (Vector: [`.svg`](images/so_do_luong_du_lieu.svg))
   * **Chú thích chèn Word:**  
     > *Hình 4.2. Luồng dữ liệu của ba nghiệp vụ vận hành (tải lên và xử lý nền, tạo và gán thông tin phân loại, tìm kiếm và lọc) ánh xạ trực tiếp trên các dịch vụ Docker Compose và vùng lưu trữ.*

3. **Sơ đồ quan hệ dữ liệu cốt lõi (ER Diagram):**
   * Tệp ảnh: [`docs/images/so_do_quan_he_du_lieu.png`](images/so_do_quan_he_du_lieu.png) (Vector: [`.svg`](images/so_do_quan_he_du_lieu.svg) · Draw.io: [`.drawio`](diagrams/so_do_quan_he_du_lieu.drawio))
   * **Chú thích chèn Word:**  
     > *Hình 4.3. Sơ đồ quan hệ dữ liệu giữa tài liệu (`Document`) và các đối tượng phân loại (`Tag`, `Correspondent`, `DocumentType`) trong cơ sở dữ liệu PostgreSQL của Paperless-ngx v3.1.3.*

4. **Bộ 5 ảnh chụp giao diện minh chứng vận hành (đã che thông tin tài khoản):**
   * [`docs/evidence/images/01_webui_login_screen.png`](evidence/images/01_webui_login_screen.png) — *Chú thích:* *Hình 4.4. Màn hình đăng nhập giao diện web Paperless-ngx tại địa chỉ `http://localhost:8000`.*
   * [`docs/evidence/images/02_openapi_schema_view.png`](evidence/images/02_openapi_schema_view.png) — *Chú thích:* *Hình 4.5. Giao diện tài liệu đặc tả OpenAPI 3.0.3 (`Paperless-ngx REST API 6.0.0 (10)`) truy cập tại `/api/schema/view/`.*
   * [`docs/evidence/images/03_flow1_tasks_completed.png`](evidence/images/03_flow1_tasks_completed.png) — *Chú thích:* *Hình 4.6. Minh chứng Luồng 1 trên giao diện Tasks: tác vụ tiếp nhận và xử lý tệp tải lên qua API đã hoàn tất (`Recently completed`) và sẵn sàng mở tài liệu.*
   * [`docs/evidence/images/04_flow2_document_metadata_assigned.png`](evidence/images/04_flow2_document_metadata_assigned.png) — *Chú thích:* *Hình 4.7. Minh chứng Luồng 2 trên màn hình chi tiết tài liệu (ID 8): thông tin Correspondent, Document type, Tag và nội dung văn bản trích xuất hiển thị sau khi gán.*
   * [`docs/evidence/images/05_flow3_search_and_filter_result.png`](evidence/images/05_flow3_search_and_filter_result.png) — *Chú thích:* *Hình 4.8. Minh chứng Luồng 3 trên giao diện Documents: tìm kiếm nội dung văn bản trả về đúng một tài liệu khớp điều kiện (`One document (filtered)`).*

---

## 4. Biên bản rà soát che thông tin nhạy cảm trước khi đưa lên GitHub

Thực hiện đúng yêu cầu bảo mật tại bảng rủi ro mục 4.5 báo cáo (*"Che token, mật khẩu; kiểm tra log và ảnh trước khi đưa vào báo cáo"*):

1. **Tệp cấu hình `.env`:** Bị chặn bởi `.gitignore` (`git status --ignored` xác nhận không theo dõi `.env`). Các script [`demo_system.py`](../scripts/demo_system.py), [`reset_data.py`](../scripts/reset_data.py), [`seed_data.py`](../scripts/seed_data.py), [`run_manual_tests.py`](../scripts/run_manual_tests.py) và [`run_tv4_tests.ps1`](../scripts/run_tv4_tests.ps1) đều đọc biến môi trường từ `.env` và không in giá trị mật khẩu hay token ra màn hình.
2. **Tệp log minh chứng (`docs/evidence/logs/*`):** Hàm `redact_sensitive()` tự động thay thế mọi chuỗi `Authorization: Token ...` thành `Token <REDACTED_TOKEN>`, mật khẩu thành `<REDACTED_PASSWORD>` / `<REDACTED_SECRET>`, địa chỉ email thành `<REDACTED_EMAIL>` và đường dẫn người dùng cục bộ thành `<USER_HOME>`.
3. **Ảnh chụp màn hình giao diện (`docs/evidence/images/*`):** Màn hình đăng nhập để trống ô mật khẩu; góc phải thanh điều hướng hiển thị tên tài khoản trên các ảnh `03`, `04`, `05` đã được phủ nhãn che `[REDACTED]`; nội dung các tệp mẫu chỉ dùng dữ liệu doanh nghiệp giả lập (`CONG TY DICH VU DAM MAY ACME`), không chứa họ tên, MSSV, email hay số điện thoại cá nhân.

---

## 5. Ghi chú cách chạy Demo (Demo Runbook)

### 5.1. Điều kiện trước khi chạy Demo
1. Docker Desktop (WSL2 backend) đang bật trên máy.
2. Đứng tại thư mục gốc kho mã nguồn `KTPM` và đảm bảo đã có tệp `.env` (nếu chưa có: `Copy-Item .env.example .env`).
3. Khởi chạy và kiểm tra trạng thái 3 container:
   ```powershell
   docker compose up -d
   docker compose ps
   ```
   Đợi tới khi cột `STATUS` của `paperless-webserver` hiển thị `(healthy)`.

### 5.2. Chạy kịch bản Demo 3 luồng vận hành tự động (Khuyến nghị khi trình bày bảo vệ)

* **Cách 1 — Chạy sạch từ đầu (xóa dữ liệu thử nghiệm cũ có phân trang + làm rỗng thùng rác + thực thi trọn vẹn 3 luồng & xuất log minh chứng, mất ~10 giây):**
  ```powershell
  .\.venv\Scripts\python.exe scripts/demo_system.py --reset-first
  ```
  > *Lưu ý:* Cờ `--reset-first` sẽ xóa toàn bộ tài liệu và thông tin phân loại hiện có trên môi trường thử nghiệm cục bộ. Chỉ sử dụng trên môi trường kiểm thử cục bộ.

* **Cách 2 — Chạy giữ nguyên dữ liệu hiện có và chỉ trình diễn trên màn hình console (không ghi đè tệp log đã lưu):**
  ```powershell
  .\.venv\Scripts\python.exe scripts/demo_system.py --no-save
  ```

### 5.3. Chạy bổ trợ bộ 18 ca kiểm thử hộp đen tài nguyên `Correspondents` (nếu giảng viên yêu cầu)
```powershell
.\.venv\Scripts\python.exe scripts/run_manual_tests.py
```
Kịch bản sẽ tự động chạy các ca kiểm thử phân vùng tương đương (EP) và giá trị biên (BVA `128`/`129` ký tự), đồng thời minh họa trực tiếp 2 phát hiện thực tế trên tài nguyên `Correspondents`: `TC-CORR-01` (phản hồi `201 Created` thiếu `document_count` — `BUG-03`) và `TC-CORR-11` (`set_permissions` sai kiểu gây `HTTP 500` — `BUG-01`).

### 5.4. Thứ tự mở màn hình đối chiếu trực quan trong buổi bảo vệ (~60 giây)
1. Chạy `.\.venv\Scripts\python.exe scripts/demo_system.py --reset-first` trên Terminal để giảng viên quan sát trực tiếp 3 luồng (`Task UUID` $\rightarrow$ `status=success` sau ~2,2 giây $\rightarrow$ `PATCH 200` & `GET 200` lưu quan hệ $\rightarrow$ tìm kiếm Tantivy & lọc đối chứng `3/3 PASS`).
2. Mở trình duyệt tại `http://localhost:8000/tasks` (tab `Recently completed`) chỉ rõ tác vụ `Consume File • API Upload` đã hoàn tất.
3. Nhấn `Open Document` vào tài liệu vừa tạo để chỉ rõ 3 trường phân loại (`Demo_DoiTac_ACME_Cloud`, `Demo_Loai_HoaDonDichVu`, `Demo_Tag_HoaDon_Q4`) và nội dung văn bản đã trích xuất bên khung phải.
4. Quay lại `http://localhost:8000/documents`, nhập mã `KTPM-R08-FLOW-ALPHA` hoặc lọc theo Correspondent để chỉ rõ hệ thống lọc chính xác còn 1 tài liệu mục tiêu.
