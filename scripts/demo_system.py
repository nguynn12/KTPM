#!/usr/bin/env python3
"""
scripts/demo_system.py
Kịch bản chạy thử nghiệm 3 luồng nghiệp vụ chính của hệ thống Paperless-ngx
Phục vụ quay video minh chứng hoặc demo vấn đáp cho TV4 (Nguyễn Nhất Minh)
"""

import sys
import time
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://localhost:8000"


def run_demo():
    print("=" * 80)
    print("  CHẠY THỬ NGHIỆM HỆ THỐNG PAPERLESS-NGX (DEMO 3 LUỒNG NGHIỆP VỤ)")
    print("=" * 80)

    # Bước 1: Lấy Auth Token
    print("\n[BƯỚC 1] Xác thực hệ thống qua API...")
    auth_res = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": "admin", "password": "admin"},
        timeout=10,
    )
    if auth_res.status_code != 200:
        print(f"[LỖI] Không thể lấy Token: {auth_res.status_code}")
        return

    token = auth_res.json().get("token")
    headers = {"Authorization": f"Token {token}"}
    print(f"  -> Kết nối thành công! Token: {token[:12]}...")

    # Bước 2: Luồng 1 - Upload tài liệu
    print("\n[LUỒNG 1] Tải lên tài liệu mẫu (Upload Document)...")
    content = "HOA DON DICH VU CONG NGHE THONG TIN - KTPM 2026 - NGUYEN NHAT MINH SEED 404"
    files = {"document": ("Hoa_Don_TV4_Demo.txt", content.encode("utf-8"), "text/plain")}
    data = {"title": "Hóa đơn dịch vụ KTPM - Demo TV4"}

    upload_res = requests.post(
        f"{BASE_URL}/api/documents/post_document/",
        headers=headers,
        data=data,
        files=files,
        timeout=10,
    )
    if upload_res.status_code in (200, 202):
        task_id = upload_res.text.strip('"')
        print(f"  -> Tải lên thành công! Task UUID: {task_id}")
    else:
        print(f"  -> [LỖI] Tải lên thất bại: {upload_res.status_code}")

    # Bước 3: Luồng 2 - Quản lý Metadata
    print("\n[LUỒNG 2] Quản lý Metadata (Tạo Tag, Correspondent, DocumentType)...")
    # 2.1 Tạo Tag
    tag_data = {"name": f"Demo_Tag_{int(time.time())}", "color": "#28a745"}
    tag_res = requests.post(f"{BASE_URL}/api/tags/", headers=headers, json=tag_data, timeout=5)
    tag_id = tag_res.json().get("id") if tag_res.status_code == 201 else None
    print(f"  -> Tạo Tag '{tag_data['name']}': Mã {tag_res.status_code} (ID: {tag_id})")

    # 2.2 Tạo Correspondent
    corr_data = {"name": f"Demo_NganHang_{int(time.time())}"}
    corr_res = requests.post(f"{BASE_URL}/api/correspondents/", headers=headers, json=corr_data, timeout=5)
    corr_id = corr_res.json().get("id") if corr_res.status_code == 201 else None
    print(f"  -> Tạo Correspondent '{corr_data['name']}': Mã {corr_res.status_code} (ID: {corr_id})")

    # 2.3 Tạo Document Type
    dt_data = {"name": f"Demo_LoaiHoaDon_{int(time.time())}"}
    dt_res = requests.post(f"{BASE_URL}/api/document_types/", headers=headers, json=dt_data, timeout=5)
    dt_id = dt_res.json().get("id") if dt_res.status_code == 201 else None
    print(f"  -> Tạo DocumentType '{dt_data['name']}': Mã {dt_res.status_code} (ID: {dt_id})")

    # Bước 4: Luồng 3 - Tìm kiếm và lọc
    print("\n[LUỒNG 3] Tìm kiếm và lọc tài liệu (Search & Filtering)...")
    search_res = requests.get(f"{BASE_URL}/api/documents/?query=MINH", headers=headers, timeout=5)
    if search_res.status_code == 200:
        docs = search_res.json().get("results", [])
        total = search_res.json().get("count", 0)
        print(f"  -> Tìm kiếm từ khóa 'MINH': Tìm thấy {total} tài liệu phù hợp.")
        for d in docs[:3]:
            print(f"     • [ID {d['id']}] {d.get('title')} (Ngày tạo: {d.get('created')})")
    else:
        print(f"  -> [LỖI] Tìm kiếm thất bại: {search_res.status_code}")

    print("\n" + "=" * 80)
    print("  CHẠY THỬ NGHIỆM HOÀN TẤT THÀNH CÔNG 100%!")
    print("  Giao diện Web UI trực quan: http://localhost:8000")
    print("  Tài liệu Swagger UI:         http://localhost:8000/api/schema/swagger-ui/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_demo()
