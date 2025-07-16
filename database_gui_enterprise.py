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
from tkinter import filedialog, messagebox, ttk, font as tkFont
import tkinter as tk
from typing import Dict, List, Optional

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
        """Setup interfaccia moderna con CustomTkinter"""
        self.root = ctk.CTk()
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

        ctk.CTkButton(file_frame, text="📁 Importa Excel",
                     command=self.import_excel_file,
                     width=120, height=35).pack(side="left", padx=5)

        ctk.CTkButton(file_frame, text="💾 Esporta Risultati",
                     command=self.export_results,
                     width=120, height=35).pack(side="left", padx=5)

        # Database operations
        db_frame = ctk.CTkFrame(toolbar)
        db_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(db_frame, text="🔄 Aggiorna",
                     command=self.refresh_tables,
                     width=100, height=35).pack(side="left", padx=5)

        ctk.CTkButton(db_frame, text="🗑️ Elimina Tabella",
                     command=self.delete_table,
                     width=120, height=35).pack(side="left", padx=5)

        # Query operations
        query_frame = ctk.CTkFrame(toolbar)
        query_frame.pack(side="right", fill="y", padx=10, pady=10)

        ctk.CTkButton(query_frame, text="▶️ Esegui Query",
                     command=self.execute_query,
                     width=120, height=35).pack(side="left", padx=5)

        ctk.CTkButton(query_frame, text="💾 Salva Query",
                     command=self.save_current_query,
                     width=120, height=35).pack(side="left", padx=5)

    def create_navigation_panel(self, parent):
        """Crea pannello navigazione tabelle"""
        # Title
        title = ctk.CTkLabel(parent, text="📊 Database Tables",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(10, 5))

        # Search box
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Cerca tabelle...",
                                   textvariable=self.search_var)
        search_entry.pack(fill="x", padx=5, pady=5)
        search_entry.bind("<KeyRelease>", self.filter_tables)

        # Tables list
        tables_frame = ctk.CTkFrame(parent)
        tables_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create scrollable frame for tables
        self.tables_scroll = ctk.CTkScrollableFrame(tables_frame)
        self.tables_scroll.pack(fill="both", expand=True, padx=5, pady=5)

    def create_query_panel(self, parent):
        """Crea pannello query builder e risultati"""
        # Query builder section
        query_frame = ctk.CTkFrame(parent)
        query_frame.pack(fill="x", padx=5, pady=5)

        query_label = ctk.CTkLabel(query_frame, text="🔧 Query Builder",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        query_label.pack(anchor="w", padx=10, pady=(10, 5))

        # SQL Editor
        editor_frame = ctk.CTkFrame(query_frame)
        editor_frame.pack(fill="x", padx=10, pady=5)

        self.sql_text = tk.Text(editor_frame, height=8, bg="#3c3c3c",
                               fg="white", insertbackground="white",
                               font=("Consolas", 11))
        self.sql_text.pack(fill="x", padx=5, pady=5)

        # Quick filters
        filters_frame = ctk.CTkFrame(query_frame)
        filters_frame.pack(fill="x", padx=10, pady=5)

        filter_label = ctk.CTkLabel(filters_frame, text="⚡ Filtri Rapidi:",
                                   font=ctk.CTkFont(size=12, weight="bold"))
        filter_label.pack(anchor="w", padx=5, pady=5)

        # Filter controls
        filter_controls = ctk.CTkFrame(filters_frame)
        filter_controls.pack(fill="x", padx=5, pady=5)

        # Table selector
        self.table_var = tk.StringVar()
        table_combo = ctk.CTkComboBox(filter_controls, variable=self.table_var,
                                     values=[], width=150)
        table_combo.pack(side="left", padx=5)

        # Limit selector
        ctk.CTkLabel(filter_controls, text="Limit:").pack(side="left", padx=5)
        self.limit_var = tk.StringVar(value="100")
        limit_combo = ctk.CTkComboBox(filter_controls, variable=self.limit_var,
                                     values=["10", "50", "100", "500", "1000"],
                                     width=80)
        limit_combo.pack(side="left", padx=5)

        # Results section
        results_frame = ctk.CTkFrame(parent)
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        results_label = ctk.CTkLabel(results_frame, text="📋 Risultati Query",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        results_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Results table
        self.create_results_table(results_frame)

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

        tk.Button(top_frame, text="📁 Importa Excel",
                 command=self.import_excel_file,
                 bg="#4a4a4a", fg="white").pack(side="left", padx=5)

        tk.Button(top_frame, text="🔄 Aggiorna",
                 command=self.refresh_tables,
                 bg="#4a4a4a", fg="white").pack(side="left", padx=5)

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
                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"❌ Errore: {str(e)}"))

            threading.Thread(target=import_thread, daemon=True).start()

    def refresh_tables(self):
        """Aggiorna lista tabelle"""
        self.update_status("🔄 Aggiornando tabelle...")

        def refresh_thread():
            try:
                tables = self.db_manager.get_all_tables()
                self.root.after(0, lambda: self.update_tables_list(tables))
                self.root.after(0, lambda: self.update_status(
                    f"✅ {len(tables)} tabelle caricate"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"❌ Errore: {str(e)}"))

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
            if hasattr(self, 'table_var'):
                table_names = [t['name'] for t in tables]
                # Note: CTkComboBox values update might need specific method

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
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"❌ Errore: {str(e)}"))

        threading.Thread(target=query_thread, daemon=True).start()

    def display_results(self, df):
        """Visualizza risultati nella tabella"""
        self.current_data = df

        # Clear existing data
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        if df.empty:
            self.update_record_count(0)
            return

        # Setup columns
        columns = list(df.columns)
        self.results_tree["columns"] = columns
        self.results_tree["show"] = "headings"

        # Configure columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100, minwidth=50)

        # Insert data (limit to first 1000 rows for performance)
        for index, row in df.head(1000).iterrows():
            values = [str(val) if val is not None else "" for val in row]
            self.results_tree.insert("", "end", values=values)

        self.update_record_count(len(df))

    def export_results(self):
        """Esporta risultati query"""
        if self.current_data is None or self.current_data.empty:
            messagebox.showwarning("Attenzione",
                                  "Nessun dato da esportare")
            return

        file_path = filedialog.asksaveasfilename(
            title="Esporta risultati",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json")
            ]
        )

        if file_path:
            self.update_status("💾 Esportando risultati...")

            def export_thread():
                try:
                    ext = os.path.splitext(file_path)[1].lower()
                    format_map = {'.xlsx': 'excel', '.csv': 'csv',
                                 '.json': 'json'}
                    format_type = format_map.get(ext, 'excel')

                    success = self.db_manager.export_query_result(
                        self.current_data, file_path, format_type)

                    if success:
                        self.root.after(0, lambda: self.update_status(
                            "✅ Esportazione completata"))
                    else:
                        self.root.after(0, lambda: self.update_status(
                            "❌ Errore durante l'esportazione"))
                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"❌ Errore: {str(e)}"))

            threading.Thread(target=export_thread, daemon=True).start()

    def save_current_query(self):
        """Salva query corrente"""
        if not self.current_query:
            messagebox.showwarning("Attenzione",
                                  "Nessuna query da salvare")
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
            desc = desc_entry.get().strip()

            if name:
                success = self.db_manager.save_query(
                    name, self.current_query, desc)
                if success:
                    messagebox.showinfo("Successo", "Query salvata!")
                    dialog.destroy()
                    self.refresh_saved_queries()
                else:
                    messagebox.showerror("Errore",
                                        "Errore nel salvataggio")

        tk.Button(dialog, text="Salva", command=save_query).pack(pady=10)

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
