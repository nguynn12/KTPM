# Kiểm tra môi trường trước khi cài (chạy 1 lệnh) — TV1
# PowerShell: powershell -ExecutionPolicy Bypass -File scripts/check_env.ps1
# Bash/WSL:  bash scripts/check_env.sh
Write-Output "=== TV1 env check ==="
try { docker --version } catch { Write-Output "THIEU Docker" }
try { docker compose version } catch { Write-Output "THIEU Docker Compose" }
try {
  docker info 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { Write-Output "Docker daemon: RUNNING" }
  else { Write-Output "Docker daemon: CHUA CHAY -> mo Docker Desktop len" }
} catch { Write-Output "Docker daemon: CHUA CHAY" }
try { python3 --version } catch { Write-Output "Python3: CHUA CO (can de chay Schemathesis + seed_api.py)" }
try { schemathesis --version } catch { Write-Output "Schemathesis: CHUA CAI (pip install schemathesis==4.30.0)" }
$free = (Get-PSDrive C).Free / 1GB
Write-Output ("O dia C trong: {0:N1} GB (can >= 10 GB)" -f $free)
$ram = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
Write-Output ("RAM: {0:N1} GB (can >= 8 GB)" -f $ram)
