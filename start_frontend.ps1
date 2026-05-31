Set-Location "C:\Users\Larry\ilm-ai-frontend"
Write-Host "Starting frontend at http://localhost:5500" -ForegroundColor Cyan
& python -m http.server 5500
