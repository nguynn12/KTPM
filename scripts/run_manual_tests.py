#!/usr/bin/env python3
"""
scripts/run_manual_tests.py
Script thực thi kiểm thử thủ công cho endpoint /api/tags/
"""

import os
import sys
import time
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
AUTH_TOKEN = os.getenv("PAPERLESS_TOKEN", "3716828bfd21075a2fb68f1b959d02d2756f8d7a")

AUTH_HEADERS = {
    "Authorization": f"Token {AUTH_TOKEN}",
    "Content-Type": "application/json",
}

def run_tests():
    print("\n--- KIỂM THỬ THỦ CÔNG: /api/tags/ ---\n")

    test_cases = [
        {
            "id": "TC-TAG-01",
            "name": "Tao Tag hop le (truong toi thieu)",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "Test_Tag_Manual_01"},
            "expected_status": 201,
        },
        {
            "id": "TC-TAG-03",
            "name": "Tao Tag thieu truong 'name'",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"color": "#112233"},
            "expected_status": 400,
        },
        {
            "id": "TC-TAG-04",
            "name": "Tao Tag voi 'name' rong",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": ""},
            "expected_status": 400,
        },
        {
            "id": "TC-TAG-07",
            "name": "Tao Tag trung ten da co",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "TV2_Tag_Invoice_202"},
            "expected_status": 400,
        },
        {
            "id": "TC-TAG-11",
            "name": "Tao Tag voi set_permissions sai kieu",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "Test_Crash_Perm", "set_permissions": {"view": False}},
            "expected_status": 400,
        },
        {
            "id": "TC-TAG-12",
            "name": "Lay danh sach Tag",
            "method": "GET",
            "endpoint": "/api/tags/?page=1&page_size=10",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
        },
        {
            "id": "TC-TAG-14",
            "name": "Lay chi tiet Tag theo ID",
            "method": "GET",
            "endpoint": "/api/tags/{id}/",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
        },
        {
            "id": "TC-TAG-19",
            "name": "Truy cap khong co token",
            "method": "GET",
            "endpoint": "/api/tags/",
            "use_auth": False,
            "payload": None,
            "expected_status": 401,
        },
    ]

    sample_tag_id = 95
    try:
        r = requests.get(f"{BASE_URL}/api/tags/", headers=AUTH_HEADERS, timeout=5)
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                sample_tag_id = results[0]["id"]
    except Exception:
        pass

    created_tag_ids = []

    print(f"{'Mã TC':<11} | {'Method':<7} | {'Kỳ vọng':<8} | {'Thực tế':<8} | {'Thời gian':<10} | {'Kết quả':<9} | {'Mô tả'}")
    print("-" * 90)

    for tc in test_cases:
        url = f"{BASE_URL}{tc['endpoint']}".replace("{id}", str(sample_tag_id))
        headers = AUTH_HEADERS if tc["use_auth"] else {"Content-Type": "application/json"}
        start_time = time.time()

        try:
            if tc["method"] == "GET":
                resp = requests.get(url, headers=headers, timeout=5)
            elif tc["method"] == "POST":
                resp = requests.post(url, headers=headers, json=tc["payload"], timeout=5)
            else:
                continue

            elapsed_ms = int((time.time() - start_time) * 1000)
            actual_status = resp.status_code

            if tc["method"] == "POST" and actual_status == 201:
                try:
                    created_tag_ids.append(resp.json().get("id"))
                except Exception:
                    pass

            if actual_status == tc["expected_status"]:
                verdict = "PASS"
            elif tc["id"] == "TC-TAG-11" and actual_status == 500:
                verdict = "BUG (500)"
            else:
                verdict = "FAIL"

            print(f"{tc['id']:<11} | {tc['method']:<7} | {tc['expected_status']:<8} | {actual_status:<8} | {elapsed_ms:>5} ms   | {verdict:<9} | {tc['name']}")

        except Exception as e:
            print(f"{tc['id']:<11} | {tc['method']:<7} | {tc['expected_status']:<8} | ERROR    | 0 ms       | FAIL      | {str(e)[:30]}")

    for tid in created_tag_ids:
        if tid:
            try:
                requests.delete(f"{BASE_URL}/api/tags/{tid}/", headers=AUTH_HEADERS, timeout=5)
            except Exception:
                pass

    print("-" * 90 + "\n")

if __name__ == "__main__":
    run_tests()
