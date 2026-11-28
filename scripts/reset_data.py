#!/usr/bin/env python3
"""
scripts/reset_data.py
Script dọn sạch dữ liệu kiểm thử (Documents + Trash, Tags, Correspondents, DocumentTypes) qua API.
Hỗ trợ lặp qua toàn bộ phân trang (pagination) và dọn thùng rác (empty trash),
giữ nguyên tài khoản người dùng và cấu hình hệ thống.
Không in mật khẩu hoặc token ra màn hình/log.
"""

import os
import sys
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


def get_auth_token() -> str:
    env_token = os.getenv("PAPERLESS_TOKEN", "").strip()
    if env_token:
        return env_token
    res = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": ADMIN_USER, "password": ADMIN_PASS},
        timeout=10,
    )
    if res.status_code == 200:
        token = res.json().get("token", "")
        print("[OK] Xác thực API thành công (Token: <REDACTED_TOKEN>)")
        return token
    print(f"[LỖI] Không thể xác thực API: HTTP {res.status_code}")
    sys.exit(1)


def delete_all_paginated(name: str, endpoint: str, headers: dict) -> int:
    deleted_total = 0
    while True:
        res = requests.get(f"{BASE_URL}{endpoint}?page=1&page_size=100", headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"[LỖI] Không thể lấy danh sách {name}: HTTP {res.status_code}")
            break
        data = res.json()
        items = data.get("results", [])
        if not items:
            break
        for item in items:
            item_id = item["id"]
            del_res = requests.delete(f"{BASE_URL}{endpoint}{item_id}/", headers=headers, timeout=15)
            if del_res.status_code in (200, 204):
                deleted_total += 1
            else:
                print(f"  - [LỖI] Không thể xóa {name} ID {item_id}: HTTP {del_res.status_code}")
        if len(items) == 0:
            break
    print(f"[OK] Đã xóa tổng cộng {deleted_total} bản ghi {name}.")
    return deleted_total


def empty_trash_if_any(headers: dict) -> None:
    res = requests.get(f"{BASE_URL}/api/trash/?page=1&page_size=100", headers=headers, timeout=15)
    if res.status_code != 200:
        return
    items = res.json().get("results", [])
    if not items:
        return
    doc_ids = [item["id"] for item in items]
    empty_res = requests.post(
        f"{BASE_URL}/api/trash/",
        headers=headers,
        json={"documents": doc_ids, "action": "empty"},
        timeout=20,
    )
    if empty_res.status_code in (200, 204):
        print(f"[OK] Đã làm rỗng thùng rác ({len(doc_ids)} tài liệu).")


def reset_api() -> None:
    print("=== BẮT ĐẦU DỌN DẸP DỮ LIỆU KIỂM THỬ QUA API (CÓ PHÂN TRANG) ===")
    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}

    delete_all_paginated("documents", "/api/documents/", headers)
    empty_trash_if_any(headers)
    delete_all_paginated("tags", "/api/tags/", headers)
    delete_all_paginated("correspondents", "/api/correspondents/", headers)
    delete_all_paginated("document_types", "/api/document_types/", headers)

    print("=== DỌN DẸP DỮ LIỆU QUA API HOÀN TẤT ===")


if __name__ == "__main__":
    reset_api()
