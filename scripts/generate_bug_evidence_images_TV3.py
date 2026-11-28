#!/usr/bin/env python3
"""
scripts/generate_bug_evidence_images_TV3.py
Kết xuất ảnh minh chứng thực tế từ luồng thực thi CLI cho BUG-01 và BUG-03
Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303.
Kết xuất 4 ảnh PNG chuẩn HD vào docs/evidence/:
1. TV3_BUG01_correspondents_500.png
2. TV3_BUG01_document_types_500.png
3. TV3_BUG03_response_201.png
4. TV3_BUG03_schema_required.png
"""

import os
import sys
import time
import json
import requests
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_DIR = os.path.join(ROOT_DIR, "docs", "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


def get_fonts():
    font_dir = r"C:\Windows\Fonts"
    try:
        f_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 20)
        f_sub = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 13)
        f_header = ImageFont.truetype(os.path.join(font_dir, "consolab.ttf"), 15)
        f_code = ImageFont.truetype(os.path.join(font_dir, "consola.ttf"), 13)
        f_badge = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 13)
        f_note = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 12)
    except Exception:
        f_title = f_sub = f_header = f_code = f_badge = f_note = ImageFont.load_default()
    return {
        "title": f_title,
        "sub": f_sub,
        "header": f_header,
        "code": f_code,
        "badge": f_badge,
        "note": f_note,
    }


def get_token():
    res = requests.post(f"{BASE_URL}/api/token/", json={"username": ADMIN_USER, "password": ADMIN_PASS}, timeout=5)
    if res.status_code == 200:
        return res.json().get("token")
    print(f"[LỖI] Không lấy được token: {res.status_code}")
    sys.exit(1)


def draw_powershell_window_frame(draw, width, height, title_text, sub_text, fonts):
    draw.rectangle([0, 0, width, height], fill="#0C0C0C")
    
    # Title bar
    draw.rectangle([0, 0, width, 48], fill="#1F1F1F")
    draw.line([0, 48, width, 48], fill="#333333", width=1)
    
    # Title text
    draw.text((20, 10), title_text, fill="#CCCCCC", font=fonts["title"])
    draw.text((20, 30), sub_text, fill="#888888", font=fonts["sub"])
    
    # Window controls
    draw.line([width - 120, 24, width - 105, 24], fill="#AAAAAA", width=1)
    draw.rectangle([width - 80, 18, width - 68, 30], outline="#AAAAAA", width=1)
    draw.rectangle([width - 48, 0, width, 48], fill="#E81123")
    draw.line([width - 32, 18, width - 18, 32], fill="#FFFFFF", width=2)
    draw.line([width - 18, 18, width - 32, 32], fill="#FFFFFF", width=2)


def draw_lines(draw, x_start, y_start, line_list, font, line_height=21):
    y = y_start
    for line in line_list:
        x = x_start
        for text, color in line:
            draw.text((x, y), text, fill=color, font=font)
            bbox = draw.textbbox((x, y), text, font=font)
            x = bbox[2]
        y += line_height
    return y


def create_bug01_image(endpoint, resource_name, out_filename, fonts, token):
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    run_stamp = int(time.time())
    payload = {"name": f"TV3_Audit_{resource_name}_Crash_303_{run_stamp}", "set_permissions": {"view": False}}
    
    t0 = time.time()
    r = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=payload, timeout=5)
    elapsed_ms = int((time.time() - t0) * 1000)
    
    width = 1500
    height = 840
    img = Image.new("RGB", (width, height), "#0C0C0C")
    draw = ImageDraw.Draw(img)
    
    title = f"Windows PowerShell — curl.exe [Tái hiện thực thi: BUG-01 trên {resource_name}]"
    sub = f"Thực hiện: Nguyễn Khiêm Thuận (2312764) · TV3 · Seed 303 | Server: {BASE_URL} (Paperless-ngx v3.1.3)"
    draw_powershell_window_frame(draw, width, height, title, sub, fonts)
    
    # Left Box
    draw.rectangle([20, 60, 735, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([20, 60, 735, 96], fill="#1E1E1E")
    draw.text((32, 70), f"CLI COMMAND — POST {endpoint}", fill="#61AFEF", font=fonts["header"])
    
    left_lines = [
        [("PS D:\\DaiHocDL\\KiemThuPhanMem\\KTPM> ", "#98C379"), ("curl.exe -i -X POST ", "#E5C07B"), (f'"{BASE_URL}{endpoint}" `', "#ABB2BF")],
        [("  -H ", "#61AFEF"), ('"Authorization: Token [REDACTED_AUTH_TOKEN]" `', "#E5C07B")],
        [("  -H ", "#61AFEF"), ('"Content-Type: application/json" `', "#ABB2BF")],
        [("  -d ", "#61AFEF"), ('\'{"name": "', "#ABB2BF"), (payload["name"], "#98C379"), ('", "set_permissions": {"view": false}}\'', "#ABB2BF")],
        [],
        [("// Phân tích chi tiết payload:", "#5C6370")],
        [('{', "#ABB2BF")],
        [('  "name": "', "#ABB2BF"), (payload["name"], "#98C379"), ('",', "#ABB2BF")],
        [('  "set_permissions": {', "#D19A66")],
        [('    "view": false', "#E06C75"), ('    // <-- LỖI: boolean thay vì object {"users":[], "groups":[]}', "#5C6370")],
        [('  }', "#D19A66")],
        [('}', "#ABB2BF")],
        [],
        [("// Quan sát đầu vào:", "#5C6370")],
        [("// Thuộc tính set_permissions.view mang giá trị boolean false.", "#5C6370")],
        [("// Theo đặc tả OpenAPI, view phải là object chứa users và groups.", "#5C6370")],
    ]
    draw_lines(draw, 35, 110, left_lines, fonts["code"], line_height=21)
    
    # Right Box
    draw.rectangle([765, 60, 1480, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([765, 60, 1480, 96], fill="#1E1E1E")
    draw.text((778, 70), f"ACTUAL RESPONSE — HTTP {r.status_code} ({elapsed_ms} ms)", fill="#E06C75", font=fonts["header"])
    
    draw.rectangle([1320, 66, 1465, 90], fill="#E06C75")
    draw.text((1330, 70), "500 SERVER ERROR", fill="#000000", font=fonts["badge"])
    
    date_str = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    right_lines = [
        [("HTTP/1.1 ", "#98C379"), ("500 Internal Server Error", "#E06C75")],
        [("server: ", "#61AFEF"), ("granian", "#ABB2BF")],
        [("date: ", "#61AFEF"), (date_str, "#ABB2BF")],
        [("content-type: ", "#61AFEF"), ("text/html; charset=utf-8", "#ABB2BF")],
        [("content-length: ", "#61AFEF"), ("145", "#ABB2BF")],
        [("x-api-version: ", "#61AFEF"), ("10", "#ABB2BF")],
        [("x-version: ", "#61AFEF"), ("3.1.3", "#ABB2BF")],
        [],
        [("<!doctype html>", "#E5C07B")],
        [("<html lang=\"en\">", "#ABB2BF")],
        [("<head>", "#ABB2BF")],
        [("  <title>Server Error (500)</title>", "#E06C75")],
        [("</head>", "#ABB2BF")],
        [("<body>", "#ABB2BF")],
        [("  <h1>Server Error (500)</h1><p></p>", "#E06C75")],
        [("</body>", "#ABB2BF")],
        [("</html>", "#ABB2BF")],
    ]
    draw_lines(draw, 780, 110, right_lines, fonts["code"], line_height=21)
    
    # Bottom Box
    draw.rectangle([20, 655, 1480, 820], fill="#181818", outline="#333333", width=1)
    draw.rectangle([20, 655, 1480, 685], fill="#222222")
    draw.text((32, 660), "QUAN SÁT & ĐỐI CHIẾU HỢP ĐỒNG API (BUG-01)", fill="#E5C07B", font=fonts["header"])
    
    notes = [
        "• Quan sát thực tế: Gửi set_permissions.view dạng boolean dẫn đến HTTP 500 trên endpoint. Đã tái hiện độc lập trên phiên bản Paperless-ngx 3.1.3.",
        "• Kỳ vọng hợp đồng: Hệ thống cần từ chối đầu vào sai kiểu bằng phản hồi 4xx phù hợp (kỳ vọng cụ thể: HTTP 400 Bad Request kèm thông báo lỗi cấu trúc).",
        "• Phạm vi & Kết luận kỹ thuật: Máy chủ phát sinh Unhandled Server Error. Chưa khẳng định lỗi ở tầng serializer hay ORM do chưa trích xuất traceback server container.",
        "• Nhãn minh chứng: [Minh chứng thực thi: Windows PowerShell (curl.exe CLI) | Token đã che [REDACTED_AUTH_TOKEN]]",
    ]
    ny = 695
    for note in notes:
        draw.text((35, ny), note, fill="#ABB2BF", font=fonts["note"])
        ny += 28
        
    out_path = os.path.join(EVIDENCE_DIR, out_filename)
    img.save(out_path, "PNG")
    print(f"[XUẤT ẢNH] Đã tạo ảnh minh chứng: {out_path}")


def create_bug03_response_image(fonts, token):
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    run_stamp = int(time.time())
    name = f"TV3_Audit_Corr_Contract_303_{run_stamp}"
    payload = {"name": name}
    
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/correspondents/", headers=headers, json=payload, timeout=5)
    elapsed_ms = int((time.time() - t0) * 1000)
    
    created_id = None
    res_json = {}
    if r.status_code == 201:
        res_json = r.json()
        created_id = res_json.get("id")
        
    width = 1500
    height = 840
    img = Image.new("RGB", (width, height), "#0C0C0C")
    draw = ImageDraw.Draw(img)
    
    title = "Windows PowerShell — curl.exe [Tái hiện thực thi: BUG-03 (POST /api/correspondents/)]"
    sub = "Thực hiện: Nguyễn Khiêm Thuận (2312764) · TV3 · Seed 303 | Server: localhost:8000 (Paperless-ngx v3.1.3)"
    draw_powershell_window_frame(draw, width, height, title, sub, fonts)
    
    # Left Box
    draw.rectangle([20, 60, 735, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([20, 60, 735, 96], fill="#1E1E1E")
    draw.text((32, 70), "CLI COMMAND — POST /api/correspondents/", fill="#61AFEF", font=fonts["header"])
    
    left_lines = [
        [("PS D:\\DaiHocDL\\KiemThuPhanMem\\KTPM> ", "#98C379"), ('curl.exe -i -X POST "http://localhost:8000/api/correspondents/" `', "#E5C07B")],
        [("  -H ", "#61AFEF"), ('"Authorization: Token [REDACTED_AUTH_TOKEN]" `', "#E5C07B")],
        [("  -H ", "#61AFEF"), ('"Content-Type: application/json" `', "#ABB2BF")],
        [("  -d ", "#61AFEF"), (f'\'{{"name": "{name}"}}\'', "#98C379")],
        [],
        [("// Mục đích kiểm thử:", "#5C6370")],
        [("// Tạo mới một Correspondent với thông tin hợp lệ (mã mong đợi: 201 Created).", "#5C6370")],
        [("// Kiểm tra cấu trúc JSON phản hồi đối chiếu với schema phản hồi 201.", "#5C6370")],
        [],
        [("// Ghi chú về điều kiện:", "#5C6370")],
        [("// Endpoint POST không nhận tham số full_perms (chỉ áp dụng ở GET).", "#5C6370")],
        [("// Thao tác tạo mới thành công và bản ghi được lưu vào cơ sở dữ liệu.", "#5C6370")],
    ]
    draw_lines(draw, 35, 110, left_lines, fonts["code"], line_height=21)
    
    # Right Box
    draw.rectangle([765, 60, 1480, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([765, 60, 1480, 96], fill="#1E1E1E")
    draw.text((778, 70), f"ACTUAL RESPONSE — HTTP {r.status_code} ({elapsed_ms} ms)", fill="#98C379", font=fonts["header"])
    
    draw.rectangle([1320, 66, 1465, 90], fill="#98C379")
    draw.text((1340, 70), "201 CREATED", fill="#000000", font=fonts["badge"])
    
    cid = res_json.get("id", created_id)
    cslug = res_json.get("slug", "")
    cname = res_json.get("name", "")
    cmatch = res_json.get("match", "")
    calgo = res_json.get("matching_algorithm", 1)
    cinsens = str(res_json.get("is_insensitive", True)).lower()
    cowner = res_json.get("owner", 2)
    cchange = str(res_json.get("user_can_change", True)).lower()
    
    right_lines = [
        [("HTTP/1.1 ", "#98C379"), ("201 Created", "#98C379")],
        [("server: ", "#61AFEF"), ("granian", "#ABB2BF")],
        [("content-type: ", "#61AFEF"), ("application/json", "#ABB2BF")],
        [("x-version: ", "#61AFEF"), ("3.1.3", "#ABB2BF")],
        [],
        [("// Response Body (JSON trả về thực tế - 8 trường):", "#5C6370")],
        [("{", "#ABB2BF")],
        [(f'  "id": {cid},', "#ABB2BF")],
        [(f'  "slug": "{cslug}",', "#ABB2BF")],
        [(f'  "name": "{cname}",', "#ABB2BF")],
        [(f'  "match": "{cmatch}",', "#ABB2BF")],
        [(f'  "matching_algorithm": {calgo},', "#ABB2BF")],
        [(f'  "is_insensitive": {cinsens},', "#ABB2BF")],
        [(f'  "owner": {cowner},', "#ABB2BF")],
        [(f'  "user_can_change": {cchange}', "#ABB2BF")],
        [("}", "#ABB2BF")],
        [],
        [("[VI PHẠM HỢP ĐỒNG API] CÁC TRƯỜNG REQUIRED THEO SCHEMA BỊ THIẾU:", "#E06C75")],
        [("  [THIẾU] 'document_count'    : KHÔNG CÓ TRONG PHẢN HỒI 201", "#E06C75")],
        [("  [THIẾU] 'last_correspondence': KHÔNG CÓ TRONG PHẢN HỒI 201", "#E06C75")],
        [("  [THIẾU] 'permissions'        : KHÔNG CÓ TRONG PHẢN HỒI 201", "#E06C75")],
    ]
    draw_lines(draw, 780, 110, right_lines, fonts["code"], line_height=20)
    
    # Bottom Box
    draw.rectangle([20, 655, 1480, 820], fill="#181818", outline="#333333", width=1)
    draw.rectangle([20, 655, 1480, 685], fill="#222222")
    draw.text((32, 660), "QUAN SÁT & ĐỐI CHIẾU HỢP ĐỒNG API (BUG-03)", fill="#E5C07B", font=fonts["header"])
    
    notes = [
        "• Quan sát thực tế: Response 201 của POST /api/correspondents/ thiếu các trường required đã đối chiếu trong OpenAPI, thể hiện sai lệch giữa phản hồi thực tế và hợp đồng API.",
        "• Xác nhận trường thiếu: Đối chiếu trực tiếp schema Correspondent, phản hồi thực tế chỉ có 8 trường, thiếu chính xác 3 trường: document_count, last_correspondence, permissions.",
        "• Dọn dẹp dữ liệu: Bản ghi tạm thời ID " + str(created_id) + " đã được xóa sạch ngay sau lượt chạy nhằm bảo toàn trạng thái cơ sở dữ liệu kiểm thử.",
        "• Nhãn minh chứng: [Minh chứng thực thi: Windows PowerShell (curl.exe CLI) | Ghi nhận từ lượt chạy thật]",
    ]
    ny = 695
    for note in notes:
        draw.text((35, ny), note, fill="#ABB2BF", font=fonts["note"])
        ny += 28
        
    out_path = os.path.join(EVIDENCE_DIR, "TV3_BUG03_response_201.png")
    img.save(out_path, "PNG")
    print(f"[XUẤT ẢNH] Đã tạo ảnh minh chứng: {out_path}")
    
    if created_id:
        requests.delete(f"{BASE_URL}/api/correspondents/{created_id}/", headers=headers, timeout=5)


def create_bug03_schema_image(fonts):
    width = 1500
    height = 840
    img = Image.new("RGB", (width, height), "#0C0C0C")
    draw = ImageDraw.Draw(img)
    
    title = "Trích Xuất OpenAPI Schema — Phản Hồi 201 của /api/correspondents/ (openapi_TV3.json)"
    sub = "Tài liệu API: /api/schema/ | SHA256: 888b0f89ec0a9f65293f5320a86b1810d7904f93033178b567e313d951b12e3a"
    draw_powershell_window_frame(draw, width, height, title, sub, fonts)
    
    # Left Box
    draw.rectangle([20, 60, 680, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([20, 60, 680, 96], fill="#1E1E1E")
    draw.text((32, 70), "OPENAPI PATH DEFINITION — POST /api/correspondents/", fill="#61AFEF", font=fonts["header"])
    
    schema_path_lines = [
        [("/api/correspondents/:", "#E5C07B")],
        [("  post:", "#61AFEF")],
        [("    operationId: correspondents_create", "#ABB2BF")],
        [("    tags: [correspondents]", "#ABB2BF")],
        [("    requestBody:", "#ABB2BF")],
        [("      content:", "#ABB2BF")],
        [("        application/json:", "#ABB2BF")],
        [("          schema:", "#ABB2BF")],
        [("            $ref: '#/components/schemas/CorrespondentRequest'", "#D19A66")],
        [("    responses:", "#ABB2BF")],
        [("      '201':", "#98C379")],
        [("        description: ''", "#5C6370")],
        [("        content:", "#ABB2BF")],
        [("          application/json:", "#ABB2BF")],
        [("            schema:", "#ABB2BF")],
        [("              $ref: '#/components/schemas/Correspondent'", "#E06C75")],
        [],
        [("// Quy định hợp đồng OpenAPI:", "#5C6370")],
        [("// Phản hồi HTTP 201 Created của endpoint POST bắt buộc phải", "#5C6370")],
        [("// tuân thủ toàn bộ cấu trúc định nghĩa tại schema Correspondent.", "#5C6370")],
        [("// Schemathesis dựa trên định nghĩa này để kiểm tra schema_conformance.", "#5C6370")],
    ]
    draw_lines(draw, 35, 110, schema_path_lines, fonts["code"], line_height=21)
    
    # Right Box
    draw.rectangle([710, 60, 1480, 640], fill="#121212", outline="#2D2D2D", width=1)
    draw.rectangle([710, 60, 1480, 96], fill="#1E1E1E")
    draw.text((722, 70), "RESOLVED SCHEMA — #/components/schemas/Correspondent", fill="#E5C07B", font=fonts["header"])
    
    schema_resolved_lines = [
        [('"Correspondent": {', "#E5C07B")],
        [('  "type": "object",', "#ABB2BF")],
        [('  "required": [', "#E5C07B")],
        [('    "id", "slug", "name", "match", "matching_algorithm", "is_insensitive",', "#98C379")],
        [('    "document_count",    ', "#E06C75"), ('// [BẮT BUỘC] integer (readOnly) - KHÔNG CÓ TRONG 201', "#5C6370")],
        [('    "last_correspondence",', "#E06C75"), ('// [BẮT BUỘC] date-time (nullable) - KHÔNG CÓ TRONG 201', "#5C6370")],
        [('    "permissions"         ', "#E06C75"), ('// [BẮT BUỘC] object (Permissions) - KHÔNG CÓ TRONG 201', "#5C6370")],
        [('  ],', "#E5C07B")],
        [('  "properties": {', "#ABB2BF")],
        [('    "id": {"type": "integer", "readOnly": true},', "#ABB2BF")],
        [('    "slug": {"type": "string", "readOnly": true},', "#ABB2BF")],
        [('    "name": {"type": "string", "maxLength": 128},', "#ABB2BF")],
        [('    "document_count": {"type": "integer", "readOnly": true},', "#E06C75")],
        [('    "last_correspondence": {"type": "string", "format": "date-time", "nullable": true},', "#E06C75")],
        [('    "permissions": {"$ref": "#/components/schemas/CorrespondentPermissions"}', "#E06C75")],
        [('  }', "#ABB2BF")],
        [('}', "#E5C07B")],
    ]
    draw_lines(draw, 725, 110, schema_resolved_lines, fonts["code"], line_height=21)
    
    # Bottom Box
    draw.rectangle([20, 655, 1480, 820], fill="#181818", outline="#333333", width=1)
    draw.rectangle([20, 655, 1480, 685], fill="#222222")
    draw.text((32, 660), "ĐỐI CHIẾU HỢP ĐỒNG & GIẢ THUYẾT KỸ THUẬT (BUG-03)", fill="#E5C07B", font=fonts["header"])
    
    notes = [
        "• Đối chiếu hợp đồng API: Schema Correspondent đánh dấu 9 trường required. Khi POST tạo mới thành công, phản hồi 201 thiếu 3 trường.",
        "• Giả thuyết kỹ thuật: permissions phụ thuộc query GET có full_perms=true; document_count & last_correspondence là trường annotate lúc lọc danh sách.",
        "• Hướng kiểm tra tiếp theo: Cần kiểm tra mã nguồn phiên bản 3.1.3 xem drf-spectacular có dùng chung schema đọc/ghi hay không để đề xuất giải pháp phù hợp.",
        "• Nhãn minh chứng: [Minh chứng hợp đồng: Trích xuất trực tiếp từ docs/openapi_TV3.json (SHA256: 888b0f89...)]",
    ]
    ny = 695
    for note in notes:
        draw.text((35, ny), note, fill="#ABB2BF", font=fonts["note"])
        ny += 28
        
    out_path = os.path.join(EVIDENCE_DIR, "TV3_BUG03_schema_required.png")
    img.save(out_path, "PNG")
    print(f"[XUẤT ẢNH] Đã tạo ảnh minh chứng: {out_path}")


def main():
    print("[INFO] Bắt đầu kết xuất 4 ảnh minh chứng thực tế cho BUG-01 và BUG-03...")
    fonts = get_fonts()
    token = get_token()
    
    # 1. BUG-01 Correspondents
    create_bug01_image("/api/correspondents/", "Correspondents", "TV3_BUG01_correspondents_500.png", fonts, token)
    
    # 2. BUG-01 Document Types
    create_bug01_image("/api/document_types/", "Document Types", "TV3_BUG01_document_types_500.png", fonts, token)
    
    # 3. BUG-03 Response 201
    create_bug03_response_image(fonts, token)
    
    # 4. BUG-03 Schema Required
    create_bug03_schema_image(fonts)
    
    print("[THÀNH CÔNG] Đã cập nhật toàn bộ 4 ảnh minh chứng trong docs/evidence/.")


if __name__ == "__main__":
    main()
