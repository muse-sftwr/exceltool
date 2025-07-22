#!/usr/bin/env python3
"""

Script per generare file Excel di test per ExcelTools

"""

import pandas as pd
import numpy as np


def create_sample_excel_files():
    """Crea file Excel di esempio per testare ExcelTools"""

    # File 1: Dati vendite
    np.random.seed(42)
    dates = \
        pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

    sales_data = {
        'Data': np.random.choice(dates, 1000),
            'Prodotto': np.random.choice([
                'Laptop',
                    'Mouse',
            'Tastiera',
            'Monitor',
            'Cuffie'
], 1000),
    'Categoria': np.random.choice([
            'Elettronica', 'Accessori', 'Computer'
    ], 1000),
        'Quantità': np.random.randint(1, 100, 1000),
            'Prezzo': np.round(np.random.uniform(10, 1000, 1000), 2),
                'Cliente': [f'Cliente_{i}' for i in np.random.randint(1, 200, 1000)],
                'Regione': np.random.choice([
                'Nord',
                    'Sud',
                    'Centro',
                    'Isole'
            ], 1000),
                'Venditore': np.random.choice([
                'Mario',
                    'Luca',
            'Sara',
            'Anna',
            'Paolo'
], 1000)
    }

    df_sales = pd.DataFrame(sales_data)
    df_sales['Totale'] = df_sales['Quantità'] * df_sales['Prezzo']
    df_sales = df_sales.sort_values('Data')

    df_sales.to_excel('test_vendite.xlsx', index=False)
    print(f"Creato: test_vendite.xlsx ({len(df_sales)} righe)")

    # File 2: Inventario
    products = [
        'Laptop',
            'Mouse',
            'Tastiera',
            'Monitor',
            'Cuffie',
            'Webcam',
            'Speaker',
            'Tablet'
]
    inventory_data = {
        'Codice_Prodotto': [f'PROD_{i:04d}' for i in range(1, \
            len(products) * 50)],
                'Nome_Prodotto': np.random.choice(products, len(products) * 49),
                    'Categoria': np.random.choice([
                'Hardware',
                    'Accessori',
                    'Audio/Video'
            ], len(products) * 49),
                'Scorte': np.random.randint(0, 500, len(products) * 49),
                'Prezzo_Acquisto': np.round(np.random.uniform(5, 800, len(products) * 49), 2),
                'Prezzo_Vendita': np.round(np.random.uniform(10, 1200, len(products) * 49), 2),
                'Fornitore': np.random.choice([
                'Fornitore_A',
                    'Fornitore_B',
                    'Fornitore_C'
            ], len(products) * 49),
                'Data_Ultimo_Carico': pd.date_range(
                start='2024-01-01',
                    periods=len(products) * 49,
                    freq='D'
        )
    }

    df_inventory = pd.DataFrame(inventory_data)
    df_inventory['Margine'] = df_inventory['Prezzo_Vendita'] - \
        df_inventory['Prezzo_Acquisto']

    df_inventory.to_excel('test_inventario.xlsx', index=False)
    print(f"Creato: test_inventario.xlsx ({len(df_inventory)} righe)")

    # File 3: File grande per test performance
    print("Creando file di test performance (50k righe)...")
    large_data = {
        'ID': range(1, 50001),
            'Timestamp': pd.date_range(
                start='2024-01-01',
                    periods=50000,
                    freq='H'
        ),
            'Valore_A': np.random.randn(50000),
                'Valore_B': np.random.randn(50000),
                'Categoria': np.random.choice([
                'Cat1',
                    'Cat2',
            'Cat3',
            'Cat4',
            'Cat5'
], 50000),
    'Status': np.random.choice(['Attivo', 'Inattivo', 'Pending'], 50000),
            'Metrica_1': np.random.uniform(0, 100, 50000),
                'Metrica_2': np.random.uniform(-50, 50, 50000),
                'Note': [f'Nota_{i}' for i in range(50000)]
    }

    df_large = pd.DataFrame(large_data)
    df_large.to_excel('test_performance_50k.xlsx', index=False)
    print(f"Creato: test_performance_50k.xlsx ({len(df_large)} righe)")

    print("\n=== File di test creati con successo! ===")
    print("Usa questi file per testare ExcelTools:")
    print("1. test_vendite.xlsx - Dati vendite (1k righe)")
    print("2. test_inventario.xlsx - Dati inventario (400+ righe)")
    print("3. test_performance_50k.xlsx - Test performance (50k righe)")


if __name__ == "__main__":
    create_sample_excel_files()
