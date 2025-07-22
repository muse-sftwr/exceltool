import pandas as pd
import numpy as np

# Dati di esempio semplici
data = {
    'Nome': ['Mario', 'Luca', 'Sara', 'Anna', 'Paolo'] * 200,
    'Età': np.random.randint(20, 65, 1000),
    'Stipendio': np.random.randint(25000, 80000, 1000),
    'Dipartimento': ['IT', 'HR', 'Sales', 'Marketing', 'Finance'] * 200,
    'Città': ['Milano', 'Roma', 'Torino', 'Napoli', 'Bologna'] * 200
}

df = pd.DataFrame(data)
df.to_excel('test_data.xlsx', index=False)
print("File test_data.xlsx creato con successo!")
