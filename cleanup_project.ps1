# EXCELTOOLS NASA - CLEANUP SCRIPT
# =================================
# Rimuove tutti i file obsoleti e mantiene solo quelli essenziali

Write-Host "Starting NASA ExcelTools Cleanup..." -ForegroundColor Yellow

# File ESSENZIALI da MANTENERE
$ESSENTIAL_FILES = @(
    "exceltools_unified.py",           # APP PRINCIPALE
    "ai_query_interpreter.py",         # MODULO AI
    "advanced_database_manager.py",    # DATABASE MANAGER
    "setup_python.ps1",               # CONFIGURAZIONE PYTHON
    "README.md",                       # DOCUMENTAZIONE
    "requirements.txt",                # DIPENDENZE
    ".git",                           # REPOSITORY GIT
    ".gitignore",                     # GIT IGNORE
    "*.xlsx",                         # FILE DI TEST
    "*.csv",                          # FILE DI TEST
    "*.db"                            # DATABASE
)

# File di TEST da mantenere
$TEST_FILES = @(
    "test_ai.py",                     # TEST AI
    "create_test_data.py"             # GENERATORE DATI TEST
)

# Directory da PULIRE (rimuovere tutto tranne essenziali)
$FILES_TO_REMOVE = @()

Get-ChildItem -Path "." -File | ForEach-Object {
    $filename = $_.Name
    $keep = $false

    # Controlla se è essenziale
    foreach ($essential in $ESSENTIAL_FILES) {
        if ($filename -like $essential) {
            $keep = $true
            break
        }
    }

    # Controlla se è un test da mantenere
    foreach ($test in $TEST_FILES) {
        if ($filename -like $test) {
            $keep = $true
            break
        }
    }

    # Se non è essenziale, aggiungilo alla lista rimozione
    if (-not $keep -and $filename -notlike "*.md" -and $filename -notlike "cleanup_*") {
        $FILES_TO_REMOVE += $filename
    }
}

Write-Host "Files da rimuovere: $($FILES_TO_REMOVE.Count)" -ForegroundColor Red

# Backup dei file prima della rimozione
if ($FILES_TO_REMOVE.Count -gt 0) {
    $backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force

    foreach ($file in $FILES_TO_REMOVE) {
        try {
            Move-Item -Path $file -Destination "$backupDir\" -Force
            Write-Host "Moved to backup: $file" -ForegroundColor Gray
        } catch {
            Write-Host "Could not move: $file" -ForegroundColor Yellow
        }
    }

    Write-Host "Backup creato in: $backupDir" -ForegroundColor Green
}

Write-Host "NASA ExcelTools Cleanup COMPLETATO!" -ForegroundColor Green

# Lista file rimanenti
Write-Host "`nFile NASA ESSENZIALI rimanenti:" -ForegroundColor Cyan
Get-ChildItem -Path "." -File | Select-Object Name, Length | Sort-Object Name
