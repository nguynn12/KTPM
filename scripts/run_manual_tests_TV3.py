#!/usr/bin/env python3
"""
scripts/run_manual_tests_TV3.py
Thực thi kiểm thử thủ công có thiết kế cho TV3 (Correspondents và Document Types)
Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303.
Không hardcode token. Lấy token trực tiếp từ API local.
Dọn dẹp chỉ các bản ghi do chính lần chạy này tạo ra.
"""

import os
import sys
import time
import requests
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")


def get_token():
    res = requests.post(f"{BASE_URL}/api/token/", json={"username": ADMIN_USER, "password": ADMIN_PASS}, timeout=10)
    if res.status_code == 200:
        return res.json().get("token")
    else:
        print(f"[LỖI] Không thể lấy token: HTTP {res.status_code}")
        sys.exit(1)


def run_manual_suite():
    token = get_token()
    auth_headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    run_stamp = int(time.time())

    created_corr_ids = []
    created_dt_ids = []

    print("\n" + "=" * 105)
    print(f"=== BỘ KIỂM THỬ THỦ CÔNG TV3 (CORRESPONDENTS & DOCUMENT TYPES) - RUN ID: {run_stamp} ===")
    print(f"=== Tác giả: Nguyễn Khiêm Thuận - MSSV: 2312764 - TV3                                  ===")
    print("=" * 105 + "\n")

    # Danh sách 18 ca kiểm thử tay
    test_cases = [
        # Correspondents
        {
            "id": "TV3-COR-01",
            "name": "Tạo Correspondent hợp lệ",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": f"TV3_Corr_Valid_{run_stamp}"},
            "expected_status": 201,
            "resource": "corr",
        },
        {
            "id": "TV3-COR-02",
            "name": "Tạo Correspondent thiếu trường 'name'",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-COR-03",
            "name": "Tạo Correspondent với 'name' rỗng",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": ""},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-COR-04",
            "name": "Tạo Correspondent với 'name' = null",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": None},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-COR-05",
            "name": "Tạo Correspondent trùng tên đã có",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": "TV2_Bank_202"},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-COR-06",
            "name": "Tạo Correspondent biên dưới L-1 (127 ký tự)",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": "C" * 127},
            "expected_status": 201,
            "resource": "corr",
        },
        {
            "id": "TV3-COR-07",
            "name": "Tạo Correspondent đúng biên L (128 ký tự)",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": "D" * 128},
            "expected_status": 201,
            "resource": "corr",
        },
        {
            "id": "TV3-COR-08",
            "name": "Tạo Correspondent vượt biên L+1 (129 ký tự)",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": "E" * 129},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-COR-10",
            "name": "Tạo Correspondent tên tiếng Việt Unicode",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": f"TV3_Nguyễn_Khiêm_Thuận_🌿_{run_stamp}"},
            "expected_status": 201,
            "resource": "corr",
        },
        {
            "id": "TV3-COR-17",
            "name": "Truy cập Correspondents không có token",
            "method": "GET",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": {"Content-Type": "application/json"},
            "json": None,
            "expected_status": 401,
            "resource": None,
        },
        {
            "id": "TV3-COR-18",
            "name": "Truy cập Correspondents với token giả",
            "method": "GET",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": {"Authorization": "Token invalid-fake-token-tv3", "Content-Type": "application/json"},
            "json": None,
            "expected_status": 401,
            "resource": None,
        },
        {
            "id": "TV3-COR-19",
            "name": "Phân trang Correspondents page=1&page_size=1",
            "method": "GET",
            "url": f"{BASE_URL}/api/correspondents/?page=1&page_size=1",
            "headers": auth_headers,
            "json": None,
            "expected_status": 200,
            "resource": None,
        },
        {
            "id": "TV3-COR-20",
            "name": "Regression BUG-01 (set_permissions.view=False)",
            "method": "POST",
            "url": f"{BASE_URL}/api/correspondents/",
            "headers": auth_headers,
            "json": {"name": f"TV3_Crash_Perm_Corr_{run_stamp}", "set_permissions": {"view": False}},
            "expected_status": 400,  # Kỳ vọng theo contract validation, nếu 500 là tái hiện BUG-01
            "resource": None,
        },
        # Document Types
        {
            "id": "TV3-DT-01",
            "name": "Tạo DocumentType hợp lệ",
            "method": "POST",
            "url": f"{BASE_URL}/api/document_types/",
            "headers": auth_headers,
            "json": {"name": f"TV3_DocType_Valid_{run_stamp}"},
            "expected_status": 201,
            "resource": "dt",
        },
        {
            "id": "TV3-DT-02",
            "name": "Tạo DocumentType thiếu trường 'name'",
            "method": "POST",
            "url": f"{BASE_URL}/api/document_types/",
            "headers": auth_headers,
            "json": {},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-DT-03",
            "name": "Tạo DocumentType với 'name' rỗng",
            "method": "POST",
            "url": f"{BASE_URL}/api/document_types/",
            "headers": auth_headers,
            "json": {"name": ""},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-DT-08",
            "name": "Tạo DocumentType vượt biên L+1 (129 ký tự)",
            "method": "POST",
            "url": f"{BASE_URL}/api/document_types/",
            "headers": auth_headers,
            "json": {"name": "F" * 129},
            "expected_status": 400,
            "resource": None,
        },
        {
            "id": "TV3-DT-20",
            "name": "Regression BUG-01 trên DocumentType",
            "method": "POST",
            "url": f"{BASE_URL}/api/document_types/",
            "headers": auth_headers,
            "json": {"name": f"TV3_Crash_Perm_DT_{run_stamp}", "set_permissions": {"view": False}},
            "expected_status": 400,
            "resource": None,
        },
    ]

    results = []
    print(f"{'Mã TC':<12} | {'Method':<6} | {'Kỳ vọng':<7} | {'Thực tế':<7} | {'Thời gian':<9} | {'Kết quả':<13} | {'Mô tả'}")
    print("-" * 105)

    for tc in test_cases:
        start_t = time.time()
        try:
            if tc["method"] == "GET":
                res = requests.get(tc["url"], headers=tc["headers"], timeout=5)
            elif tc["method"] == "POST":
                res = requests.post(tc["url"], headers=tc["headers"], json=tc["json"], timeout=5)
            else:
                continue
            elapsed_ms = int((time.time() - start_t) * 1000)
            actual_status = res.status_code

            # Ghi nhận ID nếu tạo thành công để dọn dẹp
            if tc["method"] == "POST" and actual_status == 201:
                item_id = res.json().get("id")
                if tc["resource"] == "corr" and item_id:
                    created_corr_ids.append(item_id)
                elif tc["resource"] == "dt" and item_id:
                    created_dt_ids.append(item_id)

            # Phân loại kết quả
            if actual_status == tc["expected_status"]:
                verdict = "PASS"
            elif tc["id"] in ("TV3-COR-20", "TV3-DT-20") and actual_status == 500:
                verdict = "REPRO-BUG-01"
            else:
                verdict = f"FAIL ({actual_status})"

            tc_result = {
                "id": tc["id"],
                "name": tc["name"],
                "method": tc["method"],
                "expected": tc["expected_status"],
                "actual": actual_status,
                "elapsed_ms": elapsed_ms,
                "verdict": verdict,
                "body_preview": res.text[:100].replace("\n", " "),
            }
            results.append(tc_result)
            print(f"{tc['id']:<12} | {tc['method']:<6} | {tc['expected_status']:<7} | {actual_status:<7} | {elapsed_ms:>5} ms   | {verdict:<13} | {tc['name']}")

        except Exception as e:
            tc_result = {
                "id": tc["id"],
                "name": tc["name"],
                "method": tc["method"],
                "expected": tc["expected_status"],
                "actual": "ERROR",
                "elapsed_ms": 0,
                "verdict": "ERROR",
                "body_preview": str(e)[:100],
            }
            results.append(tc_result)
            print(f"{tc['id']:<12} | {tc['method']:<6} | {tc['expected_status']:<7} | ERROR   |     0 ms   | ERROR         | {tc['name']}")

    # Kiểm tra tái hiện lần 2 cho BUG-01 (Yêu cầu tái hiện tối thiểu 2 lần)
    print("\n--- TÁI HIỆN BUG-01 LẦN 2 (XÁC MINH ĐỘC LẬP) ---")
    repro2_res = requests.post(
        f"{BASE_URL}/api/correspondents/",
        headers=auth_headers,
        json={"name": f"TV3_Crash_Perm_Repro2_{run_stamp}", "set_permissions": {"view": False}},
        timeout=5,
    )
    print(f"BUG-01 Repro 2: HTTP {repro2_res.status_code} (Xác nhận 500 Server Error: {repro2_res.status_code == 500})")

    # Kiểm tra hồi quy BUG-03: Kiểm tra response 201 của POST /api/correspondents/
    print("\n--- KIỂM TRA HỒI QUY BUG-03 (SCHEMA CONTRACT VIOLATION TRÊN 201 CREATED) ---")
    test_corr_res = requests.post(
        f"{BASE_URL}/api/correspondents/",
        headers=auth_headers,
        json={"name": f"TV3_Corr_Contract_Check_{run_stamp}"},
        timeout=5,
    )
    if test_corr_res.status_code == 201:
        corr_json = test_corr_res.json()
        item_id = corr_json.get("id")
        if item_id:
            created_corr_ids.append(item_id)
        # Theo OpenAPI schema /api/schema/, Correspondent required:
        # ['document_count', 'id', 'last_correspondence', 'name', 'permissions', 'slug', 'user_can_change']
        missing_fields = [f for f in ["document_count", "last_correspondence", "permissions"] if f not in corr_json]
        print(f"BUG-03 Check 1: HTTP 201 Created. Các trường bắt buộc theo schema bị THIẾU: {missing_fields}")
        print(f"  -> Kết quả hồi quy BUG-03: {'TÁI HIỆN THÀNH CÔNG (Thiếu trường)' if missing_fields else 'ĐÃ SỬA'}")
        
        # Tái hiện lần 2
        test_corr_res2 = requests.post(
            f"{BASE_URL}/api/correspondents/",
            headers=auth_headers,
            json={"name": f"TV3_Corr_Contract_Check2_{run_stamp}"},
            timeout=5,
        )
        if test_corr_res2.status_code == 201:
            item_id2 = test_corr_res2.json().get("id")
            if item_id2:
                created_corr_ids.append(item_id2)
            missing2 = [f for f in ["document_count", "last_correspondence", "permissions"] if f not in test_corr_res2.json()]
            print(f"BUG-03 Repro 2: HTTP 201 Created. Thiếu các trường: {missing2}")

    # Dọn dẹp chỉ các bản ghi test do lượt chạy này tạo
    print("\n--- DỌN DẸP BẢN GHI TEST DO LƯỢT CHẠY TẠO ---")
    for cid in created_corr_ids:
        requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=auth_headers, timeout=5)
    print(f"[OK] Đã xóa {len(created_corr_ids)} Correspondents tạo tạm.")

    for dtid in created_dt_ids:
        requests.delete(f"{BASE_URL}/api/document_types/{dtid}/", headers=auth_headers, timeout=5)
    print(f"[OK] Đã xóa {len(created_dt_ids)} DocumentTypes tạo tạm.")

    print("\n" + "=" * 105)
    print(f"HOÀN THÀNH {len(results)} TEST CASES THIẾT KẾ TAY")
    print("=" * 105 + "\n")

    return results


if __name__ == "__main__":
    run_manual_suite()
