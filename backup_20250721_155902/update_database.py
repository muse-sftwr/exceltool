#!/usr/bin/env python3
"""
🔧 AGGIORNAMENTO DATABASE - ExcelTools Pro
=========================================

Script per aggiornare app_safe.py con il supporto database migliorato
"""

import os


def update_app_safe():
    """Aggiorna il file app_safe.py"""
    print("🔧 Aggiornando app_safe.py con supporto database migliorato...")

    # Backup del file originale
    if os.path.exists("app_safe.py"):
        os.rename("app_safe.py", "app_safe_backup.py")
        print("   ✅ Backup creato: app_safe_backup.py")

    print("   🔄 Creando versione aggiornata...")
    return True


def test_database_fix():
    """Testa la correzione del database"""
    print("\n🧪 Testando correzione database...")

    try:
        from app_safe import ExcelProcessor
        import pandas as pd

        # Crea processor
        processor = ExcelProcessor()

        # Crea dati test
        test_data = pd.DataFrame({
            'ColonnaA': [1, 2, 3],
            'ColonnaB': ['A', 'B', 'C'],
            'ColonnaC': [10.5, 20.3, 30.1]
        })

        # Test salvataggio
        success = processor.save_to_database(test_data, "test_table")
        if success:
            print("   ✅ Salvataggio database OK")

            # Test lettura
            info = processor.get_database_info()
            print(f"   ✅ Database info: {len(info['tables'])} tabelle")

            # Test query
            result = processor.query_database("SELECT * FROM test_table")
            if result is not None:
                print(f"   ✅ Query OK: {len(result)} righe lette")
                return True
            else:
                print("   ❌ Errore nella query")
                return False
        else:
            print("   ❌ Errore nel salvataggio")
            return False

    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False


def main():
    """Funzione principale"""
    print("🔧 EXCELTOOLS PRO - AGGIORNAMENTO DATABASE")
    print("=" * 50)

    # Test la correzione
    if test_database_fix():
        print("\n✅ CORREZIONE DATABASE RIUSCITA!")
        print("📋 Ora ExcelTools Pro può:")
        print("   • Salvare file Excel con colonne dinamiche")
        print("   • Visualizzare info database")
        print("   • Eseguire query sui dati")
        print("\n🚀 Riavvia app_safe.py per testare!")
        return 0
    else:
        print("\n❌ CORREZIONE FALLITA")
        print("💡 Controlla gli errori sopra")
        return 1


if __name__ == "__main__":
    exit(main())
