@echo off
echo ================================================
echo         ExcelTools Pro - Avvio Applicazione
echo ================================================
echo.

REM Controlla se Python è installato
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

echo ✅ Python trovato
echo.

REM Controlla se le dipendenze sono installate
echo 🔧 Controllo dipendenze...
py -c "import pandas, customtkinter, openpyxl, watchdog" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installazione dipendenze mancanti...
    py -m pip install pandas customtkinter openpyxl watchdog numpy
    if %errorlevel% neq 0 (
        echo ERRORE: Impossibile installare le dipendenze
        pause
        exit /b 1
    )
)

echo ✅ Dipendenze OK
echo.

REM Avvia l'applicazione
echo 🚀 Avvio ExcelTools Pro...
echo.
py app.py

REM Se l'applicazione si chiude con errore
if %errorlevel% neq 0 (
    echo.
    echo ❌ L'applicazione si è chiusa con errori
    echo Premi un tasto per chiudere...
    pause >nul
)
