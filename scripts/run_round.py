#!/usr/bin/env python3
"""
scripts/run_round.py
Script chạy kiểm thử Schemathesis chuẩn hóa theo 3 vòng cho thành viên TV4 (Nguyễn Nhất Minh, Seed 404)
Đảm bảo số operations chuẩn hóa:
- Vòng 1: 19 operations (GET trên tags, correspondents, document_types, documents)
- Vòng 2: 18 operations (CRUD trên tags, correspondents, document_types)
- Vòng 3: 53 operations (Toàn bộ 4 nhóm tài nguyên, checks all)
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

DEFAULT_TOKEN = "3716828bfd21075a2fb68f1b959d02d2756f8d7a"


def get_auth_token(base_url, username="admin", password="admin"):
    url = f"{base_url}/api/token/"
    payload = {"username": username, "password": password}
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            token = res.json().get("token")
            return token
    except Exception:
        pass
    return os.getenv("PAPERLESS_TOKEN", DEFAULT_TOKEN)


def sanitize_text(text, sensitive_values):
    cleaned = text
    for val in sensitive_values:
        if val and len(val) >= 4:
            cleaned = cleaned.replace(val, "[REDACTED_SECRET]")
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
        ts = root.find("testsuite")
        if ts is not None:
            info["tests"] = int(ts.attrib.get("tests", 0))
            info["failures"] = int(ts.attrib.get("failures", 0))
            info["errors"] = int(ts.attrib.get("errors", 0))
            info["skipped"] = int(ts.attrib.get("skipped", 0))
            info["time"] = float(ts.attrib.get("time", 0.0))
        elif root.tag == "testsuite":
            info["tests"] = int(root.attrib.get("tests", 0))
            info["failures"] = int(root.attrib.get("failures", 0))
            info["errors"] = int(root.attrib.get("errors", 0))
            info["skipped"] = int(root.attrib.get("skipped", 0))
            info["time"] = float(root.attrib.get("time", 0.0))
    except Exception:
        pass
    return info


def run():
    parser = argparse.ArgumentParser(description="Chạy kiểm thử Schemathesis chuẩn hóa theo vòng")
    parser.add_argument("--round", type=int, required=True, choices=[1, 2, 3], help="Vòng kiểm thử (1, 2 hoặc 3)")
    parser.add_argument("--seed", type=int, default=404, help="Seed ngẫu nhiên (mặc định 404 cho TV4)")
    parser.add_argument("--max-examples", type=int, default=25, help="Số lượng examples tối đa cho mỗi endpoint")
    parser.add_argument("--workers", type=int, default=1, help="Số luồng workers")
    parser.add_argument("--url", default="http://localhost:8000", help="URL Paperless-ngx")
    parser.add_argument("--schema", default="http://localhost:8000/api/schema/", help="URL OpenAPI schema")
    parser.add_argument("--prefix", default="TV4", help="Tiền tố tên file kết quả")
    args = parser.parse_args()

    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    token = get_auth_token(args.url)
    prefix_name = f"{args.prefix}_round{args.round}_seed{args.seed}"
    log_path = results_dir / f"{prefix_name}.log"
    junit_path = results_dir / f"{prefix_name}_junit.xml"
    ndjson_path = results_dir / f"{prefix_name}.ndjson"

    # Kiểm tra schemathesis local hoặc Docker
    schemathesis_bin = sys.executable.replace("python.exe", "schemathesis.exe")
    use_docker = not (os.path.exists(schemathesis_bin) or subprocess.run(["where", "schemathesis"], capture_output=True).returncode == 0)

    if use_docker:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd().resolve() / 'results'}:/results",
            "--network", "ktpm_default",
            "schemathesis/schemathesis:latest",
            "run",
            "http://webserver:8000/api/schema/",
            "--url", "http://webserver:8000",
            "--seed", str(args.seed),
            "--max-examples", str(args.max_examples),
            "--workers", str(args.workers),
            "--mode", "all",
            "-H", f"Authorization: Token {token}",
            "--report", "junit,ndjson",
            "--report-junit-path", f"/results/{junit_path.name}",
            "--report-ndjson-path", f"/results/{ndjson_path.name}",
            "--output-sanitize", "true",
            "--no-color",
        ]
    else:
        bin_path = schemathesis_bin if os.path.exists(schemathesis_bin) else "schemathesis"
        cmd = [
            bin_path,
            "run",
            args.schema,
            "--url", args.url,
            "--seed", str(args.seed),
            "--max-examples", str(args.max_examples),
            "--workers", str(args.workers),
            "--mode", "all",
            "--header", f"Authorization: Token {token}",
            "--report", "junit,ndjson",
            "--report-junit-path", str(junit_path),
            "--report-ndjson-path", str(ndjson_path),
            "--output-sanitize", "true",
            "--no-color",
        ]

    if args.round == 1:
        cmd.extend([
            "--include-path-regex", "^/api/(tags|correspondents|document_types|documents)/",
            "--exclude-method", "POST",
            "--exclude-method", "PUT",
            "--exclude-method", "PATCH",
            "--exclude-method", "DELETE",
            "--phases", "examples,fuzzing",
            "--checks", "not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance",
        ])
    elif args.round == 2:
        cmd.extend([
            "--include-path-regex", "^/api/(tags|correspondents|document_types)/",
            "--checks", "all",
        ])
    elif args.round == 3:
        cmd.extend([
            "--include-path-regex", "^/api/(tags|correspondents|document_types|documents)/",
            "--checks", "all",
        ])

    print(f"=== BẮT ĐẦU CHẠY VÒNG {args.round} (SEED {args.seed}) ===")
    start_time = time.time()
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    elapsed = time.time() - start_time

    sanitized = sanitize_text(proc.stdout, [token])
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(sanitized)

    junit_stats = parse_junit(junit_path)
    print(f"=== KẾT THÚC VÒNG {args.round} ===")
    print(f"Exit Code: {proc.returncode}")
    print(f"Thời gian: {elapsed:.2f}s")
    print(f"JUnit Tests: {junit_stats['tests']}, Failures: {junit_stats['failures']}")
    print(f"Đã lưu: {log_path}, {junit_path}, {ndjson_path}")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(run())
