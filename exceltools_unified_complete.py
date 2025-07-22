#!/usr/bin/env python3
"""
🚀 EXCELTOOLS UNIFIED - NASA GRADE COMPLETE PLATFORM
===================================================

Sistema completo per analisi dati con AI integrata, interface responsive,
database views, merge, filtri avanzati e query execution.

Autore: NASA DevOps AI Team
Data: 2025-07-21
Versione: 3.0 - Complete & Integrated
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ Pandas not available - limited functionality")

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    HAS_CUSTOMTKINTER = True
except ImportError:
    HAS_CUSTOMTKINTER = False


class ExcelToolsUnifiedComplete:
    """🚀 Piattaforma completa NASA-grade per analisi dati"""

    def __init__(self):
        self.db_path = "exceltools_unified.db"
        self.current_data = None
        self.filtered_data = None
        self.imported_files = {}
        self.saved_views = {}
        self.current_query_result = None

        # Inizializza sistema
        self.init_database()
        self.create_main_interface()

    def init_database(self):
        """Inizializza database completo"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabella query templates
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS query_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        query TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_favorite BOOLEAN DEFAULT 0
                    )
                """)

                # Tabella viste salvate
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS saved_views (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        table_name TEXT,
                        columns_config TEXT,
                        filters_config TEXT,
                        query TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_used TIMESTAMP,
                        is_favorite BOOLEAN DEFAULT 0
                    )
                """)

                # Tabella configurazioni merge
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS merge_configs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        config_data TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Inserisci template di base se non esistono
                self.insert_default_templates(cursor)

                conn.commit()
                print("✅ Database inizializzato correttamente")

        except Exception as e:
            print(f"❌ Errore inizializzazione database: {e}")

    def insert_default_templates(self, cursor):
        """Inserisce template AI di default"""
        default_templates = [
            ("Mostra tutte le colonne",
             "basic",
             "SELECT * FROM [table_name] LIMIT 100;",
             "Visualizza tutti i dati"),
            ("Mostra colonna specifica",
             "selection",
             "SELECT [column_name] FROM [table_name];",
             "Mostra una singola colonna"),
            ("Filtro maggiore di",
             "filter",
             "SELECT * FROM [table_name] WHERE [column] > value;",
             "Filtra valori numerici"),
            ("Conteggio righe",
             "aggregate",
             "SELECT COUNT(*) as Total FROM [table_name];",
             "Conta tutte le righe"),
            ("Raggruppa e conta",
             "aggregate",
             "SELECT [column], COUNT(*) FROM [table_name] GROUP BY [column];",
             "Raggruppa per colonna"),
            ("Top 10 valori",
             "analysis",
             "SELECT * FROM [table_name] ORDER BY [column] DESC LIMIT 10;",
             "Top 10 record"),
            ("Valori unici",
             "analysis",
             "SELECT DISTINCT [column] FROM [table_name];",
             "Trova valori univoci"),
            ("Media per gruppo",
             "statistics",
             "SELECT [group_col], AVG([value_col]) "
             "FROM [table_name] GROUP BY [group_col];",
             "Calcola medie")]

        for name, category, query, description in default_templates:
            cursor.execute("""
                INSERT OR IGNORE INTO query_templates
                (name, category, query, description)
                VALUES (?, ?, ?, ?)
            """, (name, category, query, description))

    def create_main_interface(self):
        """Crea interfaccia principale completa"""
        self.root = tk.Tk()
        self.root.title("🚀 NASA ExcelTools Unified - Complete Platform")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#1e1e1e")

        # Stile
        self.setup_advanced_style()

        # Menu
        self.create_advanced_menu()

        # Toolbar completo
        self.create_complete_toolbar()

        # Area principale con pannelli
        self.create_advanced_layout()

        # Status bar avanzata
        self.create_advanced_status_bar()

        # Carica AI system
        self.init_ai_system()

        # Bind eventi
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_advanced_style(self):
        """Setup stile avanzato NASA-grade"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Colori NASA-grade
        colors = {
            'bg_main': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3c3c3c',
            'accent': '#0078d4',
            'success': '#107c10',
            'warning': '#ff8c00',
            'error': '#d13438',
            'text': '#ffffff',
            'text_muted': '#cccccc'
        }

        # Configura stili
        self.style.configure("NASA.TFrame", background=colors['bg_secondary'])
        self.style.configure("NASA.TLabel", background=colors['bg_secondary'],
                             foreground=colors['text'], font=("Segoe UI", 10))
        self.style.configure("NASA.TButton", background=colors['accent'],
                             foreground=colors['text'], font=("Segoe UI", 9))
        self.style.configure(
            "NASA.Heading.TLabel",
            background=colors['bg_secondary'],
            foreground=colors['accent'],
            font=(
                "Segoe UI",
                12,
                "bold"))

    def create_advanced_menu(self):
        """Crea menu avanzato"""
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white")
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="🔄 Import Single File",
                              command=self.import_single_file)
        file_menu.add_command(label="📂 Import Multiple Files",
                              command=self.import_multiple_files)
        file_menu.add_separator()
        file_menu.add_command(label="💾 Export Current View",
                              command=self.export_current_view)
        file_menu.add_command(label="📊 Export Query Result",
                              command=self.export_query_result)
        file_menu.add_separator()
        file_menu.add_command(label="🔄 Reload Data",
                              command=self.reload_current_data)
        file_menu.add_command(label="❌ Exit", command=self.on_closing)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="🤖 AI Query Builder",
                               command=self.open_ai_query_builder)
        tools_menu.add_command(label="🔗 Data Merge Tool",
                               command=self.open_merge_tool)
        tools_menu.add_command(label="🔍 Advanced Filters",
                               command=self.open_advanced_filters)
        tools_menu.add_command(
            label="👁️ Saved Views Manager", command=self.open_views_manager)
        tools_menu.add_separator()
        tools_menu.add_command(
            label="📊 Statistics Dashboard", command=self.open_statistics)
        tools_menu.add_command(label="🔧 Database Tools",
                               command=self.open_database_tools)

        # AI menu
        ai_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="AI", menu=ai_menu)
        ai_menu.add_command(label="🧠 Quick AI Query",
                            command=self.quick_ai_query)
        ai_menu.add_command(label="📝 Query Templates",
                            command=self.open_query_templates)
        ai_menu.add_command(label="🔍 Smart Suggestions",
                            command=self.show_smart_suggestions)
        ai_menu.add_command(label="📚 AI Learning Mode",
                            command=self.toggle_ai_learning)

    def create_complete_toolbar(self):
        """Crea toolbar completa con tutte le funzioni"""
        toolbar = ttk.Frame(self.root, style="NASA.TFrame")
        toolbar.pack(fill="x", padx=5, pady=5)

        # Sezione Import/Export
        import_frame = ttk.LabelFrame(
            toolbar, text="📂 Data Management", padding=5)
        import_frame.pack(side="left", padx=5)

        ttk.Button(
            import_frame,
            text="Import File",
            command=self.import_single_file,
            style="NASA.TButton").pack(
            side="left",
            padx=2)
        ttk.Button(
            import_frame,
            text="Import Multi",
            command=self.import_multiple_files,
            style="NASA.TButton").pack(
            side="left",
            padx=2)
        ttk.Button(
            import_frame,
            text="Export",
            command=self.export_current_view,
            style="NASA.TButton").pack(
            side="left",
            padx=2)

        # Sezione AI
        ai_frame = ttk.LabelFrame(toolbar, text="🤖 AI Tools", padding=5)
        ai_frame.pack(side="left", padx=5)

        ttk.Button(
            ai_frame,
            text="AI Query",
            command=self.open_ai_query_builder,
            style="NASA.TButton").pack(
            side="left",
            padx=2)
        ttk.Button(
            ai_frame,
            text="Templates",
            command=self.open_query_templates,
            style="NASA.TButton").pack(
            side="left",
            padx=2)

        # Sezione Analysis
        analysis_frame = ttk.LabelFrame(toolbar, text="📊 Analysis", padding=5)
        analysis_frame.pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="Filters",
            command=self.open_advanced_filters,
            style="NASA.TButton").pack(
            side="left",
            padx=2)
        ttk.Button(analysis_frame, text="Merge", command=self.open_merge_tool,
                   style="NASA.TButton").pack(side="left", padx=2)
        ttk.Button(analysis_frame, text="Stats", command=self.open_statistics,
                   style="NASA.TButton").pack(side="left", padx=2)

        # Status indicators
        status_frame = ttk.Frame(toolbar)
        status_frame.pack(side="right", padx=10)

        self.data_status = ttk.Label(
            status_frame, text="🔴 No Data", style="NASA.TLabel")
        self.data_status.pack(side="right", padx=5)

        self.ai_status = ttk.Label(
            status_frame, text="🤖 AI Ready", style="NASA.TLabel")
        self.ai_status.pack(side="right", padx=5)

    def create_advanced_layout(self):
        """Crea layout avanzato con pannelli"""
        # Frame principale
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Pannello sinistro (navigazione e controlli)
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)

        # Pannello centrale (data view)
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side="left", fill="both", expand=True, padx=5)

        # Pannello destro (query builder e AI)
        right_panel = ttk.Frame(main_frame, width=350)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)

        # Popola pannelli
        self.create_left_panel(left_panel)
        self.create_center_panel(center_panel)
        self.create_right_panel(right_panel)

    def create_left_panel(self, parent):
        """Crea pannello sinistro di navigazione"""
        # Header
        header = ttk.Label(parent, text="📂 Data Sources",
                           style="NASA.Heading.TLabel")
        header.pack(pady=(0, 10))

        # Lista file importati
        files_frame = ttk.LabelFrame(parent, text="Imported Files")
        files_frame.pack(fill="x", pady=5)

        self.files_listbox = tk.Listbox(files_frame, bg="#3c3c3c", fg="white",
                                        selectbackground="#0078d4", height=6)
        self.files_listbox.pack(fill="x", padx=5, pady=5)
        self.files_listbox.bind("<<ListboxSelect>>", self.on_file_selected)

        # Informazioni file selezionato
        info_frame = ttk.LabelFrame(parent, text="File Info")
        info_frame.pack(fill="x", pady=5)

        self.file_info = tk.Text(
            info_frame,
            height=4,
            bg="#3c3c3c",
            fg="white",
            wrap="word",
            font=(
                "Consolas",
                9))
        self.file_info.pack(fill="x", padx=5, pady=5)

        # Viste salvate
        views_frame = ttk.LabelFrame(parent, text="Saved Views")
        views_frame.pack(fill="both", expand=True, pady=5)

        self.views_listbox = tk.Listbox(views_frame, bg="#3c3c3c", fg="white",
                                        selectbackground="#0078d4")
        self.views_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.views_listbox.bind("<<ListboxSelect>>", self.on_view_selected)

        # Pulsanti azioni
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill="x", pady=5)

        ttk.Button(buttons_frame, text="🔄 Refresh Views",
                   command=self.refresh_views_list).pack(fill="x", pady=2)
        ttk.Button(
            buttons_frame,
            text="💾 Save Current View",
            command=self.save_current_view_dialog).pack(
            fill="x",
            pady=2)

    def create_center_panel(self, parent):
        """Crea pannello centrale per visualizzazione dati"""
        # Header con controlli
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(header_frame, text="📊 Data View",
                  style="NASA.Heading.TLabel").pack(side="left")

        # Controlli view
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side="right")

        ttk.Button(controls_frame, text="🔍 Filter",
                   command=self.toggle_quick_filter).pack(side="left", padx=2)
        ttk.Button(controls_frame, text="📈 Sort",
                   command=self.show_sort_options).pack(side="left", padx=2)
        ttk.Button(controls_frame, text="🔄 Refresh",
                   command=self.refresh_data_view).pack(side="left", padx=2)

        # Quick filter (nascosto di default)
        self.quick_filter_frame = ttk.Frame(parent)
        self.create_quick_filter(self.quick_filter_frame)

        # Treeview per dati
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Treeview con scrollbars
        self.data_tree = ttk.Treeview(tree_frame, show="tree headings")

        # Scrollbars
        v_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.data_tree.yview)
        h_scroll = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.data_tree.xview)

        self.data_tree.configure(
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Grid layout
        self.data_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Info pannello sotto
        info_panel = ttk.Frame(parent)
        info_panel.pack(fill="x", pady=5)

        self.data_info_label = ttk.Label(
            info_panel, text="No data loaded", style="NASA.TLabel")
        self.data_info_label.pack(side="left")

        self.selection_info_label = ttk.Label(
            info_panel, text="", style="NASA.TLabel")
        self.selection_info_label.pack(side="right")

    def create_quick_filter(self, parent):
        """Crea controlli filtro rapido"""
        ttk.Label(parent, text="Quick Filter:",
                  style="NASA.TLabel").pack(side="left", padx=5)

        self.filter_column_var = tk.StringVar()
        self.filter_column_combo = ttk.Combobox(
            parent, textvariable=self.filter_column_var, width=15)
        self.filter_column_combo.pack(side="left", padx=2)

        self.filter_operator_var = tk.StringVar(value="contains")
        filter_ops = ["contains", "equals", "starts with",
                      "ends with", ">", "<", ">=", "<="]
        ttk.Combobox(parent, textvariable=self.filter_operator_var,
                     values=filter_ops, width=10).pack(side="left", padx=2)

        self.filter_value_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.filter_value_var,
                  width=15).pack(side="left", padx=2)

        ttk.Button(parent, text="Apply", command=self.apply_quick_filter).pack(
            side="left", padx=2)
        ttk.Button(parent, text="Clear", command=self.clear_quick_filter).pack(
            side="left", padx=2)

    def create_right_panel(self, parent):
        """Crea pannello destro AI e query"""
        # Header
        header = ttk.Label(parent, text="🤖 AI Query Builder",
                           style="NASA.Heading.TLabel")
        header.pack(pady=(0, 10))

        # Input naturale
        input_frame = ttk.LabelFrame(parent, text="Natural Language Input")
        input_frame.pack(fill="x", pady=5)

        self.ai_input = tk.Text(
            input_frame,
            height=3,
            bg="#3c3c3c",
            fg="white",
            wrap="word",
            font=(
                "Segoe UI",
                10))
        self.ai_input.pack(fill="x", padx=5, pady=5)

        # Pulsanti AI
        ai_buttons = ttk.Frame(input_frame)
        ai_buttons.pack(fill="x", padx=5, pady=5)

        ttk.Button(ai_buttons, text="🧠 Generate SQL",
                   command=self.generate_ai_sql).pack(side="left", padx=2)
        ttk.Button(
            ai_buttons,
            text="▶️ Execute",
            command=self.execute_current_query).pack(
            side="left",
            padx=2)
        ttk.Button(ai_buttons, text="💡 Suggest",
                   command=self.show_ai_suggestions).pack(side="left", padx=2)

        # Query output
        query_frame = ttk.LabelFrame(parent, text="Generated SQL")
        query_frame.pack(fill="x", pady=5)

        self.query_output = tk.Text(
            query_frame,
            height=6,
            bg="#3c3c3c",
            fg="white",
            wrap="none",
            font=(
                "Consolas",
                10))

        # Scrollbar per query
        query_scroll = ttk.Scrollbar(
            query_frame, orient="vertical", command=self.query_output.yview)
        self.query_output.configure(yscrollcommand=query_scroll.set)

        self.query_output.pack(side="left", fill="both",
                               expand=True, padx=5, pady=5)
        query_scroll.pack(side="right", fill="y", pady=5)

        # Templates rapidi
        templates_frame = ttk.LabelFrame(parent, text="Quick Templates")
        templates_frame.pack(fill="x", pady=5)

        self.create_quick_templates(templates_frame)

        # Risultati query
        results_frame = ttk.LabelFrame(parent, text="Query Results")
        results_frame.pack(fill="both", expand=True, pady=5)

        self.results_tree = ttk.Treeview(results_frame, height=8)
        results_scroll = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)

        self.results_tree.pack(side="left", fill="both",
                               expand=True, padx=5, pady=5)
        results_scroll.pack(side="right", fill="y", pady=5)

    def create_quick_templates(self, parent):
        """Crea template rapidi"""
        templates = [
            ("Show All", "SELECT * FROM [table] LIMIT 100"),
            ("Count Rows", "SELECT COUNT(*) FROM [table]"),
            ("Show Columns", "SELECT [column] FROM [table]"),
            ("Group By", "SELECT [col], COUNT(*) FROM [table] GROUP BY [col]"),
            ("Top 10", "SELECT * FROM [table] ORDER BY [col] DESC LIMIT 10")
        ]

        for i, (name, query) in enumerate(templates):
            btn = ttk.Button(
                parent,
                text=name,
                command=lambda q=query: self.load_template_query(q))
            btn.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="ew")

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    def create_advanced_status_bar(self):
        """Crea status bar avanzata"""
        status_frame = ttk.Frame(self.root, style="NASA.TFrame")
        status_frame.pack(side="bottom", fill="x", padx=5, pady=2)

        # Status principale
        self.status_label = ttk.Label(
            status_frame, text="Ready", style="NASA.TLabel")
        self.status_label.pack(side="left")

        # Separatori e info aggiuntive
        ttk.Separator(status_frame, orient="vertical").pack(
            side="left", fill="y", padx=10)

        self.rows_label = ttk.Label(
            status_frame, text="Rows: 0", style="NASA.TLabel")
        self.rows_label.pack(side="left", padx=5)

        self.cols_label = ttk.Label(
            status_frame, text="Cols: 0", style="NASA.TLabel")
        self.cols_label.pack(side="left", padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame, length=200, mode='indeterminate')
        self.progress.pack(side="right", padx=5)

    def init_ai_system(self):
        """Inizializza sistema AI"""
        try:
            from ai_query_interpreter import AdvancedAIQueryInterpreter
            self.ai_interpreter = AdvancedAIQueryInterpreter()
            self.ai_status.config(text="🤖 AI Ready")
            print("✅ AI System initialized")
        except ImportError:
            self.ai_interpreter = None
            self.ai_status.config(text="🤖 AI Unavailable")
            print("⚠️ AI System not available")

    # ========================================
    # IMPLEMENTAZIONE FUNZIONI CORE
    # ========================================

    def import_single_file(self):
        """Importa un singolo file con supporto completo"""
        file_path = filedialog.askopenfilename(
            title="Select Excel or CSV file",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All supported", "*.xlsx *.xls *.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.progress.start()
            self.status_label.config(text="Importing file...")

            # Threading per non bloccare UI
            threading.Thread(target=self._import_file_thread,
                             args=(file_path,), daemon=True).start()

    def _import_file_thread(self, file_path):
        """Importa file in thread separato"""
        try:
            if not HAS_PANDAS:
                raise Exception("Pandas required for file operations")

            filename = os.path.basename(file_path)

            # Determina tipo e carica
            if file_path.lower().endswith('.csv'):
                # Prova diversi encoding
                encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
                df = None
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                if df is None:
                    raise Exception("Could not decode CSV file")
            else:
                df = pd.read_excel(file_path)

            # Salva in database
            table_name = self._sanitize_table_name(filename)
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)

            # Aggiorna interfaccia nel thread principale
            self.root.after(0, self._update_ui_after_import,
                            filename, table_name, df)

        except Exception as e:
            self.root.after(0, self._show_import_error, str(e))

    def _update_ui_after_import(self, filename, table_name, df):
        """Aggiorna UI dopo import"""
        self.progress.stop()

        # Aggiorna dati correnti
        self.current_data = df
        self.imported_files[table_name] = df

        # Aggiorna lista file
        self.files_listbox.insert(tk.END, f"{filename} ({len(df)} rows)")

        # Aggiorna info
        info = f"File: {filename}\nRows: {
            len(df):,}\nColumns: {
            len(
                df.columns)}\nTable: {table_name}"
        self.file_info.delete("1.0", tk.END)
        self.file_info.insert("1.0", info)

        # Aggiorna data view
        self.update_data_view(df)

        # Aggiorna status
        self.update_status(f"Imported: {filename}", len(df), len(df.columns))
        self.data_status.config(text="🟢 Data Loaded")

        # Aggiorna AI context
        if self.ai_interpreter:
            self.ai_interpreter.set_data_context(df, self.imported_files)

        # Aggiorna filter columns
        self.filter_column_combo.config(values=list(df.columns))

        msg = (
            f"File imported successfully!\n{len(df)} rows, "
            f"{len(df.columns)} columns"
        )
        messagebox.showinfo("Success", msg)

    def _show_import_error(self, error_msg):
        """Mostra errore import"""
        self.progress.stop()
        self.status_label.config(text="Import failed")
        messagebox.showerror(
            "Import Error", f"Failed to import file:\n{error_msg}")

    def import_multiple_files(self):
        """Importa file multipli"""
        file_paths = filedialog.askopenfilenames(
            title="Select multiple files",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All supported", "*.xlsx *.xls *.csv")
            ]
        )

        if file_paths:
            self.progress.start()
            self.status_label.config(
                text=f"Importing {len(file_paths)} files...")

            # Threading per importazione multipla
            threading.Thread(target=self._import_multiple_thread,
                             args=(file_paths,), daemon=True).start()

    def _import_multiple_thread(self, file_paths):
        """Importa file multipli in thread"""
        imported_count = 0
        errors = []

        for file_path in file_paths:
            try:
                self._import_file_thread(file_path)
                imported_count += 1
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")

        # Aggiorna UI
        self.root.after(0, self._finish_multiple_import,
                        imported_count, len(file_paths), errors)

    def _finish_multiple_import(self, success_count, total_count, errors):
        """Finalizza import multiplo"""
        self.progress.stop()

        if errors:
            error_msg = (
                f"Imported {success_count}/{total_count} files.\n\nErrors:\n"
                + "\n".join(errors[:5])
            )
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more errors"
            messagebox.showwarning("Import Complete with Errors", error_msg)
        else:
            messagebox.showinfo(
                "Success", f"All {success_count} files imported successfully!")

        self.status_label.config(
            text=f"Imported {success_count}/{total_count} files")

    def update_data_view(self, df, title="Data View"):
        """Aggiorna visualizzazione dati principale"""
        # Clear existing data
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

        if df is None or df.empty:
            self.data_info_label.config(text="No data to display")
            return

        # Configure columns
        columns = list(df.columns)
        self.data_tree["columns"] = columns
        self.data_tree["show"] = "headings"

        # Set column headings and widths
        for col in columns:
            self.data_tree.heading(col, text=col, anchor="w")
            # Auto-adjust column width based on content
            max_width = max(
                len(str(col)) * 10,  # Header width
                df[col].astype(str).str.len().max() *
                8 if not df[col].empty else 100
            )
            self.data_tree.column(col, width=min(max_width, 200), minwidth=50)

        # Insert data (limit for performance)
        max_rows = min(1000, len(df))
        for i in range(max_rows):
            values = []
            for col in columns:
                val = df.iloc[i][col]
                if pd.isna(val):
                    values.append("")
                else:
                    values.append(str(val))
            self.data_tree.insert("", "end", values=values)

        # Update info
        if len(df) > max_rows:
            info_text = f"Showing {
                max_rows:,} of {
                len(df):,} rows, {
                len(columns)} columns"
        else:
            info_text = f"{len(df):,} rows, {len(columns)} columns"

        self.data_info_label.config(text=info_text)

    def generate_ai_sql(self):
        """Genera SQL usando AI"""
        user_input = self.ai_input.get("1.0", "end-1c").strip()

        if not user_input:
            messagebox.showwarning(
                "Warning",
                "Please enter a description of what you want to analyze"
            )
            return

        if not self.ai_interpreter:
            messagebox.showerror("Error", "AI system not available")
            return

        if self.current_data is None:
            messagebox.showwarning("Warning", "Please import data first")
            return

        try:
            # Genera SQL
            sql_query = self.ai_interpreter.interpret_query(user_input)

            # Mostra nel query output
            self.query_output.delete("1.0", tk.END)
            self.query_output.insert("1.0", sql_query)

            self.status_label.config(text="AI query generated successfully")

        except Exception as e:
            messagebox.showerror(
                "AI Error", f"Error generating query:\n{str(e)}")

    def execute_current_query(self):
        """Esegue la query corrente"""
        query = self.query_output.get("1.0", "end-1c").strip()

        if not query:
            messagebox.showwarning("Warning", "No query to execute")
            return

        try:
            self.progress.start()
            self.status_label.config(text="Executing query...")

            # Threading per non bloccare UI
            threading.Thread(target=self._execute_query_thread,
                             args=(query,), daemon=True).start()

        except Exception as e:
            self.progress.stop()
            messagebox.showerror(
                "Query Error", f"Error executing query:\n{str(e)}")

    def _execute_query_thread(self, query):
        """Esegue query in thread separato"""
        try:
            # Clean query (rimuovi commenti)
            clean_query = query
            if '--' in query:
                lines = query.split('\n')
                clean_lines = []
                for line in lines:
                    if line.strip() and not line.strip().startswith('--'):
                        clean_lines.append(line)
                clean_query = '\n'.join(clean_lines)

            # Esegui query
            with sqlite3.connect(self.db_path) as conn:
                if HAS_PANDAS:
                    result_df = pd.read_sql_query(clean_query, conn)
                    self.current_query_result = result_df
                    self.root.after(0, self._update_query_results, result_df)
                else:
                    cursor = conn.cursor()
                    cursor.execute(clean_query)
                    results = cursor.fetchall()
                    columns = []
                    if cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                    self.root.after(
                        0, self._update_query_results_simple, results, columns)

        except Exception as e:
            self.root.after(0, self._show_query_error, str(e))

    def _update_query_results(self, result_df):
        """Aggiorna risultati query con pandas"""
        self.progress.stop()

        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        if result_df.empty:
            self.status_label.config(text="Query executed - no results")
            return

        # Configure columns
        columns = list(result_df.columns)
        self.results_tree["columns"] = columns
        self.results_tree["show"] = "headings"

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)

        # Insert data (limit for performance)
        max_rows = min(100, len(result_df))
        for i in range(max_rows):
            values = [str(result_df.iloc[i][col]) if not pd.isna(
                result_df.iloc[i][col]) else "" for col in columns]
            self.results_tree.insert("", "end", values=values)

        status_text = f"Query executed - {len(result_df)} results"
        if len(result_df) > max_rows:
            status_text += f" (showing {max_rows})"

        self.status_label.config(text=status_text)

        # Aggiorna SEMPRE la data view principale con i risultati query
        self.update_data_view(result_df, "Query Results")

    def _show_query_error(self, error_msg):
        """Mostra errore query"""
        self.progress.stop()
        self.status_label.config(text="Query failed")
        # Gestione errori speciali per Inbox/Shared Mailbox/delega
        error_keywords = ["inbox", "shared mailbox", "delega"]
        if any(x in error_msg.lower() for x in error_keywords):
            msg = (
                "Errore: la query fa riferimento a una mailbox o delega non "
                "configurata.\n"
                + "Suggerimento: Per accedere a Inbox/Shared Mailbox, "
                + "configura la connessione con delega o credenziali di "
                + "servizio.\n"
                + f"Dettaglio: {error_msg}"
            )
            messagebox.showerror("Query Error", msg)
        elif "ai" in error_msg.lower():
            msg = (
                f"Errore AI: {error_msg}\n"
                "Suggerimento: Verifica la sintassi della query naturale "
                "o riprova con una frase diversa."
            )
            messagebox.showerror("AI Error", msg)
        else:
            msg = f"Error executing query:\n{error_msg}"
            messagebox.showerror("Query Error", msg)

    def update_status(self, message, rows=None, cols=None):
        """Aggiorna status bar"""
        self.status_label.config(text=message)
        if rows is not None:
            self.rows_label.config(text=f"Rows: {rows:,}")
        if cols is not None:
            self.cols_label.config(text=f"Cols: {cols}")

    # ========================================
    # IMPLEMENTAZIONE FUNZIONI COMPLETE
    # ========================================

    def open_ai_query_builder(self):
        """Apre finestra AI Query Builder"""
        ai_window = tk.Toplevel(self.root)
        ai_window.title("🤖 AI Query Builder")
        ai_window.geometry("800x600")
        ai_window.configure(bg="#2d2d2d")

        # Input area
        ttk.Label(ai_window, text="Describe what you want to analyze:",
                  style="NASA.TLabel").pack(pady=10)

        input_text = tk.Text(ai_window, height=4, bg="#3c3c3c", fg="white",
                             font=("Segoe UI", 11))
        input_text.pack(fill="x", padx=20, pady=5)

        # Examples
        examples_frame = ttk.LabelFrame(ai_window, text="💡 Examples")
        examples_frame.pack(fill="x", padx=20, pady=10)

        examples = [
            "mostra solo la colonna 1",
            "conta tutte le righe della tabella",
            "filtra valori maggiori di 100",
            "raggruppa per categoria e conta",
            "trova i primi 10 valori più alti"
        ]

        for example in examples:
            btn = ttk.Button(
                examples_frame,
                text=example,
                command=lambda ex=example: input_text.insert(
                    "end",
                    ex))
            btn.pack(side="left", padx=5, pady=5)

        # Generate button
        def generate_and_execute():
            query_text = input_text.get("1.0", "end-1c").strip()
            if query_text and self.ai_interpreter:
                try:
                    sql = self.ai_interpreter.interpret_query(query_text)
                    self.query_output.delete("1.0", tk.END)
                    self.query_output.insert("1.0", sql)
                    ai_window.destroy()
                    # Auto-execute if data available
                    if self.current_data is not None:
                        self.execute_current_query()
                except Exception as e:
                    messagebox.showerror("AI Error", f"Error: {e}")

        ttk.Button(ai_window, text="🚀 Generate & Execute",
                   command=generate_and_execute).pack(pady=20)

    def open_merge_tool(self):
        """Apre strumento merge dati"""
        if not self.imported_files or len(self.imported_files) < 2:
            messagebox.showwarning(
                "Warning", "Need at least 2 imported files to merge")
            return

        merge_window = tk.Toplevel(self.root)
        merge_window.title("🔗 Data Merge Tool")
        merge_window.geometry("700x500")
        merge_window.configure(bg="#2d2d2d")

        # File selection
        ttk.Label(merge_window, text="Select files to merge:",
                  style="NASA.TLabel").pack(pady=10)

        files_frame = ttk.Frame(merge_window)
        files_frame.pack(fill="x", padx=20)

        file_vars = {}
        for table_name in self.imported_files.keys():
            var = tk.BooleanVar()
            file_vars[table_name] = var
            ttk.Checkbutton(files_frame, text=table_name,
                            variable=var).pack(anchor="w")

        # Merge options
        options_frame = ttk.LabelFrame(merge_window, text="Merge Options")
        options_frame.pack(fill="x", padx=20, pady=10)

        merge_type = tk.StringVar(value="inner")
        for mtype in ["inner", "outer", "left", "right"]:
            ttk.Radiobutton(
                options_frame,
                text=mtype.title(),
                variable=merge_type,
                value=mtype).pack(
                side="left",
                padx=10)

        def perform_merge():
            selected_files = [name for name,
                              var in file_vars.items() if var.get()]
            if len(selected_files) < 2:
                messagebox.showwarning("Warning", "Select at least 2 files")
                return

            try:
                # Simple merge on common columns
                result_df = None
                for i, file_name in enumerate(selected_files):
                    df = self.imported_files[file_name]
                    if result_df is None:
                        result_df = df
                    else:
                        # Find common columns
                        common_cols = list(
                            set(result_df.columns) & set(df.columns))
                        if common_cols:
                            result_df = pd.merge(
                                result_df, df,
                                on=common_cols[0],
                                how=merge_type.get())
                        else:
                            # Concat if no common columns
                            result_df = pd.concat(
                                [result_df, df], ignore_index=True)

                # Update main view
                self.current_data = result_df
                self.update_data_view(result_df, "Merged Data")

                merge_window.destroy()
                messagebox.showinfo(
                    "Success", f"Merged {
                        len(selected_files)} files successfully!")

            except Exception as e:
                messagebox.showerror("Merge Error", f"Error merging data: {e}")

        ttk.Button(merge_window, text="🔗 Perform Merge",
                   command=perform_merge).pack(pady=20)

    def open_advanced_filters(self):
        """Apre filtri avanzati"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        filter_window = tk.Toplevel(self.root)
        filter_window.title("🔍 Advanced Filters")
        filter_window.geometry("600x400")
        filter_window.configure(bg="#2d2d2d")

        # Filter conditions
        conditions_frame = ttk.LabelFrame(
            filter_window, text="Filter Conditions")
        conditions_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.filter_conditions = []

        def add_condition():
            condition_frame = ttk.Frame(conditions_frame)
            condition_frame.pack(fill="x", pady=5)

            # Column selection
            col_var = tk.StringVar()
            col_combo = ttk.Combobox(
                condition_frame, textvariable=col_var, values=list(
                    self.current_data.columns), width=15)
            col_combo.pack(side="left", padx=5)

            # Operator
            op_var = tk.StringVar(value="==")
            op_combo = ttk.Combobox(
                condition_frame,
                textvariable=op_var,
                values=[
                    "==",
                    "!=",
                    ">",
                    "<",
                    ">=",
                    "<=",
                    "contains"],
                width=10)
            op_combo.pack(side="left", padx=5)

            # Value
            val_var = tk.StringVar()
            val_entry = ttk.Entry(
                condition_frame, textvariable=val_var, width=15)
            val_entry.pack(side="left", padx=5)

            # Remove button
            def remove_condition():
                condition_frame.destroy()
                self.filter_conditions.remove((col_var, op_var, val_var))

            ttk.Button(condition_frame, text="❌",
                       command=remove_condition).pack(side="left", padx=5)

            self.filter_conditions.append((col_var, op_var, val_var))

        # Add first condition
        add_condition()

        # Buttons
        buttons_frame = ttk.Frame(filter_window)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(buttons_frame, text="➕ Add Condition",
                   command=add_condition).pack(side="left", padx=5)

        def apply_filters():
            try:
                filtered_df = self.current_data.copy()

                for col_var, op_var, val_var in self.filter_conditions:
                    col = col_var.get()
                    op = op_var.get()
                    val = val_var.get()

                    if col and val:
                        if op == "contains":
                            filtered_df = filtered_df[filtered_df[col].astype(
                                str).str.contains(val, na=False)]
                        elif op == "==":
                            filtered_df = filtered_df[filtered_df[col] == val]
                        elif op == "!=":
                            filtered_df = filtered_df[filtered_df[col] != val]
                        else:
                            # Numeric operations
                            try:
                                val_num = float(val)
                                if op == ">":
                                    filtered_df = filtered_df[
                                        filtered_df[col] > val_num
                                    ]
                                elif op == "<":
                                    filtered_df = filtered_df[
                                        filtered_df[col] < val_num
                                    ]
                                elif op == ">=":
                                    filtered_df = filtered_df[filtered_df[col]
                                                              >= val_num]
                                elif op == "<=":
                                    filtered_df = filtered_df[filtered_df[col]
                                                              <= val_num]
                            except ValueError:
                                continue

                self.filtered_data = filtered_df
                self.update_data_view(filtered_df, "Filtered Data")
                filter_window.destroy()

                messagebox.showinfo(
                    "Success", f"Applied filters. Showing {
                        len(filtered_df)} of {
                        len(
                            self.current_data)} rows")

            except Exception as e:
                messagebox.showerror(
                    "Filter Error", f"Error applying filters: {e}")

        ttk.Button(buttons_frame, text="🔍 Apply Filters",
                   command=apply_filters).pack(side="right", padx=5)

    def open_views_manager(self):
        """Apre gestore viste"""
        views_window = tk.Toplevel(self.root)
        views_window.title("👁️ Views Manager")
        views_window.geometry("500x400")
        views_window.configure(bg="#2d2d2d")

        # Views list
        ttk.Label(views_window, text="Saved Views:",
                  style="NASA.TLabel").pack(pady=10)

        views_listbox = tk.Listbox(
            views_window, bg="#3c3c3c", fg="white", height=10)
        views_listbox.pack(fill="both", expand=True, padx=20, pady=5)

        # Load saved views from database
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, query FROM saved_views "
                    "ORDER BY created_at DESC")
                views = cursor.fetchall()
                for name, query in views:
                    views_listbox.insert(tk.END, f"{name} - {query[:50]}...")
        except Exception as e:
            print(f"Error loading views: {e}")

        # Buttons
        buttons_frame = ttk.Frame(views_window)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        def load_selected_view():
            selection = views_listbox.curselection()
            if selection:
                view_text = views_listbox.get(selection[0])
                view_name = view_text.split(" - ")[0]
                # Load and execute view
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT query FROM saved_views WHERE name = ?",
                            (view_name,))
                        result = cursor.fetchone()
                        if result:
                            self.query_output.delete("1.0", tk.END)
                            self.query_output.insert("1.0", result[0])
                            views_window.destroy()
                            self.execute_current_query()
                except Exception as e:
                    messagebox.showerror("Error", f"Error loading view: {e}")

        ttk.Button(buttons_frame, text="📖 Load View",
                   command=load_selected_view).pack(side="left", padx=5)

        def delete_selected_view():
            selection = views_listbox.curselection()
            if selection:
                view_text = views_listbox.get(selection[0])
                view_name = view_text.split(" - ")[0]
                if messagebox.askyesno(
                        "Confirm", f"Delete view '{view_name}'?"):
                    try:
                        with sqlite3.connect(self.db_path) as conn:
                            cursor = conn.cursor()
                            cursor.execute(
                                "DELETE FROM saved_views WHERE name = ?",
                                (view_name,))
                            conn.commit()
                        views_listbox.delete(selection[0])
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Error deleting view: {e}")

        ttk.Button(buttons_frame, text="🗑️ Delete View",
                   command=delete_selected_view).pack(side="right", padx=5)

    def open_statistics(self):
        """Apre dashboard statistiche"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Statistics Dashboard")
        stats_window.geometry("800x600")
        stats_window.configure(bg="#2d2d2d")

        # Create notebook for different stats
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Basic stats tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="📊 Basic Stats")

        stats_text = tk.Text(basic_frame, bg="#3c3c3c", fg="white",
                             font=("Consolas", 10))
        stats_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Generate basic statistics
        try:
            stats_info = f"Dataset Statistics\n{'=' * 50}\n\n"
            stats_info += f"Total Rows: {len(self.current_data):,}\n"
            stats_info += (
                f"Total Columns: {len(self.current_data.columns)}\n\n"
            )

            # Column types
            stats_info += "Column Types:\n" + "-" * 20 + "\n"
            for col in self.current_data.columns:
                dtype = str(self.current_data[col].dtype)
                null_count = self.current_data[col].isnull().sum()
                stats_info += f"{col}: {dtype} ({null_count} nulls)\n"

            # Numeric columns statistics
            numeric_cols = self.current_data.select_dtypes(
                include=['number']).columns
            if len(numeric_cols) > 0:
                stats_info += (
                    f"\n\nNumeric Statistics:\n{'-' * 30}\n"
                )
                desc = self.current_data[numeric_cols].describe()
                stats_info += desc.to_string()

            stats_text.insert("1.0", stats_info)

        except Exception as e:
            stats_text.insert("1.0", f"Error generating statistics: {e}")

    def open_database_tools(self):
        """Apre strumenti database"""
        db_window = tk.Toplevel(self.root)
        db_window.title("🔧 Database Tools")
        db_window.geometry("600x500")
        db_window.configure(bg="#2d2d2d")

        # Database info
        info_frame = ttk.LabelFrame(db_window, text="Database Information")
        info_frame.pack(fill="x", padx=20, pady=10)

        info_text = tk.Text(info_frame, height=8, bg="#3c3c3c", fg="white",
                            font=("Consolas", 9))
        info_text.pack(fill="x", padx=10, pady=10)

        # Load database info
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get tables
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                db_info = f"Database: {self.db_path}\n"
                db_info += f"Tables: {len(tables)}\n\n"

                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM '{table_name}'")
                    count = cursor.fetchone()[0]
                    db_info += f"• {table_name}: {count:,} rows\n"

                info_text.insert("1.0", db_info)

        except Exception as e:
            info_text.insert("1.0", f"Error loading database info: {e}")

        # Tools buttons
        tools_frame = ttk.LabelFrame(db_window, text="Database Tools")
        tools_frame.pack(fill="x", padx=20, pady=10)

        def backup_database():
            backup_path = filedialog.asksaveasfilename(
                title="Save database backup",
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            if backup_path:
                try:
                    import shutil
                    shutil.copy2(self.db_path, backup_path)
                    messagebox.showinfo(
                        "Success", f"Database backed up to {backup_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Backup failed: {e}")

        def vacuum_database():
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("VACUUM")
                messagebox.showinfo(
                    "Success", "Database optimized successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Optimization failed: {e}")

        ttk.Button(tools_frame, text="💾 Backup Database",
                   command=backup_database).pack(side="left", padx=10, pady=10)
        ttk.Button(tools_frame, text="🔧 Optimize Database",
                   command=vacuum_database).pack(side="left", padx=10, pady=10)

    def quick_ai_query(self):
        """Query AI rapida"""
        if not self.ai_interpreter:
            messagebox.showerror("Error", "AI system not available")
            return

        query = tk.simpledialog.askstring(
            "Quick AI Query",
            "What do you want to analyze?\n\nExamples:\n"
            "• show column 1\n• count all rows\n• filter values > 100"
        )
        if query:
            try:
                sql = self.ai_interpreter.interpret_query(query)
                self.query_output.delete("1.0", tk.END)
                self.query_output.insert("1.0", sql)

                # Auto-execute if data available
                if self.current_data is not None:
                    self.execute_current_query()
                else:
                    messagebox.showinfo(
                        "SQL Generated",
                        "SQL query generated. Import data to execute.")

            except Exception as e:
                messagebox.showerror("AI Error", f"Error: {e}")

    def open_query_templates(self):
        """Apre templates query"""
        templates_window = tk.Toplevel(self.root)
        templates_window.title("📝 Query Templates")
        templates_window.geometry("700x500")
        templates_window.configure(bg="#2d2d2d")

        # Templates list
        ttk.Label(templates_window, text="Available Templates:",
                  style="NASA.TLabel").pack(pady=10)

        templates_tree = ttk.Treeview(templates_window, columns=(
            "Category", "Description"), height=15)
        templates_tree.pack(fill="both", expand=True, padx=20, pady=5)

        templates_tree.heading("#0", text="Template Name")
        templates_tree.heading("Category", text="Category")
        templates_tree.heading("Description", text="Description")

        # Load templates from database
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, category, query, description "
                    "FROM query_templates "
                    "ORDER BY category, name")
                templates = cursor.fetchall()

                for name, category, query, description in templates:
                    templates_tree.insert("", "end", text=name,
                                          values=(category, description))
        except Exception as e:
            print(f"Error loading templates: {e}")

        def load_template():
            selection = templates_tree.selection()
            if selection:
                item = templates_tree.item(selection[0])
                template_name = item['text']

                try:
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT query FROM query_templates WHERE name = ?",
                            (template_name,))
                        result = cursor.fetchone()
                        if result:
                            self.query_output.delete("1.0", tk.END)
                            self.query_output.insert("1.0", result[0])
                            templates_window.destroy()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error loading template: {e}")

        ttk.Button(templates_window, text="📖 Load Template",
                   command=load_template).pack(pady=10)

    def show_smart_suggestions(self):
        """Mostra suggerimenti intelligenti"""
        if self.current_data is None:
            messagebox.showinfo(
                "Smart Suggestions",
                "💡 Import data first to get smart suggestions!"
            )
            return

        suggestions = []

        # Analyze data and generate suggestions
        numeric_cols = self.current_data.select_dtypes(
            include=['number']).columns
        text_cols = self.current_data.select_dtypes(include=['object']).columns

        if len(numeric_cols) > 0:
            suggestions.append(f"📊 Calculate statistics for {numeric_cols[0]}")
            suggestions.append(f"📈 Find top 10 values in {numeric_cols[0]}")

        if len(text_cols) > 0:
            suggestions.append(f"🔍 Show unique values in {text_cols[0]}")
            suggestions.append(f"📊 Group by {text_cols[0]} and count")

        suggestions.append("📋 Show first 20 rows")
        suggestions.append("🔢 Count total rows")

        # Show suggestions dialog
        suggestion_text = "💡 Smart Suggestions for your data:\n\n" + \
            "\n".join(suggestions)
        messagebox.showinfo("Smart Suggestions", suggestion_text)

    def toggle_ai_learning(self):
        """Toggle modalità apprendimento AI"""
        # Placeholder for AI learning mode
        messagebox.showinfo(
            "AI Learning",
            "🧠 AI Learning mode would track and learn from your "
            "query patterns here!"
        )

    def export_current_view(self):
        """Esporta vista corrente"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export current view",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                data_to_export = self.filtered_data \
                    if self.filtered_data is not None \
                    else self.current_data

                if file_path.lower().endswith('.csv'):
                    data_to_export.to_csv(file_path, index=False)
                else:
                    data_to_export.to_excel(file_path, index=False)

                messagebox.showinfo(
                    "Success", f"Data exported successfully to {file_path}")

            except Exception as e:
                messagebox.showerror(
                    "Export Error", f"Error exporting data: {e}")

    def export_query_result(self):
        """Esporta risultato query"""
        if self.current_query_result is None:
            messagebox.showwarning("Warning", "No query results to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export query results",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                if file_path.lower().endswith('.csv'):
                    self.current_query_result.to_csv(file_path, index=False)
                else:
                    self.current_query_result.to_excel(file_path, index=False)

                messagebox.showinfo(
                    "Success", f"Query results exported to {file_path}")

            except Exception as e:
                messagebox.showerror(
                    "Export Error", f"Error exporting results: {e}")

    def reload_current_data(self):
        """Ricarica dati correnti"""
        if hasattr(self, 'current_file_path'):
            self.import_single_file()  # This will show file dialog
        else:
            messagebox.showinfo(
                "Info", "No file to reload. Use Import to load data.")

    def on_file_selected(self, event):
        """Gestisce selezione file"""
        selection = self.files_listbox.curselection()
        if selection:
            filename = self.files_listbox.get(selection[0])
            # Find corresponding data
            for table_name, df in self.imported_files.items():
                if filename.startswith(table_name) or table_name in filename:
                    self.current_data = df
                    self.update_data_view(df)
                    self.update_status(
                        f"Selected: {table_name}", len(df), len(df.columns))
                    break

    def on_view_selected(self, event):
        """Gestisce selezione vista"""
        selection = self.views_listbox.curselection()
        if selection:
            view_name = self.views_listbox.get(selection[0])
            # Load and apply view
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT query FROM saved_views WHERE name LIKE ?",
                        (f"%{view_name}%",
                         ))
                    result = cursor.fetchone()
                    if result:
                        self.query_output.delete("1.0", tk.END)
                        self.query_output.insert("1.0", result[0])
            except Exception as e:
                print(f"Error loading view: {e}")

    def refresh_views_list(self):
        """Aggiorna lista viste"""
        self.views_listbox.delete(0, tk.END)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM saved_views "
                    "ORDER BY last_used DESC, created_at DESC")
                views = cursor.fetchall()
                for (view_name,) in views:
                    self.views_listbox.insert(tk.END, view_name)
        except Exception as e:
            print(f"Error refreshing views: {e}")

    def save_current_view_dialog(self):
        """Dialog per salvare vista corrente"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to save as view")
            return

        view_name = tk.simpledialog.askstring("Save View", "Enter view name:")
        if view_name:
            try:
                # Save current query if available
                current_query = self.query_output.get("1.0", "end-1c").strip()
                if not current_query:
                    current_query = "SELECT * FROM current_data"

                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO saved_views
                        (name, query, last_used)
                        VALUES (?, ?, datetime('now'))
                    """, (view_name, current_query))
                    conn.commit()

                self.refresh_views_list()
                messagebox.showinfo(
                    "Success", f"View '{view_name}' saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving view: {e}")

    def toggle_quick_filter(self):
        """Toggle filtro rapido"""
        if self.quick_filter_frame.winfo_viewable():
            self.quick_filter_frame.pack_forget()
        else:
            children_keys = list(
                self.quick_filter_frame.master.children.keys()
            )
            first_child = children_keys[0] if children_keys else None
            self.quick_filter_frame.pack(
                fill="x", pady=5,
                after=self.quick_filter_frame.master.children[first_child]
            )

    def show_sort_options(self):
        """Mostra opzioni ordinamento"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to sort")
            return

        sort_window = tk.Toplevel(self.root)
        sort_window.title("📈 Sort Options")
        sort_window.geometry("400x300")
        sort_window.configure(bg="#2d2d2d")

        ttk.Label(sort_window, text="Select column to sort by:",
                  style="NASA.TLabel").pack(pady=10)

        col_var = tk.StringVar()
        col_combo = ttk.Combobox(sort_window, textvariable=col_var,
                                 values=list(self.current_data.columns))
        col_combo.pack(pady=10)

        order_var = tk.StringVar(value="ascending")
        ttk.Radiobutton(sort_window, text="Ascending",
                        variable=order_var, value="ascending").pack()
        ttk.Radiobutton(sort_window, text="Descending",
                        variable=order_var, value="descending").pack()

        def apply_sort():
            column = col_var.get()
            if column:
                try:
                    ascending = order_var.get() == "ascending"
                    sorted_df = self.current_data.sort_values(
                        by=column, ascending=ascending)
                    self.update_data_view(sorted_df, f"Sorted by {column}")
                    sort_window.destroy()
                except Exception as e:
                    messagebox.showerror(
                        "Sort Error", f"Error sorting data: {e}")

        ttk.Button(sort_window, text="📈 Apply Sort",
                   command=apply_sort).pack(pady=20)

    def refresh_data_view(self):
        """Aggiorna vista dati"""
        if self.current_data is not None:
            self.update_data_view(self.current_data)
            self.status_label.config(text="Data view refreshed")

    def apply_quick_filter(self):
        """Applica filtro rapido"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to filter")
            return

        column = self.filter_column_var.get()
        operator = self.filter_operator_var.get()
        value = self.filter_value_var.get()

        if not all([column, value]):
            messagebox.showwarning(
                "Warning", "Please select column and enter value")
            return

        try:
            filtered_df = self.current_data.copy()

            if operator == "contains":
                filtered_df = filtered_df[filtered_df[column].astype(
                    str).str.contains(value, na=False)]
            elif operator == "equals":
                filtered_df = filtered_df[filtered_df[column] == value]
            elif operator == "starts with":
                filtered_df = filtered_df[filtered_df[column].astype(
                    str).str.startswith(value, na=False)]
            elif operator == "ends with":
                filtered_df = filtered_df[filtered_df[column].astype(
                    str).str.endswith(value, na=False)]
            else:
                # Numeric operations
                val_num = float(value)
                if operator == ">":
                    filtered_df = filtered_df[filtered_df[column] > val_num]
                elif operator == "<":
                    filtered_df = filtered_df[filtered_df[column] < val_num]
                elif operator == ">=":
                    filtered_df = filtered_df[filtered_df[column] >= val_num]
                elif operator == "<=":
                    filtered_df = filtered_df[filtered_df[column] <= val_num]

            self.filtered_data = filtered_df
            self.update_data_view(filtered_df, "Quick Filtered")
            self.status_label.config(
                text=f"Quick filter applied: {len(filtered_df)} rows")

        except Exception as e:
            messagebox.showerror("Filter Error", f"Error applying filter: {e}")

    def clear_quick_filter(self):
        """Pulisce filtro rapido"""
        self.filter_column_var.set("")
        self.filter_operator_var.set("contains")
        self.filter_value_var.set("")

        if self.current_data is not None:
            self.filtered_data = None
            self.update_data_view(self.current_data)
            self.status_label.config(text="Quick filter cleared")

    def show_ai_suggestions(self):
        """Mostra suggerimenti AI nel pannello"""
        if not self.ai_interpreter:
            messagebox.showinfo("AI Suggestions", "🤖 AI system not available")
            return

        suggestions = [
            "Try: 'show me the first 10 rows'",
            "Try: 'count all records'",
            "Try: 'find unique values in column X'",
            "Try: 'group by category and count'",
            "Try: 'show rows where value > 100'"
        ]

        suggestion_text = "💡 AI Query Suggestions:\n\n" + \
            "\n".join(suggestions)

        # Show in AI input as placeholder
        current_text = self.ai_input.get("1.0", "end-1c").strip()
        if not current_text:
            self.ai_input.insert(
                "1.0", "# " + suggestion_text.replace("\n", "\n# "))

    def load_template_query(self, query):
        """Carica template query"""
        self.query_output.delete("1.0", tk.END)
        self.query_output.insert("1.0", query)

    def on_closing(self):
        """Chiusura applicazione"""
        if messagebox.askokcancel("Quit",
                                  "Do you want to quit NASA ExcelTools?"):
            self.root.destroy()

    def run(self):
        """Avvia applicazione"""
        print("🚀 Starting NASA ExcelTools Unified - Complete Platform")
        self.root.mainloop()


def main():
    """Funzione principale"""
    try:
        app = ExcelToolsUnifiedComplete()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
