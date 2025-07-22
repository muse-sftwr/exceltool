#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script finale per verificare lo stato di tutti gli errori di linting
dopo le correzioni applicate.
"""

import subprocess
import sys
import os


def check_flake8_status():
    """Controlla lo stato finale di tutti gli errori flake8."""
    print("🔍 VERIFICA FINALE STATO LINTING - ExcelTools Pro")
    print("=" * 60)

    try:
        # Esegui flake8 e cattura l'output
        result = subprocess.run(
            ['flake8', '.', '--statistics'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )

        print(f"📊 Codice di uscita flake8: {result.returncode}")

        if result.returncode == 0:
            print("✅ PERFETTO! Nessun errore di linting rilevato!")
            print("🎉 Il progetto ExcelTools Pro è 100% conforme a PEP8!")
        else:
            print("⚠️  Errori rilevati:")
            if result.stdout:
                print("\n📋 OUTPUT:")
                print(result.stdout)
            if result.stderr:
                print("\n❌ ERRORI:")
                print(result.stderr)

        print("\n" + "=" * 60)

        # Controlla file specifici
        files_to_check = [
            'app.py',
            'fix_code.py',
            'create_test_files.py',
            'simple_app.py'
        ]

        print("📁 VERIFICA FILE PRINCIPALI:")
        for file in files_to_check:
            if os.path.exists(file):
                file_result = subprocess.run(
                    ['flake8', file],
                    capture_output=True,
                    text=True
                )

                if file_result.returncode == 0:
                    print(f"   ✅ {file}: PERFETTO")
                else:
                    print(f"   ⚠️  {file}: errori presenti")
                    if file_result.stdout:
                        error_lines = file_result.stdout.strip().split('\n')
                        error_count = len(error_lines)
                        print(f"      📊 Errori: {error_count}")
            else:
                print(f"   ❓ {file}: file non trovato")

        return result.returncode == 0

    except FileNotFoundError:
        print("❌ Errore: flake8 non trovato!")
        print("💡 Installa con: pip install flake8")
        return False
    except Exception as e:
        print(f"❌ Errore durante la verifica: {e}")
        return False


def main():
    """Funzione principale."""
    success = check_flake8_status()

    if success:
        print("\n🎯 MISSIONE COMPLETATA!")
        print("   Tutti gli errori di linting sono stati risolti!")
        print("   ExcelTools Pro è ora completamente conforme a PEP8!")
    else:
        print("\n🔧 Alcune correzioni potrebbero essere ancora necessarie.")
        print("   Controlla l'output sopra per i dettagli.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
