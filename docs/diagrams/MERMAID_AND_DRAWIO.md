# TỔNG HỢP MÃ NGUỒN MERMAID VÀ DRAW.IO CHO 2 SƠ ĐỒ BÁO CÁO
**Đề tài R08 + K05: Kiểm thử hệ thống Paperless-ngx v3.1.3 · Nhóm 17**  
*Thành viên thực hiện: TV4 — Nguyễn Nhất Minh (MSSV: 2312690)*

Tài liệu này cung cấp đầy đủ:
1. **Mã Mermaid** để hiển thị trực tiếp trên GitHub / Markdown / Notion.
2. **Tệp Draw.io (`.drawio`)** để mở, chỉnh sửa màu sắc, kéo thả và xuất ảnh PNG/PDF trên [app.diagrams.net](https://app.diagrams.net).

---

## 1. HÌNH 1: SƠ ĐỒ KIẾN TRÚC CONTAINER HỆ THỐNG (DOCKER COMPOSE)

### 1.1. Mã nguồn Mermaid (Hình 1)
Sao chép toàn bộ khối mã dưới đây để chèn vào Markdown hoặc công cụ hỗ trợ Mermaid:

```mermaid
flowchart TB
    subgraph CLIENTS ["1. TẦNG CLIENTS & TEST HARNESS"]
        UI["🌐 Trình duyệt Web (Angular UI)<br/>http://localhost:8000"]
        ST["⚙️ Schemathesis QA (Seed 404)<br/>V1: 19 ops | V2: 18 ops | V3: 53 ops"]
        SWAGGER["📄 Swagger UI / cURL / Python<br/>http://localhost:8000/api/schema/"]
    end

    subgraph DOCKER_NET ["2. MẠNG NỘI BỘ DOCKER (ktpm_default)"]
        subgraph C_WEBSERVER ["Container 1: paperless-webserver (ghcr.io/paperless-ngx/paperless-ngx:3.1.3)"]
            DRF["Backend Django REST Framework<br/>• ViewSets: Tag, Corr, Doc, Type<br/>• Serializers & Validation<br/>• Cổng Host: 8000"]
            CELERY["Celery Worker & OCR Pipeline<br/>• Nhận task từ Redis<br/>• OCRmyPDF + Tesseract Engine<br/>• Trích xuất văn bản & Thumbnails"]
            INDEX["Whoosh Search Indexer<br/>• Chỉ mục tìm kiếm toàn văn"]
        end

        subgraph C_DB ["Container 2: paperless-db (postgres:16-alpine)"]
            PG["Cơ sở dữ liệu PostgreSQL 16<br/>• Cổng nội bộ: 5432<br/>• Bảng: documents, tags, correspondents, types, auth"]
        end

        subgraph C_BROKER ["Container 3: paperless-broker (redis:7-alpine)"]
            REDIS["Redis 7 In-Memory Broker<br/>• Cổng nội bộ: 6379<br/>• Celery Task Queue (Điều phối hàng đợi tác vụ ngầm)"]
        end
    end

    subgraph VOLUMES ["3. PERSISTENT VOLUMES (LƯU TRỮ TRÊN HOST)"]
        V_MEDIA[("📁 volume: media<br/>Tài liệu gốc, file OCR, thumbnails")]
        V_DATA[("📁 volume: data<br/>Whoosh search index, config nội bộ")]
        V_PGDATA[("🗄️ volume: pgdata<br/>Dữ liệu bảng PostgreSQL")]
        V_REDISDATA[("⚡ volume: redisdata<br/>Trạng thái hàng đợi Redis (dump.rdb)")]
        V_HOST["📂 Host Bind Mounts<br/>./consume · ./export · .env"]
    end

    %% Tương tác Clients -> Webserver
    UI -->|"HTTP :8000"| DRF
    ST -->|"REST API (Token Auth)"| DRF
    SWAGGER -->|"OpenAPI 3.0.3"| DRF

    %% Tương tác Webserver nội bộ
    DRF <-->|"Đẩy / Nhận task"| CELERY
    CELERY <-->|"Cập nhật chỉ mục"| INDEX

    %% Tương tác Webserver <-> DB
    DRF <-->|"SQL (Port 5432)"| PG
    CELERY -->|"Lưu metadata sau OCR"| PG

    %% Tương tác Webserver <-> Redis
    DRF -->|"Đẩy job upload (Port 6379)"| REDIS
    CELERY <-->|"Tiêu thụ hàng đợi task"| REDIS

    %% Gắn Volumes
    C_WEBSERVER -.->|"Gắn mount"| V_MEDIA
    C_WEBSERVER -.->|"Gắn mount"| V_DATA
    C_WEBSERVER -.->|"Gắn mount"| V_HOST
    C_DB -.->|"Gắn mount"| V_PGDATA
    C_BROKER -.->|"Gắn mount"| V_REDISDATA

    classDef clientStyle fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px;
    classDef serverStyle fill:#f8fafc,stroke:#2563eb,stroke-width:2px;
    classDef dbStyle fill:#f0fdf4,stroke:#0d9488,stroke-width:2px;
    classDef brokerStyle fill:#fef2f2,stroke:#ef4444,stroke-width:2px;
    classDef volStyle fill:#f1f5f9,stroke:#64748b,stroke-width:1.5px;

    class UI,ST,SWAGGER clientStyle;
    class C_WEBSERVER serverStyle;
    class C_DB dbStyle;
    class C_BROKER brokerStyle;
    class V_MEDIA,V_DATA,V_PGDATA,V_REDISDATA,V_HOST volStyle;
```

### 1.2. Tệp Draw.io tương ứng (Hình 1)
- Tệp tin: [`docs/diagrams/so_do_kien_truc_container.drawio`](file:///d:/Kiem-thu-phan-mem/KTPM/docs/diagrams/so_do_kien_truc_container.drawio)
- Ảnh xuất sẵn 300 DPI: [`docs/images/so_do_kien_truc_container.png`](file:///d:/Kiem-thu-phan-mem/KTPM/docs/images/so_do_kien_truc_container.png)

---

## 2. HÌNH 2: SƠ ĐỒ QUAN HỆ DỮ LIỆU CỐT LÕI (ER DIAGRAM)

### 2.1. Mã nguồn Mermaid (Hình 2)
Sao chép toàn bộ khối mã dưới đây:

```mermaid
erDiagram
    User ||--o{ Document : "owns (1 : N)"
    User ||--o{ Tag : "owns (1 : N)"
    User ||--o{ Correspondent : "owns (1 : N)"
    User ||--o{ DocumentType : "owns (1 : N)"

    Correspondent ||--o{ Document : "sender of (1 : N, null=True)"
    DocumentType ||--o{ Document : "categorizes (1 : N, null=True)"
    Document }o--o{ Tag : "tagged with (N : M qua documents_document_tags)"
    Tag ||--o{ Tag : "parent of (cây phân cấp đệ quy <= 5 cấp)"

    User {
        int id PK
        varchar username "Tên đăng nhập"
        varchar email "Email"
        boolean is_superuser "Quyền quản trị"
        boolean is_active "Trạng thái kích hoạt"
    }

    Document {
        int id PK
        varchar title "Tiêu đề (max 128)"
        text content "Văn bản trích xuất OCR"
        date created "Ngày của văn bản"
        datetime modified "Ngày chỉnh sửa"
        varchar checksum "MD5 mã băm tệp"
        varchar mime_type "Định dạng tệp"
        int correspondent_id FK "Người gửi (null được)"
        int document_type_id FK "Loại tài liệu (null được)"
        int owner_id FK "Chủ sở hữu"
    }

    Correspondent {
        int id PK
        varchar name "Tên người gửi (max 128, required)"
        varchar slug "Slug tự sinh"
        varchar match "Quy tắc so khớp (max 256)"
        int matching_algorithm "Thuật toán matching (0..6)"
        boolean is_insensitive "Không phân biệt hoa thường"
        int owner_id FK "Chủ sở hữu"
    }

    DocumentType {
        int id PK
        varchar name "Tên loại tài liệu (max 128, required)"
        varchar slug "Slug tự sinh"
        varchar match "Quy tắc so khớp (max 256)"
        int matching_algorithm "Thuật toán matching (0..6)"
        boolean is_insensitive "Không phân biệt hoa thường"
        int owner_id FK "Chủ sở hữu"
    }

    Tag {
        int id PK
        varchar name "Tên nhãn (max 128, required)"
        varchar color "Mã màu HEX (max 7, ví dụ #a6cee3)"
        varchar match "Quy tắc so khớp (max 256)"
        int matching_algorithm "Thuật toán matching (0..6)"
        boolean is_insensitive "Không phân biệt hoa thường"
        boolean is_inbox_tag "Nhãn hộp thư đến"
        int parent_id FK "Tag cha (đệ quy <= 5)"
        int owner_id FK "Chủ sở hữu"
    }
```

### 2.2. Tệp Draw.io tương ứng (Hình 2)
- Tệp tin: [`docs/diagrams/so_do_quan_he_du_lieu.drawio`](file:///d:/Kiem-thu-phan-mem/KTPM/docs/diagrams/so_do_quan_he_du_lieu.drawio)
- Ảnh xuất sẵn 300 DPI: [`docs/images/so_do_quan_he_du_lieu.png`](file:///d:/Kiem-thu-phan-mem/KTPM/docs/images/so_do_quan_he_du_lieu.png)

---

## 3. HƯỚNG DẪN MỞ VÀ CHỈNH SỬA TRÊN DRAW.IO (APP.DIAGRAMS.NET)

### Cách 1: Mở trực tiếp file `.drawio` (Khuyên dùng - Nhanh và đẹp nhất)
1. Truy cập trang web vẽ sơ đồ miễn phí: **https://app.diagrams.net/** (hoặc mở phần mềm draw.io Desktop).
2. Chọn **Open Existing Diagram** (Mở sơ đồ có sẵn) $\rightarrow$ Duyệt tới thư mục `docs/diagrams/` trong dự án:
   * Chọn `so_do_kien_truc_container.drawio` (Hình 1) hoặc `so_do_quan_he_du_lieu.drawio` (Hình 2).
3. Sơ đồ sẽ mở ra với đầy đủ các khối hộp, màu sắc chuyên nghiệp, đường mũi tên động và chữ tiếng Việt chuẩn. Bạn có thể tự do kéo giãn, đổi màu hoặc thay đổi font chữ theo ý muốn.
4. **Xuất file ảnh:** Chọn **File** $\rightarrow$ **Export as** $\rightarrow$ **PNG...** (chọn độ phân giải 300 DPI để chèn vào báo cáo Word hoặc Slide).

### Cách 2: Nhập trực tiếp mã Mermaid vào Draw.io
1. Trên giao diện của draw.io, vào menu trên cùng: **Arrange** $\rightarrow$ **Insert** $\rightarrow$ **Advanced** $\rightarrow$ **Mermaid**.
2. Dán đoạn mã Mermaid ở Mục 1.1 hoặc 2.1 phía trên vào ô nhập liệu.
3. Bấm nút **Insert** $\rightarrow$ Draw.io sẽ tự động dựng toàn bộ sơ đồ thành các đối tượng đồ họa để bạn chỉnh sửa.
