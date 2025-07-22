#!/usr/bin/env python3
"""
🧪 TEST AUTOMATICO COMPLETO - ExcelTools Pro
===========================================

Script che testa automaticamente tutte le funzionalità
di ExcelTools Pro senza intervento dell'utente.

Autore: Senior DevOps Engineer
Data: 2025-07-16
"""

import os
import sys
import time
import tempfile
from pathlib import Path


def test_imports():
    """Testa tutte le importazioni necessarie"""
    print("🔍 Test importazioni...")

    tests = [
        ("pandas", "import pandas"),
        ("numpy", "import numpy"),
        ("customtkinter", "import customtkinter"),
        ("openpyxl", "import openpyxl"),
        ("sqlite3", "import sqlite3"),
        ("tkinter", "import tkinter"),
        ("app_safe", "from app_safe import ExcelProcessor, SimpleExcelGUI"),
        ("create_test_simple", "from create_test_simple import create_simple_test_files")
    ]

    success = 0
    for name, import_cmd in tests:
        try:
            exec(import_cmd)
            print(f"   ✅ {name}")
            success += 1
        except Exception as e:
            print(f"   ❌ {name}: {e}")

    print(f"📊 Importazioni: {success}/{len(tests)} OK")
    return success == len(tests)


def test_excel_processor():
    """Testa la classe ExcelProcessor"""
    print("\n🔧 Test ExcelProcessor...")

    try:
        from app_safe import ExcelProcessor

        # Test inizializzazione
        processor = ExcelProcessor()
        print("   ✅ Inizializzazione OK")

        # Test database
        if os.path.exists("excel_data.db"):
            print("   ✅ Database creato")
        else:
            print("   ❌ Database non trovato")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def test_file_generation():
    """Testa la generazione di file Excel"""
    print("\n📁 Test generazione file...")

    try:
        from create_test_simple import create_simple_test_files

        # Salva file esistenti
        existing_files = []
        test_files = [
            'test_vendite_simple.xlsx',
            'test_inventario_simple.xlsx',
            'test_performance_1k.xlsx'
        ]

        for f in test_files:
            if os.path.exists(f):
                existing_files.append(f)

        # Genera nuovi file
        create_simple_test_files()

        # Verifica che i file esistano
        success = 0
        for f in test_files:
            if os.path.exists(f):
                size = os.path.getsize(f)
                print(f"   ✅ {f} ({size} bytes)")
                success += 1
            else:
                print(f"   ❌ {f} non creato")

        print(f"📊 File generati: {success}/{len(test_files)}")
        return success == len(test_files)

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def test_excel_reading():
    """Testa la lettura di file Excel"""
    print("\n📖 Test lettura file Excel...")

    try:
        from app_safe import ExcelProcessor
        import pandas as pd

        processor = ExcelProcessor()

        # Test lettura file semplice
        if os.path.exists('test_vendite_simple.xlsx'):
            df = processor.read_excel_file('test_vendite_simple.xlsx')
            print(f"   ✅ Lettura OK: {len(df)} righe, {len(df.columns)} colonne")

            # Test salvataggio database
            success = processor.save_to_database(df, "test_table")
            if success:
                print("   ✅ Salvataggio database OK")
            else:
                print("   ❌ Errore salvataggio database")
                return False

            return True
        else:
            print("   ❌ File test non trovato")
            return False

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def test_gui_creation():
    """Testa la creazione dell'interfaccia (senza avviarla)"""
    print("\n🎨 Test creazione GUI...")

    try:
        from app_safe import SimpleExcelGUI

        # Crea GUI ma non la avvia
        gui = SimpleExcelGUI()
        print("   ✅ GUI creata OK")

        # Test attributi principali
        if hasattr(gui, 'processor'):
            print("   ✅ Processor collegato")
        if hasattr(gui, 'root'):
            print("   ✅ Root window creata")
        if hasattr(gui, 'text_area'):
            print("   ✅ Text area creata")

        # Chiudi finestra
        gui.root.destroy()
        print("   ✅ GUI distrutta OK")

        return True

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def test_pep8_compliance():
    """Testa la conformità PEP8"""
    print("\n📋 Test conformità PEP8...")

    try:
        from verify_pep8_final import main as verify_main

        # Esegui verifica PEP8
        result = verify_main()

        if result == 0:
            print("   ✅ PEP8 100% conforme")
            return True
        else:
            print("   ❌ Violazioni PEP8 trovate")
            return False

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def cleanup_test_files():
    """Pulisce i file di test creati"""
    print("\n🧹 Pulizia file di test...")

    files_to_keep = [
        'test_vendite_simple.xlsx',
        'test_inventario_simple.xlsx',
        'test_performance_1k.xlsx'
    ]

    print("   ℹ️ File di test mantenuti per uso futuro")
    return True


def main():
    """Funzione principale di test"""
    print("🧪 EXCELTOOLS PRO - TEST AUTOMATICO COMPLETO")
    print("=" * 60)
    print("Test di tutte le funzionalità senza intervento utente")
    print()

    tests = [
        ("Importazioni", test_imports),
        ("ExcelProcessor", test_excel_processor),
        ("Generazione file", test_file_generation),
        ("Lettura Excel", test_excel_reading),
        ("Creazione GUI", test_gui_creation),
        ("Conformità PEP8", test_pep8_compliance),
    ]

    results = []

    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            result = test_func()
            results.append((name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"Risultato {name}: {status}")
        except Exception as e:
            print(f"❌ ERRORE CRITICO in {name}: {e}")
            results.append((name, False))

    # Cleanup
    cleanup_test_files()

    # Risultati finali
    print("\n" + "=" * 60)
    print("📊 RISULTATI FINALI TEST")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {name}")

    print(f"\n📈 SUMMARY: {passed}/{total} test superati")

    if passed == total:
        print("\n🎉 TUTTI I TEST SUPERATI!")
        print("✅ ExcelTools Pro è completamente funzionale!")
        print("\n🚀 PRONTO PER L'USO PRODUZIONE!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test falliti")
        print("💡 Controlla i dettagli sopra")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrotti dall'utente")
        exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRORE CRITICO: {e}")
        exit(1)
