# TV1 — 3 luồng nghiệp vụ chạy được (Phần C, kèm bằng chứng)

> Mỗi thành viên tự chạy 3 luồng này trên máy mình và chụp ảnh/quay video.
> Dưới đây là kịch bản chuẩn + lệnh API tương đương để ai cũng tái hiện được.

## Luồng 1 — Upload tài liệu và OCR

**Thao tác UI:**
1. Đăng nhập http://localhost:8000 → Dashboard.
2. Kéo-thả `seed/seed_01_hoa_don_dien.pdf` vào Dashboard.
3. Đợi 30–90 s → mở tài liệu → tab **Content** hiện đúng câu
   "Hoa don tien dien thang 9/2026 …" → OCR thành công.
4. Chụp ảnh: màn hình danh sách + nội dung Content.

**Tương đương API:**
```bash
curl -s -X POST http://localhost:8000/api/documents/post_document/ \
  -H "Authorization: Token $TOKEN" \
  -F "document=@seed/seed_01_hoa_don_dien.pdf" | head -c 300
# kỳ vọng: 200/201, trả về task id; sau ~60s GET /api/documents/ thấy tài liệu mới
```

## Luồng 2 — Tạo tag / correspondent và gắn vào tài liệu

**Thao tác UI:**
1. Settings → Tags → New → tên `hoa-don` → Save.
2. Settings → Correspondents → New → tên `Dien Luc Da Lat` → Save.
3. Mở tài liệu ở Luồng 1 → gán tag `hoa-don` + correspondent → Save.
4. Chụp ảnh: trang edit hiển thị tag + correspondent đã gán.

**Tương đương API (cũng là cách `seed_api.py` làm):**
```bash
curl -s -X POST http://localhost:8000/api/tags/ \
  -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"hoa-don"}'
curl -s -X POST http://localhost:8000/api/correspondents/ \
  -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Dien Luc Da Lat"}'
DOC_ID=1  # thay bằng id thật từ GET /api/documents/
curl -s -X PATCH http://localhost:8000/api/documents/$DOC_ID/ \
  -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  -d '{"tags":[1],"correspondent":1}'
# kỳ vọng: 200 OK; GET lại tài liệu thấy tags/correspondent đã gắn
```

## Luồng 3 — Tìm kiếm và lọc tài liệu

**Thao tác UI:**
1. Ô Search gõ `dien` → kết quả trả về đúng hóa đơn điện (tìm toàn văn trên nội dung OCR).
2. Bật bộ lọc Tags = `hoa-don` → danh sách chỉ còn tài liệu đã gắn tag.
3. Chụp ảnh/video: kết quả search + bộ lọc.

**Tương đương API:**
```bash
curl -s "http://localhost:8000/api/documents/?query=dien" \
  -H "Authorization: Token $TOKEN" | head -c 500
# kỳ vọng: 200, results chứa seed_01
curl -s "http://localhost:8000/api/documents/?tags__id__in=1" \
  -H "Authorization: Token $TOKEN" | head -c 500
# kỳ vọng: 200, mọi item đều có tag id 1
```

## Checklist bằng chứng (mỗi người)

- [ ] Ảnh 1: Dashboard sau khi upload + OCR xong (thấy text Content)
- [ ] Ảnh 2: Tag `hoa-don` + correspondent gắn trên tài liệu
- [ ] Ảnh 3: Kết quả search `dien` + lọc theo tag
- [ ] (Khuyên) 1 video 2–3 phút chạy liền 3 luồng, đề phòng demo trực tiếp lỗi ngày 20/10
