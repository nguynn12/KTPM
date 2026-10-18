#!/usr/bin/env python3
"""
scripts/prepare_baseline_TV1.py — Dựng lại ĐÚNG bộ baseline seed 101 của TV1 qua REST API.

Quy trình nhóm quy định: trước mỗi vòng kiểm thử phải "reset -> seed -> xác nhận baseline".
Script này làm đủ 3 bước đó:

  1. Reset: xoá hết documents / tags / correspondents / document_types (giữ nguyên user `admin`).
  2. Seed: upload lại 2 PDF seed của TV1 + tạo 3 tag, 2 correspondent, 2 document type
     (giống nhau trên mọi máy — xem docs/SEED_DATA_TV1.md), rồi gắn tag/correspondent/document_type
     cho tài liệu "Hoa don dien T9/2026" như biên bản results/TV1_deploy_13-10.md.
  3. Xác nhận baseline: in ra số lượng bản ghi + kết quả 2 truy vấn search/lọc để đối chiếu.

Điều kiện: `docker compose up -d` đã chạy, webserver healthy, tài khoản `admin/admin`.

Cách chạy:
  .\\.venv\\Scripts\\python.exe scripts\\prepare_baseline_TV1.py
  .\\.venv\\Scripts\\python.exe scripts\\prepare_baseline_TV1.py --all-docs   # nạp cả 6 PDF

Biến môi trường: PAPERLESS_URL, PAPERLESS_ADMIN_USER, PAPERLESS_ADMIN_PASSWORD (mặc định localhost:8000, admin/admin).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện requests. Chạy: .\\.venv\\Scripts\\python.exe -m pip install requests")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE = os.getenv("PAPERLESS_URL", "http://localhost:8000").rstrip("/")
USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
PASSWORD = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")

TAGS = ["hoa-don", "can-xu-ly", "luu-tru-lau-dai"]
CORRESPONDENTS = ["Dien Luc Da Lat", "Phong Ke Toan"]
DOC_TYPES = ["Hoa don", "Bao cao"]

# (file PDF, tiêu đề đặt cho tài liệu) — khớp biên bản TV1_deploy_13-10.md
DOCS = [
    ("TV1_Sample_01_HoaDon_101.pdf", "Hoa don dien T9/2026"),
    ("TV1_Sample_03_BaoCao_101.pdf", "Bao cao tuan 41"),
]
DOCS_ALL = [
    ("TV1_Sample_01_HoaDon_101.pdf", "Hoa don dien T9/2026"),
    ("TV1_Sample_02_HopDong_101.pdf", "Hop dong dich vu ve sinh"),
    ("TV1_Sample_03_BaoCao_101.pdf", "Bao cao tuan 41"),
    ("TV1_Sample_04_BienBanHop_101.pdf", "Bien ban hop nhom 10/10/2026"),
    ("TV1_Sample_05_PhieuThu_101.pdf", "Phieu thu PT-118"),
    ("TV1_Sample_06_HuongDanScan_101.pdf", "Huong dan scan tai lieu"),
]
SAMPLE_DIR = Path(__file__).resolve().parent / "sample_docs"


def get_token() -> str:
    r = requests.post(f"{BASE}/api/token/", json={"username": USER, "password": PASSWORD}, timeout=20)
    if r.status_code != 200:
        sys.exit(f"[LỖI] Không lấy được token (HTTP {r.status_code}). Docker đã chạy chưa?")
    return r.json()["token"]


def fetch_all(sess: requests.Session, ep: str) -> list[dict]:
    """Lấy hết bản ghi của 1 endpoint (API phân trang, next = URL trang kế tiếp)."""
    items: list[dict] = []
    url, params = f"{BASE}{ep}", {"page_size": 100}
    while url:
        r = sess.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        items += data.get("results", [])
        url, params = data.get("next"), None
    return items


def reset(sess: requests.Session) -> None:
    print("=== 1. RESET dữ liệu ===")
    for name, ep in (("documents", "/api/documents/"), ("tags", "/api/tags/"),
                     ("correspondents", "/api/correspondents/"),
                     ("document_types", "/api/document_types/")):
        items = fetch_all(sess, ep)
        for item in items:
            r = sess.delete(f"{BASE}{ep}{item['id']}/", timeout=30)
            if not r.ok:
                print(f"  [FAIL] xoá {name} id={item['id']} -> HTTP {r.status_code}")
        print(f"  [ok] {name}: đã xoá {len(items)} bản ghi")
    # Xác nhận đã sạch hoàn toàn (không còn sót do phân trang)
    for name, ep in (("documents", "/api/documents/"), ("tags", "/api/tags/"),
                     ("correspondents", "/api/correspondents/"),
                     ("document_types", "/api/document_types/")):
        left = len(fetch_all(sess, ep))
        print(f"  [--] {name} còn lại: {left}")


def upload(sess: requests.Session, docs: list[tuple[str, str]]) -> None:
    print("=== 2. SEED: upload PDF ===")
    for filename, title in docs:
        path = SAMPLE_DIR / filename
        if not path.exists():
            sys.exit(f"[LỖI] Không thấy file seed: {path}")
        with path.open("rb") as fh:
            r = sess.post(f"{BASE}/api/documents/post_document/",
                          files={"document": (filename, fh, "application/pdf")},
                          data={"title": title}, timeout=120)
        body = r.text.strip()
        print(f"  [{'ok' if r.ok else 'FAIL'}] {filename} (title='{title}') -> HTTP {r.status_code} "
              f"task={body[:36]}")


def wait_ocr(sess: requests.Session, expect: int, timeout_s: int = 300) -> list[dict]:
    print(f"=== 3. Chờ OCR xong ({expect} tài liệu) ===")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        docs = sess.get(f"{BASE}/api/documents/", timeout=30).json().get("results", [])
        ready = [d for d in docs if (d.get("content") or "").strip()]
        print(f"  ... {len(docs)}/{expect} tài liệu, {len(ready)} đã có chữ OCR")
        if len(docs) >= expect and len(ready) >= expect:
            return docs
        time.sleep(6)
    sys.exit("[LỖI] Hết thời gian chờ OCR.")


def create_metadata(sess: requests.Session) -> tuple[dict, dict, dict]:
    print("=== 4. SEED: tag / correspondent / document type ===")
    ids = {}
    for label, ep, names in (("tag", "/api/tags/", TAGS),
                             ("correspondent", "/api/correspondents/", CORRESPONDENTS),
                             ("document type", "/api/document_types/", DOC_TYPES)):
        for name in names:
            r = sess.post(f"{BASE}{ep}", json={"name": name}, timeout=30)
            print(f"  [{'ok' if r.ok else 'FAIL'}] {label} '{name}' -> HTTP {r.status_code}")
            if r.ok:
                ids[name] = r.json().get("id")
    return ids


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-docs", action="store_true", help="nạp cả 6 PDF thay vì 2 (mặc định 2 như biên bản)")
    a = ap.parse_args()
    docs = DOCS_ALL if a.all_docs else DOCS

    print(f"### prepare_baseline_TV1.py — {BASE} (user={USER}) ###")
    token = get_token()
    sess = requests.Session()
    sess.headers.update({"Authorization": f"Token {token}"})

    reset(sess)
    upload(sess, docs)
    wait_ocr(sess, len(docs))
    ids = create_metadata(sess)

    # Gắn metadata cho tài liệu "Hoa don" giống biên bản 13/10 (tag=1, corr=1, dtype=1)
    doc_list = sess.get(f"{BASE}/api/documents/", timeout=30).json().get("results", [])
    target = next((d for d in doc_list if d["title"].startswith("Hoa don")), None)
    if target:
        payload = {"tags": [ids["hoa-don"]], "correspondent": ids["Dien Luc Da Lat"],
                   "document_type": ids["Hoa don"]}
        r = sess.patch(f"{BASE}/api/documents/{target['id']}/", json=payload, timeout=30)
        print(f"=== 5. PATCH tài liệu '{target['title']}' (id={target['id']}) -> HTTP {r.status_code}")

    print("\n=== 6. XÁC NHẬN BASELINE ===")
    counts = {}
    for name, ep in (("documents", "/api/documents/"), ("tags", "/api/tags/"),
                     ("correspondents", "/api/correspondents/"), ("document_types", "/api/document_types/")):
        counts[name] = sess.get(f"{BASE}{ep}", timeout=30).json()["count"]
    print(f"  documents={counts['documents']} tags={counts['tags']} "
          f"correspondents={counts['correspondents']} document_types={counts['document_types']}")
    for d in sess.get(f"{BASE}/api/documents/", timeout=30).json()["results"]:
        print(f"    - id={d['id']} title='{d['title']}' tags={d.get('tags')} "
              f"corr={d.get('correspondent')} dtype={d.get('document_type')} "
              f"len(content)={len((d.get('content') or '').strip())}")
    q1 = sess.get(f"{BASE}/api/documents/", params={"query": "dien"}, timeout=30).json()
    q2 = sess.get(f"{BASE}/api/documents/", params={"tags__id__in": ids.get("hoa-don")}, timeout=30).json()
    print(f"  search 'dien'      -> count={q1['count']} ids={[d['id'] for d in q1['results']]}")
    print(f"  lọc tag 'hoa-don'  -> count={q2['count']} ids={[d['id'] for d in q2['results']]}")
    print("\nBaseline xong. Giờ có thể chạy: scripts/run_round_TV1.py --round 1")


if __name__ == "__main__":
    main()
