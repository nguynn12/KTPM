#!/usr/bin/env python3
"""
scripts/run_manual_tests.py
Script thực thi bộ Test Case thiết kế thủ công cho tài nguyên Tag (/api/tags/)
Phục vụ báo cáo tiến độ môn Kiểm thử phần mềm - TV2 (Tạ Nhật Nguyên)
"""

import os
import sys
import time
import json
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI Colors for Terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")
AUTH_TOKEN = os.getenv("PAPERLESS_TOKEN", "3716828bfd21075a2fb68f1b959d02d2756f8d7a")

AUTH_HEADERS = {
    "Authorization": f"Token {AUTH_TOKEN}",
    "Content-Type": "application/json",
}

def print_header():
    print(f"\n{BOLD}{CYAN}========================================================================================{RESET}")
    print(f"{BOLD}{CYAN}      BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM: BỘ KIỂM THỬ THỦ CÔNG (MANUAL TEST CASES)           {RESET}")
    print(f"{BOLD}      Hệ thống: Paperless-ngx | Tài nguyên: Tag (/api/tags/) | TV2: Tạ Nhật Nguyên      {RESET}")
    print(f"{BOLD}{CYAN}========================================================================================{RESET}\n")

def run_tests():
    print_header()

    # Danh sách 8 test cases đại diện cho báo cáo tiến độ
    # (11 ca còn lại nằm trong kế hoạch cho báo cáo chính thức)
    test_cases = [
        {
            "id": "TC-TAG-01",
            "name": "Tạo Tag hợp lệ với trường tối thiểu",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "TV2_Progress_Tag_01"},
            "expected_status": 201,
            "category": "Phân vùng tương đương (Hợp lệ)",
        },
        {
            "id": "TC-TAG-03",
            "name": "Tạo Tag thiếu trường bắt buộc 'name'",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"color": "#112233"},
            "expected_status": 400,
            "category": "Phân vùng tương đương (Thiếu dữ liệu)",
        },
        {
            "id": "TC-TAG-04",
            "name": "Tạo Tag với 'name' là chuỗi rỗng",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": ""},
            "expected_status": 400,
            "category": "Phân tích giá trị biên (Chuỗi rỗng)",
        },
        {
            "id": "TC-TAG-07",
            "name": "Tạo Tag trùng tên đã tồn tại (Unique constraint)",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "TV2_Tag_Invoice_202"},
            "expected_status": 400,
            "category": "Ràng buộc toàn vẹn cơ sở dữ liệu",
        },
        {
            "id": "TC-TAG-11",
            "name": "Tạo Tag với set_permissions sai kiểu (BUG-01)",
            "method": "POST",
            "endpoint": "/api/tags/",
            "use_auth": True,
            "payload": {"name": "TV2_Crash_Perm_Tag", "set_permissions": {"view": False}},
            "expected_status": 400,  # Mong đợi 400, nhưng thực tế 500 do bug
            "category": "Error Guessing (Tái hiện lỗi mã nguồn)",
        },
        {
            "id": "TC-TAG-12",
            "name": "Lấy danh sách Tag có phân trang",
            "method": "GET",
            "endpoint": "/api/tags/?page=1&page_size=10",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
            "category": "Kiểm thử truy vấn danh sách (Query)",
        },
        {
            "id": "TC-TAG-14",
            "name": "Lấy chi tiết một Tag hợp lệ",
            "method": "GET",
            "endpoint": "/api/tags/{id}/",
            "use_auth": True,
            "payload": None,
            "expected_status": 200,
            "category": "Kiểm thử truy vấn chi tiết (Retrieve)",
        },
        {
            "id": "TC-TAG-19",
            "name": "Truy cập không có token xác thực",
            "method": "GET",
            "endpoint": "/api/tags/",
            "use_auth": False,
            "payload": None,
            "expected_status": 401,
            "category": "Bảo mật & Phân quyền (Authentication)",
        },
    ]

    # Tìm 1 ID tag hợp lệ có sẵn trong hệ thống cho TC-TAG-14
    sample_tag_id = 95
    try:
        r = requests.get(f"{BASE_URL}/api/tags/", headers=AUTH_HEADERS, timeout=5)
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                sample_tag_id = results[0]["id"]
    except Exception:
        pass

    results_table = []
    created_tag_ids = []

    print(f"{'Mã TC':<11} | {'Phương thức':<11} | {'Kỳ vọng':<7} | {'Thực tế':<7} | {'Thời gian':<9} | {'Đánh giá':<10} | {'Mô tả kiểm thử'}")
    print("-" * 105)

    pass_count = 0
    bug_count = 0
    fail_count = 0

    for tc in test_cases:
        url = f"{BASE_URL}{tc['endpoint']}".replace("{id}", str(sample_tag_id))
        headers = AUTH_HEADERS if tc["use_auth"] else {"Content-Type": "application/json"}
        start_time = time.time()

        try:
            if tc["method"] == "GET":
                resp = requests.get(url, headers=headers, timeout=5)
            elif tc["method"] == "POST":
                resp = requests.post(url, headers=headers, json=tc["payload"], timeout=5)
            elif tc["method"] == "PUT":
                resp = requests.put(url, headers=headers, json=tc["payload"], timeout=5)
            elif tc["method"] == "PATCH":
                resp = requests.patch(url, headers=headers, json=tc["payload"], timeout=5)
            elif tc["method"] == "DELETE":
                resp = requests.delete(url, headers=headers, timeout=5)
            else:
                continue

            elapsed_ms = int((time.time() - start_time) * 1000)
            actual_status = resp.status_code

            # Nếu tạo thành công thì lưu id để cleanup
            if tc["method"] == "POST" and actual_status == 201:
                try:
                    created_tag_ids.append(resp.json().get("id"))
                except Exception:
                    pass

            # Đánh giá kết quả
            if actual_status == tc["expected_status"]:
                verdict = f"{GREEN}PASS{RESET}"
                verdict_clean = "PASS"
                pass_count += 1
            elif tc["id"] == "TC-TAG-11" and actual_status == 500:
                verdict = f"{RED}BUG (500){RESET}"
                verdict_clean = "BUG (500)"
                bug_count += 1
            else:
                verdict = f"{RED}FAIL{RESET}"
                verdict_clean = "FAIL"
                fail_count += 1

            status_display = f"{actual_status}"
            if actual_status == 500:
                status_display = f"{RED}{actual_status}{RESET}"
            elif actual_status == tc["expected_status"]:
                status_display = f"{GREEN}{actual_status}{RESET}"

            print(f"{BOLD}{tc['id']:<11}{RESET} | {tc['method']:<11} | {tc['expected_status']:<7} | {status_display:<16} | {elapsed_ms:>5} ms  | {verdict:<19} | {tc['name']}")

            results_table.append({
                "id": tc["id"],
                "method": tc["method"],
                "expected": tc["expected_status"],
                "actual": actual_status,
                "verdict": verdict_clean,
                "name": tc["name"],
                "time_ms": elapsed_ms,
            })

        except Exception as e:
            print(f"{BOLD}{tc['id']:<11}{RESET} | {tc['method']:<11} | {tc['expected_status']:<7} | ERR     | 0 ms      | {RED}ERROR{RESET}     | {str(e)[:30]}")
            fail_count += 1

    # Dọn dẹp các tag tạo ra trong khi test
    for tid in created_tag_ids:
        if tid:
            try:
                requests.delete(f"{BASE_URL}/api/tags/{tid}/", headers=AUTH_HEADERS, timeout=5)
            except Exception:
                pass

    print("-" * 105)
    print(f"\n{BOLD}TỔNG KẾT BÁO CÁO TIẾN ĐỘ:{RESET}")
    print(f"  - Tổng số test case thực thi đợt này: {BOLD}{len(test_cases)} / 19{RESET} (11 ca còn lại kế hoạch cho báo cáo chính thức)")
    print(f"  - Số ca {GREEN}PASS{RESET} (Đúng chuẩn nghiệp vụ & bảo mật): {BOLD}{GREEN}{pass_count}{RESET}")
    print(f"  - Số ca {RED}BUG{RESET} (Phát hiện lỗi sập nguồn HTTP 500 - BUG-01): {BOLD}{RED}{bug_count}{RESET}")
    print(f"  - Tỷ lệ thực thi thành công kế hoạch tiến độ: {BOLD}{((pass_count + bug_count) / len(test_cases)) * 100:.1f}%{RESET}\n")

if __name__ == "__main__":
    run_tests()
