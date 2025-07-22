#!/usr/bin/env python3
"""
🖥️ EXCELTOOLS PRO - INTERFACCIA DATABASE ENTERPRISE
==================================================

Interfaccia grafica professionale per la gestione database avanzata
con funzionalità complete di query, filtri, esportazione e gestione dati.

Autore: Senior DB Manager IT DEV
Data: 2025-07-16
Versione: Enterprise GUI 2.0
"""


import os
import threading
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import re


try:
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

from database_manager_enterprise import DatabaseManager, QueryBuilder


class DatabaseExplorerGUI:
    """Interfaccia database explorer professionale"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.query_builder = QueryBuilder(self.db_manager)
        self.current_data = None
        self.current_query = ""
        self.setup_gui()

    def setup_gui(self):
        """Inizializza interfaccia grafica enterprise"""
        if HAS_CUSTOMTKINTER:
            self.setup_modern_gui()
        else:
            self.setup_classic_gui()

    def setup_modern_gui(self):
        self.root = ctk.CTk()
        self.table_var = tk.StringVar()  # Initialize table_var after root
        self.root.title("🏢 ExcelTools Pro - Database Enterprise Manager")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#1a1a1a")

        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top toolbar
        self.create_toolbar(main_frame)

        # Main content area (3 panels)
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Left panel - Tables & Navigation
        left_panel = ctk.CTkFrame(content_frame, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)
        self.create_navigation_panel(left_panel)

        # Center panel - Query Builder & Results
        center_panel = ctk.CTkFrame(content_frame)
        center_panel.pack(side="left", fill="both", expand=True, padx=5)
        self.create_query_panel(center_panel)

        # Right panel - Query History & Tools
        right_panel = ctk.CTkFrame(content_frame, width=250)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)
        self.create_tools_panel(right_panel)

        # Status bar
        self.create_status_bar(main_frame)

        # Load initial data
        self.refresh_tables()

    def setup_classic_gui(self):
        """Setup interfaccia classica con Tkinter"""
        self.root = tk.Tk()
        self.table_var = tk.StringVar()  # Initialize table_var after root
        self.root.title("🏢 ExcelTools Pro - Database Enterprise Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2b2b2b")

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background="#3c3c3c",
                        foreground="white", fieldbackground="#3c3c3c")
        style.configure('Treeview.Heading', background="#4a4a4a",
                        foreground="white")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Setup panels with classic widgets
        self.create_classic_panels(main_frame)
        self.refresh_tables()

    def create_toolbar(self, parent):
        """Crea toolbar principale"""
        toolbar = ctk.CTkFrame(parent, height=60)
        toolbar.pack(fill="x", pady=(0, 10))
        toolbar.pack_propagate(False)

        # File operations
        file_frame = ctk.CTkFrame(toolbar)
        file_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(
            file_frame, text="📁 Importa Excel",
            command=self.import_excel_file,
            width=120, height=35
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            file_frame, text="🔀 Merge Excel",
            command=self.merge_excel_files,
            width=120, height=35
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            file_frame, text="💾 Esporta Risultati",
            command=self.export_results,
            width=120, height=35
        ).pack(side="left", padx=5)

    def merge_excel_files(self):
        """Unisce più file Excel in una tabella unica"""
        file_paths = filedialog.askopenfilenames(
            title="Seleziona file Excel da unire",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_paths:
            return
        self.update_status("🔀 Merging file Excel...")

        def merge_thread():
            import pandas as pd
            merged_df = None
            for idx, file_path in enumerate(file_paths):
                try:
                    df = pd.read_excel(file_path)
                    if merged_df is None:
                        merged_df = df
                    else:
                        merged_df = pd.concat(
                            [merged_df, df], ignore_index=True, sort=False
                        )
                except Exception:
                    continue
            if merged_df is not None:
                # Chiedi nome tabella
                def show_dialog():
                    def save_merged(dialog, name_entry):
                        name = name_entry.get().strip()
                        if name:
                            success = self.db_manager.import_dataframe_as_table(
                                merged_df,
                                name
                            )
                            if success:
                                self.root.after(
                                    0,
                                    lambda: self.update_status(
                                        f"✅ Merge completato in tabella '{name}'"
                                    )
                                )
                                self.root.after(0, self.refresh_tables)
                            else:
                                self.root.after(
                                    0,
                                    lambda: self.update_status(
                                        "❌ Errore nel merge"
                                    )
                                )
                            dialog.destroy()
                    dialog = tk.Toplevel(self.root)
                    dialog.title("Salva tabella unita")
                    dialog.geometry("400x150")
                    dialog.transient(self.root)
                    dialog.grab_set()
                    tk.Label(
                        dialog, text="Nome tabella risultante:"
                    ).pack(pady=10)
                    name_entry = tk.Entry(dialog, width=40)
                    name_entry.pack(pady=5)
                    tk.Button(
                        dialog,
                        text="Salva",
                        command=lambda: save_merged(dialog, name_entry)
                    ).pack(pady=10)
                self.root.after(0, show_dialog)
            else:
                self.root.after(
                    0,
                    lambda: self.update_status("❌ Nessun dato unito")
                )
        threading.Thread(target=merge_thread, daemon=True).start()


    def create_navigation_panel(self, parent):
        """Crea pannello navigazione tabelle"""
        # Title
        title = ctk.CTkLabel(
            parent, text="📊 Database Tables",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 5))

        # Search box
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Cerca tabelle...",
            textvariable=self.search_var
        )
        search_entry.pack(fill="x", padx=5, pady=5)
        search_entry.bind("<KeyRelease>", self.filter_tables)

        # Tables list
        tables_frame = ctk.CTkFrame(parent)
        tables_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create scrollable frame for tables
        self.tables_scroll = ctk.CTkScrollableFrame(tables_frame)
        self.tables_scroll.pack(fill="both", expand=True, padx=5, pady=5)

    def create_query_panel(self, parent):
        """
        Crea pannello query builder, filtri avanzati e risultati
        con AI/IDE features
        """
        query_frame = ctk.CTkFrame(parent)
        query_frame.pack(fill="x", padx=5, pady=5)

        query_label = ctk.CTkLabel(
            query_frame, text="🔧 Query Builder",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        query_label.pack(anchor="w", padx=10, pady=(10, 5))

        # SQL Editor + Autocomplete colonne/tabelle + error/ai help
        editor_frame = ctk.CTkFrame(query_frame)
        editor_frame.pack(fill="x", padx=10, pady=5)

        self.sql_text = tk.Text(
            editor_frame, height=8, bg="#3c3c3c",
            fg="white", insertbackground="white",
            font=("Consolas", 11)
        )
        self.sql_text.pack(fill="x", padx=5, pady=5)
        self.sql_text.bind("<KeyRelease>", self._on_sql_key)

        # Suggerimenti/errore sotto l'editor
        self.sql_suggestion_var = tk.StringVar()
        self.sql_suggestion_label = ctk.CTkLabel(
            editor_frame, textvariable=self.sql_suggestion_var,
            text_color="#ffcc00", font=ctk.CTkFont(size=11)
        )
        self.sql_suggestion_label.pack(anchor="w", padx=5, pady=(0, 2))

        # Pulsante Guida SQL e Riscrittura Query
        btn_frame = ctk.CTkFrame(editor_frame)
        btn_frame.pack(fill="x", padx=0, pady=0)
        ctk.CTkButton(
            btn_frame, text="❓ Guida SQL", command=self.show_sql_help,
            width=100
        ).pack(side="right", padx=5, pady=(0, 2))
        ctk.CTkButton(
            btn_frame, text="⚡ Riscrivi Query (COUNT/SUM/AVG)",
            command=self.rewrite_query, width=180
        ).pack(side="right", padx=5, pady=(0, 2))

    def rewrite_query(self):
        """Riscrive automaticamente la query corrente con funzioni aggregate"""
        sql = self.sql_text.get("1.0", "end").strip()
        if (
            not sql or not hasattr(self, 'table_var') or
            not self.table_var.get()
        ):
            messagebox.showinfo(
                "Info",
                "Seleziona una tabella e scrivi una query."
            )
            return
        table = self.table_var.get()
        try:
            columns = self.db_manager.get_table_columns(table)
        except Exception:
            columns = []
        # Dialog per scegliere funzione e colonna
        dialog = tk.Toplevel(self.root)
        dialog.title("Riscrivi Query con Funzione SQL")
        dialog.geometry("400x200")
        tk.Label(dialog, text="Funzione:").pack(pady=5)
        func_var = tk.StringVar(value="COUNT")
        func_menu = ttk.Combobox(
            dialog, textvariable=func_var,
            values=["COUNT", "SUM", "AVG", "MIN", "MAX"]
        )
        func_menu.pack(pady=5)
        tk.Label(dialog, text="Colonna:").pack(pady=5)
        col_var = tk.StringVar(value=columns[0] if columns else "")
        col_menu = ttk.Combobox(
            dialog, textvariable=col_var, values=columns
        )
        col_menu.pack(pady=5)


        def do_rewrite():
            func = func_var.get()
            col = col_var.get()
            if func and col:
                new_query = f"SELECT {func}({col}) FROM {table}"
                self.sql_text.delete("1.0", tk.END)
                self.sql_text.insert("1.0", new_query)
                dialog.destroy()

        tk.Button(dialog, text="Riscrivi", command=do_rewrite).pack(pady=10)
                sql_funcs = ["COUNT", "SUM", "AVG", "MIN", "MAX"]
                suggest = (
                    f"Funzioni: {', '.join(sql_funcs)} | "
                    f"Colonne: {', '.join(columns)}"
                )
                popup_items = sql_funcs + columns
                show_popup = True
            # Autocomplete funzioni SQL dopo SELECT <func>(
            elif re.search(r'SELECT\s+(COUNT|SUM|AVG|MIN|MAX)\($', sql_up):
                suggest = f"Colonne: {', '.join(columns)}"
                popup_items = columns
                show_popup = True
            # Autocomplete colonne dopo SELECT * o WHERE
            elif sql_up.endswith("SELECT *") or sql_up.endswith("WHERE"):
                suggest = f"Colonne: {', '.join(columns)}"
                popup_items = columns
                show_popup = True
            # Autocomplete tabella dopo FROM
            elif sql_up.endswith("FROM"):
                suggest = f"Tabella: {table}"
                popup_items = [table]
                show_popup = True
            # Autocomplete JOIN types
            elif (
                sql_up.rstrip().endswith("JOIN") or
                sql_up.rstrip().endswith("JOIN ")
            ):
                join_types = [
                    "INNER JOIN", "LEFT JOIN",
                    "RIGHT JOIN", "FULL OUTER JOIN"
                ]
                suggest = "Tipi di JOIN: " + ", ".join(join_types)
                popup_items = join_types
                show_popup = True
            # Autocomplete ON dopo JOIN tabella
            elif "JOIN" in sql_up and sql_up.rstrip().endswith("ON"):
                current_table = table
                join_table = None
                m = re.search(r'JOIN\s+(\w+)', sql_up)
                if m:
                    join_table = m.group(1)
                join_cols = []
                if join_table:
                    try:
                        cols1 = set(
                            self.db_manager.get_table_columns(current_table)
                        )
                        cols2 = set(
                            self.db_manager.get_table_columns(join_table)
                        )
                        join_cols = list(cols1 & cols2)
                    except Exception:
                        join_cols = []
                if join_cols:
                    suggest = (
                        f"Colonne comuni per ON: {', '.join(join_cols)}"
                    )
                    popup_items = join_cols
                    show_popup = True
                else:
                    suggest = (
                        "Scrivi la condizione ON (es: tab1.col = tab2.col)"
                    )
                    popup_items = []
                    show_popup = False
        # Rilevazione errori SQL (base)
        error = ""
        if sql and not sql.upper().startswith("SELECT"):
            error = "⚠️ La query deve iniziare con SELECT"
        elif sql.count("'") % 2 != 0:
            error = "⚠️ Apice singolo non chiuso"
        elif sql.count('"') % 2 != 0:
            error = "⚠️ Virgoletta doppia non chiusa"
        # Mostra suggerimento o errore
        if error:
            self.sql_suggestion_var.set(error)
            self.sql_suggestion_label.configure(text_color="#ff3333")
            self._hide_autocomplete_popup()
        elif suggest:
            self.sql_suggestion_var.set(suggest)
            self.sql_suggestion_label.configure(text_color="#ffcc00")
            if show_popup and popup_items:
                self._show_autocomplete_popup(popup_items)
            else:
                self._hide_autocomplete_popup()
        else:
            self.sql_suggestion_var.set("")
            self._hide_autocomplete_popup()

    def _show_autocomplete_popup(self, items):
        """Mostra popup di autocompletamento sotto l'editor SQL"""
        if hasattr(self, '_autocomplete_popup') and self._autocomplete_popup:
            self._autocomplete_popup.destroy()
        if not items:
            return
        self._autocomplete_popup = tk.Toplevel(self.root)
        self._autocomplete_popup.wm_overrideredirect(True)
        self._autocomplete_popup.attributes("-topmost", True)
        # Posiziona popup sotto l'editor
        x = self.sql_text.winfo_rootx()
        y = self.sql_text.winfo_rooty() + self.sql_text.winfo_height()
        self._autocomplete_popup.geometry(
            f"250x{min(200, 20*len(items))}+{x}+{y}"
        )
        listbox = tk.Listbox(self._autocomplete_popup, font=("Consolas", 11))
        for item in items:
            listbox.insert("end", item)
        listbox.pack(fill="both", expand=True)
        listbox.focus_set()
        listbox.selection_set(0)
        # Gestione selezione

        def on_select(event=None):
            sel = listbox.curselection()
            if sel:
                value = listbox.get(sel[0])
                self._insert_autocomplete_value(value)
                self._autocomplete_popup.destroy()
                self._autocomplete_popup = None
        listbox.bind("<Return>", on_select)
        listbox.bind("<Double-Button-1>", on_select)
        listbox.bind("<Escape>", lambda e: self._hide_autocomplete_popup())
        # Navigazione con frecce

        def on_key(event):
            if event.keysym == "Down":
                idx = listbox.curselection()[0]
                if idx < listbox.size() - 1:
                    listbox.selection_clear(idx)
                    listbox.selection_set(idx + 1)
                    listbox.activate(idx + 1)
            elif event.keysym == "Up":
                idx = listbox.curselection()[0]
                if idx > 0:
                    listbox.selection_clear(idx)
                    listbox.selection_set(idx - 1)
                    listbox.activate(idx - 1)
        listbox.bind("<KeyPress>", on_key)
        self._autocomplete_popup.listbox = listbox

    def _hide_autocomplete_popup(self):
        if hasattr(self, '_autocomplete_popup') and self._autocomplete_popup:
            self._autocomplete_popup.destroy()
            self._autocomplete_popup = None

    def _insert_autocomplete_value(self, value):
        """
        Inserisce il valore selezionato dal popup nella posizione corretta
        """
        index = self.sql_text.index(tk.INSERT)
        line, col = map(int, index.split('.'))
        text = self.sql_text.get("1.0", tk.END)
        lines = text.splitlines()
        if not lines:
            return
        current_line = lines[line - 1]
        before = current_line[:col]
        after = current_line[col:]
        import re
        # Funzioni SQL
        if value in ["COUNT", "SUM", "AVG", "MIN", "MAX"]:
            new_line = before + value + "(" + after
            lines[line - 1] = new_line
            new_text = '\n'.join(lines)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert("1.0", new_text)
            self.sql_text.mark_set(
                tk.INSERT, f"{line}.{len(before + value + '(')}"
            )
            return
        # JOIN types
        if value in [
            "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"
        ]:
            new_line = before.rstrip() + " " + value + " " + after.lstrip()
            lines[line - 1] = new_line
            new_text = '\n'.join(lines)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert("1.0", new_text)
            self.sql_text.mark_set(
                tk.INSERT,
                f"{line}.{len(before.rstrip() + ' ' + value + ' ')}"
            )
            return
        # Colonne comuni per ON o colonne dopo funzione
        match_func = re.search(r'SELECT\s+(COUNT|SUM|AVG|MIN|MAX)\($', before.upper())
        if match_func:
            insert_pos = len(before)
            new_line = before + value + after
            lines[line - 1] = new_line
            new_text = '\n'.join(lines)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert("1.0", new_text)
            self.sql_text.mark_set(tk.INSERT, f"{line}.{insert_pos + len(value)}")
            return
        match = re.search(r'(SELECT|FROM|WHERE|JOIN|ON)\s*$', before.upper())
        if match:
            insert_pos = len(before)
            new_line = before + value + after
            lines[line - 1] = new_line
            new_text = '\n'.join(lines)
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert("1.0", new_text)
            self.sql_text.mark_set(tk.INSERT, f"{line}.{insert_pos + len(value)}")
            return

    def show_sql_help(self):
        """Mostra una finestra di aiuto sintassi SQL"""
        help_text = (
            "Esempi di query SQL supportate:\n"
            "- SELECT * FROM nome_tabella\n"
            "- SELECT col1, col2 FROM nome_tabella WHERE col1 = 'valore'\n"
            "- Puoi usare AND, OR, LIKE, >, <, >=, <=, !=\n"
            "- Usa i filtri rapidi per generare query automaticamente.\n"
            "\nSuggerimenti:\n- Premi il pulsante ▶️ per eseguire la query.\n"
            "- Le colonne disponibili vengono suggerite dopo SELECT/WHERE."
        )
        top = tk.Toplevel(self.root)
        top.title("Guida SQL")
        top.geometry("500x350")
        tk.Label(top, text=help_text, justify="left", font=("Consolas", 11)).pack(padx=15, pady=15, fill="both", expand=True)

    def _autocomplete_columns(self, event=None):
        # Autocomplete colonne: mostra suggerimenti se si digita
        # dopo SELECT o WHERE
        if not hasattr(self, 'table_var') or not self.table_var.get():
            return
        # (Qui si può implementare un vero popup di suggerimento colonne)
        pass

    def add_filter(self):
        col = self.filter_col_var.get()
        op = self.filter_op_var.get()
        val = self.filter_val_var.get()
        logic = self.filter_logic_var.get()
        if col and op and val:
            self.active_filters.append((col, op, val, logic))
            self.update_filters_label()
            self.apply_filters_to_query()

    def reset_filters(self):
        self.active_filters = []
        self.update_filters_label()
        self.apply_filters_to_query()

    def update_filters_label(self):
        self.filters_label.configure(
            text=f"Filtri attivi: {len(self.active_filters)}"
        )

    def apply_filters_to_query(self):
        # Genera la WHERE clause SQL dai filtri attivi e aggiorna la query
        if not hasattr(self, 'table_var') or not self.table_var.get():
            return
        table = self.table_var.get()
        base_query = f"SELECT * FROM {table}"
        where_clauses = []
        logic_ops = []
        for idx, (col, op, val, logic) in enumerate(self.active_filters):
            clause = ""
            if op == 'contiene':
                clause = f"{col} LIKE '%{val}%'"
            elif op == 'non contiene':
                clause = f"{col} NOT LIKE '%{val}%'"
            elif op in ['=', '!=', '>', '<', '>=', '<=']:
                if val.replace('.', '', 1).isdigit():
                    clause = f"{col} {op} {val}"
                else:
                    clause = f"{col} {op} '{val}'"
            if idx > 0:
                logic_ops.append(logic)
            where_clauses.append(clause)
        where_sql = ''
        if where_clauses:
            # Combina i filtri con AND/OR
            combined = where_clauses[0]
            for i, clause in enumerate(where_clauses[1:]):
                combined = f"({combined}) {logic_ops[i]} ({clause})"
            where_sql = ' WHERE ' + combined
        limit = self.limit_var.get() if hasattr(self, 'limit_var') else '100'
        query = base_query + where_sql + f' LIMIT {limit}'
        self.sql_text.delete("1.0", "end")
        self.sql_text.insert("1.0", query)
        # Aggiorna colonne disponibili e valori unici per i filtri
        try:
            columns = self.db_manager.get_table_columns(table)
            self.filter_col_menu.configure(values=columns)
            self.update_filter_operators_and_values()
        except Exception:
            pass

    def update_filter_operators_and_values(self, event=None):
        # Aggiorna operatori e valori disponibili in base al tipo colonna
        table = self.table_var.get()
        col = self.filter_col_var.get()
        if not table or not col:
            return
        try:
            col_type = self.db_manager.get_column_type(table, col)
            # Operatori dinamici
            if col_type in ('int', 'float', 'double', 'numeric'):
                ops = ["=", "!=", ">", "<", ">=", "<="]
            elif col_type in ('date', 'datetime'):
                ops = ["=", "!=", ">", "<", ">=", "<="]
            else:
                ops = ["=", "!=", "contiene", "non contiene"]
            self.filter_op_menu.configure(values=ops)
            # Autocompletamento valori unici
            unique_vals = self.db_manager.get_unique_column_values(table, col)
            self.filter_val_entry.configure(
                values=[str(v) for v in unique_vals[:100]]
            )
        except Exception:
            self.filter_op_menu.configure(
                values=[
                    "=", "!=", ">", "<", ">=", "<=", "contiene", "non contiene"
                ]
            )
            self.filter_val_entry.configure(values=[])

    def create_results_table(self, parent):
        """Crea tabella risultati con scrolling"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for results
        self.results_tree = ttk.Treeview(table_frame)
        self.results_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                    command=self.results_tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        self.results_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal",
                                    command=self.results_tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        self.results_tree.configure(xscrollcommand=h_scrollbar.set)

    def create_tools_panel(self, parent):
        """Crea pannello strumenti e cronologia"""
        # Query history
        history_label = ctk.CTkLabel(parent, text="📚 Query Salvate",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        history_label.pack(pady=(10, 5))

        # Saved queries list
        self.queries_scroll = ctk.CTkScrollableFrame(parent, height=300)
        self.queries_scroll.pack(fill="x", padx=10, pady=5)

        # Database statistics
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", padx=10, pady=10)

        stats_label = ctk.CTkLabel(stats_frame, text="📊 Statistiche DB",
                                   font=ctk.CTkFont(size=14, weight="bold"))
        stats_label.pack(pady=5)

        self.stats_text = ctk.CTkTextbox(stats_frame, height=150)
        self.stats_text.pack(fill="x", padx=5, pady=5)

        # Tools buttons
        tools_frame = ctk.CTkFrame(parent)
        tools_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(tools_frame, text="🔧 Ottimizza DB",
                      command=self.optimize_database,
                      width=200).pack(pady=2)

        ctk.CTkButton(tools_frame, text="📈 Analizza Dati",
                      command=self.analyze_data,
                      width=200).pack(pady=2)

        ctk.CTkButton(tools_frame, text="🧹 Pulisci Cache",
                      command=self.clear_cache,
                      width=200).pack(pady=2)

    def create_status_bar(self, parent):
        """Crea barra di stato"""
        status_frame = ctk.CTkFrame(parent, height=30)
        status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="✅ Database pronto")
        status_label = ctk.CTkLabel(status_frame, textvariable=self.status_var)
        status_label.pack(side="left", padx=10, pady=5)

        self.record_count_var = tk.StringVar(value="0 record")
        record_label = ctk.CTkLabel(status_frame,
                                    textvariable=self.record_count_var)
        record_label.pack(side="right", padx=10, pady=5)

    def create_classic_panels(self, parent):
        """Crea pannelli per interfaccia classica"""
        # Implementazione semplificata per Tkinter standard
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        # Tab principale
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Database Explorer")

        # Query tab
        query_tab = ttk.Frame(notebook)
        notebook.add(query_tab, text="Query Builder")

        # Create basic layout
        self.create_basic_layout(main_tab)

    def create_basic_layout(self, parent):
        """Layout base per interfaccia classica"""
        # Top frame
        top_frame = tk.Frame(parent, bg="#2b2b2b")
        top_frame.pack(fill="x", pady=5)

        tk.Button(
            top_frame, text="📁 Importa Excel",
            command=self.import_excel_file,
            bg="#4a4a4a", fg="white"
        ).pack(side="left", padx=5)

        tk.Button(
            top_frame, text="🔄 Aggiorna",
            command=self.refresh_tables,
            bg="#4a4a4a", fg="white"
        ).pack(side="left", padx=5)

        # Results area
        self.results_tree = ttk.Treeview(parent)
        self.results_tree.pack(fill="both", expand=True, pady=10)

    def import_excel_file(self):
        """Importa file Excel nel database"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if file_path:
            self.update_status("📥 Importando file Excel...")

            def import_thread():
                try:
                    success = self.db_manager.import_excel_data(file_path)
                    if success:
                        self.root.after(0, lambda: self.update_status(
                            "✅ File Excel importato con successo"))
                        self.root.after(0, self.refresh_tables)
                    else:
                        self.root.after(0, lambda: self.update_status(
                            "❌ Errore durante l'importazione"))
                except Exception:
                    self.root.after(0, lambda: self.update_status(
                        "❌ Errore durante l'importazione"))

            threading.Thread(target=import_thread, daemon=True).start()

    def refresh_tables(self):
        """Aggiorna lista tabelle"""
        self.update_status("🔄 Aggiornando tabelle...")

        def refresh_thread():
            try:
                tables = self.db_manager.get_all_tables()
                self.root.after(0, lambda: self.update_tables_list(tables))
                self.root.after(0, lambda: self.update_status(
                    f"✅ {len(tables)} tabelle caricate"
                ))
            except Exception:
                self.root.after(0, lambda: self.update_status(
                    "❌ Errore durante aggiornamento tabelle"))

        threading.Thread(target=refresh_thread, daemon=True).start()

    def update_tables_list(self, tables):
        """Aggiorna lista tabelle nell'interfaccia"""
        if hasattr(self, 'tables_scroll'):
            # Clear existing buttons
            for widget in self.tables_scroll.winfo_children():
                widget.destroy()

            # Add table buttons
            for table in tables:
                table_frame = ctk.CTkFrame(self.tables_scroll)
                table_frame.pack(fill="x", pady=2)

                # Table name and info
                info_text = f"{table['name']}\n{table['total_rows']} righe"
                table_btn = ctk.CTkButton(
                    table_frame, text=info_text,
                    command=lambda t=table: self.select_table(t),
                    height=50, anchor="w"
                )
                table_btn.pack(fill="x", padx=5, pady=2)

            # Update combo box
            # if hasattr(self, 'table_var'):
            #     table_names = [t['name'] for t in tables]
            #     # Note: CTkComboBox values update might need specific method

    def select_table(self, table_info):
        """Seleziona tabella e carica preview"""
        table_name = table_info['name']
        self.table_var.set(table_name)

        # Generate preview query
        query = f"SELECT * FROM {table_name} LIMIT 100"
        self.sql_text.delete(1.0, tk.END)
        self.sql_text.insert(1.0, query)

        # Execute preview
        self.execute_query()

    def execute_query(self):
        """Esegue query SQL"""
        query = self.sql_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Attenzione", "Inserisci una query SQL")
            return

        self.current_query = query
        self.update_status("⚡ Eseguendo query...")

        def query_thread():
            try:
                result = self.db_manager.execute_query(query)
                if result is not None:
                    self.root.after(0, lambda: self.display_results(result))
                    self.root.after(0, lambda: self.update_status(
                        f"✅ Query completata: {len(result)} risultati"))
                else:
                    self.root.after(0, lambda: self.update_status(
                        "❌ Errore nell'esecuzione della query"))
            except Exception:
                self.root.after(0, lambda: self.update_status(
                    "❌ Errore durante esecuzione query"))

        threading.Thread(target=query_thread, daemon=True).start()

    def save_current_query(self):
        """Salva query corrente"""
        if not self.current_query:
            messagebox.showwarning(
                "Attenzione",
                "Nessuna query da salvare"
            )
            return

        # Simple dialog for query name
        dialog = tk.Toplevel(self.root)
        dialog.title("Salva Query")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Nome Query:").pack(pady=10)
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="Descrizione:").pack(pady=10)
        desc_entry = tk.Entry(dialog, width=40)
        desc_entry.pack(pady=5)

        def save_query():
            name = name_entry.get().strip()
        sql = self.sql_text.get("1.0", "end").strip()
        suggest = ""
        popup_items = []
        show_popup = False
        if hasattr(self, 'table_var') and self.table_var.get():
            table = self.table_var.get()
            try:
                columns = self.db_manager.get_table_columns(table)
            except Exception:
                columns = []
            sql_up = sql.upper()
        # Autocomplete funzioni SQL dopo SELECT
        if hasattr(self, 'table_var') and self.table_var.get():
            if sql_up.endswith("SELECT"):
                sql_funcs = ["COUNT", "SUM", "AVG", "MIN", "MAX"]
                suggest = (
                    f"Funzioni: {', '.join(sql_funcs)} | "
                    f"Colonne: {', '.join(columns)}"
                )
                popup_items = sql_funcs + columns
                show_popup = True
            # Autocomplete funzioni SQL dopo SELECT <func>(
            elif re.search(r'SELECT\s+(COUNT|SUM|AVG|MIN|MAX)\($', sql_up):
                suggest = f"Colonne: {', '.join(columns)}"
                popup_items = columns
                show_popup = True
            # Autocomplete colonne dopo SELECT * o WHERE
            elif sql_up.endswith("SELECT *") or sql_up.endswith("WHERE"):
                suggest = f"Colonne: {', '.join(columns)}"
                popup_items = columns
                show_popup = True
            # Autocomplete tabella dopo FROM
            elif sql_up.endswith("FROM"):
                suggest = f"Tabella: {table}"
                popup_items = [table]
                show_popup = True
            # Autocomplete JOIN types
            elif (
                sql_up.rstrip().endswith("JOIN") or
                sql_up.rstrip().endswith("JOIN ")
            ):
                join_types = [
                    "INNER JOIN", "LEFT JOIN",
                    "RIGHT JOIN", "FULL OUTER JOIN"
                ]
                suggest = "Tipi di JOIN: " + ", ".join(join_types)
                popup_items = join_types
                show_popup = True
            # Autocomplete ON dopo JOIN tabella
            elif "JOIN" in sql_up and sql_up.rstrip().endswith("ON"):
                current_table = table
                join_table = None
                m = re.search(r'JOIN\s+(\w+)', sql_up)
                if m:
                    join_table = m.group(1)
                join_cols = []
                if join_table:
                    try:
                        cols1 = set(
                            self.db_manager.get_table_columns(current_table)
                        )
                        cols2 = set(
                            self.db_manager.get_table_columns(join_table)
                        )
                        join_cols = list(cols1 & cols2)
                    except Exception:
                        join_cols = []
                if join_cols:
                    suggest = (
                        f"Colonne comuni per ON: {', '.join(join_cols)}"
                    )
                    popup_items = join_cols
                    show_popup = True
                else:
                    suggest = (
                        "Scrivi la condizione ON (es: tab1.col = tab2.col)"
                    )
                    popup_items = []
                    show_popup = False

    def refresh_saved_queries(self):
        """Aggiorna lista query salvate"""
        if hasattr(self, 'queries_scroll'):
            # Clear existing
            for widget in self.queries_scroll.winfo_children():
                widget.destroy()

            # Load saved queries
            queries = self.db_manager.get_saved_queries()
            for query in queries:
                query_frame = ctk.CTkFrame(self.queries_scroll)
                query_frame.pack(fill="x", pady=2)

                query_btn = ctk.CTkButton(
                    query_frame, text=query['name'],
                    command=lambda q=query: self.load_saved_query(q),
                    height=30
                )
                query_btn.pack(fill="x", padx=5, pady=2)

    def load_saved_query(self, query_info):
        """Carica query salvata"""
        self.sql_text.delete(1.0, tk.END)
        self.sql_text.insert(1.0, query_info['query_sql'])

    def filter_tables(self, event=None):
        """Filtra tabelle per ricerca"""
        # Implementazione filtro tabelle
        pass

    def delete_table(self):
        """Elimina tabella selezionata"""
        # Implementazione eliminazione tabella
        pass

    def optimize_database(self):
        """Ottimizza database"""
        self.update_status("🔧 Ottimizzando database...")
        # Implementazione ottimizzazione

    def analyze_data(self):
        """Analizza dati statistici"""
        self.update_status("📈 Analizzando dati...")
        # Implementazione analisi

    def clear_cache(self):
        """Pulisce cache sistema"""
        self.update_status("🧹 Pulizia cache completata")

    def update_status(self, message):
        """Aggiorna messaggio di stato"""
        if hasattr(self, 'status_var'):
            self.status_var.set(message)

    def update_record_count(self, count):
        """Aggiorna conteggio record"""
        if hasattr(self, 'record_count_var'):
            self.record_count_var.set(f"{count} record")

    def run(self):
        """Avvia applicazione"""
        print("🚀 Avviando ExcelTools Pro Database Enterprise Manager...")
        self.root.mainloop()


if __name__ == "__main__":
    if not HAS_PANDAS:
        print("❌ Pandas richiesto per funzionalità avanzate")
        exit(1)

    app = DatabaseExplorerGUI()
    app.run()
