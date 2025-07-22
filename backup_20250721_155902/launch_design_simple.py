#!/usr/bin/env python3
"""
🚀 LAUNCHER RAPIDO - ExcelTools Pro Design Edition
=================================================

Launcher semplice per avviare l'applicazione con il nuovo design.

Autore: Launch Engineer
Data: 2025-07-21
"""

import sys
import os

def test_basic_imports():
    """Test import di base"""
    try:
        import tkinter as tk
        print("✅ Tkinter disponibile")
        return True
    except ImportError:
        print("❌ Tkinter non disponibile")
        return False

def launch_design_edition():
    """Lancia Design Edition"""
    try:
        print("🎨 Avvio ExcelTools Pro Design Edition...")

        # Test import
        if not test_basic_imports():
            return False

        print("📦 Importazione moduli design...")
        from excel_tools_design import ExcelToolsDesignEdition
        print("✅ Moduli caricati correttamente")

        print("🚀 Avvio applicazione...")
        app = ExcelToolsDesignEdition()
        app.run()

        return True

    except ImportError as e:
        print(f"❌ Errore import: {e}")
        print("💡 Verificare che tutti i file siano presenti")
        return False
    except Exception as e:
        print(f"❌ Errore avvio: {e}")
        return False

def main():
    """Main entry point"""
    print("🔧 EXCELTOOLS PRO • DESIGN EDITION")
    print("🎨 Launcher Moderno v2.0")
    print("=" * 45)

    # Verifica file
    if not os.path.exists("excel_tools_design.py"):
        print("❌ File excel_tools_design.py non trovato!")
        print("💡 Assicurarsi di essere nella directory corretta")
        return 1

    print("✅ File design trovato")

    # Avvia applicazione
    success = launch_design_edition()

    if success:
        print("🎉 Applicazione avviata con successo!")
        return 0
    else:
        print("❌ Errore durante l'avvio")
        return 1

if __name__ == "__main__":
    sys.exit(main())
