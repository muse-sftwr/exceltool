#!/usr/bin/env python3
# cSpell:disable
"""
ExcelTools - Tool ottimizzato per gestione avanzata di file Excel
Sviluppato per performance elevate e semplicita d'uso
"""

import logging
import os
import sqlite3
import threading
from datetime import datetime
from typing import Dict, List

import customtkinter as ctk
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configurazione tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ExcelProcessor:
    """Classe ottimizzata per l'elaborazione di file Excel grandi"""

    def __init__(self):
        self.db_path = "excel_data.db"
        self.setup_database()
        self.setup_logging()

    def setup_logging(self):
        """Configura il sistema di logging"""
        log_filename = f'excel_tool_{datetime.now().strftime("%Y%m%d")}.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def setup_database(self):
        """Inizializza il database SQLite per le performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tabella principale per i dati
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS excel_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    sheet_name TEXT,
                    data_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabella per i metadati
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    file_size INTEGER,
                    rows_count INTEGER,
                    columns_count INTEGER,
                    last_modified TIMESTAMP,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Indici per le performance
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_file_name '
                'ON excel_data(file_name)'
            )
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_file_path '
                'ON file_metadata(file_path)'
            )

            conn.commit()
            conn.close()
            self.logger.info("Database inizializzato correttamente")
        except Exception as e:
            error_msg = f"Errore nell'inizializzazione del database: {e}"
            self.logger.error(error_msg)

    def read_excel_optimized(
        self, file_path: str, chunk_size: int = 10000
    ) -> pd.DataFrame:
        """Lettura ottimizzata di file Excel di grandi dimensioni"""
        try:
            self.logger.info(f"Inizio lettura file: {file_path}")

            # Verifica dimensioni file
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024*1024)
            self.logger.info(f"Dimensione file: {size_mb:.2f} MB")

            # Lettura ottimizzata basata sulle dimensioni
            if file_size > 50 * 1024 * 1024:  # > 50MB
                # Lettura a chunk per file molto grandi
                return self._read_large_excel(file_path, chunk_size)
            else:
                # Lettura diretta per file piu piccoli
                return pd.read_excel(file_path, engine='openpyxl')

        except Exception as e:
            error_msg = f"Errore nella lettura del file {file_path}: {e}"
            self.logger.error(error_msg)
            raise

    def _read_large_excel(
        self, file_path: str, chunk_size: int
    ) -> pd.DataFrame:
        """Lettura a chunk per file Excel molto grandi"""
        try:
            # Prima lettura per ottenere info sulla struttura
            sample_df = pd.read_excel(
                file_path, nrows=1000, engine='openpyxl'
            )

            # Lettura completa con dtype ottimizzati
            dtypes = self._optimize_dtypes(sample_df)

            df = pd.read_excel(
                file_path,
                engine='openpyxl',
                dtype=dtypes,
                na_values=['', 'NULL', 'null', 'N/A', '#N/A']
            )

            rows_count = len(df)
            cols_count = len(df.columns)
            success_msg = f"File letto: {rows_count} righe, {cols_count} colonne"
            self.logger.info(success_msg)
            return df

        except Exception as e:
            error_msg = f"Errore nella lettura chunk del file: {e}"
            self.logger.error(error_msg)
            raise

    def _optimize_dtypes(self, df: pd.DataFrame) -> Dict:
        """Ottimizza i tipi di dati per ridurre l'uso di memoria"""
        dtypes = {}

        for col in df.columns:
            col_type = df[col].dtype

            if col_type == 'object':
                # Prova a convertire in categoria se ci sono pochi valori unici
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.5:
                    dtypes[col] = 'category'
                else:
                    dtypes[col] = 'string'
            elif 'int' in str(col_type):
                # Ottimizza interi
                c_min = df[col].min()
                c_max = df[col].max()

                int8_min = np.iinfo(np.int8).min
                int8_max = np.iinfo(np.int8).max
                int16_min = np.iinfo(np.int16).min
                int16_max = np.iinfo(np.int16).max
                int32_min = np.iinfo(np.int32).min
                int32_max = np.iinfo(np.int32).max

                if c_min > int8_min and c_max < int8_max:
                    dtypes[col] = np.int8
                elif c_min > int16_min and c_max < int16_max:
                    dtypes[col] = np.int16
                elif c_min > int32_min and c_max < int32_max:
                    dtypes[col] = np.int32

        return dtypes

    def merge_dataframes(
        self, dataframes: List[pd.DataFrame],
        merge_strategy: str = 'concat'
    ) -> pd.DataFrame:
        """Merge ottimizzato di multiple DataFrame"""
        try:
            df_count = len(dataframes)
            self.logger.info(f"Inizio merge di {df_count} DataFrame")

            if merge_strategy == 'concat':
                # Concatenazione semplice
                result = pd.concat(dataframes, ignore_index=True, sort=False)
            elif merge_strategy == 'union':
                # Union con rimozione duplicati
                result = pd.concat(dataframes, ignore_index=True, sort=False)
                result = result.drop_duplicates()
            else:
                # Merge personalizzato
                result = dataframes[0]
                for df in dataframes[1:]:
                    result = pd.merge(result, df, how='outer')

            result_rows = len(result)
            self.logger.info(f"Merge completato: {result_rows} righe totali")
            return result

        except Exception as e:
            error_msg = f"Errore nel merge: {e}"
            self.logger.error(error_msg)
            raise

    def save_to_database(
        self, df: pd.DataFrame, table_name: str = 'excel_data'
    ):
        """Salva DataFrame nel database SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)

            # Conversione ottimizzata per SQLite
            df_copy = df.copy()

            # Gestione valori null e tipi
            for col in df_copy.columns:
                if df_copy[col].dtype == 'object':
                    df_copy[col] = df_copy[col].astype(str)
                elif 'datetime' in str(df_copy[col].dtype):
                    df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d %H:%M:%S')

            df_copy.to_sql(
                table_name, conn, if_exists='append',
                index=False, method='multi'
            )
            conn.close()

            rows_saved = len(df)
            self.logger.info(f"Dati salvati nel database: {rows_saved} righe")

        except Exception as e:
            error_msg = f"Errore nel salvataggio database: {e}"
            self.logger.error(error_msg)
            raise

    def export_to_excel(
        self, df: pd.DataFrame, output_path: str, optimize: bool = True
    ):
        """Esportazione ottimizzata in Excel"""
        try:
            if optimize and len(df) > 100000:
                # Per file molto grandi, usa writer ottimizzato
                writer_options = {'remove_timezone': True}
                with pd.ExcelWriter(
                    output_path, engine='openpyxl', options=writer_options
                ) as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
            else:
                df.to_excel(output_path, index=False, engine='openpyxl')

            self.logger.info(f"File esportato: {output_path}")

        except Exception as e:
            error_msg = f"Errore nell'esportazione: {e}"
            self.logger.error(error_msg)
            raise


class FileWatcher(FileSystemEventHandler):
    """Monitoraggio automatico delle modifiche ai file"""

    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            file_extensions = ('.xlsx', '.xls')
            if event.src_path.endswith(file_extensions):
                self.callback(event.src_path)


class ExcelToolGUI:
    """Interfaccia grafica moderna e reattiva"""

    def __init__(self):
        self.processor = ExcelProcessor()
        self.current_dataframes = []
        self.watcher_thread = None
        self.setup_gui()

    def setup_gui(self):
        """Inizializza l'interfaccia grafica"""
        self.root = ctk.CTk()
        self.root.title("ExcelTools Pro - Gestione Avanzata File Excel")
        self.root.geometry("1200x800")

        # Layout principale
        self.create_main_layout()
        self.create_menu_bar()
        self.create_status_bar()

        # Variabili di stato
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto")

    def create_main_layout(self):
        """Crea il layout principale dell'applicazione"""
        # Frame principale con split
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Pannello sinistro - Controlli
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.pack(side="left", fill="y", padx=(0, 5))

        # Pannello destro - Visualizzazione dati
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True,
                             padx=(5, 0))

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        """Crea il pannello di controllo sinistro"""
        # Titolo
        title_font = ("Arial", 18, "bold")
        title = ctk.CTkLabel(self.left_panel, text="Controlli", font=title_font)
        title.pack(pady=10)

        # Sezione Import
        import_frame = ctk.CTkFrame(self.left_panel)
        import_frame.pack(fill="x", padx=10, pady=5)

        import_font = ("Arial", 14, "bold")
        import_label = ctk.CTkLabel(
            import_frame, text="Importazione File", font=import_font
        )
        import_label.pack(pady=5)

        select_btn = ctk.CTkButton(
            import_frame,
            text="📁 Seleziona File Excel",
            command=self.select_files,
            height=40
        )
        select_btn.pack(pady=5, padx=10, fill="x")

        monitor_btn = ctk.CTkButton(
            import_frame,
            text="📂 Monitora Cartella",
            command=self.start_folder_monitoring,
            height=40
        )
        monitor_btn.pack(pady=5, padx=10, fill="x")

        # Sezione Elaborazione
        process_frame = ctk.CTkFrame(self.left_panel)
        process_frame.pack(fill="x", padx=10, pady=5)

        process_font = ("Arial", 14, "bold")
        process_label = ctk.CTkLabel(
            process_frame, text="Elaborazione", font=process_font
        )
        process_label.pack(pady=5)

        merge_btn = ctk.CTkButton(
            process_frame,
            text="🔄 Merge File",
            command=self.merge_files,
            height=40
        )
        merge_btn.pack(pady=5, padx=10, fill="x")

        save_btn = ctk.CTkButton(
            process_frame,
            text="🗃️ Salva in Database",
            command=self.save_to_db,
            height=40
        )
        save_btn.pack(pady=5, padx=10, fill="x")

        # Sezione Export
        export_frame = ctk.CTkFrame(self.left_panel)
        export_frame.pack(fill="x", padx=10, pady=5)

        export_font = ("Arial", 14, "bold")
        export_label = ctk.CTkLabel(
            export_frame, text="Esportazione", font=export_font
        )
        export_label.pack(pady=5)

        export_btn = ctk.CTkButton(
            export_frame,
            text="💾 Esporta Excel",
            command=self.export_excel,
            height=40
        )
        export_btn.pack(pady=5, padx=10, fill="x")

        stats_btn = ctk.CTkButton(
            export_frame,
            text="📊 Statistiche",
            command=self.show_statistics,
            height=40
        )
        stats_btn.pack(pady=5, padx=10, fill="x")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.left_panel)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)

    def create_right_panel(self):
        """Crea il pannello di visualizzazione dati"""
        # Titolo
        title_font = ("Arial", 18, "bold")
        title = ctk.CTkLabel(
            self.right_panel, text="Visualizzazione Dati", font=title_font
        )
        title.pack(pady=10)

        # Notebook per tab multiple
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab per preview dati
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="Anteprima Dati")

        # Tab per statistiche
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistiche")

        # Tab per log
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Log Operazioni")

        self.create_preview_tab()
        self.create_stats_tab()
        self.create_log_tab()

    def create_preview_tab(self):
        """Crea la tab di anteprima dati"""
        # Treeview per visualizzare i dati
        columns = ("Col1", "Col2", "Col3", "Col4", "Col5")
        self.tree = ttk.Treeview(
            self.preview_frame, columns=columns, show="headings", height=20
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.preview_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_stats_tab(self):
        """Crea la tab delle statistiche"""
        self.stats_text = tk.Text(self.stats_frame, wrap="word", height=20)
        stats_scroll = ttk.Scrollbar(
            self.stats_frame, orient="vertical", command=self.stats_text.yview
        )
        self.stats_text.configure(yscrollcommand=stats_scroll.set)

        self.stats_text.pack(side="left", fill="both", expand=True)
        stats_scroll.pack(side="right", fill="y")

    def create_log_tab(self):
        """Crea la tab dei log"""
        self.log_text = tk.Text(self.log_frame, wrap="word", height=20)
        log_scroll = ttk.Scrollbar(
            self.log_frame, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.pack(side="right", fill="y")

    def create_menu_bar(self):
        """Crea la barra dei menu"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Menu File
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Nuovo Progetto", command=self.new_project)
        file_menu.add_command(label="Apri Progetto", command=self.open_project)
        file_menu.add_command(label="Salva Progetto", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # Menu Strumenti
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Strumenti", menu=tools_menu)
        tools_menu.add_command(label="Impostazioni", command=self.show_settings)
        tools_menu.add_command(
            label="Pulizia Database", command=self.clean_database
        )

        # Menu Aiuto
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aiuto", menu=help_menu)
        help_menu.add_command(label="Documentazione", command=self.show_help)
        help_menu.add_command(label="Info", command=self.show_about)

    def create_status_bar(self):
        """Crea la barra di stato"""
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            self.status_frame, text="Pronto", anchor="w"
        )
        self.status_label.pack(side="left", padx=10)

        self.time_label = ctk.CTkLabel(
            self.status_frame, text="", anchor="e"
        )
        self.time_label.pack(side="right", padx=10)

        self.update_time()

    def update_time(self):
        """Aggiorna l'orario nella status bar"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time)

    def select_files(self):
        """Seleziona e carica file Excel"""
        files = filedialog.askopenfilenames(
            title="Seleziona file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )

        if files:
            self.load_files_async(files)

    def load_files_async(self, files):
        """Carica file in modo asincrono"""
        def load_worker():
            try:
                self.update_status("Caricamento file in corso...")
                self.progress_bar.set(0)

                total_files = len(files)
                loaded_dfs = []

                for i, file_path in enumerate(files):
                    file_name = os.path.basename(file_path)
                    self.log_message(f"Caricamento: {file_name}")

                    df = self.processor.read_excel_optimized(file_path)
                    loaded_dfs.append(df)

                    progress = (i + 1) / total_files
                    self.progress_bar.set(progress)

                    # Aggiorna preview con il primo file
                    if i == 0:
                        self.root.after(0, lambda: self.update_preview(df))

                self.current_dataframes = loaded_dfs
                success_msg = f"Caricati {total_files} file con successo"
                self.update_status(success_msg)
                self.progress_bar.set(1)

                # Aggiorna statistiche
                self.root.after(0, self.update_statistics)

            except Exception as e:
                error_msg = f"Errore nel caricamento: {str(e)}"
                self.log_message(error_msg)
                self.update_status("Errore nel caricamento file")

        threading.Thread(target=load_worker, daemon=True).start()

    def update_preview(self, df):
        """Aggiorna l'anteprima dei dati"""
        # Pulisce il treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Aggiorna le colonne
        if len(df.columns) > 0:
            # Max 10 colonne per performance
            display_columns = list(df.columns)[:10]
            self.tree["columns"] = display_columns

            for col in self.tree["columns"]:
                self.tree.heading(col, text=str(col))
                self.tree.column(col, width=120)

        # Aggiunge i dati (max 100 righe per performance)
        for idx, row in df.head(100).iterrows():
            values = []
            for col in self.tree["columns"]:
                cell_value = row[col]
                if pd.notna(cell_value):
                    # Limita lunghezza testo a 50 caratteri
                    display_value = str(cell_value)[:50]
                else:
                    display_value = ""
                values.append(display_value)
            self.tree.insert("", "end", values=values)

    def update_statistics(self):
        """Aggiorna le statistiche dei dati"""
        if not self.current_dataframes:
            return

        stats_text = "=== STATISTICHE DATASET ===\n\n"

        total_rows = sum(len(df) for df in self.current_dataframes)
        total_files = len(self.current_dataframes)

        stats_text += f"File caricati: {total_files}\n"
        stats_text += f"Righe totali: {total_rows:,}\n\n"

        for i, df in enumerate(self.current_dataframes, 1):
            stats_text += f"--- File {i} ---\n"
            stats_text += f"Righe: {len(df):,}\n"
            stats_text += f"Colonne: {len(df.columns)}\n"

            # Calcola memoria utilizzata
            memory_usage = df.memory_usage(deep=True).sum()
            memory_mb = memory_usage / 1024 / 1024
            stats_text += f"Memoria: {memory_mb:.2f} MB\n\n"

            # Info sulle colonne (prime 10)
            stats_text += "Colonne:\n"
            display_cols = list(df.columns)[:10]
            for col in display_cols:
                dtype = str(df[col].dtype)
                null_count = df[col].isnull().sum()
                stats_text += f"  - {col}: {dtype} (null: {null_count})\n"

            remaining_cols = len(df.columns) - 10
            if remaining_cols > 0:
                stats_text += f"  ... e altre {remaining_cols} colonne\n"

            stats_text += "\n"

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)

    def merge_files(self):
        """Merge dei file caricati"""
        if len(self.current_dataframes) < 2:
            warning_msg = "Carica almeno 2 file per il merge"
            messagebox.showwarning("Attenzione", warning_msg)
            return

        def merge_worker():
            try:
                self.update_status("Merge in corso...")
                self.progress_bar.set(0)

                merged_df = self.processor.merge_dataframes(
                    self.current_dataframes
                )

                self.current_dataframes = [merged_df]
                self.progress_bar.set(1)

                rows_count = len(merged_df)
                success_msg = f"Merge completato: {rows_count:,} righe"
                self.update_status(success_msg)

                # Aggiorna preview e statistiche
                self.root.after(0, lambda: self.update_preview(merged_df))
                self.root.after(0, self.update_statistics)

            except Exception as e:
                error_msg = f"Errore nel merge: {str(e)}"
                self.log_message(error_msg)
                self.update_status("Errore nel merge")

        threading.Thread(target=merge_worker, daemon=True).start()

    def save_to_db(self):
        """Salva i dati nel database"""
        if not self.current_dataframes:
            warning_msg = "Nessun dato da salvare"
            messagebox.showwarning("Attenzione", warning_msg)
            return

        def save_worker():
            try:
                self.update_status("Salvataggio in database...")

                total_dfs = len(self.current_dataframes)
                for i, df in enumerate(self.current_dataframes):
                    table_name = f"data_table_{i+1}"
                    self.processor.save_to_database(df, table_name)

                    progress = (i + 1) / total_dfs
                    self.progress_bar.set(progress)

                self.update_status("Dati salvati nel database")
                self.log_message("Salvataggio database completato")

            except Exception as e:
                error_msg = f"Errore nel salvataggio: {str(e)}"
                self.log_message(error_msg)
                self.update_status("Errore nel salvataggio")

        threading.Thread(target=save_worker, daemon=True).start()

    def export_excel(self):
        """Esporta i dati in Excel"""
        if not self.current_dataframes:
            warning_msg = "Nessun dato da esportare"
            messagebox.showwarning("Attenzione", warning_msg)
            return

        output_path = filedialog.asksaveasfilename(
            title="Salva file Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if output_path:
            def export_worker():
                try:
                    self.update_status("Esportazione in corso...")

                    if len(self.current_dataframes) == 1:
                        # Singolo dataframe
                        self.processor.export_to_excel(
                            self.current_dataframes[0], output_path
                        )
                    else:
                        # Multiple sheets
                        with pd.ExcelWriter(
                            output_path, engine='openpyxl'
                        ) as writer:
                            for i, df in enumerate(self.current_dataframes):
                                sheet_name = f"Sheet_{i+1}"
                                df.to_excel(
                                    writer, sheet_name=sheet_name, index=False
                                )

                    file_name = os.path.basename(output_path)
                    success_msg = f"File esportato: {file_name}"
                    self.update_status(success_msg)
                    self.log_message(f"Esportazione completata: {output_path}")

                except Exception as e:
                    error_msg = f"Errore nell'esportazione: {str(e)}"
                    self.log_message(error_msg)
                    self.update_status("Errore nell'esportazione")

            threading.Thread(target=export_worker, daemon=True).start()

    def start_folder_monitoring(self):
        """Avvia il monitoraggio di una cartella"""
        folder_path = filedialog.askdirectory(
            title="Seleziona cartella da monitorare"
        )

        if folder_path:
            def file_changed_callback(file_path):
                file_name = os.path.basename(file_path)
                self.log_message(f"File modificato: {file_name}")
                # Auto-reload del file modificato
                self.load_files_async([file_path])

            self.watcher = FileWatcher(file_changed_callback)
            self.observer = Observer()
            self.observer.schedule(self.watcher, folder_path, recursive=True)
            self.observer.start()

            status_msg = f"Monitoraggio attivo: {folder_path}"
            self.update_status(status_msg)
            log_msg = f"Monitoraggio cartella attivato: {folder_path}"
            self.log_message(log_msg)

    def show_statistics(self):
        """Mostra statistiche dettagliate"""
        self.notebook.select(1)  # Seleziona tab statistiche
        self.update_statistics()

    def update_status(self, message):
        """Aggiorna la status bar"""
        self.status_label.configure(text=message)

    def log_message(self, message):
        """Aggiunge un messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    # Metodi placeholder per menu
    def new_project(self):
        """Crea nuovo progetto"""
        self.current_dataframes = []
        self.update_preview(pd.DataFrame())
        self.update_status("Nuovo progetto")

    def open_project(self):
        """Apre progetto esistente"""
        messagebox.showinfo("Info", "Funzione in sviluppo")

    def save_project(self):
        """Salva progetto corrente"""
        messagebox.showinfo("Info", "Funzione in sviluppo")

    def show_settings(self):
        """Mostra finestra impostazioni"""
        messagebox.showinfo("Info", "Funzione in sviluppo")

    def clean_database(self):
        """Pulisce il database"""
        messagebox.showinfo("Info", "Funzione in sviluppo")

    def show_help(self):
        """Mostra documentazione"""
        help_text = """
        ExcelTools Pro - Guida Rapida

        1. Importazione:
           - Seleziona File Excel: carica uno o piu file .xlsx/.xls
           - Monitora Cartella: rileva automaticamente nuovi file

        2. Elaborazione:
           - Merge File: unisce i file caricati
           - Salva in Database: memorizza i dati per elaborazioni future

        3. Esportazione:
           - Esporta Excel: salva i dati elaborati
           - Statistiche: visualizza informazioni dettagliate

        Ottimizzazioni:
        - Gestione automatica di file fino a 150.000+ righe
        - Lettura ottimizzata per performance elevate
        - Database SQLite integrato per velocita
        """
        messagebox.showinfo("Aiuto", help_text)

    def show_about(self):
        """Mostra informazioni sull'applicazione"""
        about_text = """
        ExcelTools Pro v1.0

        Tool avanzato per la gestione di file Excel di grandi dimensioni.
        Ottimizzato per performance e semplicita d'uso.

        Caratteristiche:
        - Interfaccia moderna e intuitiva
        - Gestione file fino a 150k+ righe
        - Database integrato
        - Monitoraggio automatico
        - Export ottimizzato

        Sviluppato con Python, Pandas, CustomTkinter
        """
        messagebox.showinfo("Info", about_text)

    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    app = ExcelToolGUI()
    app.run()


if __name__ == "__main__":
    main()
