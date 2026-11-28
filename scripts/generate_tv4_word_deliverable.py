#!/usr/bin/env python3
"""
scripts/generate_tv4_word_deliverable.py
Sinh tệp Word (.docx) bàn giao Chương 4 cho TV2 tích hợp báo cáo cuối kỳ:
  - docs/TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx
Bao gồm:
  1. Bảng đối chiếu cấu hình docker-compose.yml với sơ đồ triển khai và luồng dữ liệu.
  2. Bộ 3 sơ đồ 300 DPI (Container, Luồng dữ liệu 3 nghiệp vụ, Quan hệ dữ liệu ERD) kèm chú thích chuẩn.
  3. Bảng tổng hợp và kết quả chi tiết 3 luồng vận hành (điều kiện đầu, thao tác, mong đợi, quan sát).
  4. Bộ 5 ảnh chụp giao diện thực tế đã che thông tin tài khoản kèm chú thích chèn Word.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def set_cell_bg(cell, hex_color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_pr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))


def set_cell_pad(cell, top=90, bottom=90, left=130, right=130) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_pr.append(
        parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f"</w:tcMar>"
        )
    )


def add_styled_table(doc: Document, headers: list[str], rows: list[tuple[str, ...]]) -> None:
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = ""
        run = c.paragraphs[0].add_run(h)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_bg(c, "1E3A8A")
        set_cell_pad(c)
    for i, row in enumerate(rows):
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            c.text = ""
            run = c.paragraphs[0].add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            if j == 0:
                run.font.bold = True
            set_cell_bg(c, bg)
            set_cell_pad(c)


def add_figure(doc: Document, img_path: str, caption: str, width_in: float = 6.3) -> None:
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(img_path, width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(11)
    r_cap.font.italic = True


def build_docx() -> None:
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.9)
        sec.bottom_margin = Inches(0.9)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(0.9)

    normal_font = doc.styles["Normal"].font
    normal_font.name = "Times New Roman"
    normal_font.size = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_title.add_run("NHÓM 17 — ĐỀ TÀI R08 PAPERLESS-NGX + K05 SCHEMATHESIS\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = True

    r2 = p_title.add_run("TÀI LIỆU BÀN GIAO MINH CHỨNG VẬN HÀNH & SƠ ĐỒ CHÈN CHƯƠNG 4\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(15)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(30, 58, 138)

    r3 = p_title.add_run(
        "Người thực hiện: TV4 — Nguyễn Nhất Minh (MSSV: 2312690) · Nhánh: TV4_NguyenNhatMinh\n"
        "Đã rà soát che toàn bộ token, mật khẩu và thông tin cá nhân (<REDACTED>)"
    )
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(11)
    r3.font.italic = True

    # Phần 1: Sơ đồ Container & Luồng dữ liệu kèm đối chiếu Compose
    h1 = doc.add_heading("1. Đối chiếu sơ đồ triển khai Container và Luồng dữ liệu với docker-compose.yml", level=1)
    h1.runs[0].font.name = "Times New Roman"

    compose_rows = [
        (
            "webserver\n(paperless-webserver)",
            "ghcr.io/paperless-ngx/paperless-ngx:3.1.3\nports: 8000:8000 | depends_on: db, broker\nenv_file: .env",
            "Tiến trình /init (s6-overlay) chạy đồng thời svc-webserver (Granian :8000 + Django/DRF + Angular SPA), svc-worker (Celery + OCRmyPDF/Tesseract), svc-scheduler và svc-consumer.",
        ),
        (
            "db\n(paperless-db)",
            "postgres:16-alpine\nvolumes: pgdata:/var/lib/postgresql/data\n(Không mở cổng ra Host)",
            "Cổng nội bộ 5432/tcp trên mạng ktpm_default. Lưu bảng documents_document, tags, correspondents, document_types và phân quyền.",
        ),
        (
            "broker\n(paperless-broker)",
            "redis:7-alpine\nvolumes: redisdata:/data\n(Không mở cổng ra Host)",
            "Cổng nội bộ 6379/tcp (redis://broker:6379). Hàng đợi phân phối tác vụ nền consume_file tách khỏi chu trình phản hồi HTTP.",
        ),
        (
            "Named Volumes &\nBind Mounts",
            "data, media, pgdata, redisdata\n./consume, ./export, .env\n(PAPERLESS_TIKA_ENABLED=0)",
            "media lưu tệp gốc/lưu trữ/thumbnails; data lưu chỉ mục tìm kiếm toàn văn Tantivy (v3.1.3); không dùng thêm container Tika/Gotenberg.",
        ),
    ]
    add_styled_table(
        doc,
        ["Dịch vụ / Vùng lưu trữ", "Khai báo trong docker-compose.yml", "Vai trò thực tế & Cách ánh xạ trên sơ đồ"],
        compose_rows,
    )
    doc.add_paragraph()

    add_figure(
        doc,
        "docs/images/so_do_kien_truc_container.png",
        "Hình 4.1. Kiến trúc triển khai thực tế của Paperless-ngx v3.1.3 trên Docker Compose gồm ba container (paperless-webserver, paperless-db, paperless-broker), các tiến trình nội bộ dưới s6-overlay và các vùng lưu trữ dữ liệu.",
    )
    add_figure(
        doc,
        "docs/images/so_do_luong_du_lieu.png",
        "Hình 4.2. Luồng dữ liệu của ba nghiệp vụ vận hành (tải lên và xử lý nền, tạo và gán thông tin phân loại, tìm kiếm và lọc) ánh xạ trực tiếp trên các dịch vụ Docker Compose và vùng lưu trữ.",
    )
    add_figure(
        doc,
        "docs/images/so_do_quan_he_du_lieu.png",
        "Hình 4.3. Sơ đồ quan hệ dữ liệu giữa tài liệu (Document) và các đối tượng phân loại (Tag, Correspondent, DocumentType) trong cơ sở dữ liệu PostgreSQL của Paperless-ngx v3.1.3.",
    )

    doc.add_page_break()

    # Phần 2: Bảng tổng hợp kết quả kiểm chứng 3 luồng vận hành
    h2 = doc.add_heading("2. Kết quả thực nghiệm và minh chứng ba luồng vận hành trên Paperless-ngx cục bộ", level=1)
    h2.runs[0].font.name = "Times New Roman"

    flow_rows = [
        (
            "Nền tảng &\nXác thực API",
            "3 container đã khởi chạy; tệp .env cấu hình cục bộ; dữ liệu cũ đã xóa sạch qua reset_data.py.",
            "Chạy docker compose ps; gọi GET /api/documents/ không token; gọi POST /api/token/ và GET /api/schema/.",
            "3 dịch vụ Up (webserver healthy); không token trả 401; có token trả 200 và schema 163 ops.",
            "3/3 dịch vụ Up (commit d48663e9); thiếu token trả HTTP 401; có token trả HTTP 200, OpenAPI 3.0.3 gồm 163 operations.",
        ),
        (
            "Luồng 1:\nTải lên & xử lý tài liệu",
            "Đã xác thực API; count_before = 0; chuẩn bị tệp chính Flow1_Invoice_ACME_Q4_2026.txt và tệp đối chứng.",
            "POST /api/documents/post_document/; theo dõi GET /api/tasks/?task_id=...; truy xuất GET /api/documents/8/ và /download/.",
            "Tiếp nhận trả 200 + Task UUID; xử lý nền đạt success; truy xuất được metadata, văn bản và tệp gốc.",
            "HTTP 200 + UUID 57b4f69e-...; sau 2,24s đạt status=success (document_id=8); GET /api/documents/8/ và /download/ đều trả HTTP 200 (247 bytes), nội dung khớp mã KTPM-R08-FLOW-ALPHA.",
        ),
        (
            "Luồng 2:\nGán thông tin phân loại",
            "Tài liệu ID=8 đã xử lý xong, các trường correspondent, document_type, tags đều đang rỗng.",
            "POST tạo Tag (ID=74), Correspondent (ID=117), DocumentType (ID=103); PATCH /api/documents/8/; GET truy vấn lại độc lập.",
            "Tạo mới trả 201; cập nhật trả 200; truy vấn lại xác nhận quan hệ đã lưu bền vững trong DB.",
            "3 yêu cầu POST trả HTTP 201; PATCH trả HTTP 200; truy vấn lại GET /api/documents/8/ xác nhận tags=[74], correspondent=117, document_type=103 và document_count=1.",
        ),
        (
            "Luồng 3:\nTìm kiếm & lọc tài liệu",
            "Có 2 tài liệu đối chứng biết trước quan hệ: ID=8 (ALPHA, Q4-2026, corr=117) và ID=9 (BETA, Q4-2026, corr=118).",
            "Tìm toàn văn ?query=KTPM-R08-FLOW-ALPHA; lọc đa tiêu chí tag+corr+type; kết hợp ?query=Q4-2026&correspondent__id=117.",
            "Trả HTTP 200, thu nhận đúng tài liệu ID=8 và loại trừ chính xác tài liệu đối chứng ID=9.",
            "Tìm ALPHA trả count=1 (ID=8, score=1,904); lọc đa tiêu chí trả count=1 (ID=8); truy vấn chung Q4-2026 trả 2 tài liệu [9, 8] và thu hẹp đúng còn [8] khi kết hợp lọc correspondent=117.",
        ),
    ]
    add_styled_table(
        doc,
        ["Luồng kiểm tra", "Điều kiện ban đầu", "Thao tác thực hiện", "Kết quả mong đợi", "Kết quả quan sát thực tế"],
        flow_rows,
    )
    doc.add_paragraph()

    # Phần 3: Ảnh chụp giao diện kèm chú thích
    h3 = doc.add_heading("3. Hình ảnh minh chứng giao diện (đã che thông tin nhạy cảm) kèm chú thích", level=1)
    h3.runs[0].font.name = "Times New Roman"

    ui_figs = [
        (
            "docs/evidence/images/01_webui_login_screen.png",
            "Hình 4.4. Màn hình đăng nhập giao diện web Paperless-ngx tại địa chỉ http://localhost:8000.",
        ),
        (
            "docs/evidence/images/02_openapi_schema_view.png",
            "Hình 4.5. Giao diện tài liệu đặc tả OpenAPI 3.0.3 (Paperless-ngx REST API 6.0.0 (10)) truy cập tại /api/schema/view/.",
        ),
        (
            "docs/evidence/images/03_flow1_tasks_completed.png",
            "Hình 4.6. Minh chứng Luồng 1 trên giao diện Tasks: tác vụ tiếp nhận và xử lý tệp tải lên qua API đã hoàn tất (Recently completed) và sẵn sàng mở tài liệu.",
        ),
        (
            "docs/evidence/images/04_flow2_document_metadata_assigned.png",
            "Hình 4.7. Minh chứng Luồng 2 trên màn hình chi tiết tài liệu (ID 8): thông tin Correspondent, Document type, Tag và nội dung văn bản trích xuất hiển thị sau khi gán.",
        ),
        (
            "docs/evidence/images/05_flow3_search_and_filter_result.png",
            "Hình 4.8. Minh chứng Luồng 3 trên giao diện Documents: tìm kiếm nội dung văn bản trả về đúng một tài liệu khớp điều kiện (One document (filtered)).",
        ),
    ]
    for path, cap in ui_figs:
        add_figure(doc, path, cap, width_in=6.0)

    out_file = Path("docs/TV4_MINH_CHUNG_VA_SO_DO_CHUONG4.docx")
    doc.save(str(out_file))
    print(f"[OK] Đã xuất tài liệu Word bàn giao Chương 4: {out_file}")


if __name__ == "__main__":
    build_docx()
