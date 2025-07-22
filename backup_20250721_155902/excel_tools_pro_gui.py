#!/usr/bin/env python3
"""
🖥️ GUI PROFESSIONALE EXCELTOOLS PRO DATABASE
============================================

Interfaccia utente avanzata e user-friendly per la gestione database
con funzionalità complete di query, filtri e esportazione.

Autore: Senior DB Manager IT DEV
Data: 2025-07-16
Versione: Professional GUI 3.0
"""

import os
import threading
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
from excel_database_enterprise_complete import ExcelDatabaseEnterprise

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    HAS_CUSTOMTKINTER = True
except ImportError:
    HAS_CUSTOMTKINTER = False


class ExcelToolsProGUI:
    """Interfaccia grafica professionale per ExcelTools Pro"""

    def __init__(self):
        self.db_enterprise = ExcelDatabaseEnterprise()
        self.current_table = None
        self.current_data = None
        self.current_query = ""
        self.filter_conditions = []
        self.setup_main_window()

    def setup_main_window(self):
        """Configura finestra principale"""
        if HAS_CUSTOMTKINTER:
            self.root = ctk.CTk()
            self.root.title(
                "🏢 ExcelTools Pro - Database Enterprise Manager")
            self.root.geometry("1600x1000")
            self.create_modern_interface()
        else:
            self.root = tk.Tk()
            self.root.title(
                "🏢 ExcelTools Pro - Database Enterprise Manager")
            self.root.geometry("1600x1000")
            self.create_classic_interface()

        # Carica dati iniziali
        self.refresh_all_data()

    def create_modern_interface(self):
        """Crea interfaccia moderna con CustomTkinter"""
        # Container principale
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Toolbar superiore
        self.create_main_toolbar(main_container)

        # Area contenuto principale (3 pannelli)
        content_area = ctk.CTkFrame(main_container)
        content_area.pack(fill="both", expand=True, pady=(10, 0))

        # Pannello sinistro - Navigazione tabelle
        left_panel = ctk.CTkFrame(content_area, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)
        self.create_tables_panel(left_panel)

        # Pannello centrale - Query e risultati
        center_panel = ctk.CTkFrame(content_area)
        center_panel.pack(side="left", fill="both", expand=True, padx=5)
        self.create_main_panel(center_panel)

        # Pannello destro - Strumenti e filtri
        right_panel = ctk.CTkFrame(content_area, width=300)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)
        self.create_tools_panel(right_panel)

        # Barra di stato
        self.create_status_bar(main_container)

    def create_classic_interface(self):
        """Crea interfaccia classica con Tkinter"""
        # Menu principale
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Importa Excel",
                             command=self.import_excel)
        file_menu.add_command(label="Esporta Risultati",
                             command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # Menu Database
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Aggiorna Tabelle",
                           command=self.refresh_tables)
        db_menu.add_command(label="Ottimizza Database",
                           command=self.optimize_db)

        # Notebook per organizzare le tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab principale - Esplora Database
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="🏠 Database Explorer")
        self.create_main_tab_content()

        # Tab Query Builder
        self.query_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.query_tab, text="🔧 Query Builder")
        self.create_query_tab_content()

        # Tab Statistiche
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="📊 Statistiche")
        self.create_stats_tab_content()

    def create_main_toolbar(self, parent):
        """Crea toolbar principale"""
        toolbar_frame = ctk.CTkFrame(parent, height=70)
        toolbar_frame.pack(fill="x", pady=(0, 10))
        toolbar_frame.pack_propagate(False)

        # Sezione File
        file_section = ctk.CTkFrame(toolbar_frame)
        file_section.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(
            file_section, text="📁 Importa Excel",
            command=self.import_excel, width=140, height=45
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            file_section, text="💾 Esporta Dati",
            command=self.export_results, width=140, height=45
        ).pack(side="left", padx=5)

        # Sezione Database
        db_section = ctk.CTkFrame(toolbar_frame)
        db_section.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(
            db_section, text="🔄 Aggiorna",
            command=self.refresh_all_data, width=120, height=45
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            db_section, text="🧹 Ottimizza",
            command=self.optimize_db, width=120, height=45
        ).pack(side="left", padx=5)

        # Sezione Query
        query_section = ctk.CTkFrame(toolbar_frame)
        query_section.pack(side="right", fill="y", padx=10, pady=10)

        ctk.CTkButton(
            query_section, text="▶️ Esegui Query",
            command=self.execute_query, width=140, height=45
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            query_section, text="💾 Salva Query",
            command=self.save_query, width=140, height=45
        ).pack(side="left", padx=5)

    def create_tables_panel(self, parent):
        """Crea pannello navigazione tabelle"""
        # Titolo
        title_label = ctk.CTkLabel(
            parent, text="📊 Database Tables",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(15, 10))

        # Ricerca tabelle
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=15, pady=10)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Cerca tabelle...",
            textvariable=self.search_var
        )
        search_entry.pack(fill="x", padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.filter_tables_list)

        # Lista tabelle scrollabile
        self.tables_container = ctk.CTkScrollableFrame(parent)
        self.tables_container.pack(fill="both", expand=True, padx=15, pady=10)

        # Informazioni tabella selezionata
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=15, pady=10)

        info_label = ctk.CTkLabel(
            info_frame, text="ℹ️ Info Tabella",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_label.pack(pady=5)

        self.table_info_text = ctk.CTkTextbox(info_frame, height=120)
        self.table_info_text.pack(fill="x", padx=10, pady=5)

    def create_main_panel(self, parent):
        """Crea pannello principale con query e risultati"""
        # Sezione Query Builder
        query_section = ctk.CTkFrame(parent)
        query_section.pack(fill="x", padx=10, pady=10)

        query_title = ctk.CTkLabel(
            query_section, text="🔧 SQL Query Builder",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        query_title.pack(anchor="w", padx=15, pady=(15, 5))

        # Editor SQL
        editor_frame = ctk.CTkFrame(query_section)
        editor_frame.pack(fill="x", padx=15, pady=10)

        # Textarea per SQL con scrollbar
        sql_container = tk.Frame(editor_frame)
        sql_container.pack(fill="x", padx=10, pady=10)

        self.sql_text = tk.Text(
            sql_container, height=6, bg="#2b2b2b", fg="white",
            insertbackground="white", font=("Consolas", 11),
            wrap=tk.WORD
        )
        sql_scrollbar = tk.Scrollbar(sql_container, command=self.sql_text.yview)
        self.sql_text.configure(yscrollcommand=sql_scrollbar.set)

        self.sql_text.pack(side="left", fill="both", expand=True)
        sql_scrollbar.pack(side="right", fill="y")

        # Controlli rapidi
        controls_frame = ctk.CTkFrame(query_section)
        controls_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Selezione tabella
        table_frame = ctk.CTkFrame(controls_frame)
        table_frame.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(table_frame, text="Tabella:").pack(anchor="w", padx=5)
        self.selected_table_var = tk.StringVar()
        self.table_combo = ctk.CTkComboBox(
            table_frame, variable=self.selected_table_var,
            command=self.on_table_selected, width=200
        )
        self.table_combo.pack(padx=5, pady=5)

        # Limite risultati
        limit_frame = ctk.CTkFrame(controls_frame)
        limit_frame.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(limit_frame, text="Limite:").pack(anchor="w", padx=5)
        self.limit_var = tk.StringVar(value="100")
        limit_combo = ctk.CTkComboBox(
            limit_frame, variable=self.limit_var,
            values=["50", "100", "500", "1000", "5000"], width=100
        )
        limit_combo.pack(padx=5, pady=5)

        # Sezione Risultati
        results_section = ctk.CTkFrame(parent)
        results_section.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        results_title = ctk.CTkLabel(
            results_section, text="📋 Risultati Query",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_title.pack(anchor="w", padx=15, pady=(15, 5))

        # Tabella risultati
        self.create_results_table(results_section)

    def create_results_table(self, parent):
        """Crea tabella risultati professionale"""
        table_container = ctk.CTkFrame(parent)
        table_container.pack(fill="both", expand=True, padx=15, pady=10)

        # Frame per Treeview con scrollbars
        tree_frame = tk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview per i risultati
        self.results_tree = ttk.Treeview(tree_frame)
        self.results_tree.pack(side="left", fill="both", expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.results_tree.yview
        )
        v_scrollbar.pack(side="right", fill="y")
        self.results_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.results_tree.xview
        )
        h_scrollbar.pack(side="bottom", fill="x")
        self.results_tree.configure(xscrollcommand=h_scrollbar.set)

        # Style per la tabella
        style = ttk.Style()
        style.configure("Treeview",
                       background="#3c3c3c",
                       foreground="white",
                       fieldbackground="#3c3c3c",
                       font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                       background="#4a4a4a",
                       foreground="white",
                       font=("Segoe UI", 9, "bold"))

    def create_tools_panel(self, parent):
        """Crea pannello strumenti e filtri"""
        # Filtri avanzati
        filters_frame = ctk.CTkFrame(parent)
        filters_frame.pack(fill="x", padx=10, pady=10)

        filters_title = ctk.CTkLabel(
            filters_frame, text="🔍 Filtri Avanzati",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filters_title.pack(pady=10)

        # Container filtri scrollabile
        self.filters_container = ctk.CTkScrollableFrame(filters_frame,
                                                       height=200)
        self.filters_container.pack(fill="x", padx=10, pady=5)

        # Pulsante aggiungi filtro
        ctk.CTkButton(
            filters_frame, text="➕ Aggiungi Filtro",
            command=self.add_filter, width=200
        ).pack(pady=10)

        # Query salvate
        saved_frame = ctk.CTkFrame(parent)
        saved_frame.pack(fill="x", padx=10, pady=10)

        saved_title = ctk.CTkLabel(
            saved_frame, text="📚 Query Salvate",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        saved_title.pack(pady=10)

        self.saved_queries_container = ctk.CTkScrollableFrame(saved_frame,
                                                             height=200)
        self.saved_queries_container.pack(fill="x", padx=10, pady=5)

        # Statistiche database
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        stats_title = ctk.CTkLabel(
            stats_frame, text="📊 Statistiche Database",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        stats_title.pack(pady=10)

        self.stats_display = ctk.CTkTextbox(stats_frame)
        self.stats_display.pack(fill="both", expand=True, padx=10, pady=5)

    def create_status_bar(self, parent):
        """Crea barra di stato"""
        status_frame = ctk.CTkFrame(parent, height=40)
        status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="✅ Sistema pronto")
        status_label = ctk.CTkLabel(status_frame, textvariable=self.status_var)
        status_label.pack(side="left", padx=15, pady=10)

        self.records_var = tk.StringVar(value="0 record")
        records_label = ctk.CTkLabel(status_frame, textvariable=self.records_var)
        records_label.pack(side="right", padx=15, pady=10)

    def create_main_tab_content(self):
        """Contenuto tab principale per interfaccia classica"""
        # Toolbar
        toolbar = tk.Frame(self.main_tab, bg="#f0f0f0")
        toolbar.pack(fill="x", padx=5, pady=5)

        tk.Button(toolbar, text="📁 Importa Excel",
                 command=self.import_excel).pack(side="left", padx=5)
        tk.Button(toolbar, text="🔄 Aggiorna",
                 command=self.refresh_tables).pack(side="left", padx=5)
        tk.Button(toolbar, text="▶️ Esegui Query",
                 command=self.execute_query).pack(side="left", padx=5)

        # Area principale
        main_area = tk.PanedWindow(self.main_tab, orient=tk.HORIZONTAL)
        main_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Pannello tabelle
        tables_frame = tk.Frame(main_area)
        main_area.add(tables_frame, width=300)

        tk.Label(tables_frame, text="📊 Tabelle Database",
                font=("Arial", 12, "bold")).pack(pady=5)

        self.tables_listbox = tk.Listbox(tables_frame)
        self.tables_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.tables_listbox.bind("<<ListboxSelect>>", self.on_table_select)

        # Pannello risultati
        results_frame = tk.Frame(main_area)
        main_area.add(results_frame)

        tk.Label(results_frame, text="📋 Risultati",
                font=("Arial", 12, "bold")).pack(pady=5)

        self.results_tree = ttk.Treeview(results_frame)
        self.results_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def create_query_tab_content(self):
        """Contenuto tab query builder"""
        # Editor SQL
        tk.Label(self.query_tab, text="🔧 Editor SQL",
                font=("Arial", 12, "bold")).pack(pady=5)

        self.sql_text = tk.Text(self.query_tab, height=10)
        self.sql_text.pack(fill="x", padx=10, pady=5)

        # Controlli
        controls_frame = tk.Frame(self.query_tab)
        controls_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(controls_frame, text="▶️ Esegui",
                 command=self.execute_query).pack(side="left", padx=5)
        tk.Button(controls_frame, text="💾 Salva",
                 command=self.save_query).pack(side="left", padx=5)
        tk.Button(controls_frame, text="🧹 Pulisci",
                 command=self.clear_query).pack(side="left", padx=5)

    def create_stats_tab_content(self):
        """Contenuto tab statistiche"""
        tk.Label(self.stats_tab, text="📊 Statistiche Database",
                font=("Arial", 12, "bold")).pack(pady=5)

        self.stats_display = tk.Text(self.stats_tab, height=20)
        self.stats_display.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Button(self.stats_tab, text="🔄 Aggiorna Statistiche",
                 command=self.update_stats).pack(pady=5)

    def import_excel(self):
        """Importa file Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if file_path:
            self.update_status("📥 Importando file Excel...")

            def import_task():
                try:
                    result = self.db_enterprise.import_excel_comprehensive(
                        file_path)

                    if result['success']:
                        msg = (f"✅ Import completato: "
                               f"{len(result['tables_created'])} tabelle, "
                               f"{result['total_rows']} righe totali")
                        self.root.after(0, lambda: self.update_status(msg))
                        self.root.after(0, self.refresh_all_data)
                    else:
                        errors = "; ".join(result['errors'])
                        msg = f"❌ Errori import: {errors}"
                        self.root.after(0, lambda: self.update_status(msg))

                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"❌ Errore: {str(e)}"))

            threading.Thread(target=import_task, daemon=True).start()

    def refresh_all_data(self):
        """Aggiorna tutti i dati dell'interfaccia"""
        self.update_status("🔄 Aggiornando dati...")

        def refresh_task():
            try:
                # Ottieni tabelle
                tables = self.db_enterprise.get_all_tables_info()
                self.root.after(0, lambda: self.update_tables_display(tables))

                # Ottieni query salvate
                queries = self.db_enterprise.get_saved_queries()
                self.root.after(0, lambda: self.update_saved_queries(queries))

                # Aggiorna statistiche
                self.root.after(0, self.update_database_stats)

                msg = f"✅ Aggiornamento completato: {len(tables)} tabelle"
                self.root.after(0, lambda: self.update_status(msg))

            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"❌ Errore aggiornamento: {str(e)}"))

        threading.Thread(target=refresh_task, daemon=True).start()

    def update_tables_display(self, tables):
        """Aggiorna visualizzazione tabelle"""
        if HAS_CUSTOMTKINTER and hasattr(self, 'tables_container'):
            # Pulisci container
            for widget in self.tables_container.winfo_children():
                widget.destroy()

            # Aggiungi pulsanti tabelle
            for table in tables:
                table_btn = ctk.CTkButton(
                    self.tables_container,
                    text=f"📊 {table['name']}\n{table['total_rows']} righe",
                    command=lambda t=table: self.select_table(t),
                    height=60, anchor="w"
                )
                table_btn.pack(fill="x", pady=5)

            # Aggiorna combo box
            if hasattr(self, 'table_combo'):
                table_names = [t['name'] for t in tables]
                self.table_combo.configure(values=table_names)

        elif hasattr(self, 'tables_listbox'):
            # Interfaccia classica
            self.tables_listbox.delete(0, tk.END)
            for table in tables:
                display_text = f"{table['name']} ({table['total_rows']} righe)"
                self.tables_listbox.insert(tk.END, display_text)

    def select_table(self, table_info):
        """Seleziona tabella e mostra preview"""
        self.current_table = table_info['name']
        self.selected_table_var.set(self.current_table)

        # Aggiorna info tabella
        info_text = (
            f"Tabella: {table_info['name']}\n"
            f"Righe: {table_info['total_rows']}\n"
            f"Colonne: {table_info['total_columns']}\n"
            f"Fonte: {table_info['source_file']}\n"
            f"Creata: {table_info['created_at']}"
        )

        if hasattr(self, 'table_info_text'):
            self.table_info_text.delete("1.0", tk.END)
            self.table_info_text.insert("1.0", info_text)

        # Genera query preview
        limit = self.limit_var.get()
        query = f"SELECT * FROM [{self.current_table}] LIMIT {limit}"

        if hasattr(self, 'sql_text'):
            self.sql_text.delete(1.0, tk.END)
            self.sql_text.insert(1.0, query)

        # Esegui preview automatico
        self.execute_query()

    def on_table_selected(self, selected_table):
        """Callback per selezione tabella da combo"""
        if selected_table:
            # Trova info tabella
            tables = self.db_enterprise.get_all_tables_info()
            table_info = next(
                (t for t in tables if t['name'] == selected_table), None)
            if table_info:
                self.select_table(table_info)

    def execute_query(self):
        """Esegue query SQL"""
        if hasattr(self, 'sql_text'):
            query = self.sql_text.get(1.0, tk.END).strip()
        else:
            query = ""

        if not query:
            messagebox.showwarning("Attenzione", "Inserisci una query SQL")
            return

        self.current_query = query
        self.update_status("⚡ Eseguendo query...")

        def query_task():
            try:
                result = self.db_enterprise.execute_advanced_query(query)

                if result is not None:
                    self.root.after(0, lambda: self.display_query_results(result))
                    msg = f"✅ Query completata: {len(result)} risultati"
                    self.root.after(0, lambda: self.update_status(msg))
                else:
                    self.root.after(0, lambda: self.update_status(
                        "❌ Errore nell'esecuzione della query"))

            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"❌ Errore query: {str(e)}"))

        threading.Thread(target=query_task, daemon=True).start()

    def display_query_results(self, df):
        """Visualizza risultati query nella tabella"""
        self.current_data = df

        # Pulisci tabella esistente
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        if df.empty:
            self.update_records_count(0)
            return

        # Configura colonne
        columns = list(df.columns)
        self.results_tree["columns"] = columns
        self.results_tree["show"] = "headings"

        # Imposta intestazioni colonne
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120, minwidth=80)

        # Inserisci dati (limita per performance)
        max_display = 2000
        for index, row in df.head(max_display).iterrows():
            values = []
            for val in row:
                if val is None:
                    values.append("")
                elif isinstance(val, float):
                    values.append(f"{val:.2f}")
                else:
                    values.append(str(val))

            self.results_tree.insert("", "end", values=values)

        self.update_records_count(len(df))

        # Mostra messaggio se i dati sono stati limitati
        if len(df) > max_display:
            msg = f"⚠️ Visualizzati {max_display} di {len(df)} risultati"
            self.update_status(msg)

    def export_results(self):
        """Esporta risultati correnti"""
        if self.current_data is None or self.current_data.empty:
            messagebox.showwarning("Attenzione", "Nessun dato da esportare")
            return

        file_path = filedialog.asksaveasfilename(
            title="Esporta risultati",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("HTML files", "*.html")
            ]
        )

        if file_path:
            self.update_status("💾 Esportando risultati...")

            def export_task():
                try:
                    # Determina formato da estensione
                    ext = os.path.splitext(file_path)[1].lower()
                    format_map = {
                        '.xlsx': 'excel',
                        '.csv': 'csv',
                        '.json': 'json',
                        '.html': 'html'
                    }
                    export_format = format_map.get(ext, 'excel')

                    success = self.db_enterprise.export_flexible(
                        self.current_data, file_path, export_format)

                    if success:
                        msg = f"✅ Esportazione completata: {file_path}"
                        self.root.after(0, lambda: self.update_status(msg))
                        self.root.after(0, lambda: messagebox.showinfo(
                            "Successo", f"Dati esportati in:\n{file_path}"))
                    else:
                        self.root.after(0, lambda: self.update_status(
                            "❌ Errore durante l'esportazione"))

                except Exception as e:
                    self.root.after(0, lambda: self.update_status(
                        f"❌ Errore esportazione: {str(e)}"))

            threading.Thread(target=export_task, daemon=True).start()

    def save_query(self):
        """Salva query corrente"""
        if not self.current_query:
            messagebox.showwarning("Attenzione", "Nessuna query da salvare")
            return

        # Dialog per salvare query
        dialog = tk.Toplevel(self.root)
        dialog.title("Salva Query")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Layout dialog
        tk.Label(dialog, text="Nome Query:",
                font=("Arial", 10, "bold")).pack(pady=10)
        name_entry = tk.Entry(dialog, width=50)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="Descrizione:",
                font=("Arial", 10, "bold")).pack(pady=10)
        desc_text = tk.Text(dialog, height=5, width=50)
        desc_text.pack(pady=5)

        # Checkbox preferiti
        is_favorite_var = tk.BooleanVar()
        tk.Checkbutton(dialog, text="Aggiungi ai preferiti",
                      variable=is_favorite_var).pack(pady=5)

        def save_action():
            name = name_entry.get().strip()
            desc = desc_text.get(1.0, tk.END).strip()
            is_fav = is_favorite_var.get()

            if name:
                success = self.db_enterprise.save_query_advanced(
                    name, self.current_query, desc, is_fav)

                if success:
                    messagebox.showinfo("Successo", "Query salvata!")
                    dialog.destroy()
                    self.refresh_saved_queries()
                else:
                    messagebox.showerror("Errore", "Errore nel salvataggio")
            else:
                messagebox.showwarning("Attenzione", "Inserisci un nome")

        tk.Button(dialog, text="💾 Salva Query",
                 command=save_action, font=("Arial", 10, "bold")).pack(pady=20)

    def refresh_saved_queries(self):
        """Aggiorna lista query salvate"""
        queries = self.db_enterprise.get_saved_queries()
        self.update_saved_queries(queries)

    def update_saved_queries(self, queries):
        """Aggiorna visualizzazione query salvate"""
        if hasattr(self, 'saved_queries_container'):
            # Pulisci container
            for widget in self.saved_queries_container.winfo_children():
                widget.destroy()

            # Aggiungi pulsanti query
            for query in queries:
                query_frame = ctk.CTkFrame(self.saved_queries_container)
                query_frame.pack(fill="x", pady=2)

                # Nome query con icona preferiti
                icon = "⭐" if query['is_favorite'] else "📝"
                display_name = f"{icon} {query['name']}"

                query_btn = ctk.CTkButton(
                    query_frame, text=display_name,
                    command=lambda q=query: self.load_saved_query(q),
                    height=35, anchor="w"
                )
                query_btn.pack(fill="x", padx=5, pady=2)

    def load_saved_query(self, query_info):
        """Carica query salvata nell'editor"""
        if hasattr(self, 'sql_text'):
            self.sql_text.delete(1.0, tk.END)
            self.sql_text.insert(1.0, query_info['sql_query'])

        # Mostra descrizione se presente
        if query_info.get('description'):
            messagebox.showinfo("Query Info",
                               f"Nome: {query_info['name']}\n\n"
                               f"Descrizione:\n{query_info['description']}")

    def optimize_db(self):
        """Ottimizza database"""
        self.update_status("🔧 Ottimizzando database...")

        def optimize_task():
            try:
                result = self.db_enterprise.optimize_database()

                if result['success']:
                    size_mb = result['database_size_mb']
                    msg = f"✅ Database ottimizzato: {size_mb} MB"
                    self.root.after(0, lambda: self.update_status(msg))
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Ottimizzazione Completata",
                        f"Database ottimizzato con successo!\n"
                        f"Dimensione: {size_mb} MB\n"
                        f"Pagine: {result['page_count']}"))
                else:
                    error = result.get('error', 'Errore sconosciuto')
                    self.root.after(0, lambda: self.update_status(
                        f"❌ Errore ottimizzazione: {error}"))

            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"❌ Errore: {str(e)}"))

        threading.Thread(target=optimize_task, daemon=True).start()

    def add_filter(self):
        """Aggiunge nuovo filtro"""
        if not self.current_table:
            messagebox.showwarning("Attenzione",
                                  "Seleziona prima una tabella")
            return

        # Ottieni colonne tabella corrente
        tables = self.db_enterprise.get_all_tables_info()
        table_info = next(
            (t for t in tables if t['name'] == self.current_table), None)

        if not table_info:
            return

        # Dialog per nuovo filtro
        dialog = tk.Toplevel(self.root)
        dialog.title("Aggiungi Filtro")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Selezione colonna
        tk.Label(dialog, text="Colonna:").pack(pady=5)
        column_var = tk.StringVar()
        column_combo = ttk.Combobox(dialog, textvariable=column_var,
                                   values=table_info['columns'])
        column_combo.pack(pady=5)

        # Operatore
        tk.Label(dialog, text="Operatore:").pack(pady=5)
        operator_var = tk.StringVar(value="=")
        operator_combo = ttk.Combobox(dialog, textvariable=operator_var,
                                     values=["=", "!=", ">", "<", ">=", "<=",
                                            "LIKE", "IN"])
        operator_combo.pack(pady=5)

        # Valore
        tk.Label(dialog, text="Valore:").pack(pady=5)
        value_entry = tk.Entry(dialog, width=30)
        value_entry.pack(pady=5)

        def apply_filter():
            column = column_var.get()
            operator = operator_var.get()
            value = value_entry.get()

            if column and value:
                # Aggiungi filtro alla lista
                filter_condition = {
                    'column': column,
                    'operator': operator,
                    'value': value
                }
                self.filter_conditions.append(filter_condition)

                # Aggiorna query
                self.apply_filters_to_query()
                dialog.destroy()
            else:
                messagebox.showwarning("Attenzione",
                                      "Compila tutti i campi")

        tk.Button(dialog, text="Applica Filtro",
                 command=apply_filter).pack(pady=20)

    def apply_filters_to_query(self):
        """Applica filtri correnti alla query"""
        if not self.current_table or not self.filter_conditions:
            return

        # Costruisci query con filtri
        query = self.db_enterprise.build_filtered_query(
            self.current_table,
            filters=self.filter_conditions,
            limit=int(self.limit_var.get())
        )

        # Aggiorna editor SQL
        if hasattr(self, 'sql_text'):
            self.sql_text.delete(1.0, tk.END)
            self.sql_text.insert(1.0, query)

        # Esegui query automaticamente
        self.execute_query()

    def update_database_stats(self):
        """Aggiorna statistiche database"""
        if hasattr(self, 'stats_display'):
            try:
                tables = self.db_enterprise.get_all_tables_info()
                total_rows = sum(t['total_rows'] for t in tables)
                total_columns = sum(t['total_columns'] for t in tables)

                stats_text = f"""📊 STATISTICHE DATABASE
=====================================

📋 Tabelle totali: {len(tables)}
📊 Righe totali: {total_rows:,}
🔢 Colonne totali: {total_columns}

📈 DETTAGLIO TABELLE:
"""

                for table in tables[:10]:  # Prime 10 tabelle
                    stats_text += (f"\n• {table['name']}: "
                                  f"{table['total_rows']:,} righe, "
                                  f"{table['total_columns']} colonne")

                if len(tables) > 10:
                    stats_text += f"\n... e altre {len(tables) - 10} tabelle"

                self.stats_display.delete("1.0", tk.END)
                self.stats_display.insert("1.0", stats_text)

            except Exception as e:
                error_text = f"❌ Errore nel calcolo statistiche: {str(e)}"
                self.stats_display.delete("1.0", tk.END)
                self.stats_display.insert("1.0", error_text)

    def filter_tables_list(self, event=None):
        """Filtra lista tabelle in base alla ricerca"""
        # Implementazione filtro tabelle
        search_term = self.search_var.get().lower()
        # TODO: Implementare filtro effettivo
        pass

    def on_table_select(self, event):
        """Gestisce selezione tabella in interfaccia classica"""
        selection = self.tables_listbox.curselection()
        if selection:
            # Estrai nome tabella dal testo
            selected_text = self.tables_listbox.get(selection[0])
            table_name = selected_text.split(" (")[0]

            # Trova info tabella
            tables = self.db_enterprise.get_all_tables_info()
            table_info = next(
                (t for t in tables if t['name'] == table_name), None)
            if table_info:
                self.select_table(table_info)

    def clear_query(self):
        """Pulisce editor query"""
        if hasattr(self, 'sql_text'):
            self.sql_text.delete(1.0, tk.END)

    def update_stats(self):
        """Aggiorna tab statistiche"""
        self.update_database_stats()

    def refresh_tables(self):
        """Aggiorna solo le tabelle"""
        self.refresh_all_data()

    def update_status(self, message):
        """Aggiorna messaggio di stato"""
        if hasattr(self, 'status_var'):
            self.status_var.set(message)

    def update_records_count(self, count):
        """Aggiorna conteggio record"""
        if hasattr(self, 'records_var'):
            self.records_var.set(f"{count:,} record")

    def run(self):
        """Avvia applicazione"""
        print("🚀 Avviando ExcelTools Pro Database Enterprise Manager...")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = ExcelToolsProGUI()
        app.run()
    except Exception as e:
        print(f"❌ Errore avvio applicazione: {e}")
        import traceback
        traceback.print_exc()
