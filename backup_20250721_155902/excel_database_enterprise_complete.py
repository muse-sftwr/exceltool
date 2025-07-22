#!/usr/bin/env python3
"""
🏢 EXCELTOOLS PRO DATABASE ENTERPRISE - SISTEMA COMPLETO
======================================================

Sistema professionale per gestione database con interfaccia interattiva,
query builder, filtri avanzati, esportazione flessibile e funzionalità
complete per l'interrogazione e manipolazione dei dati Excel.

Autore: Senior DB Manager IT DEV
Data: 2025-07-16
Versione: Enterprise Complete 3.0
"""

import os
import sqlite3
import threading
import logging
from typing import Any, Dict, List, Optional
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    HAS_CUSTOMTKINTER = True
except ImportError:
    HAS_CUSTOMTKINTER = False


class ExcelDatabaseEnterprise:
    """Sistema database enterprise completo"""

    def __init__(self, db_path="exceltools_enterprise.db"):
        self.db_path = db_path
        self.setup_logging()
        self.setup_database()
        self.current_table = None
        self.filter_conditions = []

    def setup_logging(self):
        """Configura logging professionale"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('database_enterprise.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("DatabaseEnterprise")

    def setup_database(self):
        """Inizializza database enterprise"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tabella metadata
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS table_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT UNIQUE,
                    source_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_rows INTEGER,
                    total_columns INTEGER,
                    description TEXT
                )
            """)

            # Tabella query salvate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    sql_query TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    is_favorite BOOLEAN DEFAULT 0
                )
            """)

            conn.commit()
            conn.close()
            self.logger.info("Database enterprise inizializzato con successo")

        except Exception as e:
            self.logger.error(f"Errore setup database: {e}")
            raise

    def import_excel_comprehensive(self, file_path: str,
                                  table_prefix: str = None) -> Dict[str, Any]:
        """Import Excel completo con gestione multi-sheet"""
        if not HAS_PANDAS:
            raise Exception("Pandas richiesto per import Excel")

        try:
            results = {
                'success': False,
                'tables_created': [],
                'total_rows': 0,
                'errors': []
            }

            # Auto-genera prefisso tabella
            if not table_prefix:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                table_prefix = f"excel_{base_name}".replace(" ", "_").lower()

            # Leggi tutti i sheet
            excel_file = pd.ExcelFile(file_path)
            conn = sqlite3.connect(self.db_path)

            for sheet_name in excel_file.sheet_names:
                try:
                    # Leggi sheet
                    df = pd.read_excel(file_path, sheet_name=sheet_name)

                    # Pulisci e prepara dati
                    df = self.clean_dataframe(df)

                    if df.empty:
                        continue

                    # Nome tabella
                    if len(excel_file.sheet_names) > 1:
                        table_name = f"{table_prefix}_{sheet_name}"
                    else:
                        table_name = table_prefix

                    table_name = self.clean_table_name(table_name)

                    # Salva nel database
                    df.to_sql(table_name, conn, if_exists='replace',
                             index=False, method='multi')

                    # Aggiorna metadata
                    self.update_table_metadata(table_name, file_path,
                                              len(df), len(df.columns))

                    results['tables_created'].append({
                        'name': table_name,
                        'sheet': sheet_name,
                        'rows': len(df),
                        'columns': len(df.columns)
                    })
                    results['total_rows'] += len(df)

                    self.logger.info(
                        f"Sheet '{sheet_name}' -> Tabella '{table_name}' "
                        f"({len(df)} righe)")

                except Exception as e:
                    error_msg = f"Errore sheet '{sheet_name}': {str(e)}"
                    results['errors'].append(error_msg)
                    self.logger.error(error_msg)

            conn.close()
            results['success'] = len(results['tables_created']) > 0

            self.logger.info(
                f"Import completato: {len(results['tables_created'])} "
                f"tabelle, {results['total_rows']} righe totali")

            return results

        except Exception as e:
            self.logger.error(f"Errore import Excel: {e}")
            return {
                'success': False,
                'tables_created': [],
                'total_rows': 0,
                'errors': [str(e)]
            }

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pulisce e prepara DataFrame per database"""
        # Rimuovi righe completamente vuote
        df = df.dropna(how='all')

        # Pulisci nomi colonne
        df.columns = [self.clean_column_name(str(col)) for col in df.columns]

        # Gestisci valori nulli
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')
            else:
                df[col] = df[col].fillna(0)

        return df

    def clean_column_name(self, name: str) -> str:
        """Pulisce nome colonna per SQL"""
        import re
        # Rimuovi caratteri speciali e sostituisci con underscore
        clean_name = re.sub(r'[^\w\s]', '', name)
        clean_name = re.sub(r'\s+', '_', clean_name.strip())

        # Assicura che inizi con lettera
        if clean_name and not clean_name[0].isalpha():
            clean_name = f"col_{clean_name}"

        return clean_name or "unnamed_column"

    def clean_table_name(self, name: str) -> str:
        """Pulisce nome tabella per SQL"""
        import re
        clean_name = re.sub(r'[^\w]', '_', name.lower())
        return clean_name[:50]  # Limita lunghezza

    def update_table_metadata(self, table_name: str, source_file: str,
                             rows: int, columns: int):
        """Aggiorna metadata tabella"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO table_metadata
                (table_name, source_file, total_rows, total_columns)
                VALUES (?, ?, ?, ?)
            """, (table_name, source_file, rows, columns))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Errore aggiornamento metadata: {e}")

    def get_all_tables_info(self) -> List[Dict[str, Any]]:
        """Ottiene informazioni complete su tutte le tabelle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Query per ottenere tabelle con metadata
            query = """
                SELECT
                    t.name as table_name,
                    COALESCE(m.source_file, 'Unknown') as source_file,
                    COALESCE(m.total_rows, 0) as total_rows,
                    COALESCE(m.total_columns, 0) as total_columns,
                    COALESCE(m.created_at, 'Unknown') as created_at
                FROM sqlite_master t
                LEFT JOIN table_metadata m ON t.name = m.table_name
                WHERE t.type = 'table'
                AND t.name NOT LIKE 'sqlite_%'
                AND t.name NOT IN ('table_metadata', 'saved_queries')
                ORDER BY m.created_at DESC
            """

            cursor.execute(query)
            tables_info = []

            for row in cursor.fetchall():
                table_name = row[0]

                # Ottieni informazioni colonne
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                # Ottieni conteggio attuale righe
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                current_rows = cursor.fetchone()[0]

                table_info = {
                    'name': table_name,
                    'source_file': row[1],
                    'total_rows': current_rows,
                    'total_columns': len(columns),
                    'created_at': row[4],
                    'columns': columns
                }

                tables_info.append(table_info)

            conn.close()
            return tables_info

        except Exception as e:
            self.logger.error(f"Errore get tables info: {e}")
            return []

    def execute_advanced_query(self, query: str) -> Optional[pd.DataFrame]:
        """Esegue query con gestione avanzata errori"""
        try:
            # Validazione base query
            if not query.strip():
                raise ValueError("Query vuota")

            # Log della query (troncata se troppo lunga)
            query_log = query[:100] + "..." if len(query) > 100 else query
            self.logger.info(f"Eseguendo query: {query_log}")

            conn = sqlite3.connect(self.db_path)
            result = pd.read_sql_query(query, conn)
            conn.close()

            self.logger.info(f"Query completata: {len(result)} risultati")
            return result

        except Exception as e:
            self.logger.error(f"Errore query: {e}")
            return None

    def build_filtered_query(self, table_name: str,
                           columns: List[str] = None,
                           filters: List[Dict[str, Any]] = None,
                           order_by: str = None,
                           limit: int = None) -> str:
        """Costruisce query con filtri avanzati"""
        # Seleziona colonne
        if columns:
            cols_str = ", ".join(f"[{col}]" for col in columns)
        else:
            cols_str = "*"

        query = f"SELECT {cols_str} FROM [{table_name}]"

        # Applica filtri
        if filters:
            conditions = []
            for f in filters:
                column = f['column']
                operator = f.get('operator', '=')
                value = f['value']

                if operator.upper() == 'LIKE':
                    conditions.append(f"[{column}] LIKE '%{value}%'")
                elif operator.upper() == 'IN':
                    if isinstance(value, list):
                        value_list = "','".join(str(v) for v in value)
                        conditions.append(f"[{column}] IN ('{value_list}')")
                elif isinstance(value, str):
                    conditions.append(f"[{column}] {operator} '{value}'")
                else:
                    conditions.append(f"[{column}] {operator} {value}")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        # ORDER BY
        if order_by:
            query += f" ORDER BY [{order_by}]"

        # LIMIT
        if limit and limit > 0:
            query += f" LIMIT {limit}"

        return query

    def get_column_statistics(self, table_name: str,
                            column_name: str) -> Dict[str, Any]:
        """Ottiene statistiche per una colonna"""
        try:
            conn = sqlite3.connect(self.db_path)

            # Statistiche base
            query = f"""
                SELECT
                    COUNT(*) as total_count,
                    COUNT([{column_name}]) as non_null_count,
                    COUNT(DISTINCT [{column_name}]) as unique_count
                FROM [{table_name}]
            """

            stats = pd.read_sql_query(query, conn).iloc[0].to_dict()

            # Valori più frequenti
            top_values_query = f"""
                SELECT [{column_name}] as value, COUNT(*) as frequency
                FROM [{table_name}]
                WHERE [{column_name}] IS NOT NULL AND [{column_name}] != ''
                GROUP BY [{column_name}]
                ORDER BY frequency DESC
                LIMIT 10
            """

            top_values = pd.read_sql_query(top_values_query, conn)
            stats['top_values'] = top_values.to_dict('records')

            # Statistiche numeriche se applicabile
            try:
                numeric_query = f"""
                    SELECT
                        MIN(CAST([{column_name}] AS REAL)) as min_value,
                        MAX(CAST([{column_name}] AS REAL)) as max_value,
                        AVG(CAST([{column_name}] AS REAL)) as avg_value
                    FROM [{table_name}]
                    WHERE [{column_name}] IS NOT NULL
                """
                numeric_stats = pd.read_sql_query(numeric_query, conn).iloc[0]
                stats.update(numeric_stats.to_dict())
            except Exception:
                pass  # Non è una colonna numerica

            conn.close()
            return stats

        except Exception as e:
            self.logger.error(f"Errore statistiche colonna: {e}")
            return {}

    def delete_records_advanced(self, table_name: str,
                               conditions: List[Dict[str, Any]]) -> int:
        """Elimina record con condizioni avanzate"""
        try:
            if not conditions:
                raise ValueError("Condizioni richieste per eliminazione")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Costruisci WHERE clause
            where_parts = []
            for condition in conditions:
                column = condition['column']
                operator = condition.get('operator', '=')
                value = condition['value']

                if isinstance(value, str):
                    where_parts.append(f"[{column}] {operator} '{value}'")
                else:
                    where_parts.append(f"[{column}] {operator} {value}")

            where_clause = " AND ".join(where_parts)
            query = f"DELETE FROM [{table_name}] WHERE {where_clause}"

            cursor.execute(query)
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            self.logger.info(f"Eliminati {deleted_count} record da {table_name}")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Errore eliminazione: {e}")
            return 0

    def export_flexible(self, data: pd.DataFrame, file_path: str,
                       export_format: str = "excel",
                       options: Dict[str, Any] = None) -> bool:
        """Esportazione flessibile in vari formati"""
        try:
            options = options or {}

            if export_format.lower() == "excel":
                # Excel con opzioni avanzate
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    data.to_excel(writer, sheet_name='Data', index=False)

                    # Aggiungi formattazione se richiesta
                    if options.get('add_formatting', False):
                        workbook = writer.book
                        worksheet = writer.sheets['Data']

                        # Header formatting
                        header_format = workbook.create_format({
                            'bold': True,
                            'bg_color': '#4F81BD',
                            'font_color': 'white'
                        })

                        for col_num, value in enumerate(data.columns.values):
                            worksheet.write(0, col_num, value, header_format)

            elif export_format.lower() == "csv":
                separator = options.get('separator', ',')
                data.to_csv(file_path, index=False, sep=separator)

            elif export_format.lower() == "json":
                orient = options.get('orient', 'records')
                data.to_json(file_path, orient=orient, indent=2)

            elif export_format.lower() == "html":
                data.to_html(file_path, index=False, escape=False)

            else:
                raise ValueError(f"Formato non supportato: {export_format}")

            self.logger.info(f"Esportazione completata: {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Errore esportazione: {e}")
            return False

    def save_query_advanced(self, name: str, query: str,
                          description: str = "",
                          is_favorite: bool = False) -> bool:
        """Salva query con opzioni avanzate"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO saved_queries
                (name, sql_query, description, is_favorite, last_used)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (name, query, description, is_favorite))

            conn.commit()
            conn.close()

            self.logger.info(f"Query salvata: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Errore salvataggio query: {e}")
            return False

    def get_saved_queries(self) -> List[Dict[str, Any]]:
        """Ottiene query salvate con informazioni complete"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, sql_query, description, created_at,
                       last_used, is_favorite
                FROM saved_queries
                ORDER BY is_favorite DESC, last_used DESC, created_at DESC
            """)

            queries = []
            for row in cursor.fetchall():
                queries.append({
                    'id': row[0],
                    'name': row[1],
                    'sql_query': row[2],
                    'description': row[3],
                    'created_at': row[4],
                    'last_used': row[5],
                    'is_favorite': bool(row[6])
                })

            conn.close()
            return queries

        except Exception as e:
            self.logger.error(f"Errore get saved queries: {e}")
            return []

    def optimize_database(self) -> Dict[str, Any]:
        """Ottimizza database e restituisce statistiche"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # VACUUM per ottimizzare spazio
            cursor.execute("VACUUM")

            # ANALYZE per aggiornare statistiche
            cursor.execute("ANALYZE")

            # Ottieni statistiche post-ottimizzazione
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]

            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]

            database_size = page_count * page_size

            conn.close()

            stats = {
                'success': True,
                'database_size_bytes': database_size,
                'database_size_mb': round(database_size / (1024 * 1024), 2),
                'page_count': page_count,
                'page_size': page_size
            }

            self.logger.info("Database ottimizzato con successo")
            return stats

        except Exception as e:
            self.logger.error(f"Errore ottimizzazione: {e}")
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    # Test del sistema
    print("🏢 ExcelTools Pro Database Enterprise - Sistema Completo")
    print("=" * 60)

    db = ExcelDatabaseEnterprise()
    print("✅ Database enterprise inizializzato")

    # Test delle funzionalità
    tables = db.get_all_tables_info()
    print(f"📊 Tabelle disponibili: {len(tables)}")

    for table in tables:
        print(f"   • {table['name']} ({table['total_rows']} righe)")

    print("\n🚀 Sistema pronto per utilizzo professionale!")
