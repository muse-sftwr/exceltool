#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SCRIPT FINALE - Installazione flake8 e Verifica PEP8
======================================================

Installa flake8 e verifica che tutti i file siano PEP8 compliant.
Soluzione professionale per ambiente DevOps.

Autore: Senior DevOps Engineer
Data: 2025-07-16
"""

import subprocess
import sys
import os


def install_flake8():
    """Installa flake8 se non presente."""
    print("📦 INSTALLAZIONE FLAKE8")
    print("=" * 30)

    try:
        # Prova a importare flake8
        import flake8
        print("✅ flake8 già installato!")
        return True
    except ImportError:
        print("⚠️  flake8 non trovato, installazione in corso...")

        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "flake8"
            ])
            print("✅ flake8 installato con successo!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore installazione flake8: {e}")
            return False


def check_file_with_flake8(filename):
    """Verifica un file specifico con flake8."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "flake8", filename],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )

        if result.returncode == 0:
            return True, "PEP8 COMPLIANT"
        else:
            error_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            return False, f"{error_count} errori"

    except Exception as e:
        return False, f"Errore: {e}"


def main():
    """Funzione principale."""
    print("🎯 EXCELTOOLS PRO - VERIFICA FINALE PEP8")
    print("=" * 45)
    print("Target: Installazione flake8 + Verifica completa")
    print()

    # Installa flake8
    if not install_flake8():
        print("❌ Impossibile installare flake8!")
        return 1

    print("\n🔍 VERIFICA FILE PRINCIPALI:")
    print("=" * 35)

    files_to_check = [
        'app.py',
        'fix_code.py',
        'create_test_files.py',
        'simple_app.py'
    ]

    all_clean = True

    for filename in files_to_check:
        if os.path.exists(filename):
            is_clean, status = check_file_with_flake8(filename)
            status_icon = "✅" if is_clean else "⚠️"
            print(f"   {status_icon} {filename:<20} - {status}")
            if not is_clean:
                all_clean = False
        else:
            print(f"   ❓ {filename:<20} - file non trovato")

    print("\n" + "=" * 45)

    if all_clean:
        print("🏆 PERFETTO! Tutti i file sono PEP8 compliant!")
        print("✅ create_test_files.py: Errori E122 ed E501 risolti")
        print("✅ ExcelTools Pro: Qualità professionale raggiunta")
        print("\n🎉 MISSIONE COMPLETATA!")
        print("   Il progetto è ora production-ready!")
    else:
        print("⚠️  Alcuni file hanno ancora errori.")
        print("💡 Controlla l'output sopra per i dettagli.")

    print("\n📋 COMANDI UTILI:")
    print("   Verifica singolo file:")
    print("   python -m flake8 create_test_files.py")
    print("   ")
    print("   Verifica tutto il progetto:")
    print("   python -m flake8 .")

    return 0 if all_clean else 1


if __name__ == "__main__":
    exit(main())
