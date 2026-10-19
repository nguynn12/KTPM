#!/usr/bin/env python3
"""
scripts/generate_architecture_diagram.py
Vẽ sơ đồ kiến trúc container hệ thống Paperless-ngx (Docker Compose)
Xuất ra file ảnh PNG chất lượng cao: docs/images/so_do_kien_truc_container.png
Phục vụ chèn vào Hình 1 của Báo cáo kiểm thử phần mềm (Nhóm 17 - Đề tài R08 + K05)
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Cấu hình font và hỗ trợ tiếng Việt
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

def draw_diagram():
    output_dir = Path("docs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "so_do_kien_truc_container.png"

    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # ==================== TIÊU ĐỀ ====================
    ax.text(8.0, 9.6, "HÌNH 1: SƠ ĐỒ KIẾN TRÚC CONTAINER HỆ THỐNG PAPERLESS-NGX", 
            fontsize=17, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(8.0, 9.2, "Môi trường Docker Compose (3 Services) · Đề tài R08 + K05 · Kiểm thử API tự động với Schemathesis", 
            fontsize=11.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # ==================== KHỐI 1: CLIENTS & KIỂM THỬ ====================
    # Khung bao Clients
    box_client = patches.FancyBboxPatch((0.5, 0.8), 3.2, 7.9,
                                        boxstyle="round,pad=0.1,rounding_size=0.2",
                                        linewidth=1.8, edgecolor='#94A3B8', facecolor='#FFFFFF', linestyle='--')
    ax.add_patch(box_client)
    ax.text(2.1, 8.4, "CLIENTS & KIỂM THỬ", fontsize=12, fontweight='bold', ha='center', color='#334155')

    # 1.1 Web Browser
    card_browser = patches.FancyBboxPatch((0.7, 6.2), 2.8, 1.9,
                                          boxstyle="round,pad=0.08,rounding_size=0.15",
                                          linewidth=1.5, edgecolor='#3B82F6', facecolor='#EFF6FF')
    ax.add_patch(card_browser)
    ax.text(2.1, 7.8, "Trình duyệt Web (UI)", fontsize=11, fontweight='bold', ha='center', color='#1D4ED8')
    ax.text(2.1, 7.4, "Angular Single Page App", fontsize=9.5, fontweight='bold', ha='center', color='#2563EB')
    ax.text(2.1, 6.9, "• Quản lý tài liệu, nhãn\n• Tìm kiếm & lọc trực quan\n• Upload hóa đơn/hợp đồng", 
            fontsize=8.5, ha='center', va='center', color='#334155')
    ax.text(2.1, 6.4, "http://localhost:8000", fontsize=8.5, fontweight='bold', ha='center', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DBEAFE', edgecolor='#93C5FD', lw=0.8))

    # 1.2 Schemathesis QA
    card_st = patches.FancyBboxPatch((0.7, 3.5), 2.8, 2.4,
                                     boxstyle="round,pad=0.08,rounding_size=0.15",
                                     linewidth=1.5, edgecolor='#A855F7', facecolor='#FAF5FF')
    ax.add_patch(card_st)
    ax.text(2.1, 5.6, "Schemathesis (QA Engine)", fontsize=11, fontweight='bold', ha='center', color='#7E22CE')
    ax.text(2.1, 5.2, "Kiểm thử API Fuzzing Tự Động", fontsize=9.5, fontweight='bold', ha='center', color='#9333EA')
    ax.text(2.1, 4.5, "• TV4 (Nguyễn Nhất Minh - Seed 404)\n• V1: GET-only (19 operations)\n• V2: CRUD Metadata (18 operations)\n• V3: All Checks (53 operations)", 
            fontsize=8.5, ha='center', va='center', color='#334155')
    ax.text(2.1, 3.75, "Token Auth: Token [Filtered]", fontsize=8.2, fontweight='bold', ha='center', color='#6B21A8',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F3E8FF', edgecolor='#D8B4FE', lw=0.8))

    # 1.3 Swagger UI / cURL
    card_curl = patches.FancyBboxPatch((0.7, 1.1), 2.8, 2.1,
                                       boxstyle="round,pad=0.08,rounding_size=0.15",
                                       linewidth=1.5, edgecolor='#10B981', facecolor='#ECFDF5')
    ax.add_patch(card_curl)
    ax.text(2.1, 2.9, "Swagger UI / cURL / Scripts", fontsize=10.5, fontweight='bold', ha='center', color='#047857')
    ax.text(2.1, 2.5, "Đặc tả OpenAPI v3.0.3", fontsize=9, fontweight='bold', ha='center', color='#059669')
    ax.text(2.1, 1.9, "• Tra cứu 163 operations\n• Tái hiện BUG-01 đến BUG-06\n• 18 Manual TCs (run_manual_tests.py)", 
            fontsize=8.5, ha='center', va='center', color='#334155')
    ax.text(2.1, 1.35, "http://localhost:8000/api/schema/", fontsize=8, fontweight='bold', ha='center', color='#065F46',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#D1FAE5', edgecolor='#6EE7B7', lw=0.8))

    # ==================== KHỐI 2: DOCKER COMPOSE NETWORK ====================
    box_docker = patches.FancyBboxPatch((4.1, 0.8), 7.8, 7.9,
                                        boxstyle="round,pad=0.1,rounding_size=0.25",
                                        linewidth=2.2, edgecolor='#0284C7', facecolor='#FFFFFF')
    ax.add_patch(box_docker)
    ax.text(8.0, 8.4, "DOCKER COMPOSE NETWORK (Mạng nội bộ: ktpm_default)", 
            fontsize=12.5, fontweight='bold', ha='center', color='#0369A1')

    # CONTAINER 1: paperless-webserver
    c1_box = patches.FancyBboxPatch((4.4, 4.4), 7.2, 3.65,
                                    boxstyle="round,pad=0.08,rounding_size=0.18",
                                    linewidth=1.8, edgecolor='#2563EB', facecolor='#F8FAFC')
    ax.add_patch(c1_box)
    ax.text(4.6, 7.75, "Container 1: paperless-webserver", fontsize=11.5, fontweight='bold', color='#1E3A8A')
    ax.text(11.4, 7.75, "ghcr.io/paperless-ngx/paperless-ngx:3.1.3 (Port 8000)", fontsize=9, ha='right', color='#1D4ED8')

    # Sub-component: Django REST API
    sub_api = patches.FancyBboxPatch((4.6, 5.5), 3.3, 2.0,
                                     boxstyle="round,pad=0.05,rounding_size=0.1",
                                     linewidth=1.2, edgecolor='#93C5FD', facecolor='#FFFFFF')
    ax.add_patch(sub_api)
    ax.text(6.25, 7.2, "Django REST Framework (DRF)", fontsize=10, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(6.25, 6.35, "• Quản lý API & Xác thực\n• ViewSets: Tag, Corr, Doc, Type\n• Serializers & Validation\n• Sinh OpenAPI Schema tự động", 
            fontsize=8.3, ha='center', va='center', color='#334155')

    # Sub-component: Celery Worker & OCR
    sub_worker = patches.FancyBboxPatch((8.1, 5.5), 3.3, 2.0,
                                        boxstyle="round,pad=0.05,rounding_size=0.1",
                                        linewidth=1.2, edgecolor='#FBBF24', facecolor='#FFFFFF')
    ax.add_patch(sub_worker)
    ax.text(9.75, 7.2, "Celery Worker & OCR Pipeline", fontsize=10, fontweight='bold', ha='center', color='#B45309')
    ax.text(9.75, 6.35, "• Nhận job nền từ hàng đợi Redis\n• Engine: OCRmyPDF + Tesseract\n• Trích xuất nội dung văn bản (OCR)\n• Tạo ảnh thu nhỏ (Thumbnails)", 
            fontsize=8.3, ha='center', va='center', color='#334155')

    # Sub-component: Search Index & Classifiers
    sub_search = patches.FancyBboxPatch((4.6, 4.6), 6.8, 0.75,
                                        boxstyle="round,pad=0.05,rounding_size=0.08",
                                        linewidth=1.0, edgecolor='#CBD5E1', facecolor='#F1F5F9')
    ax.add_patch(sub_search)
    ax.text(8.0, 4.97, "Whoosh Full-Text Indexer · Document Classifier (Tự động gán Tag/Corr) · Ingestion Watcher", 
            fontsize=8.5, ha='center', va='center', color='#475569')

    # CONTAINER 2: paperless-db (PostgreSQL)
    c2_box = patches.FancyBboxPatch((4.4, 1.1), 3.4, 2.9,
                                    boxstyle="round,pad=0.08,rounding_size=0.18",
                                    linewidth=1.8, edgecolor='#0D9488', facecolor='#F0FDF4')
    ax.add_patch(c2_box)
    ax.text(4.6, 3.7, "Container 2: paperless-db", fontsize=11, fontweight='bold', color='#0F766E')
    ax.text(7.6, 3.7, "postgres:16-alpine", fontsize=8.5, ha='right', color='#14B8A6')
    ax.text(6.1, 3.25, "PostgreSQL 16 Database", fontsize=9.5, fontweight='bold', ha='center', color='#115E59')
    ax.text(6.1, 3.0, "Port nội bộ: 5432 (paperless)", fontsize=8.5, ha='center', color='#134E4A')
    ax.text(6.1, 2.05, "Lưu trữ bảng Metadata quan hệ:\n• documents_document\n• documents_tag\n• documents_correspondent\n• documents_documenttype\n• auth_user & authtoken_token", 
            fontsize=8.2, ha='center', va='center', color='#334155')

    # CONTAINER 3: paperless-broker (Redis)
    c3_box = patches.FancyBboxPatch((8.2, 1.1), 3.4, 2.9,
                                    boxstyle="round,pad=0.08,rounding_size=0.18",
                                    linewidth=1.8, edgecolor='#EF4444', facecolor='#FEF2F2')
    ax.add_patch(c3_box)
    ax.text(8.4, 3.7, "Container 3: paperless-broker", fontsize=11, fontweight='bold', color='#B91C1C')
    ax.text(11.4, 3.7, "redis:7-alpine", fontsize=8.5, ha='right', color='#F87171')
    ax.text(9.9, 3.25, "Redis 7 In-Memory Store", fontsize=9.5, fontweight='bold', ha='center', color='#991B1B')
    ax.text(9.9, 3.0, "Port nội bộ: 6379", fontsize=8.5, ha='center', color='#7F1D1D')
    ax.text(9.9, 2.05, "Hàng đợi thông điệp & Tác vụ nền:\n• Celery Task Queue (Broker)\n• Lưu trữ trạng thái tác vụ OCR\n• Bộ đệm kết quả trung gian\n• Đảm bảo bất đồng bộ không nghẽn API", 
            fontsize=8.2, ha='center', va='center', color='#334155')

    # ==================== KHỐI 3: PERSISTENT VOLUMES ====================
    box_vols = patches.FancyBboxPatch((12.3, 0.8), 3.2, 7.9,
                                      boxstyle="round,pad=0.1,rounding_size=0.2",
                                      linewidth=1.8, edgecolor='#64748B', facecolor='#FFFFFF')
    ax.add_patch(box_vols)
    ax.text(13.9, 8.4, "PERSISTENT VOLUMES & HOST", fontsize=11.5, fontweight='bold', ha='center', color='#334155')

    # Volume: media
    v_media = patches.FancyBboxPatch((12.5, 6.7), 2.8, 1.4, boxstyle="round,pad=0.05,rounding_size=0.1",
                                     linewidth=1.2, edgecolor='#94A3B8', facecolor='#F8FAFC')
    ax.add_patch(v_media)
    ax.text(12.7, 7.8, "volume: media", fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.text(13.9, 7.3, "Gắn: /usr/src/paperless/media\n• Lưu file gốc (PDF/Text/Img)\n• File PDF sau xử lý OCR, ảnh thumb", 
            fontsize=8, ha='center', va='center', color='#475569')

    # Volume: data
    v_data = patches.FancyBboxPatch((12.5, 5.1), 2.8, 1.4, boxstyle="round,pad=0.05,rounding_size=0.1",
                                    linewidth=1.2, edgecolor='#94A3B8', facecolor='#F8FAFC')
    ax.add_patch(v_data)
    ax.text(12.7, 6.2, "volume: data", fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.text(13.9, 5.7, "Gắn: /usr/src/paperless/data\n• Whoosh Search Index files\n• Cấu hình & Cache máy chủ", 
            fontsize=8, ha='center', va='center', color='#475569')

    # Volume: pgdata
    v_pg = patches.FancyBboxPatch((12.5, 3.5), 2.8, 1.4, boxstyle="round,pad=0.05,rounding_size=0.1",
                                  linewidth=1.2, edgecolor='#5EEAD4', facecolor='#F0FDFA')
    ax.add_patch(v_pg)
    ax.text(12.7, 4.6, "volume: pgdata", fontsize=9.5, fontweight='bold', color='#0F766E')
    ax.text(13.9, 4.1, "Gắn: /var/lib/postgresql/data\n• Toàn bộ database PostgreSQL\n• Bảng dữ liệu, khóa, indexes", 
            fontsize=8, ha='center', va='center', color='#134E4A')

    # Volume: redisdata
    v_redis = patches.FancyBboxPatch((12.5, 1.9), 2.8, 1.4, boxstyle="round,pad=0.05,rounding_size=0.1",
                                     linewidth=1.2, edgecolor='#FCA5A5', facecolor='#FEF2F2')
    ax.add_patch(v_redis)
    ax.text(12.7, 3.0, "volume: redisdata", fontsize=9.5, fontweight='bold', color='#B91C1C')
    ax.text(13.9, 2.5, "Gắn: /data (dump.rdb)\n• Trạng thái hàng đợi Redis\n• Bảo đảm task không mất khi restart", 
            fontsize=8, ha='center', va='center', color='#7F1D1D')

    # Host bind: consume & export
    v_host = patches.FancyBboxPatch((12.5, 1.0), 2.8, 0.75, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    linewidth=1.0, edgecolor='#CBD5E1', facecolor='#F1F5F9')
    ax.add_patch(v_host)
    ax.text(13.9, 1.37, "Thư mục Host: ./consume · ./export · .env", fontsize=8.2, fontweight='bold', ha='center', color='#334155')

    # ==================== MŨI TÊN TƯƠNG TÁC (ARROWS) ====================
    # 1. Clients -> Webserver (HTTP 8000)
    ax.annotate("", xy=(4.4, 7.0), xytext=(3.5, 7.0),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#2563EB'))
    ax.text(3.95, 7.25, "HTTP :8000", fontsize=8.5, fontweight='bold', color='#1E40AF', ha='center')

    ax.annotate("", xy=(4.4, 6.0), xytext=(3.5, 4.7),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#7E22CE'))
    ax.text(3.95, 5.2, "REST API\nToken Auth", fontsize=8, fontweight='bold', color='#6B21A8', ha='center')

    # 2. Webserver <-> PostgreSQL (5432)
    ax.annotate("", xy=(6.1, 4.0), xytext=(6.1, 4.4),
                arrowprops=dict(arrowstyle="<->", lw=2.0, color='#0D9488'))
    ax.text(6.1, 4.18, "SQL (Port 5432)", fontsize=8.2, fontweight='bold', color='#0F766E', ha='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#5EEAD4', lw=0.6))

    # 3. Webserver <-> Redis (6379)
    ax.annotate("", xy=(9.9, 4.0), xytext=(9.9, 4.4),
                arrowprops=dict(arrowstyle="<->", lw=2.0, color='#EF4444'))
    ax.text(9.9, 4.18, "Celery (Port 6379)", fontsize=8.2, fontweight='bold', color='#B91C1C', ha='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#FCA5A5', lw=0.6))

    # 4. Webserver -> Media / Data Volumes
    ax.annotate("", xy=(12.3, 7.0), xytext=(11.6, 7.0),
                arrowprops=dict(arrowstyle="->", lw=1.8, linestyle=':', color='#64748B'))
    ax.text(11.95, 7.18, "Mount", fontsize=8, fontweight='bold', color='#475569', ha='center')

    ax.annotate("", xy=(12.3, 5.8), xytext=(11.6, 5.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, linestyle=':', color='#64748B'))

    # 5. DB -> pgdata
    ax.annotate("", xy=(12.3, 4.2), xytext=(7.8, 2.5),
                arrowprops=dict(arrowstyle="->", lw=1.5, linestyle=':', color='#0D9488'))

    # 6. Redis -> redisdata
    ax.annotate("", xy=(12.3, 2.6), xytext=(11.6, 2.5),
                arrowprops=dict(arrowstyle="->", lw=1.5, linestyle=':', color='#EF4444'))

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Đã vẽ và xuất thành công file ảnh sơ đồ: {png_path}")

if __name__ == "__main__":
    draw_diagram()
