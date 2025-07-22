"""
Modulo per la gestione delle query AI: traduzione da linguaggio naturale a SQL.
"""
# Può essere integrato con OpenAI, Azure OpenAI, o un modello locale.


class AIQueryEngine:
    def __init__(self, query_handler):
        self.query_handler = query_handler
        # Qui si può aggiungere la configurazione per OpenAI o altro modello

    def natural_language_to_sql(self, user_query, columns=None):
        """
        Simula la traduzione da linguaggio naturale a SQL.
        In produzione, integrare con un modello AI.
        """
        # MOCK: restituisce una query SQL di esempio
        if columns:
            select_cols = ', '.join(columns)
        else:
            select_cols = '*'
        # Esempio: "Mostra tutti i prodotti con prezzo > 100"
        if 'prezzo' in user_query.lower() and '>' in user_query:
            return f"SELECT {select_cols} FROM df WHERE prezzo > 100"
        # Default
        return f"SELECT {select_cols} FROM df LIMIT 10"

    def run_ai_query(self, user_query):
        columns = self.query_handler.get_columns()
        sql = self.natural_language_to_sql(user_query, columns)
        result, error = self.query_handler.run_query(sql)
        return sql, result, error
