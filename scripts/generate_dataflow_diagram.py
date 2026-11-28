#!/usr/bin/env python3
"""
scripts/generate_dataflow_diagram.py
Vẽ sơ đồ luồng dữ liệu của 3 luồng nghiệp vụ vận hành gắn trực tiếp với các dịch vụ Docker Compose:
  - Luồng 1: Tải lên và xử lý tài liệu bất đồng bộ (tách rõ thời điểm tiếp nhận & thời điểm hoàn tất + truy xuất).
  - Luồng 2: Tạo thông tin phân loại (Tag, Correspondent, DocumentType) và gán cho tài liệu (kèm truy vấn lại).
  - Luồng 3: Tìm kiếm toàn văn (Tantivy) và lọc đa tiêu chí trên PostgreSQL.

Xuất ảnh 300 DPI PNG và vector SVG tại:
  - docs/images/so_do_luong_du_lieu.png
  - docs/images/so_do_luong_du_lieu.svg
Phục vụ chèn trực tiếp vào Chương 4 báo cáo cuối kỳ (TV4 - Nguyễn Nhất Minh).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "Tahoma", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def draw_dataflow() -> None:
    output_dir = Path("docs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "so_do_luong_du_lieu.png"
    svg_path = output_dir / "so_do_luong_du_lieu.svg"

    fig, ax = plt.subplots(figsize=(16.5, 11.2), dpi=300)
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 16.5)
    ax.set_ylim(0, 11.2)
    ax.axis("off")

    # ==================== TIÊU ĐỀ ====================
    ax.text(
        8.25,
        10.78,
        "SƠ ĐỒ LUỒNG DỮ LIỆU BA NGHIỆP VỤ VẬN HÀNH TRÊN CẤU HÌNH DOCKER COMPOSE",
        fontsize=15.5,
        fontweight="bold",
        ha="center",
        va="center",
        color="#0F172A",
    )
    ax.text(
        8.25,
        10.42,
        "Ánh xạ trực tiếp giữa REST API, tiến trình trong webserver, hàng đợi broker (Redis), db (PostgreSQL) và các Docker Volumes",
        fontsize=10.3,
        fontstyle="italic",
        ha="center",
        va="center",
        color="#475569",
    )

    # ==================== CÁC CỘT THÀNH PHẦN (SWIMLANE COLUMNS) ====================
    cols = [
        (1.65, 2.30, "Client / UI / Script", "Host (:8000)", "#1D4ED8", "#EFF6FF"),
        (4.85, 2.50, "webserver: svc-webserver", "Granian + DRF API", "#2563EB", "#EFF6FF"),
        (8.05, 2.30, "broker (Redis 7)", "redis://broker:6379", "#DC2626", "#FEF2F2"),
        (11.25, 2.50, "webserver: svc-worker", "Celery + OCRmyPDF", "#D97706", "#FFFBEB"),
        (14.65, 2.70, "db (Postgres) & Volumes", "db:5432 · media · data", "#0F766E", "#F0FDFA"),
    ]

    for cx, cw, title, sub, edge, bg in cols:
        hdr = patches.FancyBboxPatch(
            (cx - cw / 2, 9.35),
            cw,
            0.78,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=1.8,
            edgecolor=edge,
            facecolor=bg,
        )
        ax.add_patch(hdr)
        ax.text(cx, 9.85, title, fontsize=9.6, fontweight="bold", ha="center", color=edge)
        ax.text(cx, 9.53, sub, fontsize=8.1, ha="center", color="#475569")
        # Đường lifeline dọc
        ax.plot([cx, cx], [0.45, 9.35], linestyle="--", linewidth=1.2, color="#CBD5E1", zorder=1)

    c1, c2, c3, c4, c5 = [c[0] for c in cols]

    def draw_band(y_bottom, height, band_title, band_sub, border_col, fill_col):
        band = patches.FancyBboxPatch(
            (0.30, y_bottom),
            15.90,
            height,
            boxstyle="round,pad=0.04,rounding_size=0.14",
            linewidth=1.5,
            edgecolor=border_col,
            facecolor=fill_col,
            zorder=0,
        )
        ax.add_patch(band)
        badge = patches.FancyBboxPatch(
            (0.45, y_bottom + height - 0.44),
            6.80,
            0.34,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            linewidth=0,
            facecolor=border_col,
            zorder=2,
        )
        ax.add_patch(badge)
        ax.text(0.60, y_bottom + height - 0.27, band_title, fontsize=9.3, fontweight="bold", va="center", color="#FFFFFF", zorder=3)
        ax.text(7.45, y_bottom + height - 0.27, band_sub, fontsize=8.4, fontstyle="italic", va="center", color="#334155", zorder=3)

    def step_arrow(x_from, x_to, y, label, col="#1E293B", dashed=False):
        ls = "--" if dashed else "-"
        ax.annotate(
            "",
            xy=(x_to, y),
            xytext=(x_from, y),
            arrowprops=dict(arrowstyle="->", lw=1.8, linestyle=ls, color=col),
            zorder=4,
        )
        mid = (x_from + x_to) / 2
        ax.text(
            mid,
            y + 0.14,
            label,
            fontsize=8.0,
            fontweight="bold",
            ha="center",
            va="bottom",
            color=col,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=0.6),
            zorder=5,
        )

    # ==================== LUỒNG 1: TẢI LÊN & XỬ LÝ TÀI LIỆU ====================
    draw_band(
        5.85,
        3.30,
        "LUỒNG 1: TẢI LÊN VÀ XỬ LÝ TÀI LIỆU BẤT ĐỒNG BỘ",
        "Tách rõ thời điểm tiếp nhận HTTP (200 + Task UUID) và thời điểm xử lý nền hoàn tất (status=success + truy xuất tài liệu)",
        "#2563EB",
        "#F8FAFC",
    )

    step_arrow(c1, c2, 8.38, "(1.1) POST /api/documents/post_document/ (multipart file + Token)", "#1D4ED8")
    step_arrow(c2, c3, 7.98, "(1.2) Ghi tạm scratch & đẩy job consume_file.delay()", "#DC2626")
    step_arrow(c2, c1, 7.58, "(1.3) Phản hồi tức thì HTTP 200 OK + Task UUID", "#1D4ED8", dashed=True)
    step_arrow(c3, c4, 7.18, "(1.4) Phân phối tác vụ nền từ hàng đợi Redis", "#D97706")
    step_arrow(c4, c5, 6.76, "(1.5) OCR/trích xuất chữ → INSERT db + lưu volume:media + chỉ mục Tantivy (volume:data)", "#0F766E")
    step_arrow(c1, c2, 6.32, "(1.6) GET /api/tasks/?task_id=... (status=success) & GET /api/documents/{id}/", "#1E40AF")
    step_arrow(c5, c1, 5.96, "(1.7) Đọc từ db & volume:media → HTTP 200 OK (JSON tài liệu + nội dung + tệp gốc)", "#0F766E", dashed=True)

    # ==================== LUỒNG 2: TẠO & GÁN THÔNG TIN PHÂN LOẠI ====================
    draw_band(
        3.15,
        2.50,
        "LUỒNG 2: TẠO THÔNG TIN PHÂN LOẠI VÀ GÁN CHO TÀI LIỆU",
        "Tạo Tag, Correspondent, DocumentType (201), cập nhật liên kết trên tài liệu (PATCH 200) và truy vấn lại độc lập",
        "#7C3AED",
        "#FCF8FF",
    )

    step_arrow(c1, c2, 4.92, "(2.1) POST /api/tags/ · /api/correspondents/ · /api/document_types/", "#6D28D9")
    step_arrow(c2, c5, 4.52, "(2.2) Validate (name<=128, unique) → INSERT bảng phân loại tại db:5432 → trả ID (201)", "#0F766E")
    step_arrow(c1, c2, 4.10, "(2.3) PATCH /api/documents/{id}/ {tags, correspondent, document_type}", "#6D28D9")
    step_arrow(c2, c5, 3.70, "(2.4) UPDATE khóa ngoại & bảng N:M tại db:5432 + đồng bộ chỉ mục Tantivy (volume:data)", "#0F766E")
    step_arrow(c1, c5, 3.30, "(2.5) Truy vấn lại độc lập GET /api/documents/{id}/ → xác nhận lưu bền vững (HTTP 200)", "#4C1D95", dashed=True)

    # ==================== LUỒNG 3: TÌM KIẾM VÀ LỌC TÀI LIỆU ====================
    draw_band(
        0.50,
        2.45,
        "LUỒNG 3: TÌM KIẾM TOÀN VĂN VÀ LỌC ĐA TIÊU CHÍ",
        "Kết hợp tra cứu chỉ mục toàn văn Tantivy (volume:data) và lọc quan hệ metadata trên PostgreSQL (db:5432)",
        "#0D9488",
        "#F0FDFA",
    )

    step_arrow(c1, c2, 2.22, "(3.1) GET /api/documents/?query=...&tags__id__all=...&correspondent__id=...", "#0F766E")
    step_arrow(c2, c5, 1.76, "(3.2) Tra cứu chỉ mục Tantivy (volume:data) lấy danh sách ID & điểm xếp hạng (score)", "#0D9488")
    step_arrow(c2, c5, 1.28, "(3.3) Kết hợp lọc khóa ngoại, kiểm tra quyền (Guardian) & phân trang trên db:5432", "#115E59")
    step_arrow(c2, c1, 0.78, "(3.4) HTTP 200 OK {count, results, __search_hit__} (khớp đúng tập dữ liệu mẫu)", "#0F766E", dashed=True)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.savefig(svg_path, format="svg", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Đã xuất sơ đồ luồng dữ liệu 3 nghiệp vụ: {png_path} & {svg_path}")


if __name__ == "__main__":
    draw_dataflow()
