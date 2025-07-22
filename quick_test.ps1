# QUICK TEST NASA EXCELTOOLS
# ==========================

$PYTHON_PATH = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"

Write-Host "QUICK NASA EXCELTOOLS TEST" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# Test 1: Python
Write-Host "`n1. Testing Python..." -ForegroundColor Yellow
& $PYTHON_PATH --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [PASS] Python OK" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] Python ERROR" -ForegroundColor Red
}

# Test 2: Pandas
Write-Host "`n2. Testing Pandas..." -ForegroundColor Yellow
& $PYTHON_PATH -c "import pandas as pd; print('   Pandas version:', pd.__version__)"
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [PASS] Pandas OK" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] Pandas ERROR" -ForegroundColor Red
}

# Test 3: Core files
Write-Host "`n3. Testing Core Files..." -ForegroundColor Yellow
$files = @("exceltools_unified.py", "ai_query_interpreter.py", "advanced_database_manager.py")
$allGood = $true

foreach ($file in $files) {
    if (Test-Path $file) {
        & $PYTHON_PATH -m py_compile $file 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   [PASS] $file" -ForegroundColor Green
        } else {
            Write-Host "   [FAIL] $file - Syntax Error" -ForegroundColor Red
            $allGood = $false
        }
    } else {
        Write-Host "   [FAIL] $file - Not Found" -ForegroundColor Red
        $allGood = $false
    }
}

# Test 4: AI Test
Write-Host "`n4. Testing AI..." -ForegroundColor Yellow
& $PYTHON_PATH test_nasa_complete.py 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [PASS] AI Test OK" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] AI Test ERROR" -ForegroundColor Red
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "RESULT: " -ForegroundColor Cyan -NoNewline
if ($allGood) {
    Write-Host "SISTEMA PRONTO!" -ForegroundColor Green
    Write-Host "`nPer avviare NASA ExcelTools:" -ForegroundColor Cyan
    Write-Host "   ./launch_nasa.ps1" -ForegroundColor White
} else {
    Write-Host "ERRORI RILEVATI" -ForegroundColor Red
    Write-Host "Controlla i file sopra indicati" -ForegroundColor Yellow
}
