"""
Modulo per parsing, esecuzione e validazione query SQL-like su DataFrame.
"""
import pandasql
import sqlparse


class QueryHandler:
    def __init__(self, excel_handler):
        self.excel_handler = excel_handler

    def run_query(self, query):
        """Esegue una query SQL-like sul DataFrame filtrato."""
        try:
            # Parsing e validazione
            parsed = sqlparse.parse(query)
            if not parsed:
                return None, 'Query vuota o non valida.'
            # Esegui query su DataFrame filtrato
            df = self.excel_handler.filtered_df
            result = pandasql.sqldf(query, {'df': df})
            return result, None
        except Exception as e:
            return None, f'Errore query: {str(e)}'

    def get_columns(self):
        """Restituisce la lista delle colonne disponibili."""
        if self.excel_handler.filtered_df is not None:
            return list(self.excel_handler.filtered_df.columns)
        return []
