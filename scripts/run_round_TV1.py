#!/usr/bin/env python3
"""
scripts/run_round_TV1.py — Runner chạy từng vòng Schemathesis cho TV1 (Trần Gia Huy, seed 101).

Ý tưởng chạy giống nhóm (docs/CLI_STANDARD_TV3.md), nhưng sửa lại cách lọc cho ĐÚNG cơ chế của
Schemathesis 4.30.1 (đã đo thực nghiệm, xem docs/ONBOARDING_TV1.md mục 10):
  - Nhiều cờ `--include-*` bị ghép OR (hợp), nên `--include-path-regex X --include-method GET`
    KHÔNG cho ra "chỉ GET trong X" mà là (X ∪ tất cả GET của toàn schema).
  - `--exclude-method` chỉ nhận MỘT giá trị mỗi lần, nên phải lặp cờ.
Vì vậy vòng 1 dùng:  --include-path-regex <4 resource>  +  --exclude-method (lặp 4 lần).

Phạm vi từng vòng (đếm từ chính /api/schema/ trả về, runner tự kiểm tra lại sau khi chạy):
  Vòng 1: chỉ GET trên tags|correspondents|document_types|documents      -> 19 operation
  Vòng 2: mọi method trên tags|correspondents|document_types             -> 18 operation
  Vòng 3: mọi method trên tags|correspondents|document_types|documents    -> 53 operation

Điều kiện trước khi chạy (quy trình nhóm: reset -> seed -> xác nhận baseline -> chạy vòng):
  1. docker compose up -d   (3 container Up, webserver healthy)
  2. scripts/prepare_baseline_TV1.py   (dựng lại đúng bộ seed 101 của TV1)

Cách chạy:
  .\\.venv\\Scripts\\python.exe scripts\\run_round_TV1.py --round 1
  hoặc:  powershell -ExecutionPolicy Bypass -File scripts\\run_round_TV1.ps1 -Round 1

Kết quả mỗi vòng ghi theo đúng quy ước tên file của nhóm (giống TV2/TV3), chạy lại sẽ ghi đè:
  results/TV1_round<N>_seed101.log, .xml (JUnit), .ndjson, _summary.md

Biến môi trường (tuỳ chọn): PAPERLESS_ADMIN_USER, PAPERLESS_ADMIN_PASSWORD, PAPERLESS_URL.
Quy tắc an toàn: chỉ chạy với localhost/127.0.0.1; token không bao giờ được in ra màn hình và
được thay bằng [REDACTED] trong mọi file kết quả (log, JUnit XML, NDJSON, summary).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SEED = 101
PAPERLESS_IMAGE = "ghcr.io/paperless-ngx/paperless-ngx:3.1.3"
PAPERLESS_SHA = "d48663e9ebaadc4b413a6ca3bc88cb5fbc4e468e"
MUTATING = ("POST", "PUT", "PATCH", "DELETE")

ROUNDS = {
    1: dict(
        scope=r"^/api/(tags|correspondents|document_types|documents)/",
        exclude_methods=list(MUTATING),
        phases="examples,fuzzing",
        checks="not_a_server_error,status_code_conformance,content_type_conformance,"
               "response_headers_conformance,response_schema_conformance",
        note="chỉ đọc (GET), trên 4 nhóm tài nguyên",
    ),
    2: dict(
        scope=r"^/api/(tags|correspondents|document_types)/",
        exclude_methods=[],
        phases=None,
        checks="all",
        note="mọi method, chỉ trên 3 nhóm metadata",
    ),
    3: dict(
        scope=r"^/api/(tags|correspondents|document_types|documents)/",
        exclude_methods=[],
        phases=None,
        checks="all",
        note="mọi method, trên cả 4 nhóm tài nguyên",
    ),
}


def schemathesis_bin() -> str:
    exe = "schemathesis.exe" if os.name == "nt" else "schemathesis"
    candidate = Path(sys.executable).with_name(exe)
    return str(candidate) if candidate.exists() else "schemathesis"


def fetch_token(base_url: str, user: str, password: str) -> str:
    payload = json.dumps({"username": user, "password": password}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/token/", data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))["token"]


def sanitize(text: str, secrets: list[str]) -> str:
    out = text
    for s in secrets:
        if s and len(s) >= 4:
            out = out.replace(s, "[REDACTED]")
    out = re.sub(r"(?i)(authorization:\s*token\s+)\S+", r"\1[REDACTED_TOKEN]", out)
    out = re.sub(r"Token\s+[0-9a-fA-F]{16,}", "Token [REDACTED_TOKEN]", out)
    return out


def sanitize_file(path: Path, secrets: list[str]) -> int:
    """Thay token trong file do Schemathesis tự ghi (XML/NDJSON) — trả về số lần thay."""
    if not path.exists():
        return 0
    raw = path.read_text(encoding="utf-8", errors="replace")
    clean = sanitize(raw, secrets)
    if clean != raw:
        path.write_text(clean, encoding="utf-8")
    hits = sum(raw.count(s) for s in secrets if s and len(s) >= 4)
    return hits


def tool_versions() -> dict:
    info = {"schemathesis": "không rõ", "python": sys.version.split()[0], "hypothesis": "không rõ"}
    try:
        r = subprocess.run([schemathesis_bin(), "--version"], capture_output=True, text=True, timeout=180)
        out = (r.stdout or r.stderr).strip()
        if out:
            info["schemathesis"] = out.splitlines()[0]
    except Exception:
        pass
    try:
        import hypothesis  # đi kèm schemathesis
        info["hypothesis"] = hypothesis.__version__
    except Exception:
        pass
    return info


def load_schema(schema_url: str) -> dict | None:
    try:
        with urllib.request.urlopen(schema_url, timeout=60) as r:
            text = r.read().decode("utf-8", errors="replace")
        try:
            return json.loads(text)
        except Exception:
            import yaml
            return yaml.safe_load(text)
    except Exception:
        return None


def count_expected_operations(schema: dict | None, scope: str, exclude_methods: list[str]) -> int | None:
    """Đếm số operation khớp phạm vi, đọc trực tiếp từ schema — không suy đoán."""
    if not isinstance(schema, dict) or "paths" not in schema:
        return None
    rx = re.compile(scope)
    skipped = {m.upper() for m in exclude_methods}
    n = 0
    for path, item in schema["paths"].items():
        if not rx.search(path):
            continue
        for method in item:
            if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options", "trace"):
                if method.upper() not in skipped:
                    n += 1
    return n


def parse_junit(path: Path) -> dict:
    info = {"tests": None, "failures": None, "errors": None, "skipped": None, "time": None}
    if not path.exists():
        return info
    try:
        root = ET.parse(path).getroot()
        suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
        acc = {k: 0 for k in ("tests", "failures", "errors", "skipped")}
        t = 0.0
        for ts in suites:
            for k in acc:
                acc[k] += int(ts.attrib.get(k, 0) or 0)
            t += float(ts.attrib.get("time", 0) or 0)
        info.update(acc)
        info["time"] = round(t, 2)
    except Exception as e:
        info["parse_error"] = str(e)
    return info


def parse_ndjson(path: Path) -> dict:
    """Schemathesis 4.x ghi mỗi dòng 1 object 1 khoá: {"TenSuKien": {...}}."""
    stats = {
        "events": 0, "operations_total": None, "operations_selected": None,
        "running_time": None, "stop_reason": None,
        "scenario_started": 0, "scenario_finished": 0, "scenario_skip": 0, "scenario_fail": 0,
        "skip_reasons": {}, "initialize_command": None, "phases": [],
    }
    if not path.exists():
        return stats
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            stats["events"] += 1
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if not isinstance(ev, dict) or len(ev) != 1:
                continue
            name, data = next(iter(ev.items()))
            if not isinstance(data, dict):
                continue
            if name == "Initialize":
                stats["initialize_command"] = data.get("command")
            elif name == "LoadingFinished":
                ops = (data.get("statistic") or {}).get("operations") or {}
                stats["operations_total"] = ops.get("total")
                stats["operations_selected"] = ops.get("selected")
            elif name == "EngineFinished":
                if data.get("running_time") is not None:
                    stats["running_time"] = round(float(data["running_time"]), 2)
                stats["stop_reason"] = data.get("stop_reason")
            elif name == "PhaseStarted":
                ph = data.get("phase")
                if isinstance(ph, dict):
                    stats["phases"].append({"name": ph.get("name"),
                                            "enabled": ph.get("is_enabled"),
                                            "reason": ph.get("skip_reason")})
                else:
                    stats["phases"].append({"name": str(ph), "enabled": None, "reason": None})
            elif name == "ScenarioStarted":
                stats["scenario_started"] += 1
            elif name == "ScenarioFinished":
                stats["scenario_finished"] += 1
                status = data.get("status")
                if status == "skip":
                    stats["scenario_skip"] += 1
                    reason = data.get("skip_reason") or "không ghi lý do"
                    stats["skip_reasons"][reason] = stats["skip_reasons"].get(reason, 0) + 1
                elif status in ("failure", "error"):
                    stats["scenario_fail"] += 1
    return stats


def parse_cli(log_text: str) -> dict:
    """Đọc bảng tổng kết của CLI (số unique failure theo check, số testcase sinh ra)."""
    out = {"checks": [], "generated": None, "found": None, "unique": None,
           "total_failures": None, "warnings": None, "time": None}
    for m in re.finditer(r"[❌✗]\s*([A-Za-z][^:\n]{2,60}?):\s*(\d+)", log_text):
        name, count = m.group(1).strip(), int(m.group(2))
        if name.lower() in ("examples", "coverage", "fuzzing", "stateful"):
            continue
        out["checks"].append((name, count))
    m = re.search(r"(\d+)\s+generated,\s*(\d+)\s+found\s+(\d+)\s+unique failures", log_text)
    if m:
        out["generated"], out["found"], out["unique"] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = re.search(r"(\d+)\s+failures?,\s*(\d+)\s+warnings?\s+in\s+([\d.]+)s", log_text)
    if m:
        out["total_failures"], out["warnings"], out["time"] = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return out


def write_summary(path: Path, round_no: int, cfg: dict, args, cli_code: int, versions: dict,
                  junit: dict, ndjson: dict, cli: dict, artifacts: dict, expected: int | None,
                  leak_hits: int) -> None:
    def v(x, unknown="không có trong output"):
        return unknown if x is None else x

    match = "-"
    if expected is not None and ndjson["operations_selected"] is not None:
        match = "KHỚP" if expected == ndjson["operations_selected"] else "KHÔNG KHỚP"

    lines = [
        f"# TÓM TẮT KẾT QUẢ CHẠY THẬT — TV1 VÒNG {round_no} (seed {SEED})",
        "",
        f"- **Người chạy:** Trần Gia Huy (TV1) — Windows 11, Docker Desktop",
        f"- **Thời điểm chạy:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Hệ thống được test:** `{PAPERLESS_IMAGE}` (SHA `{PAPERLESS_SHA}`), chạy local tại `{args.url}`",
        f"- **Công cụ:** {versions['schemathesis']} | Python {versions['python']} | Hypothesis {versions['hypothesis']}",
        f"- **Ý nghĩa vòng {round_no}:** {cfg['note']}",
        f"- **Phạm vi (regex đường dẫn):** `{cfg['scope']}`",
        f"- **Method loại trừ:** {', '.join(cfg['exclude_methods']) if cfg['exclude_methods'] else 'không loại trừ'}",
        f"- **Phases:** {cfg['phases'] or 'mặc định của Schemathesis 4.30.1 (không truyền cờ --phases)'}",
        f"- **Checks:** {cfg['checks']}",
        f"- **Cấu hình sinh:** `--seed {SEED}`, `--max-examples {args.max_examples}`, `--workers {args.workers}`, `--mode all`",
        f"- **Exit code CLI:** `{cli_code}` (1 = có vi phạm được phát hiện)",
        "",
        "Lệnh đã chạy (token đã bị Schemathesis lọc thành `[Filtered]`):",
        "",
        "```bash",
        (ndjson["initialize_command"] or "(không đọc được từ NDJSON)"),
        "```",
        "",
        "## 1. Số liệu đọc từ chính file kết quả",
        "",
        "| Chỉ số | Giá trị | Nguồn |",
        "|---|---|---|",
        f"| Operation có trong schema | {v(ndjson['operations_total'])} | NDJSON `LoadingFinished` |",
        f"| **Operation theo phạm vi (mong đợi)** | **{v(expected)}** | đếm trực tiếp từ `/api/schema/` |",
        f"| **Operation được chọn (thực tế)** | **{v(ndjson['operations_selected'])}** | NDJSON `LoadingFinished` |",
        f"| Đối chiếu mong đợi/thực tế | {match} | so sánh 2 dòng trên |",
        f"| Tổng thời gian chạy (giây) | {v(ndjson['running_time'])} | NDJSON `EngineFinished` |",
        f"| Lý do dừng | {v(ndjson['stop_reason'])} | NDJSON `EngineFinished` |",
        f"| `<testcase>` trong JUnit | {v(junit['tests'])} | JUnit XML `tests=` |",
        f"| Failures trong JUnit | {v(junit['failures'])} | JUnit XML `failures=` |",
        f"| Errors trong JUnit | {v(junit['errors'])} | JUnit XML `errors=` |",
        f"| Skipped trong JUnit | {v(junit['skipped'])} | JUnit XML `skipped=` |",
        f"| Testcase sinh ra (CLI) | {v(cli['generated'])} | bảng tổng kết CLI |",
        f"| Testcase phát hiện lỗi (CLI) | {v(cli['found'])} | bảng tổng kết CLI |",
        f"| **Lỗi khác nhau (unique failures, CLI)** | **{v(cli['unique'])}** | bảng tổng kết CLI |",
        f"| Scenario đã chạy / bỏ qua / lỗi | {ndjson['scenario_started']} / {ndjson['scenario_skip']} / {ndjson['scenario_fail']} | NDJSON `Scenario*` |",
        "",
        "> Ghi nhớ khi đọc số: `--max-examples 25` là giới hạn sinh dữ liệu của Hypothesis cho mỗi",
        "> operation, **không phải** số request đã gửi; số `<testcase>` là số operation × check được ánh",
        "> xạ, không phải số request; **unique failures không phải số bug** — nhiều failure có thể chung",
        "> một nguyên nhân, và một nguyên nhân có thể sinh nhiều failure.",
        "",
    ]

    lines += ["## 2. Phân loại lỗi theo check (đọc từ bảng tổng kết CLI)", ""]
    if cli["checks"]:
        lines += ["| Check bị vi phạm | Số lỗi khác nhau |", "|---|---|"]
        lines += [f"| {name} | {count} |" for name, count in cli["checks"]]
        total = sum(c for _, c in cli["checks"])
        lines += [f"| **Tổng** | **{total}** |"]
    else:
        lines.append("_Không có lỗi nào được CLI thống kê._")
    lines.append("")

    if ndjson["skip_reasons"]:
        lines += ["## 3. Lý do bỏ qua scenario (NDJSON)", ""]
        lines += [f"- {reason}: {count}" for reason, count in
                  sorted(ndjson["skip_reasons"].items(), key=lambda x: -x[1])]
        lines.append("")

    lines += [
        "## 4. Phases đã chạy",
        "",
        f"- Thực chạy: {', '.join(p['name'] for p in ndjson['phases'] if p['enabled']) or 'không đọc được'}",
        f"- Không chạy: {', '.join(p['name'] + ' (' + (p['reason'] or 'không bật') + ')' for p in ndjson['phases'] if p['enabled'] is False) or 'không có'}",
        "",
        "## 5. File bằng chứng (đường dẫn tương đối trong repo)",
        "",
        f"- Log CLI đã làm sạch token: `{artifacts['log']}`",
        f"- JUnit XML: `{artifacts['junit']}`",
        f"- NDJSON (sự kiện thô): `{artifacts['ndjson']}`",
        "",
        f"> Token đã bị thay bằng `[REDACTED]` trong mọi file kết quả"
        f" (số vị trí đã thay ở XML/NDJSON: {leak_hits}).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Runner Schemathesis TV1 — seed 101")
    ap.add_argument("--round", type=int, required=True, choices=[1, 2, 3])
    ap.add_argument("--url", default=os.getenv("PAPERLESS_URL", "http://localhost:8000"))
    ap.add_argument("--schema", default=None, help="mặc định: <url>/api/schema/")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--max-examples", type=int, default=25)
    ap.add_argument("--workers", type=int, default=1)
    args = ap.parse_args()

    args.url = args.url.rstrip("/")
    if "localhost" not in args.url and "127.0.0.1" not in args.url:
        print("[LỖI] Chỉ được test trên localhost/127.0.0.1 — không gửi request ra Internet.")
        return 1
    if args.schema is None:
        args.schema = f"{args.url}/api/schema/"

    cfg = ROUNDS[args.round]
    user = os.getenv("PAPERLESS_ADMIN_USER", "admin")
    password = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")

    print(f"=== TV1 / Schemathesis — VÒNG {args.round} (seed {args.seed}) ===")
    print(f"    {cfg['note']}")
    try:
        token = fetch_token(args.url, user, password)
    except Exception as e:
        print(f"[LỖI] Không lấy được token tại {args.url}/api/token/ : {e}")
        print("       Kiểm tra: Docker Desktop đã bật chưa? container webserver đã healthy chưa?")
        return 2
    print("[OK] Xác thực thành công (token không in ra màn hình).")

    expected = count_expected_operations(load_schema(args.schema), cfg["scope"], cfg["exclude_methods"])
    print(f"    Số operation mong đợi (đếm từ schema): {expected}")

    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"TV1_round{args.round}_seed{args.seed}"
    artifacts = {
        "log": results_dir / f"{prefix}.log",
        "junit": results_dir / f"{prefix}.xml",
        "ndjson": results_dir / f"{prefix}.ndjson",
    }

    cmd = [
        schemathesis_bin(), "run", args.schema,
        "--url", args.url,
        "--include-path-regex", cfg["scope"],
        "--seed", str(args.seed),
        "--max-examples", str(args.max_examples),
        "--workers", str(args.workers),
        "--mode", "all",
        "--header", f"Authorization: Token {token}",
        "--report", "junit,ndjson",
        "--report-junit-path", str(artifacts["junit"]),
        "--report-ndjson-path", str(artifacts["ndjson"]),
        "--output-sanitize", "true",
        "--no-color",
    ]
    for method in cfg["exclude_methods"]:
        cmd += ["--exclude-method", method]
    if cfg["phases"]:
        cmd += ["--phases", cfg["phases"]]
    cmd += ["--checks", cfg["checks"]]

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=7200)
    out = (proc.stdout or "") + (proc.stderr or "")

    artifacts["log"].write_text(sanitize(out, [token, password]), encoding="utf-8")
    leak_hits = sanitize_file(artifacts["junit"], [token, password])
    leak_hits += sanitize_file(artifacts["ndjson"], [token, password])

    versions = tool_versions()
    junit = parse_junit(artifacts["junit"])
    ndjson = parse_ndjson(artifacts["ndjson"])
    cli = parse_cli(out)
    summary_path = results_dir / f"{prefix}_summary.md"
    write_summary(summary_path, args.round, cfg, args, proc.returncode, versions, junit,
                  ndjson, cli, {k: f"results/{p.name}" for k, p in artifacts.items()},
                  expected, leak_hits)

    print(f"[XONG] Exit code CLI: {proc.returncode}")
    print(f"       operation chọn được = {ndjson['operations_selected']} (mong đợi {expected})")
    print(f"       JUnit: tests={junit['tests']} failures={junit['failures']} errors={junit['errors']}")
    print(f"       CLI: {cli['generated']} testcase sinh ra, {cli['unique']} lỗi khác nhau, "
          f"{ndjson['running_time']}s")
    if expected is not None and ndjson["operations_selected"] != expected:
        print("       [CẢNH BÁO] Số operation thực tế KHÁC mong đợi — kiểm tra lại cấu hình lọc!")
    print(f"       log: {artifacts['log'].name}")
    print(f"       summary: {summary_path.name}")
    return 0 if proc.returncode == 0 else proc.returncode


if __name__ == "__main__":
    sys.exit(main())
