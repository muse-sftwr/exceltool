@echo off
REM NASA EXCELTOOLS LAUNCHER
REM =========================
REM Avvia ExcelTools con Python configurato

set PYTHON_PATH=C:\Users\C3602943\AppData\Local\Programs\Python\Python313\python.exe

echo.
echo ======================================
echo   NASA EXCELTOOLS UNIFIED LAUNCHER
echo ======================================
echo.

echo Testing Python...
"%PYTHON_PATH%" --version

echo.
echo Testing pandas...
"%PYTHON_PATH%" -c "import pandas as pd; print('Pandas OK:', pd.__version__)"

echo.
echo Launching ExcelTools Unified...
"%PYTHON_PATH%" exceltools_unified.py

pause
