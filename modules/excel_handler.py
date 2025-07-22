"""
Modulo per la gestione di file Excel: caricamento, salvataggio, filtri rapidi.
"""
import pandas as pd


class ExcelHandler:
    def __init__(self):
        self.df = None
        self.filtered_df = None
        self.filters = []  # Lista di tuple (colonna, operatore, valore)

    def load_excel(self, file_path):
        """Carica un file Excel in un DataFrame."""
        self.df = pd.read_excel(file_path)
        self.filtered_df = self.df.copy()
        self.filters = []
        return self.df

    def save_excel(self, file_path):
        """Salva il DataFrame filtrato su file Excel."""
        if self.filtered_df is not None:
            self.filtered_df.to_excel(file_path, index=False)

    def apply_filters(self, filters):
        """Applica filtri cumulativi e restituisce il DataFrame filtrato."""
        df = self.df.copy()
        for col, op, val in filters:
            if op == '=':
                df = df[df[col] == val]
            elif op == '!=':
                df = df[df[col] != val]
            elif op == '>':
                df = df[df[col] > val]
            elif op == '<':
                df = df[df[col] < val]
            elif op == '>=':
                df = df[df[col] >= val]
            elif op == '<=':
                df = df[df[col] <= val]
            elif op == 'contiene':
                df = df[df[col].astype(str).str.contains(
                    str(val), case=False, na=False
                )]
            elif op == 'non contiene':
                df = df[~df[col].astype(str).str.contains(
                    str(val), case=False, na=False
                )]
        self.filtered_df = df
        return df

    def clear_filters(self):
        self.filters = []
        self.filtered_df = self.df.copy()
        return self.filtered_df
