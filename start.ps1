# Detener servidor anterior
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

Start-Sleep 2

# Iniciar servidor
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Start-Process -WorkingDirectory "$PSScriptRoot\backend" -FilePath "python" -ArgumentList "main.py" -NoNewWindow

Start-Sleep 4

Write-Host "============================================"
Write-Host "  CRM Inteligente corriendo en:"
Write-Host "  http://localhost:8000"
Write-Host "============================================"
Write-Host ""
Write-Host "Presiona cualquier tecla para abrir el navegador..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:8000"
