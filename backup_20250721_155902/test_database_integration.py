#!/usr/bin/env python3
"""
🧪 TEST DATABASE EXCEL - ExcelTools Pro
======================================

Script per testare l'integrazione database con file Excel reali
"""

import pandas as pd
import os
from app_safe import ExcelProcessor


def test_real_excel_integration():
    """Testa l'integrazione completa con file Excel"""
    print("🧪 TEST INTEGRAZIONE DATABASE-EXCEL")
    print("=" * 50)

    # Crea processor
    processor = ExcelProcessor()
    print("✅ ExcelProcessor inizializzato")

    # Test 1: File Excel con colonne dinamiche
    print("\n📊 Test 1: File Excel con colonne personalizzate")
    test_data = pd.DataFrame({
        'ID_Cliente': [1, 2, 3, 4, 5],
        'Nome_Cliente': ['Mario', 'Luigi', 'Peach', 'Bowser', 'Yoshi'],
        'Età': [35, 42, 28, 45, 30],
        'Città': ['Milano', 'Roma', 'Napoli', 'Torino', 'Venezia'],
        'Fatturato': [1500.50, 2300.75, 980.25, 3200.00, 1750.80]
    })

    # Salva come file Excel
    test_file = "test_clienti_dynamic.xlsx"
    test_data.to_excel(test_file, index=False)
    print(f"   ✅ File creato: {test_file}")

    # Leggi il file
    df_loaded = processor.read_excel_file(test_file)
    rows, cols = len(df_loaded), len(df_loaded.columns)
    print(f"   ✅ File letto: {rows} righe, {cols} colonne")

    # Salva nel database
    success = processor.save_to_database(df_loaded, "clienti_test")
    if success:
        print("   ✅ Salvataggio database riuscito")
    else:
        print("   ❌ Errore nel salvataggio")
        return False

    # Test 2: Verifica database
    print("\n🔍 Test 2: Verifica contenuto database")
    db_info = processor.get_database_info()

    for table in db_info["tables"]:
        name = table["name"]
        rows = table["rows"]
        cols = table["columns"]
        print(f"   📋 Tabella: {name}")
        print(f"      • Righe: {rows}")
        cols_preview = ', '.join(cols[:5])
        if len(cols) > 5:
            cols_preview += '...'
        print(f"      • Colonne: {cols_preview}")

    # Test 3: Query dati
    print("\n📈 Test 3: Query sui dati")
    try:
        query = "SELECT * FROM clienti_test WHERE Età > 30"
        result = processor.query_database(query)
        if result is not None:
            result_count = len(result)
            print(f"   ✅ Query eseguita: {result_count} risultati "
                  "(clienti > 30 anni)")

            # Mostra sample
            for i, row in result.head(2).iterrows():
                nome = row['Nome_Cliente']
                eta = row['Età']
                fatturato = row['Fatturato']
                print(f"      • {nome} ({eta} anni) - €{fatturato}")
        else:
            print("   ❌ Errore nella query")
            return False
    except Exception as e:
        print(f"   ❌ Errore query: {e}")
        return False

    # Test 4: File con molte colonne
    print("\n📊 Test 4: File con molte colonne")
    wide_data = pd.DataFrame({
        f'Col_{i}': [f'Valore_{i}_{j}' for j in range(10)]
        for i in range(15)  # 15 colonne
    })

    wide_file = "test_wide_columns.xlsx"
    wide_data.to_excel(wide_file, index=False)

    df_wide = processor.read_excel_file(wide_file)
    success_wide = processor.save_to_database(df_wide, "wide_test")

    if success_wide:
        cols_count = len(df_wide.columns)
        print(f"   ✅ File con {cols_count} colonne salvato correttamente")
    else:
        print("   ❌ Errore con file a molte colonne")
        return False

    # Cleanup
    for f in [test_file, wide_file]:
        if os.path.exists(f):
            os.remove(f)

    print("\n🎉 TUTTI I TEST SUPERATI!")
    print("✅ Database supporta colonne dinamiche")
    print("✅ Query funzionanti")
    print("✅ File Excel multipli gestiti correttamente")
    return True


def demo_database_features():
    """Dimostra le funzionalità del database"""
    print("\n🎯 DEMO FUNZIONALITÀ DATABASE")
    print("=" * 40)

    processor = ExcelProcessor()

    # Crea dati demo
    demo_data = pd.DataFrame({
        'Prodotto': ['Laptop', 'Mouse', 'Tastiera', 'Monitor'],
        'Prezzo': [899.99, 25.50, 75.00, 299.99],
        'Disponibilità': [15, 50, 30, 8],
        'Categoria': ['Computer', 'Accessori', 'Accessori', 'Monitor']
    })

    processor.save_to_database(demo_data, "prodotti_demo")

    # Query demo
    queries = [
        ("SELECT * FROM prodotti_demo", "Tutti i prodotti"),
        ("SELECT * FROM prodotti_demo WHERE Prezzo > 100", "Prodotti > €100"),
        ("SELECT Categoria, COUNT(*) as Conteggio FROM prodotti_demo "
         "GROUP BY Categoria", "Conteggio per categoria")
    ]

    for query, description in queries:
        print(f"\n📊 {description}:")
        try:
            result = processor.query_database(query)
            if result is not None and not result.empty:
                print(result.to_string(index=False))
            else:
                print("   Nessun risultato")
        except Exception as e:
            print(f"   Errore: {e}")


if __name__ == "__main__":
    try:
        if test_real_excel_integration():
            demo_database_features()
            print("\n🚀 INTEGRAZIONE DATABASE COMPLETAMENTE FUNZIONALE!")
        else:
            print("\n❌ Test falliti - controlla gli errori")
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")
