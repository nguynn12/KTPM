# TỔNG HỢP MÃ NGUỒN MERMAID VÀ TỆP DRAW.IO CHO BỘ SƠ ĐỒ BÁO CÁO (CHƯƠNG 2 & CHƯƠNG 4)
**Đề tài R08 + K05: Kiểm thử API Paperless-ngx v3.1.3 bằng Schemathesis · Nhóm 17**  
*Thành viên thực hiện & đối chiếu cấu hình Compose: TV4 — Nguyễn Nhất Minh (MSSV: 2312690)*

Tài liệu này cung cấp mã nguồn sơ đồ đã đối chiếu 1–1 với [`docker-compose.yml`](../../docker-compose.yml) và kết quả vận hành thực tế:
1. **Sơ đồ kiến trúc triển khai Container (Docker Compose)** — chèn Chương 4.
2. **Sơ đồ luồng dữ liệu 3 nghiệp vụ vận hành trên cấu hình Compose** — chèn Chương 4.
3. **Sơ đồ quan hệ dữ liệu cốt lõi (ER Diagram)** — tham chiếu Chương 2 / Chương 4.

---

## 1. SƠ ĐỒ KIẾN TRÚC TRIỂN KHAI CONTAINER (DOCKER COMPOSE)

- **Ảnh 300 DPI chèn Word:** [`docs/images/so_do_kien_truc_container.png`](../images/so_do_kien_truc_container.png)
- **Ảnh Vector SVG:** [`docs/images/so_do_kien_truc_container.svg`](../images/so_do_kien_truc_container.svg)
- **Tệp chỉnh sửa Draw.io:** [`docs/diagrams/so_do_kien_truc_container.drawio`](so_do_kien_truc_container.drawio)
- **Chú thích gợi ý chèn Word:**  
  *Hình 4.1. Kiến trúc triển khai ba dịch vụ Docker Compose (`webserver`, `db`, `broker`), các tiến trình nội bộ dưới `s6-overlay` và các vùng lưu trữ của Paperless-ngx v3.1.3 trong môi trường thực nghiệm.*

```mermaid
flowchart LR
    subgraph CLIENTS ["TÁC NHÂN BÊN NGOÀI (HOST)"]
        UI["Trình duyệt Web (Angular SPA)<br/>http://localhost:8000"]
        ST["Schemathesis CLI v4.30.1<br/>Seeds: 101..505 | V1:19 · V2:18 · V3:53<br/>Header: Token &lt;REDACTED&gt;"]
        SC["Scripts Kiểm thử &amp; Demo<br/>demo_system.py · seed_data.py<br/>/api/schema/ · /api/schema/view/"]
    end

    subgraph DOCKER_NET ["MẠNG NỘI BỘ DOCKER COMPOSE (Bridge: ktpm_default)"]
        subgraph WEBSERVER ["Service: webserver (paperless-webserver) — ghcr.io/paperless-ngx/paperless-ngx:3.1.3 (8000:8000)"]
            DRF["svc-webserver (Granian :8000)<br/>Django + DRF ViewSets &amp; Serializers<br/>drf-spectacular (/api/schema/)"]
            WORKER["svc-worker &amp; svc-scheduler<br/>Celery Worker + Celery Beat<br/>OCRmyPDF + Tesseract"]
            INDEX["Tantivy Search Engine &amp; svc-consumer<br/>Chỉ mục toàn văn · Theo dõi /consume"]
        end

        DB[("Service: db (paperless-db)<br/>postgres:16-alpine · Nội bộ 5432/tcp<br/>documents, tags, correspondents, types")]
        BROKER[("Service: broker (paperless-broker)<br/>redis:7-alpine · Nội bộ 6379/tcp<br/>PAPERLESS_REDIS=redis://broker:6379")]
    end

    subgraph VOLUMES ["VÙNG LƯU TRỮ &amp; CẤU HÌNH"]
        V_MEDIA[("Named Volume: media<br/>/usr/src/paperless/media")]
        V_DATA[("Named Volume: data<br/>/usr/src/paperless/data (Tantivy)")]
        V_BIND["Bind Mounts &amp; env_file<br/>./consume · ./export · .env"]
        V_PG[("Named Volume: pgdata<br/>/var/lib/postgresql/data")]
        V_RD[("Named Volume: redisdata<br/>/data")]
    end

    UI -->|"HTTP :8000"| DRF
    ST -->|"REST API (:8000)"| DRF
    SC -->|"HTTP :8000"| DRF

    DRF <-->|"SQL :5432"| DB
    WORKER -->|"SQL :5432"| DB
    DRF -->|"Đẩy job :6379"| BROKER
    BROKER -->|"Phân phối task"| WORKER
    WORKER <--> INDEX

    WEBSERVER -.->|"mount"| V_MEDIA
    WEBSERVER -.->|"mount"| V_DATA
    WEBSERVER -.->|"bind / env"| V_BIND
    DB -.->|"mount"| V_PG
    BROKER -.->|"mount"| V_RD
```

---

## 2. SƠ ĐỒ LUỒNG DỮ LIỆU BA NGHIỆP VỤ VẬN HÀNH TRÊN CẤU HÌNH COMPOSE

- **Ảnh 300 DPI chèn Word:** [`docs/images/so_do_luong_du_lieu.png`](../images/so_do_luong_du_lieu.png)
- **Ảnh Vector SVG:** [`docs/images/so_do_luong_du_lieu.svg`](../images/so_do_luong_du_lieu.svg)
- **Chú thích gợi ý chèn Word:**  
  *Hình 4.2. Luồng dữ liệu của ba nghiệp vụ vận hành trọng tâm (tải lên và xử lý nền, gán thông tin phân loại, tìm kiếm và lọc) ánh xạ trên các dịch vụ Docker Compose và vùng lưu trữ.*

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Web UI / Script
    participant API as webserver: svc-webserver (DRF :8000)
    participant Redis as broker: redis:7-alpine (:6379)
    participant Worker as webserver: svc-worker (Celery + OCR)
    participant Store as db (Postgres :5432) + volumes (media, data)

    rect rgb(239, 246, 255)
    Note over Client,Store: Luồng 1 — Tải lên và xử lý tài liệu bất đồng bộ
    Client->>API: POST /api/documents/post_document/ (multipart + Token <REDACTED>)
    API->>Redis: Ghi tạm scratch & đẩy consume_file.delay()
    API-->>Client: HTTP 200 OK + Task UUID (tiếp nhận tức thì)
    Redis->>Worker: Phân phối tác vụ nền consume_file
    Worker->>Store: OCR/trích xuất văn bản -> INSERT db + lưu volume:media + chỉ mục Tantivy (volume:data)
    Client->>API: GET /api/tasks/?task_id=... (status=success) & GET /api/documents/{id}/
    API->>Store: Truy xuất metadata, nội dung văn bản và tệp lưu trữ
    Store-->>Client: HTTP 200 OK (tài liệu hoàn tất xử lý & tải được tệp gốc)
    end

    rect rgb(250, 245, 255)
    Note over Client,Store: Luồng 2 — Tạo thông tin phân loại và gán cho tài liệu
    Client->>API: POST /api/tags/, /api/correspondents/, /api/document_types/
    API->>Store: Validate ràng buộc & INSERT vào db:5432
    Store-->>Client: HTTP 201 Created (trả về ID từng đối tượng phân loại)
    Client->>API: PATCH /api/documents/{id}/ {tags, correspondent, document_type}
    API->>Store: UPDATE khóa ngoại & bảng N:M + đồng bộ chỉ mục Tantivy
    Client->>API: GET /api/documents/{id}/ (truy vấn lại độc lập)
    Store-->>Client: HTTP 200 OK (xác nhận quan hệ phân loại đã lưu bền vững)
    end

    rect rgb(240, 253, 250)
    Note over Client,Store: Luồng 3 — Tìm kiếm toàn văn và lọc đa tiêu chí
    Client->>API: GET /api/documents/?query=...&tags__id__all=...&correspondent__id=...
    API->>Store: Tra cứu chỉ mục ngược Tantivy (volume:data) lấy ID & điểm xếp hạng (score)
    API->>Store: Kết hợp lọc metadata, quyền Guardian & phân trang trên PostgreSQL (db:5432)
    Store-->>Client: HTTP 200 OK {count, results, __search_hit__} (khớp đúng tập dữ liệu đối chứng)
    end
```

---

## 3. SƠ ĐỒ QUAN HỆ DỮ LIỆU CỐT LÕI (ER DIAGRAM)

- **Ảnh 300 DPI chèn Word:** [`docs/images/so_do_quan_he_du_lieu.png`](../images/so_do_quan_he_du_lieu.png)
- **Ảnh Vector SVG:** [`docs/images/so_do_quan_he_du_lieu.svg`](../images/so_do_quan_he_du_lieu.svg)
- **Tệp chỉnh sửa Draw.io:** [`docs/diagrams/so_do_quan_he_du_lieu.drawio`](so_do_quan_he_du_lieu.drawio)
- **Chú thích gợi ý chèn Word:**  
  *Hình 4.3. Sơ đồ quan hệ dữ liệu giữa thực thể tài liệu (`Document`) và ba nhóm thực thể phân loại (`Tag`, `Correspondent`, `DocumentType`) trong PostgreSQL (`src/documents/models.py`, tag `v3.1.3`).*
