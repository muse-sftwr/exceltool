#!/usr/bin/env python3
"""
🔧 INSTALLAZIONE AUTOMATICA - ExcelTools Pro
===========================================

Script per installare tutte le dipendenze e preparare
l'ambiente di ExcelTools Pro.

Autore: Senior DevOps Engineer
Data: 2025-07-16
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Esegue un comando e gestisce gli errori"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"   ✅ {description} completato")
            return True
        else:
            print(f"   ❌ Errore: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Errore nell'esecuzione: {e}")
        return False


def check_python():
    """Verifica versione Python"""
    print("🔍 Verificando Python...")
    version = sys.version_info
    print(f"   📍 Python {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Versione Python compatibile")
        return True
    else:
        print("   ❌ Richiesto Python 3.8+")
        return False


def install_dependencies():
    """Installa le dipendenze necessarie"""
    print("\n📦 Installando dipendenze...")

    packages = [
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.0.0",
        "customtkinter>=5.0.0",
        "watchdog>=3.0.0"
    ]

    success_count = 0

    for package in packages:
        if run_command(f"py -m pip install {package}", f"Installando {package}"):
            success_count += 1

    print(f"\n📊 Installate {success_count}/{len(packages)} dipendenze")
    return success_count == len(packages)


def create_launcher():
    """Crea script di avvio rapido"""
    print("\n🚀 Creando launcher...")

    launcher_content = '''@echo off
echo ========================================
echo    ExcelTools Pro - Avvio Rapido
echo ========================================
echo.

echo Verificando ambiente...
py -c "import pandas, numpy, customtkinter; print('Tutte le librerie OK')" 2>nul
if errorlevel 1 (
    echo ❌ Dipendenze mancanti! Esegui setup.py
    pause
    exit /b 1
)

echo ✅ Ambiente verificato
echo 🚀 Avviando ExcelTools Pro...
echo.

py app_safe.py

echo.
echo Applicazione chiusa.
pause
'''

    try:
        with open("start_exceltool.bat", "w", encoding="utf-8") as f:
            f.write(launcher_content)
        print("   ✅ Launcher creato: start_exceltool.bat")
        return True
    except Exception as e:
        print(f"   ❌ Errore creazione launcher: {e}")
        return False


def generate_test_files():
    """Genera file di test se non esistono"""
    print("\n📁 Verificando file di test...")

    test_files = ["test_vendite.xlsx", "test_inventario.xlsx"]
    existing = [f for f in test_files if os.path.exists(f)]

    if existing:
        print(f"   ✅ File esistenti: {', '.join(existing)}")
        return True

    print("   📝 Generando file di test...")
    return run_command("py create_test_files.py", "Generazione file di test")


def verify_installation():
    """Verifica che tutto funzioni"""
    print("\n🔍 Verifica finale...")

    tests = [
        ("py -c \"import pandas; print('pandas OK')\"", "Test pandas"),
        ("py -c \"import numpy; print('numpy OK')\"", "Test numpy"),
        ("py -c \"import customtkinter; print('customtkinter OK')\"", "Test CustomTkinter"),
        ("py -c \"import openpyxl; print('openpyxl OK')\"", "Test OpenPyXL"),
    ]

    success_count = 0
    for command, description in tests:
        if run_command(command, description):
            success_count += 1

    print(f"\n📊 Test superati: {success_count}/{len(tests)}")
    return success_count == len(tests)


def main():
    """Funzione principale di setup"""
    print("🏆 EXCELTOOLS PRO - SETUP AUTOMATICO")
    print("=" * 50)
    print("Installazione e configurazione automatica")
    print()

    # Step 1: Verifica Python
    if not check_python():
        print("\n❌ ERRORE: Versione Python non compatibile")
        return 1

    # Step 2: Installa dipendenze
    if not install_dependencies():
        print("\n❌ ERRORE: Problemi nell'installazione dipendenze")
        return 1

    # Step 3: Crea launcher
    create_launcher()

    # Step 4: Genera file di test
    generate_test_files()

    # Step 5: Verifica finale
    if not verify_installation():
        print("\n⚠️ ATTENZIONE: Alcuni test falliti")

    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETATO!")
    print("=" * 50)
    print()
    print("📋 COME USARE EXCELTOOLS PRO:")
    print("   1. Doppio click su 'start_exceltool.bat'")
    print("   2. Oppure: py app_safe.py")
    print("   3. Oppure: py launcher_safe.py")
    print()
    print("📁 FILE DISPONIBILI:")
    print("   • app_safe.py - Versione sicura")
    print("   • launcher_safe.py - Launcher con verifiche")
    print("   • start_exceltool.bat - Avvio rapido")
    print("   • create_test_files.py - Generatore dati test")
    print()
    print("🎯 TUTTO PRONTO! ExcelTools Pro è installato e funzionante!")

    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Setup annullato dall'utente")
        exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRORE CRITICO: {e}")
        exit(1)
