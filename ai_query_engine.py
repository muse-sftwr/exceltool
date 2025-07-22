
from ai_query_interpreter_clean import AdvancedAIQueryInterpreter


class AIQueryEngine(AdvancedAIQueryInterpreter):

    def interpret_query(self, user_input, filtered_data):
        # Estende interpret_query per restituire anche colonne mostrate
        # ed errori
        try:
            self.current_data = filtered_data
            sql = super().interpret_query(user_input)
            shown_cols = self._extract_shown_columns_from_query(sql)
            return sql, shown_cols, None
        except Exception as e:
            return '', None, str(e)

    def _extract_shown_columns_from_query(self, query_result):
        import re
        m = re.search(r'SELECT (.+?) FROM', query_result, re.IGNORECASE)
        if m:
            cols = m.group(1)
            cols = re.sub(
                r'\b(AVG|COUNT|SUM|MIN|MAX)\s*\(',
                '',
                cols,
                flags=re.IGNORECASE
            )
            cols = re.sub(
                r'\)',
                '',
                cols,
                flags=re.IGNORECASE
            )
            cols = [
                c.strip().strip('[]')
                for c in cols.split(',')
                if c.strip() and not c.strip().startswith('*')
            ]
            return cols
        return None
