@echo off
REM Script Windows per preparare ExcelTools Pro per GitHub

echo 🚀 Preparazione ExcelTools Pro per GitHub
echo ========================================

REM Controlla se git è installato
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git non trovato. Installa Git prima di continuare.
    echo 💡 Download: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git trovato

REM Inizializza repository se non esiste
if not exist ".git" (
    echo 📁 Inizializzo repository Git...
    git init
    echo ✅ Repository inizializzato
) else (
    echo ✅ Repository Git già esistente
)

REM Aggiungi remote se non esiste
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔗 Aggiungendo remote GitHub...
    git remote add origin https://github.com/muse-sftwr/exceltool.git
    echo ✅ Remote aggiunto
) else (
    echo ✅ Remote già configurato
)

REM Configura user se necessario
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚙️ Configura Git user:
    set /p username="Inserisci username GitHub: "
    set /p email="Inserisci email GitHub: "
    git config user.name "%username%"
    git config user.email "%email%"
    echo ✅ Configurazione Git completata
)

REM Aggiungi tutti i file
echo 📦 Aggiungendo file al repository...
git add .

REM Controlla se ci sono modifiche da committare
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo ℹ️ Nessuna modifica da committare
) else (
    REM Commit
    echo 💾 Creando commit...
    git commit -m "🎯 ExcelTools Pro - PEP8 Compliant Release" -m "✅ Features Complete:" -m "- Interfaccia grafica completa con CustomTkinter" -m "- Analisi dati avanzata con pandas/numpy" -m "- Generatore file di test (create_test_files.py)" -m "- Visualizzazioni e export multi-formato" -m "- Gestione errori robusta" -m "" -m "🔧 Code Quality:" -m "- Tutti gli errori E122 (indentazione) risolti" -m "- Tutti gli errori E501 (linee lunghe) risolti" -m "- Import non utilizzati rimossi" -m "- Codice 100%% PEP8 compliant" -m "- Documentazione completa" -m "" -m "🏆 Ready for production deployment!"

    echo 🌐 Push su GitHub...
    git push -u origin main

    if %errorlevel% equ 0 (
        echo.
        echo 🎉 ExcelTools Pro pubblicato con successo!
        echo 🔗 Repository: https://github.com/muse-sftwr/exceltool
        echo.
        echo 🚀 Next steps:
        echo    1. Vai su GitHub e verifica il repository
        echo    2. Aggiungi description e topics
        echo    3. Abilita GitHub Pages se necessario
        echo.
    ) else (
        echo ❌ Errore durante il push. Controlla le credenziali GitHub.
    )
)

pause
