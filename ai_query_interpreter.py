
import re
from typing import List

class AdvancedAIQueryInterpreter:
    def __init__(self):
        self.current_data = None
        self.imported_files = {}

    def interpret_query(self, user_input: str) -> str:
        if not user_input:
            return "-- Inserisci una richiesta in linguaggio naturale"
        input_lower = user_input.lower().strip()
        if self.current_data is None:
            return "-- Carica prima dei dati per utilizzare l'AI Query Builder"
        try:
            columns = list(self.current_data.columns)
            numeric_cols = list(self.current_data.select_dtypes(include=['number']).columns)
            text_cols = list(self.current_data.select_dtypes(include=['object', 'string']).columns)
            table_name = list(self.imported_files.keys())[0] if self.imported_files else 'data'
            if any(word in input_lower for word in ['mostra', 'show', 'seleziona', 'select', 'visualizza', 'dammi']):
                mentioned_cols = self._find_mentioned_columns(input_lower, columns)
                if mentioned_cols:
                    cols_str = ", ".join(f"[{col}]" for col in mentioned_cols)
                    solo_words = ['solo', 'only', 'soltanto', 'unicamente']
                    if any(word in input_lower for word in solo_words):
                        return f"-- Mostra solo: {', '.join(mentioned_cols)}\nSELECT {cols_str} FROM [{table_name}];"
                    else:
                        return f"-- Mostra colonne: {', '.join(mentioned_cols)}\nSELECT {cols_str} FROM [{table_name}];"
                elif any(word in input_lower for word in ['tutto', 'all', 'tutti', 'completo']):
                    return f"-- Mostra tutti i dati\nSELECT * FROM [{table_name}];"
            if any(word in input_lower for word in ['filtra', 'filter', 'dove', 'where', 'condizione', 'condizioni']):
                return self._generate_filter_query(input_lower, columns, numeric_cols, text_cols, table_name)
            if any(word in input_lower for word in ['raggruppa', 'group', 'per', 'by', 'gruppo', 'group by']):
                return self._generate_group_query(input_lower, text_cols, numeric_cols, table_name)
            if any(word in input_lower for word in ['ordina', 'sort', 'ordine', 'order', 'crescente', 'decrescente', 'asc', 'desc']):
                return self._generate_sort_query(input_lower, columns, numeric_cols, text_cols, table_name)
            if any(word in input_lower for word in ['primi', 'ultimi', 'top', 'first', 'last', 'migliori']):
                return self._generate_limit_query(input_lower, columns, numeric_cols, table_name)
            if any(word in input_lower for word in ['media', 'average', 'mean', 'somma', 'sum', 'totale', 'conta', 'count', 'numero']):
                return self._generate_stats_query(input_lower, numeric_cols, text_cols, table_name)
            if any(word in input_lower for word in ['null', 'mancanti', 'missing', 'vuoti', 'empty']):
                return self._generate_null_query(columns, table_name)
            return self._generate_default_query(numeric_cols, text_cols, table_name)
        except Exception as e:
            return f"-- Errore interpretazione query: {e}"

    def _find_mentioned_columns(self, input_text: str, columns: List[str]) -> List[str]:
        mentioned = []
        for col in columns:
            if col.lower() in input_text:
                mentioned.append(col)
        return mentioned

    def _generate_filter_query(self, input_text: str, columns: List[str], numeric_cols: List[str], text_cols: List[str], table_name: str) -> str:
        query = f"SELECT * FROM [{table_name}] WHERE "
        numbers = re.findall(r'\d+', input_text)
            if col.lower() in input_text:
                return f"-- Ordina per {col} ({direction})\nSELECT * FROM [{table_name}] ORDER BY [{col}] {direction};"
        order_col = numeric_cols[0] if numeric_cols else columns[0]
        return f"-- Ordina per {order_col}\nSELECT * FROM [{table_name}] ORDER BY [{order_col}] {direction};"

    def _generate_limit_query(self, input_text: str, columns: List[str], numeric_cols: List[str], table_name: str) -> str:
        numbers = re.findall(r'\d+', input_text)
        limit = numbers[0] if numbers else '10'
        if any(word in input_text for word in ['primi', 'top', 'first', 'migliori']):
            if numeric_cols:
                order_col = numeric_cols[0]
                return f"-- Primi {limit} record per {order_col}\nSELECT TOP {limit} * FROM [{table_name}] ORDER BY [{order_col}] DESC;"
            else:
                return f"-- Primi {limit} record\nSELECT TOP {limit} * FROM [{table_name}];"
        else:
            if numeric_cols:
                order_col = numeric_cols[0]
                return f"-- Ultimi {limit} record per {order_col}\nSELECT TOP {limit} * FROM [{table_name}] ORDER BY [{order_col}] ASC;"
            else:
                return f"-- Ultimi {limit} record\nSELECT TOP {limit} * FROM [{table_name}] ORDER BY 1 DESC;"

    def _generate_stats_query(self, input_text: str, numeric_cols: List[str], text_cols: List[str], table_name: str) -> str:
        if any(word in input_text for word in ['media', 'average', 'mean']):
            if numeric_cols:
                if len(numeric_cols) == 1:
                    return f"-- Media di {numeric_cols[0]}\nSELECT AVG([{numeric_cols[0]}]) as Media FROM [{table_name}];"
                else:
                    avg_cols = ", ".join(f"AVG([{col}]) as Media_{col}" for col in numeric_cols[:3])
                    return f"-- Medie colonne numeriche\nSELECT {avg_cols} FROM [{table_name}];"
            else:
                return f"-- Nessuna colonna numerica per calcolare la media\nSELECT COUNT(*) as Totale_Righe FROM [{table_name}];"
        elif any(word in input_text for word in ['somma', 'sum', 'totale']):
            if numeric_cols:
                sum_cols = ", ".join(f"SUM([{col}]) as Totale_{col}" for col in numeric_cols[:3])
                return f"-- Somme colonne numeriche\nSELECT {sum_cols} FROM [{table_name}];"
            else:
                return f"-- Nessuna colonna numerica per calcolare la somma\nSELECT COUNT(*) as Totale_Righe FROM [{table_name}];"
        elif any(word in input_text for word in ['conta', 'count', 'numero']):
            if text_cols:
                return f"-- Conta valori unici in {text_cols[0]}\nSELECT COUNT(DISTINCT [{text_cols[0]}]) as Distinti FROM [{table_name}];"
            else:
                return f"-- Conta totale righe\nSELECT COUNT(*) as Totale_Righe FROM [{table_name}];"
        return f"-- Esempio statistica\nSELECT COUNT(*) as Totale_Righe FROM [{table_name}];"

    def _generate_null_query(self, columns: List[str], table_name: str) -> str:
        null_checks = " OR ".join(f"[{col}] IS NULL" for col in columns[:5])
        return f"-- Trova righe con valori mancanti\nSELECT * FROM [{table_name}] WHERE {null_checks};"

    def _generate_default_query(self, numeric_cols: List[str], text_cols: List[str], table_name: str) -> str:
        if numeric_cols and text_cols:
            return f"-- Analisi generale dei dati\nSELECT [{text_cols[0]}], COUNT(*) as Conteggio, AVG([{numeric_cols[0]}]) as Media FROM [{table_name}] GROUP BY [{text_cols[0]}] ORDER BY Conteggio DESC;"
        elif numeric_cols:
            stats_cols = ", ".join(f"AVG([{col}]) as Media_{col}, MIN([{col}]) as Min_{col}, MAX([{col}]) as Max_{col}" for col in numeric_cols[:2])
            return f"-- Statistiche colonne numeriche\nSELECT {stats_cols} FROM [{table_name}];"
        else:
            return f"-- Panoramica dati\nSELECT TOP 100 * FROM [{table_name}];"
