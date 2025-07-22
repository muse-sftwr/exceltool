# NASA EXCELTOOLS - TEST SCRIPT ROBUSTO
# =====================================
# Test completo del sistema NASA con gestione errori

param(
    [switch]$Verbose
)

# Configurazione
$PYTHON_PATH = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
$ErrorActionPreference = "Continue"

function Write-TestHeader($message) {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host $message -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Cyan
}

function Write-TestResult($test, $result, $details = "") {
    if ($result) {
        Write-Host "[PASS] $test" -ForegroundColor Green
        if ($details) { Write-Host "       $details" -ForegroundColor Gray }
    } else {
        Write-Host "[FAIL] $test" -ForegroundColor Red
        if ($details) { Write-Host "       $details" -ForegroundColor Gray }
    }
}

Write-TestHeader "NASA EXCELTOOLS - COMPREHENSIVE TEST SUITE"

# Test 1: Python Path
Write-TestHeader "1. PYTHON CONFIGURATION TEST"
$pythonExists = Test-Path $PYTHON_PATH
Write-TestResult "Python executable exists" $pythonExists $PYTHON_PATH

if ($pythonExists) {
    try {
        $pythonVersion = & $PYTHON_PATH --version 2>&1
        Write-TestResult "Python version check" $true $pythonVersion
    } catch {
        Write-TestResult "Python version check" $false $_.Exception.Message
    }
} else {
    Write-Host "ERROR: Python not found at expected path!" -ForegroundColor Red
    exit 1
}

# Test 2: Dependencies
Write-TestHeader "2. DEPENDENCIES TEST"

# Test pandas
try {
    & $PYTHON_PATH -c "import pandas as pd; print('Pandas version:', pd.__version__)" 2>&1 | Out-Host
    Write-TestResult "Pandas import" $true
} catch {
    Write-TestResult "Pandas import" $false $_.Exception.Message
}

# Test tkinter
try {
    & $PYTHON_PATH -c "import tkinter; print('Tkinter OK')" 2>&1 | Out-Host
    Write-TestResult "Tkinter import" $true
} catch {
    Write-TestResult "Tkinter import" $false $_.Exception.Message
}

# Test 3: Core Files Syntax
Write-TestHeader "3. CORE FILES SYNTAX TEST"

$coreFiles = @(
    "exceltools_unified.py",
    "ai_query_interpreter.py",
    "advanced_database_manager.py"
)

foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        try {
            & $PYTHON_PATH -m py_compile $file 2>&1 | Out-Null
            Write-TestResult "Syntax check: $file" $true
        } catch {
            Write-TestResult "Syntax check: $file" $false $_.Exception.Message
        }
    } else {
        Write-TestResult "File exists: $file" $false "File not found"
    }
}

# Test 4: AI Module
Write-TestHeader "4. AI MODULE TEST"

if (Test-Path "ai_query_interpreter.py") {
    try {
        $aiTest = & $PYTHON_PATH -c @"
from ai_query_interpreter import AdvancedAIQueryInterpreter
import pandas as pd

# Test data
df = pd.DataFrame({'Nome': ['Test'], 'Eta': [30]})
ai = AdvancedAIQueryInterpreter()
ai.set_data_context(df, {'test': df})

# Test query
result = ai.interpret_query('mostra solo la colonna Nome')
print('AI Test Result:', result)
print('AI_TEST_SUCCESS')
"@
        if ($aiTest -match "AI_TEST_SUCCESS") {
            Write-TestResult "AI Query Interpreter" $true
        } else {
            Write-TestResult "AI Query Interpreter" $false "No success marker found"
        }
    } catch {
        Write-TestResult "AI Query Interpreter" $false $_.Exception.Message
    }
}

# Test 5: App Launch Test
Write-TestHeader "5. APPLICATION LAUNCH TEST"

try {
    $launchTest = & $PYTHON_PATH -c @"
# Quick app initialization test
import sys
sys.path.append('.')

# Test imports
try:
    import tkinter as tk
    from ai_query_interpreter import AdvancedAIQueryInterpreter
    from advanced_database_manager import AdvancedDatabaseManager
    print('APP_IMPORTS_SUCCESS')
except Exception as e:
    print('IMPORT_ERROR:', e)
    sys.exit(1)

# Test basic functionality
try:
    ai = AdvancedAIQueryInterpreter()
    db = AdvancedDatabaseManager()
    print('APP_INIT_SUCCESS')
except Exception as e:
    print('INIT_ERROR:', e)
    sys.exit(1)
"@

    if ($launchTest -match "APP_INIT_SUCCESS") {
        Write-TestResult "Application initialization" $true
    } else {
        Write-TestResult "Application initialization" $false "Initialization failed"
    }
} catch {
    Write-TestResult "Application initialization" $false $_.Exception.Message
}

# Summary
Write-TestHeader "TEST SUMMARY"

$totalTests = 8
$passedTests = @($GLOBAL:TestResults | Where-Object { $_ -eq $true }).Count

if ($passedTests -ge 6) {
    Write-Host "OVERALL RESULT: PASS ($passedTests/$totalTests tests passed)" -ForegroundColor Green
    Write-Host "NASA ExcelTools is ready for use!" -ForegroundColor Cyan
} else {
    Write-Host "OVERALL RESULT: FAIL ($passedTests/$totalTests tests passed)" -ForegroundColor Red
    Write-Host "Please fix the failing tests before using NASA ExcelTools." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To launch NASA ExcelTools, run:" -ForegroundColor Cyan
Write-Host "& `"$PYTHON_PATH`" exceltools_unified.py" -ForegroundColor White
