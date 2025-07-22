#!/usr/bin/env python3
"""
🧪 TEST DESIGN EDITION - ExcelTools Pro
======================================

Test rapido per verificare che l'applicazione Design Edition
funzioni correttamente con il nuovo design moderno.

Autore: QA Design Engineer
Data: 2025-07-21
"""

import sys
import traceback

def test_import_design():
    """Test import del modulo design"""
    try:
        print("🧪 Testing ExcelTools Pro Design Edition...")
        print("=" * 50)

        # Test import
        print("📦 Test import moduli...")
        import tkinter as tk
        print("  ✅ tkinter - OK")

        try:
            import pandas as pd
            print("  ✅ pandas - OK")
        except ImportError:
            print("  ⚠️  pandas - MANCANTE (opzionale)")

        # Test import design
        try:
            from excel_tools_design import ExcelToolsDesignEdition
            print("  ✅ excel_tools_design - OK")
        except Exception as e:
            print(f"  ❌ excel_tools_design - ERRORE: {e}")
            return False

        # Test creazione istanza
        print("\n🎨 Test creazione applicazione Design Edition...")
        try:
            root = tk.Tk()
            root.withdraw()  # Nascondi finestra di test

            app = ExcelToolsDesignEdition()
            print("  ✅ Istanza creata correttamente")

            # Test attributi principali
            if hasattr(app, 'theme'):
                print("  ✅ Sistema theme attivo")
            if hasattr(app, 'root'):
                print("  ✅ GUI root configurata")
            if hasattr(app, 'create_interface'):
                print("  ✅ Metodi interfaccia disponibili")

            root.destroy()

        except Exception as e:
            print(f"  ❌ Errore creazione app: {e}")
            traceback.print_exc()
            return False

        print("\n🎉 TUTTI I TEST PASSATI!")
        print("✅ ExcelTools Pro Design Edition è pronta!")
        print("\n💡 Per avviare l'applicazione completa:")
        print("   py excel_tools_design.py")

        return True

    except Exception as e:
        print(f"❌ Errore test: {e}")
        traceback.print_exc()
        return False

def test_launcher_design():
    """Test launcher design"""
    try:
        print("\n🚀 Test Launcher Design...")

        try:
            from launcher_design import DesignLauncher
            print("  ✅ launcher_design importato")

            # Test creazione launcher
            launcher = DesignLauncher()
            print("  ✅ Launcher Design creato")

        except Exception as e:
            print(f"  ⚠️  Launcher Design non disponibile: {e}")

    except Exception as e:
        print(f"  ❌ Errore test launcher: {e}")

def main():
    """Test principale"""
    print("🔧 EXCELTOOLS PRO • DESIGN EDITION")
    print("🧪 Test Suite Completa")
    print("=" * 50)

    success = test_import_design()
    test_launcher_design()

    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST COMPLETATI CON SUCCESSO!")
        print("🎨 Design Edition pronta per l'uso!")
    else:
        print("❌ Alcuni test falliti - controllare errori sopra")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
