@echo off
echo ================================================
echo    ExcelTools Pro - Avvio Applicazione
echo ================================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Python non trovato nel PATH
    echo Installa Python 3.8+ da python.org
    pause
    exit /b 1
)

echo Python trovato, controllo dipendenze...

REM Installa dipendenze se necessario
pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo Installazione pandas...
    pip install pandas
)

pip show openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo Installazione openpyxl...
    pip install openpyxl
)

pip show customtkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo Installazione customtkinter...
    pip install customtkinter
)

echo.
echo Avvio ExcelTools Pro...
echo.

REM Avvia l'applicazione
python app.py

if %errorlevel% neq 0 (
    echo.
    echo ERRORE nell'avvio dell'applicazione principale
    echo Provo con la versione semplificata...
    echo.
    python simple_app.py
)

echo.
echo Applicazione chiusa.
pause
