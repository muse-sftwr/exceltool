import pandas as pd
import numpy as np

# Genera dataset più grande per test performance
print("Generando dataset di test...")

# Dataset 1: 10,000 righe
data_large = {
    'ID': range(1, 10001),
        'Nome': [f'Cliente_{i}' for i in range(1, 10001)],
            'Valore_A': np.random.randint(1, 1000, 10000),
            'Valore_B': np.random.uniform(0, 100, 10000),
            'Categoria': np.random.choice(['A', 'B', 'C', 'D'], 10000),
            'Data': pd.date_range('2024-01-01', periods=10000, freq='H'),
            'Status': np.random.choice(['Attivo', 'Inattivo'], 10000)
        }

df_large = pd.DataFrame(data_large)
df_large.to_excel('test_10k.xlsx', index=False)

print("Creato test_10k.xlsx - 10,000 righe")

# Dataset 2: Dati finanziari
financial_data = {
    'Simbolo': np.random.choice([
        'AAPL',
            'GOOGL',
            'MSFT',
            'AMZN',
            'TSLA'
], 5000),
    'Data': pd.date_range('2023-01-01', periods=5000, freq='D'),
        'Prezzo_Apertura': np.random.uniform(100, 500, 5000),
            'Prezzo_Chiusura': np.random.uniform(100, 500, 5000),
            'Volume': np.random.randint(1000000, 50000000, 5000),
            'Variazione_Perc': np.random.uniform(-10, 10, 5000)
        }

df_financial = pd.DataFrame(financial_data)
df_financial.to_excel('test_financial.xlsx', index=False)

print("Creato test_financial.xlsx - 5,000 righe")

print("File di test creati con successo!")
print("Usa l'applicazione per caricare e testare questi file.")
