#!/usr/bin/env python3
"""
ExcelTools Pro - Applicazione Semplificata
Versione sicura e funzionante per gestione file Excel
"""

import os
import sqlite3
import threading
import logging
from datetime import datetime
# from typing import List, Dict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ Pandas non disponibile - funzionalità limitate")

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    HAS_CUSTOMTKINTER = True
except ImportError:
    HAS_CUSTOMTKINTER = False
    print("⚠️ CustomTkinter non disponibile - usando Tkinter standard")


class ExcelProcessor:
    """Processore Excel semplificato e sicuro"""

    def __init__(self):
        self.db_path = "excel_data.db"
        self.setup_logging()
        self.setup_database()

    def setup_logging(self):
        """Configura logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_database(self):
        """Inizializza database SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS excel_data (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            self.logger.info("Database inizializzato")
        except Exception as e:
            self.logger.error(f"Errore database: {e}")

    def read_excel_file(self, file_path: str):
        """Legge file Excel"""
        if not HAS_PANDAS:
            raise ImportError("Pandas non disponibile")

        try:
            df = pd.read_excel(file_path)
            self.logger.info(f"File letto: {file_path} ({len(df)} righe)")
            return df
        except Exception as e:
            self.logger.error(f"Errore lettura {file_path}: {e}")
            raise

    def save_to_database(self, df, table_name="excel_data"):
        """Salva DataFrame nel database con gestione colonne dinamiche"""
        if not HAS_PANDAS:
            return False

        try:
            conn = sqlite3.connect(self.db_path)

            # Usa replace per sovrascrivere la tabella con nuova struttura
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            self.logger.info(f"Dati salvati: {len(df)} righe nella tabella {table_name}")
            return True
        except Exception as e:
            self.logger.error(f"Errore salvataggio: {e}")
            return False

    def get_database_info(self):
        """Ottiene informazioni sui dati nel database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Lista tabelle
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            info = {"tables": []}
            for table in tables:
                table_name = table[0]

                # Info tabella
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]

                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                info["tables"].append({
                    "name": table_name,
                    "rows": row_count,
                    "columns": columns
                })

            conn.close()
            return info
        except Exception as e:
            self.logger.error(f"Errore info database: {e}")
            return {"tables": []}

    def query_database(self, query="SELECT * FROM excel_data LIMIT 10"):
        """Esegue query sul database"""
        try:
            conn = sqlite3.connect(self.db_path)
            result = pd.read_sql_query(query, conn)
            conn.close()
            return result
        except Exception as e:
            self.logger.error(f"Errore query: {e}")
            return None


class SimpleExcelGUI:
    """Interfaccia grafica semplificata"""

    def __init__(self):
        self.processor = ExcelProcessor()
        self.current_data = None
        self.setup_gui()

    def setup_gui(self):
        """Crea interfaccia"""
        if HAS_CUSTOMTKINTER:
            self.root = ctk.CTk()
            self.root.title("ExcelTools Pro - Versione Sicura")
            self.root.geometry("800x600")
        else:
            self.root = tk.Tk()
            self.root.title("ExcelTools Pro - Versione Standard")
            self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Titolo
        title_label = ttk.Label(
            main_frame,
            text="📊 ExcelTools Pro",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        if HAS_CUSTOMTKINTER:
            load_btn = ctk.CTkButton(
                btn_frame,
                text="📁 Carica File Excel",
                command=self.load_file,
                width=200
            )
        else:
            load_btn = ttk.Button(
                btn_frame,
                text="📁 Carica File Excel",
                command=self.load_file
            )
        load_btn.pack(side="left", padx=5)

        if HAS_CUSTOMTKINTER:
            save_btn = ctk.CTkButton(
                btn_frame,
                text="💾 Salva in Database",
                command=self.save_data,
                width=200
            )
        else:
            save_btn = ttk.Button(
                btn_frame,
                text="💾 Salva in Database",
                command=self.save_data
            )
        save_btn.pack(side="left", padx=5)

        if HAS_CUSTOMTKINTER:
            view_btn = ctk.CTkButton(
                btn_frame,
                text="🔍 Visualizza Database",
                command=self.view_database,
                width=200
            )
        else:
            view_btn = ttk.Button(
                btn_frame,
                text="🔍 Visualizza Database",
                command=self.view_database
            )
        view_btn.pack(side="left", padx=5)

        # Area di testo per output
        self.text_area = tk.Text(main_frame, height=20, width=80)
        self.text_area.pack(fill="both", expand=True, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_area.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.pack(side="bottom", fill="x")

        # Messaggio iniziale
        self.log_message("✅ ExcelTools Pro avviato correttamente")
        if HAS_PANDAS:
            self.log_message("✅ Pandas disponibile - tutte le funzionalità attive")
        else:
            self.log_message("⚠️ Pandas non disponibile - alcune funzionalità limitate")

    def log_message(self, message):
        """Aggiunge messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_area.see(tk.END)

    def load_file(self):
        """Carica file Excel"""
        if not HAS_PANDAS:
            messagebox.showerror("Errore", "Pandas non disponibile")
            return

        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )

        if not file_path:
            return

        def load_worker():
            try:
                self.status_var.set("Caricamento in corso...")
                self.log_message(f"📁 Caricamento: {os.path.basename(file_path)}")

                df = self.processor.read_excel_file(file_path)
                self.current_data = df

                self.log_message(f"✅ File caricato: {len(df)} righe, {len(df.columns)} colonne")
                self.log_message(f"📊 Colonne: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")

                self.status_var.set(f"File caricato: {len(df)} righe")

            except Exception as e:
                self.log_message(f"❌ Errore: {str(e)}")
                self.status_var.set("Errore nel caricamento")

        threading.Thread(target=load_worker, daemon=True).start()

    def save_data(self):
        """Salva dati nel database"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Nessun dato da salvare")
            return

        def save_worker():
            try:
                self.status_var.set("Salvataggio in corso...")
                self.log_message("💾 Salvando dati nel database...")

                success = self.processor.save_to_database(self.current_data)

                if success:
                    self.log_message("✅ Dati salvati nel database")
                    self.status_var.set("Dati salvati")
                else:
                    self.log_message("❌ Errore nel salvataggio")
                    self.status_var.set("Errore salvataggio")

            except Exception as e:
                self.log_message(f"❌ Errore: {str(e)}")
                self.status_var.set("Errore")
        threading.Thread(target=save_worker, daemon=True).start()

    def view_database(self):
        """Visualizza i dati del database"""
        def view_worker():
            try:
                self.status_var.set("Caricamento database...")
                self.log_message("🔍 Visualizzando dati database...")

                # Ottieni info database
                db_info = self.processor.get_database_info()

                if not db_info["tables"]:
                    self.log_message("📭 Database vuoto - nessuna tabella trovata")
                    self.status_var.set("Database vuoto")
                    return

                # Mostra info tabelle
                for table in db_info["tables"]:
                    name = table["name"]
                    rows = table["rows"]
                    cols = len(table["columns"])
                    self.log_message(f"📊 Tabella: {name} ({rows} righe, {cols} colonne)")

                # Carica dati da visualizzare
                query = "SELECT * FROM excel_data LIMIT 10"
                result = self.processor.query_database(query)

                if result is not None and not result.empty:
                    self.log_message(f"📋 Prime 10 righe caricate:")

                    # Mostra sample dei dati
                    for i, row in result.head(3).iterrows():
                        sample = ", ".join([f"{col}:{val}" for col, val in zip(row.index[:3], row.values[:3])])
                        self.log_message(f"   Riga {i+1}: {sample}...")

                    self.status_var.set(f"Database caricato: {len(result)} righe mostrate")
                else:
                    self.log_message("📭 Nessun dato nella tabella excel_data")
                    self.status_var.set("Tabella vuota")

            except Exception as e:
                self.log_message(f"❌ Errore visualizzazione: {str(e)}")
                self.status_var.set("Errore visualizzazione")

        threading.Thread(target=view_worker, daemon=True).start()

    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    print("🚀 Avviando ExcelTools Pro...")

    try:
        app = SimpleExcelGUI()
        app.run()
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
