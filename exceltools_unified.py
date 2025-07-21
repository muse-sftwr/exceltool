#!/usr/bin/env python3
"""
🚀 EXCELTOOLS UNIFIED - Strumento Completo e Ottimizzato
========================================================

Un unico strumento che integra tutte le funzionalità:
- Database Manager con interfaccia ottimizzata
- Import/Export Excel con anteprima
- Query Builder visuale integrato
- Filtri avanzati sempre visibili
- Interfaccia responsive e moderna

Autore: Senior Developer
Data: 2025-07-21
Versione: Unified 1.0
"""

import os
import sqlite3
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ pandas non disponibile - alcune funzionalità saranno limitate")

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
        """Crea barra degli strumenti"""
        if HAS_CUSTOMTKINTER:
            toolbar = ctk.CTkFrame(self.root)
        else:
            toolbar = ttk.Frame(self.root)

        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Pulsanti principali
        buttons = [
            ("📁 Importa Excel", self.import_excel),
            ("�+ Import Multi", self.import_multiple),
            ("🔗 Merge Files", self.merge_files),
            ("�💾 Esporta Dati", self.export_data),
            ("🔍 Filtri Avanzati", self.toggle_filters),
            ("⚡ Query Builder", self.open_query_builder),
            ("👁️ Viste Salvate", self.manage_saved_views),
            ("📊 Statistiche", self.show_statistics),
            ("🔄 Refresh", self.refresh_data)
        ]

        for i, (text, command) in enumerate(buttons):
            if HAS_CUSTOMTKINTER:
                btn = ctk.CTkButton(toolbar, text=text, command=command, width=120)
            else:
                btn = ttk.Button(toolbar, text=text, command=command, width=15)
            btn.grid(row=0, column=i, padx=5, pady=5)

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

    def run(self):
        """Avvia l'applicazione"""
        print("🚀 Avvio ExcelTools Unified...")
        print("📊 Interfaccia ottimizzata per il tuo schermo")
        print("🔍 Pannello filtri sempre visibile")
        print("⚡ Query builder integrato")
        print("✅ Pronto all'uso!")

        self.root.mainloop()

    # ==================== NUOVE FUNZIONALITÀ ====================

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
