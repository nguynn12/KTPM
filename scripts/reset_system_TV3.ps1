# scripts/reset_system_TV3.ps1
# Script khôi phục toàn bộ hệ thống Paperless-ngx về baseline sạch bằng Docker Volumes
# Tác giả: Nguyễn Khiêm Thuận - MSSV 2312764 - TV3 - Seed 303
# Có cơ chế xác nhận an toàn, kiểm tra endpoint chính xác, tự động seed lại và xác nhận baseline.

param (
    [switch]$Force = $false
)

Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "=== QUY TRÌNH RESET TOÀN BỘ HỆ THỐNG VÀ DỮ LIỆU BẰNG DOCKER VOLUMES ===" -ForegroundColor Yellow
Write-Host "=== Tác giả: Nguyễn Khiêm Thuận - MSSV: 2312764 - TV3 - Seed: 303  ===" -ForegroundColor Yellow
Write-Host "======================================================================`n" -ForegroundColor Yellow

if (-not $Force) {
    $confirm = Read-Host "CẢNH BÁO: Thao tác này sẽ xóa toàn bộ database và volumes Docker (down -v). Bạn có chắc chắn muốn tiếp tục? (Y/N)"
    if ($confirm -ne 'Y' -and $confirm -ne 'y') {
        Write-Host "[HỦY BỎ] Đã dừng quy trình reset theo yêu cầu người dùng." -ForegroundColor Red
        exit 0
    }
}

Write-Host "`n[1/5] Đang dừng và xóa toàn bộ volumes cũ..." -ForegroundColor Cyan
docker compose down -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "[LỖI] Lệnh docker compose down -v thất bại!" -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/5] Đang khởi động lại cụm container..." -ForegroundColor Cyan
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[LỖI] Lệnh docker compose up -d thất bại!" -ForegroundColor Red
    exit 1
}

Write-Host "`n[3/5] Đang kiểm tra webserver sẵn sàng (tối đa 90 giây)..." -ForegroundColor Cyan
$ready = $false
for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 3
    try {
        $res = Invoke-WebRequest -Uri "http://localhost:8000/api/" -Method Get -TimeoutSec 3 -SkipHttpErrorCheck -ErrorAction SilentlyContinue
        # Chấp nhận mã 200 hoặc 401/403 vì webserver Django đã phản hồi
        if ($res.StatusCode -in 200, 301, 302, 401, 403) {
            $ready = $true
            break
        }
    } catch {
        # Tiếp tục chờ
    }
    Write-Host "." -NoNewline
}

if (-not $ready) {
    Write-Host "`n[LỖI NGHIÊM TRỌNG] Webserver chưa sẵn sàng sau 90 giây. Dừng quy trình để kiểm tra docker logs." -ForegroundColor Red
    exit 1
}

Write-Host "`n[OK] Webserver đã sẵn sàng phục vụ HTTP." -ForegroundColor Green

Write-Host "`n[4/5] Chờ tài khoản admin và seed lại dữ liệu nền (kèm xác thực 3 luồng)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

& .\.venv\Scripts\python.exe -u scripts/seed_and_verify_flows_TV3.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[LỖI] Seed dữ liệu nền thất bại!" -ForegroundColor Red
    exit 1
}

Write-Host "`n[5/5] Đã khôi phục baseline thành công và sẵn sàng cho vòng chạy tiếp theo!" -ForegroundColor Green
