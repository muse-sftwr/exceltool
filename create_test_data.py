#!/usr/bin/env python3
"""
🔧 CREATORE FILE EXCEL DI TEST
=============================

Crea file Excel di esempio per testare ExcelTools Pro.

Autore: Test Data Engineer
Data: 2025-07-16
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def create_sample_excel():
    """Crea file Excel di esempio con dati realistici"""

    print("🔧 Creazione file Excel di test...")

    # Genera dati campione
    np.random.seed(42)
    random.seed(42)

    # Dataset vendite prodotti
    products = [
        "Laptop Dell XPS", "MacBook Pro", "iPad Air", "Samsung Galaxy",
        "iPhone 14", "Surface Pro", "ThinkPad X1", "Gaming PC",
        "Monitor 4K", "Tastiera Meccanica", "Mouse Wireless", "Webcam HD"
    ]

    regions = ["Nord", "Sud", "Centro", "Isole"]
    sales_reps = [
        "Mario Rossi", "Giulia Bianchi", "Luca Verde", "Anna Neri",
        "Paolo Blu", "Sara Rosa", "Marco Giallo", "Elena Viola"
    ]

    # Genera 500 righe di dati
    n_records = 500

    data = {
        'ID_Vendita': range(1, n_records + 1),
        'Data_Vendita': [
            (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            for _ in range(n_records)
        ],
        'Prodotto': [random.choice(products) for _ in range(n_records)],
        'Quantità': [random.randint(1, 10) for _ in range(n_records)],
        'Prezzo_Unitario': [
            round(random.uniform(50, 2000), 2) for _ in range(n_records)
        ],
        'Regione': [random.choice(regions) for _ in range(n_records)],
        'Venditore': [random.choice(sales_reps) for _ in range(n_records)],
        'Sconto_%': [round(random.uniform(0, 25), 1) for _ in range(n_records)],
        'Cliente_Premium': [random.choice([True, False]) for _ in range(n_records)],
        'Categoria': [
            random.choice(['Elettronica', 'Computer', 'Accessori', 'Mobile'])
            for _ in range(n_records)
        ]
    }

    # Calcola totale vendita
    df = pd.DataFrame(data)
    df['Totale_Vendita'] = df['Quantità'] * \
        df['Prezzo_Unitario'] * (1 - df['Sconto_%'] / 100)
    df['Totale_Vendita'] = df['Totale_Vendita'].round(2)

    # Aggiungi alcune righe con valori null per testare
    df.loc[random.sample(range(len(df)), 20), 'Sconto_%'] = np.nan
    df.loc[random.sample(range(len(df)), 15), 'Cliente_Premium'] = np.nan

    # Salva file
    filename = "vendite_esempio.xlsx"
    df.to_excel(filename, index=False)

    print(f"✅ File creato: {filename}")
    print(f"📊 Righe: {len(df)}")
    print(f"📋 Colonne: {len(df.columns)}")
    print(f"🔢 Colonne: {', '.join(df.columns)}")

    return filename, df


def create_multiple_sheets_excel():
    """Crea file Excel con più fogli"""

    print("\n🔧 Creazione file Excel multi-sheet...")

    with pd.ExcelWriter("dati_aziendali_esempio.xlsx") as writer:

        # Foglio 1: Vendite
        np.random.seed(42)
        vendite_data = {
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'] * 4,
            'Anno': [2023] * 12 + [2024] * 12,
            'Vendite_Euro': [random.randint(10000, 50000) for _ in range(24)],
            'Costi_Euro': [random.randint(5000, 25000) for _ in range(24)],
            'Profitto_%': [round(random.uniform(10, 40), 1) for _ in range(24)]
        }
        df_vendite = pd.DataFrame(vendite_data)
        df_vendite.to_excel(writer, sheet_name='Vendite_Mensili', index=False)

        # Foglio 2: Dipendenti
        dipendenti_data = {
            'ID_Dipendente': range(1, 51),
            'Nome': [f"Dipendente_{i}" for i in range(1, 51)],
            'Reparto': [random.choice(['Vendite', 'IT', 'HR', 'Marketing', 'Finanza']) for _ in range(50)],
            'Stipendio_Euro': [random.randint(25000, 80000) for _ in range(50)],
            'Anzianità_Anni': [random.randint(1, 20) for _ in range(50)],
            'Performance_Score': [round(random.uniform(3.0, 5.0), 1) for _ in range(50)]
        }
        df_dipendenti = pd.DataFrame(dipendenti_data)
        df_dipendenti.to_excel(writer, sheet_name='Dipendenti', index=False)

        # Foglio 3: Inventario
        prodotti_inventario = {
            'Codice_Prodotto': [f"PROD_{i:03d}" for i in range(1, 101)],
            'Nome_Prodotto': [f"Prodotto {i}" for i in range(1, 101)],
            'Categoria': [random.choice(['A', 'B', 'C', 'D']) for _ in range(100)],
            'Quantità_Stock': [random.randint(0, 1000) for _ in range(100)],
            'Prezzo_Acquisto': [round(random.uniform(10, 500), 2) for _ in range(100)],
            'Prezzo_Vendita': [round(random.uniform(15, 750), 2) for _ in range(100)],
            'Fornitore': [f"Fornitore_{random.randint(1, 10)}" for _ in range(100)]
        }
        df_inventario = pd.DataFrame(prodotti_inventario)
        df_inventario.to_excel(writer, sheet_name='Inventario', index=False)

    print("✅ File multi-sheet creato: dati_aziendali_esempio.xlsx")
    print("📄 Fogli: Vendite_Mensili, Dipendenti, Inventario")

    return "dati_aziendali_esempio.xlsx"


def main():
    """Crea file di esempio"""
    print("🔧 EXCELTOOLS PRO - CREATORE FILE DI TEST")
    print("=" * 50)

    try:
        # File singolo
        file1, df = create_sample_excel()

        # File multi-sheet
        file2 = create_multiple_sheets_excel()

        print(f"\n🎉 File di test creati con successo!")
        print(f"📁 File 1: {file1} ({len(df)} righe)")
        print(f"📁 File 2: {file2} (3 fogli)")
        print(f"\n💡 Ora puoi testare ExcelTools Pro importando questi file!")

    except Exception as e:
        print(f"❌ Errore creazione file: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
