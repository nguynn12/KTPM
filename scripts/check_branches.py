import subprocess

branches = ['origin/TV1_TranGiaHuy', 'origin/TV2_TaNhatNguyen', 'origin/TV3_KhiemThuan', 'origin/TV4_NguyenNhatMinh', 'origin/TV5_TranQuocKhanh', 'origin/master']
keywords = ['quan hệ dữ liệu', 'sơ đồ quan hệ', 'erd', 'hình 2', 'hinh 2', 'hinh_2']

print("BẮT ĐẦU QUÉT TẤT CẢ CÁC NHÁNH...")
for b in branches:
    print(f"\n==================== {b} ====================")
    found_any = False
    for kw in keywords:
        cmd = ['git', 'grep', '-i', kw, b]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        lines = [l for l in p.stdout.splitlines() if l.strip()]
        if lines:
            found_any = True
            print(f"  [Từ khóa '{kw}'] - {len(lines)} kết quả:")
            for l in lines[:4]:
                print(f"    {l[:130]}")
    if not found_any:
        print("  -> Không tìm thấy tài liệu hay sơ đồ nào liên quan.")

# Kiểm tra các tệp ảnh trên tất cả các nhánh
print("\n==================== TẤT CẢ FILE ẢNH/ĐỒ HỌA TRÊN MỌI NHÁNH ====================")
p = subprocess.run(['git', 'log', '--all', '--name-only', '--oneline', '--diff-filter=A', '--', '*.png', '*.jpg', '*.svg', '*.puml'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
for l in p.stdout.splitlines():
    if any(ext in l.lower() for ext in ['.png', '.jpg', '.svg', '.puml']):
        print("  " + l)
