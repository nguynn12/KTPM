# Đối chiếu kết quả TV2 seed 202

Bảng này ghi số liệu cho các mục 5.2–5.4 trong báo cáo. Mỗi dòng sử dụng kết quả của cùng một lượt chạy.

| Vòng | Operation được chọn | Ca sinh ra (CLI) | Failure (JUnit) | Unique failure (CLI) | Thời gian (giây) |
|---|---:|---:|---:|---:|---:|
| 1 | 19 | 159 | 14 | 16 | 31,85 |
| 2 | 18 | 1.481 | 19 | 58 | 203,24 |
| 3 | 53 | 2.056 | 53 | 136 | 211,21 |

## Nguồn đối chiếu

- **Vòng 1.** Sử dụng lượt đã lưu ở commit `650373a`. Xem [bản tóm tắt](TV2_round1_seed202_summary.md), [JUnit](TV2_round1_seed202_junit.xml) và [NDJSON](TV2_round1_seed202.ndjson). Lượt thăm dò 65 operation và lượt chạy lại cục bộ cùng tên được tách khỏi dòng này.
- **Vòng 2.** CLI ghi 18/163 operation được chọn, 1.481 ca sinh ra, 49 ca phát hiện 58 unique failure và 72 ca được bỏ qua. [NDJSON](TV2_round2_seed202.ndjson) xác nhận số operation và thời gian toàn lượt. [JUnit](TV2_round2_seed202_junit.xml) ghi 19 mục kiểm thử, cả 19 thất bại.
- **Vòng 3.** CLI ghi 53/163 operation được chọn, 2.056 ca sinh ra, 108 ca phát hiện 136 unique failure và 120 ca được bỏ qua. [NDJSON](TV2_round3_seed202.ndjson) xác nhận số operation và thời gian toàn lượt. [JUnit](TV2_round3_seed202_junit.xml) ghi 54 mục kiểm thử, 53 mục thất bại.

Các log CLI gốc của vòng 2–3 được đối chiếu trên máy và thuộc mẫu `*.log` bị Git bỏ qua. Bản đối chiếu chỉ trích số liệu tổng hợp. Có thể đối chiếu thêm với [ghi chú thực nghiệm TV2](../docs/FILL_IN.md#2-kết-quả-kiểm-thử-schemathesis-trích-xuất-từ-results).

## Cách đọc chỉ số

- Số operation lấy từ phạm vi được chọn. Một operation là một cặp phương thức HTTP và đường dẫn.
- Cột Failure (JUnit) lấy từ thuộc tính `failures` của `testsuite`. JUnit vòng 2 và 3 có thêm một mục tổng hợp `Stateful tests`.
- Cột Unique failure (CLI) lấy từ phần tổng kết của Schemathesis. Số lỗi phần mềm độc lập cần được xác định qua hồ sơ của từng phát hiện.
- Thời gian dùng thời gian toàn lượt trong phần tổng kết CLI và sự kiện `EngineFinished`, làm tròn đến hai chữ số thập phân.

Bản đối chiếu được tổng hợp với hỗ trợ của Codex từ kết quả chạy đã lưu của TV2.
