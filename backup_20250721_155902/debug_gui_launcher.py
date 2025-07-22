#!/usr/bin/env python3
"""
🔧 EXCELTOOLS PRO - DEBUG GUI LAUNCHER
=====================================

Script di debug per identificare problemi nella GUI principale.

Autore: Senior Debug Engineer
Data: 2025-07-16
"""

import sys
import traceback

def test_basic_imports():
    """Test import base"""
    print("🔍 Test import dipendenze...")

    try:
        import tkinter as tk
        print("✅ tkinter - OK")
    except Exception as e:
        print(f"❌ tkinter - ERRORE: {e}")
        return False

    try:
        import customtkinter as ctk
        print("✅ customtkinter - OK")
    except Exception as e:
        print(f"❌ customtkinter - ERRORE: {e}")

    try:
        import pandas as pd
        print("✅ pandas - OK")
    except Exception as e:
        print(f"❌ pandas - ERRORE: {e}")

    try:
        import sqlite3
        print("✅ sqlite3 - OK")
    except Exception as e:
        print(f"❌ sqlite3 - ERRORE: {e}")
        return False

    return True

def test_advanced_imports():
    """Test import moduli avanzati"""
    print("\n🔍 Test import moduli avanzati...")

    try:
        from advanced_database_manager import AdvancedDatabaseManager
        print("✅ AdvancedDatabaseManager - OK")
    except Exception as e:
        print(f"❌ AdvancedDatabaseManager - ERRORE: {e}")
        print("Dettagli:")
        traceback.print_exc()
        return False

    try:
        from advanced_excel_tools_gui import AdvancedExcelToolsGUI
        print("✅ AdvancedExcelToolsGUI - OK")
    except Exception as e:
        print(f"❌ AdvancedExcelToolsGUI - ERRORE: {e}")
        print("Dettagli:")
        traceback.print_exc()
        return False

    return True

def test_gui_creation():
    """Test creazione GUI base"""
    print("\n🔍 Test creazione GUI base...")

    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x200")

        label = tk.Label(root, text="Test GUI")
        label.pack(pady=20)

        # Test rapido e chiusura
        root.update()
        root.destroy()
        print("✅ GUI tkinter base - OK")
        return True

    except Exception as e:
        print(f"❌ GUI tkinter base - ERRORE: {e}")
        traceback.print_exc()
        return False

def test_customtkinter_gui():
    """Test GUI CustomTkinter"""
    print("\n🔍 Test GUI CustomTkinter...")

    try:
        import customtkinter as ctk

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("Test CTk")
        root.geometry("300x200")

        label = ctk.CTkLabel(root, text="Test CustomTkinter")
        label.pack(pady=20)

        # Test rapido e chiusura
        root.update()
        root.destroy()
        print("✅ GUI CustomTkinter - OK")
        return True

    except Exception as e:
        print(f"❌ GUI CustomTkinter - ERRORE: {e}")
        traceback.print_exc()
        return False

def test_advanced_gui_init():
    """Test inizializzazione GUI avanzata"""
    print("\n🔍 Test inizializzazione GUI avanzata...")

    try:
        from advanced_excel_tools_gui import AdvancedExcelToolsGUI

        # Prova solo inizializzazione senza mainloop
        print("  Creazione istanza...")
        app = AdvancedExcelToolsGUI()

        print("  Verifica attributi...")
        if hasattr(app, 'root'):
            print("  ✅ root attributo presente")
        else:
            print("  ❌ root attributo mancante")
            return False

        print("  Test update rapido...")
        app.root.update()

        print("  Chiusura...")
        app.root.destroy()

        print("✅ GUI avanzata inizializzazione - OK")
        return True

    except Exception as e:
        print(f"❌ GUI avanzata inizializzazione - ERRORE: {e}")
        print("Dettagli completi:")
        traceback.print_exc()
        return False

def main():
    """Test completo debug"""
    print("🔧 EXCELTOOLS PRO - DEBUG GUI LAUNCHER")
    print("=" * 50)

    # Test progressivi
    tests = [
        ("Import Base", test_basic_imports),
        ("Import Avanzati", test_advanced_imports),
        ("GUI Base", test_gui_creation),
        ("CustomTkinter", test_customtkinter_gui),
        ("GUI Avanzata Init", test_advanced_gui_init)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' fallito con eccezione: {e}")
            traceback.print_exc()
            results.append((test_name, False))

    # Risultati finali
    print(f"\n{'='*50}")
    print("📊 RISULTATI DEBUG:")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1

    print(f"\nRisultato: {passed}/{len(results)} test passati")

    if passed == len(results):
        print("\n🎉 Tutti i test passati! Il problema potrebbe essere nel mainloop.")
        print("💡 Prova a eseguire: py quick_gui_test.py")
    else:
        print(f"\n⚠️ {len(results) - passed} test falliti. Controlla gli errori sopra.")

    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
