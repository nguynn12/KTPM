#!/usr/bin/env python3
"""
scripts/reset_data_TV3.py
Dọn dẹp dữ liệu qua REST API có xử lý phân trang toàn diện (full pagination),
xử lý trash và nạp lại dữ liệu baseline nhóm cho TV3.
Không xóa Docker volume.
"""

import os
import sys
import time
from pathlib import Path
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
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
        return res.json().get("token")
    else:
        print(f"[LỖI] Không thể lấy token: HTTP {res.status_code}")
        sys.exit(1)


def get_all_items(endpoint, headers):
    items = []
    url = f"{BASE_URL}{endpoint}"
    while url:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            break
        data = res.json()
        items.extend(data.get("results", []))
        url = data.get("next")
    return items


def clean_api_data(headers):
    print("=== DỌN DẸP DỮ LIỆU QUA API (XỬ LÝ ĐẦY ĐỦ PHÂN TRANG) ===")

    # 1. Xóa documents
    docs = get_all_items("/api/documents/", headers)
    print(f"[INFO] Tìm thấy {len(docs)} documents cần xóa...")
    for d in docs:
        del_res = requests.delete(f"{BASE_URL}/api/documents/{d['id']}/", headers=headers, timeout=10)
        print(f"  - Xóa Document ID {d['id']}: HTTP {del_res.status_code}")

    # Xóa thùng rác (trash) nếu có
    try:
        requests.post(f"{BASE_URL}/api/documents/empty_trash/", headers=headers, timeout=10)
    except Exception:
        pass

    # 2. Xóa Tags
    tags = get_all_items("/api/tags/", headers)
    print(f"[INFO] Tìm thấy {len(tags)} tags cần xóa...")
    for t in tags:
        del_res = requests.delete(f"{BASE_URL}/api/tags/{t['id']}/", headers=headers, timeout=10)
        print(f"  - Xóa Tag ID {t['id']}: HTTP {del_res.status_code}")

    # 3. Xóa Correspondents
    corrs = get_all_items("/api/correspondents/", headers)
    print(f"[INFO] Tìm thấy {len(corrs)} correspondents cần xóa...")
    for c in corrs:
        del_res = requests.delete(f"{BASE_URL}/api/correspondents/{c['id']}/", headers=headers, timeout=10)
        print(f"  - Xóa Correspondent ID {c['id']}: HTTP {del_res.status_code}")

    # 4. Xóa Document Types
    dtypes = get_all_items("/api/document_types/", headers)
    print(f"[INFO] Tìm thấy {len(dtypes)} document_types cần xóa...")
    for dt in dtypes:
        del_res = requests.delete(f"{BASE_URL}/api/document_types/{dt['id']}/", headers=headers, timeout=10)
        print(f"  - Xóa DocumentType ID {dt['id']}: HTTP {del_res.status_code}")

    print("=== DỌN DẸP API HOÀN TẤT ===")


def wait_for_task(task_id, headers, timeout_seconds=60):
    url = f"{BASE_URL}/api/tasks/?task_id={task_id}"
    start = time.time()
    while time.time() - start < timeout_seconds:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            tasks = data.get("results", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            for t in tasks:
                if str(t.get("task_id")) == str(task_id):
                    status = str(t.get("status", "")).lower()
                    if status == "success":
                        doc_ids = t.get("related_document_ids", [])
                        doc_id = doc_ids[0] if doc_ids else (t.get("result_data", {}) or {}).get("document_id")
                        return True, doc_id
                    elif status == "failure":
                        return False, None
        time.sleep(2)
    return False, None


def reseed_baseline(headers):
    print("\n=== NẠP LẠI BASELINE NHÓM (4 Tags, 3 Correspondents, 3 DocTypes, 2 TXT) ===")
    tags = [
        {"name": "TV2_Tag_Invoice_202", "color": "#e6194b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Urgent_202", "color": "#3cb44b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Archive_202", "color": "#ffe119", "is_inbox_tag": False},
        {"name": "TV2_Tag_Finance_202", "color": "#4363d8", "is_inbox_tag": False},
    ]
    tag_map = {}
    for t in tags:
        r = requests.post(f"{BASE_URL}/api/tags/", json=t, headers=headers, timeout=10)
        if r.status_code == 201:
            tag_map[t["name"]] = r.json()["id"]

    corrs = [
        {"name": "TV2_Bank_202"},
        {"name": "TV2_Supplier_202"},
        {"name": "TV2_University_202"},
    ]
    corr_map = {}
    for c in corrs:
        r = requests.post(f"{BASE_URL}/api/correspondents/", json=c, headers=headers, timeout=10)
        if r.status_code == 201:
            corr_map[c["name"]] = r.json()["id"]

    dtypes = [
        {"name": "TV2_DocType_Invoice_202"},
        {"name": "TV2_DocType_Receipt_202"},
        {"name": "TV2_DocType_Contract_202"},
    ]
    dtype_map = {}
    for dt in dtypes:
        r = requests.post(f"{BASE_URL}/api/document_types/", json=dt, headers=headers, timeout=10)
        if r.status_code == 201:
            dtype_map[dt["name"]] = r.json()["id"]

    sample_dir = Path("scripts/sample_docs")
    sample_dir.mkdir(parents=True, exist_ok=True)
    txt_samples = [
        {
            "filename": "TV2_Sample_Invoice_202.txt",
            "title": "Hoa Don Thanh Toan Dich Vu KTPM Seed 202",
            "content": "HOA DON BAN HANG - SO TIEN 202.000 VND - NGUOI BAN: TV2 TA NHAT NGUYEN - DH DA LAT",
            "tag": "TV2_Tag_Invoice_202",
            "corr": "TV2_Bank_202",
            "dtype": "TV2_DocType_Invoice_202",
        },
        {
            "filename": "TV2_Sample_Contract_202.txt",
            "title": "Hop Dong Kiem Thu He Thong Schemathesis Seed 202",
            "content": "HOP DONG KIEM THU PHAN MEM MON HOC - NHOM 5 - PHU TRACH TV2 TA NHAT NGUYEN SEED 202",
            "tag": "TV2_Tag_Finance_202",
            "corr": "TV2_University_202",
            "dtype": "TV2_DocType_Contract_202",
        },
    ]

    for s in txt_samples:
        fpath = sample_dir / s["filename"]
        if not fpath.exists():
            fpath.write_text(s["content"], encoding="utf-8")
        post_data = {"title": s["title"]}
        if s["tag"] in tag_map:
            post_data["tags"] = [tag_map[s["tag"]]]
        if s["corr"] in corr_map:
            post_data["correspondent"] = corr_map[s["corr"]]
        if s["dtype"] in dtype_map:
            post_data["document_type"] = dtype_map[s["dtype"]]

        with open(fpath, "rb") as f:
            files = {"document": (s["filename"], f, "text/plain")}
            res = requests.post(f"{BASE_URL}/api/documents/post_document/", data=post_data, files=files, headers=headers, timeout=20)
            if res.status_code in (200, 202):
                task_id = res.text.strip('"')
                wait_for_task(task_id, headers)

    print("=== BASELINE NHÓM ĐÃ ĐƯỢC PHỤC HỒI HOÀN TOÀN ===")
    for ep in ["tags", "correspondents", "document_types", "documents"]:
        r = requests.get(f"{BASE_URL}/api/{ep}/", headers=headers)
        print(f"  - Baseline {ep} count: {r.json().get('count')}")


if __name__ == "__main__":
    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}
    clean_api_data(headers)
    reseed_baseline(headers)
