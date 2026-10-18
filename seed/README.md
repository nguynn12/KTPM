# Bộ seed chung của nhóm (TV1 chuẩn bị)

Mục tiêu: **5 máy — cùng 1 bộ dữ liệu ban đầu** để số liệu Schemathesis so sánh được.

## Gồm những gì

| File | Nội dung |
|---|---|
| `seed_01_hoa_don_dien.pdf` … `seed_06_bao_cao_tuan.pdf` | 6 PDF mẫu 1 trang, có text thật (không scan ảnh) để OCR/consume luôn thành công; không chứa thông tin cá nhân |
| `seed_api.py` | Tạo qua REST API: 3 tag, 2 correspondent, 2 document type **giống nhau** trên mọi máy |
| `generate_seed.py` / `generate_seed.ps1` | Sinh lại 6 PDF (PDF 1.4 tối giản, ASCII thuần) khi cần |

Danh mục mẫu do `seed_api.py` tạo:

- Tags: `hoa-don`, `can-xu-ly`, `luu-tru-lau-dai`
- Correspondents: `Dien Luc Da Lat`, `Phong Ke Toan`
- Document types: `Hoa don`, `Bao cao`

## Cách dùng (sau khi `docker compose up -d` và tạo admin)

```bash
# 1. Upload 6 PDF (chọn 1 trong 2 cách):
cp seed/*.pdf consume/        # hệ thống tự nuốt trong ~60s
# hoặc kéo-thả từng file vào giao diện web http://localhost:8000

# 2. Tạo metadata mẫu giống nhau:
pip install requests
python3 seed/seed_api.py --base-url http://localhost:8000 --username <ADMIN> --password <MK>
```

## Sinh lại PDF khi cần

```bash
python3 seed/generate_seed.py          # Linux/macOS/WSL
# hoặc trên PowerShell thuần:
powershell -ExecutionPolicy Bypass -File seed/generate_seed.ps1
```

## Lưu ý

- Không bỏ file `.env` thật, token hay mật khẩu admin vào thư mục này.
- Muốn test tiếng Việt: thêm PDF tiếng Việt + đặt `PAPERLESS_OCR_LANGUAGE=vie`
  (cần `docker compose up -d` lại để container cài gói `tesseract-ocr-vie`).
