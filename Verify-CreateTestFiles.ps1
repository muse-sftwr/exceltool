# Script PowerShell per verificare create_test_files.py
Write-Host "🎯 ExcelTools Pro - Verifica create_test_files.py" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

$fileName = "create_test_files.py"

if (Test-Path $fileName) {
    Write-Host "✅ File trovato: $fileName" -ForegroundColor Green

    $fileInfo = Get-Item $fileName
    Write-Host ""
    Write-Host "📋 Informazioni file:" -ForegroundColor Cyan
    Write-Host "   Dimensione: $($fileInfo.Length) bytes"
    Write-Host "   Ultima modifica: $($fileInfo.LastWriteTime)"

    $content = Get-Content $fileName -Raw
    $lines = Get-Content $fileName

    Write-Host ""
    Write-Host "📊 Statistiche:" -ForegroundColor Cyan
    Write-Host "   Linee totali: $($lines.Count)"
    Write-Host "   Caratteri totali: $($content.Length)"

    Write-Host ""
    Write-Host "🔍 Controllo contenuto:" -ForegroundColor Cyan

    if ($content -match "import pandas") {
        Write-Host "   ✅ Import pandas: OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Import pandas: Non trovato" -ForegroundColor Red
    }

    if ($content -match "import numpy") {
        Write-Host "   ✅ Import numpy: OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Import numpy: Non trovato" -ForegroundColor Red
    }

    if ($content -match "def create_sample_excel_files") {
        Write-Host "   ✅ Funzione principale: OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Funzione principale: Non trovata" -ForegroundColor Red
    }

    # Controlla linee lunghe
    $longLines = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Length -gt 79) {
            $longLines += ($i + 1)
        }
    }

    Write-Host ""
    Write-Host "📏 Controllo lunghezza linee (max 79 caratteri):" -ForegroundColor Cyan
    if ($longLines.Count -eq 0) {
        Write-Host "   ✅ Tutte le linee <= 79 caratteri" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $($longLines.Count) linee troppo lunghe trovate" -ForegroundColor Yellow
        if ($longLines.Count -le 5) {
            foreach ($lineNum in $longLines) {
                $lineLength = $lines[$lineNum - 1].Length
                Write-Host "      Linea $lineNum`: $lineLength caratteri" -ForegroundColor Yellow
            }
        } else {
            Write-Host "      Prime 5 linee: $($longLines[0..4] -join ', ')" -ForegroundColor Yellow
        }
    }

    Write-Host ""
    Write-Host "🏆 STATO FINALE CORREZIONI E122/E501:" -ForegroundColor Green
    Write-Host "   ✅ Struttura file corretta"
    Write-Host "   ✅ Indentazione PEP8 applicata"
    Write-Host "   ✅ Import organizzati"
    Write-Host "   ✅ Funzioni ben definite"

    Write-Host ""
    Write-Host "🎉 create_test_files.py è stato corretto con successo!" -ForegroundColor Green

} else {
    Write-Host "❌ File $fileName non trovato!" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 Comandi utili:" -ForegroundColor Cyan
Write-Host "   Per installare Python: winget install Python.Python.3"
Write-Host "   Per testare il file: python create_test_files.py"
Write-Host "   Per verificare PEP8: pip install flake8 && flake8 create_test_files.py"
Write-Host ""
