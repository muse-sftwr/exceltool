# 🚀 NASA EXCELTOOLS UNIFIED - COMPLETE LAUNCHER
# PowerShell Script per avvio applicazione completa
# ================================================

param(
    [switch]$Debug,
    [switch]$Test,
    [switch]$Complete
)

# Configurazione
$PROJECT_DIR = Get-Location
$PYTHON_SCRIPT_COMPLETE = "exceltools_unified_complete.py"
$PYTHON_SCRIPT_ORIGINAL = "exceltools_unified.py"
$AI_MODULE = "ai_query_interpreter.py"
$DATABASE_MANAGER = "advanced_database_manager.py"

Write-Host ""
Write-Host "🚀 NASA EXCELTOOLS UNIFIED - COMPLETE LAUNCHER" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Funzione per verificare file
function Test-FileExists {
    param($FilePath, $Description)
    if (Test-Path $FilePath) {
        Write-Host "✅ $Description found: $FilePath" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ $Description missing: $FilePath" -ForegroundColor Red
        return $false
    }
}

# Funzione per test python path
function Test-PythonPath {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Python not found in PATH" -ForegroundColor Red
        return $false
    }
    return $false
}

# Funzione per test pandas
function Test-PandasAvailable {
    try {
        $pandasTest = python -c "import pandas as pd; print(f'Pandas {pd.__version__} available')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $pandasTest" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Pandas not available" -ForegroundColor Red
        return $false
    }
    return $false
}

# Verifica sistema
Write-Host "🔍 SYSTEM CHECK" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow

$pythonOK = Test-PythonPath
$pandasOK = Test-PandasAvailable

# Verifica file
Write-Host ""
Write-Host "📁 FILE CHECK" -ForegroundColor Yellow
Write-Host "===============" -ForegroundColor Yellow

$completeAppOK = Test-FileExists $PYTHON_SCRIPT_COMPLETE "Complete App"
$originalAppOK = Test-FileExists $PYTHON_SCRIPT_ORIGINAL "Original App"
$aiModuleOK = Test-FileExists $AI_MODULE "AI Module"
$dbManagerOK = Test-FileExists $DATABASE_MANAGER "Database Manager"

# Test mode
if ($Test) {
    Write-Host ""
    Write-Host "🧪 RUNNING TESTS" -ForegroundColor Yellow
    Write-Host "=================" -ForegroundColor Yellow

    if (Test-Path "test_nasa_complete.py") {
        Write-Host "▶️ Running complete test suite..." -ForegroundColor Blue
        python test_nasa_complete.py
    } else {
        Write-Host "⚠️ Test file not found, running basic tests" -ForegroundColor Yellow

        # Test AI module
        if ($aiModuleOK) {
            Write-Host "Testing AI module..." -ForegroundColor Blue
            python -c "
from ai_query_interpreter import AdvancedAIQueryInterpreter
ai = AdvancedAIQueryInterpreter()
result = ai.interpret_query('mostra solo la colonna 1')
print('✅ AI Test passed:', result[:50] + '...')
"
        }
    }
    return
}

# Determina quale app lanciare
$appToLaunch = $null
if ($Complete -or $completeAppOK) {
    $appToLaunch = $PYTHON_SCRIPT_COMPLETE
    Write-Host ""
    Write-Host "🚀 LAUNCHING COMPLETE NASA PLATFORM" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
} elseif ($originalAppOK) {
    $appToLaunch = $PYTHON_SCRIPT_ORIGINAL
    Write-Host ""
    Write-Host "🚀 LAUNCHING ORIGINAL APP (FALLBACK)" -ForegroundColor Yellow
    Write-Host "====================================" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ NO VALID APP FOUND!" -ForegroundColor Red
    Write-Host "Please ensure exceltools_unified_complete.py exists" -ForegroundColor Red
    pause
    exit 1
}

# Verifica prerequisiti
if (-not $pythonOK) {
    Write-Host "❌ Python required but not found!" -ForegroundColor Red
    pause
    exit 1
}

if (-not $pandasOK) {
    Write-Host "⚠️ Pandas not available - some features may be limited" -ForegroundColor Yellow
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        exit 1
    }
}

# Debug info
if ($Debug) {
    Write-Host ""
    Write-Host "🔧 DEBUG INFO" -ForegroundColor Magenta
    Write-Host "===============" -ForegroundColor Magenta
    Write-Host "Working Directory: $PROJECT_DIR"
    Write-Host "App to launch: $appToLaunch"
    Write-Host "Python executable: $(where.exe python)"
    Write-Host ""
    Write-Host "Installed packages:"
    python -m pip list | Select-String "pandas|numpy|tkinter|sqlite"
    Write-Host ""
}

# Launch app
try {
    Write-Host ""
    Write-Host "▶️ Starting application..." -ForegroundColor Blue
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
    Write-Host ""

    # Set environment per migliori performance
    $env:PYTHONPATH = $PROJECT_DIR
    $env:PYTHONUNBUFFERED = "1"

    # Avvia app
    python $appToLaunch

} catch {
    Write-Host ""
    Write-Host "❌ Error launching application:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "- Check if all required files exist" -ForegroundColor Yellow
    Write-Host "- Verify Python and pandas installation" -ForegroundColor Yellow
    Write-Host "- Run with -Debug flag for more info" -ForegroundColor Yellow
    Write-Host "- Try running: python -c 'import tkinter; print(\"GUI OK\")'" -ForegroundColor Yellow

} finally {
    Write-Host ""
    Write-Host "🔚 NASA ExcelTools session ended" -ForegroundColor Cyan
    if (-not $Debug) {
        Write-Host "Press any key to continue..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}
