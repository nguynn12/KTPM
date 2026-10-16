# BẰNG CHỨNG BA LUỒNG NGHIỆP VỤ THỰC TẾ — TV3

**Thành viên:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303  
**Thời gian thực hiện:** 2026-10-13 11:56:41  
**Môi trường:** Paperless-ngx v3.1.3 trên Docker Windows local (`http://localhost:8000`)  
**Tài khoản thực hiện:** `admin` (xác thực token tự động qua local API, token an toàn không lưu)

---

## 1. Dữ liệu nền đã nạp (Group Baseline)
- **Tags nền:** 4 (`TV2_Tag_Invoice_202`, `TV2_Tag_Urgent_202`, `TV2_Tag_Archive_202`, `TV2_Tag_Finance_202`)
- **Correspondents nền:** 3 (`TV2_Bank_202`, `TV2_Supplier_202`, `TV2_University_202`)
- **Document Types nền:** 3 (`TV2_DocType_Invoice_202`, `TV2_DocType_Receipt_202`, `TV2_DocType_Contract_202`)
- **Tài liệu TXT nền:** 2 (`TV2_Sample_Invoice_202.txt`, `TV2_Sample_Contract_202.txt`)
- **Bộ PDF bổ sung TV3:** 8 tệp PDF mẫu sinh bằng ReportLab trong `scripts/sample_docs/`

---

## 2. Chi tiết thực thi 3 Luồng nghiệp vụ

### Luồng 1 (TV3-FLOW-01): Upload PDF -> Chờ Celery Task -> GET chi tiết và kiểm tra Content
- **Tệp upload:** `scripts/sample_docs/TV3_Sample_01_Report_303.pdf`
- **Endpoint gọi:** `POST /api/documents/post_document/`
- **HTTP Status:** `200`
- **Task UUID nhận được:** `ea3629b6-2918-43fa-94d9-6366fee4a86c`
- **Kết quả Task:** `SUCCESS`
- **ID tài liệu tạo ra trong CSDL:** `4`
- **Kiểm tra GET:** `GET /api/documents/4/` -> HTTP `200`
- **Độ dài văn bản trích xuất (Content Length):** `306` ký tự
- **Nội dung nhận dạng mẫu:**
```text
BAO CAO KIEM THU PHAN MEM SCHEMATHESIS

Hoc phan: Kiem thu phan mem - Nhom 5

Thanh vien thuc hien: Nguyen Khiem Thuan (TV3) - MSSV: 2312764

Seed kiem thu: 303 | Pham vi: Phan D-E REST API Fuzzing

H
```
- **Kết luận:** **PASS**. Hệ thống upload, hàng đợi Redis/Celery xử lý và trích xuất nội dung văn bản thành công.

---

### Luồng 2 (TV3-FLOW-02): Tạo/Gán Tag, Correspondent, Document Type -> GET đối chiếu
- **Tag tạo mới:** `TV3_Tag_Verified_303` (ID: `5`, HTTP 201)
- **Correspondent tạo mới:** `TV3_Auditor_303` (ID: `4`, HTTP 201)
- **DocumentType tạo mới:** `TV3_DocType_Report_303` (ID: `4`, HTTP 201)
- **Gán metadata vào tài liệu:** `PATCH /api/documents/4/` -> HTTP `200`
- **Payload gán:**
```json
{
  "tags": [5],
  "correspondent": 4,
  "document_type": 4
}
```
- **Kiểm tra đối chiếu:** `GET /api/documents/4/` -> HTTP `200`
- **Kết quả kiểm tra:** Cả 3 trường Tag, Correspondent, DocumentType đều khớp chính xác giá trị đã gán.
- **Kết luận:** **PASS**. Luồng quản lý và liên kết quan hệ thực thể hoạt động đúng nghiệp vụ.

---

### Luồng 3 (TV3-FLOW-03): Tìm kiếm toàn văn (Search) và Lọc theo thuộc tính (Filter)
- **3.1 Tìm kiếm toàn văn:**
  - URL: `GET /api/documents/?query=Schemathesis`
  - HTTP Status: `200`
  - Kết quả: Tài liệu ID `4` nằm trong danh sách trả về.
- **3.2 Lọc theo Tag:**
  - URL: `GET /api/documents/?tags__id__all=5`
  - HTTP Status: `200`
  - Kết quả: Tài liệu ID `4` nằm trong danh sách trả về.
- **Kết luận:** **PASS**. Luồng tìm kiếm full-text và bộ lọc đa chiều qua API hoạt động chính xác.

---

### Xác minh Chuyên sâu: Nhận dạng Quang học Thực tế (OCR trên Ảnh Scan)
- **Mục tiêu:** Chứng minh hệ thống thực hiện OCR hình ảnh thực sự (Tesseract OCR), phân biệt rõ ràng với trích xuất văn bản có sẵn từ file PDF số / file TXT.
- **Tệp thử nghiệm:** [`scripts/sample_docs/TV3_Sample_Scan_Image_303.png`](../scripts/sample_docs/TV3_Sample_Scan_Image_303.png) (tệp ảnh PNG 800x400 chứa chữ vẽ pixel).
- **Endpoint gọi:** `POST /api/documents/post_document/` với `files={"document": ("TV3_Sample_Scan_Image_303.png", ..., "image/png")}`.
- **HTTP Status:** `200 OK`
- **Task UUID Celery:** `2aee9b15-8383-424b-bded-3b5c4bc5e91c` -> Kết quả: `SUCCESS`.
- **ID tài liệu tạo ra trong CSDL:** `5`
- **Nội dung trích xuất nhận dạng từ Tesseract OCR (`GET /api/documents/5/`):**
```text
HOADON BAN LE SCAN OCR TV3

Nguo! mua hang Nguyen khiem Thuan

Mssv 2312784 1V3 Seed 303

Mon hoe: Kiem thu phan mem NhomS

Chung minh nhan dang OCR Tesseract thuc te

Sotien thanh tean 303000 VND
```
- **Đối chiếu & Đánh giá:** Tesseract OCR bên trong container `paperless-webserver` đã nhận dạng thành công các dòng chữ từ bức ảnh thô (ví dụ: *"HOADON BAN LE SCAN OCR TV3"*, *"Nguyen khiem Thuan"*, *"Seed 303"*, *"Sotien thanh tean 303000 VND"*). Đây là bằng chứng xác thực quá trình số hóa OCR thực sự trên máy local của TV3.

