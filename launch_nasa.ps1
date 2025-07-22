# NASA EXCELTOOLS - LAUNCHER DEFINITIVO
# =====================================
# Launcher robusto per ExcelTools NASA

$PYTHON_PATH = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"

Write-Host ""
Write-Host "NASA EXCELTOOLS LAUNCHER" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
if (-not (Test-Path $PYTHON_PATH)) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Expected path: $PYTHON_PATH" -ForegroundColor Yellow
    pause
    exit 1
}

# Mostra versione Python
Write-Host "Python version:" -ForegroundColor Green
& $PYTHON_PATH --version

Write-Host ""
Write-Host "Launching NASA ExcelTools Unified..." -ForegroundColor Yellow

# Avvia l'applicazione
try {
    & $PYTHON_PATH exceltools_unified.py
} catch {
    Write-Host "ERROR launching application: $($_.Exception.Message)" -ForegroundColor Red
    pause
}
