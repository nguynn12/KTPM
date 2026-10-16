# PINNED VERSIONS TV3 — MÔI TRƯỜNG KIỂM THỬ THỰC TẾ

**Người thực hiện:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303  
**Thời gian ghi nhận:** 13/10/2026  
**Mục đích:** Ghi nhận chính xác toàn bộ phiên bản phần mềm, thư viện và mã băm cấu hình trên máy Windows local để đảm bảo tính tái lập và minh bạch khoa học.

---

## 1. Môi trường Hệ thống & Hạ tầng
| Thành phần | Phiên bản / Định danh thực tế trên máy |
|---|---|
| Hệ điều hành | Windows (x86_64) |
| Docker Engine | Docker Desktop 29.7.2 (context: desktop-linux, kernel: 6.6.87.2-microsoft-standard-WSL2) |
| Docker Compose | v5.4.0 |
| Paperless-ngx Image | `ghcr.io/paperless-ngx/paperless-ngx:3.1.3` (pin cố định trong `docker-compose.yml`) |
| Redis Broker Image | `redis:7-alpine` |
| PostgreSQL DB Image | `postgres:16-alpine` |
| Git Commit nhóm | `62e9a2ffbcb36bec9672c0e0c7a504cab20bf3f8` (nhánh `master`) |
| OpenAPI Schema JSON SHA256 | `888b0f89ec0a9f65293f5320a86b1810d7904f93033178b567e313d951b12e3a` (docs/openapi_TV3.json) |
| OpenAPI Schema YAML SHA256 | `4b56422b2e5bc4190efdefab3444c46336062c06c5c1478a2f44c1d6082785e0` (docs/openapi_TV3.yaml) |

---

## 2. Công cụ Kiểm thử & Python Runtime
| Công cụ / Thư viện | Phiên bản thực tế |
|---|---|
| Python Runtime (Venv) | Python 3.14.4 (C:\Users\thorj\AppData\Local\Python\pythoncore-3.14-64\python.exe) |
| Schemathesis | 4.30.1 |
| Hypothesis Engine | 6.169.0 |
| Requests | 2.34.2 |
| ReportLab | 5.0.1 |
| Pytest | 9.1.1 |
| Rich | 15.0.0 |
| jsonschema-rs | 0.58.6 |

---

## 3. Danh sách đầy đủ `pip freeze` trong `.venv`

```text
anyio==4.15.1
certifi==2026.7.22
charset-normalizer==3.5.2
click==8.5.0
colorama==0.4.6
graphql-core==3.2.13
harfile==0.5.0
hypothesis==6.169.0
hypothesis-graphql==0.13.2
idna==3.20
iniconfig==2.3.1
jsonschema_rs==0.58.6
markdown-it-py==4.2.0
MarkupSafe==3.0.4
mdurl==0.1.2
packaging==26.3
pillow==12.3.0
pluggy==1.6.0
Pygments==2.21.0
pyrate-limiter==4.5.0
pytest==9.1.1
PyYAML==6.0.3
reportlab==5.0.1
requests==2.34.2
rich==15.0.0
schemathesis==4.30.1
sortedcontainers==2.4.0
typing_extensions==4.16.0
urllib3==2.8.0
Werkzeug==3.1.9
```
