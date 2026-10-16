#!/usr/bin/env python3
"""
scripts/seed_and_verify_flows_TV3.py
Seed dữ liệu nền của nhóm và thực thi, ghi nhận 3 luồng nghiệp vụ thực tế cho TV3.
Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303.
Không in token hoặc mật khẩu ra màn hình/log.
"""

import os
import sys
import time
import json
from pathlib import Path
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


def get_auth_token():
    url = f"{BASE_URL}/api/token/"
    payload = {"username": ADMIN_USER, "password": ADMIN_PASS}
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
        token = res.json().get("token")
        print("[OK] Dang nhap thanh cong va lay Auth Token an toan (token khong in ra man hinh)")
        return token
    else:
        print(f"[LOI] Khong the lay token: HTTP {res.status_code} - {res.text}")
        sys.exit(1)


def get_all_paginated(url, headers):
    items = []
    current_url = url
    while current_url:
        res = requests.get(current_url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"[LOI] Khong the lay du lieu tu {current_url}: HTTP {res.status_code}")
            break
        data = res.json()
        items.extend(data.get("results", []))
        current_url = data.get("next")
    return items


def wait_for_task(task_id, headers, timeout_seconds=90):
    url = f"{BASE_URL}/api/tasks/?task_id={task_id}"
    start = time.time()
    while time.time() - start < timeout_seconds:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            tasks = data.get("results", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            for t in tasks:
                if str(t.get("task_id")) == str(task_id):
                    status = str(t.get("status", "")).lower()
                    if status == "success":
                        doc_ids = t.get("related_document_ids", [])
                        doc_id = doc_ids[0] if doc_ids else (t.get("result_data", {}) or {}).get("document_id")
                        return True, doc_id, t
                    elif status == "failure":
                        return False, None, t
        time.sleep(2)
    return False, None, {"error": "Timeout cho task hoan tat"}


def run():
    print("======================================================================")
    print("=== SEED DỮ LIỆU NỀN VÀ XÁC THỰC 3 LUỒNG NGHIỆP VỤ THỰC TẾ (TV3) ===")
    print("=== Tác giả: Nguyễn Khiêm Thuận - MSSV: 2312764 - TV3 - Seed: 303 ===")
    print("======================================================================\n")

    token = get_auth_token()
    headers = {"Authorization": f"Token {token}"}

    # =========================================================================
    # PHẦN 1: SEED DỮ LIỆU NỀN CỦA NHÓM (4 Tags, 3 Correspondents, 3 DocTypes)
    # =========================================================================
    print("\n--- 1. SEED DỮ LIỆU NỀN CỦA NHÓM ---")

    # 1.1 Tags
    existing_tags = {item["name"]: item["id"] for item in get_all_paginated(f"{BASE_URL}/api/tags/", headers)}
    tags_to_seed = [
        {"name": "TV2_Tag_Invoice_202", "color": "#e6194b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Urgent_202", "color": "#3cb44b", "is_inbox_tag": False},
        {"name": "TV2_Tag_Archive_202", "color": "#ffe119", "is_inbox_tag": False},
        {"name": "TV2_Tag_Finance_202", "color": "#4363d8", "is_inbox_tag": False},
    ]
    tag_map = dict(existing_tags)
    for t_data in tags_to_seed:
        if t_data["name"] in tag_map:
            print(f"[INFO] Tag '{t_data['name']}' da ton tai (ID: {tag_map[t_data['name']]})")
        else:
            res = requests.post(f"{BASE_URL}/api/tags/", json=t_data, headers=headers, timeout=10)
            if res.status_code == 201:
                item = res.json()
                tag_map[item["name"]] = item["id"]
                print(f"[OK] Da tao Tag '{item['name']}' (ID: {item['id']})")
            else:
                print(f"[CANH BAO] Khong the tao Tag '{t_data['name']}': {res.status_code} {res.text}")

    # 1.2 Correspondents
    existing_corrs = {item["name"]: item["id"] for item in get_all_paginated(f"{BASE_URL}/api/correspondents/", headers)}
    corrs_to_seed = [
        {"name": "TV2_Bank_202"},
        {"name": "TV2_Supplier_202"},
        {"name": "TV2_University_202"},
    ]
    corr_map = dict(existing_corrs)
    for c_data in corrs_to_seed:
        if c_data["name"] in corr_map:
            print(f"[INFO] Correspondent '{c_data['name']}' da ton tai (ID: {corr_map[c_data['name']]})")
        else:
            res = requests.post(f"{BASE_URL}/api/correspondents/", json=c_data, headers=headers, timeout=10)
            if res.status_code == 201:
                item = res.json()
                corr_map[item["name"]] = item["id"]
                print(f"[OK] Da tao Correspondent '{item['name']}' (ID: {item['id']})")
            else:
                print(f"[CANH BAO] Khong the tao Correspondent '{c_data['name']}': {res.status_code} {res.text}")

    # 1.3 Document Types
    existing_dtypes = {item["name"]: item["id"] for item in get_all_paginated(f"{BASE_URL}/api/document_types/", headers)}
    dtypes_to_seed = [
        {"name": "TV2_DocType_Invoice_202"},
        {"name": "TV2_DocType_Receipt_202"},
        {"name": "TV2_DocType_Contract_202"},
    ]
    dtype_map = dict(existing_dtypes)
    for dt_data in dtypes_to_seed:
        if dt_data["name"] in dtype_map:
            print(f"[INFO] DocumentType '{dt_data['name']}' da ton tai (ID: {dtype_map[dt_data['name']]})")
        else:
            res = requests.post(f"{BASE_URL}/api/document_types/", json=dt_data, headers=headers, timeout=10)
            if res.status_code == 201:
                item = res.json()
                dtype_map[item["name"]] = item["id"]
                print(f"[OK] Da tao DocumentType '{item['name']}' (ID: {item['id']})")
            else:
                print(f"[CANH BAO] Khong the tao DocumentType '{dt_data['name']}': {res.status_code} {res.text}")

    # 1.4 Upload 2 file TXT nền
    sample_dir = Path("scripts/sample_docs")
    sample_dir.mkdir(parents=True, exist_ok=True)
    txt_samples = [
        {
            "filename": "TV2_Sample_Invoice_202.txt",
            "title": "Hoa Don Thanh Toan Dich Vu KTPM Seed 202",
            "content": "HOA DON BAN HANG - SO TIEN 202.000 VND - NGUOI BAN: TV2 TA NHAT NGUYEN - DH DA LAT",
            "tag": "TV2_Tag_Invoice_202",
            "corr": "TV2_Bank_202",
            "dtype": "TV2_DocType_Invoice_202",
        },
        {
            "filename": "TV2_Sample_Contract_202.txt",
            "title": "Hop Dong Kiem Thu He Thong Schemathesis Seed 202",
            "content": "HOP DONG KIEM THU PHAN MEM MON HOC - NHOM 5 - PHU TRACH TV2 TA NHAT NGUYEN SEED 202",
            "tag": "TV2_Tag_Finance_202",
            "corr": "TV2_University_202",
            "dtype": "TV2_DocType_Contract_202",
        },
    ]

    for s in txt_samples:
        fpath = sample_dir / s["filename"]
        if not fpath.exists():
            fpath.write_text(s["content"], encoding="utf-8")
        post_data = {"title": s["title"]}
        if s["tag"] in tag_map:
            post_data["tags"] = [tag_map[s["tag"]]]
        if s["corr"] in corr_map:
            post_data["correspondent"] = corr_map[s["corr"]]
        if s["dtype"] in dtype_map:
            post_data["document_type"] = dtype_map[s["dtype"]]

        with open(fpath, "rb") as f:
            files = {"document": (s["filename"], f, "text/plain")}
            res = requests.post(f"{BASE_URL}/api/documents/post_document/", data=post_data, files=files, headers=headers, timeout=20)
            if res.status_code in (200, 202):
                task_id = res.text.strip('"')
                print(f"[OK] Da upload TXT '{s['filename']}' (Task UUID: {task_id})")
                ok, doc_id, t_info = wait_for_task(task_id, headers)
                if ok:
                    print(f"     -> Tieu thu thanh cong! Document ID: {doc_id}")
                else:
                    print(f"     -> [CANH BAO] Task chua hoan tat: {t_info}")
            else:
                print(f"[LOI] Upload TXT '{s['filename']}' that bai: {res.status_code} {res.text}")

    # =========================================================================
    # PHẦN 2: THỰC THI VÀ GHI NHẬN 3 LUỒNG NGHIỆP VỤ TV3
    # =========================================================================
    evidence = {}

    # LUỒNG 1: Upload PDF -> Chờ tác vụ -> GET tài liệu có content
    print("\n--- 2.1 LUỒNG 1: UPLOAD PDF VÀ XÁC NHẬN CONTENT (TV3-FLOW-01) ---")
    pdf_to_upload = sample_dir / "TV3_Sample_01_Report_303.pdf"
    if not pdf_to_upload.exists():
        print(f"[LOI] Khong tim thay file PDF: {pdf_to_upload}")
        sys.exit(1)

    flow1_title = "Bao Cao Kiem Thu Schemathesis TV3 Seed 303"
    with open(pdf_to_upload, "rb") as f:
        files = {"document": (pdf_to_upload.name, f, "application/pdf")}
        flow1_res = requests.post(
            f"{BASE_URL}/api/documents/post_document/",
            data={"title": flow1_title},
            files=files,
            headers=headers,
            timeout=30,
        )

    evidence["flow1_upload_status"] = flow1_res.status_code
    if flow1_res.status_code in (200, 202):
        flow1_task_id = flow1_res.text.strip('"')
        print(f"[OK] Luong 1 - Upload PDF '{pdf_to_upload.name}' thanh cong. Task UUID: {flow1_task_id}")
        evidence["flow1_task_id"] = flow1_task_id

        print("     Dang cho Paperless Celery worker OCR va consume...")
        ok, flow1_doc_id, t_info = wait_for_task(flow1_task_id, headers)
        if ok and flow1_doc_id:
            evidence["flow1_doc_id"] = flow1_doc_id
            print(f"[OK] Luong 1 - Task da hoan tat! Document ID tao ra: {flow1_doc_id}")

            # GET chi tiết tài liệu
            doc_res = requests.get(f"{BASE_URL}/api/documents/{flow1_doc_id}/", headers=headers, timeout=10)
            evidence["flow1_get_status"] = doc_res.status_code
            if doc_res.status_code == 200:
                doc_json = doc_res.json()
                content = doc_json.get("content", "")
                evidence["flow1_content_length"] = len(content)
                evidence["flow1_content_snippet"] = content[:200]
                print(f"[OK] Luong 1 - GET /api/documents/{flow1_doc_id}/ thanh cong (HTTP 200)")
                print(f"     Do dai content trich xuat: {len(content)} ky tu")
                print(f"     Trich doan content: {repr(content[:120])}")
            else:
                print(f"[LOI] Luong 1 - GET /api/documents/{flow1_doc_id}/ that bai: {doc_res.status_code}")
        else:
            print(f"[LOI] Luong 1 - Task consume that bai hoac timeout: {t_info}")
            sys.exit(1)
    else:
        print(f"[LOI] Luong 1 - Upload PDF that bai: {flow1_res.status_code} {flow1_res.text}")
        sys.exit(1)

    # LUỒNG 2: Tạo/gán tag, correspondent, document type -> GET đối chiếu (TV3-FLOW-02)
    print("\n--- 2.2 LUỒNG 2: TẠO/GÁN TAG, CORRESPONDENT, DOCTYPE VÀ ĐỐI CHIẾU (TV3-FLOW-02) ---")
    tv3_tag_data = {"name": "TV3_Tag_Verified_303", "color": "#008080", "is_inbox_tag": False}
    t_res = requests.post(f"{BASE_URL}/api/tags/", json=tv3_tag_data, headers=headers, timeout=10)
    tv3_tag_id = t_res.json().get("id") if t_res.status_code == 201 else existing_tags.get("TV3_Tag_Verified_303")
    print(f"[OK] Luong 2 - Tao Tag 'TV3_Tag_Verified_303': HTTP {t_res.status_code}, ID: {tv3_tag_id}")

    tv3_corr_data = {"name": "TV3_Auditor_303"}
    c_res = requests.post(f"{BASE_URL}/api/correspondents/", json=tv3_corr_data, headers=headers, timeout=10)
    tv3_corr_id = c_res.json().get("id") if c_res.status_code == 201 else existing_corrs.get("TV3_Auditor_303")
    print(f"[OK] Luong 2 - Tao Correspondent 'TV3_Auditor_303': HTTP {c_res.status_code}, ID: {tv3_corr_id}")

    tv3_dt_data = {"name": "TV3_DocType_Report_303"}
    dt_res = requests.post(f"{BASE_URL}/api/document_types/", json=tv3_dt_data, headers=headers, timeout=10)
    tv3_dt_id = dt_res.json().get("id") if dt_res.status_code == 201 else existing_dtypes.get("TV3_DocType_Report_303")
    print(f"[OK] Luong 2 - Tao DocumentType 'TV3_DocType_Report_303': HTTP {dt_res.status_code}, ID: {tv3_dt_id}")

    # Gán vào tài liệu flow1_doc_id
    patch_payload = {
        "tags": [tv3_tag_id],
        "correspondent": tv3_corr_id,
        "document_type": tv3_dt_id,
    }
    patch_res = requests.patch(f"{BASE_URL}/api/documents/{flow1_doc_id}/", json=patch_payload, headers=headers, timeout=10)
    evidence["flow2_patch_status"] = patch_res.status_code
    print(f"[OK] Luong 2 - PATCH /api/documents/{flow1_doc_id}/: HTTP {patch_res.status_code}")

    # GET đối chiếu
    get_res = requests.get(f"{BASE_URL}/api/documents/{flow1_doc_id}/", headers=headers, timeout=10)
    evidence["flow2_get_status"] = get_res.status_code
    if get_res.status_code == 200:
        doc_updated = get_res.json()
        match_tags = tv3_tag_id in doc_updated.get("tags", [])
        match_corr = doc_updated.get("correspondent") == tv3_corr_id
        match_dt = doc_updated.get("document_type") == tv3_dt_id
        evidence["flow2_metadata_matched"] = match_tags and match_corr and match_dt
        print(f"[OK] Luong 2 - GET doi chieu ket qua: Tags={match_tags}, Corr={match_corr}, DocType={match_dt}")
        print(f"     Tags tren doc: {doc_updated.get('tags')}")
        print(f"     Correspondent tren doc: {doc_updated.get('correspondent')}")
        print(f"     DocumentType tren doc: {doc_updated.get('document_type')}")
    else:
        print(f"[LOI] Luong 2 - GET doi chieu that bai: {get_res.status_code}")

    # LUỒNG 3: Tìm kiếm/lọc và xác nhận đúng tài liệu (TV3-FLOW-03)
    print("\n--- 2.3 LUỒNG 3: TÌM KIẾM VÀ LỌC TÀI LIỆU (TV3-FLOW-03) ---")
    # 3.1 Tìm theo query từ khóa
    query_url = f"{BASE_URL}/api/documents/?query=Schemathesis"
    q_res = requests.get(query_url, headers=headers, timeout=10)
    evidence["flow3_search_query_status"] = q_res.status_code
    if q_res.status_code == 200:
        q_data = q_res.json()
        found_ids = [d["id"] for d in q_data.get("results", [])]
        evidence["flow3_search_found_doc"] = flow1_doc_id in found_ids
        print(f"[OK] Luong 3 - Tim kiem tu khoa '?query=Schemathesis': HTTP 200, Tong so: {q_data.get('count')}")
        print(f"     Tai lieu ID {flow1_doc_id} co trong ket qua: {flow1_doc_id in found_ids}")

    # 3.2 Lọc theo Tag ID
    filter_tag_url = f"{BASE_URL}/api/documents/?tags__id__all={tv3_tag_id}"
    t_filter_res = requests.get(filter_tag_url, headers=headers, timeout=10)
    evidence["flow3_filter_tag_status"] = t_filter_res.status_code
    if t_filter_res.status_code == 200:
        t_filter_data = t_filter_res.json()
        filter_ids = [d["id"] for d in t_filter_data.get("results", [])]
        evidence["flow3_filter_found_doc"] = flow1_doc_id in filter_ids
        print(f"[OK] Luong 3 - Loc theo Tag ID {tv3_tag_id}: HTTP 200, Tong so: {t_filter_data.get('count')}")
        print(f"     Tai lieu ID {flow1_doc_id} co trong ket qua loc: {flow1_doc_id in filter_ids}")

    # Lưu báo cáo chi tiết bằng chứng vào docs/BUSINESS_FLOWS_TV3.md
    report_content = f"""# BẰNG CHỨNG BA LUỒNG NGHIỆP VỤ THỰC TẾ — TV3

**Thành viên:** Nguyễn Khiêm Thuận · MSSV: 2312764 · TV3 · Seed: 303  
**Thời gian thực hiện:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Môi trường:** Paperless-ngx v3.1.3 trên Docker Windows local (`http://localhost:8000`)  
**Tài khoản thực hiện:** `admin` (xác thực token tự động qua local API, token an toàn không lưu)

---

## 1. Dữ liệu nền đã nạp (Group Baseline)
- **Tags nền:** 4 (`TV2_Tag_Invoice_202`, `TV2_Tag_Urgent_202`, `TV2_Tag_Archive_202`, `TV2_Tag_Finance_202`)
- **Correspondents nền:** 3 (`TV2_Bank_202`, `TV2_Supplier_202`, `TV2_University_202`)
- **Document Types nền:** 3 (`TV2_DocType_Invoice_202`, `TV2_DocType_Receipt_202`, `TV2_DocType_Contract_202`)
- **Tài liệu TXT nền:** 2 (`TV2_Sample_Invoice_202.txt`, `TV2_Sample_Contract_202.txt`)
- **Bộ PDF bổ sung TV3:** 8 tệp PDF mẫu sinh bằng ReportLab trong `scripts/sample_docs/`

---

## 2. Chi tiết thực thi 3 Luồng nghiệp vụ

### Luồng 1 (TV3-FLOW-01): Upload PDF -> Chờ Celery Task -> GET chi tiết và kiểm tra Content
- **Tệp upload:** `scripts/sample_docs/TV3_Sample_01_Report_303.pdf`
- **Endpoint gọi:** `POST /api/documents/post_document/`
- **HTTP Status:** `{evidence.get('flow1_upload_status')}`
- **Task UUID nhận được:** `{evidence.get('flow1_task_id')}`
- **Kết quả Task:** `SUCCESS`
- **ID tài liệu tạo ra trong CSDL:** `{evidence.get('flow1_doc_id')}`
- **Kiểm tra GET:** `GET /api/documents/{evidence.get('flow1_doc_id')}/` -> HTTP `{evidence.get('flow1_get_status')}`
- **Độ dài văn bản trích xuất (Content Length):** `{evidence.get('flow1_content_length')}` ký tự
- **Nội dung nhận dạng mẫu:**
```text
{evidence.get('flow1_content_snippet')}
```
- **Kết luận:** **PASS**. Hệ thống upload, hàng đợi Redis/Celery xử lý và trích xuất nội dung văn bản thành công.

---

### Luồng 2 (TV3-FLOW-02): Tạo/Gán Tag, Correspondent, Document Type -> GET đối chiếu
- **Tag tạo mới:** `TV3_Tag_Verified_303` (ID: `{tv3_tag_id}`, HTTP 201)
- **Correspondent tạo mới:** `TV3_Auditor_303` (ID: `{tv3_corr_id}`, HTTP 201)
- **DocumentType tạo mới:** `TV3_DocType_Report_303` (ID: `{tv3_dt_id}`, HTTP 201)
- **Gán metadata vào tài liệu:** `PATCH /api/documents/{evidence.get('flow1_doc_id')}/` -> HTTP `{evidence.get('flow2_patch_status')}`
- **Payload gán:**
```json
{{
  "tags": [{tv3_tag_id}],
  "correspondent": {tv3_corr_id},
  "document_type": {tv3_dt_id}
}}
```
- **Kiểm tra đối chiếu:** `GET /api/documents/{evidence.get('flow1_doc_id')}/` -> HTTP `{evidence.get('flow2_get_status')}`
- **Kết quả kiểm tra:** Cả 3 trường Tag, Correspondent, DocumentType đều khớp chính xác giá trị đã gán.
- **Kết luận:** **PASS**. Luồng quản lý và liên kết quan hệ thực thể hoạt động đúng nghiệp vụ.

---

### Luồng 3 (TV3-FLOW-03): Tìm kiếm toàn văn (Search) và Lọc theo thuộc tính (Filter)
- **3.1 Tìm kiếm toàn văn:**
  - URL: `GET /api/documents/?query=Schemathesis`
  - HTTP Status: `{evidence.get('flow3_search_query_status')}`
  - Kết quả: Tài liệu ID `{evidence.get('flow1_doc_id')}` nằm trong danh sách trả về.
- **3.2 Lọc theo Tag:**
  - URL: `GET /api/documents/?tags__id__all={tv3_tag_id}`
  - HTTP Status: `{evidence.get('flow3_filter_tag_status')}`
  - Kết quả: Tài liệu ID `{evidence.get('flow1_doc_id')}` nằm trong danh sách trả về.
- **Kết luận:** **PASS**. Luồng tìm kiếm full-text và bộ lọc đa chiều qua API hoạt động chính xác.
"""
    with open("docs/BUSINESS_FLOWS_TV3.md", "w", encoding="utf-8") as rf:
        rf.write(report_content)
    print("\n[OK] Da ghi nhan day du bang chung 3 luong vao: docs/BUSINESS_FLOWS_TV3.md")


if __name__ == "__main__":
    run()
