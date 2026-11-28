#!/usr/bin/env python3
"""
scripts/generate_sample_pdfs_TV3.py
Tạo 8 file PDF mẫu bổ sung cho TV3 (Nguyễn Khiêm Thuận - MSSV 2312764 - Seed 303)
Sử dụng thư viện ReportLab để sinh tài liệu PDF có nội dung chữ rõ ràng.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def create_sample_pdfs():
    out_dir = Path("scripts/sample_docs")
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_definitions = [
        (
            "TV3_Sample_01_Report_303.pdf",
            "BAO CAO KIEM THU PHAN MEM SCHEMATHESIS",
            [
                "Hoc phan: Kiem thu phan mem - Nhom 5",
                "Thanh vien thuc hien: Nguyen Khiem Thuan (TV3) - MSSV: 2312764",
                "Seed kiem thu: 303 | Pham vi: Phan D-E REST API Fuzzing",
                "He thong muc tieu: Paperless-ngx v3.1.3",
                "Noi dung: Danh gia tuan thu dac ta OpenAPI, loi 5xx va validation.",
            ],
        ),
        (
            "TV3_Sample_02_Invoice_303.pdf",
            "HOA DON DICH VU DIEN TOAN DAM MAY",
            [
                "Ma hoa don: HD-CLOUD-303-2026",
                "Khach hang: Nguyen Khiem Thuan - 2312764",
                "Don vi phat hanh: Dich vu Ha tang Kiem thu DL",
                "So tien thanh toan: 3.030.000 VND",
                "Trang thai: Da thanh toan thanh cong qua chuyen khoan ngan hang.",
            ],
        ),
        (
            "TV3_Sample_03_Contract_303.pdf",
            "HOP DONG CUNG CAP PHAN MEM VA DICH VU KIEM THU",
            [
                "So hop dong: HD-KTPM-303/2026",
                "Ben A: Dai dien nghien cuu phan mem TV3 Nguyen Khiem Thuan",
                "Ben B: Don vi doi tac thu nghiem he thong",
                "Pham vi cong viec: Fuzzing API tu dong bang Schemathesis seed 303.",
                "Thoi han thuc hien: Thang 10 nam 2026.",
            ],
        ),
        (
            "TV3_Sample_04_Receipt_303.pdf",
            "BIEN LAI THU PHI KIEM THU CHAT LUONG",
            [
                "Bien lai so: BL-303-764",
                "Nguoi nop tien: Nguyen Khiem Thuan",
                "Ly do thu: Phi tham dinh he thong Paperless-ngx",
                "So tien: 500.000 VND",
                "Ngay thu tien: 13/10/2026.",
            ],
        ),
        (
            "TV3_Sample_05_Memo_303.pdf",
            "THONG BAO NOI BO VE KE HOACH TEST 3 VONG",
            [
                "Kinh gui: Cac thanh vien nhom Kiem thu phan mem",
                "Nguoi gui: TV3 - Nguyen Khiem Thuan - Seed 303",
                "Noi dung: Ke hoach thuc hien Vong 1 (GET allowlist), Vong 2 (CRUD nhom 1),",
                "va Vong 3 (Full CRUD ket hop Documents).",
                "Yeu cau: Dam bao baseline truoc moi vong test.",
            ],
        ),
        (
            "TV3_Sample_06_Proposal_303.pdf",
            "DE XUAT PHUONG AN PROPERTY-BASED TESTING",
            [
                "De an: Ung dung Schemathesis va Hypothesis trong phat hien loi API",
                "Tac gia: Nguyen Khiem Thuan (2312764)",
                "Muc tieu: Tu dong sinh input ngau nhien theo rang buoc OpenAPI.",
                "Giai phap: Phat hien loi unhandled exception 500 va vi pham schema.",
            ],
        ),
        (
            "TV3_Sample_07_Specification_303.pdf",
            "TAI LIEU DAC TA RANG BUOC API PAPERLESS-NGX",
            [
                "Tai nguyen xem xet: Tags, Correspondents, Document Types, Documents",
                "Rang buoc do dai: name toi da 128 ky tu",
                "Rang buoc duy nhat: UniqueConstraint (name, owner)",
                "Chuan phan hoi: 201 Created khi tao moi, 400 Bad Request khi sai du lieu.",
            ],
        ),
        (
            "TV3_Sample_08_Certificate_303.pdf",
            "GIAY CHUNG NHAN HOAN THANH QUY TRINH KIEM THU",
            [
                "Chung nhan sinh vien: Nguyen Khiem Thuan - MSSV: 2312764",
                "Da hoan thanh toan bo 3 vong kiem thu Schemathesis va 3 luong nghiep vu",
                "Seed xac thuc: 303",
                "He thong: Paperless-ngx 3.1.3 tren Docker Windows localhost.",
            ],
        ),
    ]

    for fname, title, lines in pdf_definitions:
        fpath = out_dir / fname
        c = canvas.Canvas(str(fpath), pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, 720, title)
        c.setFont("Helvetica", 10)
        y = 680
        for line in lines:
            c.drawString(72, y, line)
            y -= 22
        c.save()
        print(f"[OK] Da tao file PDF: {fpath.name} ({fpath.stat().st_size} bytes)")


if __name__ == "__main__":
    create_sample_pdfs()
