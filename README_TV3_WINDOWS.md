# TV3 — Làm theo thứ tự trên máy Windows

Nguyễn Khiêm Thuận · 2312764 · seed Schemathesis 303 · Phần D–E.

## 1. Mở Docker Desktop và lấy repo
Mở Docker Desktop, chờ engine chạy. Mở PowerShell tại thư mục bạn muốn lưu bài.

Nếu chưa có repo:
```powershell
git clone https://github.com/nguynn12/KTPM.git
cd KTPM
```
Nếu đã có repo: vào thư mục KTPM, chạy `git status` và `git branch --show-current`. Khi đang ở `master` và không có thay đổi cần giữ, chạy `git pull --ff-only origin master`. Nếu có thay đổi hoặc xung đột, để Antigravity kiểm tra, không dùng reset --hard.

## 2. Mở đúng thư mục trong Antigravity
Chọn File > Open Folder, chọn thư mục KTPM chứa docker-compose.yml. Giải nén bộ bàn giao TV3 này vào đó. Chép AGENT_TASKS.md bạn đã tải vào docs/AGENT_TASKS.md nếu chưa có. Mở PROMPT_ANTIGRAVITY_TV3.txt, Ctrl+A, Ctrl+C rồi dán toàn bộ vào chat Antigravity và gửi.

Prompt đã chứa họ tên, seed, vai trò, hướng dẫn nhóm và các vấn đề phát hiện trong repo. Antigravity cần đọc repo hiện tại trước khi sửa. Đừng bảo nó làm lại kiến trúc A–B hoặc lấy số liệu TV2 làm của bạn.

## 3. Nếu muốn tự bật hệ thống trước
Chạy từ GỐC thư mục KTPM:
```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
docker compose up -d
docker compose ps
```
Mở http://localhost:8000. Nếu vừa dựng mới bằng file mẫu chưa sửa, thử admin/admin; nếu đã có mật khẩu riêng thì dùng mật khẩu đó. File mẫu đã cấu hình tự tạo admin. Không cần chạy createsuperuser lần nữa khi đăng nhập được. Nếu bị lỗi, lấy `docker compose logs --tail 100 webserver`; kiểm tra và che thông tin bí mật trước khi gửi.

## 4. Bạn phải trực tiếp làm trên máy
- Cài/mở Docker nếu chưa sẵn sàng; nhập mật khẩu local khi được hỏi.
- Quyết định có xóa dữ liệu để reset hay không. Chỉ đồng ý khi đây là instance học tập, không có tài liệu quan trọng cần giữ. AGENT_TASKS mục 7 yêu cầu xác nhận trước lần reset đầu tiên.
- Tự chụp ảnh đăng nhập, danh sách tài liệu, Swagger và ba luồng nghiệp vụ. Trong ảnh không để lộ token.
- Để Antigravity chạy seed 303, lưu file TV3_*; gửi kết quả về để cập nhật slide.

## 5. Các file cần gửi lại
Ưu tiên docs/TV3_SUMMARY_FOR_SLIDES.md và results/TV3_round*_seed303*.md/.log/.xml/.ndjson, cùng ảnh minh chứng. Không gửi .env, mật khẩu hoặc token. Nếu chưa chạy được, chỉ cần gửi ảnh lỗi mới nhất và `docker compose ps`.

## 6. Slide hiện tại dùng thế nào?
Slide_TV3_Schemathesis_Phan_D_E.pptx là nội dung Phần D–E, có speaker notes để tập nói. Trang bằng chứng đang ghi CHƯA CHẠY vì chưa có log TV3. Không báo cáo số liệu TV2 thành số liệu cá nhân. Sau khi có log, điền trang bằng chứng và bổ sung ảnh thật.

## 7. Ghi nhận khi chuẩn bị bộ này
Đã clone và đọc repo master tại 62e9a2f; đã chạy CLI `schemathesis --version` và `schemathesis run --help` của 4.30.1. Môi trường chuẩn bị không có Docker, không mở Antigravity trên máy bạn, chưa khởi chạy Paperless và chưa thực thi kiểm thử TV3. Những việc đó được chuyển thành quy trình chạy tại máy bạn.
