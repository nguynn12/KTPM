# scripts/run_tv4_tests.ps1
# Script tự động hóa kiểm thử Schemathesis cho TV4 (Seed: 404) trên Windows PowerShell (Tối ưu tốc độ cao)

param (
    [int]$Round = 1,
    [int]$MaxExamples = 20
)

# Cấu hình encoding UTF-8 để Click / Schemathesis không bị lỗi charmap trên Windows
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$SEED = 404
$TV_NAME = "TV4"
$BASE_URL = "http://localhost:8000"

# Đảm bảo thư mục results tồn tại
if (-not (Test-Path "results")) {
    New-Item -ItemType Directory -Path "results" | Out-Null
}

function Get-AuthToken {
    Write-Host "[+] Đang lấy Token xác thực từ $BASE_URL/api/token/ ..." -ForegroundColor Cyan
    try {
        $body = @{ username = "admin"; password = "admin" } | ConvertTo-Json
        $res = Invoke-RestMethod -Uri "$BASE_URL/api/token/" -Method Post -Body $body -ContentType "application/json"
        Write-Host "[OK] Đã lấy Token thành công!" -ForegroundColor Green
        return $res.token
    } catch {
        Write-Host "[LỖI] Không thể kết nối hoặc sai tài khoản: $_" -ForegroundColor Red
        exit 1
    }
}

$token = Get-AuthToken

switch ($Round) {
    1 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "🚀 BẮT ĐẦU VÒNG 1: GET (CHỈ ĐỌC) - SEED: $SEED (Max Examples: $MaxExamples)" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow
        
        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-method GET `
            --seed $SEED `
            --max-examples $MaxExamples `
            --no-shrink `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round1_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round1_seed${SEED}.ndjson"
            
        Write-Host "`n✅ Hoàn thành Vòng 1! Kết quả đã lưu vào thư mục results/" -ForegroundColor Green
    }
    2 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "🚀 BẮT ĐẦU VÒNG 2: GHI DỮ LIỆU (POST/PATCH/PUT/DELETE) - SEED: $SEED (Tối ưu tốc độ cao)" -ForegroundColor Yellow
        Write-Host "Phạm vi: tags, correspondents, document_types (Max Examples: $MaxExamples, No-shrink)" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow
        
        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-path-regex '^/api/(tags|correspondents|document_types)/' `
            --seed $SEED `
            --max-examples $MaxExamples `
            --no-shrink `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round2_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round2_seed${SEED}.ndjson"
            
        Write-Host "`n✅ Hoàn thành Vòng 2! Kết quả đã lưu vào thư mục results/" -ForegroundColor Green
    }
    3 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "🚀 BẮT ĐẦU VÒNG 3: MỞ RỘNG (THÊM DOCUMENTS & TOÀN BỘ CHECKS) - SEED: $SEED" -ForegroundColor Yellow
        Write-Host "Phạm vi: tags, correspondents, document_types, documents + --checks all (Max Examples: $MaxExamples)" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow
        
        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-path-regex '^/api/(tags|correspondents|document_types|documents)/' `
            --checks all `
            --seed $SEED `
            --max-examples $MaxExamples `
            --no-shrink `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round3_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round3_seed${SEED}.ndjson"
            
        Write-Host "`n✅ Hoàn thành Vòng 3! Kết quả đã lưu vào thư mục results/" -ForegroundColor Green
    }
    default {
        Write-Host "Vòng không hợp lệ. Vui lòng chọn 1, 2, hoặc 3." -ForegroundColor Red
    }
}
