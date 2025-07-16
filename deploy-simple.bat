@echo off
echo ========================================
echo    ExcelTools Pro - GitHub Deployment
echo ========================================

cd /d "d:\Users\C3602943\OneDrive - ARÇELİK A.Ş\Documents\Myproject\ExcelTools"

echo Inizializzando repository Git...
git init

echo Aggiungendo remote origin...
git remote add origin https://github.com/muse-sftwr/exceltool.git

echo Aggiungendo file al repository...
git add .

echo Creando commit iniziale...
git commit -m "Initial commit - ExcelTools Pro v1.0"

echo Configurando branch principale...
git branch -M main

echo Pushing al repository GitHub...
git push -u origin main

echo.
echo ========================================
echo    Deployment completato!
echo ========================================
pause
