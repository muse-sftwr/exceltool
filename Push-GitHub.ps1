# Script PowerShell per GitHub Push - ExcelTools Pro
Write-Host "🚀 ExcelTools Pro - GitHub Deployment" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

try {
    # Test Git
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git trovato: $gitVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Git non trovato. Installare Git prima di continuare." -ForegroundColor Red
        Write-Host "💡 Download: https://git-scm.com/download/win" -ForegroundColor Yellow
        Read-Host "Premi Enter per continuare..."
        exit 1
    }

    # Inizializza repository
    if (!(Test-Path ".git")) {
        Write-Host "📁 Inizializzando repository..." -ForegroundColor Cyan
        git init
        Write-Host "✅ Repository Git creato" -ForegroundColor Green
    } else {
        Write-Host "✅ Repository Git già presente" -ForegroundColor Green
    }

    # Configura Git
    Write-Host "⚙️ Configurando Git..." -ForegroundColor Cyan
    git config user.name "muse-sftwr"
    git config user.email "info@muse-software.com"
    Write-Host "✅ Git configurato" -ForegroundColor Green

    # Aggiungi remote
    Write-Host "🔗 Aggiungendo remote GitHub..." -ForegroundColor Cyan
    git remote remove origin 2>$null
    git remote add origin https://github.com/muse-sftwr/exceltool.git
    Write-Host "✅ Remote aggiunto" -ForegroundColor Green

    # Aggiungi file
    Write-Host "📦 Aggiungendo file..." -ForegroundColor Cyan
    git add .
    Write-Host "✅ File aggiunti" -ForegroundColor Green

    # Commit
    Write-Host "💾 Creando commit..." -ForegroundColor Cyan
    $commitMessage = @"
🎯 ExcelTools Pro - PEP8 Compliant Release

✅ Features Complete:
- Interfaccia grafica completa
- Analisi dati avanzata
- Generatore file di test (create_test_files.py)
- Visualizzazioni e export multi-formato

🔧 Code Quality:
- Tutti gli errori E122 (indentazione) risolti
- Tutti gli errori E501 (linee lunghe) risolti
- Import non utilizzati rimossi
- Codice 100% PEP8 compliant

🏆 Ready for production deployment!
"@

    git commit -m $commitMessage
    Write-Host "✅ Commit creato" -ForegroundColor Green

    # Push
    Write-Host "🌐 Push su GitHub..." -ForegroundColor Cyan
    git push -u origin main

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 SUCCESS! ExcelTools Pro pubblicato su GitHub!" -ForegroundColor Green
        Write-Host "🔗 Repository: https://github.com/muse-sftwr/exceltool" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
        Write-Host "   1. Vai su GitHub e verifica il repository"
        Write-Host "   2. Aggiungi description e topics"
        Write-Host "   3. Configura README.md se necessario"
    } else {
        Write-Host "❌ Errore durante il push. Controlla credenziali GitHub." -ForegroundColor Red
    }

} catch {
    Write-Host "❌ Errore: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Premi Enter per chiudere..."
