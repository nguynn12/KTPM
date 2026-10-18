# SEED_DATA_TV1 — Bộ seed chung của nhóm (TV1 chuẩn bị)

Mục tiêu: **5 máy – cùng 1 bộ dữ liệu ban đầu** để số liệu Schemathesis so sánh được.

## Gồm những gì

| File | Nội dung |
|---|---|
| `scripts/sample_docs/TV1_Sample_0{1..6}_*_101.pdf` | 6 PDF mẫu 1 trang, có text thật (không scan ảnh) để OCR/consume luôn thành công; không chứa thông tin cá nhân |
| `scripts/seed_and_verify_flows_TV1.py` | Tạo qua REST API: 3 tag, 2 correspondent, 2 document type **giống nhau** trên mỗi máy |
| `scripts/generate_sample_pdfs_TV1.py` / `.ps1` | Sinh lại 6 PDF (PDF 1.4 tối giản, ASCII thuần) khi cần |

6 file PDF mẫu (đặt trong `scripts/sample_docs/`, theo quy ước `TV1_Sample_<số>_<tên>_101.pdf`):

| File | Nội dung nhúng trong PDF |
|---|---|
| `TV1_Sample_01_HoaDon_101.pdf` | Hóa đơn tiền điện 9/2026 — Dien Luc Da Lat — 452.300 VND |
| `TV1_Sample_02_HopDong_101.pdf` | Hợp đồng dịch vụ vệ sinh văn phòng — DV-2026-041 |
| `TV1_Sample_03_BaoCao_101.pdf` | Báo cáo tuần 41 — nhóm KTPM |
| `TV1_Sample_04_BienBanHop_101.pdf` | Biên bản họp nhóm 10/10/2026 |
| `TV1_Sample_05_PhieuThu_101.pdf` | Phiếu thu PT-118 — 2.000.000 VND |
| `TV1_Sample_06_HuongDanScan_101.pdf` | Hướng dẫn scan tài liệu (PDF ≥ 300 DPI) |

Danh mục mẫu do `scripts/seed_and_verify_flows_TV1.py` tạo:

- Tags: `hoa-don`, `can-xu-ly`, `luu-tru-lau-dai`
- Correspondents: `Dien Luc Da Lat`, `Phong Ke Toan`
- Document types: `Hoa don`, `Bao cao`

## Cách dùng (sau khi `docker compose up -d` và tạo admin)

```bash
# 1. Upload 6 PDF (chọn 1 trong 2 cách):
cp scripts/sample_docs/*.pdf consume/        # hệ thống tự nuốt trong ~60s
# hoặc kéo-thả từng file vào giao diện web http://localhost:8000

# 2. Tạo metadata mẫu giống nhau:
pip install requests
python3 scripts/seed_and_verify_flows_TV1.py --base-url http://localhost:8000 --username <ADMIN> --password <MK>
```

## Sinh lại PDF khi cần

```bash
python3 scripts/generate_sample_pdfs_TV1.py          # Linux/macOS/WSL
# hoặc trên PowerShell thuần (không cần Python):
powershell -ExecutionPolicy Bypass -File scripts/generate_sample_pdfs_TV1.ps1
```

Cả 2 script ghi file vào `scripts/sample_docs/`.

## Lưu ý

- Không để file `.env` thật, token hay mật khẩu admin vào thư mục này.
- Đây là seed **101** của TV1; TV2 dùng seed 202 (`scripts/sample_docs/TV2_Sample_*.txt`), TV3 dùng seed 303.
- Muốn test tiếng Việt: thêm PDF tiếng Việt + đặt `PAPERLESS_OCR_LANGUAGE=vie`
  (cần `docker compose up -d` lại để container cài gói `tesseract-ocr-vie`).
