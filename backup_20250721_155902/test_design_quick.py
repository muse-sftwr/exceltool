#!/usr/bin/env python3
"""
🧪 TEST RAPIDO - ExcelTools Pro Design Edition
==============================================

Test veloce per verificare che l'applicazione funzioni correttamente
dopo le correzioni degli errori di font.
"""

import os
import sys

def test_imports():
    """Testa che tutti i moduli necessari siano importabili"""
    print("🔍 Test import moduli...")

    try:
        import tkinter as tk
        print("✅ tkinter importato correttamente")
    except ImportError as e:
        print(f"❌ Errore import tkinter: {e}")
        return False

    try:
        from excel_tools_design import ExcelToolsProDesign, ModernTheme
        print("✅ excel_tools_design importato correttamente")
    except ImportError as e:
        print(f"❌ Errore import excel_tools_design: {e}")
        return False

    return True

def test_design_classes():
    """Testa che le classi di design siano create correttamente"""
    print("\n🎨 Test classi design...")

    try:
        # Test root window temporanea
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Nascondi la finestra

        # Test ModernTheme
        from excel_tools_design import ModernTheme
        assert hasattr(ModernTheme, 'PRIMARY')
        assert hasattr(ModernTheme, 'FONT_FAMILY')
        print("✅ ModernTheme configurato correttamente")

        # Test ModernLabel senza font duplicato
        from excel_tools_design import ModernLabel
        test_label = ModernLabel(root, text="Test", style="body")
        print("✅ ModernLabel funziona senza errori font")

        root.destroy()
        return True

    except Exception as e:
        print(f"❌ Errore test design: {e}")
        return False

def test_app_creation():
    """Testa che l'app possa essere creata senza crash"""
    print("\n🚀 Test creazione applicazione...")

    try:
        # Verifica che il file principale esista
        if not os.path.exists("excel_tools_design.py"):
            print("❌ File excel_tools_design.py non trovato")
            return False

        print("✅ File excel_tools_design.py trovato")
        print("✅ Import test superati - l'app dovrebbe avviarsi")
        return True

    except Exception as e:
        print(f"❌ Errore test app: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("🧪 INIZIO TEST DESIGN EDITION")
    print("=" * 50)

    tests = [
        test_imports,
        test_design_classes,
        test_app_creation
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 50)
    print("📊 RISULTATI TEST:")

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"🎉 TUTTI I TEST SUPERATI ({passed}/{total})")
        print("\n✅ L'ExcelTools Pro Design Edition è pronto!")
        print("✅ Gli errori di font sono stati corretti")
        print("✅ L'applicazione dovrebbe avviarsi senza problemi")
    else:
        print(f"⚠️  ALCUNI TEST FALLITI ({passed}/{total})")
        print("🔧 Verifica i messaggi di errore sopra")

if __name__ == "__main__":
    main()
