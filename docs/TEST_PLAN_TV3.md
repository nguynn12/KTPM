# TEST PLAN TV3 — Phần D: Schemathesis và kế hoạch kiểm thử

**Tác giả:** Nguyễn Khiêm Thuận · 2312764 · TV3 · seed 303.
**Ngày soạn:** 13/10/2026. **Trạng thái:** Đã thực thi Vòng 1, kiểm thử thủ công và xác thực 3 luồng nghiệp vụ trên máy Windows local.
**Căn cứ repo:** master 62e9a2ffbcb36bec9672c0e0c7a504cab20bf3f8.

## 1. Mục tiêu
Đánh giá API Paperless-ngx tuân thủ OpenAPI và xử lý dữ liệu không hợp lệ có kiểm soát. Tập trung vào lỗi 5xx, status/content-type/header/body lệch hợp đồng và validation đầu vào. Bổ sung ca thiết kế tay để kiểm tra nghiệp vụ mà schema không diễn tả đầy đủ. Không kết luận hệ thống hết lỗi khi một lượt fuzz không phát hiện lỗi.

## 2. Nguyên lý kỹ thuật K05
Schemathesis đọc OpenAPI: paths, methods, parameters, requestBody, responses và các ràng buộc như type/required/maxLength. Công cụ sinh nhiều input hợp lệ và không hợp lệ, gửi request tới API local rồi dùng checks làm oracle (chuẩn đối chiếu). Hypothesis hỗ trợ tìm trường hợp biên và thu nhỏ input gây lỗi để dễ tái hiện. Seed điều khiển phần ngẫu nhiên; muốn tái lập còn phải ghi đúng phiên bản, schema, trạng thái dữ liệu, flags, phases và cấu hình.

Một operation là một cặp METHOD + PATH; một operation có thể nhận nhiều test case/request. Một response có thể vi phạm nhiều checks; nhiều failures có thể chung một nguyên nhân. Vì vậy không đồng nhất operations, generated cases, requests, failures và bugs. JUnit có thể nhóm theo operation; không dùng số phần tử testcase trong XML làm số request.

## 3. Môi trường và giả định
| Nội dung | Quy định / bằng chứng |
|---|---|
| API | Chỉ http://localhost:8000 |
| Paperless-ngx | Compose hiện pin image 3.1.3; kiểm tra image thực tế trên máy |
| Mã nguồn upstream | ARCHITECTURE_NOTES của TV2 ghi tag v3.1.3, SHA d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e; cần kiểm chứng trước khi phân tích dòng nguồn |
| Schemathesis | 4.30.1, xác nhận từ Initialize trong log TV2 và CLI đã cài để kiểm tra |
| Python | >=3.10 theo metadata của Schemathesis 4.30.1; đề cũ ghi >=3.9 chưa đủ |
| Sinh dữ liệu | seed 303; max-examples 25; workers 1; ghi phiên bản Hypothesis/pip freeze |
| Xác thực | Token lấy từ tài khoản admin local; không dùng token chép từ repo |
| Điều kiện nền | Docker ổn định, schema tải được, baseline thống nhất, consume/OCR hoàn tất |
| Giới hạn phiên bản | Không dùng main/latest cho Paperless hoặc tự nâng Schemathesis giữa các vòng |

## 4. Phạm vi
| Tài nguyên | Nghiệp vụ chính | Vòng |
|---|---|---|
| /api/tags/ | Nhãn, tên, phân trang, CRUD | 1, 2, 3 |
| /api/correspondents/ | Đơn vị liên hệ, CRUD, validation | 1, 2, 3 |
| /api/document_types/ | Loại tài liệu, CRUD, validation | 1, 2, 3 |
| /api/documents/ | Danh sách, lọc, tài liệu và thao tác con trong allowlist | 1 chỉ GET; 3 mở rộng |

Ngoài phạm vi fuzz: users, groups, token, profile, config, ui_settings, mail_*, remote_version, các nhóm endpoint khác và mọi server Internet. Token/schema được gọi riêng để chuẩn bị. Chưa đánh giá tải lớn, UI đầy đủ, bảo mật toàn diện hoặc độ chính xác OCR trên nhiều loại tài liệu.

## 5. Ba vòng thực hiện
| Vòng | Phạm vi và cấu hình | Chuẩn bị | Bằng chứng |
|---|---|---|---|
| 1 | GET trên 4 nhóm; phases examples,fuzzing; 5 checks response cốt lõi | Baseline sạch, token hợp lệ | log + XML + NDJSON |
| 2 | Đọc/ghi trên tags, correspondents, document_types; checks all, phases mặc định | Reset được xác nhận, seed lại, kiểm tra baseline | log + XML + NDJSON |
| 3 | Thêm documents; checks all, phases mặc định | Reset được xác nhận, seed lại, chờ consume | log + XML + NDJSON |

Vòng 1 tắt coverage/stateful để giữ mục tiêu GET và tránh coverage probe dùng phương thức khác. Bản 4.30.1 có coverage test các phương thức chưa khai báo; operation filter không nên được hiểu là bảo đảm mọi request luôn dùng đúng một method khi chạy mọi phase. Vòng 2–3 có thể có probe trong các nhóm endpoint cho phép; cần ghi nhận số request thực tế riêng.

**Khác với log TV2:** vòng 1 TV2 không có allowlist path, trong LoadingFinished có các endpoint users/config/mail. TV3 thu hẹp đúng phạm vi đề. Do khác phạm vi/phases/checks, không so tổng số cases hai người như cùng điều kiện. Muốn so sánh định lượng, thống nhất cấu hình rồi chạy lại các lượt liên quan; không sửa log cũ.

## 6. Pass, Fail, Error và Blocked
- PASS: tất cả assertions áp dụng cho case đạt; status/body phù hợp oracle đã định trước. Input sai bị từ chối 400 có thể là PASS. Nếu status 400 thiếu trong schema thì vẫn có failure hợp đồng cần phân loại.
- FAIL: assertion bị vi phạm, ví dụ 5xx, response 201 thiếu trường required, tạo tên vượt biên thành công khi hợp đồng yêu cầu từ chối. Lưu request/response và check cụ thể.
- ERROR/BLOCKED: không đủ điều kiện thực thi/đánh giá như Docker không chạy, token sai ngoài ý muốn, schema không tải, timeout do môi trường. Không quy thành lỗi phần mềm khi chưa xác minh.
- 404 do ID ngẫu nhiên chưa có không tự chứng minh CRUD lỗi. Case kiểm tra GET thành công phải tạo dữ liệu và dùng ID thật.
- --checks all không đồng nghĩa kiểm hết mọi nghiệp vụ hoặc kiểm thử tải; tập checks phụ thuộc phiên bản. Không tự đưa ngưỡng latency thành tiêu chí khi nhóm chưa quy định.

## 7. Rủi ro và biện pháp
| Rủi ro | Ảnh hưởng | Biện pháp |
|---|---|---|
| Fuzzing thay đổi dữ liệu | Trùng tên, mất bản ghi, sai baseline | Instance local riêng; reset có xác nhận, seed và đối chiếu trước vòng ghi |
| Reset không đủ | So sánh sai giữa các vòng | Reset API hiện chỉ trang đầu; kiểm tra count, trash, task; volume reset phải hỏi trước |
| Khác phiên bản/seed/schema | Kết quả khó so sánh | Ghi tag, commit, package versions, schema hash, flags/phases |
| Token hỏng hoặc bị lộ | Toàn 401; lộ thông tin xác thực | Lấy token local; tiền kiểm auth; không hard-code; sanitize và quét log |
| Schema chưa đúng | Báo lỗi hợp đồng nhưng nghiệp vụ vẫn chạy | Tách schema mismatch khỏi lỗi server, ghi đúng nguồn oracle |
| OCR bất đồng bộ | Upload accepted nhưng tài liệu chưa xuất hiện | Poll trạng thái task/document đến timeout; không báo thành công sớm |
| TXT bị gọi là OCR | Bằng chứng không đúng | Dùng PDF/scan thích hợp; phân biệt trích xuất text và nhận dạng ảnh |
| Thời gian hạn chế | Lượt chạy dở hoặc smoke test | Ghi rõ incomplete/smoke, không suy thành full run |

## 8. Điều kiện bắt đầu và kết thúc
Bắt đầu khi Docker/web ổn định, đăng nhập được, schema có đủ endpoint, baseline xác minh, local-only được giữ và nơi lưu kết quả không trùng TV2. Trước xóa/reset, người dùng đã đồng ý.

Kết thúc khi đã ghi trạng thái từng vòng (hoàn tất/thất bại/chưa chạy/bị chặn), lưu kết quả thật, thực hiện ca tay phù hợp, phân loại failures, và có bằng chứng ba luồng. Được kết thúc với bug còn mở; không yêu cầu sửa mọi bug của phần mềm upstream để báo cáo. Lỗi cần request tối thiểu và tối thiểu hai lần tái hiện; nếu người thứ hai tái hiện thì ghi đã xác nhận giữa máy theo quy tắc nhóm.

## 9. Sản phẩm TV3
TEST_PLAN_TV3.md (D), TEST_CASES_TV3.md (E), CLI_STANDARD_TV3.md, results/TV3_* log/số liệu riêng, ảnh luồng nghiệp vụ, TV3_SUMMARY_FOR_SLIDES.md và slide Phần D–E. Chưa có kết quả TV3 trong bộ chuẩn bị này.

## Nguồn
- PDF kế hoạch nhóm, trang 2, 4–6, 8–9; AGENT_TASKS.md mục 5–10.
- https://github.com/nguynn12/KTPM/tree/62e9a2ffbcb36bec9672c0e0c7a504cab20bf3f8
- docker-compose.yml; scripts/*.py; scripts/reset_system.ps1; docs/ARCHITECTURE_NOTES.md; docs/TEST_CASES.md; Initialize/LoadingFinished trong results/TV2_*.ndjson.
- Schemathesis 4.30.1: output --help và metadata gói đã kiểm tra, không suy CLI từ bản cũ trong PDF.
- https://schemathesis.readthedocs.io/en/stable/ ; https://schemathesis.readthedocs.io/en/stable/reference/cli/ ; https://schemathesis.readthedocs.io/en/stable/reference/checks/ (tài liệu stable có thể thay đổi; CLI bản cài là căn cứ cú pháp).
