#!/usr/bin/env python3
"""
scripts/generate_erd_diagram.py
Vẽ sơ đồ quan hệ dữ liệu (ER Diagram) hệ thống Paperless-ngx
Xuất ra file ảnh PNG chất lượng cao: docs/images/so_do_quan_he_du_lieu.png
và file vector: docs/images/so_do_quan_he_du_lieu.svg
Phục vụ chèn vào Hình 2 của Báo cáo kiểm thử phần mềm (Nhóm 17 - Đề tài R08 + K05)
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

def draw_erd():
    output_dir = Path("docs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "so_do_quan_he_du_lieu.png"

    fig, ax = plt.subplots(figsize=(16, 10.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10.5)
    ax.axis('off')

    # ==================== TIÊU ĐỀ ====================
    ax.text(8.0, 10.1, "HÌNH 2: SƠ ĐỒ QUAN HỆ DỮ LIỆU CỐT LÕI (ER DIAGRAM) PAPERLESS-NGX", 
            fontsize=16.5, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(8.0, 9.7, "Căn cứ trực tiếp từ models.py (tag v3.1.3) · 4 Thực thể API trọng tâm: Document, Tag, Correspondent, DocumentType", 
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#475569')

    # Helper function vẽ bảng thực thể
    def draw_entity(x, y, w, h, title, subtitle, fields, header_color, border_color):
        # Card background
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.15",
                                      linewidth=1.8, edgecolor=border_color, facecolor='#FFFFFF')
        ax.add_patch(card)
        # Header background
        header_h = 0.75
        header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                        boxstyle="round,pad=0.06,rounding_size=0.15",
                                        linewidth=0, facecolor=header_color)
        ax.add_patch(header)
        # Sửa góc dưới của header cho thẳng
        rect_fix = patches.Rectangle((x, y + h - header_h), w, 0.2, linewidth=0, facecolor=header_color)
        ax.add_patch(rect_fix)

        ax.text(x + w/2, y + h - 0.28, title, fontsize=11.5, fontweight='bold', ha='center', color='#FFFFFF')
        ax.text(x + w/2, y + h - 0.55, subtitle, fontsize=8.5, ha='center', color='#E2E8F0')

        # Fields
        cur_y = y + h - 0.95
        for f in fields:
            is_pk = "PK" in f
            is_fk = "FK" in f
            f_color = '#0F172A'
            if is_pk:
                f_color = '#B91C1C'
            elif is_fk:
                f_color = '#1D4ED8'

            ax.text(x + 0.2, cur_y, f, fontsize=8.8, va='center', color=f_color,
                    fontweight='bold' if (is_pk or is_fk) else 'normal')
            cur_y -= 0.28

    # ==================== VẼ CÁC BẢNG THỰC THỂ ====================

    # 1. USER (auth_user) - Đặt ở đỉnh
    fields_user = [
        "[PK] id : int",
        "• username : varchar(150)",
        "• email : varchar(254)",
        "• is_superuser : boolean",
        "• is_active : boolean",
    ]
    draw_entity(6.3, 7.3, 3.4, 2.2, "User (auth_user)", "Bảng quản lý người dùng", fields_user, '#334155', '#64748B')

    # 2. DOCUMENT (documents_document) - Thực thể trung tâm
    fields_doc = [
        "[PK] id : int",
        "• title : varchar(128)",
        "• content : text (Nội dung OCR)",
        "• created : date (Ngày tài liệu)",
        "• modified : datetime (Ngày sửa)",
        "• added : datetime (Ngày nạp)",
        "• checksum : varchar(32) (MD5)",
        "• mime_type : varchar(256)",
        "[FK] correspondent_id : int",
        "[FK] document_type_id : int",
        "[FK] owner_id : int",
    ]
    draw_entity(6.1, 2.7, 3.8, 3.9, "Document", "documents_document (Trung tâm)", fields_doc, '#1D4ED8', '#3B82F6')

    # 3. CORRESPONDENT (documents_correspondent) - Bên trái
    fields_corr = [
        "[PK] id : int",
        "• name : varchar(128) (Bắt buộc)",
        "• slug : slug (Tự sinh)",
        "• match : varchar(256)",
        "• matching_algorithm : int (0..6)",
        "• is_insensitive : boolean",
        "[FK] owner_id : int",
        "[Model] Kế thừa MatchingModel",
    ]
    draw_entity(0.8, 4.3, 3.6, 3.1, "Correspondent", "documents_correspondent (Người gửi)", fields_corr, '#0D9488', '#14B8A6')

    # 4. DOCUMENT TYPE (documents_documenttype) - Bên phải
    fields_dtype = [
        "[PK] id : int",
        "• name : varchar(128) (Bắt buộc)",
        "• slug : slug (Tự sinh)",
        "• match : varchar(256)",
        "• matching_algorithm : int (0..6)",
        "• is_insensitive : boolean",
        "[FK] owner_id : int",
        "[Model] Kế thừa MatchingModel",
    ]
    draw_entity(11.6, 4.3, 3.6, 3.1, "DocumentType", "documents_documenttype (Loại tệp)", fields_dtype, '#D97706', '#F59E0B')

    # 5. TAG (documents_tag) - Đặt ở góc dưới trái
    fields_tag = [
        "[PK] id : int",
        "• name : varchar(128) (Bắt buộc)",
        "• color : varchar(7) (HEX #rrggbb)",
        "• match : varchar(256)",
        "• matching_algorithm : int (0..6)",
        "• is_insensitive : boolean",
        "• is_inbox_tag : boolean",
        "[FK] parent_id : int (đệ quy <= 5)",
        "[FK] owner_id : int",
        "[Model] MatchingModel & TreeNode",
    ]
    draw_entity(0.8, 0.4, 3.8, 3.6, "Tag", "documents_tag (Nhãn phân loại)", fields_tag, '#7C3AED', '#8B5CF6')

    # 6. BẢNG TRUNG GIAN N:M: documents_document_tags - Đặt ở giữa dưới
    fields_rel = [
        "[PK] id : int",
        "[FK] document_id : int",
        "[FK] tag_id : int",
        "• Ràng buộc: Unique(doc_id, tag_id)",
    ]
    draw_entity(6.1, 0.6, 3.8, 1.8, "Document_Tags", "Bảng trung gian Nhiều-Nhiều (N:M)", fields_rel, '#64748B', '#94A3B8')

    # ==================== ĐƯỜNG QUAN HỆ & CHÚ THÍCH ====================

    # [1] User -> Document (1 : N)
    ax.annotate("", xy=(8.0, 6.6), xytext=(8.0, 7.3),
                arrowprops=dict(arrowstyle="->", lw=1.8, color='#334155'))
    ax.text(8.05, 6.95, "owns (1 : N)", fontsize=8.5, fontweight='bold', color='#334155')

    # [2] User -> Correspondent (1 : N)
    ax.annotate("", xy=(2.6, 7.4), xytext=(6.3, 8.4),
                arrowprops=dict(arrowstyle="->", lw=1.5, linestyle='--', color='#0D9488'))
    ax.text(4.4, 8.0, "owns (1 : N)", fontsize=8.2, fontweight='bold', color='#0F766E')

    # [3] User -> DocumentType (1 : N)
    ax.annotate("", xy=(13.4, 7.4), xytext=(9.7, 8.4),
                arrowprops=dict(arrowstyle="->", lw=1.5, linestyle='--', color='#D97706'))
    ax.text(11.5, 8.0, "owns (1 : N)", fontsize=8.2, fontweight='bold', color='#B45309')

    # [4] User -> Tag (1 : N)
    ax.annotate("", xy=(0.8, 2.5), xytext=(6.3, 7.8),
                arrowprops=dict(arrowstyle="->", lw=1.2, linestyle=':', color='#7C3AED'))

    # [5] Correspondent -> Document (1 : N, Nullable)
    ax.annotate("", xy=(6.1, 5.0), xytext=(4.4, 5.0),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#0D9488'))
    ax.text(5.25, 5.2, "sender of\n(1 : N)", fontsize=9, fontweight='bold', ha='center', color='#0F766E',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#F0FDFA', edgecolor='#5EEAD4', lw=0.6))

    # [6] DocumentType -> Document (1 : N, Nullable)
    ax.annotate("", xy=(9.9, 5.0), xytext=(11.6, 5.0),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#D97706'))
    ax.text(10.75, 5.2, "categorizes\n(1 : N)", fontsize=9, fontweight='bold', ha='center', color='#B45309',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFBEB', edgecolor='#FCD34D', lw=0.6))

    # [7] Document <-> Tag (N : M thông qua bảng trung gian)
    ax.annotate("", xy=(8.0, 2.4), xytext=(8.0, 2.7),
                arrowprops=dict(arrowstyle="->", lw=2.0, color='#1D4ED8'))
    ax.annotate("", xy=(4.6, 1.5), xytext=(6.1, 1.5),
                arrowprops=dict(arrowstyle="->", lw=2.0, color='#7C3AED'))
    ax.text(5.35, 1.7, "N : M", fontsize=9, fontweight='bold', ha='center', color='#6B21A8',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FAF5FF', edgecolor='#D8B4FE', lw=0.6))

    # [8] Tag -> Tag (Đệ quy cây phân cấp TreeNodeModel)
    loop_arc = patches.Arc((4.6, 2.8), 1.2, 1.2, angle=0, theta1=270, theta2=90, color='#7C3AED', lw=1.6)
    ax.add_patch(loop_arc)
    ax.annotate("", xy=(4.6, 3.4), xytext=(4.5, 3.4),
                arrowprops=dict(arrowstyle="->", lw=1.6, color='#7C3AED'))
    ax.text(5.3, 2.8, "parent of\n(đệ quy <= 5)", fontsize=8, fontweight='bold', color='#6B21A8', va='center')

    # ==================== HỘP GIẢI THÍCH NGUYÊN TẮC THIẾT KẾ ====================
    box_notes = patches.FancyBboxPatch((11.4, 0.4), 4.1, 3.6,
                                       boxstyle="round,pad=0.08,rounding_size=0.15",
                                       linewidth=1.2, edgecolor='#CBD5E1', facecolor='#F1F5F9')
    ax.add_patch(box_notes)
    ax.text(13.45, 3.7, "QUY TẮC TOÀN VẸN & LIÊN KẾT", fontsize=10, fontweight='bold', ha='center', color='#1E293B')
    ax.text(11.6, 3.3, "1. Thực thể trung tâm:", fontsize=8.8, fontweight='bold', color='#1E40AF')
    ax.text(11.6, 3.05, "   Document liên kết với Correspondent và\n   DocumentType theo quan hệ 1:N (null=True).", fontsize=8.2, color='#334155')

    ax.text(11.6, 2.65, "2. Gắn nhãn đa chiều (N : M):", fontsize=8.8, fontweight='bold', color='#6B21A8')
    ax.text(11.6, 2.4, "   Một tài liệu có thể gắn nhiều Tag và một\n   Tag có thể phân loại nhiều tài liệu.", fontsize=8.2, color='#334155')

    ax.text(11.6, 2.0, "3. Kế thừa MatchingModel:", fontsize=8.8, fontweight='bold', color='#0F766E')
    ax.text(11.6, 1.75, "   Tag, Corr, DocType chia sẻ chung thuật\n   toán so khớp tự động (match, algo, insens).", fontsize=8.2, color='#334155')

    ax.text(11.6, 1.35, "4. Tính duy nhất (UniqueConstraint):", fontsize=8.8, fontweight='bold', color='#B91C1C')
    ax.text(11.6, 1.1, "   Tên (name) là duy nhất theo từng Owner.\n   Độ dài tối đa trường name: 128 ký tự.", fontsize=8.2, color='#334155')

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Đã vẽ và xuất thành công file ảnh ERD: {png_path}")

if __name__ == "__main__":
    draw_erd()
