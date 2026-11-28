#!/usr/bin/env python3
"""
scripts/run_round_TV3.py
Runner thực thi từng vòng Schemathesis cho TV3 (Nguyễn Khiêm Thuận - MSSV 2312764 - Seed 303).
Hỗ trợ --round 1 | 2 | 3.
Bảo mật: Không in token, tự động che phủ (sanitize) thông tin xác thực trong log và báo cáo.
"""

import os
import sys
import time
import argparse
import subprocess
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_auth_token(base_url, username, password):
    url = f"{base_url}/api/token/"
    payload = {"username": username, "password": password}
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            token = res.json().get("token")
            return token
        else:
            print(f"[LỖI] Không thể lấy token xác thực: HTTP {res.status_code} - {res.text}")
            sys.exit(2)
    except Exception as e:
        print(f"[LỖI] Kết nối tới API thất bại: {e}")
        sys.exit(2)


def sanitize_text(text, sensitive_values):
    cleaned = text
    for val in sensitive_values:
        if val and len(val) >= 4:
            cleaned = cleaned.replace(val, "[REDACTED_SECRET]")
    # Che thêm các chuỗi Token dạng hex 40 ký tự
    cleaned = re.sub(r"Token\s+[a-fA-F0-9]{32,}", "Token [REDACTED_TOKEN]", cleaned)
    cleaned = re.sub(r"Authorization:\s*Token\s+[^\r\n]+", "Authorization: Token [REDACTED_TOKEN]", cleaned)
    return cleaned


def parse_ndjson(ndjson_path):
    stats = {
        "operations_selected": None,
        "running_time": None,
        "events_count": 0,
        "failures": [],
        "errors": [],
    }
    if not os.path.exists(ndjson_path):
        return stats

    with open(ndjson_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            stats["events_count"] += 1
            try:
                ev = json.loads(line)
                ev_type = ev.get("type")
                if ev_type == "LoadingFinished":
                    stat = ev.get("statistic", {})
                    stats["operations_selected"] = stat.get("operations", {}).get("selected")
                elif ev_type == "EngineFinished":
                    stats["running_time"] = ev.get("running_time")
                elif ev_type == "AfterExecution":
                    status = ev.get("status")
                    if status == "failure":
                        stats["failures"].append(ev)
                    elif status == "error":
                        stats["errors"].append(ev)
            except Exception:
                pass
    return stats


def parse_junit(junit_path):
    info = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    if not os.path.exists(junit_path):
        return info
    try:
        tree = ET.parse(junit_path)
        root = tree.getroot()
        if root.tag == "testsuites":
            for ts in root.findall("testsuite"):
                info["tests"] += int(ts.attrib.get("tests", 0))
                info["failures"] += int(ts.attrib.get("failures", 0))
                info["errors"] += int(ts.attrib.get("errors", 0))
                info["skipped"] += int(ts.attrib.get("skipped", 0))
                info["time"] += float(ts.attrib.get("time", 0.0))
        elif root.tag == "testsuite":
            info["tests"] = int(root.attrib.get("tests", 0))
            info["failures"] = int(root.attrib.get("failures", 0))
            info["errors"] = int(root.attrib.get("errors", 0))
            info["skipped"] = int(root.attrib.get("skipped", 0))
            info["time"] = float(root.attrib.get("time", 0.0))
    except Exception as e:
        info["parse_error"] = str(e)
    return info


def parse_cli_summary(log_text):
    summary = {}
    m_passed = re.search(r"(\d+)\s+passed", log_text)
    m_failed = re.search(r"(\d+)\s+failed", log_text)
    m_errored = re.search(r"(\d+)\s+errored", log_text)
    if m_passed:
        summary["passed"] = int(m_passed.group(1))
    if m_failed:
        summary["failed"] = int(m_failed.group(1))
    if m_errored:
        summary["errored"] = int(m_errored.group(1))

    m_time = re.search(r"in\s+([\d\.]+)s", log_text)
    if m_time:
        summary["time_seconds"] = float(m_time.group(1))

    m_ops = re.search(r"(\d+)\s+selected", log_text)
    if m_ops:
        summary["operations_selected"] = int(m_ops.group(1))
    return summary


def run():
    parser = argparse.ArgumentParser(description="Runner Schemathesis TV3 - Seed 303")
    parser.add_argument("--round", type=int, required=True, choices=[1, 2, 3], help="Vòng kiểm thử (1, 2 hoặc 3)")
    parser.add_argument("--url", default=os.getenv("PAPERLESS_URL", "http://localhost:8000"), help="Base URL API")
    parser.add_argument("--schema", default="http://localhost:8000/api/schema/", help="OpenAPI schema endpoint/file")
    parser.add_argument("--seed", type=int, default=303, help="Seed ngẫu nhiên Schemathesis (mặc định: 303)")
    parser.add_argument("--max-examples", type=int, default=25, help="Giới hạn ví dụ sinh tối đa (mặc định: 25)")
    parser.add_argument("--workers", type=int, default=1, help="Số worker song song (mặc định: 1)")
    args = parser.parse_args()

    # Kiểm tra URL chỉ localhost
    if "localhost" not in args.url and "127.0.0.1" not in args.url:
        print("[LỖI] Quy tắc nghiêm ngặt: Chỉ kiểm thử API trên localhost (127.0.0.1)!")
        sys.exit(1)

    admin_user = os.getenv("PAPERLESS_ADMIN_USER", "admin")
    admin_pass = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")

    print(f"\n======================================================================")
    print(f"=== KHỞI CHẠY SCHEMATHESIS TV3 - VÒNG {args.round} (SEED {args.seed}) ===")
    print(f"=== Tác giả: Nguyễn Khiêm Thuận - MSSV: 2312764 - TV3             ===")
    print(f"======================================================================\n")

    token = get_auth_token(args.url, admin_user, admin_pass)
    print("[OK] Xác thực thành công. Bắt đầu chuẩn bị tham số chạy...")

    # Xác định đường dẫn file kết quả
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    prefix = f"TV3_round{args.round}_seed{args.seed}_{timestamp}"

    log_path = results_dir / f"{prefix}.log"
    junit_path = results_dir / f"{prefix}.xml"
    ndjson_path = results_dir / f"{prefix}.ndjson"
    summary_md_path = results_dir / f"{prefix}_summary.md"

    # Xây dựng tham số theo từng vòng
    schemathesis_bin = sys.executable.replace("python.exe", "schemathesis.exe")
    if not os.path.exists(schemathesis_bin):
        schemathesis_bin = "schemathesis"

    cmd = [
        schemathesis_bin,
        "run",
        args.schema,
        "--url",
        args.url,
        "--seed",
        str(args.seed),
        "--max-examples",
        str(args.max_examples),
        "--workers",
        str(args.workers),
        "--mode",
        "all",
        "--header",
        f"Authorization: Token {token}",
        "--report",
        "junit,ndjson",
        "--report-junit-path",
        str(junit_path),
        "--report-ndjson-path",
        str(ndjson_path),
        "--output-sanitize",
        "true",
        "--no-color",
    ]

    phases_used = ""
    checks_used = ""
    scope_used = ""

    if args.round == 1:
        scope_used = r"^/api/(tags|correspondents|document_types|documents)/"
        phases_used = "examples,fuzzing"
        checks_used = "not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance"
        cmd.extend([
            "--include-path-regex",
            scope_used,
            "--exclude-method",
            "POST",
            "--exclude-method",
            "PUT",
            "--exclude-method",
            "PATCH",
            "--exclude-method",
            "DELETE",
            "--phases",
            phases_used,
            "--checks",
            checks_used,
        ])
    elif args.round == 2:
        scope_used = r"^/api/(tags|correspondents|document_types)/"
        phases_used = "examples,coverage,fuzzing,stateful (mặc định Schemathesis 4.30.1)"
        checks_used = "all"
        cmd.extend([
            "--include-path-regex",
            scope_used,
            "--checks",
            "all",
        ])
    elif args.round == 3:
        scope_used = r"^/api/(tags|correspondents|document_types|documents)/"
        phases_used = "examples,coverage,fuzzing,stateful (mặc định Schemathesis 4.30.1)"
        checks_used = "all"
        cmd.extend([
            "--include-path-regex",
            scope_used,
            "--checks",
            "all",
        ])

    # In lệnh (đã che token)
    display_cmd = []
    for arg in cmd:
        if arg.startswith("Authorization: Token"):
            display_cmd.append("Authorization: Token [REDACTED_AUTH_TOKEN]")
        else:
            display_cmd.append(arg)
    print(f"Lệnh thực thi: {' '.join(display_cmd)}\n")

    start_time = time.time()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=env)
    elapsed_total = time.time() - start_time
    exit_code = proc.returncode

    # Sanitize log output
    sanitized_output = sanitize_text(proc.stdout, [token, admin_pass])
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(sanitized_output)

    # Sanitize ndjson nếu có chứa token
    if ndjson_path.exists():
        nd_text = ndjson_path.read_text(encoding="utf-8", errors="replace")
        nd_sanitized = sanitize_text(nd_text, [token, admin_pass])
        ndjson_path.write_text(nd_sanitized, encoding="utf-8")

    # Sanitize junit nếu có chứa token
    if junit_path.exists():
        junit_text = junit_path.read_text(encoding="utf-8", errors="replace")
        junit_sanitized = sanitize_text(junit_text, [token, admin_pass])
        junit_path.write_text(junit_sanitized, encoding="utf-8")

    # Thu thập số liệu thực tế
    ndjson_stats = parse_ndjson(str(ndjson_path))
    junit_stats = parse_junit(str(junit_path))
    cli_summary = parse_cli_summary(sanitized_output)

    ops_selected = ndjson_stats["operations_selected"] or cli_summary.get("operations_selected", "không có trong output")
    running_time = ndjson_stats["running_time"] or cli_summary.get("time_seconds", round(elapsed_total, 2))

    print(f"=== KẾT THÚC CHẠY VÒNG {args.round} ===")
    print(f"CLI Exit Code: {exit_code} (0: Tất cả đạt, 1: Có failure/error hợp đồng hoặc server, >1: Lỗi cấu hình)")
    print(f"Thời gian chạy thực tế: {running_time}s (tổng: {elapsed_total:.2f}s)")
    print(f"Operations được chọn: {ops_selected}")
    print(f"JUnit Summary: tests={junit_stats.get('tests')}, failures={junit_stats.get('failures')}, errors={junit_stats.get('errors')}")
    print(f"Đã lưu tệp nhật ký: {log_path}")
    print(f"Đã lưu JUnit XML: {junit_path}")
    print(f"Đã lưu NDJSON: {ndjson_path}")

    # Ghi file summary markdown
    summary_md = f"""# TÓM TẮT KẾT QUẢ KIỂM THỬ THỰC TẾ — TV3 VÒNG {args.round}

- **Tác giả:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: {args.seed}
- **Thời gian thực hiện:** {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Vòng kiểm thử:** Vòng {args.round}
- **CLI Exit Code:** `{exit_code}`
- **Công cụ:** Schemathesis 4.30.1 | Python 3.14.4 | Hypothesis 6.169.0
- **Phạm vi Regex:** `{scope_used}`
- **Phases:** `{phases_used}`
- **Checks:** `{checks_used}`
- **Cấu hình sinh:** `--max-examples {args.max_examples}`, `--workers {args.workers}`, `--mode all`

---

## 1. Bảng số liệu đo lường thực tế

| Chỉ số | Giá trị ghi nhận từ công cụ | Nguồn trích xuất |
|---|---|---|
| Operations được chọn | {ops_selected} | NDJSON LoadingFinished / CLI |
| Tổng thời gian chạy | {running_time} giây | NDJSON EngineFinished / CLI |
| Số testcase trong JUnit report | {junit_stats.get('tests')} | JUnit XML `<testsuite tests="...">` |
| Số failures trong JUnit | {junit_stats.get('failures')} | JUnit XML `<testsuite failures="...">` |
| Số errors trong JUnit | {junit_stats.get('errors')} | JUnit XML `<testsuite errors="...">` |
| Passed reported (CLI) | {cli_summary.get('passed', 'không có trong output')} | CLI summary output |
| Failed reported (CLI) | {cli_summary.get('failed', 'không có trong output')} | CLI summary output |
| Errored reported (CLI) | {cli_summary.get('errored', 'không có trong output')} | CLI summary output |

> [!NOTE]
> - `max-examples` ({args.max_examples}) là tham số giới hạn sinh của thuật toán Hypothesis cho mỗi operation, không phải tổng số request thực tế.
> - Số phần tử `<testcase>` trong JUnit XML đại diện cho các operations/checks được ánh xạ, không đồng nhất với tổng số request HTTP đã gửi qua mạng.
> - Exit code `{exit_code}`: Nếu mã là 1, công cụ đã chạy hoàn tất và phát hiện vi phạm kiểm thử (failures/errors), không phải do môi trường bị hỏng.

---

## 2. Đường dẫn các tệp bằng chứng thực tế
- File Log chi tiết: [{log_path.name}](file:///{log_path.resolve().as_posix()})
- File JUnit XML: [{junit_path.name}](file:///{junit_path.resolve().as_posix()})
- File NDJSON: [{ndjson_path.name}](file:///{ndjson_path.resolve().as_posix()})

---

## 3. Quét bảo mật đầu ra
- Toàn bộ giá trị Authorization token và mật khẩu quản trị đã được làm sạch (`[REDACTED]`).
- Tùy chọn `--output-sanitize true` đã được bật trong quá trình chạy.
"""
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"Đã lưu tóm tắt kết quả: {summary_md_path}\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(run())
