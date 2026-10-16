#!/usr/bin/env python3
"""
scripts/build_bug_evidence_slides_TV3.py
Tạo file trình chiếu PowerPoint 2 slide chuẩn cho BUG-01 và BUG-03
Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303.
Lưu file vào: docs/slides/TV3_BUG_EVIDENCE_303.pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

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
CARD_BG = RGBColor(24, 24, 24)        # #181818
CARD_BORDER = RGBColor(51, 51, 51)    # #333333
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
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.32), Inches(9.3), Inches(0.85))
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
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.0), Inches(0.4), Inches(2.7), Inches(0.45))
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


def build_slide1(prs):
    # Slide 1: BUG-01
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    
    add_header(slide, "BUG-01: Dữ Liệu Permissions Sai Kiểu Gây Lỗi Máy Chủ HTTP 500", "Severity đề xuất: High", RED_ACCENT)
    
    # 2 Images side by side
    img1_path = os.path.join(EVIDENCE_DIR, "TV3_BUG01_correspondents_500.png")
    img2_path = os.path.join(EVIDENCE_DIR, "TV3_BUG01_document_types_500.png")
    
    img_w = Inches(5.9)
    img_h = Inches(3.32)
    top_y = Inches(1.3)
    
    if os.path.exists(img1_path):
        slide.shapes.add_picture(img1_path, Inches(0.6), top_y, width=img_w, height=img_h)
    if os.path.exists(img2_path):
        slide.shapes.add_picture(img2_path, Inches(6.8), top_y, width=img_w, height=img_h)
        
    # Bottom Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.75), Inches(12.1), Inches(2.35))
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
        run1.font.size = Pt(11)
        run1.font.color.rgb = pre_color
        
        run2 = p.add_run()
        run2.text = text
        run2.font.bold = body_bold
        run2.font.size = Pt(11)
        run2.font.color.rgb = body_color

    # Speaker Notes chuẩn hóa
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = (
        "SPEAKER NOTES — SLIDE 1 (BUG-01):\n"
        "- Người trình bày: Nguyễn Khiêm Thuận (TV3) - MSSV: 2312764 - Seed: 303.\n"
        "- Bằng chứng thực thi: docs/evidence/TV3_BUG01_correspondents_500.png và docs/evidence/TV3_BUG01_document_types_500.png.\n"
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
    
    # 2 Images side by side
    img1_path = os.path.join(EVIDENCE_DIR, "TV3_BUG03_response_201.png")
    img2_path = os.path.join(EVIDENCE_DIR, "TV3_BUG03_schema_required.png")
    
    img_w = Inches(5.9)
    img_h = Inches(3.32)
    top_y = Inches(1.3)
    
    if os.path.exists(img1_path):
        slide.shapes.add_picture(img1_path, Inches(0.6), top_y, width=img_w, height=img_h)
    if os.path.exists(img2_path):
        slide.shapes.add_picture(img2_path, Inches(6.8), top_y, width=img_w, height=img_h)
        
    # Bottom Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.75), Inches(12.1), Inches(2.35))
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
        ("• Giả thuyết kỹ thuật & Hướng kiểm tra: ", True, GREEN_ACCENT, "Có thể do trường permissions phụ thuộc logic truy vấn GET có cờ full_perms=true, và các trường document_count, last_correspondence là trường annotate lúc lọc danh sách. Cần kiểm tra mã nguồn phiên bản 3.1.3 để xác minh trước khi đề xuất giải pháp tách serializer cho phản hồi 201.", False, TEXT_LIGHT),
        ("• Phạm vi ghi nhận hồ sơ: ", True, YELLOW_ACCENT, "Hồ sơ TV3 chỉ xác nhận lỗi này trên endpoint POST /api/correspondents/. Chưa mở rộng cho các tài nguyên khác nếu chưa kiểm thử độc lập.", False, TEXT_LIGHT),
    ]
    
    for prefix, pre_bold, pre_color, text, body_bold, body_color in bullet_items:
        p = ctf.add_paragraph()
        p.space_after = Pt(4)
        run1 = p.add_run()
        run1.text = prefix
        run1.font.bold = pre_bold
        run1.font.size = Pt(11)
        run1.font.color.rgb = pre_color
        
        run2 = p.add_run()
        run2.text = text
        run2.font.bold = body_bold
        run2.font.size = Pt(11)
        run2.font.color.rgb = body_color

    # Speaker Notes chuẩn hóa
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = (
        "SPEAKER NOTES — SLIDE 2 (BUG-03):\n"
        "- Người trình bày: Nguyễn Khiêm Thuận (TV3) - MSSV: 2312764 - Seed: 303.\n"
        "- Bằng chứng thực thi: docs/evidence/TV3_BUG03_response_201.png và đối chiếu hợp đồng tại docs/evidence/TV3_BUG03_schema_required.png (trích xuất từ docs/openapi_TV3.json, SHA256: 888b0f89...).\n"
        "- Quan sát cốt lõi: Response 201 của POST /api/correspondents/ thiếu các trường required đã đối chiếu trong OpenAPI, thể hiện sai lệch giữa phản hồi thực tế và hợp đồng API.\n"
        "- Xác minh cụ thể: Cả 3 trường document_count, last_correspondence, permissions đều được schema đánh dấu là required nhưng vắng mặt hoàn toàn trong response 201.\n"
        "- Đánh giá mức độ nghiêm trọng: Severity đề xuất là Medium vì chức năng tạo mới đối tượng trên cơ sở dữ liệu vẫn thành công, nhưng client tự động sinh từ OpenAPI schema có thể bị crash khi parse thiếu trường bắt buộc.\n"
        "- Hướng kiểm tra tiếp theo: Kiểm tra mã nguồn Paperless-ngx 3.1.3 để làm rõ giả thuyết drf-spectacular dùng chung một schema cho cả thao tác đọc và ghi."
    )


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    print("[INFO] Bắt đầu khởi tạo 2 slide minh chứng lỗi TV3 theo nhận định chuẩn hóa...")
    build_slide1(prs)
    build_slide2(prs)
    
    prs.save(OUTPUT_PPTX)
    print(f"[THÀNH CÔNG] Đã cập nhật file slide hoàn chỉnh: {OUTPUT_PPTX}")
    print(f"  - Kích thước: 13.333 x 7.5 inches (Widescreen 16:9)")
    print(f"  - Số slide: {len(prs.slides)}")
    print(f"  - Dung lượng: {os.path.getsize(OUTPUT_PPTX) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
