# PYTHON PATH CONFIGURATOR
# ==============================
# Configurazione permanente Python per ExcelTools NASA

$PYTHON_PATH = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"

# Test Python
Write-Host "Testing Python..." -ForegroundColor Green
& $PYTHON_PATH --version

# Set alias per questa sessione
Set-Alias -Name python -Value $PYTHON_PATH

Write-Host "Python configurato correttamente!" -ForegroundColor Green
Write-Host "Path: $PYTHON_PATH" -ForegroundColor Yellow

# Test import pandas
Write-Host "Testing pandas..." -ForegroundColor Green
& $PYTHON_PATH -c "import pandas as pd; print('Pandas version:', pd.__version__)"

Write-Host "Sistema pronto per ExcelTools NASA!" -ForegroundColor Cyan
