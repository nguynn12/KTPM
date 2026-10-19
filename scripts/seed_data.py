#!/usr/bin/env python3
"""
scripts/seed_data.py
Script seed dữ liệu ban đầu cho hệ thống Paperless-ngx
Phục vụ đề tài Kiểm thử phần mềm - TV4 (Nguyễn Nhất Minh) - Seed: 404
"""

import os
import sys
import random
import argparse
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
    res = requests.post(url, data=payload, timeout=10)
    if res.status_code == 200:
        token = res.json().get("token")
        print(f"[OK] Đã lấy Auth Token: {token[:8]}...")
        return token
    else:
        print(f"[LỖI] Không thể lấy token: {res.status_code} {res.text}")
        sys.exit(1)


def seed(seed_val=404, prefix="TV4"):
    print(f"=== BẮT ĐẦU SEED DỮ LIỆU (SEED {seed_val}, PREFIX {prefix}) ===")
    random.seed(seed_val)
    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}

    # 1. Tạo Tags
    tags = [
        {"name": f"{prefix}_Tag_Invoice_{seed_val}", "color": "#e6194b", "is_inbox_tag": False},
        {"name": f"{prefix}_Tag_Urgent_{seed_val}", "color": "#3cb44b", "is_inbox_tag": False},
        {"name": f"{prefix}_Tag_Archive_{seed_val}", "color": "#ffe119", "is_inbox_tag": False},
        {"name": f"{prefix}_Tag_Finance_{seed_val}", "color": "#4363d8", "is_inbox_tag": False},
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
        {"name": f"{prefix}_Bank_{seed_val}"},
        {"name": f"{prefix}_Supplier_{seed_val}"},
        {"name": f"{prefix}_University_{seed_val}"},
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
        {"name": f"{prefix}_DocType_Invoice_{seed_val}"},
        {"name": f"{prefix}_DocType_Receipt_{seed_val}"},
        {"name": f"{prefix}_DocType_Contract_{seed_val}"},
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
            "filename": f"{prefix}_Sample_Invoice_{seed_val}.txt",
            "title": f"Hoa Don Thanh Toan Dich Vu KTPM Seed {seed_val}",
            "content": f"HOA DON BAN HANG - SO TIEN {seed_val}.000 VND - NGUOI BAN: {prefix} NGUYEN NHAT MINH - DH DA LAT",
            "tag": f"{prefix}_Tag_Invoice_{seed_val}",
            "corr": f"{prefix}_Bank_{seed_val}",
            "dtype": f"{prefix}_DocType_Invoice_{seed_val}",
        },
        {
            "filename": f"{prefix}_Sample_Contract_{seed_val}.txt",
            "title": f"Hop Dong Kiem Thu He Thong Schemathesis Seed {seed_val}",
            "content": f"HOP DONG KIEM THU PHAN MEM MON HOC - NHOM 17 - PHU TRACH {prefix} NGUYEN NHAT MINH SEED {seed_val}",
            "tag": f"{prefix}_Tag_Finance_{seed_val}",
            "corr": f"{prefix}_University_{seed_val}",
            "dtype": f"{prefix}_DocType_Contract_{seed_val}",
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
    parser = argparse.ArgumentParser(description="Seed dữ liệu cho hệ thống Paperless-ngx")
    parser.add_argument("--seed", type=int, default=404, help="Seed ngẫu nhiên")
    parser.add_argument("--prefix", default="TV4", help="Tiền tố tên đối tượng")
    args = parser.parse_args()
    seed(args.seed, args.prefix)
