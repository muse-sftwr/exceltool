#!/usr/bin/env python3
"""
🚀 LAUNCHER SICURO - ExcelTools Pro
==================================

Script che verifica tutte le dipendenze e avvia ExcelTools
in modo sicuro senza errori.

Autore: Senior DevOps Engineer
Data: 2025-07-16
"""

import sys
import os


def check_dependencies():
    """Verifica che tutte le dipendenze siano disponibili."""
    print("🔍 Verificando dipendenze...")

    required_modules = [
        ('pandas', 'pandas>=2.0.0'),
        ('numpy', 'numpy>=1.24.0'),
        ('customtkinter', 'customtkinter>=5.0.0'),
        ('openpyxl', 'openpyxl>=3.0.0'),
        ('watchdog', 'watchdog>=3.0.0'),
        ('sqlite3', 'sqlite3 (built-in)'),
        ('tkinter', 'tkinter (built-in)'),
        ('threading', 'threading (built-in)'),
        ('logging', 'logging (built-in)')
    ]

    missing = []

    for module, description in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} - MANCANTE")
            missing.append(module)

    if missing:
        print(f"\n❌ Dipendenze mancanti: {', '.join(missing)}")
        print("💡 Installa con: py -m pip install " + " ".join(missing))
        return False

    print("✅ Tutte le dipendenze sono disponibili!")
    return True


def check_files():
    """Verifica che tutti i file necessari esistano."""
    print("\n🔍 Verificando file del progetto...")

    required_files = [
        'app.py',
        'create_test_files.py',
        'requirements.txt',
        'README.md'
    ]

    missing = []

    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MANCANTE")
            missing.append(file)

    if missing:
        print(f"\n❌ File mancanti: {', '.join(missing)}")
        return False

    print("✅ Tutti i file necessari sono presenti!")
    return True


def test_import():
    """Testa l'importazione del modulo principale."""
    print("\n🔍 Testando importazione moduli...")

    try:
        # Test import delle classi principali
        sys.path.insert(0, '.')

        # Test ExcelProcessor
        from app import ExcelProcessor
        ExcelProcessor()  # Test inizializzazione
        print("   ✅ ExcelProcessor importato e inizializzato")

        # Test GUI (senza avviarla)
        import app  # noqa: F401
        print("   ✅ Modulo app importato completamente")

        print("✅ Tutti i moduli importati correttamente!")
        return True

    except Exception as e:
        print(f"   ❌ Errore nell'importazione: {e}")
        return False


def create_test_data():
    """Crea file di test se non esistono."""
    print("\n🔍 Verificando file di test...")

    test_files = [
        'test_vendite.xlsx',
        'test_inventario.xlsx',
        'test_performance_50k.xlsx'
    ]

    existing = [f for f in test_files if os.path.exists(f)]

    if existing:
        print(f"   ✅ File di test esistenti: {', '.join(existing)}")
        return True

    print("   📁 Nessun file di test trovato. Generando...")

    try:
        from create_test_files import create_sample_excel_files
        create_sample_excel_files()
        print("   ✅ File di test generati con successo!")
        return True
    except Exception as e:
        print(f"   ❌ Errore nella generazione file di test: {e}")
        return False


def launch_application():
    """Avvia l'applicazione ExcelTools Pro."""
    print("\n🚀 Avviando ExcelTools Pro...")

    try:
        from app import main
        print("   ✅ Applicazione avviata!")
        print("   💡 L'interfaccia grafica dovrebbe aprirsi ora...")
        main()

    except KeyboardInterrupt:
        print("\n   🛑 Applicazione chiusa dall'utente")
        return True
    except Exception as e:
        print(f"   ❌ Errore nell'avvio: {e}")
        return False


def main():
    """Funzione principale del launcher."""
    print("🏆 EXCELTOOLS PRO - LAUNCHER SICURO")
    print("=" * 50)
    print("Verifica automatica e avvio sicuro dell'applicazione")
    print()

    # Step 1: Verifica dipendenze
    if not check_dependencies():
        print("\n❌ ERRORE: Dipendenze mancanti")
        return 1

    # Step 2: Verifica file
    if not check_files():
        print("\n❌ ERRORE: File mancanti")
        return 1

    # Step 3: Test importazione
    if not test_import():
        print("\n❌ ERRORE: Problemi nell'importazione")
        return 1

    # Step 4: Crea file di test se necessari
    create_test_data()

    # Step 5: Avvia applicazione
    print("\n" + "=" * 50)
    print("🎉 TUTTO PRONTO! Avviando ExcelTools Pro...")
    print("=" * 50)

    launch_application()

    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Operazione annullata dall'utente")
        exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRORE CRITICO: {e}")
        exit(1)
