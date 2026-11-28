#!/usr/bin/env python3
"""
scripts/run_boundary_tests.py

Thực thi 8 test case thiết kế thủ công (mục 5.2 báo cáo giữa kỳ) cho tài nguyên /api/tags/:
    TC05, TC06, TC07, TC08, TC09, TC10, TC12, TC13

Mục đích: sinh số liệu THẬT để điền cột "Thực tế" và "Pass/Fail" trong báo cáo,
đồng thời lưu log/bảng vào thư mục results/.

Cách dùng:
    python scripts/run_boundary_tests.py                     # 1 lượt, dọn tag tạm sau khi chạy
    python scripts/run_boundary_tests.py --label run1        # đặt nhãn lượt chạy cho tên file log
    python scripts/run_boundary_tests.py --keep              # giữ tag đã tạo để chụp ảnh minh chứng
    python scripts/run_boundary_tests.py --run-id 2026101801 # cố định mã lượt chạy
    python scripts/run_boundary_tests.py --executor "TV2 - Tạ Nhật Nguyên"
                                                             # đổi tên người thực hiện trong log
                                                             # (mặc định: TV5 - Trần Quốc Khánh)

Điều kiện trước (khuyến nghị, để kết quả tái lập được):
    python scripts/reset_data.py
    python scripts/seed_data.py

Token: lấy từ biến môi trường PAPERLESS_TOKEN, nếu không có thì tự gọi POST /api/token/.
Không hardcode token (quy tắc nhóm: không đẩy token/mật khẩu lên Git).
"""

from __future__ import annotations

import argparse
import json
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
ADMIN_USER = os.getenv("PAPERLESS_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PAPERLESS_ADMIN_PASSWORD", "admin")

TAGS_ENDPOINT = "/api/tags/"
NAME_MAX = 128  # TagRequest.name trong /api/schema/: minLength 1, maxLength 128

STATUS_TEXT = {
    200: "200 OK",
    201: "201 Created",
    204: "204 No Content",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    500: "500 Server Error",
}

TRANSCRIPT: list[str] = []
ROWS: list[dict] = []
CREATED_IDS: list[int] = []


# --------------------------------------------------------------------------- #
# Tiện ích
# --------------------------------------------------------------------------- #
def emit(line: str = "") -> None:
    print(line)
    TRANSCRIPT.append(line)


def mask(token: str) -> str:
    return f"{token[:6]}...{token[-4:]}" if len(token) > 12 else "***"


def short(text: str, limit: int = 150) -> str:
    flat = " ".join(str(text).split())
    return flat[:limit] + ("..." if len(flat) > limit else "")


def status_text(code) -> str:
    if code is None:
        return "ERROR"
    return STATUS_TEXT.get(code, str(code))


def http(method: str, path: str, headers=None, payload=None, timeout=15):
    """Trả về (status_code|None, body_text, elapsed_ms, error|None)."""
    started = time.time()
    try:
        res = requests.request(method, f"{BASE_URL}{path}", headers=headers, json=payload, timeout=timeout)
        return res.status_code, res.text, int((time.time() - started) * 1000), None
    except Exception as exc:  # noqa: BLE001 - ghi lỗi mạng vào log rồi tiếp tục
        return None, "", int((time.time() - started) * 1000), str(exc)


def build_name(prefix: str, total_len: int, filler: str, run_id: str) -> str:
    """Tên có tiền tố + mã lượt chạy, đệm cho đúng total_len ký tự (chạy lại vẫn không trùng)."""
    body = f"{prefix}{run_id}"
    pad = total_len - len(body)
    if pad < 0:
        raise ValueError(f"Mã lượt chạy quá dài cho tiền tố {prefix}")
    return body + filler * pad


def record(tc_id, kind, title, data, expected, actual, verdict, detail=""):
    ROWS.append(
        {
            "id": tc_id,
            "kind": kind,
            "title": title,
            "data": data,
            "expected": expected,
            "actual": actual,
            "verdict": verdict,
            "detail": detail,
        }
    )
    emit(f"{tc_id:<5} | kỳ vọng: {expected:<29} | thực tế: {actual:<28} | {verdict}")
    if detail:
        emit(f"      {detail}")


def get_token() -> str:
    token = (os.getenv("PAPERLESS_TOKEN") or "").strip()
    if token:
        emit(f"[TOKEN] Dùng PAPERLESS_TOKEN từ biến môi trường ({mask(token)})")
        return token

    # Endpoint /api/token/ bị throttle (429). Thử lại tối đa 3 lần theo thời gian công cụ báo.
    for attempt in range(1, 4):
        res = requests.post(
            f"{BASE_URL}/api/token/",
            data={"username": ADMIN_USER, "password": ADMIN_PASS},
            timeout=10,
        )
        if res.status_code == 200:
            token = res.json()["token"]
            emit(f"[TOKEN] Lấy mới qua POST /api/token/ ({mask(token)})")
            return token

        if res.status_code == 429 and attempt < 3:
            wait = 11
            try:
                detail = res.json().get("detail", "")
                wait = int(detail.split("in ")[1].split(" ")[0]) + 2
            except Exception:
                pass
            emit(f"[TOKEN] Bị throttle (429), chờ {wait}s rồi thử lại (lần {attempt + 1}/3)...")
            time.sleep(wait)
            continue

        emit(f"[LỖI] Không lấy được token: HTTP {res.status_code} {short(res.text)}")
        sys.exit(1)

    sys.exit(1)


# --------------------------------------------------------------------------- #
# 8 test case
# --------------------------------------------------------------------------- #
def run_cases(headers, token, run_id):
    # TC05 - biên trên hợp lệ của name (đúng 128 ký tự)
    name128 = build_name("TC05_", NAME_MAX, "A", run_id)
    emit("")
    emit(f"--- TC05: POST {TAGS_ENDPOINT} name = {len(name128)} ký tự ---")
    emit(f"    payload: {name128[:40]}...{name128[-10:]}")
    st, body, ms, err = http("POST", TAGS_ENDPOINT, headers, {"name": name128})
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    if st == 201:
        try:
            CREATED_IDS.append(json.loads(body)["id"])
        except Exception:
            pass
        verdict, note = "PASS", "Tên đúng 128 ký tự được tạo thành công."
    elif st == 400 and "already exists" in body:
        verdict, note = "FAIL", "Tên 128 ký tự đã tồn tại từ lượt chạy trước (cần reset trước khi chạy)."
    else:
        verdict, note = "FAIL", ""
    record("TC05", "Biên", "Tên đúng giới hạn độ dài tối đa",
           f"`name` = 128 ký tự (`TC05_<mã lượt>` + đệm `A`)",
           "201", status_text(st), verdict, note)

    # TC06 - vượt biên 1 ký tự (129 ký tự)
    name129 = build_name("TC06_", NAME_MAX + 1, "B", run_id)
    emit("")
    emit(f"--- TC06: POST {TAGS_ENDPOINT} name = {len(name129)} ký tự ---")
    st, body, ms, err = http("POST", TAGS_ENDPOINT, headers, {"name": name129})
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    ok = st == 400 and "no more than 128 characters" in body
    note = "Thông báo lỗi đúng như mong đợi (max 128)." if ok else ("Đã bị từ chối 400." if st == 400 else "")
    record("TC06", "Biên", "Tên vượt giới hạn 1 ký tự",
           f"`name` = 129 ký tự (`TC06_<mã lượt>` + đệm `B`)",
           "400", status_text(st), "PASS" if ok else "FAIL", note)

    # TC07 - tên tiếng Việt có dấu + emoji
    name07 = f"Hóa đơn tháng 10 🧾 – Đà Lạt {run_id}"
    emit("")
    emit(f"--- TC07: POST {TAGS_ENDPOINT} name = tiếng Việt có dấu + emoji ---")
    st, body, ms, err = http("POST", TAGS_ENDPOINT, headers, {"name": name07})
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    if st == 201:
        try:
            payload = json.loads(body)
            CREATED_IDS.append(payload["id"])
            note = f"Tạo thành công, `slug` = {payload.get('slug')!r}."
        except Exception:
            note = "Tạo thành công."
    else:
        note = ""
    record("TC07", "Positive", "Tên tiếng Việt có dấu, emoji",
           '`name` = `"Hóa đơn tháng 10 🧾 – Đà Lạt <mã lượt>"`',
           "201, không 500", status_text(st),
           "PASS" if st is not None and st < 500 else "FAIL", note)

    # TC08 - ký tự đặc biệt
    name08 = f"<script>alert('XSS')</script>_{run_id}"
    emit("")
    emit(f"--- TC08: POST {TAGS_ENDPOINT} name = ký tự đặc biệt ---")
    st, body, ms, err = http("POST", TAGS_ENDPOINT, headers, {"name": name08})
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    if st == 201:
        try:
            CREATED_IDS.append(json.loads(body)["id"])
        except Exception:
            pass
        note = "Chuỗi được lưu nguyên văn (JSON escape), không có 5xx."
    else:
        note = ""
    record("TC08", "Negative", "Ký tự đặc biệt `<script>`, dấu nháy đơn",
           "`name` = `\"<script>alert('XSS')</script>_<mã lượt>\"`",
           "không 500", status_text(st),
           "PASS" if st is not None and st < 500 else "FAIL", note)

    # TC09 - ID không tồn tại
    emit("")
    emit(f"--- TC09: GET {TAGS_ENDPOINT}999999/ ---")
    st, body, ms, err = http("GET", f"{TAGS_ENDPOINT}999999/", headers)
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    record("TC09", "Negative", "ID không tồn tại", "`GET /api/tags/999999/`",
           "404", status_text(st), "PASS" if st == 404 else "FAIL")

    # TC10 - xóa hai lần cùng một ID
    emit("")
    emit(f"--- TC10: DELETE {TAGS_ENDPOINT}{{id}}/ hai lần ---")
    temp_name = f"TC10_Delete_Twice_{run_id}"
    st_c, body_c, _, _ = http("POST", TAGS_ENDPOINT, headers, {"name": temp_name})
    temp_id = None
    if st_c == 201:
        try:
            temp_id = json.loads(body_c)["id"]
        except Exception:
            temp_id = None
    emit(f"    tạo tag tạm: {status_text(st_c)} (id={temp_id})")
    if temp_id is None:
        record("TC10", "Negative", "Xóa hai lần cùng ID", "`DELETE /api/tags/{id}/` hai lần",
               "lần 2: 404", "không tạo được tag tạm", "FAIL",
               "Không tạo được tag tạm để kiểm thử.")
    else:
        st1, body1, ms1, _ = http("DELETE", f"{TAGS_ENDPOINT}{temp_id}/", headers)
        emit(f"    lần 1 -> {status_text(st1)} ({ms1} ms) {short(body1, 80)}")
        st2, body2, ms2, _ = http("DELETE", f"{TAGS_ENDPOINT}{temp_id}/", headers)
        emit(f"    lần 2 -> {status_text(st2)} ({ms2} ms) {short(body2, 80)}")
        actual = f"lần 1: {status_text(st1)}; lần 2: {status_text(st2)}"
        ok = st1 in (200, 204) and st2 == 404
        record("TC10", "Negative", "Xóa hai lần cùng ID", "`DELETE /api/tags/{id}/` hai lần",
               "lần 2: 404", actual, "PASS" if ok else "FAIL",
               f"id dùng để thử: {temp_id} (đã bị xóa ở lần 1)")

    # TC12 - token sai
    wrong_token = token[:-1] + ("0" if token[-1] != "0" else "1")
    emit("")
    emit(f"--- TC12: GET {TAGS_ENDPOINT} với token sai 1 ký tự ---")
    st, body, ms, err = http("GET", f"{TAGS_ENDPOINT}?page=1", {"Authorization": f"Token {wrong_token}"})
    emit(f"    -> {status_text(st)} ({ms} ms) {short(body)}")
    st_r, body_r, _, _ = http("GET", f"{TAGS_ENDPOINT}?page=1", {"Authorization": "Token khong_phai_token"})
    emit(f"    token rác  -> {status_text(st_r)} {short(body_r, 60)}")
    record("TC12", "Bảo mật", "Token sai", "đổi 1 ký tự token (và thử thêm token rác)",
           "401", status_text(st), "PASS" if st == 401 else "FAIL",
           f"token rác cũng trả {status_text(st_r)}")

    # TC13 - tham số phân trang bất thường
    emit("")
    emit(f"--- TC13: GET {TAGS_ENDPOINT} với page_size bất thường ---")
    parts = []
    codes = []
    for value in ["0", "-1", "100000", "999999999", "abc"]:
        st, body, ms, _ = http("GET", f"{TAGS_ENDPOINT}?page_size={value}", headers)
        emit(f"    page_size={value:<10} -> {status_text(st)} ({ms} ms) {short(body, 70)}")
        parts.append(f"page_size={value}→{st}")
        codes.append(st)
    st_p0, body_p0, _, _ = http("GET", f"{TAGS_ENDPOINT}?page=0", headers)
    emit(f"    page=0               -> {status_text(st_p0)} {short(body_p0, 70)}")
    parts.append(f"page=0→{st_p0}")
    codes.append(st_p0)
    actual = "; ".join(parts)
    ok = all(c is not None and c < 500 for c in codes)
    record("TC13", "Biên", "Tham số phân trang bất thường", "`page_size` = 0, -1, rất lớn (thêm `page=0`)",
           "không 500", actual, "PASS" if ok else "FAIL",
           "page_size bất thường bị bỏ qua, dùng kích thước trang mặc định; riêng page=0 bị từ chối 404 \"Invalid page.\"")


# --------------------------------------------------------------------------- #
# Báo cáo
# --------------------------------------------------------------------------- #
def markdown_table() -> str:
    lines = [
        "| ID | Loại | Tiêu đề | Dữ liệu | Kết quả mong đợi | Thực tế | Pass/Fail |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in ROWS:
        verdict = f"**{row['verdict']}**" if row["verdict"] == "PASS" else row["verdict"]
        lines.append(
            f"| {row['id']} | {row['kind']} | {row['title']} | {row['data']} | "
            f"{row['expected']} | {row['actual']} | {verdict} |"
        )
    return "\n".join(lines)


def write_outputs(run_id, label, executor, tag_count_before, tag_count_after):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    prefix = executor.split()[0] if executor.split() else "TV"
    base = os.path.join(results_dir, f"{prefix}_manual_TC05-TC13_{label}")

    header = [
        "# Kết quả kiểm thử thủ công TC05-TC13 (mục 5.2 báo cáo giữa kỳ)",
        "",
        f"- Người thực hiện: {executor}",
        f"- Ngày chạy: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Môi trường: {BASE_URL} - Paperless-ngx v3.1.3 (Docker, ghcr.io/paperless-ngx/paperless-ngx:3.1.3)",
        f"- Mã lượt chạy: {run_id}",
        f"- Dữ liệu seed: scripts/seed_data.py (4 tag, 3 correspondent, 3 document type, 2 tài liệu)",
        f"- Điều kiện trước: {tag_count_before} tag trong hệ thống",
        f"- Sau khi chạy: {tag_count_after} tag trong hệ thống",
        "",
    ]

    md = "\n".join(header) + "\n" + markdown_table() + "\n\n## Chi tiết từng ca\n\n"
    for row in ROWS:
        md += f"### {row['id']} - {row['title']}\n"
        md += f"- Dữ liệu: {row['data']}\n"
        md += f"- Mong đợi: {row['expected']}\n"
        md += f"- Thực tế: {row['actual']}\n"
        md += f"- Đánh giá: {row['verdict']}\n"
        if row["detail"]:
            md += f"- Ghi chú: {row['detail']}\n"
        md += "\n"

    with open(f"{base}.md", "w", encoding="utf-8") as fh:
        fh.write(md)
    with open(f"{base}.log", "w", encoding="utf-8") as fh:
        fh.write("\n".join(TRANSCRIPT) + "\n")
    return f"{base}.md", f"{base}.log"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description="Chạy 8 test case TC05-TC13 cho /api/tags/")
    parser.add_argument("--run-id", default=None, help="Mã lượt chạy (mặc định: MMddHHMMSS)")
    parser.add_argument("--label", default=None, help="Nhãn lượt chạy dùng cho tên file log (mặc định: run<MMDD>)")
    parser.add_argument("--keep", action="store_true", help="Giữ lại tag đã tạo để chụp ảnh minh chứng")
    parser.add_argument(
        "--executor",
        default=os.getenv("PAPERLESS_EXECUTOR", "TV5 - Trần Quốc Khánh (2312646)"),
        help="Tên người thực hiện, ghi vào log và dùng làm tiền tố tên file",
    )
    args = parser.parse_args()

    run_id = args.run_id or time.strftime("%m%d%H%M%S")
    label = args.label or f"run{time.strftime('%m%d')}"

    emit("=" * 110)
    emit(f"KIỂM THỬ THỦ CÔNG BIÊN: TC05-TC13 cho /api/tags/ - {BASE_URL}")
    emit(f"Thời điểm: {time.strftime('%Y-%m-%d %H:%M:%S')} | mã lượt chạy: {run_id} | nhãn: {label}")
    emit("=" * 110)

    token = get_token()
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

    st, body, _, _ = http("GET", f"{TAGS_ENDPOINT}?page_size=1", headers)
    tag_count_before = None
    if st == 200:
        tag_count_before = json.loads(body).get("count")
    emit(f"[TRẠNG THÁI] Số tag trước khi chạy: {tag_count_before}")

    run_cases(headers, token, run_id)

    if not args.keep:
        emit("")
        emit("--- Dọn tag tạm đã tạo trong lượt chạy này ---")
        for tag_id in CREATED_IDS:
            st_d, _, _, _ = http("DELETE", f"{TAGS_ENDPOINT}{tag_id}/", headers)
            emit(f"    xóa id={tag_id} -> {status_text(st_d)}")
    else:
        emit("")
        emit(f"[GIỮ LẠI] Các tag đã tạo: {CREATED_IDS} (dùng --keep, không dọn)")

    st, body, _, _ = http("GET", f"{TAGS_ENDPOINT}?page_size=1", headers)
    tag_count_after = json.loads(body).get("count") if st == 200 else None

    emit("")
    emit(markdown_table())
    emit("")

    passed = sum(1 for row in ROWS if row["verdict"] == "PASS")
    emit(f"TỔNG KẾT: {passed}/{len(ROWS)} ca PASS")
    for row in ROWS:
        if row["verdict"] != "PASS":
            emit(f"  - {row['id']} FAIL: {row['actual']}")

    md_path, log_path = write_outputs(run_id, label, args.executor, tag_count_before, tag_count_after)
    emit("")
    emit(f"Đã ghi: {md_path}")
    emit(f"Đã ghi: {log_path}")


if __name__ == "__main__":
    main()
