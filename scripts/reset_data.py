#!/usr/bin/env python3
"""
scripts/reset_data.py
Script dọn sạch dữ liệu kiểm thử (Documents, Tags, Correspondents, DocumentTypes) qua API
giữ nguyên người dùng và cấu hình hệ thống.
"""

import os
import sys
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")


def get_auth_token():
    url = f"{BASE_URL}/api/token/"
    payload = {"username": ADMIN_USER, "password": ADMIN_PASS}
    res = requests.post(url, data=payload, timeout=10)
    if res.status_code == 200:
        return res.json().get("token")
    else:
        print(f"[LỖI] Không thể lấy token: {res.status_code}")
        sys.exit(1)


def reset_api():
    print("=== BẮT ĐẦU DỌN DẸP DỮ LIỆU QUA API ===")
    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}

    endpoints = [
        ("documents", "/api/documents/"),
        ("tags", "/api/tags/"),
        ("correspondents", "/api/correspondents/"),
        ("document_types", "/api/document_types/"),
    ]

    for name, ep in endpoints:
        res = requests.get(f"{BASE_URL}{ep}", headers=headers)
        if res.status_code == 200:
            items = res.json().get("results", [])
            print(f"[INFO] Tìm thấy {len(items)} {name} cần xóa...")
            for item in items:
                item_id = item["id"]
                del_res = requests.delete(f"{BASE_URL}{ep}{item_id}/", headers=headers)
                if del_res.status_code in (204, 200):
                    print(f"  - Đã xóa {name} ID {item_id}")
                else:
                    print(f"  - [LỖI] Không thể xóa {name} ID {item_id}: {del_res.status_code}")
        else:
            print(f"[LỖI] Không thể lấy danh sách {name}: {res.status_code}")

    print("=== DỌN DẸP DỮ LIỆU QUA API HOÀN TẤT ===")


if __name__ == "__main__":
    reset_api()
