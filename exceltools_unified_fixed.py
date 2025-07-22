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
    print("⚠️ customtkinter non disponibile - usando tkinter standard")


class ExcelToolsUnified:
    """Strumento unificato per gestione Excel e Database"""

    def __init__(self):
        self.db_path = "exceltools_unified.db"
        self.current_data = None
        self.filtered_data = None
        self.imported_files = {}
        self.saved_views = {}

        # Inizializza database
        self.init_database()

        # Crea interfaccia principale
        self.create_main_interface()

    def init_database(self):
        """Inizializza il database SQLite"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabella per template query
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS query_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        query TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Tabella per viste salvate
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS saved_views (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        filters JSON,
                        columns JSON,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                conn.commit()
                print("✅ Database inizializzato correttamente")

        except Exception as e:
            print(f"❌ Errore inizializzazione database: {e}")

    def create_main_interface(self):
        """Crea l'interfaccia principale"""
        self.root = tk.Tk()
        self.root.title("🚀 ExcelTools Unified - NASA Grade Platform")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        # Stile personalizzato
        self.setup_style()

        # Menu principale
        self.create_menu()

        # Toolbar
        self.create_toolbar()

        # Area principale
        self.create_main_area()

        # Status bar
        self.create_status_bar()

        # Bind eventi
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_style(self):
        """Configura lo stile dell'interfaccia"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configura colori scuri
        self.style.configure("TFrame", background="#2d2d2d")
        self.style.configure("TLabel", background="#2d2d2d", foreground="white")
        self.style.configure("TButton", background="#404040", foreground="white")
        self.style.map("TButton",
                      background=[('active', '#505050'), ('pressed', '#303030')])

    def create_menu(self):
        """Crea il menu principale"""
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white")
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Single File...",
                             command=self.import_excel)
        file_menu.add_command(label="Import Multiple Files...",
                             command=self.import_multiple)
        file_menu.add_separator()
        file_menu.add_command(label="Export Data...", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white")
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="AI Query Builder",
                              command=self.open_ai_query_builder)
        tools_menu.add_command(label="Statistics", command=self.show_statistics)
        tools_menu.add_command(label="Filters", command=self.toggle_filters)

    def create_toolbar(self):
        """Crea la toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=5, pady=5)

        # Import section
        import_frame = ttk.LabelFrame(toolbar, text="Data Import", padding=5)
        import_frame.pack(side="left", padx=5)

        ttk.Button(import_frame, text="📂 Single File",
                  command=self.import_excel).pack(side="left", padx=2)
        ttk.Button(import_frame, text="📂+ Multi Import",
                  command=self.import_multiple).pack(side="left", padx=2)

        # Analysis section
        analysis_frame = ttk.LabelFrame(toolbar, text="Analysis", padding=5)
        analysis_frame.pack(side="left", padx=5)

        ttk.Button(analysis_frame, text="⚡ AI Query",
                  command=self.open_ai_query_builder).pack(side="left", padx=2)
        ttk.Button(analysis_frame, text="📊 Stats",
                  command=self.show_statistics).pack(side="left", padx=2)

        # Status
        self.connection_status = ttk.Label(toolbar, text="🟢 Ready")
        self.connection_status.pack(side="right", padx=10)

    def create_main_area(self):
        """Crea l'area principale con treeview"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview con scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, show="tree headings")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                   command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal",
                                   command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)

        # Pack treeview e scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

    def create_status_bar(self):
        """Crea la status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken")
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
                messagebox.showerror("Error",
                                   "Pandas required for file operations")
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
                text=f"Loaded: {filename} ({len(df)} rows, {len(df.columns)} cols)"
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

        # Inserisci dati (limite 1000 righe per performance)
        max_rows = min(1000, len(df))
        for i in range(max_rows):
            row_data = [str(df.iloc[i, j]) for j in range(len(df.columns))]
            self.tree.insert("", "end", text=str(i+1), values=row_data)

        if len(df) > max_rows:
            self.tree.insert("", "end", text="...",
                           values=["..." for _ in df.columns])

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

    def open_ai_query_builder(self):
        """Apre il AI Query Builder"""
        if self.current_data is None:
            messagebox.showwarning("Warning",
                                 "Please import data first")
            return

        # Crea finestra AI Query Builder
        ai_window = tk.Toplevel(self.root)
        ai_window.title("🤖 AI Query Builder - NASA Grade")
        ai_window.geometry("900x700")
        ai_window.transient(self.root)

        # Input per linguaggio naturale
        input_frame = ttk.LabelFrame(ai_window, text="Natural Language Input",
                                   padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame,
                 text="Describe what you want to analyze:").pack(anchor="w")

        self.ai_input = tk.Text(input_frame, height=3, wrap="word")
        self.ai_input.pack(fill="x", pady=5)

        # Bottoni
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=5)

        ttk.Button(button_frame, text="🧠 Generate Query",
                  command=self.generate_ai_query).pack(side="left", padx=5)
        ttk.Button(button_frame, text="▶️ Execute",
                  command=self.execute_ai_query).pack(side="left", padx=5)

        # Output query
        output_frame = ttk.LabelFrame(ai_window, text="Generated Query",
                                    padding=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.query_output = tk.Text(output_frame, wrap="none",
                                   font=("Consolas", 10))

        # Scrollbars per output
        output_scroll_v = ttk.Scrollbar(output_frame, orient="vertical",
                                      command=self.query_output.yview)
        output_scroll_h = ttk.Scrollbar(output_frame, orient="horizontal",
                                      command=self.query_output.xview)

        self.query_output.configure(yscrollcommand=output_scroll_v.set,
                                   xscrollcommand=output_scroll_h.set)

        self.query_output.pack(side="left", fill="both", expand=True)
        output_scroll_v.pack(side="right", fill="y")
        output_scroll_h.pack(side="bottom", fill="x")

    def generate_ai_query(self):
        """Genera query AI basata sull'input in linguaggio naturale"""
        user_input = self.ai_input.get("1.0", "end-1c").strip()

        if not user_input:
            messagebox.showwarning("Warning",
                                 "Please describe what you want to analyze")
            return

        # Genera query usando AI
        generated_query = self.ai_query_interpreter(user_input)

        if generated_query:
            self.query_output.delete("1.0", "end")
            self.query_output.insert("1.0", generated_query)
            messagebox.showinfo("AI Query Generated",
                              "Query generated successfully! Review and execute.")
        else:
            messagebox.showwarning("AI Generation",
                                 "Could not generate query. Try using more specific terms.")

    def ai_query_interpreter(self, user_input):
        """🤖 AI INTELLIGENTE - Interpreta linguaggio naturale e genera SQL"""
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

    def execute_ai_query(self):
        """Esegue la query dall'AI Query Builder"""
        query = self.query_output.get("1.0", "end-1c").strip()

        if not query:
            messagebox.showwarning("Warning",
                                 "Please enter or generate a query first")
            return

        try:
            # Questo è un esempio - implementa l'esecuzione SQL sui dati
            messagebox.showinfo("Query Execution",
                              "Query execution feature coming soon!")

        except Exception as e:
            messagebox.showerror("Query Error",
                               f"Error executing query:\n{str(e)}")

    def show_statistics(self):
        """Mostra statistiche dei dati"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data loaded")
            return

        if not HAS_PANDAS:
            messagebox.showerror("Error", "Pandas required for statistics")
            return

        # Crea finestra statistiche
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Data Statistics")
        stats_window.geometry("800x600")
        stats_window.transient(self.root)

        # Text widget per statistiche
        stats_text = tk.Text(stats_window, wrap="none", font=("Consolas", 10))
        stats_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Calcola e mostra statistiche
        df = self.current_data
        stats_info = []

        stats_info.append("📊 DATASET OVERVIEW")
        stats_info.append("=" * 50)
        stats_info.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        stats_info.append(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        stats_info.append("")

        stats_info.append("📋 COLUMN INFORMATION")
        stats_info.append("=" * 50)
        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            stats_info.append(f"{col}: {dtype} | Nulls: {null_count} | Unique: {unique_count}")

        stats_info.append("")
        stats_info.append("📈 NUMERIC STATISTICS")
        stats_info.append("=" * 50)
        stats_info.append(str(df.describe()))

        # Inserisci nel text widget
        stats_text.insert("1.0", "\n".join(stats_info))
        stats_text.config(state="disabled")

    def toggle_filters(self):
        """Attiva/disattiva i filtri"""
        messagebox.showinfo("Filters", "Advanced filtering feature coming soon!")

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
    try:
        app = ExcelToolsUnified()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
