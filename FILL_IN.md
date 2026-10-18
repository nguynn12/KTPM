# BẢNG TỔNG HỢP DỮ LIỆU THỰC TẾ HỆ THỐNG (FILL_IN.MD)

> **Ghi chú bảo đảm tính trung thực:** Toàn bộ thông tin dưới đây được trích xuất trực tiếp từ máy tính thực thi, cấu hình repo và các file log thực tế trong thư mục `results/`, `docs/`, `scripts/` của **TV1 (Trần Gia Huy)**. Không sử dụng số liệu giả định hay ước đoán. Những mục chưa thực hiện được ghi rõ "Chưa chạy" / "Chưa có dữ liệu".

---

## 1. Phiên bản & Môi trường thực thi (TV1)

| Thành phần | Thông tin / Phiên bản trích xuất thực tế | Lệnh kiểm tra thực tế |
|---|---|---|
| **Hệ điều hành (OS)** | Windows 11 + WSL2 (Ubuntu) | `scripts/check_env.ps1`, `docs/TV1_Onboarding.md` |
| **Docker Engine** | `Docker version 29.8.0, build 88096ef` | `docker --version` |
| **Docker Compose** | `Docker Compose version v5.5.1` | `docker compose version` |
| **Python (Host)** | `Python 3.15.0` | `python --version` |
| **Schemathesis** | **Chưa cài** (`schemathesis: command not found`) | `schemathesis --version` |
| **Tag Paperless-ngx (pin)** | `v3.1.3` | `PINNED-VERSIONS.md` |
| **Commit SHA Paperless-ngx (pin)** | `d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e` | `PINNED-VERSIONS.md` |
| **Tag Image Docker (`docker-compose.pinned.yml`)** | • `broker`: `docker.io/valkey/valkey:9-alpine`<br>• `db`: `docker.io/library/postgres:18`<br>• `webserver`: `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` | Đọc trực tiếp từ file `docker/docker-compose.pinned.yml` |
| **Tên các Container** | `webserver`, `db`, `broker` | `docker compose ps` (theo `docker-compose.pinned.yml`) |
| **Port** | `8000` → http://localhost:8000 | `docker-compose.pinned.yml` |

---

## 2. Kết quả kiểm thử Schemathesis (TV1)

> **Trạng thái: CHƯA CHẠY.** TV1 đã dựng hệ thống thật (13/10/2026) và chạy 3 luồng nghiệp vụ, nhưng **chưa cài Schemathesis** nên chưa chạy vòng 1–3.

| Mục | Giá trị |
|---|---|
| **Vòng kiểm thử** | Chưa chạy |
| **Seed của TV1** | `101` (theo quy ước nhóm: TV1=101, TV2=202, TV3=303, TV4=404, TV5=505) |
| **Lệnh kiểm thử** | Chưa có |
| **Số endpoint/operation được test** | Chưa có dữ liệu |
| **Số test case sinh ra** | Chưa có dữ liệu |
| **Số test thất bại** | Chưa có dữ liệu |
| **Thời gian chạy** | Chưa có dữ liệu |
| **File mẫu** | `results/TV1_101_mau.md` (mẫu để điền sau khi chạy thật) |
| **File triển khai thật** | `results/TV1_deploy_13-10.md` (biên bản dựng hệ thống + 3 luồng nghiệp vụ, đã chạy) |

---

## 3. Danh sách BUG (TV1)

| ID | Endpoint | Loại lỗi | Mô tả 1 dòng | Tái hiện ≥ 2 lần | Bằng chứng tái hiện |
|---|---|---|---|---|---|
| — | — | — | **Chưa có kết quả chạy thử Schemathesis** | — | — |

> BUG-01, BUG-02, BUG-03 trong file này là dữ liệu của TV2 (seed 202), không thuộc phân công TV1. TV1 sẽ tự ghi lỗi vào `docs/bugs/BUG-xx.md` sau khi chạy Schemathesis vòng 1–3 với seed 101.

---

## 4. Bảng Test Case thực thi thực tế (TV1)

| Mã TC | Phương thức | Endpoint | Kết quả mong đợi | Kết quả thực tế | Đánh giá | Ghi chú thực tế |
|---|---|---|---|---|---|---|
| — | — | — | — | — | **Chưa chạy** | TV1 chưa có file `docs/TEST_CASES.md` (trách nhiệm của TV3 theo kế hoạch phân công). Test case sẽ được thiết kế và chạy trong giai đoạn mở rộng sau giữa kỳ. |

---

## 5. Ánh xạ Endpoint → Mã nguồn (tham khảo từ Paperless-ngx v3.1.3)

*Căn cứ từ mã nguồn Paperless-ngx tag `v3.1.3` (commit `d48663e`), dùng làm tài liệu tham khảo cho TV1 khi đọc mã nguồn sau khi chạy thử:*

| Nhóm Endpoint | ViewSet / View | Serializer | Model | File và Số dòng cụ thể |
|---|---|---|---|---|
| `/api/tags/` | `TagViewSet` | `TagSerializer` | `Tag` | • View: `src/documents/views.py:599-677`<br>• Serializer: `src/documents/serialisers.py:617-746`<br>• Model: `src/documents/models.py:102-140` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/correspondents/` | `CorrespondentViewSet` | `CorrespondentSerializer` | `Correspondent` | • View: `src/documents/views.py:553-596`<br>• Serializer: `src/documents/serialisers.py:541-560`<br>• Model: `src/documents/models.py:96-101` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/document_types/` | `DocumentTypeViewSet` | `DocumentTypeSerializer` | `DocumentType` | • View: `src/documents/views.py:680-698`<br>• Serializer: `src/documents/serialisers.py:562-601`<br>• Model: `src/documents/models.py:141-156` *(kế thừa `MatchingModel`: dòng 65-94)* |
| `/api/documents/` | `UnifiedSearchViewSet` *(kế thừa `DocumentViewSet`)* | `DocumentSerializer` *(và `SearchResultSerializer`)* | `Document` | • View: `src/documents/views.py:2402-2460`<br>*(Lớp cha `DocumentViewSet`: dòng 980-2401)*<br>• Serializer: `src/documents/serialisers.py:1047-1334`<br>*(Lớp tìm kiếm `SearchResultSerializer`: dòng 1336-1377)*<br>• Model: `src/documents/models.py:157-550` |

---

## 6. Thống kê Git Log & Đóng góp TV1

- **Nhánh:** `TV1_TranGiaHuy` (nhánh mới hoàn toàn, không kế thừa lịch sử `master`)
- **Remote:** `https://github.com/nguynn12/KTPM.git`
- **Số commit:** 8 commit
- **Commit đầu tiên:** `a19c309` — `chore(repo): khoi tao repo TV1 + .gitignore + README + requirements`
- **Commit gần nhất:** `20fbca1` — `scripts(check): script kiem tra moi truong truoc khi cai`
- **Danh sách commit chi tiết:**
  1. `a19c309` chore(repo): khoi tao repo TV1 + .gitignore + README + requirements
  2. `32e9c32` docs(pin): pin Paperless-ngx v3.1.3 + commit SHA + Schemathesis 4.30.1
  3. `2b0e7bb` feat(docker): compose pin 3.1.3 + file env mau
  4. `4aedd5c` feat(seed): 6 PDF mau + seed_api.py + generator + README
  5. `4aac7c3` docs(onboarding): huong dan cai Paperless-ngx tu may sach (Phan C)
  6. `54879be` docs(flows): 3 luong nghiep vu chay duoc (Phan C)
  7. `cfa36c5` test(results): bien ban duct thuc TV1 13/10 + mau seed 101
  8. `20fbca1` scripts(check): script kiem tra moi truong truoc khi cai

- **Các thành viên khác (TV2, TV3, TV4, TV5):** CHƯA CÓ commit trên nhánh `TV1_TranGiaHuy` (mỗi thành viên commit trên tài khoản của mình để peer-review cuối kỳ).

---

## 7. Các mục người dùng bắt buộc PHẢI TỰ LÀM

Agent không thể và không được phép tạo tự động các nội dung mang tính chất định danh cá nhân và minh chứng hình ảnh thực tế sau đây:

1. **Thông tin định danh hành chính của nhóm:**
   - [ ] Tên nhóm chính thức theo danh sách lớp học phần.
   - [ ] Họ tên và Mã số sinh viên (MSSV) của toàn bộ 5 thành viên (TV1, TV2, TV3, TV4, TV5).
   - [ ] Đường dẫn (Link) bảng quản lý tiến độ công việc trên **Trello** (hoặc Jira/Notion).

2. **Ảnh chụp màn hình thực tế (Screenshots) có gắn dấu hiệu nhận diện (để vào báo cáo Word/Slide):**
   - [ ] Ảnh chụp màn hình đăng nhập thành công vào Paperless-ngx UI (`http://localhost:8000`).
   - [ ] Ảnh chụp danh sách tài liệu (`/documents`) với dữ liệu đã seed.
   - [ ] Ảnh chụp giao diện Swagger UI tài liệu đặc tả API (`http://localhost:8000/api/schema/swagger-ui/`).
   - [ ] Ảnh chụp kết quả chạy Schemathesis trên Terminal / PowerShell (sau khi chạy vòng 1–3).
   - [ ] Ảnh chụp tái hiện BUG trên giao diện UI hoặc Postman/Swagger (sau khi tìm thấy lỗi).

3. **Video minh chứng (Screen Recording):**
   - [ ] Quay video màn hình (độ dài 1-3 phút) thao tác kiểm thử 3 luồng nghiệp vụ trên hệ thống cục bộ:
     1. Luồng 1: Tải lên tài liệu mẫu (Upload document).
     2. Luồng 2: Gắn nhãn (Tag), người gửi (Correspondent), loại tài liệu (Document Type).
     3. Luồng 3: Tìm kiếm tài liệu bằng từ khóa và bộ lọc.

4. **Chạy thực tế Schemathesis (seed 101):**
   - [ ] Cài `pip install "schemathesis==4.30.1"`.
   - [ ] Chạy Vòng 1, Vòng 2, Vòng 3 theo `docs/TV1_Onboarding.md`.
   - [ ] Điền số liệu thật vào `results/TV1_101_<ngày>.md` (mẫu hiện tại là `results/TV1_101_mau.md`).
   - [ ] Ghi file `docs/bugs/BUG-xx.md` cho mỗi lỗi phát hiện (nếu có).
