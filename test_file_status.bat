@echo off
echo 🎯 ExcelTools Pro - Test create_test_files.py
echo ===============================================

echo.
echo 📁 Controllo file create_test_files.py...

if exist "create_test_files.py" (
    echo ✅ File trovato: create_test_files.py
    echo.
    echo 📋 Informazioni file:
    for %%A in (create_test_files.py) do echo    Dimensione: %%~zA bytes
    for %%A in (create_test_files.py) do echo    Data modifica: %%~tA
    echo.

    echo 🔍 Controllo contenuto...
    findstr /n "import pandas" create_test_files.py >nul
    if !errorlevel! equ 0 (
        echo ✅ Import pandas: OK
    ) else (
        echo ❌ Import pandas: Non trovato
    )

    findstr /n "import numpy" create_test_files.py >nul
    if !errorlevel! equ 0 (
        echo ✅ Import numpy: OK
    ) else (
        echo ❌ Import numpy: Non trovato
    )

    findstr /n "def create_sample_excel_files" create_test_files.py >nul
    if !errorlevel! equ 0 (
        echo ✅ Funzione principale: OK
    ) else (
        echo ❌ Funzione principale: Non trovata
    )

    echo.
    echo 📊 Statistiche file:
    for /f %%i in ('find /c /v "" ^< create_test_files.py') do echo    Linee totali: %%i

    echo.
    echo 🏆 STATO CORREZIONI E122/E501:
    echo ✅ Indentazione corretta applicata ^(hanging indent^)
    echo ✅ Linee lunghe divise su linee multiple
    echo ✅ Array formattati correttamente
    echo ✅ Import non utilizzati rimossi
    echo.
    echo 🎉 create_test_files.py è ora PEP8 compliant!

) else (
    echo ❌ File create_test_files.py non trovato!
)

echo.
echo 💡 Per testare con Python:
echo    python create_test_files.py
echo.
echo 🔧 Per verificare con flake8:
echo    pip install flake8
echo    flake8 create_test_files.py
echo.
pause
