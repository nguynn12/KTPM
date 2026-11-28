# Chuẩn lệnh TV3 — Schemathesis 4.30.1

Chạy ở gốc KTPM trên PowerShell sau khi Docker, dữ liệu nền và token đã sẵn sàng. Các lệnh dưới đây đã đối chiếu --help bản 4.30.1; chưa được chạy với Paperless ở môi trường chuẩn bị. Tệp TV3 không phải kết quả TV2.

## Cài môi trường
```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "schemathesis==4.30.1" requests reportlab
.\.venv\Scripts\schemathesis.exe --version
.\.venv\Scripts\schemathesis.exe run --help
New-Item -ItemType Directory -Force results | Out-Null
$env:PYTHONIOENCODING = "utf-8"
```
Python phải >=3.10. Gọi thẳng executable trong .venv giúp tránh lỗi ExecutionPolicy khi activate.

## Lấy token mà không in lên màn hình
```powershell
$cred = Get-Credential -UserName admin -Message "Nhap tai khoan Paperless local"
$login = @{ username=$cred.UserName; password=$cred.GetNetworkCredential().Password } | ConvertTo-Json
$auth = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/token/" -ContentType "application/json" -Body $login
$token = $auth.token
Remove-Variable login, auth, cred
if (!$token) { throw "Khong lay duoc token" }
```
Không chạy `$token` riêng để in giá trị. Nếu Antigravity có thể chạy Python lấy token và truyền cho CLI kín thì ưu tiên cách đó.

## Tạo tham số và tên log cho mỗi vòng
Sửa `$round` thành 1, 2 hoặc 3. Trước vòng 2/3 phải reset, seed và xác nhận baseline. Đoạn này KHÔNG reset hoặc xóa dữ liệu.

```powershell
$round = 1
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$prefix = "results/TV3_round${round}_seed303_${stamp}"
$scope = if ($round -eq 2) { '^/api/(tags|correspondents|document_types)/' } else { '^/api/(tags|correspondents|document_types|documents)/' }
$stArgs = @(
    'run', 'http://localhost:8000/api/schema/',
    '--url', 'http://localhost:8000',
    '--include-path-regex', $scope,
    '--seed', '303', '--max-examples', '25', '--workers', '1',
    '--mode', 'all', '--header', "Authorization: Token $token",
    '--report', 'junit,ndjson',
    '--report-junit-path', "${prefix}.xml",
    '--report-ndjson-path', "${prefix}.ndjson",
    '--output-sanitize', 'true', '--no-color'
)
if ($round -eq 1) {
    $stArgs += @('--include-method','GET','--phases','examples,fuzzing','--checks','not_a_server_error,status_code_conformance,content_type_conformance,response_headers_conformance,response_schema_conformance')
} else {
    $stArgs += @('--checks','all')
}
& .\.venv\Scripts\schemathesis.exe @stArgs 2>&1 | Tee-Object -FilePath "${prefix}.log"
$runExit = $LASTEXITCODE
Write-Host "CLI exit code: $runExit"
```

Không in `$stArgs` nguyên vẹn vì nó chứa token. Kiểm tra log không có token trước khi chia sẻ. Nếu cần giới hạn thời gian, thống nhất và ghi flag vào summary; không thay đổi âm thầm giữa các lượt. max-examples 25 là tham số sinh, không được dùng làm tổng số request thực tế.

## Đọc kết quả
- Giữ mã thoát: test có failure vẫn có giá trị báo cáo; lỗi CLI/schema/auth phải phân loại riêng.
- Ghi operations được chọn từ LoadingFinished.statistic.operations.selected, thời gian từ EngineFinished.running_time nếu có. Chỉ dùng đúng metric công cụ thực sự in.
- Không đếm dòng NDJSON hoặc phần tử JUnit testcase thành số generated cases. Dùng phần summary của CLI/định dạng report phù hợp; thiếu thì ghi không có trong output.
- Ghi đủ phases/checks. TV2 vòng 1 dùng phạm vi rộng hơn, vì vậy số liệu không so trực tiếp như cùng một test suite.
- .gitignore repo đang bỏ qua *.log. Muốn commit log đã làm sạch, thêm ngoại lệ `!results/TV3_*.log` sau dòng bỏ qua hoặc stage riêng file sạch bằng `git add -f results/<ten>.log`; không bỏ qua bước rà bí mật.

## Những lệnh không nên chạy máy móc
- Không dùng --hypothesis-seed / --method từ ví dụ phiên bản cũ.
- Không dùng docker compose down -v ngoài quy trình reset đã được xác nhận.
- Không dùng token trong script cũ. Không chạy tạo admin lặp lại khi auto-admin đã thành công.
- Khi clone mới, dùng git clone; git pull chỉ dùng trong repo đã có.
