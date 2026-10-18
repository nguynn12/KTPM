# Kết quả chạy của TV1 — seed 101 (mẫu, TV1 điền sau khi chạy thật)

| Mục | Giá trị |
|---|---|
| Họ tên, ngày chạy | ___ , ___/10/2026 |
| Hệ điều hành, RAM | Windows 11 + WSL2 (Ubuntu), RAM ___ GB |
| Docker / Compose | Docker 29.8.0, Compose v5.5.1 (ghi nhận ngày 12/10/2026) |
| Paperless-ngx (tag) | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (SHA `d48663e…`) |
| Schemathesis | `4.30.1` (`pip install "schemathesis==4.30.1"`) |
| Seed | **101** (Hypothesis seed của TV1) |
| Vòng chạy | 1 / 2 / 3 (1 file cho mỗi vòng) |

| Mục | Vòng 1 (GET) | Vòng 2 (tags/correspondents/doc_types) | Vòng 3 (mở rộng + documents) |
|---|---|---|---|
| Số endpoint được test | | | |
| Số test case sinh ra | | | |
| Số test thất bại | | | |
| Thời gian chạy | | | |
| File log | `results/TV1_vong1.log` | `results/TV1_vong2.log` | `results/TV1_vong3.log` |

Chạy kèm `tee` để lưu log:
```bash
schemathesis run ... --hypothesis-seed=101 2>&1 | tee results/TV1_vong1.log
```

## Lỗi ghi nhận (copy thêm bảng cho mỗi lỗi)

| Trường | Nội dung |
|---|---|
| ID | BUG-TV1-01 |
| Endpoint + method | |
| Loại lỗi | 5xx / response sai schema / status code không có trong tài liệu / khác |
| Dữ liệu gửi vào | |
| Kết quả thực tế | |
| Kết quả mong đợi | |
| Lệnh `curl` tái hiện | |
| Ai tìm thấy, seed nào | TV1, seed 101 |
| Tái hiện trên máy khác? | Có / Không / Chưa thử |
| Phân loại | đã xác nhận (≥2 người) / cần kiểm tra lại / false positive (schema sai, dữ liệu vô lý) |
