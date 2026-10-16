# scripts/open_reproduce_windows.ps1
# Script ho tro mo man hinh thuc thi that tren Windows cho TV3 (Nguyen Khiem Thuan - MSSV 2312764)
# Phuc vu xem truc tiep va chup man hinh thu cong (Win + Shift + S) theo yeu cau nhom truong

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "   TV3 (Nguyen Khiem Thuan - 2312764 - Seed 303): MAN HINH TAI HIEN LOI   " -ForegroundColor Yellow
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/3] Dang lay token xac thuc tu Paperless-ngx (http://localhost:8000)..." -ForegroundColor Gray

$tokenRes = Invoke-RestMethod -Uri "http://localhost:8000/api/token/" -Method Post -ContentType "application/json" -Body '{"username":"admin","password":"admin"}' -ErrorAction SilentlyContinue
if (-not $tokenRes.token) {
    Write-Host "[LOI] Khong the ket noi toi http://localhost:8000/api/token/. Hay dam bao Docker dang chay." -ForegroundColor Red
    pause
    exit
}
$token = $tokenRes.token
$maskedToken = $token.Substring(0, 4) + "..." + $token.Substring($token.Length - 4)
Write-Host "  -> Da xac thuc thanh cong. Token phien: $maskedToken (che an toan khi chup)." -ForegroundColor Green
Write-Host ""

# --- BUG-01 TAI HIEN ---
Write-Host "--------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "[BANG CHUNG 1] BUG-01: POST /api/correspondents/ voi set_permissions.view = false" -ForegroundColor Magenta
Write-Host "Lenh thuc thi:" -ForegroundColor Gray
Write-Host "curl.exe -i -X POST http://localhost:8000/api/correspondents/ -H `"Authorization: Token [REDACTED_AUTH_TOKEN]`" -H `"Content-Type: application/json`" -d `"{\`"name\`": \`"TV3_Manual_Capture_Cor\`", \`"set_permissions\`": {\`"view\`": false}}`"" -ForegroundColor White
Write-Host ""
Write-Host "Ket qua phan hoi thuc te tu may chu:" -ForegroundColor Yellow
curl.exe -i -s -X POST "http://localhost:8000/api/correspondents/" -H "Authorization: Token $token" -H "Content-Type: application/json" -d "{\`"name\`": \`"TV3_Manual_Capture_Cor\`", \`"set_permissions\`": {\`"view\`": false}}"
Write-Host ""

Write-Host "--------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "[BANG CHUNG 2] BUG-01: POST /api/document_types/ voi set_permissions.view = false" -ForegroundColor Magenta
Write-Host "Lenh thuc thi:" -ForegroundColor Gray
Write-Host "curl.exe -i -X POST http://localhost:8000/api/document_types/ -H `"Authorization: Token [REDACTED_AUTH_TOKEN]`" -H `"Content-Type: application/json`" -d `"{\`"name\`": \`"TV3_Manual_Capture_DT\`", \`"set_permissions\`": {\`"view\`": false}}`"" -ForegroundColor White
Write-Host ""
Write-Host "Ket qua phan hoi thuc te tu may chu:" -ForegroundColor Yellow
curl.exe -i -s -X POST "http://localhost:8000/api/document_types/" -H "Authorization: Token $token" -H "Content-Type: application/json" -d "{\`"name\`": \`"TV3_Manual_Capture_DT\`", \`"set_permissions\`": {\`"view\`": false}}"
Write-Host ""

# --- BUG-03 TAI HIEN ---
Write-Host "--------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "[BANG CHUNG 3] BUG-03: POST /api/correspondents/ tra 201 nhung thieu truong required" -ForegroundColor Magenta
Write-Host "Lenh thuc thi:" -ForegroundColor Gray
Write-Host "curl.exe -i -X POST http://localhost:8000/api/correspondents/ -H `"Authorization: Token [REDACTED_AUTH_TOKEN]`" -H `"Content-Type: application/json`" -d `"{\`"name\`": \`"TV3_Manual_Capture_201\`"}`"" -ForegroundColor White
Write-Host ""
Write-Host "Ket qua phan hoi thuc te tu may chu:" -ForegroundColor Yellow
$corRes = curl.exe -i -s -X POST "http://localhost:8000/api/correspondents/" -H "Authorization: Token $token" -H "Content-Type: application/json" -d "{\`"name\`": \`"TV3_Manual_Capture_201\`"}"
$corRes
Write-Host ""
Write-Host "-> Doi chieu schema: Thieu 3 truong required (document_count, last_correspondence, permissions)." -ForegroundColor Red

# Don dep ban ghi tam
$cleanMatch = $corRes | Select-String -Pattern '"id":(\d+)'
if ($cleanMatch) {
    $tempId = $cleanMatch.Matches[0].Groups[1].Value
    Invoke-RestMethod -Uri "http://localhost:8000/api/correspondents/$tempId/" -Method Delete -Headers @{"Authorization" = "Token $token"} -ErrorAction SilentlyContinue | Out-Null
    Write-Host "-> Da don dep ID tam $tempId tren he thong." -ForegroundColor Gray
}

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "Ban co the nhan Win + Shift + S de chup vung cua so terminal nay lam minh chung!" -ForegroundColor Green
Write-Host "Mo Swagger UI tren trinh duyet de chup schema doi chieu? (Y/N)" -ForegroundColor Yellow
$ans = Read-Host
if ($ans -eq "Y" -or $ans -eq "y") {
    Start-Process "http://localhost:8000/api/schema/swagger-ui/#/correspondents/correspondents_create"
}
