# scripts/run_tv4_tests.ps1
# Script tự động hóa kiểm thử Schemathesis chuẩn hóa 3 vòng cho TV4 (Seed: 404) trên Windows PowerShell.
# Đọc thông tin xác thực từ tệp .env (không hardcode mật khẩu hay in token ra màn hình).

param (
    [int]$Round = 1,
    [int]$MaxExamples = 25
)

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Nạp biến từ .env nếu có
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line.Split("=", 2)
            $k = $parts[0].Trim()
            $v = $parts[1].Trim().Trim('"').Trim("'")
            if (-not [Environment]::GetEnvironmentVariable($k)) {
                [Environment]::SetEnvironmentVariable($k, $v)
            }
        }
    }
}

$SEED = 404
$TV_NAME = "TV4"
$BASE_URL = if ($env:PAPERLESS_URL) { $env:PAPERLESS_URL.TrimEnd("/") } else { "http://localhost:8000" }
$ADMIN_USER = if ($env:PAPERLESS_ADMIN_USER) { $env:PAPERLESS_ADMIN_USER } else { "admin" }
$ADMIN_PASS = if ($env:PAPERLESS_ADMIN_PASSWORD) { $env:PAPERLESS_ADMIN_PASSWORD } else { "admin" }

if (-not (Test-Path "results")) {
    New-Item -ItemType Directory -Path "results" | Out-Null
}

function Get-AuthToken {
    if ($env:PAPERLESS_TOKEN) {
        return $env:PAPERLESS_TOKEN
    }
    Write-Host "[+] Đang xác thực API tại $BASE_URL/api/token/ ..." -ForegroundColor Cyan
    try {
        $body = @{ username = $ADMIN_USER; password = $ADMIN_PASS } | ConvertTo-Json
        $res = Invoke-RestMethod -Uri "$BASE_URL/api/token/" -Method Post -Body $body -ContentType "application/json"
        Write-Host "[OK] Xác thực thành công (Token: <REDACTED_TOKEN>)" -ForegroundColor Green
        return $res.token
    } catch {
        Write-Host "[LỖI] Không thể kết nối hoặc xác thực thất bại." -ForegroundColor Red
        exit 1
    }
}

$token = Get-AuthToken

switch ($Round) {
    1 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "BẮT ĐẦU VÒNG 1 CHUẨN HÓA: GET (19 OPERATIONS) - SEED: $SEED" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow

        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-path-regex '^/api/(tags|correspondents|document_types|documents)/' `
            --exclude-method POST --exclude-method PUT --exclude-method PATCH --exclude-method DELETE `
            --phases examples,fuzzing `
            --checks not_a_server_error,status_code_conformance,content_type_conformance,response_schema_conformance `
            --seed $SEED `
            --max-examples $MaxExamples `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round1_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round1_seed${SEED}.ndjson"

        Write-Host "`n[OK] Hoàn thành Vòng 1 (19 operations)! Kết quả lưu tại results/" -ForegroundColor Green
    }
    2 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "BẮT ĐẦU VÒNG 2 CHUẨN HÓA: CRUD METADATA (18 OPERATIONS) - SEED: $SEED" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow

        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-path-regex '^/api/(tags|correspondents|document_types)/' `
            --checks all `
            --seed $SEED `
            --max-examples $MaxExamples `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round2_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round2_seed${SEED}.ndjson"

        Write-Host "`n[OK] Hoàn thành Vòng 2 (18 operations)! Kết quả lưu tại results/" -ForegroundColor Green
    }
    3 {
        Write-Host "`n=======================================================" -ForegroundColor Yellow
        Write-Host "BẮT ĐẦU VÒNG 3 CHUẨN HÓA: TOÀN DIỆN 4 NHÓM API (53 OPERATIONS) - SEED: $SEED" -ForegroundColor Yellow
        Write-Host "=======================================================" -ForegroundColor Yellow

        .\.venv\Scripts\schemathesis.exe run "$BASE_URL/api/schema/" `
            --url $BASE_URL `
            --header "Authorization: Token $token" `
            --include-path-regex '^/api/(tags|correspondents|document_types|documents)/' `
            --checks all `
            --seed $SEED `
            --max-examples $MaxExamples `
            --report junit,ndjson `
            --report-junit-path "results/${TV_NAME}_round3_seed${SEED}_junit.xml" `
            --report-ndjson-path "results/${TV_NAME}_round3_seed${SEED}.ndjson"

        Write-Host "`n[OK] Hoàn thành Vòng 3 (53 operations)! Kết quả lưu tại results/" -ForegroundColor Green
    }
    default {
        Write-Host "Vòng không hợp lệ. Vui lòng chọn 1, 2, hoặc 3." -ForegroundColor Red
    }
}
