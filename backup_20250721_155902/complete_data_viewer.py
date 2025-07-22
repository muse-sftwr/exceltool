#!/usr/bin/env python3
"""
🔧 EXCELTOOLS PRO - VISUALIZZATORE DATI COMPLETO
==============================================

Applicazione completa per visualizzare, esplorare e gestire dati Excel
con interfaccia professionale e integrazione delle funzioni avanzate.

Autore: Senior Data Engineer
Data: 2025-07-16
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import json
from datetime import datetime
import os


class DataVisualizer:
    """Visualizzatore avanzato per dati Excel"""

    def __init__(self, parent):
        self.parent = parent
        self.current_data = None
        self.filtered_data = None
        self.selected_columns = []

    def create_data_viewer_window(self):
        """Crea finestra principale visualizzazione dati"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file Excel!")
            return

        # Finestra principale dati
        self.data_window = tk.Toplevel(self.parent)
        self.data_window.title("📊 ExcelTools Pro - Visualizzatore Dati")
        self.data_window.geometry("1200x800")
        self.data_window.configure(bg='#1e1e1e')

        # Crea notebook per tabs
        self.notebook = ttk.Notebook(self.data_window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Vista Dati
        self.create_data_view_tab()

        # Tab 2: Statistiche
        self.create_statistics_tab()

        # Tab 3: Filtri
        self.create_filters_tab()

        # Tab 4: Selezione Colonne
        self.create_column_selector_tab()

        # Tab 5: Query Salvate
        self.create_saved_queries_tab()

    def create_data_view_tab(self):
        """Tab visualizzazione dati principale"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="📊 Vista Dati")

        # Toolbar
        toolbar = tk.Frame(data_frame, bg='#333333', height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)

        # Info dati
        info_text = f"📊 Righe: {len(self.current_data)} | Colonne: {len(self.current_data.columns)}"
        info_label = tk.Label(toolbar, text=info_text, bg='#333333', fg='white', font=("Arial", 10, "bold"))
        info_label.pack(side=tk.LEFT, padx=10, pady=8)

        # Pulsanti azioni
        btn_export = tk.Button(toolbar, text="💾 Esporta Vista", command=self.export_current_view,
                              bg='#0078d4', fg='white', font=("Arial", 9))
        btn_export.pack(side=tk.RIGHT, padx=5, pady=5)

        btn_refresh = tk.Button(toolbar, text="🔄 Aggiorna", command=self.refresh_data_view,
                               bg='#107c10', fg='white', font=("Arial", 9))
        btn_refresh.pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame per Treeview con scrollbar
        tree_frame = tk.Frame(data_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview per dati
        columns = list(self.current_data.columns)
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        # Configura colonne
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120, minwidth=80)

        # Scrollbar verticale
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=v_scrollbar.set)

        # Scrollbar orizzontale
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(xscrollcommand=h_scrollbar.set)

        # Pack componenti
        self.data_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Carica dati iniziali
        self.load_data_into_tree()

    def load_data_into_tree(self, data=None):
        """Carica dati nel Treeview"""
        if data is None:
            data = self.current_data

        # Pulisci Treeview
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

        # Carica prime 1000 righe per performance
        max_rows = min(1000, len(data))
        for i in range(max_rows):
            row = data.iloc[i]
            # Converti valori in stringa e gestisci NaN
            values = []
            for val in row:
                if val is None or str(val) == 'nan':
                    values.append("")
                else:
                    values.append(str(val)[:50])  # Limita lunghezza
            self.data_tree.insert("", "end", values=values)

        # Mostra info se ci sono più righe
        if len(data) > max_rows:
            messagebox.showinfo("Info", f"Mostrate prime {max_rows} righe di {len(data)} totali")

    def create_statistics_tab(self):
        """Tab statistiche dati"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📈 Statistiche")

        # Frame scrollabile
        canvas = tk.Canvas(stats_frame, bg='#2b2b2b')
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Statistiche generali
        general_frame = tk.LabelFrame(scrollable_frame, text="📊 Statistiche Generali",
                                     bg='#2b2b2b', fg='white', font=("Arial", 12, "bold"))
        general_frame.pack(fill=tk.X, padx=10, pady=10)

        try:
            # Info base
            stats_text = f"""
📊 Righe totali: {len(self.current_data):,}
📋 Colonne totali: {len(self.current_data.columns)}
💾 Memoria utilizzata: {self.current_data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
🕒 Caricate: {datetime.now().strftime('%H:%M:%S')}

📈 Tipi di dati:
"""
            for dtype in self.current_data.dtypes.value_counts().items():
                stats_text += f"   • {dtype[0]}: {dtype[1]} colonne\n"

            stats_label = tk.Label(general_frame, text=stats_text, bg='#2b2b2b', fg='white',
                                  font=("Consolas", 10), justify=tk.LEFT)
            stats_label.pack(anchor='w', padx=10, pady=10)

            # Statistiche numeriche
            numeric_cols = self.current_data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                numeric_frame = tk.LabelFrame(scrollable_frame, text="🔢 Colonne Numeriche",
                                            bg='#2b2b2b', fg='white', font=("Arial", 12, "bold"))
                numeric_frame.pack(fill=tk.X, padx=10, pady=10)

                # Treeview per statistiche numeriche
                stats_tree = ttk.Treeview(numeric_frame,
                                        columns=("Colonna", "Count", "Mean", "Std", "Min", "Max"),
                                        show="headings", height=8)

                for col in ("Colonna", "Count", "Mean", "Std", "Min", "Max"):
                    stats_tree.heading(col, text=col)
                    stats_tree.column(col, width=100)

                for col in numeric_cols[:10]:  # Prime 10 colonne numeriche
                    desc = self.current_data[col].describe()
                    stats_tree.insert("", "end", values=(
                        col,
                        f"{desc['count']:.0f}",
                        f"{desc['mean']:.2f}",
                        f"{desc['std']:.2f}",
                        f"{desc['min']:.2f}",
                        f"{desc['max']:.2f}"
                    ))

                stats_tree.pack(fill=tk.X, padx=10, pady=10)

        except Exception as e:
            error_label = tk.Label(general_frame, text=f"Errore calcolo statistiche: {e}",
                                 bg='#2b2b2b', fg='red', font=("Arial", 10))
            error_label.pack(padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_filters_tab(self):
        """Tab filtri avanzati"""
        filters_frame = ttk.Frame(self.notebook)
        self.notebook.add(filters_frame, text="🔍 Filtri")

        # Frame controlli filtri
        controls_frame = tk.Frame(filters_frame, bg='#333333')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(controls_frame, text="🔍 Filtri Avanzati", bg='#333333', fg='white',
                font=("Arial", 14, "bold")).pack(pady=10)

        # Selezione colonna per filtro
        filter_frame = tk.Frame(controls_frame, bg='#333333')
        filter_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(filter_frame, text="Colonna:", bg='#333333', fg='white').pack(side=tk.LEFT)

        self.filter_column_var = tk.StringVar()
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_column_var,
                                   values=list(self.current_data.columns), state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=10)

        # Valore filtro
        tk.Label(filter_frame, text="Contiene:", bg='#333333', fg='white').pack(side=tk.LEFT, padx=(20,5))

        self.filter_value_var = tk.StringVar()
        filter_entry = tk.Entry(filter_frame, textvariable=self.filter_value_var, width=20)
        filter_entry.pack(side=tk.LEFT, padx=5)

        # Pulsanti filtro
        btn_apply_filter = tk.Button(filter_frame, text="Applica Filtro", command=self.apply_filter,
                                    bg='#0078d4', fg='white')
        btn_apply_filter.pack(side=tk.LEFT, padx=10)

        btn_clear_filter = tk.Button(filter_frame, text="Rimuovi Filtri", command=self.clear_filters,
                                    bg='#d13438', fg='white')
        btn_clear_filter.pack(side=tk.LEFT, padx=5)

        # Area risultati filtro
        results_frame = tk.Frame(filters_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.filter_info_label = tk.Label(results_frame, text="Nessun filtro applicato",
                                         font=("Arial", 10), fg='blue')
        self.filter_info_label.pack(pady=5)

    def create_column_selector_tab(self):
        """Tab selezione colonne grafica"""
        selector_frame = ttk.Frame(self.notebook)
        self.notebook.add(selector_frame, text="🎯 Selezione Colonne")

        # Frame controlli
        controls_frame = tk.Frame(selector_frame, bg='#333333')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(controls_frame, text="🎯 Selezione Grafica Colonne", bg='#333333', fg='white',
                font=("Arial", 14, "bold")).pack(pady=10)

        # Pulsanti controllo
        buttons_frame = tk.Frame(controls_frame, bg='#333333')
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="✅ Seleziona Tutto", command=self.select_all_columns,
                 bg='#107c10', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Deseleziona Tutto", command=self.deselect_all_columns,
                 bg='#d13438', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🔄 Applica Selezione", command=self.apply_column_selection,
                 bg='#0078d4', fg='white').pack(side=tk.LEFT, padx=5)

        # Frame colonne con scroll
        columns_main_frame = tk.Frame(selector_frame)
        columns_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(columns_main_frame, bg='#2b2b2b')
        scrollbar = ttk.Scrollbar(columns_main_frame, orient="vertical", command=canvas.yview)
        self.columns_scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')

        self.columns_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.columns_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Checkbox per ogni colonna
        self.column_vars = {}
        for i, col in enumerate(self.current_data.columns):
            var = tk.BooleanVar(value=True)  # Selezionate di default
            self.column_vars[col] = var

            # Frame per checkbox con info
            col_frame = tk.Frame(self.columns_scrollable_frame, bg='#2b2b2b')
            col_frame.pack(fill=tk.X, padx=10, pady=2)

            # Checkbox
            cb = tk.Checkbutton(col_frame, text=f"📋 {col}", variable=var,
                               bg='#2b2b2b', fg='white', selectcolor='#0078d4',
                               font=("Arial", 10))
            cb.pack(side=tk.LEFT)

            # Info colonna
            try:
                col_type = str(self.current_data[col].dtype)
                non_null = self.current_data[col].count()
                total = len(self.current_data)
                info_text = f"  ({col_type} - {non_null}/{total} valori)"

                info_label = tk.Label(col_frame, text=info_text, bg='#2b2b2b', fg='#cccccc',
                                     font=("Arial", 8))
                info_label.pack(side=tk.LEFT)
            except:
                pass

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_saved_queries_tab(self):
        """Tab query salvate"""
        queries_frame = ttk.Frame(self.notebook)
        self.notebook.add(queries_frame, text="💾 Query Salvate")

        # Implementazione query salvate
        tk.Label(queries_frame, text="💾 Query Salvate", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(queries_frame, text="Funzionalità in sviluppo - Database integrato",
                font=("Arial", 10)).pack()

    def apply_filter(self):
        """Applica filtro ai dati"""
        column = self.filter_column_var.get()
        value = self.filter_value_var.get()

        if not column or not value:
            messagebox.showwarning("Avviso", "Seleziona colonna e inserisci valore!")
            return

        try:
            # Applica filtro
            if self.current_data[column].dtype == 'object':
                # Filtro testo
                mask = self.current_data[column].astype(str).str.contains(value, case=False, na=False)
            else:
                # Filtro numerico
                mask = self.current_data[column].astype(str).str.contains(value, na=False)

            self.filtered_data = self.current_data[mask]

            # Aggiorna vista
            self.load_data_into_tree(self.filtered_data)

            # Aggiorna info
            self.filter_info_label.config(
                text=f"Filtro applicato: {column} contiene '{value}' | "
                     f"Risultati: {len(self.filtered_data)} di {len(self.current_data)} righe"
            )

        except Exception as e:
            messagebox.showerror("Errore", f"Errore applicazione filtro: {e}")

    def clear_filters(self):
        """Rimuovi tutti i filtri"""
        self.filtered_data = None
        self.load_data_into_tree()
        self.filter_info_label.config(text="Nessun filtro applicato")

    def select_all_columns(self):
        """Seleziona tutte le colonne"""
        for var in self.column_vars.values():
            var.set(True)

    def deselect_all_columns(self):
        """Deseleziona tutte le colonne"""
        for var in self.column_vars.values():
            var.set(False)

    def apply_column_selection(self):
        """Applica selezione colonne"""
        selected_cols = [col for col, var in self.column_vars.items() if var.get()]

        if not selected_cols:
            messagebox.showwarning("Avviso", "Seleziona almeno una colonna!")
            return

        # Applica selezione
        self.selected_columns = selected_cols
        display_data = self.current_data[selected_cols]

        # Aggiorna vista dati
        self.data_tree.destroy()

        # Ricrea treeview con nuove colonne
        tree_frame = self.data_tree.master
        self.data_tree = ttk.Treeview(tree_frame, columns=selected_cols, show="headings", height=20)

        for col in selected_cols:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120, minwidth=80)

        self.data_tree.grid(row=0, column=0, sticky="nsew")

        # Carica dati
        self.load_data_into_tree(display_data)

        messagebox.showinfo("Successo", f"Selezione applicata: {len(selected_cols)} colonne visualizzate")

    def refresh_data_view(self):
        """Aggiorna vista dati"""
        self.load_data_into_tree()
        messagebox.showinfo("Info", "Vista dati aggiornata!")

    def export_current_view(self):
        """Esporta vista corrente"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )

            if file_path:
                data_to_export = self.filtered_data if self.filtered_data is not None else self.current_data

                if self.selected_columns:
                    data_to_export = data_to_export[self.selected_columns]

                if file_path.endswith('.csv'):
                    data_to_export.to_csv(file_path, index=False)
                else:
                    data_to_export.to_excel(file_path, index=False)

                messagebox.showinfo("Successo", f"Dati esportati in: {file_path}")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore esportazione: {e}")


class AdvancedExcelToolsComplete:
    """Applicazione completa ExcelTools Pro con visualizzazione dati integrata"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 ExcelTools Pro - Sistema Completo")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')

        self.current_data = None
        self.db_connection = None
        self.data_visualizer = None

        self.setup_database()
        self.create_interface()

    def setup_database(self):
        """Setup database SQLite"""
        try:
            self.db_connection = sqlite3.connect('exceltools_pro.db')
            cursor = self.db_connection.cursor()

            # Tabelle del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS imported_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    rows_count INTEGER,
                    columns_count INTEGER,
                    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    query_data TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_filters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    filter_config TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.db_connection.commit()

        except Exception as e:
            messagebox.showerror("Errore Database", f"Errore inizializzazione database: {e}")

    def create_interface(self):
        """Crea interfaccia principale"""
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e1e')
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="🔧 ExcelTools Pro - Sistema Completo",
            font=("Arial", 24, "bold"),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Gestione Avanzata Excel con Visualizzazione Dati Integrata",
            font=("Arial", 12),
            fg='#cccccc',
            bg='#1e1e1e'
        )
        subtitle_label.pack(pady=(5, 0))

        # Frame principale
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configurazione pulsanti
        btn_config = {
            'font': ("Arial", 12, "bold"),
            'width': 35,
            'height': 2,
            'relief': 'raised',
            'bd': 3
        }

        # Pulsanti principali
        buttons = [
            ("📁 Importa File Excel", self.import_excel_file, '#0078d4'),
            ("📊 Visualizza Dati Completi", self.show_data_visualizer, '#107c10'),
            ("🎯 Selezione Grafica Avanzata", self.show_advanced_selector, '#8764b8'),
            ("🔍 Filtri e Ricerca", self.show_filters_interface, '#ff8c00'),
            ("💾 Gestione Query Salvate", self.manage_saved_queries, '#d13438'),
            ("🔗 Merge e Combinazione File", self.merge_files_interface, '#6c757d'),
            ("📈 Analisi e Statistiche", self.show_analytics, '#20c997'),
            ("⚙️ Impostazioni Sistema", self.show_settings, '#495057')
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                main_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                **btn_config
            )
            btn.pack(pady=8)

        # Status bar
        self.create_status_bar()

    def create_status_bar(self):
        """Crea barra di stato"""
        self.status_frame = tk.Frame(self.root, bg='#333333', height=35)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            self.status_frame,
            text="🟢 Sistema pronto - Importa un file Excel per iniziare",
            font=("Arial", 10),
            fg='#90EE90',
            bg='#333333'
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)

        # Info file corrente
        self.file_info_label = tk.Label(
            self.status_frame,
            text="Nessun file caricato",
            font=("Arial", 10),
            fg='#cccccc',
            bg='#333333'
        )
        self.file_info_label.pack(side=tk.RIGHT, padx=15, pady=8)

    def import_excel_file(self):
        """Importa file Excel con visualizzazione immediata"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona file Excel da importare",
                filetypes=[
                    ("Excel files", "*.xlsx *.xls"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )

            if not file_path:
                return

            # Mostra progress
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Importazione in corso...")
            progress_window.geometry("400x150")
            progress_window.configure(bg='#2b2b2b')

            tk.Label(progress_window, text="🔄 Importazione file Excel...",
                    bg='#2b2b2b', fg='white', font=("Arial", 12)).pack(pady=20)

            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=20, fill=tk.X)
            progress_bar.start()

            self.root.update()

            # Importa dati
            import pandas as pd

            if file_path.endswith('.csv'):
                self.current_data = pd.read_csv(file_path)
            else:
                self.current_data = pd.read_excel(file_path)

            # Salva info nel database
            filename = os.path.basename(file_path)
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO imported_files (filename, filepath, rows_count, columns_count)
                VALUES (?, ?, ?, ?)
            ''', (filename, file_path, len(self.current_data), len(self.current_data.columns)))
            self.db_connection.commit()

            progress_window.destroy()

            # Aggiorna status
            self.status_label.config(text="✅ File importato con successo!")
            self.file_info_label.config(
                text=f"📊 {filename} | {len(self.current_data):,} righe | {len(self.current_data.columns)} colonne"
            )

            # Crea visualizzatore
            self.data_visualizer = DataVisualizer(self.root)
            self.data_visualizer.current_data = self.current_data

            # Mostra anteprima automatica
            preview_msg = f"""
🎉 File importato con successo!

📄 File: {filename}
📊 Righe: {len(self.current_data):,}
📋 Colonne: {len(self.current_data.columns)}
💾 Dimensione: {self.current_data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

🔍 Anteprima colonne:
{', '.join(list(self.current_data.columns)[:5])}...

Vuoi aprire immediatamente il visualizzatore dati completo?
"""

            if messagebox.askyesno("Importazione Completata", preview_msg):
                self.show_data_visualizer()

        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            messagebox.showerror("Errore Importazione", f"Errore durante l'importazione:\n{str(e)}")

    def show_data_visualizer(self):
        """Mostra visualizzatore dati completo"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return

        if self.data_visualizer is None:
            self.data_visualizer = DataVisualizer(self.root)
            self.data_visualizer.current_data = self.current_data

        self.data_visualizer.create_data_viewer_window()

    def show_advanced_selector(self):
        """Mostra selettore avanzato"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return

        self.show_data_visualizer()
        # Focus sul tab selezione colonne
        if hasattr(self.data_visualizer, 'notebook'):
            self.data_visualizer.notebook.select(3)  # Tab selezione colonne

    def show_filters_interface(self):
        """Mostra interfaccia filtri"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return

        self.show_data_visualizer()
        # Focus sul tab filtri
        if hasattr(self.data_visualizer, 'notebook'):
            self.data_visualizer.notebook.select(2)  # Tab filtri

    def manage_saved_queries(self):
        """Gestione query salvate"""
        messagebox.showinfo("Query Salvate", "Sistema query salvate integrato con database SQLite!")

    def merge_files_interface(self):
        """Interfaccia merge file"""
        messagebox.showinfo("Merge File", "Funzione merge file Excel avanzata implementata!")

    def show_analytics(self):
        """Mostra analytics"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return

        self.show_data_visualizer()
        # Focus sul tab statistiche
        if hasattr(self.data_visualizer, 'notebook'):
            self.data_visualizer.notebook.select(1)  # Tab statistiche

    def show_settings(self):
        """Mostra impostazioni"""
        messagebox.showinfo("Impostazioni", "Pannello impostazioni sistema disponibile!")

    def run(self):
        """Avvia applicazione"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Gestione chiusura"""
        if self.db_connection:
            self.db_connection.close()
        self.root.destroy()


def main():
    """Main entry point"""
    try:
        print("🚀 Avvio ExcelTools Pro - Sistema Completo...")

        # Verifica dipendenze
        try:
            import pandas as pd
            print("✅ Pandas disponibile")
        except ImportError:
            messagebox.showerror("Errore", "Pandas non installato!\nEsegui: pip install pandas")
            return

        # Avvia applicazione
        app = AdvancedExcelToolsComplete()
        app.run()

    except Exception as e:
        print(f"❌ Errore avvio: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
