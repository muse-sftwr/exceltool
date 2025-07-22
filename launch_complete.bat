@echo off
REM NASA ExcelTools Complete Launcher
REM ==================================

echo.
echo 🚀 NASA EXCELTOOLS UNIFIED - COMPLETE PLATFORM
echo ===============================================
echo.

cd /d "%~dp0"

echo 🔍 System Check:
echo ================

REM Test Python
C:\Users\C3602943\AppData\Local\Programs\Python\Python313\python.exe --version
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo ✅ Python found

REM Test pandas
C:\Users\C3602943\AppData\Local\Programs\Python\Python313\python.exe -c "import pandas; print('✅ Pandas available')"
if errorlevel 1 (
    echo ⚠️ Pandas not available - installing...
    C:\Users\C3602943\AppData\Local\Programs\Python\Python313\python.exe -m pip install pandas
)

echo.
echo 🚀 Launching NASA ExcelTools Complete...
echo ========================================
echo.

REM Launch application
C:\Users\C3602943\AppData\Local\Programs\Python\Python313\python.exe simple_launcher.py

if errorlevel 1 (
    echo.
    echo ❌ Application failed to start
    echo.
    echo 💡 Troubleshooting:
    echo - Check if all files exist
    echo - Verify Python installation
    echo - Check for error messages above
    echo.
    pause
)

echo.
echo 🔚 NASA ExcelTools session ended
pause
