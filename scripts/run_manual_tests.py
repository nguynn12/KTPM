#!/usr/bin/env python3
"""
scripts/run_manual_tests.py
Script thực thi kiểm thử thủ công tự động cho hệ thống Paperless-ngx
Phục vụ đề tài Kiểm thử phần mềm - TV4 (Nguyễn Nhất Minh - MSSV: 2312690)
Tài nguyên chuyên trách: Correspondents (TC-CORR-01 đến TC-CORR-18) và Tags (TC-TAG-01 đến TC-TAG-19)
"""

import os
import sys
import time
import argparse
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
    try:
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code == 200:
            return res.json().get("token")
    except Exception as e:
        print(f"[CẢNH BÁO] Không thể lấy token tự động: {e}")
    return os.getenv("PAPERLESS_TOKEN", "")


def run_correspondent_tests(headers):
    print("\n" + "=" * 95)
    print("  BỘ KIỂM THỬ THỦ CÔNG: TÀI NGUYÊN CORRESPONDENTS (PHỤ TRÁCH BỞI TV4 - NGUYỄN NHẤT MINH)")
    print("=" * 95 + "\n")

    # Lấy 1 ID mẫu để test GET {id}
    sample_id = None
    try:
        res = requests.get(f"{BASE_URL}/api/correspondents/", headers=headers, timeout=5)
        if res.status_code == 200:
            results = res.json().get("results", [])
            if results:
                sample_id = results[0]["id"]
    except Exception:
        pass

    test_cases = [
        {
            "id": "TC-CORR-01",
            "name": "Tao Correspondent hop le (truong toi thieu name)",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "TV4_Manual_Bank_Test"},
            "expected_status": 201,
            "check_schema": "document_count",  # Bắt BUG-03
        },
        {
            "id": "TC-CORR-02",
            "name": "Tao Correspondent day du cac truong",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {
                "name": "TV4_Full_Supplier_Test",
                "match": "hop dong nha cung cap",
                "matching_algorithm": 1,
                "is_insensitive": True,
            },
            "expected_status": 201,
        },
        {
            "id": "TC-CORR-03",
            "name": "Tao Correspondent thieu truong 'name'",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"match": "test"},
            "expected_status": 400,
        },
        {
            "id": "TC-CORR-04",
            "name": "Tao Correspondent voi 'name' la chuoi rong",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": ""},
            "expected_status": 400,
        },
        {
            "id": "TC-CORR-05",
            "name": "Tao Correspondent voi name dung 128 ky tu",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "A" * 128},
            "expected_status": 201,
        },
        {
            "id": "TC-CORR-06",
            "name": "Tao Correspondent vuot bien 129 ky tu",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "B" * 129},
            "expected_status": 400,
        },
        {
            "id": "TC-CORR-07",
            "name": "Tao Correspondent trung ten da co trong he thong",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "TV4_Bank_404"},
            "expected_status": 400,
        },
        {
            "id": "TC-CORR-08",
            "name": "Tao Correspondent voi matching_algorithm sai mien (99)",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "Test_Algo_99", "matching_algorithm": 99},
            "expected_status": 400,
        },
        {
            "id": "TC-CORR-11",
            "name": "Tao Correspondent voi set_permissions sai kieu (BUG-01)",
            "method": "POST",
            "endpoint": "/api/correspondents/",
            "use_auth": True,
            "payload": {"name": "Test_Crash_Corr", "set_permissions": {"view": False}},
            "expected_status": 400,  # Mong đợi 400, hệ thống sập 500
        },
        {
            "id": "TC-CORR-12",
            "name": "Lay danh sach Correspondent co phan trang",
            "method": "GET",
            "endpoint": "/api/correspondents/?page=1&page_size=10",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
        },
        {
            "id": "TC-CORR-13",
            "name": "Lay chi tiet Correspondent theo ID ton tai",
            "method": "GET",
            "endpoint": f"/api/correspondents/{sample_id}/" if sample_id else "/api/correspondents/1/",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
        },
        {
            "id": "TC-CORR-14",
            "name": "Lay chi tiet voi ID khong ton tai (999999)",
            "method": "GET",
            "endpoint": "/api/correspondents/999999/",
            "use_auth": True,
            "payload": None,
            "expected_status": 404,
        },
        {
            "id": "TC-CORR-18",
            "name": "Truy cap API khong kem Authorization header",
            "method": "GET",
            "endpoint": "/api/correspondents/",
            "use_auth": False,
            "payload": None,
            "expected_status": 401,
        },
    ]

    created_ids = []
    print(f"{'Mã TC':<11} | {'Method':<7} | {'Kỳ vọng':<8} | {'Thực tế':<8} | {'Thời gian':<10} | {'Kết quả':<11} | {'Mô tả'}")
    print("-" * 95)

    for tc in test_cases:
        url = f"{BASE_URL}{tc['endpoint']}"
        hdrs = headers if tc["use_auth"] else {"Content-Type": "application/json"}
        start = time.time()

        try:
            if tc["method"] == "GET":
                resp = requests.get(url, headers=hdrs, timeout=5)
            elif tc["method"] == "POST":
                resp = requests.post(url, headers=hdrs, json=tc["payload"], timeout=5)
            else:
                continue

            elapsed_ms = int((time.time() - start) * 1000)
            actual_status = resp.status_code

            if tc["method"] == "POST" and actual_status == 201:
                try:
                    cid = resp.json().get("id")
                    if cid:
                        created_ids.append(cid)
                except Exception:
                    pass

            verdict = "FAIL"
            if actual_status == tc["expected_status"]:
                verdict = "PASS"
                # Kiểm tra thêm nếu có check_schema
                if tc.get("check_schema") and actual_status == 201:
                    body = resp.json()
                    if tc["check_schema"] not in body:
                        verdict = "BUG-03"

            elif tc["id"] == "TC-CORR-11" and actual_status == 500:
                verdict = "BUG-01 (500)"

            print(f"{tc['id']:<11} | {tc['method']:<7} | {tc['expected_status']:<8} | {actual_status:<8} | {elapsed_ms:>5} ms   | {verdict:<11} | {tc['name']}")

        except Exception as e:
            print(f"{tc['id']:<11} | {tc['method']:<7} | {tc['expected_status']:<8} | ERROR    | 0 ms       | FAIL        | {str(e)[:30]}")

    # Dọn dẹp các đối tượng đã tạo tạm
    for cid in created_ids:
        try:
            requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=headers, timeout=5)
        except Exception:
            pass

    print("-" * 95 + "\n")


def main():
    token = get_auth_token()
    if not token:
        print("[LỖI] Không thể kết nối tới Paperless-ngx trên http://localhost:8000")
        sys.exit(1)

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    print(f"[OK] Đã xác thực thành công qua API token: {token[:8]}...")
    run_correspondent_tests(headers)


if __name__ == "__main__":
    main()
