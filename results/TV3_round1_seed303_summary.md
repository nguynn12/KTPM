# TÓM TẮT KẾT QUẢ KIỂM THỬ THỰC TẾ — TV3 VÒNG 1

- **Tác giả:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303
- **Thời gian thực hiện:** 2026-10-13 11:59:02
- **Vòng kiểm thử:** Vòng 1
- **CLI Exit Code:** `1`
- **Công cụ:** Schemathesis 4.30.1 | Python 3.14.4 | Hypothesis 6.169.0
- **Phạm vi Regex:** `^/api/(tags|correspondents|document_types|documents)/`
- **Phases:** `examples,fuzzing`
- **Checks:** `not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance`
- **Cấu hình sinh:** `--max-examples 25`, `--workers 1`, `--mode all`

---

## 1. Bảng số liệu đo lường thực tế

| Chỉ số | Giá trị ghi nhận từ công cụ | Nguồn trích xuất |
|---|---|---|
| Operations được chọn | 99 | NDJSON LoadingFinished / CLI |
| Tổng thời gian chạy | 1.03 giây | NDJSON EngineFinished / CLI |
| Số testcase trong JUnit report | 99 | JUnit XML `<testsuite tests="...">` |
| Số failures trong JUnit | 82 | JUnit XML `<testsuite failures="...">` |
| Số errors trong JUnit | 0 | JUnit XML `<testsuite errors="...">` |
| Passed reported (CLI) | 17 | CLI summary output |
| Failed reported (CLI) | 82 | CLI summary output |
| Errored reported (CLI) | không có trong output | CLI summary output |

> [!NOTE]
> - `max-examples` (25) là tham số giới hạn sinh của thuật toán Hypothesis cho mỗi operation, không phải tổng số request thực tế.
> - Số phần tử `<testcase>` trong JUnit XML đại diện cho các operations/checks được ánh xạ, không đồng nhất với tổng số request HTTP đã gửi qua mạng.
> - Exit code `1`: Nếu mã là 1, công cụ đã chạy hoàn tất và phát hiện vi phạm kiểm thử (failures/errors), không phải do môi trường bị hỏng.

---

## 2. Đường dẫn các tệp bằng chứng thực tế
- File Log chi tiết: [TV3_round1_seed303.log](file:///D:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303.log)
- File JUnit XML: [TV3_round1_seed303.xml](file:///D:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303.xml)
- File NDJSON: [TV3_round1_seed303.ndjson](file:///D:/DaiHocDL/KiemThuPhanMem/KTPM/results/TV3_round1_seed303.ndjson)

---

## 3. Quét bảo mật đầu ra
- Toàn bộ giá trị Authorization token và mật khẩu quản trị đã được làm sạch (`[REDACTED]`).
- Tùy chọn `--output-sanitize true` đã được bật trong quá trình chạy.
