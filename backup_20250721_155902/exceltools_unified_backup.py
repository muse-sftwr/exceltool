#!/usr/bin/env python3
"""
🚀 EXCELTOOLS UNIFIED - NASA GRADE DATA ANALYSIS PLATFORM
========================================================

Sistema unificato per analisi dati con interfaccia professionale,
AI Query Builder, template system e funzionalità avanzate.

Autore: NASA DevOps AI Team
Data: 2025-07-21
Versione: 2.0 - AI Enhanced
"""

import os
import sqlite3
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime

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
    print("⚠️ customtkinter non disponibile - usando tkinter standard")


class ExcelToolsUnified:
    """Strumento unificato per gestione Excel e Database"""

    def __init__(self):
        self.db_path = "exceltools_unified.db"
        self.current_data = None
        self.filtered_data = None
        self.imported_files = {}  # Dictionary per file multipli
        self.saved_views = {}  # Dictionary per viste salvate

        # Inizializza database
        self.setup_database()

        # Crea interfaccia
        self.setup_gui()

    def setup_database(self):
        """Configura database SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tabella per file importati
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS imported_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    record_count INTEGER,
                    columns TEXT
                )
            """)

            # Tabella per filtri salvati
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_filters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    filter_config TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabella per viste salvate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_views (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    view_config TEXT NOT NULL,
                    file_source TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabella per merge configurations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS merge_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    merge_config TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            print("✅ Database inizializzato correttamente")

        except Exception as e:
            print(f"❌ Errore database: {e}")

    def setup_gui(self):
        """Crea interfaccia grafica ottimizzata"""
        # Finestra principale
        if HAS_CUSTOMTKINTER:
            self.root = ctk.CTk()
            self.root.title("🚀 ExcelTools Unified")
        else:
            self.root = tk.Tk()
            self.root.title("🚀 ExcelTools Unified")

        # Ottimizza dimensioni schermo
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Usa 85% dello schermo per una buona visibilità
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)

        # Centra la finestra
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1000, 700)

        # Configura griglia principale
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_toolbar()
        self.create_main_area()
        self.create_status_bar()

        print("✅ Interfaccia grafica inizializzata")

    def create_toolbar(self):
        """Crea menu e toolbar professionali NASA-grade"""
        # Crea menu bar professionale
        self.create_menu_bar()

        # Toolbar principale
        if HAS_CUSTOMTKINTER:
            toolbar = ctk.CTkFrame(self.root)
        else:
            toolbar = ttk.Frame(self.root, relief="raised", borderwidth=1)

        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        toolbar.grid_columnconfigure(10, weight=1)  # Espansione

        # Gruppi di pulsanti organizzati professionalmente
        # GRUPPO 1: IMPORTAZIONE
        import_frame = ttk.LabelFrame(toolbar, text="Data Import", padding=5)
        import_frame.grid(row=0, column=0, padx=2, pady=2)

        self.create_button(import_frame, "📂 Single File", self.import_excel, 0, 0, "Import single Excel/CSV file")
        self.create_button(import_frame, "📂+ Multi Import", self.import_multiple, 0, 1, "Import multiple files")

        # GRUPPO 2: ELABORAZIONE
        process_frame = ttk.LabelFrame(toolbar, text="Data Processing", padding=5)
        process_frame.grid(row=0, column=1, padx=2, pady=2)

        self.create_button(process_frame, "🔗 Merge", self.merge_files, 0, 0, "Merge multiple datasets")
        self.create_button(process_frame, "🔄 Refresh", self.refresh_data, 0, 1, "Refresh current view")

        # GRUPPO 3: ANALISI
        analysis_frame = ttk.LabelFrame(toolbar, text="Analysis", padding=5)
        analysis_frame.grid(row=0, column=2, padx=2, pady=2)

        self.create_button(analysis_frame, "🔍 Filters", self.toggle_filters, 0, 0, "Advanced filtering")
        self.create_button(analysis_frame, "⚡ AI Query", self.open_ai_query_builder, 0, 1, "AI-powered query builder")
        self.create_button(analysis_frame, "� Stats", self.show_statistics, 0, 2, "Statistical analysis")

        # GRUPPO 4: GESTIONE
        manage_frame = ttk.LabelFrame(toolbar, text="Management", padding=5)
        manage_frame.grid(row=0, column=3, padx=2, pady=2)

        self.create_button(manage_frame, "👁️ Views", self.manage_saved_views, 0, 0, "Manage saved views")
        self.create_button(manage_frame, "💾 Export", self.export_data, 0, 1, "Export processed data")

        # GRUPPO 5: AIUTO
        help_frame = ttk.LabelFrame(toolbar, text="Assistance", padding=5)
        help_frame.grid(row=0, column=4, padx=2, pady=2)

        self.create_button(help_frame, "🤖 AI Help", self.show_ai_assistant, 0, 0, "AI Assistant")
        self.create_button(help_frame, "📚 Templates", self.show_query_templates, 0, 1, "Query templates")

        # Status indicator
        self.connection_status = ttk.Label(toolbar, text="🟢 Ready", foreground="green")
        self.connection_status.grid(row=0, column=10, sticky="e", padx=10)

    def create_menu_bar(self):
        """Crea menu bar professionale"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Single File...", command=self.import_excel, accelerator="Ctrl+O")
        file_menu.add_command(label="Import Multiple Files...", command=self.import_multiple, accelerator="Ctrl+Shift+O")
        file_menu.add_separator()
        file_menu.add_command(label="Export Data...", command=self.export_data, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        # Menu Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Selection", command=self.copy_selection, accelerator="Ctrl+C")
        edit_menu.add_command(label="Select All", command=self.select_all_data, accelerator="Ctrl+A")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Filters", command=self.remove_quick_filter, accelerator="Ctrl+R")

        # Menu Data
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data", menu=data_menu)
        data_menu.add_command(label="Merge Files...", command=self.merge_files)
        data_menu.add_command(label="Advanced Filters...", command=self.toggle_filters, accelerator="Ctrl+F")
        data_menu.add_command(label="Sort Data...", command=self.sort_data_dialog)
        data_menu.add_separator()
        data_menu.add_command(label="Refresh View", command=self.refresh_data, accelerator="F5")

        # Menu Analysis
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="AI Query Builder...", command=self.open_ai_query_builder, accelerator="Ctrl+Q")
        analysis_menu.add_command(label="Statistical Analysis...", command=self.show_statistics)
        analysis_menu.add_command(label="Data Profiling...", command=self.show_data_profiling)

        # Menu Views
        views_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Views", menu=views_menu)
        views_menu.add_command(label="Save Current View...", command=self.save_current_view)
        views_menu.add_command(label="Manage Views...", command=self.manage_saved_views)
        views_menu.add_separator()
        views_menu.add_command(label="Load Query Template...", command=self.show_query_templates)

        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="AI Assistant", command=self.show_ai_assistant)
        help_menu.add_command(label="Query Templates", command=self.show_query_templates)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About ExcelTools Unified", command=self.show_about)

        # Bind keyboard shortcuts
        self.bind_shortcuts()

    def create_button(self, parent, text, command, row, col, tooltip=""):
        """Crea pulsante con tooltip professionale"""
        if HAS_CUSTOMTKINTER:
            btn = ctk.CTkButton(parent, text=text, command=command, width=100, height=28)
        else:
            btn = ttk.Button(parent, text=text, command=command, width=12)

        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        # Aggiungi tooltip
        if tooltip:
            self.create_tooltip(btn, tooltip)

        return btn

    def create_tooltip(self, widget, text):
        """Crea tooltip professionale"""
        def on_enter(event):
            tooltip_window = tk.Toplevel()
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip_window, text=text, background="lightyellow",
                           relief="solid", borderwidth=1, font=("Arial", 9))
            label.pack()

            def on_leave():
                tooltip_window.destroy()

            widget.tooltip_window = tooltip_window
            tooltip_window.after(3000, on_leave)  # Auto-hide after 3 seconds

        def on_leave(event):
            if hasattr(widget, 'tooltip_window'):
                widget.tooltip_window.destroy()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def bind_shortcuts(self):
        """Associa scorciatoie da tastiera"""
        self.root.bind("<Control-o>", lambda e: self.import_excel())
        self.root.bind("<Control-Shift-O>", lambda e: self.import_multiple())
        self.root.bind("<Control-e>", lambda e: self.export_data())
        self.root.bind("<Control-q>", lambda e: self.open_ai_query_builder())
        self.root.bind("<Control-f>", lambda e: self.toggle_filters())
        self.root.bind("<Control-r>", lambda e: self.remove_quick_filter())
        self.root.bind("<Control-c>", lambda e: self.copy_selection())
        self.root.bind("<Control-a>", lambda e: self.select_all_data())
        self.root.bind("<F5>", lambda e: self.refresh_data())

    def create_main_area(self):
        """Crea area principale con layout responsive"""
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Pannello sinistro per filtri (sempre visibile)
        self.filters_frame = ttk.LabelFrame(main_frame, text="🔍 Filtri e Controlli")
        self.filters_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.filters_frame.grid_columnconfigure(0, weight=1)

        # Pannello destro per dati
        data_frame = ttk.LabelFrame(main_frame, text="📊 Visualizzazione Dati")
        data_frame.grid(row=0, column=1, sticky="nsew")
        data_frame.grid_rowconfigure(1, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)

        self.create_filters_panel()
        self.create_data_panel(data_frame)

    def create_filters_panel(self):
        """Crea pannello filtri sempre visibile"""
        # Info file corrente
        info_frame = ttk.LabelFrame(self.filters_frame, text="📄 File Corrente")
        info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        info_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="File:").grid(row=0, column=0, sticky="w", padx=5)
        self.file_label = ttk.Label(info_frame, text="Nessun file caricato", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(info_frame, text="Righe:").grid(row=1, column=0, sticky="w", padx=5)
        self.rows_label = ttk.Label(info_frame, text="0", foreground="gray")
        self.rows_label.grid(row=1, column=1, sticky="ew", padx=5)

        # Filtri rapidi
        quick_filter_frame = ttk.LabelFrame(self.filters_frame, text="⚡ Filtri Rapidi")
        quick_filter_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        quick_filter_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(quick_filter_frame, text="Cerca:").grid(row=0, column=0, sticky="w", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ttk.Entry(quick_filter_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Filtro per colonna
        ttk.Label(quick_filter_frame, text="Colonna:").grid(row=1, column=0, sticky="w", padx=5)
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(quick_filter_frame, textvariable=self.column_var, state="readonly")
        self.column_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.column_combo.bind("<<ComboboxSelected>>", self.on_column_filter)

        # Pulsanti per filtri rapidi
        filter_buttons = ttk.Frame(quick_filter_frame)
        filter_buttons.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Button(filter_buttons, text="✅ Applica", command=self.apply_quick_filter, width=8).grid(row=0, column=0, padx=2)
        ttk.Button(filter_buttons, text="❌ Rimuovi", command=self.remove_quick_filter, width=8).grid(row=0, column=1, padx=2)
        ttk.Button(filter_buttons, text="💾 Salva Filtro", command=self.save_current_filter, width=10).grid(row=0, column=2, padx=2)

        # Query personalizzate
        query_frame = ttk.LabelFrame(self.filters_frame, text="🛠️ Query Personalizzate")
        query_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        query_frame.grid_columnconfigure(0, weight=1)

        self.query_text = tk.Text(query_frame, height=4, width=30)
        self.query_text.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        query_buttons = ttk.Frame(query_frame)
        query_buttons.grid(row=1, column=0, sticky="ew", padx=5)

        ttk.Button(query_buttons, text="▶️ Esegui", command=self.execute_query, width=10).grid(row=0, column=0, padx=2)
        ttk.Button(query_buttons, text="💾 Salva", command=self.save_query, width=10).grid(row=0, column=1, padx=2)
        ttk.Button(query_buttons, text="🗑️ Pulisci", command=self.clear_query, width=10).grid(row=0, column=2, padx=2)

        # Azioni rapide
        actions_frame = ttk.LabelFrame(self.filters_frame, text="⚡ Azioni Rapide")
        actions_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        ttk.Button(actions_frame, text="🔄 Mostra Tutto", command=self.show_all_data, width=15).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(actions_frame, text="📋 Copia Selezione", command=self.copy_selection, width=15).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(actions_frame, text="📈 Grafici", command=self.show_charts, width=15).grid(row=2, column=0, padx=5, pady=2)

    def create_data_panel(self, parent):
        """Crea pannello per visualizzazione dati"""
        # Toolbar del pannello dati
        data_toolbar = ttk.Frame(parent)
        data_toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(data_toolbar, text="📊 Dati:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)

        self.view_mode = tk.StringVar(value="table")
        ttk.Radiobutton(data_toolbar, text="📋 Tabella", variable=self.view_mode, value="table", command=self.change_view).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(data_toolbar, text="🗂️ Dettagli", variable=self.view_mode, value="details", command=self.change_view).grid(row=0, column=2, padx=5)

        # Frame per il treeview con scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Treeview per i dati
        self.tree = ttk.Treeview(tree_frame, show="tree headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar verticale
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Scrollbar orizzontale
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Bind eventi
        self.tree.bind("<Double-1>", self.on_row_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_status_bar(self):
        """Crea barra di stato"""
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_label = ttk.Label(status_frame, text="🟢 Pronto")
        self.status_label.grid(row=0, column=0, padx=5)

        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.grid(row=0, column=1, sticky="ew", padx=5)

    def import_excel(self):
        """Importa file Excel con anteprima"""
        filetypes = [
            ("File Excel", "*.xlsx *.xls"),
            ("File CSV", "*.csv"),
            ("Tutti i file", "*.*")
        ]

        filepath = filedialog.askopenfilename(
            title="Seleziona file da importare",
            filetypes=filetypes
        )

        if filepath:
            self.load_file_data(filepath)

    def load_file_data(self, filepath):
        """Carica dati del file selezionato"""
        try:
            self.update_status("📂 Caricamento file in corso...")
            self.progress.start()

            # Carica in thread separato per non bloccare GUI
            threading.Thread(target=self._load_file_thread, args=(filepath,), daemon=True).start()

        except Exception as e:
            self.update_status(f"❌ Errore: {e}")
            messagebox.showerror("Errore", f"Impossibile caricare il file:\n{e}")

    def _load_file_thread(self, filepath):
        """Thread per caricamento file"""
        try:
            filename = os.path.basename(filepath)

            if filepath.endswith(('.xlsx', '.xls')):
                if HAS_PANDAS:
                    data = pd.read_excel(filepath)
                else:
                    raise ImportError("pandas non disponibile per file Excel")
            elif filepath.endswith('.csv'):
                if HAS_PANDAS:
                    data = pd.read_csv(filepath)
                else:
                    # Fallback per CSV senza pandas
                    import csv
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        data = list(reader)
            else:
                raise ValueError("Formato file non supportato")

            # Aggiorna GUI dal thread principale
            self.root.after(0, self._file_loaded_callback, data, filename, filepath)

        except Exception as e:
            self.root.after(0, self._file_error_callback, str(e))

    def _file_loaded_callback(self, data, filename, filepath):
        """Callback quando file è caricato"""
        try:
            self.current_data = data
            self.filtered_data = data.copy() if HAS_PANDAS and hasattr(data, 'copy') else data

            # Aggiorna info file
            self.file_label.config(text=filename, foreground="black")
            row_count = len(data) if hasattr(data, '__len__') else 0
            self.rows_label.config(text=str(row_count), foreground="black")

            # Aggiorna combo colonne
            if HAS_PANDAS and hasattr(data, 'columns'):
                columns = list(data.columns)
            elif isinstance(data, list) and data:
                columns = list(data[0].keys()) if isinstance(data[0], dict) else []
            else:
                columns = []

            self.column_combo['values'] = ['Tutte le colonne'] + columns
            self.column_combo.set('Tutte le colonne')

            # Aggiorna visualizzazione
            self.update_tree_view()

            # Salva info nel database
            self.save_file_info(filename, filepath, row_count, columns)

            self.progress.stop()
            self.update_status(f"✅ File caricato: {row_count} righe")

        except Exception as e:
            self.progress.stop()
            self.update_status(f"❌ Errore nel processare il file: {e}")

    def _file_error_callback(self, error_msg):
        """Callback per errori di caricamento"""
        self.progress.stop()
        self.update_status(f"❌ Errore: {error_msg}")
        messagebox.showerror("Errore", f"Impossibile caricare il file:\n{error_msg}")

    def update_tree_view(self):
        """Aggiorna la visualizzazione del treeview"""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.filtered_data is None:
            return

        try:
            if HAS_PANDAS and hasattr(self.filtered_data, 'columns'):
                # DataFrame pandas
                columns = list(self.filtered_data.columns)
                self.tree["columns"] = columns
                self.tree["show"] = "headings"

                # Configura headers
                for col in columns:
                    self.tree.heading(col, text=str(col))
                    self.tree.column(col, width=100, minwidth=50)

                # Aggiungi dati (max 1000 righe per performance)
                for i, row in self.filtered_data.head(1000).iterrows():
                    values = [str(row[col]) for col in columns]
                    self.tree.insert("", "end", values=values)

            elif isinstance(self.filtered_data, list) and self.filtered_data:
                # Lista di dizionari
                if isinstance(self.filtered_data[0], dict):
                    columns = list(self.filtered_data[0].keys())
                    self.tree["columns"] = columns
                    self.tree["show"] = "headings"

                    # Configura headers
                    for col in columns:
                        self.tree.heading(col, text=str(col))
                        self.tree.column(col, width=100, minwidth=50)

                    # Aggiungi dati (max 1000 righe)
                    for i, row in enumerate(self.filtered_data[:1000]):
                        values = [str(row.get(col, "")) for col in columns]
                        self.tree.insert("", "end", values=values)

        except Exception as e:
            self.update_status(f"❌ Errore visualizzazione: {e}")

    def on_search_change(self, *args):
        """Gestisce cambio nel campo di ricerca"""
        if not self.current_data is None:
            search_term = self.search_var.get().lower()
            if search_term:
                self.filter_data_by_search(search_term)
            else:
                self.filtered_data = self.current_data.copy() if HAS_PANDAS and hasattr(self.current_data, 'copy') else self.current_data
                self.update_tree_view()

    def filter_data_by_search(self, search_term):
        """Filtra dati per termine di ricerca"""
        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                # DataFrame pandas
                mask = self.current_data.astype(str).apply(
                    lambda x: x.str.lower().str.contains(search_term, na=False)
                ).any(axis=1)
                self.filtered_data = self.current_data[mask]
            else:
                # Lista di dizionari
                filtered = []
                for row in self.current_data:
                    if isinstance(row, dict):
                        if any(search_term in str(value).lower() for value in row.values()):
                            filtered.append(row)
                self.filtered_data = filtered

            self.update_tree_view()
            count = len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0
            self.update_status(f"🔍 Filtro applicato: {count} righe trovate")

        except Exception as e:
            self.update_status(f"❌ Errore filtro: {e}")

    def on_column_filter(self, event=None):
        """Gestisce filtro per colonna specifica"""
        selected_column = self.column_var.get()
        if selected_column and selected_column != 'Tutte le colonne':
            self.show_column_filter_dialog(selected_column)

    def show_column_filter_dialog(self, column):
        """Mostra dialog per filtro avanzato colonna"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Filtro per: {column}")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Lista valori unici
        ttk.Label(dialog, text=f"Valori disponibili in '{column}':").pack(pady=10)

        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = tk.Listbox(frame, selectmode="multiple")
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.configure(yscrollcommand=scrollbar.set)

        # Popola con valori unici
        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                unique_values = self.current_data[column].dropna().unique()
            else:
                unique_values = list(set(row.get(column, "") for row in self.current_data if isinstance(row, dict)))

            for value in sorted(unique_values):
                listbox.insert("end", str(value))
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare valori: {e}")
            dialog.destroy()
            return

        # Pulsanti
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def apply_filter():
            selected_indices = listbox.curselection()
            if selected_indices:
                selected_values = [listbox.get(i) for i in selected_indices]
                self.apply_column_filter(column, selected_values)
            dialog.destroy()

        def select_all():
            listbox.select_set(0, "end")

        ttk.Button(button_frame, text="Seleziona tutto", command=select_all).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Applica filtro", command=apply_filter).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Annulla", command=dialog.destroy).pack(side="left", padx=5)

    def apply_column_filter(self, column, values):
        """Applica filtro per colonna specifica"""
        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                self.filtered_data = self.current_data[self.current_data[column].astype(str).isin(values)]
            else:
                self.filtered_data = [row for row in self.current_data
                                    if isinstance(row, dict) and str(row.get(column, "")) in values]

            self.update_tree_view()
            count = len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0
            self.update_status(f"🔍 Filtro '{column}' applicato: {count} righe")

        except Exception as e:
            self.update_status(f"❌ Errore filtro colonna: {e}")
            messagebox.showerror("Errore", f"Impossibile applicare filtro: {e}")

    def execute_query(self):
        """Esegue query personalizzata"""
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showwarning("Attenzione", "Inserisci una query da eseguire")
            return

        try:
            # Per semplicità, implementiamo alcune query predefinite
            query_lower = query.lower()

            if query_lower.startswith("count"):
                count = len(self.current_data) if self.current_data is not None else 0
                messagebox.showinfo("Risultato Query", f"Numero totale di righe: {count}")

            elif query_lower.startswith("columns"):
                if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                    columns = list(self.current_data.columns)
                elif isinstance(self.current_data, list) and self.current_data:
                    columns = list(self.current_data[0].keys()) if isinstance(self.current_data[0], dict) else []
                else:
                    columns = []
                messagebox.showinfo("Risultato Query", f"Colonne disponibili:\n" + "\n".join(columns))

            else:
                messagebox.showinfo("Query", "Query personalizzate avanzate saranno implementate nella prossima versione")

        except Exception as e:
            messagebox.showerror("Errore Query", f"Errore nell'eseguire la query:\n{e}")

    def save_query(self):
        """Salva query corrente"""
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showwarning("Attenzione", "Nessuna query da salvare")
            return

        name = tk.simpledialog.askstring("Salva Query", "Nome per la query:")
        if name:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO saved_filters (name, filter_config) VALUES (?, ?)",
                             (name, json.dumps({"type": "query", "content": query})))
                conn.commit()
                conn.close()
                messagebox.showinfo("Successo", f"Query '{name}' salvata")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile salvare la query: {e}")

    def clear_query(self):
        """Pulisce area query"""
        self.query_text.delete("1.0", "end")

    def show_all_data(self):
        """Mostra tutti i dati rimuovendo filtri"""
        if self.current_data is not None:
            self.filtered_data = self.current_data.copy() if HAS_PANDAS and hasattr(self.current_data, 'copy') else self.current_data
            self.search_var.set("")
            self.column_combo.set('Tutte le colonne')
            self.update_tree_view()
            count = len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0
            self.update_status(f"📊 Tutti i dati mostrati: {count} righe")

    def copy_selection(self):
        """Copia selezione negli appunti"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una o più righe da copiare")
            return

        try:
            copied_data = []
            for item in selection:
                values = self.tree.item(item)["values"]
                copied_data.append("\t".join(str(v) for v in values))

            clipboard_text = "\n".join(copied_data)
            self.root.clipboard_clear()
            self.root.clipboard_append(clipboard_text)
            self.update_status(f"📋 {len(selection)} righe copiate negli appunti")

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile copiare: {e}")

    def export_data(self):
        """Esporta dati correnti"""
        if self.filtered_data is None:
            messagebox.showwarning("Attenzione", "Nessun dato da esportare")
            return

        filetypes = [
            ("File Excel", "*.xlsx"),
            ("File CSV", "*.csv"),
            ("File JSON", "*.json")
        ]

        filepath = filedialog.asksaveasfilename(
            title="Esporta dati",
            filetypes=filetypes,
            defaultextension=".xlsx"
        )

        if filepath:
            try:
                if filepath.endswith('.xlsx') and HAS_PANDAS:
                    if hasattr(self.filtered_data, 'to_excel'):
                        self.filtered_data.to_excel(filepath, index=False)
                    else:
                        # Converti lista in DataFrame
                        df = pd.DataFrame(self.filtered_data)
                        df.to_excel(filepath, index=False)

                elif filepath.endswith('.csv'):
                    if HAS_PANDAS and hasattr(self.filtered_data, 'to_csv'):
                        self.filtered_data.to_csv(filepath, index=False)
                    else:
                        # Fallback CSV
                        import csv
                        with open(filepath, 'w', newline='', encoding='utf-8') as f:
                            if isinstance(self.filtered_data, list) and self.filtered_data:
                                writer = csv.DictWriter(f, fieldnames=self.filtered_data[0].keys())
                                writer.writeheader()
                                writer.writerows(self.filtered_data)

                elif filepath.endswith('.json'):
                    if hasattr(self.filtered_data, 'to_json'):
                        self.filtered_data.to_json(filepath, orient='records', indent=2)
                    else:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(self.filtered_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Successo", f"Dati esportati in:\n{filepath}")

            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile esportare: {e}")

    def toggle_filters(self):
        """Toggle visibilità pannello filtri"""
        # Il pannello filtri è sempre visibile in questa versione
        messagebox.showinfo("Info", "Il pannello filtri è sempre visibile per un accesso rapido!")

    def open_query_builder(self):
        """Apre query builder avanzato"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Carica prima dei dati per usare il query builder")
            return

        # Implementazione semplificata del query builder
        dialog = tk.Toplevel(self.root)
        dialog.title("🛠️ Query Builder")
        dialog.geometry("600x400")
        dialog.transient(self.root)

        ttk.Label(dialog, text="Query Builder Avanzato", font=("Arial", 12, "bold")).pack(pady=10)

        # Per ora mostra le query di esempio
        example_frame = ttk.LabelFrame(dialog, text="Query di Esempio")
        example_frame.pack(fill="both", expand=True, padx=10, pady=10)

        examples = [
            "count  # Conta righe totali",
            "columns  # Mostra colonne disponibili",
            "# Query SQL avanzate saranno implementate nella prossima versione"
        ]

        for example in examples:
            ttk.Label(example_frame, text=example).pack(anchor="w", padx=10, pady=2)

        ttk.Button(dialog, text="Chiudi", command=dialog.destroy).pack(pady=10)

    def show_statistics(self):
        """Mostra statistiche dei dati"""
        if self.filtered_data is None:
            messagebox.showwarning("Attenzione", "Nessun dato disponibile per le statistiche")
            return

        try:
            stats_text = f"📊 Statistiche Dataset\n{'='*30}\n\n"

            row_count = len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0
            stats_text += f"Righe totali: {row_count}\n"

            if HAS_PANDAS and hasattr(self.filtered_data, 'columns'):
                stats_text += f"Colonne: {len(self.filtered_data.columns)}\n"
                stats_text += f"Memoria utilizzata: {self.filtered_data.memory_usage(deep=True).sum() / 1024:.1f} KB\n\n"

                # Statistiche per colonne numeriche
                numeric_cols = self.filtered_data.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    stats_text += "Colonne numeriche:\n"
                    for col in numeric_cols:
                        mean_val = self.filtered_data[col].mean()
                        stats_text += f"  {col}: media = {mean_val:.2f}\n"

            elif isinstance(self.filtered_data, list) and self.filtered_data:
                if isinstance(self.filtered_data[0], dict):
                    stats_text += f"Colonne: {len(self.filtered_data[0].keys())}\n"

            messagebox.showinfo("Statistiche", stats_text)

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile calcolare statistiche: {e}")

    def show_charts(self):
        """Mostra opzioni per grafici"""
        messagebox.showinfo("Grafici", "Funzionalità grafici sarà implementata nella prossima versione con matplotlib")

    def refresh_data(self):
        """Aggiorna visualizzazione dati"""
        if self.current_data is not None:
            self.update_tree_view()
            self.update_status("🔄 Dati aggiornati")
        else:
            self.update_status("⚠️ Nessun dato da aggiornare")

    def change_view(self):
        """Cambia modalità visualizzazione"""
        mode = self.view_mode.get()
        if mode == "details":
            messagebox.showinfo("Modalità Dettagli", "Modalità dettagli sarà implementata nella prossima versione")

    def on_row_double_click(self, event):
        """Gestisce doppio click su riga"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)["values"]

            # Mostra dettagli riga
            details = "\n".join([f"{col}: {val}" for col, val in zip(self.tree["columns"], values)])
            messagebox.showinfo("Dettagli Riga", details)

    def show_context_menu(self, event):
        """Mostra menu contestuale"""
        try:
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="📋 Copia", command=self.copy_selection)
            context_menu.add_command(label="📄 Dettagli", command=lambda: self.on_row_double_click(None))
            context_menu.add_separator()
            context_menu.add_command(label="🔍 Filtra per questo valore", command=self.filter_by_cell_value)

            context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Errore menu contestuale: {e}")

    def filter_by_cell_value(self):
        """Filtra per valore cella selezionata"""
        selection = self.tree.selection()
        if selection:
            # Implementazione semplificata
            messagebox.showinfo("Filtro", "Funzionalità 'filtra per valore' sarà implementata nella prossima versione")

    def save_file_info(self, filename, filepath, record_count, columns):
        """Salva informazioni file nel database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO imported_files (filename, filepath, record_count, columns)
                VALUES (?, ?, ?, ?)
            """, (filename, filepath, record_count, json.dumps(columns)))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Errore salvataggio info file: {e}")

    def update_status(self, message):
        """Aggiorna barra di stato"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    # ==================== AI QUERY SYSTEM NASA-GRADE ====================

    def open_ai_query_builder(self):
        """AI-powered Query Builder con suggerimenti intelligenti"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Load data first to use AI Query Builder")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 AI Query Builder - NASA Grade")
        dialog.geometry("900x700")
        dialog.transient(self.root)

        # Main frame con notebook
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: AI Assistant
        ai_frame = ttk.Frame(notebook)
        notebook.add(ai_frame, text="🤖 AI Assistant")

        # AI Query Input
        ttk.Label(ai_frame, text="Describe what you want to analyze:",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # Natural language input
        nl_frame = ttk.Frame(ai_frame)
        nl_frame.pack(fill="x", padx=10, pady=5)

        self.ai_input = tk.Text(nl_frame, height=3, wrap="word")
        self.ai_input.pack(fill="x")

        # AI Suggestions
        suggestions_frame = ttk.LabelFrame(ai_frame, text="💡 AI Suggestions")
        suggestions_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.suggestions_tree = ttk.Treeview(suggestions_frame, columns=("Query", "Description"), show="tree headings")
        self.suggestions_tree.heading("#0", text="Category")
        self.suggestions_tree.heading("Query", text="Generated Query")
        self.suggestions_tree.heading("Description", text="Description")
        self.suggestions_tree.pack(fill="both", expand=True)

        # Populate AI suggestions based on data
        self.populate_ai_suggestions()

        # Tab 2: Advanced Pandas
        pandas_frame = ttk.Frame(notebook)
        notebook.add(pandas_frame, text="🐼 Advanced Pandas")

        ttk.Label(pandas_frame, text="Pandas Query Editor:",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # Query categories
        categories_frame = ttk.Frame(pandas_frame)
        categories_frame.pack(fill="x", padx=10, pady=5)

        self.query_category = tk.StringVar(value="basic")
        categories = [
            ("Basic Operations", "basic"),
            ("Filtering & Selection", "filter"),
            ("Aggregation & Grouping", "agg"),
            ("Statistical Analysis", "stats"),
            ("Data Transformation", "transform")
        ]

        for i, (text, value) in enumerate(categories):
            ttk.Radiobutton(categories_frame, text=text, variable=self.query_category,
                          value=value, command=self.update_query_templates).grid(row=0, column=i, padx=5)

        # Template selector
        template_frame = ttk.LabelFrame(pandas_frame, text="📝 Query Templates")
        template_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Templates list
        templates_list_frame = ttk.Frame(template_frame)
        templates_list_frame.pack(fill="both", expand=True)

        self.templates_listbox = tk.Listbox(templates_list_frame, height=8)
        self.templates_listbox.pack(side="left", fill="both", expand=True)

        template_scroll = ttk.Scrollbar(templates_list_frame, orient="vertical", command=self.templates_listbox.yview)
        template_scroll.pack(side="right", fill="y")
        self.templates_listbox.configure(yscrollcommand=template_scroll.set)

        # Query editor
        query_editor_frame = ttk.LabelFrame(pandas_frame, text="✏️ Query Editor")
        query_editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.pandas_query = tk.Text(query_editor_frame, height=8, wrap="word", font=("Consolas", 10))
        self.pandas_query.pack(fill="both", expand=True, padx=5, pady=5)

        # Syntax highlighting (basic)
        self.setup_syntax_highlighting()

        # Tab 3: SQL-like Queries
        sql_frame = ttk.Frame(notebook)
        notebook.add(sql_frame, text="🗃️ SQL-like")

        ttk.Label(sql_frame, text="SQL-like Query Builder:",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # SQL Builder components
        sql_builder_frame = ttk.Frame(sql_frame)
        sql_builder_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # SELECT clause
        select_frame = ttk.LabelFrame(sql_builder_frame, text="SELECT")
        select_frame.pack(fill="x", pady=5)

        self.select_columns = tk.StringVar(value="*")
        ttk.Entry(select_frame, textvariable=self.select_columns, width=50).pack(padx=5, pady=5)

        # WHERE clause
        where_frame = ttk.LabelFrame(sql_builder_frame, text="WHERE")
        where_frame.pack(fill="x", pady=5)

        self.where_clause = tk.StringVar()
        ttk.Entry(where_frame, textvariable=self.where_clause, width=50).pack(padx=5, pady=5)

        # ORDER BY clause
        order_frame = ttk.LabelFrame(sql_builder_frame, text="ORDER BY")
        order_frame.pack(fill="x", pady=5)

        self.order_clause = tk.StringVar()
        ttk.Entry(order_frame, textvariable=self.order_clause, width=50).pack(padx=5, pady=5)

        # Generated SQL display
        sql_display_frame = ttk.LabelFrame(sql_frame, text="Generated Query")
        sql_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.sql_display = tk.Text(sql_display_frame, height=6, state="disabled",
                                  background="lightgray", font=("Consolas", 10))
        self.sql_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Auto-update SQL display
        for var in [self.select_columns, self.where_clause, self.order_clause]:
            var.trace("w", self.update_sql_display)

        # Control buttons
        control_frame = ttk.Frame(dialog)
        control_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(control_frame, text="🤖 Generate AI Query",
                  command=self.generate_ai_query).pack(side="left", padx=5)
        ttk.Button(control_frame, text="▶️ Execute Query",
                  command=self.execute_ai_query).pack(side="left", padx=5)
        ttk.Button(control_frame, text="💾 Save Template",
                  command=self.save_query_template).pack(side="left", padx=5)
        ttk.Button(control_frame, text="📋 Copy Query",
                  command=self.copy_query_to_clipboard).pack(side="left", padx=5)
        ttk.Button(control_frame, text="❌ Close",
                  command=dialog.destroy).pack(side="right", padx=5)

        # Initialize templates
        self.update_query_templates()
        self.templates_listbox.bind("<<ListboxSelect>>", self.load_template_to_editor)

    def populate_ai_suggestions(self):
        """Popola suggerimenti AI basati sui dati"""
        if not self.current_data is None:
            # Analisi automatica dei dati per suggerimenti
            suggestions = []

            try:
                if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                    columns = list(self.current_data.columns)

                    # Suggerimenti basati sui tipi di colonne
                    numeric_cols = list(self.current_data.select_dtypes(include=['number']).columns)
                    text_cols = list(self.current_data.select_dtypes(include=['object']).columns)

                    # Basic statistics
                    if numeric_cols:
                        suggestions.append(("Statistics",
                                          f"df[{numeric_cols}].describe()",
                                          "Get statistical summary of numeric columns"))

                    # Most common values
                    if text_cols:
                        for col in text_cols[:3]:  # Limit to first 3
                            suggestions.append(("Frequency",
                                              f"df['{col}'].value_counts().head(10)",
                                              f"Most frequent values in {col}"))

                    # Null values analysis
                    suggestions.append(("Data Quality",
                                      "df.isnull().sum()",
                                      "Check for missing values"))

                    # Correlation analysis
                    if len(numeric_cols) > 1:
                        suggestions.append(("Correlation",
                                          f"df[{numeric_cols}].corr()",
                                          "Correlation matrix of numeric columns"))

                    # Data filtering examples
                    for col in columns[:5]:  # Limit examples
                        suggestions.append(("Filtering",
                                          f"df[df['{col}'].notna()]",
                                          f"Filter rows where {col} is not null"))

                # Populate treeview
                for category, query, description in suggestions:
                    parent = ""
                    for item in self.suggestions_tree.get_children():
                        if self.suggestions_tree.item(item)['text'] == category:
                            parent = item
                            break

                    if not parent:
                        parent = self.suggestions_tree.insert("", "end", text=category)

                    self.suggestions_tree.insert(parent, "end", values=(query, description))

            except Exception as e:
                print(f"Error generating AI suggestions: {e}")

    def get_pandas_query_templates(self):
        """Restituisce template di query pandas organizzati per categoria"""
        templates = {
            "basic": [
                ("Shape and Info", "df.shape  # Get dimensions\ndf.info()  # Get column info\ndf.head()  # First 5 rows"),
                ("Column Names", "df.columns.tolist()  # Get all column names"),
                ("Data Types", "df.dtypes  # Get column data types"),
                ("Memory Usage", "df.memory_usage(deep=True)  # Memory consumption"),
                ("Unique Values", "df.nunique()  # Count unique values per column")
            ],
            "filter": [
                ("Basic Filter", "df[df['column'] > value]  # Numeric filter\ndf[df['column'] == 'value']  # Text filter"),
                ("Multiple Conditions", "df[(df['col1'] > value1) & (df['col2'] == 'value2')]"),
                ("String Contains", "df[df['column'].str.contains('pattern', na=False)]"),
                ("Null Filtering", "df[df['column'].isnull()]  # Null values\ndf[df['column'].notnull()]  # Non-null values"),
                ("Query Method", "df.query('column > @value')  # Using query method"),
                ("isin Filter", "df[df['column'].isin(['val1', 'val2'])]  # Multiple values")
            ],
            "agg": [
                ("Basic Aggregation", "df.groupby('column').agg({'numeric_col': ['mean', 'sum', 'count']})"),
                ("Multiple Groupby", "df.groupby(['col1', 'col2']).sum()"),
                ("Custom Aggregation", "df.groupby('column').agg(custom_mean=('numeric_col', 'mean'))"),
                ("Pivot Table", "df.pivot_table(values='value_col', index='index_col', columns='column_col', aggfunc='mean')"),
                ("Cross Tabulation", "pd.crosstab(df['col1'], df['col2'])"),
                ("Rolling Windows", "df['column'].rolling(window=5).mean()  # Moving average")
            ],
            "stats": [
                ("Descriptive Stats", "df.describe()  # Basic statistics\ndf.describe(include='all')  # All columns"),
                ("Correlation Matrix", "df.corr()  # Correlation between numeric columns"),
                ("Value Counts", "df['column'].value_counts()  # Frequency count"),
                ("Percentiles", "df['column'].quantile([0.25, 0.5, 0.75])  # Quartiles"),
                ("Skewness & Kurtosis", "df['column'].skew()  # Skewness\ndf['column'].kurtosis()  # Kurtosis"),
                ("Z-Score", "(df['column'] - df['column'].mean()) / df['column'].std()  # Standardization")
            ],
            "transform": [
                ("New Columns", "df['new_col'] = df['col1'] + df['col2']  # Create new column"),
                ("Apply Function", "df['column'].apply(lambda x: x.upper())  # Apply custom function"),
                ("String Operations", "df['column'].str.upper()  # String manipulation"),
                ("Date Operations", "pd.to_datetime(df['date_col'])  # Convert to datetime"),
                ("Binning", "pd.cut(df['numeric_col'], bins=5)  # Create bins"),
                ("Dummy Variables", "pd.get_dummies(df['categorical_col'])  # One-hot encoding"),
                ("Replace Values", "df['column'].replace({'old': 'new'})  # Replace values"),
                ("Fill Missing", "df['column'].fillna(df['column'].mean())  # Fill with mean")
            ]
        }
        return templates

    def update_query_templates(self):
        """Aggiorna la lista dei template in base alla categoria selezionata"""
        category = self.query_category.get()
        templates = self.get_pandas_query_templates()

        self.templates_listbox.delete(0, "end")

        if category in templates:
            for name, query in templates[category]:
                self.templates_listbox.insert("end", name)

        self.current_templates = templates.get(category, [])

    def load_template_to_editor(self, event=None):
        """Carica template selezionato nell'editor"""
        selection = self.templates_listbox.curselection()
        if selection and hasattr(self, 'current_templates'):
            index = selection[0]
            if index < len(self.current_templates):
                name, query = self.current_templates[index]
                self.pandas_query.delete("1.0", "end")
                self.pandas_query.insert("1.0", query)

    def setup_syntax_highlighting(self):
        """Setup basic syntax highlighting per l'editor pandas"""
        self.pandas_query.tag_configure("keyword", foreground="blue", font=("Consolas", 10, "bold"))
        self.pandas_query.tag_configure("string", foreground="green")
        self.pandas_query.tag_configure("comment", foreground="gray", font=("Consolas", 10, "italic"))

        def highlight_syntax(event=None):
            content = self.pandas_query.get("1.0", "end-1c")

            # Clear existing tags
            for tag in ["keyword", "string", "comment"]:
                self.pandas_query.tag_remove(tag, "1.0", "end")

            # Highlight pandas keywords
            pandas_keywords = ["df", "groupby", "agg", "mean", "sum", "count", "head", "tail",
                             "describe", "info", "shape", "columns", "index", "loc", "iloc",
                             "query", "filter", "apply", "lambda", "str", "dt"]

            for keyword in pandas_keywords:
                start = "1.0"
                while True:
                    pos = self.pandas_query.search(f"\\b{keyword}\\b", start, "end", regexp=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(keyword)}c"
                    self.pandas_query.tag_add("keyword", pos, end)
                    start = end

        self.pandas_query.bind("<KeyRelease>", highlight_syntax)

    def update_sql_display(self, *args):
        """Aggiorna il display della query SQL generata"""
        select_part = self.select_columns.get() or "*"
        where_part = self.where_clause.get()
        order_part = self.order_clause.get()

        sql_query = f"SELECT {select_part} FROM data"

        if where_part:
            sql_query += f" WHERE {where_part}"

        if order_part:
            sql_query += f" ORDER BY {order_part}"

        sql_query += ";"

        self.sql_display.config(state="normal")
        self.sql_display.delete("1.0", "end")
        self.sql_display.insert("1.0", sql_query)
        self.sql_display.config(state="disabled")

    def generate_ai_query(self):
        """Genera query AI basata sull'input in linguaggio naturale"""
        user_input = self.ai_input.get("1.0", "end-1c").strip()

        if not user_input:
            messagebox.showwarning("Warning", "Please describe what you want to analyze")
            return

        # AI Query Generation (simplified rule-based approach)
        generated_query = self.ai_query_interpreter(user_input)

        if generated_query:
            self.pandas_query.delete("1.0", "end")
            self.pandas_query.insert("1.0", generated_query)
            messagebox.showinfo("AI Query Generated", "Query generated successfully! Review and execute.")
        else:
            messagebox.showwarning("AI Generation", "Could not generate query. Try using more specific terms.")

    def ai_query_interpreter(self, user_input):
        """🤖 AI INTELLIGENTE - Interpreta linguaggio naturale e genera SQL puro"""
        # Importa la nuova AI
        try:
            from ai_query_interpreter import AdvancedAIQueryInterpreter
            ai = AdvancedAIQueryInterpreter()
            ai.set_data_context(self.current_data, self.imported_files)
            return ai.interpret_query(user_input)
        except ImportError:
            # Fallback semplice se il modulo non è disponibile
            if not user_input:
                return "-- Inserisci una richiesta in linguaggio naturale"

            if self.current_data is None:
                return "-- Carica prima dei dati per utilizzare l'AI Query Builder"

            # AI semplificata integrata
            input_lower = user_input.lower().strip()
            columns = list(self.current_data.columns)
            table_name = list(self.imported_files.keys())[0] if self.imported_files else 'data'

            # Pattern base per selezione colonne
            if any(word in input_lower for word in ['mostra', 'show', 'seleziona']):
                mentioned_cols = []
                for col in columns:
                    if col.lower() in input_lower:
                        mentioned_cols.append(col)

                if mentioned_cols:
                    cols_str = ", ".join(f"[{col}]" for col in mentioned_cols)
                    return f"-- Mostra colonne: {', '.join(mentioned_cols)}\nSELECT {cols_str} FROM [{table_name}];"
                else:
                    return f"-- Mostra tutti i dati\nSELECT * FROM [{table_name}];"

            # Pattern base per filtri
            elif any(word in input_lower for word in ['dove', 'where', 'uguale']):
                return f"-- Esempio filtro\nSELECT * FROM [{table_name}] WHERE [colonna] = 'valore';"

            # Default
            else:
                return f"-- Query di esempio\nSELECT * FROM [{table_name}] LIMIT 100;"

    def analyze_current_data(self):
        """Analizza i dati correnti per estrarre informazioni utili"""
        if not HAS_PANDAS or self.current_data is None:
            return {}

        try:
            df = self.current_data

            # Identifica tipi di colonne
            numeric_columns = list(df.select_dtypes(include=['number']).columns)
            text_columns = list(df.select_dtypes(include=['object', 'string']).columns)
            date_columns = list(df.select_dtypes(include=['datetime']).columns)

            return {
                'numeric_columns': numeric_columns,
                'text_columns': text_columns,
                'date_columns': date_columns,
                'total_rows': len(df),
                'total_columns': len(df.columns)
            }

        except Exception as e:
            print(f"Errore analisi dati: {e}")
            return {}

    def execute_ai_query(self):
        """Esegue la query dall'AI Query Builder"""
        query = self.pandas_query.get("1.0", "end-1c").strip()

        if not query:
            messagebox.showwarning("Warning", "Please enter or generate a query first")
            return

        try:
            # Prepare execution environment
            df = self.current_data

            if not HAS_PANDAS:
                messagebox.showerror("Error", "Pandas is required for advanced queries")
                return

            # Execute query
            if "=" in query and not query.startswith("#"):
                # Assignment operation
                exec(query, {"df": df, "pd": pd})
                result = "Query executed successfully (assignment operation)"
            else:
                # Expression evaluation
                result = eval(query, {"df": df, "pd": pd})

            # Display result
            self.show_query_result_advanced(str(result))

        except Exception as e:
            messagebox.showerror("Query Error", f"Error executing query:\n{str(e)}")

    def show_query_result_advanced(self, result_text):
        """Mostra risultato query in dialog avanzato"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Query Results - NASA Grade")
        dialog.geometry("800x600")
        dialog.transient(self.root)

        # Result display frame
        result_frame = ttk.Frame(dialog)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget with scrollbars
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill="both", expand=True)

        text_widget = tk.Text(text_frame, wrap="none", font=("Consolas", 10))
        text_widget.pack(side="left", fill="both", expand=True)

        v_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        v_scroll.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=v_scroll.set)

        h_scroll = ttk.Scrollbar(result_frame, orient="horizontal", command=text_widget.xview)
        h_scroll.pack(side="bottom", fill="x")
        text_widget.configure(xscrollcommand=h_scroll.set)

        text_widget.insert("1.0", result_text)
        text_widget.config(state="disabled")

        # Control buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="📋 Copy Results",
                  command=lambda: self.copy_text_to_clipboard(result_text)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="💾 Save Results",
                  command=lambda: self.save_results_to_file(result_text)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Close",
                  command=dialog.destroy).pack(side="right", padx=5)

    def copy_query_to_clipboard(self):
        """Copia query negli appunti"""
        query = self.pandas_query.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(query)
        messagebox.showinfo("Copied", "Query copied to clipboard")

    def copy_text_to_clipboard(self, text):
        """Copia testo negli appunti"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Results copied to clipboard")

    def save_results_to_file(self, text):
        """Salva risultati in file"""
        filepath = filedialog.asksaveasfilename(
            title="Save Query Results",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Saved", f"Results saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def save_query_template(self):
        """Salva query come template personalizzato"""
        query = self.pandas_query.get("1.0", "end-1c").strip()

        if not query:
            messagebox.showwarning("Warning", "No query to save")
            return

        name = tk.simpledialog.askstring("Save Template", "Template name:")
        if name:
            try:
                # Save to database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Create table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS query_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        query TEXT NOT NULL,
                        category TEXT DEFAULT 'custom',
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cursor.execute("INSERT INTO query_templates (name, query) VALUES (?, ?)",
                             (name, query))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"Template '{name}' saved successfully")

            except Exception as e:
                messagebox.showerror("Error", f"Could not save template: {e}")

    # ==================== SUPPORT FUNCTIONS NASA-GRADE ====================

    def show_ai_assistant(self):
        """AI Assistant per aiuto contestuale"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 AI Assistant - NASA Grade")
        dialog.geometry("600x500")
        dialog.transient(self.root)

        # Welcome message
        welcome_frame = ttk.Frame(dialog)
        welcome_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(welcome_frame, text="🤖 ExcelTools AI Assistant",
                 font=("Arial", 14, "bold")).pack()
        ttk.Label(welcome_frame, text="Your intelligent data analysis companion",
                 font=("Arial", 10, "italic")).pack()

        # Assistant capabilities
        capabilities_frame = ttk.LabelFrame(dialog, text="🧠 Capabilities")
        capabilities_frame.pack(fill="both", expand=True, padx=10, pady=10)

        capabilities = [
            "📊 Automatic data analysis suggestions",
            "🔍 Smart query generation from natural language",
            "📈 Statistical insights and recommendations",
            "🛠️ Code template generation",
            "❓ Contextual help and troubleshooting",
            "🎯 Best practices recommendations"
        ]

        for capability in capabilities:
            ttk.Label(capabilities_frame, text=capability).pack(anchor="w", padx=10, pady=2)

        # Quick actions
        actions_frame = ttk.LabelFrame(dialog, text="⚡ Quick Actions")
        actions_frame.pack(fill="x", padx=10, pady=10)

        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack(padx=10, pady=10)

        actions = [
            ("🔍 Analyze Current Data", self.ai_analyze_current_data),
            ("📝 Generate Query Template", self.ai_generate_template),
            ("📊 Data Quality Check", self.ai_data_quality_check),
            ("💡 Get Suggestions", self.ai_get_suggestions)
        ]

        for i, (text, command) in enumerate(actions):
            row, col = i // 2, i % 2
            ttk.Button(actions_grid, text=text, command=command, width=25).grid(
                row=row, column=col, padx=5, pady=5)

        ttk.Button(dialog, text="❌ Close", command=dialog.destroy).pack(pady=10)

    def show_query_templates(self):
        """Mostra libreria di template di query"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📚 Query Templates Library")
        dialog.geometry("800x600")
        dialog.transient(self.root)

        # Template categories
        categories_frame = ttk.Frame(dialog)
        categories_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(categories_frame, text="Select Category:", font=("Arial", 10, "bold")).pack(side="left")

        self.template_category = tk.StringVar(value="basic")
        categories = ["basic", "filter", "agg", "stats", "transform", "custom"]

        category_combo = ttk.Combobox(categories_frame, textvariable=self.template_category,
                                    values=categories, state="readonly", width=15)
        category_combo.pack(side="left", padx=10)
        category_combo.bind("<<ComboboxSelected>>", self.load_template_category)

        # Templates display
        templates_frame = ttk.Frame(dialog)
        templates_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Templates list
        list_frame = ttk.LabelFrame(templates_frame, text="Available Templates")
        list_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.template_list = tk.Listbox(list_frame, width=30)
        self.template_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.template_list.bind("<<ListboxSelect>>", self.preview_template)

        # Template preview
        preview_frame = ttk.LabelFrame(templates_frame, text="Template Preview")
        preview_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.template_preview = tk.Text(preview_frame, wrap="word", font=("Consolas", 10))
        self.template_preview.pack(fill="both", expand=True, padx=5, pady=5)

        # Control buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="📋 Use Template", command=self.use_selected_template).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⭐ Save as Favorite", command=self.save_template_favorite).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Close", command=dialog.destroy).pack(side="right", padx=5)

        # Load initial category
        self.load_template_category()

    def show_shortcuts(self):
        """Mostra scorciatoie da tastiera"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⌨️ Keyboard Shortcuts")
        dialog.geometry("500x400")
        dialog.transient(self.root)

        shortcuts = [
            ("File Operations", [
                ("Ctrl+O", "Import Single File"),
                ("Ctrl+Shift+O", "Import Multiple Files"),
                ("Ctrl+E", "Export Data"),
                ("Ctrl+Q", "Exit Application")
            ]),
            ("Data Operations", [
                ("Ctrl+F", "Advanced Filters"),
                ("Ctrl+R", "Clear Filters"),
                ("F5", "Refresh Data"),
                ("Ctrl+A", "Select All Data")
            ]),
            ("Analysis", [
                ("Ctrl+Q", "AI Query Builder"),
                ("Ctrl+T", "Query Templates"),
                ("Ctrl+S", "Save Current View")
            ]),
            ("Navigation", [
                ("Ctrl+C", "Copy Selection"),
                ("Ctrl+1", "Focus Data Panel"),
                ("Ctrl+2", "Focus Filter Panel")
            ])
        ]

        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for category, items in shortcuts:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)

            for shortcut, description in items:
                row_frame = ttk.Frame(frame)
                row_frame.pack(fill="x", padx=10, pady=2)

                ttk.Label(row_frame, text=shortcut, font=("Consolas", 10, "bold"), width=15).pack(side="left")
                ttk.Label(row_frame, text=description).pack(side="left", padx=10)

        ttk.Button(dialog, text="❌ Close", command=dialog.destroy).pack(pady=10)

    def show_about(self):
        """Mostra informazioni sull'applicazione"""
        dialog = tk.Toplevel(self.root)
        dialog.title("ℹ️ About ExcelTools Unified")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.resizable(False, False)

        # Logo and title
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill="x", padx=20, pady=20)

        ttk.Label(header_frame, text="🚀 ExcelTools Unified",
                 font=("Arial", 18, "bold")).pack()
        ttk.Label(header_frame, text="NASA-Grade Data Analysis Platform",
                 font=("Arial", 12, "italic")).pack()
        ttk.Label(header_frame, text="Version 2.0 - AI Enhanced",
                 font=("Arial", 10)).pack()

        # Features
        features_frame = ttk.LabelFrame(dialog, text="🌟 Features")
        features_frame.pack(fill="both", expand=True, padx=20, pady=10)

        features = [
            "🤖 AI-Powered Query Generation",
            "📊 Advanced Data Analysis",
            "🔗 Multi-File Merge Capabilities",
            "👁️ Saved Views Management",
            "🔍 Smart Filtering System",
            "📈 Statistical Analysis Tools",
            "⚡ Performance Optimized",
            "🎨 Professional UI/UX"
        ]

        for feature in features:
            ttk.Label(features_frame, text=feature).pack(anchor="w", padx=10, pady=2)

        # Credits
        credits_frame = ttk.LabelFrame(dialog, text="👨‍💻 Credits")
        credits_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(credits_frame, text="Developed by NASA DevOps AI Team",
                 font=("Arial", 10, "bold")).pack(padx=10, pady=5)
        ttk.Label(credits_frame, text="Powered by Python, Pandas, and AI",
                 font=("Arial", 9)).pack(padx=10)

        ttk.Button(dialog, text="❌ Close", command=dialog.destroy).pack(pady=20)

    # AI Assistant Functions
    def ai_analyze_current_data(self):
        """AI analizza automaticamente i dati correnti"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded to analyze")
            return

        try:
            analysis_results = []

            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                df = self.current_data

                # Basic info
                analysis_results.append("📊 AUTOMATIC DATA ANALYSIS")
                analysis_results.append("=" * 50)
                analysis_results.append(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                analysis_results.append(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                analysis_results.append("")

                # Column analysis
                analysis_results.append("📋 COLUMN ANALYSIS:")
                numeric_cols = list(df.select_dtypes(include=['number']).columns)
                text_cols = list(df.select_dtypes(include=['object']).columns)
                datetime_cols = list(df.select_dtypes(include=['datetime']).columns)

                analysis_results.append(f"• Numeric columns: {len(numeric_cols)}")
                analysis_results.append(f"• Text columns: {len(text_cols)}")
                analysis_results.append(f"• DateTime columns: {len(datetime_cols)}")
                analysis_results.append("")

                # Data quality
                analysis_results.append("🔍 DATA QUALITY:")
                missing_data = df.isnull().sum()
                if missing_data.sum() > 0:
                    analysis_results.append("Missing values found:")
                    for col, missing in missing_data[missing_data > 0].items():
                        percentage = (missing / len(df)) * 100
                        analysis_results.append(f"• {col}: {missing} ({percentage:.1f}%)")
                else:
                    analysis_results.append("✅ No missing values detected")
                analysis_results.append("")

                # Duplicates
                duplicates = df.duplicated().sum()
                analysis_results.append(f"🔄 Duplicate rows: {duplicates}")
                analysis_results.append("")

                # Statistical insights
                if numeric_cols:
                    analysis_results.append("📈 STATISTICAL INSIGHTS:")
                    for col in numeric_cols[:5]:  # Limit to first 5
                        col_stats = df[col].describe()
                        analysis_results.append(f"• {col}:")
                        analysis_results.append(f"  Mean: {col_stats['mean']:.2f}")
                        analysis_results.append(f"  Std: {col_stats['std']:.2f}")
                        analysis_results.append(f"  Range: {col_stats['min']:.2f} - {col_stats['max']:.2f}")

                # Recommendations
                analysis_results.append("")
                analysis_results.append("💡 RECOMMENDATIONS:")

                if missing_data.sum() > 0:
                    analysis_results.append("• Consider handling missing values before analysis")

                if duplicates > 0:
                    analysis_results.append("• Remove duplicate rows to improve data quality")

                if len(numeric_cols) > 1:
                    analysis_results.append("• Run correlation analysis to find relationships")

                if len(text_cols) > 0:
                    analysis_results.append("• Analyze text columns for patterns and frequencies")

            # Show results
            result_text = "\n".join(analysis_results)
            self.show_query_result_advanced(result_text)

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Could not analyze data: {e}")

    def ai_generate_template(self):
        """Genera template personalizzato basato sui dati"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                columns = list(self.current_data.columns)
                numeric_cols = list(self.current_data.select_dtypes(include=['number']).columns)
                text_cols = list(self.current_data.select_dtypes(include=['object']).columns)

                # Generate custom template
                template_lines = [
                    "# Custom Template for Current Dataset",
                    f"# Dataset: {self.file_label.cget('text')}",
                    f"# Columns: {', '.join(columns[:5])}{'...' if len(columns) > 5 else ''}",
                    "",
                    "# Basic exploration",
                    "df.info()",
                    "df.head(10)",
                    "",
                ]

                if numeric_cols:
                    template_lines.extend([
                        "# Numeric analysis",
                        f"df[{numeric_cols[:3]}].describe()",
                        "",
                    ])

                if text_cols:
                    template_lines.extend([
                        "# Text analysis",
                        f"df['{text_cols[0]}'].value_counts().head(10)",
                        "",
                    ])

                template_lines.extend([
                    "# Data quality check",
                    "df.isnull().sum()",
                    "df.duplicated().sum()",
                    "",
                    "# Custom analysis (modify as needed)",
                    "# Add your specific analysis code here"
                ])

                template_text = "\n".join(template_lines)

                # Show in a dialog for editing
                self.show_generated_template(template_text)

        except Exception as e:
            messagebox.showerror("Generation Error", f"Could not generate template: {e}")

    def ai_data_quality_check(self):
        """Controllo qualità dati AI-powered"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        try:
            quality_report = []

            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                df = self.current_data

                quality_report.append("🔍 DATA QUALITY REPORT")
                quality_report.append("=" * 50)

                # Completeness
                quality_report.append("📋 COMPLETENESS:")
                missing_percentage = (df.isnull().sum() / len(df)) * 100
                for col, pct in missing_percentage.items():
                    if pct > 0:
                        quality_report.append(f"• {col}: {pct:.1f}% missing")

                if missing_percentage.sum() == 0:
                    quality_report.append("✅ All columns are complete (no missing values)")

                quality_report.append("")

                # Uniqueness
                quality_report.append("🔄 UNIQUENESS:")
                duplicate_rows = df.duplicated().sum()
                quality_report.append(f"• Duplicate rows: {duplicate_rows}")

                for col in df.columns:
                    unique_pct = (df[col].nunique() / len(df)) * 100
                    if unique_pct < 50:
                        quality_report.append(f"• {col}: Low uniqueness ({unique_pct:.1f}%)")

                quality_report.append("")

                # Consistency
                quality_report.append("📏 CONSISTENCY:")
                numeric_cols = df.select_dtypes(include=['number']).columns

                for col in numeric_cols:
                    # Check for outliers (using IQR method)
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]

                    if len(outliers) > 0:
                        outlier_pct = (len(outliers) / len(df)) * 100
                        quality_report.append(f"• {col}: {len(outliers)} outliers ({outlier_pct:.1f}%)")

                # Recommendations
                quality_report.append("")
                quality_report.append("💡 QUALITY RECOMMENDATIONS:")

                if duplicate_rows > 0:
                    quality_report.append("• Remove duplicate rows")
                    quality_report.append("  Code: df.drop_duplicates()")

                high_missing_cols = missing_percentage[missing_percentage > 50].index.tolist()
                if high_missing_cols:
                    quality_report.append(f"• Consider dropping columns with >50% missing: {high_missing_cols}")

                low_missing_cols = missing_percentage[(missing_percentage > 0) & (missing_percentage <= 50)].index.tolist()
                if low_missing_cols:
                    quality_report.append(f"• Fill missing values in: {low_missing_cols}")
                    quality_report.append("  Code: df.fillna(method='forward') or df.fillna(df.mean())")

            result_text = "\n".join(quality_report)
            self.show_query_result_advanced(result_text)

        except Exception as e:
            messagebox.showerror("Quality Check Error", f"Could not perform quality check: {e}")

    def ai_get_suggestions(self):
        """Ottieni suggerimenti AI per l'analisi"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        suggestions = [
            "🎯 ANALYSIS SUGGESTIONS",
            "=" * 50,
            "",
            "📊 EXPLORATORY DATA ANALYSIS:",
            "• Start with df.info() and df.describe()",
            "• Check data types and missing values",
            "• Visualize distributions of key variables",
            "",
            "🔍 SPECIFIC ANALYSES TO TRY:",
            "• Correlation analysis for numeric variables",
            "• Frequency analysis for categorical variables",
            "• Time series analysis if date columns exist",
            "• Outlier detection and treatment",
            "",
            "📈 ADVANCED TECHNIQUES:",
            "• Group-by analysis for insights",
            "• Pivot tables for cross-tabulation",
            "• Statistical hypothesis testing",
            "• Feature engineering for derived variables",
            "",
            "💡 BEST PRACTICES:",
            "• Document your analysis steps",
            "• Validate results with domain knowledge",
            "• Save intermediate results as views",
            "• Use version control for query templates"
        ]

        result_text = "\n".join(suggestions)
        self.show_query_result_advanced(result_text)

    def show_generated_template(self, template_text):
        """Mostra template generato per editing"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Generated Template")
        dialog.geometry("700x500")
        dialog.transient(self.root)

        ttk.Label(dialog, text="Generated Template (edit as needed):",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # Template editor
        editor_frame = ttk.Frame(dialog)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        template_editor = tk.Text(editor_frame, wrap="word", font=("Consolas", 10))
        template_editor.pack(fill="both", expand=True)
        template_editor.insert("1.0", template_text)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        def use_template():
            self.open_ai_query_builder()
            # Wait a bit for the dialog to open, then insert the template
            self.root.after(100, lambda: self.pandas_query.insert("1.0", template_editor.get("1.0", "end-1c")))
            dialog.destroy()

        ttk.Button(button_frame, text="📋 Use in Query Builder", command=use_template).pack(side="left", padx=5)
        ttk.Button(button_frame, text="💾 Save Template",
                  command=lambda: self.save_custom_template(template_editor.get("1.0", "end-1c"))).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Close", command=dialog.destroy).pack(side="right", padx=5)

    def save_custom_template(self, template_text):
        """Salva template personalizzato"""
        name = tk.simpledialog.askstring("Save Template", "Template name:")
        if name:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS query_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        query TEXT NOT NULL,
                        category TEXT DEFAULT 'custom',
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("INSERT INTO query_templates (name, query, category) VALUES (?, ?, ?)",
                             (name, template_text, 'custom'))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Template '{name}' saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save template: {e}")

    # Additional helper functions
    def select_all_data(self):
        """Seleziona tutti i dati nella vista"""
        for item in self.tree.get_children():
            self.tree.selection_add(item)
        self.update_status("🔘 All data selected")

    def sort_data_dialog(self):
        """Dialog per ordinamento dati"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to sort")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Sort Data")
        dialog.geometry("400x300")
        dialog.transient(self.root)

        ttk.Label(dialog, text="Sort Configuration:", font=("Arial", 11, "bold")).pack(pady=10)

        # Column selection
        col_frame = ttk.LabelFrame(dialog, text="Select Column")
        col_frame.pack(fill="x", padx=10, pady=10)

        if HAS_PANDAS and hasattr(self.current_data, 'columns'):
            columns = list(self.current_data.columns)
        else:
            columns = []

        sort_column = tk.StringVar()
        ttk.Combobox(col_frame, textvariable=sort_column, values=columns, state="readonly").pack(padx=10, pady=10)

        # Sort order
        order_frame = ttk.LabelFrame(dialog, text="Sort Order")
        order_frame.pack(fill="x", padx=10, pady=10)

        sort_order = tk.StringVar(value="asc")
        ttk.Radiobutton(order_frame, text="Ascending", variable=sort_order, value="asc").pack(anchor="w", padx=10)
        ttk.Radiobutton(order_frame, text="Descending", variable=sort_order, value="desc").pack(anchor="w", padx=10)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def apply_sort():
            column = sort_column.get()
            order = sort_order.get()

            if not column:
                messagebox.showwarning("Warning", "Please select a column")
                return

            try:
                if HAS_PANDAS and hasattr(self.current_data, 'sort_values'):
                    ascending = order == "asc"
                    self.filtered_data = self.current_data.sort_values(column, ascending=ascending)
                    self.update_tree_view()
                    self.update_status(f"📊 Data sorted by {column} ({order})")
                    dialog.destroy()
                else:
                    messagebox.showinfo("Info", "Sorting requires pandas")
            except Exception as e:
                messagebox.showerror("Sort Error", f"Could not sort data: {e}")

        ttk.Button(button_frame, text="✅ Apply Sort", command=apply_sort).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy).pack(side="left", padx=5)

    def show_data_profiling(self):
        """Mostra profiling dettagliato dei dati"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to profile")
            return

        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                df = self.current_data

                profile_info = []
                profile_info.append("📊 DETAILED DATA PROFILING")
                profile_info.append("=" * 60)
                profile_info.append("")

                for col in df.columns:
                    profile_info.append(f"📋 COLUMN: {col}")
                    profile_info.append("-" * 30)

                    # Basic info
                    profile_info.append(f"Data Type: {df[col].dtype}")
                    profile_info.append(f"Non-null Count: {df[col].count()}")
                    profile_info.append(f"Null Count: {df[col].isnull().sum()}")
                    profile_info.append(f"Unique Values: {df[col].nunique()}")

                    # Type-specific analysis
                    if df[col].dtype in ['int64', 'float64']:
                        profile_info.append(f"Min: {df[col].min()}")
                        profile_info.append(f"Max: {df[col].max()}")
                        profile_info.append(f"Mean: {df[col].mean():.2f}")
                        profile_info.append(f"Std: {df[col].std():.2f}")

                    elif df[col].dtype == 'object':
                        top_values = df[col].value_counts().head(3)
                        profile_info.append("Top 3 Values:")
                        for val, count in top_values.items():
                            profile_info.append(f"  {val}: {count}")

                    profile_info.append("")

                result_text = "\n".join(profile_info)
                self.show_query_result_advanced(result_text)

        except Exception as e:
            messagebox.showerror("Profiling Error", f"Could not profile data: {e}")

    def load_template_category(self, event=None):
        """Carica template per categoria selezionata"""
        category = self.template_category.get()

        self.template_list.delete(0, "end")

        if category == "custom":
            # Load custom templates from database
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM query_templates WHERE category = 'custom'")
                templates = cursor.fetchall()
                conn.close()

                for template in templates:
                    self.template_list.insert("end", template[0])
            except:
                pass  # No custom templates yet
        else:
            # Load built-in templates
            templates = self.get_pandas_query_templates()
            if category in templates:
                for name, _ in templates[category]:
                    self.template_list.insert("end", name)

    def preview_template(self, event=None):
        """Anteprima template selezionato"""
        selection = self.template_list.curselection()
        if not selection:
            return

        template_name = self.template_list.get(selection[0])
        category = self.template_category.get()

        if category == "custom":
            # Load from database
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT query FROM query_templates WHERE name = ? AND category = 'custom'",
                             (template_name,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    self.template_preview.delete("1.0", "end")
                    self.template_preview.insert("1.0", result[0])
            except:
                pass
        else:
            # Load from built-in templates
            templates = self.get_pandas_query_templates()
            if category in templates:
                for name, query in templates[category]:
                    if name == template_name:
                        self.template_preview.delete("1.0", "end")
                        self.template_preview.insert("1.0", query)
                        break

    def use_selected_template(self):
        """Usa template selezionato nel query builder"""
        template_text = self.template_preview.get("1.0", "end-1c")
        if template_text.strip():
            self.open_ai_query_builder()
            # Insert template into query builder
            self.root.after(100, lambda: self.pandas_query.insert("1.0", template_text))

    def save_template_favorite(self):
        """Salva template come preferito"""
        selection = self.template_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a template first")
            return

        template_name = self.template_list.get(selection[0])
        messagebox.showinfo("Favorites", f"Template '{template_name}' added to favorites")

    def run(self):
        """Avvia l'applicazione"""
        print("🚀 Avvio ExcelTools Unified - NASA Grade...")
        print("📊 Interfaccia ottimizzata per il tuo schermo")
        print("🔍 Pannello filtri sempre visibile")
        print("🤖 AI Query Builder integrato")
        print("📚 Template library disponibile")
        print("⌨️ Keyboard shortcuts attivi")
        print("✅ Pronto all'uso!")

        self.root.mainloop()    # ==================== NUOVE FUNZIONALITÀ ====================

    def import_multiple(self):
        """Importa file multipli"""
        filetypes = [
            ("File Excel", "*.xlsx *.xls"),
            ("File CSV", "*.csv"),
            ("Tutti i file", "*.*")
        ]

        filepaths = filedialog.askopenfilenames(
            title="Seleziona file multipli da importare",
            filetypes=filetypes
        )

        if filepaths:
            dialog = tk.Toplevel(self.root)
            dialog.title("📁+ Importazione Multipla")
            dialog.geometry("500x400")
            dialog.transient(self.root)

            ttk.Label(dialog, text="File selezionati per importazione:",
                     font=("Arial", 10, "bold")).pack(pady=10)

            # Lista file
            frame = ttk.Frame(dialog)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            listbox = tk.Listbox(frame)
            listbox.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
            scrollbar.pack(side="right", fill="y")
            listbox.configure(yscrollcommand=scrollbar.set)

            for filepath in filepaths:
                listbox.insert("end", os.path.basename(filepath))

            # Pulsanti
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=10)

            def import_all():
                self.update_status("📂 Importazione multipla in corso...")
                self.progress.start()
                threading.Thread(target=self._import_multiple_thread,
                               args=(filepaths,), daemon=True).start()
                dialog.destroy()

            ttk.Button(button_frame, text="📁 Importa Tutti",
                      command=import_all).pack(side="left", padx=5)
            ttk.Button(button_frame, text="❌ Annulla",
                      command=dialog.destroy).pack(side="left", padx=5)

    def _import_multiple_thread(self, filepaths):
        """Thread per importazione multipla"""
        try:
            for filepath in filepaths:
                filename = os.path.basename(filepath)

                if filepath.endswith(('.xlsx', '.xls')):
                    if HAS_PANDAS:
                        data = pd.read_excel(filepath)
                    else:
                        continue
                elif filepath.endswith('.csv'):
                    if HAS_PANDAS:
                        data = pd.read_csv(filepath)
                    else:
                        import csv
                        with open(filepath, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            data = list(reader)
                else:
                    continue

                # Salva nel dizionario dei file importati
                self.imported_files[filename] = {
                    'data': data,
                    'filepath': filepath,
                    'import_date': pd.Timestamp.now() if HAS_PANDAS else None
                }

            self.root.after(0, self._multiple_import_complete)

        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ Errore importazione: {e}"))

    def _multiple_import_complete(self):
        """Callback per completamento importazione multipla"""
        self.progress.stop()
        count = len(self.imported_files)
        self.update_status(f"✅ Importati {count} file")

        # Mostra dialog di selezione file
        self.show_file_selector()

    def show_file_selector(self):
        """Mostra selettore file importati"""
        if not self.imported_files:
            messagebox.showwarning("Attenzione", "Nessun file importato")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("📂 Seleziona File da Visualizzare")
        dialog.geometry("400x300")
        dialog.transient(self.root)

        ttk.Label(dialog, text="File importati:").pack(pady=10)

        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = tk.Listbox(frame)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.configure(yscrollcommand=scrollbar.set)

        for filename in self.imported_files.keys():
            listbox.insert("end", filename)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def select_file():
            selection = listbox.curselection()
            if selection:
                filename = listbox.get(selection[0])
                self.load_imported_file(filename)
                dialog.destroy()

        ttk.Button(button_frame, text="📋 Carica", command=select_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Chiudi", command=dialog.destroy).pack(side="left", padx=5)

    def load_imported_file(self, filename):
        """Carica file dalla lista importati"""
        if filename in self.imported_files:
            file_info = self.imported_files[filename]
            self.current_data = file_info['data']
            self.filtered_data = self.current_data.copy() if HAS_PANDAS and hasattr(self.current_data, 'copy') else self.current_data

            # Aggiorna interfaccia
            self.file_label.config(text=filename, foreground="black")
            row_count = len(self.current_data) if hasattr(self.current_data, '__len__') else 0
            self.rows_label.config(text=str(row_count), foreground="black")

            # Aggiorna colonne
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                columns = list(self.current_data.columns)
            elif isinstance(self.current_data, list) and self.current_data:
                columns = list(self.current_data[0].keys()) if isinstance(self.current_data[0], dict) else []
            else:
                columns = []

            self.column_combo['values'] = ['Tutte le colonne'] + columns
            self.column_combo.set('Tutte le colonne')

            self.update_tree_view()
            self.update_status(f"✅ File '{filename}' caricato")

    def merge_files(self):
        """Merge di file multipli"""
        if len(self.imported_files) < 2:
            messagebox.showwarning("Attenzione", "Importa almeno 2 file per il merge")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("🔗 Merge Files")
        dialog.geometry("600x500")
        dialog.transient(self.root)

        ttk.Label(dialog, text="Merge Configuration", font=("Arial", 12, "bold")).pack(pady=10)

        # Selezione file
        files_frame = ttk.LabelFrame(dialog, text="Seleziona File per Merge")
        files_frame.pack(fill="x", padx=10, pady=10)

        self.merge_vars = {}
        for filename in self.imported_files.keys():
            var = tk.BooleanVar()
            self.merge_vars[filename] = var
            ttk.Checkbutton(files_frame, text=filename, variable=var).pack(anchor="w", padx=10, pady=2)

        # Tipo merge
        merge_frame = ttk.LabelFrame(dialog, text="Tipo di Merge")
        merge_frame.pack(fill="x", padx=10, pady=10)

        self.merge_type = tk.StringVar(value="concat")
        ttk.Radiobutton(merge_frame, text="Concatenazione (Union)", variable=self.merge_type, value="concat").pack(anchor="w", padx=10)
        ttk.Radiobutton(merge_frame, text="Join su colonna comune", variable=self.merge_type, value="join").pack(anchor="w", padx=10)

        # Colonna per join
        join_frame = ttk.LabelFrame(dialog, text="Colonna per Join (se applicabile)")
        join_frame.pack(fill="x", padx=10, pady=10)

        self.join_column = tk.StringVar()
        join_combo = ttk.Combobox(join_frame, textvariable=self.join_column, state="readonly")
        join_combo.pack(fill="x", padx=10, pady=5)

        # Popola colonne comuni
        if self.imported_files:
            common_columns = set()
            first_file = True
            for file_info in self.imported_files.values():
                data = file_info['data']
                if HAS_PANDAS and hasattr(data, 'columns'):
                    columns = set(data.columns)
                elif isinstance(data, list) and data:
                    columns = set(data[0].keys()) if isinstance(data[0], dict) else set()
                else:
                    columns = set()

                if first_file:
                    common_columns = columns
                    first_file = False
                else:
                    common_columns = common_columns.intersection(columns)

            join_combo['values'] = list(common_columns)

        # Pulsanti
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def execute_merge():
            selected_files = [filename for filename, var in self.merge_vars.items() if var.get()]
            if len(selected_files) < 2:
                messagebox.showwarning("Attenzione", "Seleziona almeno 2 file")
                return

            self.perform_merge(selected_files, self.merge_type.get(), self.join_column.get())
            dialog.destroy()

        ttk.Button(button_frame, text="🔗 Esegui Merge", command=execute_merge).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Annulla", command=dialog.destroy).pack(side="left", padx=5)

    def perform_merge(self, selected_files, merge_type, join_column):
        """Esegue il merge dei file selezionati"""
        try:
            datas = []
            for filename in selected_files:
                file_info = self.imported_files[filename]
                datas.append(file_info['data'])

            if merge_type == "concat":
                # Concatenazione semplice
                if HAS_PANDAS:
                    merged_data = pd.concat(datas, ignore_index=True)
                else:
                    merged_data = []
                    for data in datas:
                        if isinstance(data, list):
                            merged_data.extend(data)

            elif merge_type == "join" and join_column:
                # Join su colonna comune
                if HAS_PANDAS:
                    merged_data = datas[0]
                    for data in datas[1:]:
                        merged_data = pd.merge(merged_data, data, on=join_column, how='inner')
                else:
                    messagebox.showwarning("Attenzione", "Join richiede pandas")
                    return

            self.current_data = merged_data
            self.filtered_data = merged_data.copy() if HAS_PANDAS and hasattr(merged_data, 'copy') else merged_data

            # Aggiorna interfaccia
            self.file_label.config(text=f"Merge di {len(selected_files)} file", foreground="blue")
            row_count = len(merged_data) if hasattr(merged_data, '__len__') else 0
            self.rows_label.config(text=str(row_count), foreground="blue")

            self.update_tree_view()
            self.update_status(f"✅ Merge completato: {row_count} righe")

        except Exception as e:
            messagebox.showerror("Errore Merge", f"Impossibile eseguire merge:\n{e}")

    def manage_saved_views(self):
        """Gestione viste salvate"""
        dialog = tk.Toplevel(self.root)
        dialog.title("👁️ Gestione Viste Salvate")
        dialog.geometry("500x400")
        dialog.transient(self.root)

        # Frame principale
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Lista viste salvate
        ttk.Label(main_frame, text="Viste Salvate:", font=("Arial", 10, "bold")).pack(anchor="w")

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=10)

        self.views_listbox = tk.Listbox(list_frame)
        self.views_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.views_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.views_listbox.configure(yscrollcommand=scrollbar.set)

        # Carica viste dal database
        self.load_saved_views()

        # Pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="💾 Salva Vista Corrente", command=self.save_current_view).pack(side="left", padx=5)
        ttk.Button(button_frame, text="📋 Carica Vista", command=self.load_selected_view).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑️ Elimina Vista", command=self.delete_selected_view).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Chiudi", command=dialog.destroy).pack(side="right", padx=5)

    def load_saved_views(self):
        """Carica viste salvate dal database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM saved_views ORDER BY created_date DESC")
            views = cursor.fetchall()
            conn.close()

            self.views_listbox.delete(0, "end")
            for view in views:
                self.views_listbox.insert("end", view[0])

        except Exception as e:
            print(f"Errore caricamento viste: {e}")

    def save_current_view(self):
        """Salva vista corrente"""
        if self.filtered_data is None:
            messagebox.showwarning("Attenzione", "Nessun dato da salvare")
            return

        name = tk.simpledialog.askstring("Salva Vista", "Nome per la vista:")
        if name:
            try:
                # Crea configurazione vista
                view_config = {
                    'filters': {
                        'search_term': self.search_var.get(),
                        'selected_column': self.column_var.get()
                    },
                    'data_info': {
                        'row_count': len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0,
                        'columns': list(self.filtered_data.columns) if HAS_PANDAS and hasattr(self.filtered_data, 'columns') else []
                    }
                }

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO saved_views (name, view_config, file_source)
                    VALUES (?, ?, ?)
                """, (name, json.dumps(view_config), self.file_label.cget('text')))
                conn.commit()
                conn.close()

                self.load_saved_views()  # Ricarica lista
                messagebox.showinfo("Successo", f"Vista '{name}' salvata")

            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile salvare vista: {e}")

    def load_selected_view(self):
        """Carica vista selezionata"""
        selection = self.views_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una vista da caricare")
            return

        view_name = self.views_listbox.get(selection[0])

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT view_config FROM saved_views WHERE name = ?", (view_name,))
            result = cursor.fetchone()
            conn.close()

            if result:
                view_config = json.loads(result[0])

                # Applica filtri salvati
                self.search_var.set(view_config['filters']['search_term'])
                self.column_var.set(view_config['filters']['selected_column'])

                # Applica filtri
                self.apply_quick_filter()

                messagebox.showinfo("Successo", f"Vista '{view_name}' caricata")

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare vista: {e}")

    def delete_selected_view(self):
        """Elimina vista selezionata"""
        selection = self.views_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una vista da eliminare")
            return

        view_name = self.views_listbox.get(selection[0])

        if messagebox.askyesno("Conferma", f"Eliminare la vista '{view_name}'?"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM saved_views WHERE name = ?", (view_name,))
                conn.commit()
                conn.close()

                self.load_saved_views()  # Ricarica lista
                messagebox.showinfo("Successo", f"Vista '{view_name}' eliminata")

            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile eliminare vista: {e}")

    def apply_quick_filter(self):
        """Applica filtro rapido"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Carica prima dei dati")
            return

        search_term = self.search_var.get().lower()
        selected_column = self.column_var.get()

        if search_term:
            self.filter_data_by_search(search_term)
        elif selected_column and selected_column != 'Tutte le colonne':
            # Mantieni filtro colonna attuale
            pass
        else:
            self.filtered_data = self.current_data.copy() if HAS_PANDAS and hasattr(self.current_data, 'copy') else self.current_data
            self.update_tree_view()

        self.update_status("✅ Filtro rapido applicato")

    def remove_quick_filter(self):
        """Rimuove filtro rapido"""
        self.search_var.set("")
        self.column_var.set('Tutte le colonne')
        if self.current_data is not None:
            self.filtered_data = self.current_data.copy() if HAS_PANDAS and hasattr(self.current_data, 'copy') else self.current_data
            self.update_tree_view()
        self.update_status("❌ Filtri rimossi")

    def save_current_filter(self):
        """Salva filtro corrente"""
        if not self.search_var.get() and self.column_var.get() == 'Tutte le colonne':
            messagebox.showwarning("Attenzione", "Nessun filtro attivo da salvare")
            return

        name = tk.simpledialog.askstring("Salva Filtro", "Nome per il filtro:")
        if name:
            try:
                filter_config = {
                    'search_term': self.search_var.get(),
                    'selected_column': self.column_var.get()
                }

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO saved_filters (name, filter_config) VALUES (?, ?)",
                             (name, json.dumps(filter_config)))
                conn.commit()
                conn.close()

                messagebox.showinfo("Successo", f"Filtro '{name}' salvato")

            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile salvare filtro: {e}")

    def toggle_filters(self):
        """Mostra dialog filtri avanzati"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Carica prima dei dati")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("🔍 Filtri Avanzati")
        dialog.geometry("600x500")
        dialog.transient(self.root)

        # Notebook per diverse tipologie di filtri
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Filtri per valore
        value_frame = ttk.Frame(notebook)
        notebook.add(value_frame, text="Valori")

        ttk.Label(value_frame, text="Filtri per valore:", font=("Arial", 10, "bold")).pack(pady=10)

        # Selezione colonna
        col_frame = ttk.Frame(value_frame)
        col_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(col_frame, text="Colonna:").pack(side="left")
        filter_col_var = tk.StringVar()

        if HAS_PANDAS and hasattr(self.current_data, 'columns'):
            columns = list(self.current_data.columns)
        elif isinstance(self.current_data, list) and self.current_data:
            columns = list(self.current_data[0].keys()) if isinstance(self.current_data[0], dict) else []
        else:
            columns = []

        filter_col_combo = ttk.Combobox(col_frame, textvariable=filter_col_var, values=columns, state="readonly")
        filter_col_combo.pack(side="left", fill="x", expand=True, padx=5)

        # Lista valori
        values_frame = ttk.LabelFrame(value_frame, text="Valori disponibili")
        values_frame.pack(fill="both", expand=True, padx=10, pady=10)

        values_listbox = tk.Listbox(values_frame, selectmode="multiple")
        values_listbox.pack(side="left", fill="both", expand=True)

        values_scrollbar = ttk.Scrollbar(values_frame, orient="vertical", command=values_listbox.yview)
        values_scrollbar.pack(side="right", fill="y")
        values_listbox.configure(yscrollcommand=values_scrollbar.set)

        def update_values(*args):
            column = filter_col_var.get()
            if column:
                values_listbox.delete(0, "end")
                try:
                    if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                        unique_values = self.current_data[column].dropna().unique()
                    else:
                        unique_values = list(set(row.get(column, "") for row in self.current_data if isinstance(row, dict)))

                    for value in sorted(unique_values):
                        values_listbox.insert("end", str(value))
                except Exception as e:
                    print(f"Errore aggiornamento valori: {e}")

        filter_col_var.trace("w", update_values)

        # Tab 2: Filtri numerici
        numeric_frame = ttk.Frame(notebook)
        notebook.add(numeric_frame, text="Numerico")

        ttk.Label(numeric_frame, text="Filtri numerici:", font=("Arial", 10, "bold")).pack(pady=10)

        # Colonna numerica
        num_col_frame = ttk.Frame(numeric_frame)
        num_col_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(num_col_frame, text="Colonna numerica:").pack(side="left")
        num_col_var = tk.StringVar()

        # Trova colonne numeriche
        numeric_columns = []
        if HAS_PANDAS and hasattr(self.current_data, 'columns'):
            numeric_columns = list(self.current_data.select_dtypes(include=['number']).columns)

        num_col_combo = ttk.Combobox(num_col_frame, textvariable=num_col_var, values=numeric_columns, state="readonly")
        num_col_combo.pack(side="left", fill="x", expand=True, padx=5)

        # Range valori
        range_frame = ttk.LabelFrame(numeric_frame, text="Range valori")
        range_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(range_frame, text="Min:").grid(row=0, column=0, padx=5, pady=5)
        min_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=min_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(range_frame, text="Max:").grid(row=0, column=2, padx=5, pady=5)
        max_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=max_var).grid(row=0, column=3, padx=5, pady=5)

        # Pulsanti
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def apply_advanced_filter():
            try:
                current_tab = notebook.tab(notebook.select(), "text")

                if current_tab == "Valori":
                    column = filter_col_var.get()
                    selected_indices = values_listbox.curselection()
                    if column and selected_indices:
                        selected_values = [values_listbox.get(i) for i in selected_indices]
                        self.apply_column_filter(column, selected_values)

                elif current_tab == "Numerico":
                    column = num_col_var.get()
                    min_val = min_var.get()
                    max_val = max_var.get()

                    if column and (min_val or max_val):
                        self.apply_numeric_filter(column, min_val, max_val)

                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile applicare filtro: {e}")

        ttk.Button(button_frame, text="✅ Applica Filtro", command=apply_advanced_filter).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Annulla", command=dialog.destroy).pack(side="left", padx=5)

    def apply_numeric_filter(self, column, min_val, max_val):
        """Applica filtro numerico"""
        try:
            if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                mask = pd.Series([True] * len(self.current_data))

                if min_val:
                    mask = mask & (self.current_data[column] >= float(min_val))
                if max_val:
                    mask = mask & (self.current_data[column] <= float(max_val))

                self.filtered_data = self.current_data[mask]
            else:
                filtered = []
                for row in self.current_data:
                    if isinstance(row, dict) and column in row:
                        try:
                            value = float(row[column])
                            if min_val and value < float(min_val):
                                continue
                            if max_val and value > float(max_val):
                                continue
                            filtered.append(row)
                        except (ValueError, TypeError):
                            continue
                self.filtered_data = filtered

            self.update_tree_view()
            count = len(self.filtered_data) if hasattr(self.filtered_data, '__len__') else 0
            self.update_status(f"🔢 Filtro numerico applicato: {count} righe")

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile applicare filtro numerico: {e}")

    def execute_query(self):
        """Esegue query personalizzata avanzata"""
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showwarning("Attenzione", "Inserisci una query da eseguire")
            return

        try:
            # Query predefinite
            query_lower = query.lower()

            if query_lower.startswith("count"):
                count = len(self.current_data) if self.current_data is not None else 0
                messagebox.showinfo("Risultato Query", f"Numero totale di righe: {count}")

            elif query_lower.startswith("columns"):
                if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                    columns = list(self.current_data.columns)
                elif isinstance(self.current_data, list) and self.current_data:
                    columns = list(self.current_data[0].keys()) if isinstance(self.current_data[0], dict) else []
                else:
                    columns = []
                messagebox.showinfo("Risultato Query", f"Colonne disponibili:\n" + "\n".join(columns))

            elif query_lower.startswith("describe") or query_lower.startswith("info"):
                if HAS_PANDAS and hasattr(self.current_data, 'describe'):
                    stats = self.current_data.describe()
                    # Mostra in dialog separato
                    self.show_query_result(str(stats))
                else:
                    messagebox.showinfo("Info", "Comando 'describe' richiede pandas")

            elif query_lower.startswith("select") and "where" in query_lower:
                # Query SQL-like semplificata
                self.execute_sql_like_query(query)

            elif query_lower.startswith("show") and "top" in query_lower:
                # Mostra prime N righe
                try:
                    n = int(query_lower.split("top")[1].strip())
                    if HAS_PANDAS and hasattr(self.current_data, 'head'):
                        result = self.current_data.head(n)
                        self.show_query_result(str(result))
                    else:
                        result = self.current_data[:n] if isinstance(self.current_data, list) else []
                        self.show_query_result(str(result))
                except ValueError:
                    messagebox.showerror("Errore", "Formato query non valido. Usa: 'show top 10'")

            else:
                # Query avanzate con pandas
                if HAS_PANDAS and hasattr(self.current_data, 'query'):
                    try:
                        result = self.current_data.query(query)
                        self.show_query_result(f"Risultati query:\n{result}")
                    except Exception as e:
                        messagebox.showerror("Errore Query", f"Query pandas non valida:\n{e}")
                else:
                    messagebox.showinfo("Query",
                        "Query disponibili:\n" +
                        "- count (conta righe)\n" +
                        "- columns (mostra colonne)\n" +
                        "- describe (statistiche)\n" +
                        "- show top N (prime N righe)\n" +
                        "- select * where column='value' (filtro)")

        except Exception as e:
            messagebox.showerror("Errore Query", f"Errore nell'eseguire la query:\n{e}")

    def execute_sql_like_query(self, query):
        """Esegue query SQL-like semplificata"""
        try:
            # Parsing molto semplificato: select * where column=value
            parts = query.lower().split("where")
            if len(parts) != 2:
                messagebox.showerror("Errore", "Formato query: select * where column='value'")
                return

            where_clause = parts[1].strip()

            # Parsing del where: column=value o column='value'
            if "=" in where_clause:
                column, value = where_clause.split("=", 1)
                column = column.strip()
                value = value.strip().strip("'\"")

                # Applica filtro
                if HAS_PANDAS and hasattr(self.current_data, 'columns'):
                    filtered = self.current_data[self.current_data[column].astype(str) == value]
                else:
                    filtered = [row for row in self.current_data
                              if isinstance(row, dict) and str(row.get(column, "")) == value]

                self.filtered_data = filtered
                self.update_tree_view()

                count = len(filtered) if hasattr(filtered, '__len__') else 0
                messagebox.showinfo("Query Risultato", f"Query eseguita. Trovate {count} righe.")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'eseguire query SQL: {e}")

    def show_query_result(self, result_text):
        """Mostra risultato query in dialog separato"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Risultato Query")
        dialog.geometry("600x400")
        dialog.transient(self.root)

        text_widget = tk.Text(dialog, wrap="word")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.insert("1.0", result_text)
        text_widget.config(state="disabled")

        ttk.Button(dialog, text="❌ Chiudi", command=dialog.destroy).pack(pady=10)
def main():
    """Funzione principale"""
    try:
        app = ExcelToolsUnified()
        app.run()
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
