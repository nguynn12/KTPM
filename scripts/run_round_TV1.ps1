# Wrapper chạy 1 vòng Schemathesis cho TV1 — dùng venv của repo (D:\KTPM\.venv).
# Ví dụ: powershell -ExecutionPolicy Bypass -File scripts\run_round_TV1.ps1 -Round 1
param(
  [Parameter(Mandatory = $true)][ValidateRange(1, 3)][int]$Round,
  [int]$MaxExamples = 25
)

$root = Split-Path $PSScriptRoot -Parent
$py = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
  Write-Output "Chua co venv tai $py"
  Write-Output "Tao bang: python -m venv `"$root\.venv`" ; `"$py`" -m pip install `"schemathesis==4.30.1`""
  exit 1
}

$runner = Join-Path $PSScriptRoot "run_round_TV1.py"
& $py $runner --round $Round --max-examples $MaxExamples
exit $LASTEXITCODE
