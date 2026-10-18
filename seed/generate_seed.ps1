# Sinh lại 6 PDF seed trên PowerShell thuần (không cần Python) — TV1.
# Chạy: powershell -ExecutionPolicy Bypass -File seed/generate_seed.ps1
$docs = @(
  @("seed_01_hoa_don_dien.pdf", "Hoa don tien dien thang 9/2026 - Dien Luc Da Lat - So tien: 452.300 VND - Han thanh toan: 15/10/2026."),
  @("seed_02_hop_dong_dich_vu.pdf", "Hop dong dich vu ve sinh van phong - So HD: DV-2026-041 - Thoi han: 12 thang - Ben cung cap: Cong ty Sach Dep."),
  @("seed_03_bao_cao_tuan.pdf", "Bao cao tuan 41 - Nhom KTPM - Hoan thanh: cai dat moi truong, upload tai lieu mau - Tuan toi: chay Schemathesis vong 1."),
  @("seed_04_bien_ban_hop.pdf", "Bien ban hop nhom ngay 10/10/2026 - Noi dung: chot tag v3.2.1, phan cong 5 thanh vien, lap repo Git chung."),
  @("seed_05_phieu_thu.pdf", "Phieu thu so PT-118 - Nguoi nop: Nguyen Van A - So tien: 2.000.000 VND - Ly do: tam ung van phong pham."),
  @("seed_06_huong_dan_scan.pdf", "Huong dan scan tai lieu - Dinh dang: PDF, toi thieu 300 DPI - Dat ten file theo mau: YYYY-MM-DD-noi-dung.pdf.")
)
function New-SeedPdf($name, $text) {
  $t = $text -replace "\\", "\\" -replace "\(", "\(" -replace "\)", "\)"
  $stream = "BT /F1 14 Tf 72 720 Td 80 TL ($t) Tj ET"
  $len = [System.Text.Encoding]::GetEncoding("iso-8859-1").GetByteCount($stream) + 1
  $objs = @(
    "<< /Type /Catalog /Pages 2 0 R >>",
    "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
    "<< /Length $len >>`nstream`n$stream`nendstream",
    "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
  )
  $enc = [System.Text.Encoding]::GetEncoding("iso-8859-1")
  $out = New-Object System.Collections.Generic.List[byte]
  $out.AddRange($enc.GetBytes("%PDF-1.4`n"))
  $offs = @()
  for ($i = 0; $i -lt $objs.Count; $i++) {
    $offs += $out.Count
    $out.AddRange($enc.GetBytes("$($i+1) 0 obj`n$($objs[$i])`nendobj`n"))
  }
  $xref = $out.Count
  $out.AddRange($enc.GetBytes("xref`n0 $($objs.Count+1)`n0000000000 65535 f `n"))
  foreach ($o in $offs) { $out.AddRange($enc.GetBytes(("{0:D10} 00000 n `n" -f $o))) }
  $out.AddRange($enc.GetBytes("trailer`n<< /Size $($objs.Count+1) /Root 1 0 R >>`nstartxref`n$xref`n%%EOF`n"))
  $dir = Split-Path $PSCommandPath -Parent
  [System.IO.File]::WriteAllBytes((Join-Path $dir $name), $out.ToArray())
  Write-Output "wrote $name ($($out.Count) bytes)"
}
foreach ($d in $docs) { New-SeedPdf $d[0] $d[1] }
