#!/usr/bin/env python3
"""Tạo metadata seed giống nhau trên mọi máy qua REST API — TV1.
Chạy sau khi đã upload 6 PDF seed:
  pip install requests
  python3 scripts/seed_and_verify_flows_TV1.py --base-url http://localhost:8000 --username ADMIN --password MAT_KHAU
"""
import argparse
import sys

try:
    import requests
except ImportError:
    sys.exit("Thieu thu vien requests. Chay: pip install requests")

TAGS = ["hoa-don", "can-xu-ly", "luu-tru-lau-dai"]
CORRESPONDENTS = ["Dien Luc Da Lat", "Phong Ke Toan"]
DOC_TYPES = ["Hoa don", "Bao cao"]

def get_token(base: str, user: str, pwd: str) -> str:
    r = requests.post(f"{base}/api/token/",
                      json={"username": user, "password": pwd}, timeout=15)
    r.raise_for_status()
    return r.json()["token"]

def ensure_list(sess: requests.Session, base: str, path: str, items: list[str]) -> None:
    existing = {o.get("name") for o in sess.get(f"{base}{path}", timeout=15).json().get("results", [])}
    for name in items:
        if name in existing:
            print(f"  [skip] {path} '{name}' da ton tai")
            continue
        r = sess.post(f"{base}{path}", json={"name": name}, timeout=15)
        print(f"  [{'ok' if r.ok else 'FAIL'}] POST {path} '{name}' -> {r.status_code}")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://localhost:8000")
    ap.add_argument("--username", required=True)
    ap.add_argument("--password", required=True)
    a = ap.parse_args()
    base = a.base_url.rstrip("/")
    token = get_token(base, a.username, a.password)
    sess = requests.Session()
    sess.headers.update({"Authorization": f"Token {token}", "Content-Type": "application/json"})
    print("Tags:");           ensure_list(sess, base, "/api/tags/", TAGS)
    print("Correspondents:"); ensure_list(sess, base, "/api/correspondents/", CORRESPONDENTS)
    print("Document types:"); ensure_list(sess, base, "/api/document_types/", DOC_TYPES)
    print("Xong. Kiem tra tren giao dien web muc Tags / Correspondents / Document types.")

if __name__ == "__main__":
    main()
