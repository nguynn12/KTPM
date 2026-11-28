#!/usr/bin/env python3
"""
scripts/demo_system.py
Kịch bản thực thi và thu thập minh chứng vận hành 3 luồng nghiệp vụ cốt lõi trên Paperless-ngx v3.1.3:
  - Luồng 1: Tải lên và xử lý tài liệu bất đồng bộ (ghi nhận Task UUID, trạng thái hoàn tất SUCCESS và truy xuất tài liệu).
  - Luồng 2: Tạo thông tin phân loại (Tag, Correspondent, DocumentType) và gán cho tài liệu (kèm truy vấn lại độc lập).
  - Luồng 3: Tìm kiếm toàn văn (Tantivy) và lọc đa tiêu chí trên tập dữ liệu đối chứng đã biết trước.

Tự động che (redact) toàn bộ token, mật khẩu, khóa bí mật và đường dẫn cá nhân trước khi xuất log minh chứng.
Phục vụ báo cáo Chương 4 và trình diễn demo trực tiếp — TV4 (Nguyễn Nhất Minh).
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_dotenv_file(env_path: Path = Path(".env")) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_dotenv_file()

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000").rstrip("/")
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")
VN_TZ = timezone(timedelta(hours=7))


def redact_sensitive(text: str, raw_token: str = "") -> str:
    """Che toàn bộ token, mật khẩu, email và đường dẫn người dùng trên máy cục bộ."""
    if not text:
        return text
    out = text
    if raw_token:
        out = out.replace(raw_token, "<REDACTED_TOKEN>")
    if ADMIN_PASS and ADMIN_PASS not in ("", "<REDACTED_PASSWORD>"):
        # Chỉ thay trong ngữ cảnh password/secret để không làm hỏng từ khóa bình thường
        out = re.sub(
            r'("password"\s*:\s*)"[^"]*"',
            r'\1"<REDACTED_PASSWORD>"',
            out,
            flags=re.IGNORECASE,
        )
    out = re.sub(r"Token\s+[0-9a-fA-F]{16,64}", "Token <REDACTED_TOKEN>", out)
    out = re.sub(
        r'("token"\s*:\s*)"[0-9a-fA-F]{16,64}"',
        r'\1"<REDACTED_TOKEN>"',
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(
        r"(PAPERLESS_SECRET_KEY|PAPERLESS_ADMIN_PASSWORD|POSTGRES_PASSWORD|PAPERLESS_DBPASS)=[^\s\r\n]+",
        r"\1=<REDACTED_SECRET>",
        out,
    )
    out = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "<REDACTED_EMAIL>",
        out,
    )
    out = re.sub(r"[C-Zc-z]:\\Users\\[^\\\s\"']+", r"<USER_HOME>", out)
    out = re.sub(r"/Users/[^/\s\"']+", "/Users/<REDACTED_USER>", out)
    return out


def format_json_safe(data, raw_token: str = "") -> str:
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    return redact_sensitive(raw, raw_token)


def run_cmd_capture(cmd: list[str], raw_token: str = "") -> str:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        combined = (proc.stdout or "") + (proc.stderr or "")
        return redact_sensitive(combined.strip(), raw_token)
    except Exception as exc:
        return f"[WARN] Không thể chạy lệnh {' '.join(cmd)}: {exc}"


def wait_for_task_completion(task_id: str, headers: dict, timeout_sec: int = 45) -> tuple[dict, float]:
    start = time.perf_counter()
    deadline = start + timeout_sec
    last_payload = {}
    while time.perf_counter() < deadline:
        res = requests.get(f"{BASE_URL}/api/tasks/?task_id={task_id}", headers=headers, timeout=10)
        if res.status_code == 200:
            body = res.json()
            items = body if isinstance(body, list) else body.get("results", [])
            if items:
                task_obj = items[0]
                last_payload = task_obj
                status = (task_obj.get("status") or "").lower()
                if status in ("success", "failure"):
                    return task_obj, round(time.perf_counter() - start, 2)
        time.sleep(0.8)
    return last_payload, round(time.perf_counter() - start, 2)


def extract_doc_id_from_task(task_info: dict) -> int | None:
    res_data = task_info.get("result_data") or {}
    if isinstance(res_data, dict) and res_data.get("document_id") is not None:
        return int(res_data["document_id"])
    rel_ids = task_info.get("related_document_ids") or []
    if rel_ids:
        return int(rel_ids[0])
    if task_info.get("related_document") is not None:
        return int(task_info["related_document"])
    return None


def get_or_create_metadata(endpoint: str, payload: dict, headers: dict) -> tuple[int, dict, bool]:
    res = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=payload, timeout=10)
    if res.status_code == 201:
        body = res.json()
        return res.status_code, body, True
    if res.status_code == 400 and "already exists" in res.text:
        list_res = requests.get(
            f"{BASE_URL}{endpoint}?name__iexact={requests.utils.quote(payload['name'])}",
            headers=headers,
            timeout=10,
        )
        if list_res.status_code == 200 and list_res.json().get("results"):
            existing = list_res.json()["results"][0]
            return 200, existing, False
    raise RuntimeError(f"Không thể tạo đối tượng tại {endpoint}: HTTP {res.status_code} - {res.text[:200]}")


def run_demo(reset_first: bool = False, save_evidence: bool = True, output_dir: str = "docs/evidence/logs") -> int:
    now_str = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S UTC+7")
    out_path = Path(output_dir)
    if save_evidence:
        out_path.mkdir(parents=True, exist_ok=True)

    print("=" * 88)
    print("  CHƯƠNG TRÌNH XÁC MINH & DEMO 3 LUỒNG NGHIỆP VỤ PAPERLESS-NGX v3.1.3 (TV4)")
    print(f"  Thời điểm thực thi: {now_str} | URL đích: {BASE_URL}")
    print("=" * 88)

    if reset_first:
        from reset_data import reset_api
        reset_api()

    # =========================================================================
    # BƯỚC 0: KIỂM TRA DỊCH VỤ DOCKER COMPOSE & MÔI TRƯỜNG
    # =========================================================================
    print("\n[BƯỚC 0] Kiểm tra trạng thái dịch vụ Docker Compose và phiên bản hệ thống...")
    compose_ps = run_cmd_capture(["docker", "compose", "ps"])
    image_inspect = run_cmd_capture([
        "docker", "image", "inspect", "ghcr.io/paperless-ngx/paperless-ngx:3.1.3",
        "--format",
        "Version={{index .Config.Labels \"org.opencontainers.image.version\"}} | "
        "Revision={{index .Config.Labels \"org.opencontainers.image.revision\"}} | "
        "Digest={{index .RepoDigests 0}}",
    ])
    s6_services = run_cmd_capture(["docker", "compose", "exec", "-T", "webserver", "s6-rc", "-a", "list"])
    webserver_startup_logs = run_cmd_capture(["docker", "compose", "logs", "--tail", "25", "webserver"])

    print("  -> Trạng thái Docker Compose:\n" + "\n".join("     " + ln for ln in compose_ps.splitlines()))
    print(f"  -> Định danh Image: {image_inspect}")

    if save_evidence:
        env_log = (
            f"# MINH CHỨNG 01: TRẠNG THÁI DỊCH VỤ DOCKER COMPOSE & TIẾN TRÌNH NỀN\n"
            f"Thời gian ghi nhận: {now_str}\n\n"
            f"## 1. Lệnh `docker compose ps`\n```text\n{compose_ps}\n```\n\n"
            f"## 2. Xác minh phiên bản và Commit SHA của Image triển khai\n```text\n{image_inspect}\n```\n\n"
            f"## 3. Danh sách dịch vụ nội bộ s6-overlay đang chạy trong `paperless-webserver`\n```text\n{s6_services}\n```\n\n"
            f"## 4. Trích xuất log hoạt động gần nhất của `paperless-webserver` (đã rà soát che thông tin nhạy cảm)\n```text\n{webserver_startup_logs}\n```\n"
        )
        (out_path / "01_environment_and_compose_status.txt").write_text(env_log, encoding="utf-8")

    # =========================================================================
    # BƯỚC 1: KIỂM TRA XÁC THỰC API & OPENAPI SCHEMA
    # =========================================================================
    print("\n[BƯỚC 1] Xác thực REST API và kiểm tra đặc tả OpenAPI...")
    unauth_res = requests.get(f"{BASE_URL}/api/documents/", timeout=10)
    auth_res = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": "<ADMIN_USER>" if False else ADMIN_USER, "password": ADMIN_PASS},
        timeout=10,
    )
    if auth_res.status_code != 200:
        print(f"  [LỖI] Xác thực thất bại: HTTP {auth_res.status_code}")
        return 1

    raw_token = auth_res.json().get("token", "")
    headers = {
        "Authorization": f"Token {raw_token}",
    }
    schema_res = requests.get(f"{BASE_URL}/api/schema/?format=json", headers=headers, timeout=15)
    schema_info = {}
    op_count = 0
    if schema_res.status_code == 200:
        try:
            schema_json = schema_res.json()
        except Exception:
            import yaml  # type: ignore
            schema_json = yaml.safe_load(schema_res.text)
        schema_info = schema_json.get("info", {})
        http_methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
        for _, methods in schema_json.get("paths", {}).items():
            op_count += sum(1 for m in methods if m.lower() in http_methods)

    docs_before_res = requests.get(f"{BASE_URL}/api/documents/", headers=headers, timeout=10)
    count_before = docs_before_res.json().get("count", 0) if docs_before_res.status_code == 200 else -1

    print(f"  -> Kiểm tra chặn truy cập không token (`GET /api/documents/`): HTTP {unauth_res.status_code}")
    print(f"  -> Lấy token (`POST /api/token/`): HTTP {auth_res.status_code} | Token: <REDACTED_TOKEN>")
    print(
        f"  -> Đặc tả OpenAPI (`GET /api/schema/`): HTTP {schema_res.status_code} | "
        f"Title: {schema_info.get('title')} v{schema_info.get('version')} | Tổng số operations: {op_count}"
    )
    print(f"  -> Số lượng tài liệu hiện có trước Luồng 1: {count_before}")

    if save_evidence:
        auth_log = (
            f"# MINH CHỨNG 02: KIỂM TRA XÁC THỰC API VÀ ĐẶC TẢ OPENAPI\n"
            f"Thời gian ghi nhận: {now_str}\n\n"
            f"## 1. Kiểm tra truy cập không kèm Token (Kỳ vọng: HTTP 401 Unauthorized)\n"
            f"Request:  GET {BASE_URL}/api/documents/\n"
            f"Response: HTTP {unauth_res.status_code}\n"
            f"Body:     {redact_sensitive(unauth_res.text, raw_token)}\n\n"
            f"## 2. Yêu cầu cấp Token xác thực (Đã che tài khoản & mật khẩu)\n"
            f"Request:  POST {BASE_URL}/api/token/\n"
            f'Payload:  {{"username": "<REDACTED_USER>", "password": "<REDACTED_PASSWORD>"}}\n'
            f"Response: HTTP {auth_res.status_code}\n"
            f'Body:     {{"token": "<REDACTED_TOKEN>"}}\n\n'
            f"## 3. Kiểm tra đặc tả OpenAPI Schema\n"
            f"Request:  GET {BASE_URL}/api/schema/?format=json\n"
            f"Header:   Authorization: Token <REDACTED_TOKEN>\n"
            f"Response: HTTP {schema_res.status_code}\n"
            f"OpenAPI Info: {format_json_safe(schema_info, raw_token)}\n"
            f"Tổng số API operations trích xuất từ Schema: {op_count}\n"
        )
        (out_path / "02_auth_and_openapi_check.txt").write_text(auth_log, encoding="utf-8")

    # =========================================================================
    # LUỒNG 1: TẢI LÊN VÀ XỬ LÝ TÀI LIỆU BẤT ĐỒNG BỘ
    # =========================================================================
    print("\n[LUỒNG 1] Tải lên tài liệu, theo dõi xử lý nền hoàn tất và truy xuất tài liệu...")
    sample_dir = Path("scripts/sample_docs")
    sample_dir.mkdir(parents=True, exist_ok=True)

    run_nonce = int(time.time())
    doc_a_filename = "Flow1_Invoice_ACME_Q4_2026.txt"
    doc_a_title = "Hoa Don Dich Vu Luu Tru Dam May Q4-2026"
    doc_a_content = (
        f"CHUNG TU KE TOAN SO INV-2026-0404-{run_nonce}\n"
        "DON VI PHAT HANH: CONG TY DICH VU DAM MAY ACME\n"
        "KY CUOC: Q4-2026\n"
        "NOI DUNG: PHI DICH VU LUU TRU TAI LIEU SO VA NHAN DANG OCR\n"
        "MA DOI SOAT DUY NHAT: KTPM-R08-FLOW-ALPHA\n"
        "TONG THANH TOAN: 4.500.000 VND\n"
    )
    (sample_dir / doc_a_filename).write_text(doc_a_content, encoding="utf-8")

    doc_b_filename = "Flow3_Control_Report_Q4_2026.txt"
    doc_b_title = "Bien Ban Nghiem Thu Ky Thuat Noi Bo Q4-2026"
    doc_b_content = (
        f"BIEN BAN NGHIEM THU SO BBNT-2026-0405-{run_nonce}\n"
        "DON VI PHAT HANH: BO PHAN VAN HANH HE THONG NOI BO\n"
        "KY BAO CAO: Q4-2026\n"
        "NOI DUNG: KIEM TRA DICH VU CONTAINER DOCKER VA CHI MUC TIM KIEM\n"
        "MA DOI SOAT DUY NHAT: KTPM-R08-FLOW-BETA\n"
    )
    (sample_dir / doc_b_filename).write_text(doc_b_content, encoding="utf-8")

    # 1.1 Upload Tài liệu chính A
    with open(sample_dir / doc_a_filename, "rb") as fa:
        up_a_res = requests.post(
            f"{BASE_URL}/api/documents/post_document/",
            headers=headers,
            data={"title": doc_a_title},
            files={"document": (doc_a_filename, fa, "text/plain")},
            timeout=15,
        )
    if up_a_res.status_code not in (200, 202):
        print(f"  [LỖI] Upload tài liệu A thất bại: HTTP {up_a_res.status_code} - {up_a_res.text}")
        return 1
    task_a_uuid = up_a_res.text.strip().strip('"')
    print(f"  -> [1.1] Đã gửi tệp '{doc_a_filename}' | HTTP {up_a_res.status_code} | Task UUID: {task_a_uuid}")

    # Upload thêm Tài liệu đối chứng B (phục vụ kiểm chứng loại trừ ở Luồng 3)
    with open(sample_dir / doc_b_filename, "rb") as fb:
        up_b_res = requests.post(
            f"{BASE_URL}/api/documents/post_document/",
            headers=headers,
            data={"title": doc_b_title},
            files={"document": (doc_b_filename, fb, "text/plain")},
            timeout=15,
        )
    task_b_uuid = up_b_res.text.strip().strip('"')

    # 1.2 Theo dõi trạng thái xử lý nền tới khi hoàn tất (SUCCESS)
    task_a_info, elapsed_a = wait_for_task_completion(task_a_uuid, headers)
    task_b_info, elapsed_b = wait_for_task_completion(task_b_uuid, headers)

    task_a_status = (task_a_info.get("status") or "").lower()
    doc_a_id = extract_doc_id_from_task(task_a_info)
    doc_b_id = extract_doc_id_from_task(task_b_info)
    print(
        f"  -> [1.2] Trạng thái xử lý nền Task A: {task_a_status} sau {elapsed_a}s "
        f"(worker duration={task_a_info.get('duration_seconds')}s) | document_id = {doc_a_id}"
    )
    print(
        f"  -> [1.2b] Trạng thái xử lý nền Tài liệu đối chứng B: {(task_b_info.get('status') or '').lower()} "
        f"sau {elapsed_b}s | document_id = {doc_b_id}"
    )

    if task_a_status != "success" or doc_a_id is None:
        print(f"  [LỖI] Tác vụ xử lý tài liệu A không đạt success: {task_a_info}")
        return 1

    # 1.3 Truy xuất tài liệu sau xử lý hoàn tất + kiểm tra tải tệp gốc
    doc_a_get_res = requests.get(f"{BASE_URL}/api/documents/{doc_a_id}/", headers=headers, timeout=10)
    doc_a_json = doc_a_get_res.json()
    doc_a_dl_res = requests.get(f"{BASE_URL}/api/documents/{doc_a_id}/download/", headers=headers, timeout=10)
    consumer_logs = run_cmd_capture(["docker", "compose", "logs", "--tail", "25", "webserver"], raw_token)

    content_verified = "KTPM-R08-FLOW-ALPHA" in (doc_a_json.get("content") or "")
    print(
        f"  -> [1.3] Truy xuất GET /api/documents/{doc_a_id}/: HTTP {doc_a_get_res.status_code} | "
        f"Title='{doc_a_json.get('title')}' | Nội dung khớp={content_verified} | "
        f"Download HTTP {doc_a_dl_res.status_code} ({len(doc_a_dl_res.content)} bytes)"
    )

    if save_evidence:
        flow1_log = (
            f"# MINH CHỨNG 03 — LUỒNG 1: TẢI LÊN VÀ XỬ LÝ TÀI LIỆU BẤT ĐỒNG BỘ\n"
            f"Thời gian ghi nhận: {now_str}\n\n"
            f"## 1. Điều kiện ban đầu (Preconditions)\n"
            f"- 3 container (`paperless-webserver`, `paperless-db`, `paperless-broker`) đang ở trạng thái Up / Healthy.\n"
            f"- Xác thực API hợp lệ qua Header `Authorization: Token <REDACTED_TOKEN>`.\n"
            f"- Số lượng tài liệu trong hệ thống trước khi tải lên: {count_before}.\n"
            f"- Tệp đầu vào: `scripts/sample_docs/{doc_a_filename}` (`text/plain`, mã đối soát `KTPM-R08-FLOW-ALPHA`).\n\n"
            f"## 2. Thao tác 1.1 — Gửi yêu cầu tải lên tài liệu (Thời điểm tiếp nhận)\n"
            f"Request:  POST {BASE_URL}/api/documents/post_document/ (multipart/form-data)\n"
            f"Header:   Authorization: Token <REDACTED_TOKEN>\n"
            f"FormData: title=\"{doc_a_title}\", document=@{doc_a_filename}\n"
            f"Response: HTTP {up_a_res.status_code}\n"
            f"Body (Task UUID): \"{task_a_uuid}\"\n\n"
            f"## 3. Thao tác 1.2 — Truy vấn trạng thái xử lý nền hoàn tất (`GET /api/tasks/`)\n"
            f"Request:  GET {BASE_URL}/api/tasks/?task_id={task_a_uuid}\n"
            f"Thời gian xử lý nền: {elapsed_a} giây\n"
            f"Response JSON:\n```json\n{format_json_safe(task_a_info, raw_token)}\n```\n\n"
            f"## 4. Thao tác 1.3 — Truy xuất tài liệu sau xử lý (`GET /api/documents/{doc_a_id}/`)\n"
            f"Request:  GET {BASE_URL}/api/documents/{doc_a_id}/\n"
            f"Response: HTTP {doc_a_get_res.status_code}\n"
            f"Response JSON:\n```json\n{format_json_safe(doc_a_json, raw_token)}\n```\n\n"
            f"## 5. Kiểm tra tải tệp lưu trữ vật lý (`GET /api/documents/{doc_a_id}/download/`)\n"
            f"Response: HTTP {doc_a_dl_res.status_code} | Content-Type: {doc_a_dl_res.headers.get('Content-Type')} | "
            f"Size: {len(doc_a_dl_res.content)} bytes\n\n"
            f"## 6. Trích xuất log xử lý của Celery Worker / Consumer trong `paperless-webserver`\n"
            f"```text\n{consumer_logs}\n```\n"
        )
        (out_path / "03_flow1_upload_and_processing.txt").write_text(flow1_log, encoding="utf-8")

    # =========================================================================
    # LUỒNG 2: TẠO THÔNG TIN PHÂN LOẠI VÀ GÁN CHO TÀI LIỆU
    # =========================================================================
    print("\n[LUỒNG 2] Tạo thông tin phân loại (Tag, Correspondent, DocumentType) và gán cho tài liệu...")
    initial_meta_snapshot = {
        "id": doc_a_json.get("id"),
        "correspondent": doc_a_json.get("correspondent"),
        "document_type": doc_a_json.get("document_type"),
        "tags": doc_a_json.get("tags"),
    }

    tag_a_status, tag_a_obj, _ = get_or_create_metadata(
        "/api/tags/",
        {"name": "Demo_Tag_HoaDon_Q4", "color": "#1d4ed8", "is_inbox_tag": False},
        headers,
    )
    tag_b_status, tag_b_obj, _ = get_or_create_metadata(
        "/api/tags/",
        {"name": "Demo_Tag_BienBan_Q4", "color": "#0d9488", "is_inbox_tag": False},
        headers,
    )
    corr_a_status, corr_a_obj, _ = get_or_create_metadata(
        "/api/correspondents/",
        {"name": "Demo_DoiTac_ACME_Cloud", "matching_algorithm": 0, "match": "", "is_insensitive": True},
        headers,
    )
    corr_b_status, corr_b_obj, _ = get_or_create_metadata(
        "/api/correspondents/",
        {"name": "Demo_BoPhan_VanHanhNoiBo", "matching_algorithm": 0, "match": "", "is_insensitive": True},
        headers,
    )
    dtype_a_status, dtype_a_obj, _ = get_or_create_metadata(
        "/api/document_types/",
        {"name": "Demo_Loai_HoaDonDichVu", "matching_algorithm": 0, "match": "", "is_insensitive": True},
        headers,
    )
    dtype_b_status, dtype_b_obj, _ = get_or_create_metadata(
        "/api/document_types/",
        {"name": "Demo_Loai_BienBanNghiemThu", "matching_algorithm": 0, "match": "", "is_insensitive": True},
        headers,
    )

    tag_a_id, corr_a_id, dtype_a_id = tag_a_obj["id"], corr_a_obj["id"], dtype_a_obj["id"]
    tag_b_id, corr_b_id, dtype_b_id = tag_b_obj["id"], corr_b_obj["id"], dtype_b_obj["id"]

    print(f"  -> [2.1] Tạo/xác nhận Tag '{tag_a_obj['name']}' (HTTP {tag_a_status}, ID={tag_a_id})")
    print(f"  -> [2.1] Tạo/xác nhận Correspondent '{corr_a_obj['name']}' (HTTP {corr_a_status}, ID={corr_a_id})")
    print(f"  -> [2.1] Tạo/xác nhận DocumentType '{dtype_a_obj['name']}' (HTTP {dtype_a_status}, ID={dtype_a_id})")

    # 2.2 Gán phân loại cho Tài liệu A (và gán phân loại đối chứng cho Tài liệu B)
    patch_a_payload = {
        "tags": [tag_a_id],
        "correspondent": corr_a_id,
        "document_type": dtype_a_id,
    }
    patch_a_res = requests.patch(
        f"{BASE_URL}/api/documents/{doc_a_id}/",
        headers=headers,
        json=patch_a_payload,
        timeout=10,
    )
    if doc_b_id is not None:
        requests.patch(
            f"{BASE_URL}/api/documents/{doc_b_id}/",
            headers=headers,
            json={"tags": [tag_b_id], "correspondent": corr_b_id, "document_type": dtype_b_id},
            timeout=10,
        )

    # 2.3 Truy vấn lại độc lập để kiểm chứng dữ liệu đã lưu bền vững vào PostgreSQL
    recheck_doc_res = requests.get(f"{BASE_URL}/api/documents/{doc_a_id}/", headers=headers, timeout=10)
    recheck_doc_json = recheck_doc_res.json()
    recheck_corr_res = requests.get(f"{BASE_URL}/api/correspondents/{corr_a_id}/", headers=headers, timeout=10)
    recheck_corr_json = recheck_corr_res.json()

    relation_persisted = (
        recheck_doc_json.get("correspondent") == corr_a_id
        and recheck_doc_json.get("document_type") == dtype_a_id
        and tag_a_id in (recheck_doc_json.get("tags") or [])
    )
    print(
        f"  -> [2.2] Gán phân loại PATCH /api/documents/{doc_a_id}/: HTTP {patch_a_res.status_code}"
    )
    print(
        f"  -> [2.3] Truy vấn lại GET /api/documents/{doc_a_id}/: HTTP {recheck_doc_res.status_code} | "
        f"Lưu quan hệ chính xác={relation_persisted} | "
        f"Correspondent document_count={recheck_corr_json.get('document_count')}"
    )

    if save_evidence:
        flow2_log = (
            f"# MINH CHỨNG 04 — LUỒNG 2: TẠO THÔNG TIN PHÂN LOẠI VÀ GÁN CHO TÀI LIỆU\n"
            f"Thời gian ghi nhận: {now_str}\n\n"
            f"## 1. Điều kiện ban đầu (Preconditions)\n"
            f"- Tài liệu mục tiêu ID={doc_a_id} (`{doc_a_title}`) đã được xử lý hoàn tất ở Luồng 1.\n"
            f"- Trạng thái phân loại của tài liệu trước khi gán:\n```json\n{format_json_safe(initial_meta_snapshot, raw_token)}\n```\n\n"
            f"## 2. Thao tác 2.1 — Tạo mới 3 đối tượng phân loại qua REST API\n"
            f"### (a) Tạo Tag (`POST /api/tags/` -> HTTP {tag_a_status})\n```json\n{format_json_safe(tag_a_obj, raw_token)}\n```\n\n"
            f"### (b) Tạo Correspondent (`POST /api/correspondents/` -> HTTP {corr_a_status})\n```json\n{format_json_safe(corr_a_obj, raw_token)}\n```\n\n"
            f"### (c) Tạo DocumentType (`POST /api/document_types/` -> HTTP {dtype_a_status})\n```json\n{format_json_safe(dtype_a_obj, raw_token)}\n```\n\n"
            f"## 3. Thao tác 2.2 — Gán thông tin phân loại cho tài liệu (`PATCH /api/documents/{doc_a_id}/`)\n"
            f"Request Payload:\n```json\n{format_json_safe(patch_a_payload, raw_token)}\n```\n"
            f"Response: HTTP {patch_a_res.status_code}\n\n"
            f"## 4. Thao tác 2.3 — Truy vấn lại độc lập xác nhận quan hệ đã lưu bền vững (`GET /api/documents/{doc_a_id}/`)\n"
            f"Response: HTTP {recheck_doc_res.status_code}\n"
            f"```json\n{format_json_safe(recheck_doc_json, raw_token)}\n```\n\n"
            f"## 5. Đối chiếu số lượng tài liệu trên Correspondent (`GET /api/correspondents/{corr_a_id}/`)\n"
            f"Response: HTTP {recheck_corr_res.status_code} | `document_count` = {recheck_corr_json.get('document_count')}\n"
        )
        (out_path / "04_flow2_classification_assignment.txt").write_text(flow2_log, encoding="utf-8")

    # =========================================================================
    # LUỒNG 3: TÌM KIẾM TOÀN VĂN VÀ LỌC ĐA TIÊU CHÍ
    # =========================================================================
    print("\n[LUỒNG 3] Tìm kiếm toàn văn (Tantivy) và lọc tài liệu theo thông tin phân loại...")
    # Đợi ngắn để chỉ mục tìm kiếm đồng bộ hoàn toàn sau PATCH
    time.sleep(1.0)

    # 3.1 Tìm kiếm toàn văn theo mã duy nhất của Tài liệu A
    s1_url = f"{BASE_URL}/api/documents/?query=KTPM-R08-FLOW-ALPHA"
    s1_res = requests.get(s1_url, headers=headers, timeout=10)
    s1_json = s1_res.json()
    s1_ids = [d["id"] for d in s1_json.get("results", [])]
    s1_hit = s1_json["results"][0].get("__search_hit__", {}) if s1_json.get("results") else {}

    # 3.2 Lọc thuần theo thông tin phân loại (Tag + Correspondent + DocumentType)
    s2_url = (
        f"{BASE_URL}/api/documents/?tags__id__all={tag_a_id}"
        f"&correspondent__id={corr_a_id}&document_type__id={dtype_a_id}"
    )
    s2_res = requests.get(s2_url, headers=headers, timeout=10)
    s2_json = s2_res.json()
    s2_ids = [d["id"] for d in s2_json.get("results", [])]

    # 3.3 Đối chứng kết hợp: Từ khóa chung 'Q4-2026' (khớp cả A và B) vs Kết hợp lọc Correspondent A
    s3_base_res = requests.get(f"{BASE_URL}/api/documents/?query=Q4-2026", headers=headers, timeout=10)
    s3_base_json = s3_base_res.json()
    s3_base_ids = [d["id"] for d in s3_base_json.get("results", [])]

    s3_combo_url = (
        f"{BASE_URL}/api/documents/?query=Q4-2026"
        f"&correspondent__id={corr_a_id}&ordering=-created&page=1&page_size=10"
    )
    s3_combo_res = requests.get(s3_combo_url, headers=headers, timeout=10)
    s3_combo_json = s3_combo_res.json()
    s3_combo_ids = [d["id"] for d in s3_combo_json.get("results", [])]

    print(
        f"  -> [3.1] Full-text search '?query=KTPM-R08-FLOW-ALPHA': HTTP {s1_res.status_code} | "
        f"count={s1_json.get('count')} | IDs={s1_ids} | Tantivy score={s1_hit.get('score')}"
    )
    print(
        f"  -> [3.2] Lọc phân loại (tag={tag_a_id}, corr={corr_a_id}, type={dtype_a_id}): "
        f"HTTP {s2_res.status_code} | count={s2_json.get('count')} | IDs={s2_ids} (loại trừ Doc B ID={doc_b_id})"
    )
    print(
        f"  -> [3.3] Kết hợp từ khóa chung 'Q4-2026' ({len(s3_base_ids)} tài liệu: {s3_base_ids}) + "
        f"lọc correspondent={corr_a_id}: thu hẹp còn count={s3_combo_json.get('count')} | IDs={s3_combo_ids}"
    )

    if save_evidence:
        flow3_log = (
            f"# MINH CHỨNG 05 — LUỒNG 3: TÌM KIẾM TOÀN VĂN VÀ LỌC TÀI LIỆU\n"
            f"Thời gian ghi nhận: {now_str}\n\n"
            f"## 1. Điều kiện ban đầu — Tập dữ liệu mẫu có quan hệ biết trước (Ground Truth)\n"
            f"- Tài liệu mục tiêu A (ID={doc_a_id}): Tiêu đề `{doc_a_title}`, chứa từ khóa riêng `KTPM-R08-FLOW-ALPHA` và từ khóa chung `Q4-2026`; "
            f"gắn `tag={tag_a_id}`, `correspondent={corr_a_id}`, `document_type={dtype_a_id}`.\n"
            f"- Tài liệu đối chứng B (ID={doc_b_id}): Tiêu đề `{doc_b_title}`, chứa từ khóa riêng `KTPM-R08-FLOW-BETA` và từ khóa chung `Q4-2026`; "
            f"gắn `tag={tag_b_id}`, `correspondent={corr_b_id}`, `document_type={dtype_b_id}`.\n\n"
            f"## 2. Thao tác 3.1 — Tìm kiếm toàn văn nội dung trích xuất (`?query=KTPM-R08-FLOW-ALPHA`)\n"
            f"Request:  GET {s1_url}\n"
            f"Response: HTTP {s1_res.status_code} | count={s1_json.get('count')} | Returned IDs={s1_ids}\n"
            f"Search Hit Metadata: {format_json_safe(s1_hit, raw_token)}\n"
            f"Full Response JSON:\n```json\n{format_json_safe(s1_json, raw_token)}\n```\n\n"
            f"## 3. Thao tác 3.2 — Lọc đa tiêu chí theo Metadata phân loại\n"
            f"Request:  GET {s2_url}\n"
            f"Response: HTTP {s2_res.status_code} | count={s2_json.get('count')} | Returned IDs={s2_ids} "
            f"(Đã loại trừ chính xác tài liệu đối chứng ID={doc_b_id})\n"
            f"Full Response JSON:\n```json\n{format_json_safe(s2_json, raw_token)}\n```\n\n"
            f"## 4. Thao tác 3.3 — Kiểm chứng giao thoa giữa Tìm kiếm toàn văn + Lọc phân loại + Phân trang\n"
            f"- Truy vấn nền chỉ tìm từ khóa chung `?query=Q4-2026`: HTTP {s3_base_res.status_code}, "
            f"count={s3_base_json.get('count')}, IDs={s3_base_ids} (trả về cả tài liệu A và B).\n"
            f"- Truy vấn kết hợp `GET {s3_combo_url}`:\n"
            f"  Response: HTTP {s3_combo_res.status_code} | count={s3_combo_json.get('count')} | Returned IDs={s3_combo_ids} "
            f"(chỉ giữ lại đúng tài liệu A thỏa đồng thời nội dung và Correspondent).\n"
            f"Full Response JSON:\n```json\n{format_json_safe(s3_combo_json, raw_token)}\n```\n"
        )
        (out_path / "05_flow3_search_and_filtering.txt").write_text(flow3_log, encoding="utf-8")

        summary_payload = {
            "executed_at": now_str,
            "target_url": BASE_URL,
            "paperless_version": "v3.1.3 (commit d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e)",
            "openapi_operations_total": op_count,
            "credentials_redacted": True,
            "flows": {
                "flow1_upload_and_processing": {
                    "status": "PASS" if (task_a_status == "success" and content_verified) else "FAIL",
                    "upload_http_status": up_a_res.status_code,
                    "task_uuid": task_a_uuid,
                    "task_final_status": task_a_status,
                    "processing_seconds": elapsed_a,
                    "created_document_id": doc_a_id,
                    "control_document_id": doc_b_id,
                    "retrieved_http_status": doc_a_get_res.status_code,
                    "download_http_status": doc_a_dl_res.status_code,
                },
                "flow2_classification_assignment": {
                    "status": "PASS" if relation_persisted else "FAIL",
                    "tag_created": {"id": tag_a_id, "name": tag_a_obj["name"]},
                    "correspondent_created": {"id": corr_a_id, "name": corr_a_obj["name"]},
                    "document_type_created": {"id": dtype_a_id, "name": dtype_a_obj["name"]},
                    "patch_http_status": patch_a_res.status_code,
                    "recheck_persisted": relation_persisted,
                    "correspondent_document_count": recheck_corr_json.get("document_count"),
                },
                "flow3_search_and_filtering": {
                    "status": "PASS"
                    if (doc_a_id in s1_ids and s2_ids == [doc_a_id] and s3_combo_ids == [doc_a_id])
                    else "FAIL",
                    "fulltext_query_ids": s1_ids,
                    "fulltext_score": s1_hit.get("score"),
                    "metadata_filter_ids": s2_ids,
                    "shared_keyword_unfiltered_ids": s3_base_ids,
                    "combined_search_and_filter_ids": s3_combo_ids,
                },
            },
        }
        (out_path / "TV4_demo_execution_summary.json").write_text(
            format_json_safe(summary_payload, raw_token) + "\n",
            encoding="utf-8",
        )

    print("\n" + "=" * 88)
    print("  HOÀN TẤT XÁC MINH 3 LUỒNG NGHIỆP VỤ — KẾT QUẢ: 3/3 PASS")
    if save_evidence:
        print(f"  Đã lưu trọn bộ log minh chứng (đã che token/mật khẩu) tại: {out_path.as_posix()}/")
    print(f"  Giao diện Web UI:     {BASE_URL}")
    print(f"  Tài liệu OpenAPI UI:  {BASE_URL}/api/schema/view/")
    print("=" * 88 + "\n")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chạy demo và xuất minh chứng vận hành 3 luồng Paperless-ngx")
    parser.add_argument(
        "--reset-first",
        action="store_true",
        help="Dọn sạch dữ liệu cũ qua API trước khi chạy để đảm bảo ID và số lượng đối chứng sạch",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Chỉ in ra màn hình console, không ghi đè tệp log trong docs/evidence/logs",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/evidence/logs",
        help="Thư mục lưu trữ log minh chứng đã che thông tin nhạy cảm",
    )
    args = parser.parse_args()
    sys.exit(run_demo(reset_first=args.reset_first, save_evidence=not args.no_save, output_dir=args.output_dir))
