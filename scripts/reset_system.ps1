# scripts/reset_system.ps1
# Script khoi phuc toan bo he thong ve trang thai sach bang Docker Volumes
Write-Host "=== DANG KHOI DONG LAI HE THONG PAPERLESS-NGX (RESET VOLUMES) ===" -ForegroundColor Yellow

docker compose down -v
docker compose up -d

Write-Host "Dang cho webserver khoi dong va hoan tat migration..." -ForegroundColor Cyan
$ready = $false
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 3
    try {
        $res = Invoke-WebRequest -Uri "http://localhost:8000/api/" -Method Get -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($res.StatusCode -in 200, 302) {
            $ready = $true
            break
        }
    } catch {
        # tiep tuc cho
    }
    Write-Host "." -NoNewline
}

if ($ready) {
    Write-Host "`n[OK] He thong da san sang tren http://localhost:8000" -ForegroundColor Green
} else {
    Write-Host "`n[CANH BAO] Webserver chua phan hoi sau 3 phut. Kiem tra 'docker compose logs'." -ForegroundColor Red
}
