#!/usr/bin/env python3
"""
🏢 EXCELTOOLS PRO DATABASE MANAGER - ENTERPRISE EDITION
=======================================================

Sistema di gestione database professionale e interattivo
con funzionalità complete per query, filtri, esportazione e gestione dati.

Autore: Senior DB Manager IT DEV
Data: 2025-07-16
Versione: Enterprise 2.0
"""

import os
import sqlite3
import logging
from typing import List, Dict, Optional, Any

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class DatabaseManager:
    """Manager database professionale con funzionalità avanzate"""

    def __init__(self, db_path="exceltools_enterprise.db"):
        self.db_path = db_path
        self.setup_logging()
        self.setup_database()

    def setup_logging(self):
        """Configura logging professionale"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('exceltools_enterprise.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ExcelToolsEnterprise")

    def setup_database(self):
        """Inizializza database con tabelle enterprise"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tabella metadata per tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT UNIQUE,
                    source_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_rows INTEGER,
                    total_columns INTEGER,
                    description TEXT
                )
            """)

            # Tabella per query salvate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    query_sql TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_favorite BOOLEAN DEFAULT 0
                )
            """)

            conn.commit()
            conn.close()
            self.logger.info("Database enterprise inizializzato")
        except Exception as e:
            self.logger.error(f"Errore setup database: {e}")

    def import_excel_data(self, file_path: str, table_name: str = None,
                          sheet_names: List[str] = None) -> bool:
        """Importa dati Excel con gestione multi-sheet"""
        try:
            if not HAS_PANDAS:
                raise Exception("Pandas non disponibile")


            import re
            # Auto-genera nome tabella se non fornito
            if not table_name:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                # Sostituisci tutto ciò che non è lettera/numero con _
                safe_base = re.sub(r'[^a-zA-Z0-9]', '_', base_name)
                table_name = f"excel_{safe_base}".lower()

            # Leggi Excel con tutti i sheet
            excel_file = pd.ExcelFile(file_path)
            sheets_to_import = sheet_names or excel_file.sheet_names

            conn = sqlite3.connect(self.db_path)
            total_imported = 0


            for sheet_name in sheets_to_import:
                df = pd.read_excel(file_path, sheet_name=sheet_name)

                # Nome tabella con sheet, SQL-safe
                if len(sheets_to_import) > 1:
                    # Sostituisci tutto ciò che non è lettera/numero con _ anche per il nome sheet
                    safe_sheet = re.sub(r'[^a-zA-Z0-9]', '_', str(sheet_name))
                    sheet_table_name = f"{table_name}_{safe_sheet}".lower()
                else:
                    sheet_table_name = table_name

                # Pulisci nomi colonne
                df.columns = [
                    str(col).strip().replace(" ", "_").replace(
                        "(", "").replace(")", "").replace(
                        "/", "_").replace("-", "_")
                    for col in df.columns
                ]

                # Rimuovi righe completamente vuote
                df = df.dropna(how='all')

                # Sostituisci NaN con valori appropriati
                for col in df.columns:
                    if df[col].dtype == 'object':
                        df[col] = df[col].fillna('')
                    else:
                        df[col] = df[col].fillna(0)

                # Salva nel database
                df.to_sql(sheet_table_name, conn, if_exists='replace',
                          index=False)

                # Aggiorna metadata
                self.update_metadata(sheet_table_name, file_path,
                                     len(df), len(df.columns))

                total_imported += len(df)
                self.logger.info(
                    f"Importati {len(df)} record in {sheet_table_name}")

            conn.close()
            self.logger.info(
                f"Import completato: {total_imported} record totali")
            return True

        except Exception as e:
            self.logger.error(f"Errore import Excel: {e}")
            return False

    def update_metadata(self, table_name: str, source_file: str,
                        rows: int, columns: int):
        """Aggiorna metadata tabella"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO metadata
                (table_name, source_file, total_rows, total_columns,
                 updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (table_name, source_file, rows, columns))

            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Errore aggiornamento metadata: {e}")

    def get_all_tables(self) -> List[Dict[str, Any]]:
        """Ottiene lista completa tabelle con metadata"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT
                    t.name as table_name,
                    COALESCE(m.source_file, 'Unknown') as source_file,
                    COALESCE(m.total_rows, 0) as total_rows,
                    COALESCE(m.total_columns, 0) as total_columns,
                    COALESCE(m.created_at, 'Unknown') as created_at,
                    COALESCE(m.updated_at, 'Unknown') as updated_at
                FROM sqlite_master t
                LEFT JOIN metadata m ON t.name = m.table_name
                WHERE t.type = 'table'
                AND t.name NOT LIKE 'sqlite_%'
                AND t.name NOT IN ('metadata', 'saved_queries')
                ORDER BY m.updated_at DESC
            """

            cursor.execute(query)
            tables = []

            for row in cursor.fetchall():
                table_info = {
                    'name': row[0],
                    'source_file': row[1],
                    'total_rows': row[2],
                    'total_columns': row[3],
                    'created_at': row[4],
                    'updated_at': row[5]
                }

                # Ottieni colonne effettive
                cursor.execute(f"PRAGMA table_info({row[0]})")
                columns = [col[1] for col in cursor.fetchall()]
                table_info['columns'] = columns

                tables.append(table_info)

            conn.close()
            return tables

        except Exception as e:
            self.logger.error(f"Errore get tables: {e}")
            return []

    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """Esegue query SQL con gestione errori avanzata"""
        try:
            conn = sqlite3.connect(self.db_path)
            result = pd.read_sql_query(query, conn)
            conn.close()
            self.logger.info(f"Query eseguita: {len(result)} risultati")
            return result
        except Exception as e:
            self.logger.error(f"Errore query: {e}")
            return None

    def delete_records(self, table_name: str,
                       where_clause: str = None) -> bool:
        """Elimina record con clausola WHERE opzionale"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if where_clause:
                query = f"DELETE FROM {table_name} WHERE {where_clause}"
            else:
                query = f"DELETE FROM {table_name}"

            cursor.execute(query)
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            msg = f"Eliminati {deleted_count} record da {table_name}"
            self.logger.info(msg)
            return True

        except Exception as e:
            self.logger.error(f"Errore eliminazione: {e}")
            return False

    def export_query_result(self, query_result: pd.DataFrame,
                            file_path: str,
                            format_type: str = "excel") -> bool:
        """Esporta risultati query in vari formati"""
        try:
            if format_type.lower() == "excel":
                query_result.to_excel(file_path, index=False)
            elif format_type.lower() == "csv":
                query_result.to_csv(file_path, index=False)
            elif format_type.lower() == "json":
                query_result.to_json(file_path, orient='records', indent=2)
            else:
                raise ValueError(f"Formato non supportato: {format_type}")

            self.logger.info(f"Esportazione completata: {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Errore esportazione: {e}")
            return False

    def save_query(self, name: str, query_sql: str,
                   description: str = "") -> bool:
        """Salva query per riutilizzo futuro"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO saved_queries
                (name, query_sql, description)
                VALUES (?, ?, ?)
            """, (name, query_sql, description))

            conn.commit()
            conn.close()
            self.logger.info(f"Query salvata: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Errore salvataggio query: {e}")
            return False

    def get_saved_queries(self) -> List[Dict[str, Any]]:
        """Ottiene lista query salvate"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, query_sql, description, created_at,
                       is_favorite
                FROM saved_queries
                ORDER BY is_favorite DESC, created_at DESC
            """)

            queries = []
            for row in cursor.fetchall():
                queries.append({
                    'id': row[0],
                    'name': row[1],
                    'query_sql': row[2],
                    'description': row[3],
                    'created_at': row[4],
                    'is_favorite': bool(row[5])
                })

            conn.close()
            return queries

        except Exception as e:
            self.logger.error(f"Errore get saved queries: {e}")
            return []


class QueryBuilder:
    """Builder per costruire query SQL in modo visuale"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def build_select_query(self, table_name: str, columns: List[str] = None,
                           where_conditions: List[Dict] = None,
                           order_by: str = None, limit: int = None) -> str:
        """Costruisce query SELECT"""
        # Seleziona colonne
        if columns:
            cols = ", ".join(columns)
        else:
            cols = "*"

        query = f"SELECT {cols} FROM {table_name}"

        # Clausole WHERE
        if where_conditions:
            where_parts = []
            for condition in where_conditions:
                column = condition.get('column')
                operator = condition.get('operator', '=')
                value = condition.get('value')

                if isinstance(value, str):
                    part = f"{column} {operator} '{value}'"
                    where_parts.append(part)
                else:
                    part = f"{column} {operator} {value}"
                    where_parts.append(part)

            if where_parts:
                query += " WHERE " + " AND ".join(where_parts)

        # ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"

        # LIMIT
        if limit:
            query += f" LIMIT {limit}"

        return query

    def build_aggregation_query(self, table_name: str, group_by: str,
                                aggregations: List[Dict]) -> str:
        """Costruisce query di aggregazione"""
        agg_parts = []
        for agg in aggregations:
            func = agg.get('function', 'COUNT')
            column = agg.get('column', '*')
            alias = agg.get('alias', f"{func}_{column}")
            agg_parts.append(f"{func}({column}) as {alias}")

        agg_str = ", ".join(agg_parts)
        query = (f"SELECT {group_by}, {agg_str} FROM {table_name} "
                 f"GROUP BY {group_by}")

        return query


if __name__ == "__main__":
    # Test del sistema
    db_manager = DatabaseManager()
    print("🏢 ExcelTools Pro Database Manager Enterprise - Inizializzato")
    print("✅ Sistema pronto per l'uso professionale")
