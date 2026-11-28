#!/usr/bin/env python3
"""
scripts/run_manual_tests_TV3_part2.py
Chay not 22 ca NOT RUN (TV3): 7 Correspondents + 15 Document Types.
Tu dong cap nhat docs/TEST_CASES_TV3.md (co backup .bak).

Chay: .venv/Scripts/python.exe scripts/run_manual_tests_TV3_part2.py
"""

import os
import sys
import time
import re
import shutil
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
# tim thu muc goc project (noi co .env): thu muc cha cua scripts/, hoac noi chay script
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == "scripts" else os.getcwd()
BASE_URL = os.getenv("PAPERLESS_URL", "http://localhost:8000")


def load_dotenv():
    env = {}
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env


_dotenv = load_dotenv()
ADMIN_USER = os.getenv("PL_USER", _dotenv.get("PAPERLESS_ADMIN_USER", "admin"))
ADMIN_PASS = os.getenv("PL_PASS", _dotenv.get("PAPERLESS_ADMIN_PASSWORD", ""))
if not ADMIN_PASS:
    print("THIEU MAT KHAU: khong tim thay PAPERLESS_ADMIN_PASSWORD trong .env")
    sys.exit(1)


def get_token():
    r = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": ADMIN_USER, "password": ADMIN_PASS},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["token"]


token = get_token()
H = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
H_NOAUTH = {"Content-Type": "application/json"}
H_FAKE = {"Authorization": "Token invalid-fake-token-tv3", "Content-Type": "application/json"}

RUN = int(time.time()) % 1000000
STATUS_LABEL = {200: "200 OK", 201: "201 Created", 204: "204 No Content",
                400: "400 Bad Request", 401: "401 Unauthorized", 404: "404 Not Found"}

results = []  # (case_id, expected, actual, verdict)
created = {"correspondents": [], "document_types": []}


def rec(cid, expected, actual):
    verdict = "PASS" if actual == expected else "FAIL"
    results.append((cid, expected, actual, verdict))
    return verdict


def mk(res, payload):
    r = requests.post(f"{BASE_URL}/api/{res}/", headers=H, json=payload, timeout=10)
    if r.status_code == 201:
        try:
            created[res].append(r.json()["id"])
        except Exception:
            pass
    return r


def run():
    print("=== PART 2: 22 ca NOT RUN (TV3) - RUN %s ===\n" % RUN)
    print(f"{'Ma TC':<12} | {'Ky vong':<7} | {'Thuc te':<7} | {'Ket qua':<6} | Mo ta")
    print("-" * 80)

    # ---------- CORRESPONDENTS (7 ca) ----------
    r = mk("correspondents", {"name": "C" * 1000})
    rec("TV3-COR-09", 400, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR11_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        g = requests.get(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        ok = g.status_code == 200 and g.json().get("name") == f"TV3_P2_COR11_{RUN}"
        rec("TV3-COR-11", 200, g.status_code if ok else -1)
    else:
        rec("TV3-COR-11", 200, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR12_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        created["correspondents"].remove(cid)
        g = requests.get(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        rec("TV3-COR-12", 404, g.status_code)
    else:
        rec("TV3-COR-12", 404, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR13_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        p = requests.patch(f"{BASE_URL}/api/correspondents/{cid}/",
                           headers=H, json={"name": f"TV3_P2_COR13_NEW_{RUN}"}, timeout=10)
        g = requests.get(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        ok = p.status_code == 200 and g.json().get("name") == f"TV3_P2_COR13_NEW_{RUN}"
        rec("TV3-COR-13", 200, p.status_code if ok else -1)
    else:
        rec("TV3-COR-13", 200, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR14_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        p = requests.put(f"{BASE_URL}/api/correspondents/{cid}/", headers=H,
                         json={"name": f"TV3_P2_COR14_PUT_{RUN}", "matching_algorithm": 2},
                         timeout=10)
        rec("TV3-COR-14", 200, p.status_code)
    else:
        rec("TV3-COR-14", 200, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR15_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        d = requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        created["correspondents"].remove(cid)
        rec("TV3-COR-15", 204, d.status_code)
    else:
        rec("TV3-COR-15", 204, r.status_code)

    r = mk("correspondents", {"name": f"TV3_P2_COR16_{RUN}"})
    cid = r.json()["id"] if r.status_code == 201 else None
    if cid:
        requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        created["correspondents"].remove(cid)
        d2 = requests.delete(f"{BASE_URL}/api/correspondents/{cid}/", headers=H, timeout=10)
        rec("TV3-COR-16", 404, d2.status_code)
    else:
        rec("TV3-COR-16", 404, r.status_code)

    # ---------- DOCUMENT TYPES (15 ca) ----------
    r = mk("document_types", {"name": None})
    rec("TV3-DT-04", 400, r.status_code)

    dup_name = f"TV3_P2_DT_DUP_{RUN}"
    r1 = mk("document_types", {"name": dup_name})
    r2 = requests.post(f"{BASE_URL}/api/document_types/", headers=H,
                       json={"name": dup_name}, timeout=10)
    rec("TV3-DT-05", 400, r2.status_code if r1.status_code == 201 else r1.status_code)

    r = mk("document_types", {"name": "D" * 127})
    rec("TV3-DT-06", 201, r.status_code)
    r = mk("document_types", {"name": "D" * 128})
    rec("TV3-DT-07", 201, r.status_code)
    r = mk("document_types", {"name": "D" * 1000})
    rec("TV3-DT-09", 400, r.status_code)
    r = mk("document_types", {"name": f"TV3_Lo\u1ea1i_H\u1ee3p_\u0110\u1ed3ng_\U0001f4dd_{RUN}"})
    rec("TV3-DT-10", 201, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT11_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        g = requests.get(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        ok = g.status_code == 200 and g.json().get("name") == f"TV3_P2_DT11_{RUN}"
        rec("TV3-DT-11", 200, g.status_code if ok else -1)
    else:
        rec("TV3-DT-11", 200, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT12_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        requests.delete(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        created["document_types"].remove(did)
        g = requests.get(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        rec("TV3-DT-12", 404, g.status_code)
    else:
        rec("TV3-DT-12", 404, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT13_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        p = requests.patch(f"{BASE_URL}/api/document_types/{did}/", headers=H,
                           json={"name": f"TV3_P2_DT13_NEW_{RUN}"}, timeout=10)
        rec("TV3-DT-13", 200, p.status_code)
    else:
        rec("TV3-DT-13", 200, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT14_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        p = requests.put(f"{BASE_URL}/api/document_types/{did}/", headers=H,
                         json={"name": f"TV3_P2_DT14_PUT_{RUN}", "matching_algorithm": 3},
                         timeout=10)
        rec("TV3-DT-14", 200, p.status_code)
    else:
        rec("TV3-DT-14", 200, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT15_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        d = requests.delete(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        created["document_types"].remove(did)
        rec("TV3-DT-15", 204, d.status_code)
    else:
        rec("TV3-DT-15", 204, r.status_code)

    r = mk("document_types", {"name": f"TV3_P2_DT16_{RUN}"})
    did = r.json()["id"] if r.status_code == 201 else None
    if did:
        requests.delete(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        created["document_types"].remove(did)
        d2 = requests.delete(f"{BASE_URL}/api/document_types/{did}/", headers=H, timeout=10)
        rec("TV3-DT-16", 404, d2.status_code)
    else:
        rec("TV3-DT-16", 404, r.status_code)

    g = requests.get(f"{BASE_URL}/api/document_types/", headers=H_NOAUTH, timeout=10)
    rec("TV3-DT-17", 401, g.status_code)
    g = requests.get(f"{BASE_URL}/api/document_types/", headers=H_FAKE, timeout=10)
    rec("TV3-DT-18", 401, g.status_code)
    g = requests.get(f"{BASE_URL}/api/document_types/?page=1&page_size=1", headers=H, timeout=10)
    rec("TV3-DT-19", 200, g.status_code)

    for cid, exp, act, ver in results:
        print(f"{cid:<12} | {exp:<7} | {act:<7} | {ver:<6}")
    print("-" * 80)

    # don dep
    n_c = n_d = 0
    for tid in created["correspondents"]:
        try:
            requests.delete(f"{BASE_URL}/api/correspondents/{tid}/", headers=H, timeout=10)
            n_c += 1
        except Exception:
            pass
    for tid in created["document_types"]:
        try:
            requests.delete(f"{BASE_URL}/api/document_types/{tid}/", headers=H, timeout=10)
            n_d += 1
        except Exception:
            pass
    print(f"[OK] Da don dep: {n_c} Correspondents, {n_d} DocumentTypes.\n")
    return results


def patch_md(results):
    md_path = os.path.join(ROOT, "docs", "TEST_CASES_TV3.md")
    if not os.path.exists(md_path):
        print("Khong tim thay docs/TEST_CASES_TV3.md de cap nhat.")
        return
    shutil.copy(md_path, md_path + ".bak")
    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()

    by_id = {cid: (exp, act, ver) for cid, exp, act, ver in results}
    updated = []
    for i, ln in enumerate(lines):
        m = re.match(r"\|\s*(TV3-[A-Z]+-\d+)\s*\|", ln)
        if m and m.group(1) in by_id:
            cid = m.group(1)
            exp, act, ver = by_id[cid]
            parts = ln.rstrip("\n").split("|")
            if len(parts) >= 9:
                actual_label = STATUS_LABEL.get(act, str(act))
                parts[7] = f" {actual_label} "
                parts[8] = f" **{ver}** "
                lines[i] = "|".join(parts) + "\n"
                updated.append(cid)

    # cap nhat dong thong ke
    text = "".join(lines)
    cor_pass = sum(1 for cid, e, a, v in results if cid.startswith("TV3-COR") and v == "PASS")
    dt_pass = sum(1 for cid, e, a, v in results if cid.startswith("TV3-DT") and v == "PASS")
    text = re.sub(
        r"\*Thống kê Correspondents:\* \*\*\d+ PASS\*\*, \*\*1 REPRO-BUG-01\*\*, \*\*\d+ NOT RUN\*\* \(Tổng: 20 ca\)\.",
        f"*Thống kê Correspondents:* **{12 + cor_pass} PASS**, **1 REPRO-BUG-01**, **0 NOT RUN** (Tổng: 20 ca).",
        text,
    )
    text = re.sub(
        r"\*Thống kê Document Types:\* \*\*\d+ PASS\*\*, \*\*1 REPRO-BUG-01\*\*, \*\*\d+ NOT RUN\*\* \(Tổng: 20 ca\)\.",
        f"*Thống kê Document Types:* **{4 + dt_pass} PASS**, **1 REPRO-BUG-01**, **0 NOT RUN** (Tổng: 20 ca).",
        text,
    )
    text = re.sub(
        r"- \*\*22 ca NOT RUN:\*\*.*",
        "- **22 ca NOT RUN:** Đã chạy bổ sung bằng runner part2 — 0 ca NOT RUN còn lại.",
        text,
    )
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Da cap nhat {len(updated)} dong trong TEST_CASES_TV3.md (backup: TEST_CASES_TV3.md.bak)")


if __name__ == "__main__":
    res = run()
    patch_md(res)
    npass = sum(1 for r in res if r[3] == "PASS")
    print(f"TONG: {npass}/{len(res)} PASS")
