#!/usr/bin/env python3
"""Sinh lại 6 PDF seed tối giản (PDF 1.4, text ASCII) — TV1.
Chạy: python3 scripts/generate_sample_pdfs_TV1.py  (ghi vào scripts/sample_docs/)
Không cần thư viện ngoài.
"""
from pathlib import Path

DOCS = [
    ("TV1_Sample_01_HoaDon_101.pdf", "Hoa don tien dien thang 9/2026 - Dien Luc Da Lat - So tien: 452.300 VND - Han thanh toan: 15/10/2026."),
    ("TV1_Sample_02_HopDong_101.pdf", "Hop dong dich vu ve sinh van phong - So HD: DV-2026-041 - Thoi han: 12 thang - Ben cung cap: Cong ty Sach Dep."),
    ("TV1_Sample_03_BaoCao_101.pdf", "Bao cao tuan 41 - Nhom KTPM - Hoan thanh: cai dat moi truong, upload tai lieu mau - Tuan toi: chay Schemathesis vong 1."),
    ("TV1_Sample_04_BienBanHop_101.pdf", "Bien ban hop nhom ngay 10/10/2026 - Noi dung: chot tag v3.1.3, phan cong 5 thanh vien, lap repo Git chung."),
    ("TV1_Sample_05_PhieuThu_101.pdf", "Phieu thu so PT-118 - Nguoi nop: Nguyen Van A - So tien: 2.000.000 VND - Ly do: tam ung van phong pham."),
    ("TV1_Sample_06_HuongDanScan_101.pdf", "Huong dan scan tai lieu - Dinh dang: PDF, toi thieu 300 DPI - Dat ten file theo mau: YYYY-MM-DD-noi-dung.pdf."),
]

def make_pdf(text: str) -> bytes:
    text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        "<< /Length %d >>\nstream\nBT /F1 14 Tf 72 720 Td 80 TL (%s) Tj ET\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    stream_body = f"BT /F1 14 Tf 72 720 Td 80 TL ({text}) Tj ET"
    objs[3] = objs[3] % (len(stream_body.encode("latin-1")) + 1, text)
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode("latin-1")
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("latin-1")
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode("latin-1")
    return bytes(out)

def main() -> None:
    dest = Path(__file__).parent / "sample_docs"
    for name, text in DOCS:
        (dest / name).write_bytes(make_pdf(text))
        print(f"wrote {name} ({(dest / name).stat().st_size} bytes)")

if __name__ == "__main__":
    main()
