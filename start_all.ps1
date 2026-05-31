# Opens 3 terminals: backend, telegram bot, frontend
$root = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-File", "$root\start_backend.ps1"
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-File", "$root\start_bot.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-File", "$root\start_frontend.ps1"
Write-Host "Started backend (8000), Telegram bot, and frontend (5500)." -ForegroundColor Green
Write-Host "Open http://localhost:5500 in your browser." -ForegroundColor Cyan
