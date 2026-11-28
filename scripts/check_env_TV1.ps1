# Kiem tra moi truong truoc khi cai (chay 1 lenh) — TV1
# PowerShell: powershell -ExecutionPolicy Bypass -File scripts/check_env_TV1.ps1
# Bash/WSL:  bash scripts/check_env_TV1.sh
Write-Output "=== TV1 env check ==="

function Write-Check([string]$Name, [bool]$Ok, [string]$Detail) {
  if ($Ok) { $tag = "[OK]  " } else { $tag = "[WARN]" }
  Write-Output ("{0} {1}: {2}" -f $tag, $Name, $Detail)
}

$os = (Get-CimInstance Win32_OperatingSystem).Caption
Write-Output ("OS: {0}" -f $os)

try {
  $dockerVersion = (docker --version 2>&1 | Out-String).Trim()
  Write-Check "Docker" ($LASTEXITCODE -eq 0) $dockerVersion
} catch {
  Write-Check "Docker" $false "THIEU Docker"
}

try {
  $composeVersion = (docker compose version 2>&1 | Out-String).Trim()
  Write-Check "Docker Compose" ($LASTEXITCODE -eq 0) $composeVersion
} catch {
  Write-Check "Docker Compose" $false "THIEU Docker Compose"
}

docker info 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  Write-Check "Docker daemon" $true "RUNNING"
} else {
  Write-Check "Docker daemon" $false "CHUA CHAY -> mo Docker Desktop len"
}

$py13 = $null
try {
  $py13 = (py -3.13 --version 2>&1 | Out-String).Trim()
} catch { }
if ($LASTEXITCODE -eq 0 -and $py13) {
  Write-Check "Python 3.13" $true $py13
} else {
  Write-Check "Python 3.13" $false "CHUA CO -> winget install -e --id Python.Python.3.13"
}

try {
  $pyDefault = (python --version 2>&1 | Out-String).Trim()
  if ($LASTEXITCODE -eq 0 -and $pyDefault) { Write-Output ("INFO  Python mac dinh: {0}" -f $pyDefault) }
} catch { }

$venvPy = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$venvSt = Join-Path $PSScriptRoot "..\.venv\Scripts\schemathesis.exe"
if (Test-Path $venvPy) {
  Write-Check "venv" $true (Resolve-Path $venvPy)
} else {
  Write-Check "venv" $false "CHUA CO -> py -3.13 -m venv .venv"
}

if (Test-Path $venvSt) {
  $stVersion = (& $venvSt --version 2>&1 | Out-String).Trim()
  Write-Check "Schemathesis (venv)" $true $stVersion
} elseif (Get-Command schemathesis -ErrorAction SilentlyContinue) {
  $stVersion = (schemathesis --version 2>&1 | Out-String).Trim()
  Write-Check "Schemathesis (PATH)" $true $stVersion
} else {
  Write-Check "Schemathesis" $false "CHUA CAI -> pip install `"schemathesis==4.30.1`""
}

foreach ($letter in @("C", "D")) {
  if (Test-Path "${letter}:\") {
    $free = [math]::Round((Get-PSDrive $letter).Free / 1GB, 1)
    Write-Check ("O dia {0} trong" -f $letter) ($free -ge 10) ("{0} GB (can >= 10 GB)" -f $free)
  }
}

$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
Write-Check "RAM" ($ram -ge 8) ("{0} GB (can >= 8 GB)" -f $ram)

$port = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($port) {
  Write-Check "Port 8000" $false "DANG BI CHIEM -> doi ports + PAPERLESS_URL hoac dung port khac"
} else {
  Write-Check "Port 8000" $true "FREE"
}
