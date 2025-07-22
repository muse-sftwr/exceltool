#!/usr/bin/env python3
"""
Script semplificato per generare file Excel di test
"""

import pandas as pd
import numpy as np


def create_simple_test_files():
    """Crea file Excel di test semplici e sicuri"""

    print("📊 Creando file di test per ExcelTools Pro...")

    # File 1: Vendite (semplificato)
    np.random.seed(42)
    sales_data = {
        'Data': pd.date_range('2024-01-01', periods=100, freq='D'),
        'Prodotto': np.random.choice(['Laptop', 'Mouse', 'Tastiera'], 100),
        'Quantità': np.random.randint(1, 10, 100),
        'Prezzo': np.random.uniform(10, 1000, 100).round(2),
        'Cliente': [f'Cliente_{i}' for i in range(1, 101)]
    }

    df_sales = pd.DataFrame(sales_data)
    df_sales['Totale'] = df_sales['Quantità'] * df_sales['Prezzo']
    df_sales.to_excel('test_vendite_simple.xlsx', index=False)
    print(f"✅ Creato: test_vendite_simple.xlsx ({len(df_sales)} righe)")

    # File 2: Inventario (semplificato)
    inventory_data = {
        'Codice': [f'PROD_{i:03d}' for i in range(1, 51)],
        'Nome': np.random.choice(['Laptop', 'Mouse', 'Tastiera', 'Monitor'], 50),
        'Scorte': np.random.randint(0, 100, 50),
        'Prezzo_Acquisto': np.random.uniform(50, 500, 50).round(2),
        'Prezzo_Vendita': np.random.uniform(100, 800, 50).round(2)
    }

    df_inventory = pd.DataFrame(inventory_data)
    df_inventory['Margine'] = (
        df_inventory['Prezzo_Vendita'] - df_inventory['Prezzo_Acquisto']
    )
    df_inventory.to_excel('test_inventario_simple.xlsx', index=False)
    print(f"✅ Creato: test_inventario_simple.xlsx ({len(df_inventory)} righe)")

    # File 3: Performance test (piccolo)
    perf_data = {
        'ID': range(1, 1001),
        'Timestamp': pd.date_range('2024-01-01', periods=1000, freq='H'),
        'Valore': np.random.randn(1000).round(3),
        'Categoria': np.random.choice(['A', 'B', 'C'], 1000),
        'Status': np.random.choice(['OK', 'Warning', 'Error'], 1000)
    }

    df_perf = pd.DataFrame(perf_data)
    df_perf.to_excel('test_performance_1k.xlsx', index=False)
    print(f"✅ Creato: test_performance_1k.xlsx ({len(df_perf)} righe)")

    print("\n🎉 File di test creati con successo!")
    print("📁 File disponibili:")
    print("   • test_vendite_simple.xlsx - Dati vendite (100 righe)")
    print("   • test_inventario_simple.xlsx - Inventario (50 righe)")
    print("   • test_performance_1k.xlsx - Performance test (1k righe)")


if __name__ == "__main__":
    create_simple_test_files()
