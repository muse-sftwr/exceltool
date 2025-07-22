#!/usr/bin/env python3
"""
🚀 LAUNCHER RAPIDO - ExcelTools Pro Advanced Database Manager
=============================================================

Launcher per avviare rapidamente la versione completamente funzionale
del database manager con tutte le implementazioni operative.
"""

import os
import sys
import subprocess

def main():
    print("🚀 LAUNCHER EXCELTOOLS PRO - ADVANCED DATABASE MANAGER")
    print("=" * 60)
    print()

    # Verifica file
    functional_file = "database_manager_functional.py"
    if not os.path.exists(functional_file):
        print(f"❌ ERRORE: File {functional_file} non trovato!")
        print("   Assicurati di essere nella directory corretta.")
        return

    print("✅ File trovato:", functional_file)
    print()

    # Info versione
    print("📋 CARATTERISTICHE VERSIONE FUNZIONALE:")
    print("   ✅ Import CSV/Excel completamente funzionante")
    print("   ✅ Export CSV/Excel completamente funzionante")
    print("   ✅ Selezione tabelle/colonne funzionante")
    print("   ✅ Filtri avanzati completamente operativi")
    print("   ✅ Query SQL eseguibili")
    print("   ✅ Viste salvabili e caricabili")
    print("   ✅ Interfaccia responsive (80% schermo)")
    print("   ✅ Pannelli ridimensionabili")
    print("   ✅ Tutte le funzioni implementate")
    print()

    # File test disponibili
    test_files = ["test_employees.csv", "test_products.csv"]
    available_tests = [f for f in test_files if os.path.exists(f)]

    if available_tests:
        print("📄 FILE TEST DISPONIBILI:")
        for test_file in available_tests:
            print(f"   ✅ {test_file}")
        print("   Usa questi file per testare l'import!")
    else:
        print("⚠️  File test non trovati (verranno creati automaticamente)")
    print()

    # Controlla dipendenze
    print("🔍 CONTROLLO DIPENDENZE:")
    try:
        import pandas
        print("   ✅ pandas disponibile")
    except ImportError:
        print("   ⚠️  pandas non disponibile (funzionalità import/export limitate)")

    try:
        import tkinter
        print("   ✅ tkinter disponibile")
    except ImportError:
        print("   ❌ tkinter non disponibile (errore critico)")
        return

    try:
        import customtkinter
        print("   ✅ customtkinter disponibile (interfaccia moderna)")
    except ImportError:
        print("   ⚠️  customtkinter non disponibile (interfaccia base)")
    print()

    # Avvio
    print("🚀 AVVIO APPLICAZIONE...")
    print("   La finestra si aprirà con dimensioni responsive")
    print("   Usa la GUIDA_TEST_FUNZIONALITA.md per i test")
    print()

    try:
        # Avvia l'applicazione
        subprocess.run([sys.executable, functional_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRORE avvio applicazione: {e}")
    except KeyboardInterrupt:
        print("\n🔄 Applicazione chiusa dall'utente")
    except Exception as e:
        print(f"❌ ERRORE imprevisto: {e}")

if __name__ == "__main__":
    main()
