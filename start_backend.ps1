Set-Location $PSScriptRoot
Write-Host "Starting Ilm AI Backend on http://localhost:8000" -ForegroundColor Cyan
& .\venv\Scripts\uvicorn.exe main:app --reload --host 127.0.0.1 --port 8000
