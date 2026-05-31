Set-Location $PSScriptRoot
Write-Host "Starting Ilm AI Telegram Bot..." -ForegroundColor Cyan
& .\venv\Scripts\python.exe run_telegram_bot.py
