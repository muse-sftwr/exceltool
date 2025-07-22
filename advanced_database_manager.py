#!/usr/bin/env python3
"""
🏢 EXCELTOOLS PRO - ADVANCED DATABASE MANAGER
============================================

Sistema avanzato di gestione database con interfaccia grafica per
selezione dati, query builder visuale, merge di file e gestione
viste salvate.

Autore: Senior DB IT Manager Developer & DevOps Analyst
Data: 2025-07-16
Versione: Advanced 4.0
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
import tkinter as tk
from tkinter import ttk, messagebox

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


class AdvancedDatabaseManager:
    """Manager database avanzato con funzionalità enterprise"""

    def __init__(self, db_path="exceltools_advanced.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Inizializza database con tabelle avanzate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabella per viste salvate
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                table_name TEXT,
                selected_columns TEXT,
                filters TEXT,
                query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0,
                view_type TEXT DEFAULT 'custom'
            )
        """)

        # Tabella per configurazioni merge
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS merge_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                source_tables TEXT,
                join_conditions TEXT,
                merge_type TEXT,
                output_columns TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabella per filtri predefiniti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filter_presets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                table_name TEXT,
                filter_conditions TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        conn.commit()
        conn.close()

    def save_view(self, name: str, table_name: str,
                  selected_columns: List[str], filters: List[Dict],
                  description: str = "", is_favorite: bool = False) -> bool:
        """Salva una vista personalizzata"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Genera query dalla configurazione
            query = self.build_query_from_config(
                table_name, selected_columns, filters)

            cursor.execute("""
                INSERT OR REPLACE INTO saved_views
                (name, description, table_name, selected_columns, filters,
                 query, is_favorite, last_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                name, description, table_name,
                json.dumps(selected_columns), json.dumps(filters),
                query, is_favorite
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Errore salvataggio vista: {e}")
            return False

    def get_saved_views(self) -> List[Dict[str, Any]]:
        """Ottiene tutte le viste salvate"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, description, table_name, selected_columns,
                       filters, query, created_at, last_used, is_favorite
                FROM saved_views
                ORDER BY is_favorite DESC, last_used DESC
            """)

            views = []
            for row in cursor.fetchall():
                views.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'table_name': row[3],
                    'selected_columns': json.loads(row[4] or '[]'),
                    'filters': json.loads(row[5] or '[]'),
                    'query': row[6],
                    'created_at': row[7],
                    'last_used': row[8],
                    'is_favorite': bool(row[9])
                })

            conn.close()
            return views

        except Exception as e:
            print(f"Errore recupero viste: {e}")
            return []

    def save_merge_config(
        self,
        name: str,
        source_tables: List[str],
        join_conditions: List[Dict],
        merge_type: str,
        output_columns: List[str],
        description: str = ""
    ) -> bool:
        """Salva configurazione merge"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO merge_configs
                (name, description, source_tables, join_conditions,
                 merge_type, output_columns)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, description, json.dumps(source_tables),
                json.dumps(join_conditions), merge_type,
                json.dumps(output_columns)
            ))

            conn.commit()
            conn.close()
            cursor.execute(
                """
                INSERT OR REPLACE INTO merge_configs
                (name, description, source_tables, join_conditions,
                 merge_type, output_columns)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    description,
                    json.dumps(source_tables),
                    json.dumps(join_conditions),
                    merge_type,
                    json.dumps(output_columns)
                )
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, description, source_tables, join_conditions,
                       merge_type, output_columns, created_at
                FROM merge_configs
                ORDER BY created_at DESC
            """)

            configs = []
            for row in cursor.fetchall():
                configs.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'source_tables': json.loads(row[3] or '[]'),
                    'join_conditions': json.loads(row[4] or '[]'),
                    'merge_type': row[5],
                    'output_columns': json.loads(row[6] or '[]'),
                    'created_at': row[7]
                })

            conn.close()
            return configs

        except Exception as e:
            print(f"Errore recupero config merge: {e}")
            return []

    def execute_merge(self, config: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """Esegue merge basato su configurazione"""
        try:
            if not HAS_PANDAS:
                raise Exception("Pandas richiesto per merge")

            source_tables = config['source_tables']
            join_conditions = config['join_conditions']
            # merge_type = config['merge_type']  # Unused variable removed

            if len(source_tables) < 2:
                raise Exception("Almeno 2 tabelle richieste per merge")

            conn = sqlite3.connect(self.db_path)

            # Carica prima tabella
            df_result = pd.read_sql_query(
                f"SELECT * FROM [{source_tables[0]}]", conn)

            # Merge con tabelle successive
            for i, table in enumerate(source_tables[1:], 1):
                df_next = pd.read_sql_query(f"SELECT * FROM [{table}]", conn)

                # Trova condizione join per questa tabella
                join_condition = None
                for jc in join_conditions:
                    if jc.get('right_table') == table:
                        join_condition = jc
                        break

                if join_condition:
                    left_on = join_condition.get('left_column')
                    right_on = join_condition.get('right_column')
                    how = join_condition.get('join_type', 'inner')

                    df_result = df_result.merge(
                        df_next, left_on=left_on, right_on=right_on, how=how)

            conn.close()

            # Filtra colonne output se specificate
            output_columns = config.get('output_columns')
            if output_columns and all(col in df_result.columns
                                      for col in output_columns):
                df_result = df_result[output_columns]

            return df_result

        except Exception as e:
            print(f"Errore esecuzione merge: {e}")
            return None

    def build_query_from_config(self, table_name: str,
                                selected_columns: List[str],
                                filters: List[Dict]) -> str:
        """Costruisce query SQL da configurazione visuale"""
        # Seleziona colonne
        if selected_columns:
            cols = ", ".join(f"[{col}]" for col in selected_columns)
        else:
            cols = "*"

        query = f"SELECT {cols} FROM [{table_name}]"

        # Applica filtri
        if filters:
            conditions = []
            for f in filters:
                column = f['column']
                operator = f['operator']
                value = f['value']

                if operator == 'LIKE':
                    conditions.append(f"[{column}] LIKE '%{value}%'")
                elif operator == 'IN':
                    if isinstance(value, list):
                        values_str = "','".join(str(v) for v in value)
                        conditions.append(f"[{column}] IN ('{values_str}')")
                elif operator in ['IS NULL', 'IS NOT NULL']:
                    conditions.append(f"[{column}] {operator}")
                elif isinstance(value, str):
                    conditions.append(f"[{column}] {operator} '{value}'")
                else:
                    conditions.append(f"[{column}] {operator} {value}")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        return query

    def get_all_tables_with_details(self) -> List[Dict[str, Any]]:
        """Ottiene dettagli completi di tutte le tabelle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Lista tabelle utente
            cursor.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                AND name NOT IN ('saved_views', 'merge_configs',
                                'filter_presets')
                ORDER BY name
                """
            )

            tables = []
            for (table_name,) in cursor.fetchall():
                # Info colonne
                cursor.execute(f"PRAGMA table_info([{table_name}])")
                columns_info = cursor.fetchall()

                columns = []
                for col_info in columns_info:
                    columns.append({
                        'name': col_info[1],
                        'type': col_info[2],
                        'not_null': bool(col_info[3]),
                        'pk': bool(col_info[5])
                    })

                # Conteggio righe
                cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
                row_count = cursor.fetchone()[0]

                # Sample data per preview
                cursor.execute(f"SELECT * FROM [{table_name}] LIMIT 3")
                sample_data = cursor.fetchall()

                tables.append({
                    'name': table_name,
                    'columns': columns,
                    'row_count': row_count,
                    'sample_data': sample_data
                })

            conn.close()
            return tables

        except Exception as e:
            print(f"Errore get tables details: {e}")
            return []

    def get_column_unique_values(
            self,
            table_name: str,
            column_name: str,
            limit: int = 100) -> List[str]:
        """Ottiene valori unici di una colonna per filtri"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT DISTINCT [{column_name}]
                FROM [{table_name}]
                WHERE [{column_name}] IS NOT NULL
                ORDER BY [{column_name}]
                LIMIT {limit}
            """)

            values = [str(row[0]) for row in cursor.fetchall()]
            conn.close()
            return values

        except Exception as e:
            print(f"Errore get unique values: {e}")
            return []

    def export_view_to_excel(self, data: pd.DataFrame, file_path: str,
                             view_name: str = "Data") -> bool:
        """Esporta vista in Excel con formattazione"""
        try:
            if not HAS_PANDAS:
                return False

            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=view_name, index=False)

                # Formattazione base
                # workbook = writer.book  # Unused variable removed
                worksheet = writer.sheets[view_name]

                # Auto-width colonne
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = (
                        adjusted_width
                    )

            return True

        except Exception as e:
            print(f"Errore export Excel: {e}")
            return False


class GraphicalDataSelector:
    """Interfaccia grafica per selezione dati"""

    def __init__(self, parent, db_manager: AdvancedDatabaseManager,
                 on_selection_change=None):
        self.parent = parent
        self.db_manager = db_manager
        self.on_selection_change = on_selection_change
        self.current_table = None
        self.selected_columns = []
        self.active_filters = []
        self.setup_gui()

    def setup_gui(self):
        """Configura interfaccia selezione grafica"""
        # Frame principale
        if HAS_CUSTOMTKINTER:
            self.main_frame = ctk.CTkFrame(self.parent)
        else:
            self.main_frame = tk.Frame(self.parent, bg="#2b2b2b")

        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Titolo
        if HAS_CUSTOMTKINTER:
            title = ctk.CTkLabel(
                self.main_frame,
                text="🎨 Selezione Grafica Dati",
                font=ctk.CTkFont(size=18, weight="bold")
            )
        else:
            title = tk.Label(
                self.main_frame,
                text="🎨 Selezione Grafica Dati",
                font=("Arial", 14, "bold"),
                bg="#2b2b2b", fg="white"
            )
        title.pack(pady=10)

        # Selezione tabella
        self.create_table_selector()

        # Selezione colonne
        self.create_column_selector()

        # Filtri
        self.create_filter_section()

        # Preview risultati
        self.create_preview_section()

        # Azioni
        self.create_action_buttons()

    def create_table_selector(self):
        """Crea sezione selezione tabella"""
        if HAS_CUSTOMTKINTER:
            table_frame = ctk.CTkFrame(self.main_frame)
        else:
            table_frame = tk.Frame(self.main_frame, bg="#3c3c3c")
        table_frame.pack(fill="x", padx=10, pady=5)

        if HAS_CUSTOMTKINTER:
            ctk.CTkLabel(
                table_frame,
                text="📋 Seleziona Tabella:",
                font=ctk.CTkFont(
                    weight="bold")).pack(
                anchor="w",
                padx=10,
                pady=5)
        else:
            tk.Label(
                table_frame,
                text="📋 Seleziona Tabella:",
                font=(
                    "Arial",
                    10,
                    "bold"),
                bg="#3c3c3c",
                fg="white").pack(
                anchor="w",
                padx=10,
                pady=5)

        # Combo tabelle
        self.table_var = tk.StringVar()
        if HAS_CUSTOMTKINTER:
            self.table_combo = ctk.CTkComboBox(
                table_frame, variable=self.table_var,
                command=self.on_table_selected, width=300
            )
        else:
            self.table_combo = ttk.Combobox(
                table_frame, textvariable=self.table_var, width=40
            )
            self.table_combo.bind(
                "<<ComboboxSelected>>",
                self.on_table_selected)

        self.table_combo.pack(padx=10, pady=5)

        # Info tabella
        if HAS_CUSTOMTKINTER:
            self.table_info = ctk.CTkTextbox(table_frame, height=60)
        else:
            self.table_info = tk.Text(
                table_frame, height=3, bg="#4a4a4a", fg="white")
        self.table_info.pack(fill="x", padx=10, pady=5)

        self.load_tables()

    def create_column_selector(self):
        """Crea sezione selezione colonne"""
        if HAS_CUSTOMTKINTER:
            col_frame = ctk.CTkFrame(self.main_frame)
        else:
            col_frame = tk.Frame(self.main_frame, bg="#3c3c3c")
        col_frame.pack(fill="x", padx=10, pady=5)

        if HAS_CUSTOMTKINTER:
            ctk.CTkLabel(
                col_frame,
                text="🔢 Seleziona Colonne:",
                font=ctk.CTkFont(
                    weight="bold")).pack(
                anchor="w",
                padx=10,
                pady=5)
        else:
            tk.Label(
                col_frame,
                text="🔢 Seleziona Colonne:",
                font=(
                    "Arial",
                    10,
                    "bold"),
                bg="#3c3c3c",
                fg="white").pack(
                anchor="w",
                padx=10,
                pady=5)

        # Frame per checkboxes colonne
        self.columns_frame = tk.Frame(col_frame, bg="#3c3c3c")
        self.columns_frame.pack(fill="x", padx=10, pady=5)

        # Pulsanti selezione rapida
        buttons_frame = tk.Frame(col_frame, bg="#3c3c3c")
        buttons_frame.pack(fill="x", padx=10, pady=5)

        if HAS_CUSTOMTKINTER:
            ctk.CTkButton(
                buttons_frame,
                text="Seleziona Tutto",
                command=self.select_all_columns,
                width=120).pack(
                side="left",
                padx=5)
            ctk.CTkButton(
                buttons_frame,
                text="Deseleziona Tutto",
                command=self.deselect_all_columns,
                width=120).pack(
                side="left",
                padx=5)
        else:
            tk.Button(
                buttons_frame,
                text="Seleziona Tutto",
                command=self.select_all_columns).pack(
                side="left",
                padx=5)
            tk.Button(
                buttons_frame,
                text="Deseleziona Tutto",
                command=self.deselect_all_columns).pack(
                side="left",
                padx=5)

    def create_filter_section(self):
        """Crea sezione filtri"""
        if HAS_CUSTOMTKINTER:
            filter_frame = ctk.CTkFrame(self.main_frame)
        else:
            filter_frame = tk.Frame(self.main_frame, bg="#3c3c3c")
        filter_frame.pack(fill="both", expand=True, padx=10, pady=5)

        if HAS_CUSTOMTKINTER:
            ctk.CTkLabel(
                filter_frame,
                text="🔍 Filtri:",
                font=ctk.CTkFont(
                    weight="bold")).pack(
                anchor="w",
                padx=10,
                pady=5)
        else:
            tk.Label(
                filter_frame,
                text="🔍 Filtri:",
                font=(
                    "Arial",
                    10,
                    "bold"),
                bg="#3c3c3c",
                fg="white").pack(
                anchor="w",
                padx=10,
                pady=5)

        # Scrollable frame per filtri
        if HAS_CUSTOMTKINTER:
            self.filters_scroll = ctk.CTkScrollableFrame(
                filter_frame, height=200)
        else:
            canvas = tk.Canvas(filter_frame, bg="#3c3c3c", height=200)
            scrollbar = tk.Scrollbar(
                filter_frame,
                orient="vertical",
                command=canvas.yview)
            self.filters_scroll = tk.Frame(canvas, bg="#3c3c3c")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True, padx=10)
            scrollbar.pack(side="right", fill="y")
            canvas.create_window(
                (0, 0), window=self.filters_scroll, anchor="nw")

        self.filters_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # Pulsante aggiungi filtro
        if HAS_CUSTOMTKINTER:
            ctk.CTkButton(filter_frame, text="➕ Aggiungi Filtro",
                          command=self.add_filter, width=150).pack(pady=5)
        else:
            tk.Button(filter_frame, text="➕ Aggiungi Filtro",
                      command=self.add_filter).pack(pady=5)

    def create_preview_section(self):
        """Crea sezione preview"""
        if HAS_CUSTOMTKINTER:
            preview_frame = ctk.CTkFrame(self.main_frame)
        else:
            preview_frame = tk.Frame(self.main_frame, bg="#3c3c3c")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        if HAS_CUSTOMTKINTER:
            ctk.CTkLabel(
                preview_frame,
                text="👁️ Preview:",
                font=ctk.CTkFont(
                    weight="bold")).pack(
                anchor="w",
                padx=10,
                pady=5)
        else:
            tk.Label(
                preview_frame,
                text="👁️ Preview:",
                font=(
                    "Arial",
                    10,
                    "bold"),
                bg="#3c3c3c",
                fg="white").pack(
                anchor="w",
                padx=10,
                pady=5)

        # Treeview per preview
        tree_frame = tk.Frame(preview_frame, bg="#3c3c3c")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.preview_tree = ttk.Treeview(tree_frame)
        self.preview_tree.pack(side="left", fill="both", expand=True)

        preview_scroll = ttk.Scrollbar(tree_frame, orient="vertical",
                                       command=self.preview_tree.yview)
        preview_scroll.pack(side="right", fill="y")
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)

    def create_action_buttons(self):
        """Crea pulsanti azione"""
        if HAS_CUSTOMTKINTER:
            actions_frame = ctk.CTkFrame(self.main_frame)
        else:
            actions_frame = tk.Frame(self.main_frame, bg="#3c3c3c")
        actions_frame.pack(fill="x", padx=10, pady=10)

        if HAS_CUSTOMTKINTER:
            ctk.CTkButton(
                actions_frame,
                text="🔄 Aggiorna Preview",
                command=self.update_preview,
                width=150).pack(
                side="left",
                padx=5)
            ctk.CTkButton(
                actions_frame,
                text="💾 Salva Vista",
                command=self.save_current_view,
                width=150).pack(
                side="left",
                padx=5)
            ctk.CTkButton(
                actions_frame,
                text="📊 Applica Selezione",
                command=self.apply_selection,
                width=150).pack(
                side="left",
                padx=5)
        else:
            tk.Button(actions_frame, text="🔄 Aggiorna Preview",
                      command=self.update_preview).pack(side="left", padx=5)
            tk.Button(actions_frame, text="💾 Salva Vista",
                      command=self.save_current_view).pack(side="left", padx=5)
            tk.Button(actions_frame, text="📊 Applica Selezione",
                      command=self.apply_selection).pack(side="left", padx=5)

    def load_tables(self):
        """Carica lista tabelle"""
        tables = self.db_manager.get_all_tables_with_details()
        table_names = [t['name'] for t in tables]

        if HAS_CUSTOMTKINTER:
            self.table_combo.configure(values=table_names)
        else:
            self.table_combo['values'] = table_names

        self.tables_data = {t['name']: t for t in tables}

    def on_table_selected(self, event_or_value=None):
        """Gestisce selezione tabella"""
        table_name = self.table_var.get()
        if not table_name or table_name not in self.tables_data:
            return

        self.current_table = table_name
        table_data = self.tables_data[table_name]

        # Aggiorna info tabella
        info_text = (f"Righe: {table_data['row_count']:,}\n"
                     f"Colonne: {len(table_data['columns'])}")

        if HAS_CUSTOMTKINTER:
            self.table_info.delete("1.0", tk.END)
            self.table_info.insert("1.0", info_text)
        else:
            self.table_info.delete("1.0", tk.END)
            self.table_info.insert("1.0", info_text)

        # Aggiorna selezione colonne
        self.update_column_checkboxes(table_data['columns'])

        # Reset filtri
        self.active_filters = []
        self.update_filters_display()

    def update_column_checkboxes(self, columns):
        """Aggiorna checkboxes colonne"""
        # Pulisci frame esistente
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        self.column_vars = {}

        # Crea checkbox per ogni colonna
        for i, col in enumerate(columns):
            var = tk.BooleanVar()
            self.column_vars[col['name']] = var

            frame = tk.Frame(self.columns_frame, bg="#3c3c3c")
            frame.grid(row=i // 3, column=i % 3, padx=5, pady=2, sticky="w")

            checkbox = tk.Checkbutton(
                frame,
                text=f"{col['name']} ({col['type']})",
                variable=var,
                command=self.on_column_selection_change,
                bg="#3c3c3c",
                fg="white",
                selectcolor="#4a4a4a"
            )
            checkbox.pack(anchor="w")

    def on_column_selection_change(self):
        """Gestisce cambio selezione colonne"""
        self.selected_columns = [
            col for col, var in self.column_vars.items() if var.get()
        ]

    def select_all_columns(self):
        """Seleziona tutte le colonne"""
        for var in self.column_vars.values():
            var.set(True)
        self.on_column_selection_change()

    def deselect_all_columns(self):
        """Deseleziona tutte le colonne"""
        for var in self.column_vars.values():
            var.set(False)
        self.on_column_selection_change()

    def add_filter(self):
        """Aggiunge nuovo filtro"""
        if not self.current_table:
            messagebox.showwarning("Attenzione", "Seleziona prima una tabella")
            return

        dialog = FilterDialog(self.parent, self.current_table,
                              self.tables_data[self.current_table]['columns'],
                              self.db_manager)
        filter_config = dialog.get_filter()

        if filter_config:
            self.active_filters.append(filter_config)
            self.update_filters_display()

    def update_filters_display(self):
        """Aggiorna visualizzazione filtri"""
        # Pulisci filtri esistenti
        for widget in self.filters_scroll.winfo_children():
            widget.destroy()

        # Mostra filtri attivi
        for i, filter_config in enumerate(self.active_filters):
            if HAS_CUSTOMTKINTER:
                filter_frame = ctk.CTkFrame(self.filters_scroll)
            else:
                filter_frame = tk.Frame(self.filters_scroll, bg="#4a4a4a")
            filter_frame.pack(fill="x", pady=2)

            # Testo filtro
            filter_text = (
                f"{filter_config['column']} "
                f"{filter_config['operator']} "
                f"{filter_config['value']}"
            )

            if HAS_CUSTOMTKINTER:
                ctk.CTkLabel(
                    filter_frame,
                    text=filter_text).pack(
                    side="left",
                    padx=5)
                ctk.CTkButton(
                    filter_frame,
                    text="❌",
                    width=30,
                    command=lambda idx=i: self.remove_filter(idx)).pack(
                    side="right",
                    padx=5)
            else:
                tk.Label(filter_frame, text=filter_text,
                         bg="#4a4a4a", fg="white").pack(side="left", padx=5)
                tk.Button(
                    filter_frame,
                    text="❌",
                    width=3,
                    command=lambda idx=i: self.remove_filter(idx)).pack(
                    side="right",
                    padx=5)

    def remove_filter(self, index):
        """Rimuove filtro"""
        if 0 <= index < len(self.active_filters):
            self.active_filters.pop(index)
            self.update_filters_display()

    def update_preview(self):
        """Aggiorna preview dati"""
        if not self.current_table:
            return

        try:
            # Costruisci query
            query = self.db_manager.build_query_from_config(
                self.current_table, self.selected_columns, self.active_filters
            )
            query += " LIMIT 10"  # Limita preview

            # Esegui query
            conn = sqlite3.connect(self.db_manager.db_path)
            if HAS_PANDAS:
                df = pd.read_sql_query(query, conn)

                # Aggiorna treeview
                self.preview_tree.delete(*self.preview_tree.get_children())

                if not df.empty:
                    # Configura colonne
                    columns = list(df.columns)
                    self.preview_tree["columns"] = columns
                    self.preview_tree["show"] = "headings"

                    for col in columns:
                        self.preview_tree.heading(col, text=col)
                        self.preview_tree.column(col, width=100)

                    # Inserisci dati
                    for _, row in df.iterrows():
                        values = [
                            str(val) if val is not None else "" for val in row
                        ]
                        self.preview_tree.insert("", "end", values=values)

            conn.close()

        except Exception as e:
            messagebox.showerror("Errore", f"Errore preview: {e}")

    def save_current_view(self):
        """Salva vista corrente"""
        if not self.current_table:
            messagebox.showwarning("Attenzione", "Seleziona una tabella")
            return

        dialog = SaveViewDialog(self.parent)
        view_config = dialog.get_config()

        if view_config:
            success = self.db_manager.save_view(
                view_config['name'], self.current_table,
                self.selected_columns, self.active_filters,
                view_config['description'], view_config['is_favorite']
            )

            if success:
                messagebox.showinfo("Successo", "Vista salvata!")
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio")

    def apply_selection(self):
        """Applica selezione corrente"""
        if self.on_selection_change:
            config = {
                'table': self.current_table,
                'columns': self.selected_columns,
                'filters': self.active_filters
            }
            self.on_selection_change(config)


class FilterDialog:
    """Dialog per creazione filtri"""

    def __init__(self, parent, table_name, columns, db_manager):
        self.parent = parent
        self.table_name = table_name
        self.columns = columns
        self.db_manager = db_manager
        self.result = None
        self.create_dialog()

    def create_dialog(self):
        """Crea dialog filtro"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Nuovo Filtro")
        self.dialog.geometry("400x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Selezione colonna
        tk.Label(self.dialog, text="Colonna:").pack(pady=5)
        self.column_var = tk.StringVar()
        column_combo = ttk.Combobox(
            self.dialog, textvariable=self.column_var, values=[
                col['name'] for col in self.columns])
        column_combo.pack(pady=5)
        column_combo.bind("<<ComboboxSelected>>", self.on_column_change)

        # Operatore
        tk.Label(self.dialog, text="Operatore:").pack(pady=5)
        self.operator_var = tk.StringVar(value="=")
        operator_combo = ttk.Combobox(
            self.dialog,
            textvariable=self.operator_var,
            values=[
                "=",
                "!=",
                ">",
                "<",
                ">=",
                "<=",
                "LIKE",
                "IN",
                "IS NULL",
                "IS NOT NULL"])
        operator_combo.pack(pady=5)

        # Valore
        tk.Label(self.dialog, text="Valore:").pack(pady=5)
        self.value_frame = tk.Frame(self.dialog)
        self.value_frame.pack(pady=5, fill="x", padx=20)

        self.value_entry = tk.Entry(self.value_frame)
        self.value_entry.pack(fill="x")

        # Lista valori disponibili
        self.values_listbox = tk.Listbox(self.dialog, height=6)
        self.values_listbox.pack(pady=5, fill="both", expand=True, padx=20)
        self.values_listbox.bind("<<ListboxSelect>>", self.on_value_select)

        # Pulsanti
        buttons_frame = tk.Frame(self.dialog)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="OK",
            command=self.confirm).pack(
            side="left",
            padx=5)
        tk.Button(
            buttons_frame,
            text="Annulla",
            command=self.cancel).pack(
            side="left",
            padx=5)

    def on_column_change(self, event=None):
        """Carica valori unici per colonna selezionata"""
        column = self.column_var.get()
        if column:
            values = self.db_manager.get_column_unique_values(
                self.table_name, column)

            self.values_listbox.delete(0, tk.END)
            for value in values:
                self.values_listbox.insert(tk.END, value)

    def on_value_select(self, event=None):
        """Inserisce valore selezionato"""
        selection = self.values_listbox.curselection()
        if selection:
            value = self.values_listbox.get(selection[0])
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, value)

    def confirm(self):
        """Conferma filtro"""
        column = self.column_var.get()
        operator = self.operator_var.get()
        value = self.value_entry.get()

        if column and operator:
            self.result = {
                'column': column,
                'operator': operator,
                'value': value
            }
            self.dialog.destroy()

    def cancel(self):
        """Annulla dialog"""
        self.dialog.destroy()

    def get_filter(self):
        """Restituisce configurazione filtro"""
        self.dialog.wait_window()
        return self.result


class SaveViewDialog:
    """Dialog per salvataggio vista"""

    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.create_dialog()

    def create_dialog(self):
        """Crea dialog salvataggio"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Salva Vista")
        self.dialog.geometry("400x250")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Nome vista
        tk.Label(
            self.dialog,
            text="Nome Vista:",
            font=(
                "Arial",
                10,
                "bold")).pack(
            pady=5)
        self.name_entry = tk.Entry(self.dialog, width=40)
        self.name_entry.pack(pady=5)

        # Descrizione
        tk.Label(
            self.dialog,
            text="Descrizione:",
            font=(
                "Arial",
                10,
                "bold")).pack(
            pady=5)
        self.desc_text = tk.Text(self.dialog, height=4, width=40)
        self.desc_text.pack(pady=5)

        # Checkbox preferiti
        self.favorite_var = tk.BooleanVar()
        tk.Checkbutton(self.dialog, text="Aggiungi ai preferiti",
                       variable=self.favorite_var).pack(pady=5)

        # Pulsanti
        buttons_frame = tk.Frame(self.dialog)
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Salva", command=self.save,
                  font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(
            buttons_frame,
            text="Annulla",
            command=self.cancel).pack(
            side="left",
            padx=5)

    def save(self):
        """Salva configurazione"""
        name = self.name_entry.get().strip()
        if name:
            self.result = {
                'name': name,
                'description': self.desc_text.get("1.0", tk.END).strip(),
                'is_favorite': self.favorite_var.get()
            }
            self.dialog.destroy()
        else:
            messagebox.showwarning(
                "Attenzione", "Inserisci un nome per la vista")

    def cancel(self):
        """Annulla dialog"""
        self.dialog.destroy()

    def get_config(self):
        """Restituisce configurazione"""
        self.dialog.wait_window()
        return self.result


if __name__ == "__main__":
    # Test del sistema
    print("🏢 Advanced Database Manager - Test")

    db = AdvancedDatabaseManager()
    print("✅ Database manager inizializzato")

    # Test GUI components
    if HAS_CUSTOMTKINTER:
        root = ctk.CTk()
        root.title("Test Graphical Data Selector")

        def on_selection_change(config):
            print(f"Selezione cambiata: {config}")

        selector = GraphicalDataSelector(root, db, on_selection_change)
        print("✅ Interfaccia grafica inizializzata")

        root.mainloop()
    else:
        print("⚠️ CustomTkinter non disponibile - test GUI limitato")
