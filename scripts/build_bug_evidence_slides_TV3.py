#!/usr/bin/env python3
"""
scripts/build_bug_evidence_slides_TV3.py
Tạo file trình chiếu PowerPoint 2 slide chuẩn cho BUG-01 và BUG-03
Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303.
Sử dụng 3 ảnh chụp màn hình thực tế TV3_REAL_ và 1 ảnh Trích xuất OpenAPI schema.
Bảo đảm tỷ lệ ảnh gốc, không méo hình, chữ đọc rõ ràng.
Lưu file vào: docs/slides/TV3_BUG_EVIDENCE_303.pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image as PILImage

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_DIR = os.path.join(ROOT_DIR, "docs", "evidence")
SLIDES_DIR = os.path.join(ROOT_DIR, "docs", "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)
OUTPUT_PPTX = os.path.join(SLIDES_DIR, "TV3_BUG_EVIDENCE_303.pptx")

# Palette
DARK_BG = RGBColor(12, 12, 12)        # #0C0C0C
CARD_BG = RGBColor(20, 20, 20)        # #141414
CARD_BORDER = RGBColor(45, 45, 45)    # #2D2D2D
TEXT_LIGHT = RGBColor(230, 230, 230)  # #E6E6E6
TEXT_MUTED = RGBColor(150, 150, 150)  # #969696
RED_ACCENT = RGBColor(224, 108, 117)  # #E06C75
GREEN_ACCENT = RGBColor(152, 195, 121)# #98C379
BLUE_ACCENT = RGBColor(97, 175, 239)  # #61AFEF
YELLOW_ACCENT = RGBColor(229, 192, 123)# #E5C07B


def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG


def add_header(slide, title_text, badge_text, badge_color):
    # Title Box
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.28), Inches(9.3), Inches(0.85))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    
    p2 = tf.add_paragraph()
    p2.text = "Thành viên 3: Nguyễn Khiêm Thuận · MSSV: 2312764 · Seed: 303 | Paperless-ngx v3.1.3 | Schemathesis 4.30.1"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_MUTED

    # Badge Box (Right side)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.0), Inches(0.35), Inches(2.7), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = badge_color
    badge.line.color.rgb = badge_color
    btf = badge.text_frame
    btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = badge_text
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = RGBColor(0, 0, 0)


def add_image_container(slide, left, top, width, height, caption_text, img_path):
    # Outer container box
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    frame.fill.solid()
    frame.fill.fore_color.rgb = CARD_BG
    frame.line.color.rgb = CARD_BORDER
    frame.line.width = Pt(1)
    
    # Header bar for caption
    hdr_h = Inches(0.32)
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, hdr_h)
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = RGBColor(30, 30, 30)
    hdr.line.color.rgb = CARD_BORDER
    hdr.line.width = Pt(1)
    
    htf = hdr.text_frame
    htf.margin_left = Inches(0.12)
    htf.margin_top = Inches(0.04)
    htf.margin_bottom = htf.margin_right = 0
    hp = htf.paragraphs[0]
    hp.text = caption_text
    hp.font.size = Pt(9.5)
    hp.font.bold = True
    hp.font.color.rgb = YELLOW_ACCENT
    
    # Add Image inside container preserving exact aspect ratio
    if os.path.exists(img_path):
        with PILImage.open(img_path) as im:
            orig_w, orig_h = im.size
            
        avail_w = width - Inches(0.16)
        avail_h = height - hdr_h - Inches(0.12)
        
        # Calculate fit scale without distortion
        scale_w = avail_w / orig_w
        scale_h = avail_h / orig_h
        scale = min(scale_w, scale_h)
        
        final_w = orig_w * scale
        final_h = orig_h * scale
        
        # Center horizontally and vertically inside available area
        img_left = left + Inches(0.08) + (avail_w - final_w) / 2
        img_top = top + hdr_h + Inches(0.06) + (avail_h - final_h) / 2
        
        slide.shapes.add_picture(img_path, img_left, img_top, width=final_w, height=final_h)


def build_slide1(prs):
    # Slide 1: BUG-01
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    
    add_header(slide, "BUG-01: Dữ Liệu Permissions Sai Kiểu Gây Lỗi Máy Chủ HTTP 500", "Severity đề xuất: High", RED_ACCENT)
    
    img1_path = os.path.join(EVIDENCE_DIR, "TV3_REAL_BUG01_correspondents_500.png")
    img2_path = os.path.join(EVIDENCE_DIR, "TV3_REAL_BUG01_document_types_500.png")
    
    col_w = Inches(5.95)
    col_h = Inches(3.25)
    top_y = Inches(1.25)
    
    add_image_container(
        slide, Inches(0.6), top_y, col_w, col_h,
        "Ảnh chụp màn hình thực tế: POST /api/correspondents/ (HTTP 500 Server Error)",
        img1_path
    )
    add_image_container(
        slide, Inches(6.75), top_y, col_w, col_h,
        "Ảnh chụp màn hình thực tế: POST /api/document_types/ (HTTP 500 Server Error)",
        img2_path
    )
        
    # Bottom Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.65), Inches(12.1), Inches(2.45))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1)
    
    ctf = card.text_frame
    ctf.word_wrap = True
    ctf.margin_left = Inches(0.25)
    ctf.margin_right = Inches(0.25)
    ctf.margin_top = Inches(0.18)
    ctf.margin_bottom = Inches(0.15)
    
    p_card_title = ctf.paragraphs[0]
    p_card_title.text = "TÓM TẮT KỸ THUẬT & QUAN SÁT THỰC TẾ (BUG-01)"
    p_card_title.font.size = Pt(13)
    p_card_title.font.bold = True
    p_card_title.font.color.rgb = YELLOW_ACCENT
    
    bullet_items = [
        ("• Quan sát cốt lõi: ", True, BLUE_ACCENT, "Gửi set_permissions.view dạng boolean dẫn đến HTTP 500 trên hai endpoint. Hệ thống cần từ chối đầu vào sai kiểu bằng phản hồi 4xx phù hợp.", False, TEXT_LIGHT),
        ("• Hiện tượng thực tế (Actual): ", True, RED_ACCENT, "HTTP 500 Internal Server Error (trang HTML Django); máy chủ phát sinh ngoại lệ chưa được xử lý (Unhandled Server Error) khi nhận boolean thay vì object.", False, TEXT_LIGHT),
        ("• Kỳ vọng đối chiếu (Expected): ", True, GREEN_ACCENT, "HTTP 400 Bad Request; theo đặc tả OpenAPI, view phải là object chứa danh sách ID người dùng/nhóm ({users: [], groups: []}).", False, TEXT_LIGHT),
        ("• Phạm vi & Kết luận kiểm thử: ", True, YELLOW_ACCENT, "Đã tái hiện độc lập trên cả hai endpoint: POST /api/correspondents/ và POST /api/document_types/. Không tự ý khẳng định lỗi ở tầng serializer hay ORM do chưa trích xuất traceback nội bộ container.", False, TEXT_LIGHT),
    ]
    
    for prefix, pre_bold, pre_color, text, body_bold, body_color in bullet_items:
        p = ctf.add_paragraph()
        p.space_after = Pt(4)
        run1 = p.add_run()
        run1.text = prefix
        run1.font.bold = pre_bold
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = pre_color
        
        run2 = p.add_run()
        run2.text = text
        run2.font.bold = body_bold
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = body_color

    # Speaker Notes
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = (
        "SPEAKER NOTES — SLIDE 1 (BUG-01):\n"
        "- Người trình bày: Nguyễn Khiêm Thuận (TV3) - MSSV: 2312764 - Seed: 303.\n"
        "- Bằng chứng thực tế: Hai ảnh chụp màn hình thực tế tại docs/evidence/TV3_REAL_BUG01_correspondents_500.png và docs/evidence/TV3_REAL_BUG01_document_types_500.png.\n"
        "- Quan sát cốt lõi: Gửi set_permissions.view dạng boolean dẫn đến HTTP 500 trên cả hai endpoint /api/correspondents/ và /api/document_types/. Hệ thống cần từ chối đầu vào sai kiểu bằng phản hồi 4xx phù hợp (kỳ vọng cụ thể: HTTP 400 Bad Request).\n"
        "- Đánh giá mức độ nghiêm trọng: Severity đề xuất là High (để nhóm thảo luận và thống nhất), vì máy chủ phát sinh lỗi 500 đối với payload sai định dạng dữ liệu thay vì trả mã 4xx từ chối an toàn.\n"
        "- Điểm lưu ý bảo vệ đồ án: Giữ đúng nguyên tắc kiểm thử hộp đen; không quy kết nguyên nhân do lỗi serializer, TypeError hay ORM nếu chưa trích xuất traceback từ container logs."
    )


def build_slide2(prs):
    # Slide 2: BUG-03
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    
    add_header(slide, "BUG-03: Phản Hồi Tạo Mới (201 Created) Thiếu Trường Bắt Buộc Theo Schema", "Severity đề xuất: Medium", YELLOW_ACCENT)
    
    img1_path = os.path.join(EVIDENCE_DIR, "TV3_REAL_BUG03_response_201.png")
    img2_path = os.path.join(EVIDENCE_DIR, "TV3_BUG03_schema_required.png")
    
    col_w = Inches(5.95)
    col_h = Inches(3.25)
    top_y = Inches(1.25)
    
    add_image_container(
        slide, Inches(0.6), top_y, col_w, col_h,
        "Ảnh chụp màn hình thực tế: POST /api/correspondents/ (Máy chủ trả HTTP 201)",
        img1_path
    )
    add_image_container(
        slide, Inches(6.75), top_y, col_w, col_h,
        "Trích xuất OpenAPI schema: Cấu trúc response 201 (#/components/schemas/Correspondent)",
        img2_path
    )
        
    # Bottom Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.65), Inches(12.1), Inches(2.45))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1)
    
    ctf = card.text_frame
    ctf.word_wrap = True
    ctf.margin_left = Inches(0.25)
    ctf.margin_right = Inches(0.25)
    ctf.margin_top = Inches(0.18)
    ctf.margin_bottom = Inches(0.15)
    
    p_card_title = ctf.paragraphs[0]
    p_card_title.text = "TÓM TẮT KỸ THUẬT & ĐỐI CHIẾU HỢP ĐỒNG API (BUG-03)"
    p_card_title.font.size = Pt(13)
    p_card_title.font.bold = True
    p_card_title.font.color.rgb = YELLOW_ACCENT
    
    bullet_items = [
        ("• Quan sát cốt lõi: ", True, BLUE_ACCENT, "Response 201 của POST /api/correspondents/ thiếu các trường required đã đối chiếu trong OpenAPI, thể hiện sai lệch giữa phản hồi thực tế và hợp đồng API.", False, TEXT_LIGHT),
        ("• Trường bắt buộc bị thiếu đã xác minh: ", True, RED_ACCENT, "Đối chiếu trực tiếp schema Correspondent: phản hồi thực tế chỉ trả về 8 trường, thiếu chính xác 3 trường required: document_count, last_correspondence, permissions.", False, TEXT_LIGHT),
        ("• Hiện tượng quan sát (Actual): ", True, GREEN_ACCENT, "Khi gửi POST tạo mới, máy chủ trả HTTP 201 Created nhưng payload thiếu 3 trường required. Do chưa kiểm tra lại bản ghi bằng phương thức GET, hồ sơ chỉ ghi nhận kết quả quan sát trực tiếp từ phản hồi HTTP 201 của máy chủ (không khẳng định đã xác minh lưu database).", False, TEXT_LIGHT),
        ("• Giả thuyết kỹ thuật & Hướng kiểm tra: ", True, YELLOW_ACCENT, "Có thể do trường permissions phụ thuộc logic truy vấn GET có cờ full_perms=true, và các trường document_count, last_correspondence là trường annotate lúc lọc danh sách. Cần kiểm tra mã nguồn phiên bản 3.1.3 để xác minh trước khi đề xuất giải pháp tách serializer cho phản hồi 201.", False, TEXT_LIGHT),
        ("• Phạm vi ghi nhận hồ sơ: ", True, TEXT_MUTED, "Hồ sơ TV3 chỉ xác nhận lỗi này trên endpoint POST /api/correspondents/. Chưa mở rộng cho các tài nguyên khác nếu chưa kiểm thử độc lập.", False, TEXT_LIGHT),
    ]
    
    for prefix, pre_bold, pre_color, text, body_bold, body_color in bullet_items:
        p = ctf.add_paragraph()
        p.space_after = Pt(3)
        run1 = p.add_run()
        run1.text = prefix
        run1.font.bold = pre_bold
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = pre_color
        
        run2 = p.add_run()
        run2.text = text
        run2.font.bold = body_bold
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = body_color

    # Speaker Notes
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = (
        "SPEAKER NOTES — SLIDE 2 (BUG-03):\n"
        "- Người trình bày: Nguyễn Khiêm Thuận (TV3) - MSSV: 2312764 - Seed: 303.\n"
        "- Bằng chứng thực tế: Ảnh chụp màn hình thực tế (docs/evidence/TV3_REAL_BUG03_response_201.png) và Trích xuất OpenAPI schema (docs/evidence/TV3_BUG03_schema_required.png, SHA256: 888b0f89...).\n"
        "- Quan sát cốt lõi: Khi gửi request POST /api/correspondents/, máy chủ trả HTTP 201 Created nhưng response body thiếu 3 trường required đã đối chiếu trong OpenAPI (document_count, last_correspondence, permissions), thể hiện sai lệch giữa phản hồi thực tế và hợp đồng API.\n"
        "- Lưu ý bảo vệ đồ án: Chỉ khẳng định kết quả quan sát được từ phản hồi HTTP 201 của máy chủ; không khẳng định đã xác minh lưu vào database vì chưa kiểm tra lại bản ghi bằng phương thức GET.\n"
        "- Đánh giá mức độ nghiêm trọng: Severity đề xuất là Medium (sai lệch hợp đồng API, client tự động sinh có thể gặp lỗi deserialize).\n"
        "- Hướng kiểm tra tiếp theo: Kiểm tra mã nguồn Paperless-ngx 3.1.3 để làm rõ giả thuyết drf-spectacular dùng chung một schema cho cả thao tác đọc và ghi."
    )


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    print("[INFO] Bắt đầu khởi tạo 2 slide minh chứng lỗi TV3 với ảnh chụp thực tế TV3_REAL_...")
    build_slide1(prs)
    build_slide2(prs)
    
    prs.save(OUTPUT_PPTX)
    print(f"[THÀNH CÔNG] Đã cập nhật file slide hoàn chỉnh: {OUTPUT_PPTX}")
    print(f"  - Kích thước: 13.333 x 7.5 inches (Widescreen 16:9)")
    print(f"  - Số slide: {len(prs.slides)}")
    print(f"  - Dung lượng: {os.path.getsize(OUTPUT_PPTX) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
