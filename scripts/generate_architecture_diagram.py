#!/usr/bin/env python3
"""
scripts/generate_architecture_diagram.py
Vẽ sơ đồ kiến trúc triển khai Container hệ thống Paperless-ngx v3.1.3 đối chiếu 1-1 với docker-compose.yml.
Xuất ảnh 300 DPI PNG và vector SVG tại:
  - docs/images/so_do_kien_truc_container.png
  - docs/images/so_do_kien_truc_container.svg
Phục vụ chèn trực tiếp vào Chương 4 báo cáo cuối kỳ (Nhóm 17 - Đề tài R08 + K05).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "Tahoma", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def draw_diagram() -> None:
    output_dir = Path("docs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "so_do_kien_truc_container.png"
    svg_path = output_dir / "so_do_kien_truc_container.svg"

    fig, ax = plt.subplots(figsize=(16.5, 10.2), dpi=300)
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 16.5)
    ax.set_ylim(0, 10.2)
    ax.axis("off")

    # ==================== TIÊU ĐỀ ====================
    ax.text(
        8.25,
        9.78,
        "SƠ ĐỒ KIẾN TRÚC TRIỂN KHAI CONTAINER PAPERLESS-NGX (DOCKER COMPOSE)",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="center",
        color="#0F172A",
    )
    ax.text(
        8.25,
        9.40,
        "Đối chiếu trực tiếp từ docker-compose.yml · Image ghcr.io/paperless-ngx/paperless-ngx:3.1.3 (commit d48663e9)",
        fontsize=10.8,
        fontstyle="italic",
        ha="center",
        va="center",
        color="#475569",
    )

    # ==================== KHỐI 1: TÁC NHÂN BÊN NGOÀI (HOST CLIENTS) ====================
    box_client = patches.FancyBboxPatch(
        (0.35, 0.55),
        3.15,
        8.45,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        linewidth=1.6,
        edgecolor="#64748B",
        facecolor="#FFFFFF",
        linestyle="--",
    )
    ax.add_patch(box_client)
    ax.text(1.92, 8.73, "TÁC NHÂN BÊN NGOÀI (HOST)", fontsize=11, fontweight="bold", ha="center", color="#1E293B")

    # 1.1 Web Browser
    c_ui = patches.FancyBboxPatch(
        (0.55, 6.45),
        2.75,
        1.95,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.5,
        edgecolor="#2563EB",
        facecolor="#EFF6FF",
    )
    ax.add_patch(c_ui)
    ax.text(1.92, 8.12, "Trình duyệt Web (Người dùng)", fontsize=10.2, fontweight="bold", ha="center", color="#1D4ED8")
    ax.text(1.92, 7.80, "Giao diện Angular SPA", fontsize=9, fontweight="bold", ha="center", color="#2563EB")
    ax.text(
        1.92,
        7.25,
        "• Tải lên & xem trạng thái xử lý\n• Gán Tag, Correspondent, Type\n• Tìm kiếm & lọc trực quan",
        fontsize=8.3,
        ha="center",
        va="center",
        color="#334155",
    )
    ax.text(
        1.92,
        6.68,
        "http://localhost:8000",
        fontsize=8.2,
        fontweight="bold",
        ha="center",
        color="#1E40AF",
        bbox=dict(boxstyle="round,pad=0.18", facecolor="#DBEAFE", edgecolor="#93C5FD", lw=0.8),
    )

    # 1.2 Schemathesis CLI
    c_st = patches.FancyBboxPatch(
        (0.55, 3.55),
        2.75,
        2.55,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.5,
        edgecolor="#9333EA",
        facecolor="#FAF5FF",
    )
    ax.add_patch(c_st)
    ax.text(1.92, 5.82, "Schemathesis CLI v4.30.1", fontsize=10.2, fontweight="bold", ha="center", color="#7E22CE")
    ax.text(1.92, 5.50, "Kỹ thuật K05 (Schema-Based / Fuzz)", fontsize=8.7, fontweight="bold", ha="center", color="#9333EA")
    ax.text(
        1.92,
        4.70,
        "• Đọc đặc tả /api/schema/ (OAS 3.0.3)\n• Seeds: 101, 202, 303, 404, 505\n• V1: 19 GET | V2: 18 CRUD | V3: 53 ops\n• Kiểm tra 5xx & tuân thủ Schema",
        fontsize=8.2,
        ha="center",
        va="center",
        color="#334155",
    )
    ax.text(
        1.92,
        3.82,
        "Header: Token <REDACTED>",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        color="#6B21A8",
        bbox=dict(boxstyle="round,pad=0.18", facecolor="#F3E8FF", edgecolor="#D8B4FE", lw=0.8),
    )

    # 1.3 Python Scripts / cURL / OpenAPI UI
    c_sc = patches.FancyBboxPatch(
        (0.55, 0.85),
        2.75,
        2.35,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.5,
        edgecolor="#059669",
        facecolor="#ECFDF5",
    )
    ax.add_patch(c_sc)
    ax.text(1.92, 2.92, "Scripts Kiểm thử & Demo", fontsize=10.2, fontweight="bold", ha="center", color="#047857")
    ax.text(1.92, 2.60, "Python requests / OpenAPI View", fontsize=8.8, fontweight="bold", ha="center", color="#059669")
    ax.text(
        1.92,
        1.90,
        "• demo_system.py (3 luồng vận hành)\n• seed_data.py & reset_data.py\n• run_manual_tests.py (EP / BVA)",
        fontsize=8.2,
        ha="center",
        va="center",
        color="#334155",
    )
    ax.text(
        1.92,
        1.12,
        "/api/schema/ · /api/schema/view/",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        color="#065F46",
        bbox=dict(boxstyle="round,pad=0.18", facecolor="#D1FAE5", edgecolor="#6EE7B7", lw=0.8),
    )

    # ==================== KHỐI 2: MẠNG NỘI BỘ DOCKER COMPOSE ====================
    box_net = patches.FancyBboxPatch(
        (4.35, 0.55),
        7.55,
        8.45,
        boxstyle="round,pad=0.08,rounding_size=0.22",
        linewidth=2.2,
        edgecolor="#0284C7",
        facecolor="#FFFFFF",
    )
    ax.add_patch(box_net)
    ax.text(
        8.12,
        8.73,
        "MẠNG NỘI BỘ DOCKER COMPOSE (Bridge: ktpm_default)",
        fontsize=11.5,
        fontweight="bold",
        ha="center",
        color="#0369A1",
    )

    # --- Service 1: webserver (Top half) ---
    c_web = patches.FancyBboxPatch(
        (4.60, 4.65),
        7.05,
        3.80,
        boxstyle="round,pad=0.06,rounding_size=0.16",
        linewidth=1.9,
        edgecolor="#2563EB",
        facecolor="#F8FAFC",
    )
    ax.add_patch(c_web)
    ax.text(4.78, 8.18, "Service: webserver (paperless-webserver)", fontsize=10.8, fontweight="bold", color="#1E3A8A")
    ax.text(11.48, 8.18, "ports: \"8000:8000\" · /init (s6-overlay)", fontsize=8.6, fontweight="bold", ha="right", color="#1D4ED8")
    ax.text(
        4.78,
        7.88,
        "image: ghcr.io/paperless-ngx/paperless-ngx:3.1.3  |  depends_on: [db, broker]",
        fontsize=8.3,
        color="#475569",
    )

    # Sub-process 1: svc-webserver
    sub_drf = patches.FancyBboxPatch(
        (4.78, 5.68),
        3.28,
        1.98,
        boxstyle="round,pad=0.05,rounding_size=0.10",
        linewidth=1.3,
        edgecolor="#93C5FD",
        facecolor="#FFFFFF",
    )
    ax.add_patch(sub_drf)
    ax.text(6.42, 7.42, "svc-webserver (Granian :8000)", fontsize=9.5, fontweight="bold", ha="center", color="#1E40AF")
    ax.text(
        6.42,
        6.50,
        "• Phục vụ Angular UI & REST API\n• Django + DRF ViewSets & Serializers\n• drf-spectacular (/api/schema/)\n• Xác thực Token & phân quyền Guardian",
        fontsize=8.1,
        ha="center",
        va="center",
        color="#334155",
    )

    # Sub-process 2: svc-worker & svc-scheduler
    sub_wk = patches.FancyBboxPatch(
        (8.22, 5.68),
        3.25,
        1.98,
        boxstyle="round,pad=0.05,rounding_size=0.10",
        linewidth=1.3,
        edgecolor="#FBBF24",
        facecolor="#FFFBEB",
    )
    ax.add_patch(sub_wk)
    ax.text(9.84, 7.42, "svc-worker & svc-scheduler", fontsize=9.5, fontweight="bold", ha="center", color="#B45309")
    ax.text(
        9.84,
        6.50,
        "• Celery Worker nhận task consume_file\n• OCRmyPDF + Tesseract trích xuất chữ\n• Sinh ảnh thu nhỏ & lưu tệp lưu trữ\n• Celery Beat lập lịch tác vụ định kỳ",
        fontsize=8.1,
        ha="center",
        va="center",
        color="#334155",
    )

    # Sub-process 3: Tantivy + svc-consumer
    sub_idx = patches.FancyBboxPatch(
        (4.78, 4.82),
        6.69,
        0.66,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        linewidth=1.1,
        edgecolor="#CBD5E1",
        facecolor="#F1F5F9",
    )
    ax.add_patch(sub_idx)
    ax.text(
        8.12,
        5.15,
        "Tantivy Full-Text Search Engine (lập chỉ mục & xếp hạng điểm tìm kiếm)  ·  svc-consumer (theo dõi thư mục /consume)",
        fontsize=8.2,
        fontweight="bold",
        ha="center",
        va="center",
        color="#334155",
    )

    # --- Service 2: db (Middle-left, aligned with pgdata on right!) ---
    c_db = patches.FancyBboxPatch(
        (4.60, 2.55),
        3.35,
        1.65,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.8,
        edgecolor="#0D9488",
        facecolor="#F0FDF4",
    )
    ax.add_patch(c_db)
    ax.text(6.27, 3.95, "Service: db (paperless-db)", fontsize=10.0, fontweight="bold", ha="center", color="#0F766E")
    ax.text(6.27, 3.68, "postgres:16-alpine · Nội bộ 5432/tcp", fontsize=8.2, fontweight="bold", ha="center", color="#115E59")
    ax.text(
        6.27,
        3.08,
        "Lưu metadata có cấu trúc: documents_document,\ntags, correspondents, document_types, auth_user\n(Không mở cổng ra Host — cô lập trong mạng nội bộ)",
        fontsize=7.9,
        ha="center",
        va="center",
        color="#334155",
    )

    # --- Service 3: broker (Bottom-right, aligned with redisdata on right!) ---
    c_br = patches.FancyBboxPatch(
        (8.30, 0.80),
        3.35,
        1.65,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.8,
        edgecolor="#EF4444",
        facecolor="#FEF2F2",
    )
    ax.add_patch(c_br)
    ax.text(9.97, 2.20, "Service: broker (paperless-broker)", fontsize=10.0, fontweight="bold", ha="center", color="#B91C1C")
    ax.text(9.97, 1.93, "redis:7-alpine · Nội bộ 6379/tcp", fontsize=8.2, fontweight="bold", ha="center", color="#991B1B")
    ax.text(
        9.97,
        1.33,
        "PAPERLESS_REDIS=redis://broker:6379\nHàng đợi tác vụ Celery & bộ nhớ đệm trạng thái\n(Không mở cổng ra Host — truyền thông nội bộ)",
        fontsize=7.9,
        ha="center",
        va="center",
        color="#334155",
    )

    # Ghi chú cấu hình thực tế ở góc dưới trái mạng Docker
    note_cfg = patches.FancyBboxPatch(
        (4.60, 0.80),
        3.35,
        1.45,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        linewidth=1.2,
        edgecolor="#CBD5E1",
        facecolor="#F8FAFC",
    )
    ax.add_patch(note_cfg)
    ax.text(6.27, 2.02, "Ghi chú đối chiếu Compose", fontsize=9.0, fontweight="bold", ha="center", color="#1E293B")
    ax.text(
        6.27,
        1.38,
        "• Tổng cộng đúng 3 containers chạy thực tế\n• PAPERLESS_TIKA_ENABLED=0 (không dùng\n  container Tika / Gotenberg phụ trợ)\n• DBHOST=db · REDIS=redis://broker:6379",
        fontsize=7.8,
        ha="center",
        va="center",
        color="#475569",
    )

    # ==================== KHỐI 3: VOLUMES & BIND MOUNTS ====================
    box_vol = patches.FancyBboxPatch(
        (12.55, 0.55),
        3.60,
        8.45,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        linewidth=1.6,
        edgecolor="#64748B",
        facecolor="#FFFFFF",
    )
    ax.add_patch(box_vol)
    ax.text(14.35, 8.73, "VÙNG LƯU TRỮ & CẤU HÌNH", fontsize=11, fontweight="bold", ha="center", color="#1E293B")

    def draw_vol(y, h, title, mount_str, desc, edge, bg, title_col):
        vbox = patches.FancyBboxPatch(
            (12.75, y),
            3.20,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.10",
            linewidth=1.3,
            edgecolor=edge,
            facecolor=bg,
        )
        ax.add_patch(vbox)
        ax.text(12.90, y + h - 0.24, title, fontsize=9.2, fontweight="bold", color=title_col)
        ax.text(12.90, y + h - 0.47, mount_str, fontsize=7.8, fontstyle="italic", color="#475569")
        ax.text(12.90, y + 0.30, desc, fontsize=7.9, va="center", color="#334155")

    draw_vol(
        7.15,
        1.25,
        "Named Volume: media",
        "→ /usr/src/paperless/media",
        "Tệp gốc (originals/), bản lưu trữ OCR\n(archive/) và ảnh thu nhỏ (thumbnails/)",
        "#60A5FA",
        "#EFF6FF",
        "#1E3A8A",
    )
    draw_vol(
        5.70,
        1.25,
        "Named Volume: data",
        "→ /usr/src/paperless/data",
        "Chỉ mục tìm kiếm toàn văn Tantivy,\ndữ liệu mô hình phân loại nội bộ",
        "#94A3B8",
        "#F8FAFC",
        "#1E293B",
    )
    draw_vol(
        4.15,
        1.35,
        "Bind Mounts & env_file (Host)",
        "./consume · ./export · .env",
        "• ./consume → /usr/src/paperless/consume\n• ./export  → /usr/src/paperless/export\n• env_file: .env (biến môi trường & khóa)",
        "#F59E0B",
        "#FFFBEB",
        "#92400E",
    )
    draw_vol(
        2.60,
        1.25,
        "Named Volume: pgdata",
        "→ /var/lib/postgresql/data",
        "Lưu trữ bền vững toàn bộ dữ liệu bảng\nvà chỉ mục quan hệ của PostgreSQL 16",
        "#2DD4BF",
        "#F0FDFA",
        "#0F766E",
    )
    draw_vol(
        0.85,
        1.25,
        "Named Volume: redisdata",
        "→ /data (Redis persistence)",
        "Lưu trạng thái hàng đợi và snapshot\nRedis khi khởi động lại dịch vụ",
        "#FCA5A5",
        "#FEF2F2",
        "#B91C1C",
    )

    # ==================== MŨI TÊN KẾT NỐI KHÔNG CHỒNG LẤP ====================
    # Clients -> webserver (:8000)
    ax.annotate("", xy=(4.60, 7.35), xytext=(3.30, 7.35), arrowprops=dict(arrowstyle="->", lw=2.0, color="#2563EB"))
    ax.text(
        3.93,
        7.58,
        "HTTP :8000",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        color="#1E40AF",
        bbox=dict(boxstyle="round,pad=0.14", facecolor="#FFFFFF", edgecolor="#93C5FD", lw=0.7),
    )

    ax.annotate("", xy=(4.60, 6.50), xytext=(3.30, 4.95), arrowprops=dict(arrowstyle="->", lw=2.0, color="#9333EA"))
    ax.text(
        3.92,
        5.95,
        "REST API\n(:8000)",
        fontsize=7.8,
        fontweight="bold",
        ha="center",
        color="#6B21A8",
        bbox=dict(boxstyle="round,pad=0.14", facecolor="#FFFFFF", edgecolor="#D8B4FE", lw=0.7),
    )

    ax.annotate("", xy=(4.60, 5.95), xytext=(3.30, 2.25), arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669"))

    # webserver <-> db (5432) — thẳng đứng bên trái, hoàn toàn sạch!
    ax.annotate("", xy=(6.27, 4.20), xytext=(6.27, 4.65), arrowprops=dict(arrowstyle="<->", lw=2.1, color="#0D9488"))
    ax.text(
        6.27,
        4.42,
        "SQL :5432",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        va="center",
        color="#0F766E",
        bbox=dict(boxstyle="round,pad=0.14", facecolor="#FFFFFF", edgecolor="#5EEAD4", lw=0.8),
    )

    # webserver <-> broker (6379) — thẳng đứng bên phải, hoàn toàn sạch!
    ax.annotate("", xy=(9.97, 2.45), xytext=(9.97, 4.65), arrowprops=dict(arrowstyle="<->", lw=2.1, color="#EF4444"))
    ax.text(
        9.97,
        3.55,
        "Celery Queue\nRedis :6379",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        va="center",
        color="#B91C1C",
        bbox=dict(boxstyle="round,pad=0.16", facecolor="#FFFFFF", edgecolor="#FCA5A5", lw=0.8),
    )

    # webserver -> media, data, bind mounts (ngang sang phải)
    ax.annotate("", xy=(12.75, 7.75), xytext=(11.65, 7.75), arrowprops=dict(arrowstyle="->", lw=1.7, ls="--", color="#2563EB"))
    ax.annotate("", xy=(12.75, 6.30), xytext=(11.65, 6.30), arrowprops=dict(arrowstyle="->", lw=1.7, ls="--", color="#475569"))
    ax.annotate("", xy=(12.75, 4.95), xytext=(11.65, 4.95), arrowprops=dict(arrowstyle="->", lw=1.7, ls="--", color="#D97706"))
    ax.text(12.20, 8.00, "Mount", fontsize=7.8, fontweight="bold", ha="center", color="#475569")

    # db -> pgdata (đi ngang ở y=3.22 phía trên broker y<=2.45 — KHÔNG cắt qua broker!)
    ax.annotate("", xy=(12.75, 3.22), xytext=(7.95, 3.22), arrowprops=dict(arrowstyle="->", lw=1.7, ls="--", color="#0D9488"))
    ax.text(
        11.20,
        3.40,
        "volume: pgdata",
        fontsize=7.6,
        fontweight="bold",
        ha="center",
        color="#0F766E",
        bbox=dict(boxstyle="round,pad=0.12", facecolor="#FFFFFF", edgecolor="#99F6E4", lw=0.6),
    )

    # broker -> redisdata (đi ngang ở y=1.48)
    ax.annotate("", xy=(12.75, 1.48), xytext=(11.65, 1.48), arrowprops=dict(arrowstyle="->", lw=1.7, ls="--", color="#EF4444"))

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.savefig(svg_path, format="svg", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Đã xuất sơ đồ kiến trúc container: {png_path} & {svg_path}")


if __name__ == "__main__":
    draw_diagram()
