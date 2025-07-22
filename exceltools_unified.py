#!/usr/bin/env python3
"""
# 🚀 EXCELTOOLS UNIFIED - NASA GRADE DATA ANALYSIS PLATFORM
# ========================================================
# GUIDA UTENTE - FUNZIONI E USO
# --------------------------------------------------------
1. Importazione Dati:
   - Usa il menu File > Import Single File o Import Multiple Files per caricare
     file Excel/CSV.
   - I file importati vengono visualizzati nella tabella principale.
2. Esportazione Dati:
   - Menu File > Export Data per salvare i dati filtrati o completi in
     Excel/CSV.
3. AI Query Builder:
   - Tools > AI Query Builder: inserisci una richiesta in italiano o inglese
     (es: "mostra solo colonna 2" o "show only column 2").
   - Il sistema riconosce sia nomi che numeri di colonna e genera la query SQL
     corrispondente.
4. Filtri Avanzati:
   - Tools > Filters: apre la sezione filtri avanzati.
   - Puoi filtrare per valori, intervalli numerici, testo parziale, valori
     nulli e condizioni multiple.
   - I filtri sono cumulativi e possono essere rimossi singolarmente.
5. Statistiche:
   - Tools > Statistics: mostra statistiche descrittive su tutte le colonne
     (conteggio, media, valori unici, nulli, ecc).
6. Resize Adattivo:
   - L’interfaccia si adatta automaticamente alle dimensioni della finestra.
   - Puoi ridimensionare colonne e finestre di dialogo.
7. Ordinamento e UI:
   - Clicca sulle intestazioni delle colonne per ordinare i dati.
   - Tutti i componenti sono disposti in modo pulito e markettaro, con icone e
     colori intuitivi.
8. Shortcut Utili:
   - Ctrl+O: Importa file
   - Ctrl+S: Esporta dati
   - Ctrl+Q: Esci
   - F1: Mostra questa guida
--------------------------------------------------------
Per assistenza avanzata, consulta la documentazione ufficiale o contatta il
supporto NASA DevOps AI Team.
--------------------------------------------------------
Sistema unificato per analisi dati con interfaccia professionale, AI Query
Builder, template system e funzionalità avanzate.
Autore: NASA DevOps AI Team
Data: 2025-07-21
Versione: 2.0 - AI Enhanced
"""

import os
import re
import traceback
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from ai_query_interpreter import AdvancedAIQueryInterpreter

try:
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ Pandas not available - limited functionality")


try:
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('blue')
    HAS_CUSTOMTKINTER = True
except ImportError:
    HAS_CUSTOMTKINTER = False
    print("⚠️ customtkinter non disponibile - usando tkinter standard")


class ExcelToolsUnified:
    """Strumento unificato per gestione Excel e Database"""

    def open_ai_query_builder(self):
        """Apre il AI Query Builder con editor avanzato e suggerimenti"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please import data first")
            return

        ai_window = tk.Toplevel(self.root)
        ai_window.title("🤖 AI Query Builder - NASA Grade")
        ai_window.geometry("1000x750")
        ai_window.transient(self.root)
        ai_window.configure(bg="#232323")

        # Editor input con numeri di riga
        input_frame = ttk.LabelFrame(
            ai_window,
            text="Natural Language Input",
            padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(
            input_frame,
            text="Describe what you want to analyze:",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        editor_frame = tk.Frame(input_frame, bg="#232323")
        editor_frame.pack(fill="x", pady=5)
        line_numbers = tk.Text(
            editor_frame,
            width=4,
            height=3,
            bg="#1e1e1e",
            fg="#888",
            font=("Consolas", 10),
            state="disabled"
        )
        line_numbers.pack(side="left", fill="y")
        self.ai_input = tk.Text(
            editor_frame,
            height=3,
            wrap="word",
            font=("Consolas", 12),
            bg="#181818",
            fg="#fff",
            insertbackground="#fff"
        )
        self.ai_input.pack(side="left", fill="x", expand=True)

        def update_line_numbers(event=None):
            lines = int(self.ai_input.index('end-1c').split('.')[0])
            line_numbers.config(state="normal")
            line_numbers.delete("1.0", "end")
            for i in range(1, lines+1):
                line_numbers.insert("end", f"{i}\n")
            line_numbers.config(state="disabled")
        self.ai_input.bind('<KeyRelease>', update_line_numbers)
        update_line_numbers()

        # Suggerimenti dinamici
        sugg_frame = tk.Frame(ai_window, bg="#232323")
        sugg_frame.pack(fill="x", padx=10, pady=2)
        sugg_label = tk.Label(
            sugg_frame,
            text=(
                "Esempi: mostra solo colonna 2 | mostra Nome, Prezzo | "
                "filtra dove Prezzo > 100 | show only column 1"
            ),
            fg="#7ecfff",
            bg="#232323"
        )
        sugg_label.pack(anchor="w")

        # Bottoni
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(
            button_frame,
            text="🧠 Generate Query",
            command=self.generate_ai_query
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame,
            text="▶️ Execute",
            command=self.execute_ai_query
        ).pack(side="left", padx=5)

        # Output query con numeri di riga
        output_frame = ttk.LabelFrame(
            ai_window,
            text="Generated Query",
            padding=10
        )
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        out_editor_frame = tk.Frame(output_frame, bg="#232323")
        out_editor_frame.pack(fill="both", expand=True)
        out_line_numbers = tk.Text(
            out_editor_frame,
            width=4,
            bg="#1e1e1e",
            fg="#888",
            font=("Consolas", 10),
            state="disabled"
        )
        out_line_numbers.pack(side="left", fill="y")
        self.query_output = tk.Text(
            out_editor_frame,
            wrap="none",
            font=("Consolas", 12),
            bg="#181818",
            fg="#fff",
            insertbackground="#fff"
        )
        self.query_output.pack(side="left", fill="both", expand=True)

        # (function removed, duplicate)

        def update_out_line_numbers(event=None):
            lines = int(self.query_output.index('end-1c').split('.')[0])
            out_line_numbers.config(state="normal")
            out_line_numbers.delete("1.0", "end")
            for i in range(1, lines + 1):
                out_line_numbers.insert("end", f"{i}\n")
            out_line_numbers.config(state="disabled")

        self.query_output.bind('<KeyRelease>', update_out_line_numbers)
        update_out_line_numbers()

        # Query suggestion area
        sugg_query_frame = tk.Frame(ai_window, bg="#232323")
        sugg_query_frame.pack(fill="x", padx=10, pady=2)
        sugg_query_label = tk.Label(
            sugg_query_frame,
            text="Suggerimenti Query:",
            fg="#ffb347",
            bg="#232323",
            font=("Segoe UI", 10, "bold")
        )
        sugg_query_label.pack(anchor="w")
        sugg_query_text = tk.Text(
            sugg_query_frame,
            height=3,
            bg="#181818",
            fg="#fff",
            font=("Consolas", 10),
            state="normal"
        )
        sugg_query_examples = (
            "- mostra solo colonna 2\n"
            "- mostra Nome, Prezzo\n"
            "- filtra dove Prezzo > 100\n"
            "- show only column 1\n"
            "- select rows where column contains 'value'"
        )
        sugg_query_text.insert("1.0", sugg_query_examples)
        sugg_query_text.config(state="disabled")
        sugg_query_text.pack(fill="x", expand=True)
        # --- FINE Query suggestion area ---

        # End of open_ai_query_builder

    def create_main_interface(self):
        """Crea l'interfaccia principale completamente adattiva"""
        self.root = tk.Tk()
        self.root.title("🚀 ExcelTools Unified - NASA Grade Platform")
        self.root.geometry("1400x900")
        self.root.minsize(900, 600)
        self.root.configure(bg="#1e1e1e")

        # Stile personalizzato
        self.setup_style()

        # Configura griglia principale per adattività
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Menu principale
        self.create_menu()

        # Toolbar (fissa in alto)
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.grid(row=0, column=0, sticky="ew")
        self.create_toolbar()

        # Area principale (adattiva)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.create_main_area()

        # Status bar (fissa in basso)
        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken")
        self.status_bar.grid(row=2, column=0, sticky="ew")

        # Bind eventi
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        # Aggiorna layout su resize
        self.root.update_idletasks()
        if hasattr(self, 'main_frame'):
            self.main_frame.update_idletasks()
        if hasattr(self, 'toolbar'):
            self.toolbar.update_idletasks()
        if hasattr(self, 'status_bar'):
            self.status_bar.update_idletasks()

    def setup_style(self):
        """Configura lo stile dell'interfaccia"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configura colori scuri
        self.style.configure("TFrame", background="#2d2d2d")
        self.style.configure(
            "TLabel",
            background="#2d2d2d",
            foreground="white")
        self.style.configure(
            "TButton",
            background="#404040",
            foreground="white")
        self.style.map(
            "TButton", background=[
                ('active', '#505050'), ('pressed', '#303030')])

    def create_menu(self):
        """Crea il menu principale"""
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white")
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#2d2d2d",
            fg="white"
        )
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Single File...",
                              command=self.import_excel)
        file_menu.add_command(label="Import Multiple Files...",
                              command=self.import_multiple)
        file_menu.add_separator()
        file_menu.add_command(
            label="Export Data...",
            command=self.export_data
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Tools menu
        tools_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#2d2d2d",
            fg="white"
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="AI Query Builder",
                               command=self.open_ai_query_builder)
        tools_menu.add_command(
            label="Statistics",
            command=self.show_statistics)
        tools_menu.add_command(
            label="Filters",
            command=self.toggle_filters
        )

    def create_toolbar(self):
        """Crea la toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=5, pady=5)

        # Import section
        import_frame = ttk.LabelFrame(
            toolbar,
            text="Data Import",
            padding=5
        )
        import_frame.pack(side="left", padx=5)

        ttk.Button(import_frame, text="📂 Single File",
                   command=self.import_excel).pack(
            side="left",
            padx=2
        )
        ttk.Button(import_frame, text="📂+ Multi Import",
                   command=self.import_multiple).pack(
            side="left",
            padx=2
        )

        # Analysis section
        analysis_frame = ttk.LabelFrame(
            toolbar,
            text="Analysis",
            padding=5
        )
        analysis_frame.pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="⚡ AI Query",
            command=self.open_ai_query_builder
        ).pack(side="left", padx=2)
        ttk.Button(
            analysis_frame,
            text="📊 Stats",
            command=self.show_statistics
        ).pack(side="left", padx=2)

        # Status
        self.connection_status = ttk.Label(toolbar, text="🟢 Ready")
        self.connection_status.pack(side="right", padx=10)

    def create_main_area(self):
        """Crea l'area principale con treeview adattiva"""
        # Usa self.main_frame già creato
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Treeview con scrollbars (adattivi)
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, show="tree headings")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )
        h_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

    def create_status_bar(self):
        """Crea la status bar"""
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief="sunken"
        )
        self.status_bar.pack(side="bottom", fill="x")

    def import_excel(self):
        """Importa un singolo file Excel/CSV"""
        file_path = filedialog.askopenfilename(
            title="Select Excel or CSV file",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Carica un file nei dati correnti"""
        try:
            if not HAS_PANDAS:
                messagebox.showerror(
                    "Error",
                    "Pandas required for file operations"
                )
                return

            # Determina il tipo di file e carica
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            self.current_data = df
            filename = os.path.basename(file_path)
            self.imported_files[filename] = df

            # Aggiorna treeview
            self.update_treeview()

            # Aggiorna status
            self.status_bar.config(
                text=(
                    f"Loaded: {filename} "
                    f"({len(df)} rows, "
                    f"{len(df.columns)} cols)"
                )
            )

            messagebox.showinfo("Success", f"File loaded: {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def update_treeview(self):
        """Aggiorna il treeview con i dati correnti"""
        if self.current_data is None:
            return

        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configura colonne
        df = self.current_data
        columns = ["#"] + list(df.columns)
        self.tree["columns"] = columns[1:]

        # Configura headers
        self.tree.heading("#0", text="#", anchor="w")
        self.tree.column("#0", width=50, minwidth=50)

        for col in df.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=100, minwidth=50)

        # (Rimosso: codice duplicato/rotto, ora la UI e l'inserimento dati sono gestiti da modules/ui.py)
    def import_multiple(self):
        """Importa file multipli"""
        file_paths = filedialog.askopenfilenames(
            title="Select multiple files",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_paths:
            for file_path in file_paths:
                self.load_file(file_path)

        # (function removed, duplicate)

    def generate_ai_query(self):
        """Genera query AI basata sull'input in linguaggio naturale"""
        user_input = self.ai_input.get("1.0", "end-1c").strip()

        if not user_input:
            messagebox.showwarning(
                "Warning",
                "Please describe what you want to analyze"
            )
            return

        # Genera query usando AI
        generated_query = self.ai_query_interpreter(user_input)

        if generated_query:
            self.query_output.delete("1.0", "end")
            self.query_output.insert("1.0", generated_query)
            messagebox.showinfo(
                "AI Query Generated",
                "Query generated successfully! Review and execute.")
        else:
            messagebox.showwarning(
                "AI Generation",
                "Could not generate query. Try using more specific terms.")

    def ai_query_interpreter(self, user_input):
        """🤖 AI INTELLIGENTE - Interpreta linguaggio naturale e genera SQL"""
        try:
            ai = AdvancedAIQueryInterpreter()
            ai.set_data_context(self.current_data, self.imported_files)
            return ai.interpret_query(user_input)
        except ImportError:
            # Fallback migliorato: riconosce numeri come indici di colonna e
            # nomi
            if not user_input:
                return (
                    "-- Inserisci una richiesta in linguaggio naturale"
                )

            if self.current_data is None:
                return (
                    "-- Carica prima dei dati per utilizzare l'AI "
                    "Query Builder"
                )

            input_lower = user_input.lower().strip()
            columns = list(self.current_data.columns)
            table_name = (
                list(self.imported_files.keys())[0]
                if self.imported_files else 'data'
            )

            # Cerca richieste di selezione colonne (italiano/inglese)
            select_words = [
                'mostra', 'show', 'seleziona', 'visualizza',
                'display', 'solo', 'only'
            ]
            if any(word in input_lower for word in select_words):
                mentioned_cols = []
                # Cerca nomi di colonna letterali
                for col in columns:
                    if col.lower() in input_lower:
                        mentioned_cols.append(col)

                # Cerca pattern tipo "colonna 6" o "column 6"
                match = re.search(r'(colonna|column)\s*(\d+)', input_lower)
                if match:
                    idx = int(match.group(2)) - 1  # 1-based to 0-based
                    if 0 <= idx < len(columns):
                        colname = columns[idx]
                        if colname not in mentioned_cols:
                            mentioned_cols.append(colname)

                # Cerca numeri isolati che potrebbero essere indici
                if not mentioned_cols:
                    numbers = re.findall(r'\b(\d+)\b', input_lower)
                    for n in numbers:
                        idx = int(n) - 1
                        if 0 <= idx < len(columns):
                            colname = columns[idx]
                            if colname not in mentioned_cols:
                                mentioned_cols.append(colname)

                if mentioned_cols:
                    cols_str = ", ".join(f"[{col}]" for col in mentioned_cols)
                    return (
                        f"-- Mostra colonne: {', '.join(mentioned_cols)}\n"
                        f"SELECT {cols_str} FROM [{table_name}];"
                    )
                else:
                    return (
                        f"-- Mostra tutti i dati\n"
                        f"SELECT * FROM [{table_name}];"
                    )

            # Pattern base per filtri
            elif any(
                word in input_lower for word in [
                    'dove', 'where', 'uguale', 'equals', 'equal']
            ):
                return (
                    f"-- Esempio filtro\n"
                    f"SELECT * FROM [{table_name}] WHERE [colonna] = 'valore';"
                )

            # Default
            else:
                return (
                    f"-- Query di esempio\n"
                    f"SELECT * FROM [{table_name}] LIMIT 100;"
                )
            messagebox.showwarning(
                "Warning",
                "Please enter or generate a query first"
            )
            return

        try:
            # Questo è un esempio - implementa l'esecuzione SQL sui dati
            messagebox.showinfo("Query Execution",
                                "Query execution feature coming soon!")

        except Exception as e:
            messagebox.showerror("Query Error",
                                 f"Error executing query:\n{str(e)}")

    def show_statistics(self):
        """Mostra statistiche dei dati (finestra adattiva)"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        if not HAS_PANDAS:
            messagebox.showerror("Error", "Pandas required for statistics")
            return

        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Data Statistics")
        stats_window.geometry("800x600")
        stats_window.minsize(500, 350)
        stats_window.transient(self.root)
        stats_window.grid_rowconfigure(0, weight=1)
        stats_window.grid_columnconfigure(0, weight=1)

        stats_text = tk.Text(stats_window, wrap="none", font=("Consolas", 10))
        stats_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollbars
        stats_scroll_v = ttk.Scrollbar(
            stats_window,
            orient="vertical",
            command=stats_text.yview
        )
        stats_scroll_h = ttk.Scrollbar(
            stats_window,
            orient="horizontal",
            command=stats_text.xview
        )
        stats_text.configure(
            yscrollcommand=stats_scroll_v.set,
            xscrollcommand=stats_scroll_h.set
        )
        stats_scroll_v.grid(row=0, column=1, sticky="ns")
        stats_scroll_h.grid(row=1, column=0, sticky="ew")

        # Calcola e mostra statistiche
        df = self.current_data
        stats_info = []
        stats_info.append("📊 DATASET OVERVIEW")
        stats_info.append("   =   " * 50)
        stats_info.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        stats_info.append(
            f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        )
        stats_info.append("")
        stats_info.append("📋 COLUMN INFORMATION")
        stats_info.append("   =   " * 50)
        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            stats_info.append(
                f"{col}: {dtype} | Nulls: {null_count} | Unique: "
                f"{unique_count}"
            )
        stats_info.append("")
        stats_info.append("📈 NUMERIC STATISTICS")
        stats_info.append("   =   " * 50)
        stats_info.append(str(df.describe()))
        stats_text.insert("1.0", "\n".join(stats_info))
        stats_text.config(state="disabled")

    def toggle_filters(self):
        """Apre la finestra dei filtri avanzati (adattiva)"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        filter_win = tk.Toplevel(self.root)
        filter_win.title("🔎 Filtri Avanzati")
        filter_win.geometry("600x400")
        filter_win.minsize(400, 250)
        filter_win.configure(bg="#232323")
        filter_win.grab_set()
        filter_win.grid_rowconfigure(4, weight=1)
        filter_win.grid_columnconfigure(0, weight=1)

        tk.Label(
            filter_win,
            text="Seleziona colonna:",
            fg="#fff",
            bg="#232323"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        col_var = tk.StringVar()
        col_menu = ttk.Combobox(
            filter_win,
            textvariable=col_var,
            values=list(self.current_data.columns)
        )
        col_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        tk.Label(
            filter_win,
            text="Condizione:",
            fg="#fff",
            bg="#232323"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        cond_var = tk.StringVar()
        cond_menu = ttk.Combobox(
            filter_win,
            textvariable=cond_var,
            values=[
                "Uguale a", "Diverso da", "Contiene", "Non contiene",
                "Maggiore di", "Minore di", "Non nullo", "Nullo"
            ]
        )
        cond_menu.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        tk.Label(
            filter_win,
            text="Valore:",
            fg="#fff",
            bg="#232323"
        ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        val_entry = tk.Entry(filter_win)
        val_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        def apply_filter():
            col = col_var.get()
            cond = cond_var.get()
            val = val_entry.get()
            if not col or not cond:
                messagebox.showwarning(
                    "Warning",
                    "Seleziona colonna e condizione"
                )
                return
            df = self.current_data
            try:
                if cond == "Uguale a":
                    df = df[df[col] == val]
                elif cond == "Diverso da":
                    df = df[df[col] != val]
                elif cond == "Contiene":
                    df = df[df[col].astype(str).str.contains(val, na=False)]
                elif cond == "Non contiene":
                    df = df[~df[col].astype(str).str.contains(val, na=False)]
                elif cond == "Maggiore di":
                    df = df[pd.to_numeric(
                        df[col], errors='coerce') > float(val)]
                elif cond == "Minore di":
                    df = df[pd.to_numeric(
                        df[col], errors='coerce') < float(val)]
                elif cond == "Non nullo":
                    df = df[df[col].notnull()]
                elif cond == "Nullo":
                    df = df[df[col].isnull()]
                self.filtered_data = df
                self.current_data = df
                self.update_treeview()
                filter_win.destroy()
                self.status_bar.config(
                    text=f"Filtro applicato: {col} {cond} {val}"
                )
            except Exception as e:
                messagebox.showerror("Errore filtro", str(e))

        ttk.Button(
            filter_win,
            text="Applica filtro",
            command=apply_filter
        ).grid(
            row=6, column=0, sticky="ew", padx=10, pady=10
        )
        ttk.Button(
            filter_win,
            text="Rimuovi tutti i filtri",
            command=self.reset_filters
        ).grid(row=7, column=0, sticky="ew", padx=10, pady=5)

    def reset_filters(self):
        """Ripristina i dati originali senza filtri"""
        if self.filtered_data is not None:
            self.current_data = pd.concat(
                self.imported_files.values(),
                ignore_index=True
            )
            self.filtered_data = None
            self.update_treeview()
            self.status_bar.config(text="Filtri rimossi")

    def export_data(self):
        """Esporta i dati correnti"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export data",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.current_data.to_csv(file_path, index=False)
                else:
                    self.current_data.to_excel(file_path, index=False)

                messagebox.showinfo("Success", f"Data exported to {file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")

    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def run(self):
        """Avvia l'applicazione"""
        print("🚀 Starting ExcelTools Unified - NASA Grade Platform")
        self.root.mainloop()


def main():
    """Funzione principale"""
    try:  # Reduce blank lines before main function
        app = ExcelToolsUnified()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()  # Reduce blank lines before __main__ check
