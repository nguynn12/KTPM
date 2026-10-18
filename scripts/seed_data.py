#!/usr/bin/env python3
"""
scripts/seed_data.py
Script seed dữ liệu ban đầu cho hệ thống Paperless-ngx
Phục vụ đề tài Kiểm thử phần mềm - TV2 (Tạ Nhật Nguyên) - Seed: 202
"""

import os
import sys
import random
import time
from pathlib import Path
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SEED_VALUE = 202
random.seed(SEED_VALUE)

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")


def get_auth_token():
    url = f"{BASE_URL}/api/token/"
    payload = {"username": ADMIN_USER, "password": ADMIN_PASS}
    res = requests.post(url, data=payload, timeout=10)
    if res.status_code == 200:
        token = res.json().get("token")
        print(f"[OK] Đã lấy Auth Token: {token[:8]}...")
        return token
    else:
        print(f"[LỖI] Không thể lấy token: {res.status_code} {res.text}")
        sys.exit(1)


def seed():
    print(f"=== BẮT ĐẦU SEED DỮ LIỆU (SEED {SEED_VALUE}) ===")
    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}

    # 1. Tạo Tags
    tags = [
        {"name": "TV2_Tag_Invoice_202", "color": "#e6194b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Urgent_202", "color": "#3cb44b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Archive_202", "color": "#ffe119", "is_inbox_tag": False},
        {"name": "TV2_Tag_Finance_202", "color": "#4363d8", "is_inbox_tag": False},
    ]
    created_tags = {}
    for tag_data in tags:
        res = requests.post(f"{BASE_URL}/api/tags/", json=tag_data, headers=headers)
        if res.status_code == 201:
            item = res.json()
            created_tags[item["name"]] = item["id"]
            print(f"[OK] Đã tạo Tag '{item['name']}' (ID: {item['id']})")
        elif res.status_code == 400 and "already exists" in res.text:
            print(f"[INFO] Tag '{tag_data['name']}' đã tồn tại")
        else:
            print(f"[CẢNH BÁO] Không thể tạo tag '{tag_data['name']}': {res.status_code} {res.text}")

    # 2. Tạo Correspondents
    correspondents = [
        {"name": "TV2_Bank_202"},
        {"name": "TV2_Supplier_202"},
        {"name": "TV2_University_202"},
    ]
    created_correspondents = {}
    for corr in correspondents:
        res = requests.post(f"{BASE_URL}/api/correspondents/", json=corr, headers=headers)
        if res.status_code == 201:
            item = res.json()
            created_correspondents[item["name"]] = item["id"]
            print(f"[OK] Đã tạo Correspondent '{item['name']}' (ID: {item['id']})")
        elif res.status_code == 400 and "already exists" in res.text:
            print(f"[INFO] Correspondent '{corr['name']}' đã tồn tại")
        else:
            print(f"[CẢNH BÁO] Không thể tạo correspondent '{corr['name']}': {res.status_code} {res.text}")

    # 3. Tạo Document Types
    doc_types = [
        {"name": "TV2_DocType_Invoice_202"},
        {"name": "TV2_DocType_Receipt_202"},
        {"name": "TV2_DocType_Contract_202"},
    ]
    created_doc_types = {}
    for dt in doc_types:
        res = requests.post(f"{BASE_URL}/api/document_types/", json=dt, headers=headers)
        if res.status_code == 201:
            item = res.json()
            created_doc_types[item["name"]] = item["id"]
            print(f"[OK] Đã tạo DocumentType '{item['name']}' (ID: {item['id']})")
        elif res.status_code == 400 and "already exists" in res.text:
            print(f"[INFO] DocumentType '{dt['name']}' đã tồn tại")
        else:
            print(f"[CẢNH BÁO] Không thể tạo doc_type '{dt['name']}': {res.status_code} {res.text}")

    # 4. Upload 2 tài liệu mẫu qua Luồng 1 (POST /api/documents/post_document/)
    temp_dir = Path("scripts/sample_docs")
    temp_dir.mkdir(parents=True, exist_ok=True)

    sample_files = [
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
            "content": "HOP DONG KIEM THU PHAN MEM MON HOC - NHÓM 5 - PHU TRACH TV2 TA NHAT NGUYEN SEED 202",
            "tag": "TV2_Tag_Finance_202",
            "corr": "TV2_University_202",
            "dtype": "TV2_DocType_Contract_202",
        },
    ]

    for sample in sample_files:
        file_path = temp_dir / sample["filename"]
        file_path.write_text(sample["content"], encoding="utf-8")

        post_data = {
            "title": sample["title"],
        }
        if sample["tag"] in created_tags:
            post_data["tags"] = [created_tags[sample["tag"]]]
        if sample["corr"] in created_correspondents:
            post_data["correspondent"] = created_correspondents[sample["corr"]]
        if sample["dtype"] in created_doc_types:
            post_data["document_type"] = created_doc_types[sample["dtype"]]

        with open(file_path, "rb") as f:
            files = {"document": (sample["filename"], f, "text/plain")}
            res = requests.post(
                f"{BASE_URL}/api/documents/post_document/",
                data=post_data,
                files=files,
                headers=headers,
            )
            if res.status_code in (200, 202):
                task_id = res.text.strip('"')
                print(f"[OK] Đã tải lên '{sample['filename']}' thành công (Task UUID: {task_id})")
            else:
                print(f"[LỖI] Tải lên '{sample['filename']}' thất bại: {res.status_code} {res.text}")

    print("=== SEED DỮ LIỆU HOÀN TẤT THÀNH CÔNG ===")


if __name__ == "__main__":
    seed()
