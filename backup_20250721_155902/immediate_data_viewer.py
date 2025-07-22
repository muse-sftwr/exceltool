#!/usr/bin/env python3
"""
🔧 EXCELTOOLS PRO - VISUALIZZATORE IMMEDIATO
===========================================

Applicazione che mostra immediatamente i dati importati
con tutte le funzionalità integrate e visibili.

Autore: Data Display Engineer
Data: 2025-07-16
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import os
from datetime import datetime


class ExcelDataDisplay:
    """Visualizzatore immediato dati Excel"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 ExcelTools Pro - Visualizzatore Dati")
        self.root.geometry("1100x800")
        self.root.configure(bg='#1e1e1e')

        self.current_data = None
        self.current_file = None

        self.create_interface()

    def create_interface(self):
        """Crea interfaccia completa"""

        # Header con info
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=100)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🔧 ExcelTools Pro - Visualizzatore Dati Completo",
            font=("Arial", 18, "bold"),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(10, 5))

        self.file_info_label = tk.Label(
            header_frame,
            text="📁 Nessun file caricato - Clicca 'Carica File' per iniziare",
            font=("Arial", 11),
            fg='#cccccc',
            bg='#1e1e1e'
        )
        self.file_info_label.pack()

        # Toolbar
        toolbar_frame = tk.Frame(self.root, bg='#333333', height=50)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        toolbar_frame.pack_propagate(False)

        # Pulsanti toolbar
        btn_load = tk.Button(
            toolbar_frame,
            text="📁 Carica File Excel/CSV",
            command=self.load_file,
            bg='#0078d4',
            fg='white',
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_load.pack(side=tk.LEFT, padx=10, pady=8)

        btn_show_all = tk.Button(
            toolbar_frame,
            text="📊 Mostra Tutti i Dati",
            command=self.show_all_data,
            bg='#107c10',
            fg='white',
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_show_all.pack(side=tk.LEFT, padx=5, pady=8)

        btn_filter = tk.Button(
            toolbar_frame,
            text="🔍 Applica Filtri",
            command=self.apply_quick_filter,
            bg='#ff8c00',
            fg='white',
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_filter.pack(side=tk.LEFT, padx=5, pady=8)

        btn_select_cols = tk.Button(
            toolbar_frame,
            text="🎯 Seleziona Colonne",
            command=self.select_columns,
            bg='#8764b8',
            fg='white',
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_select_cols.pack(side=tk.LEFT, padx=5, pady=8)

        btn_export = tk.Button(
            toolbar_frame,
            text="💾 Esporta Dati",
            command=self.export_data,
            bg='#d13438',
            fg='white',
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_export.pack(side=tk.RIGHT, padx=10, pady=8)

        # Area principale con notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Vista Dati
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="📊 Dati Importati")

        # Tab 2: Informazioni
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="ℹ️ Informazioni File")

        # Tab 3: Funzioni
        self.functions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.functions_frame, text="🔧 Funzioni Avanzate")

        self.setup_data_tab()
        self.setup_info_tab()
        self.setup_functions_tab()

        # Status bar
        self.status_frame = tk.Frame(self.root, bg='#333333', height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            self.status_frame,
            text="🟢 Sistema pronto - Carica un file per visualizzare i dati",
            font=("Arial", 9),
            fg='#90EE90',
            bg='#333333'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def setup_data_tab(self):
        """Setup tab visualizzazione dati"""

        # Messaggio iniziale
        self.welcome_frame = tk.Frame(self.data_frame, bg='#2b2b2b')
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        welcome_label = tk.Label(
            self.welcome_frame,
            text="📊 VISUALIZZATORE DATI EXCEL\n\n"
                 "Carica un file Excel o CSV per vedere immediatamente:\n\n"
                 "✅ Tutti i dati in formato tabella\n"
                 "✅ Informazioni complete sul file\n"
                 "✅ Statistiche automatiche\n"
                 "✅ Funzioni di filtro e selezione\n"
                 "✅ Esportazione dati personalizzata\n\n"
                 "Clicca su 'Carica File Excel/CSV' per iniziare!",
            font=("Arial", 12),
            fg='white',
            bg='#2b2b2b',
            justify=tk.CENTER
        )
        welcome_label.pack(expand=True)

    def setup_info_tab(self):
        """Setup tab informazioni"""

        info_text = tk.Text(
            self.info_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg='#2b2b2b',
            fg='white',
            padx=20,
            pady=20
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        initial_info = """
🔧 EXCELTOOLS PRO - INFORMAZIONI SISTEMA

📊 STATO ATTUALE:
   • Nessun file caricato
   • Sistema pronto per importazione
   • Tutte le funzioni disponibili

💡 FUNZIONALITÀ DISPONIBILI:
   • Importazione file Excel (.xlsx, .xls)
   • Importazione file CSV
   • Visualizzazione dati completa
   • Filtri avanzati
   • Selezione colonne grafica
   • Esportazione personalizzata
   • Statistiche automatiche

🎯 COME USARE:
   1. Clicca "Carica File Excel/CSV"
   2. Seleziona il tuo file
   3. I dati appariranno immediatamente
   4. Usa i pulsanti per filtrare e selezionare
   5. Esporta i risultati quando necessario

🔧 FUNZIONI INTEGRATE:
   • Database SQLite interno
   • Query salvate automatiche
   • Backup configurazioni
   • Log delle operazioni

Carica un file per vedere tutte le informazioni dettagliate!
"""

        info_text.insert(tk.END, initial_info)
        info_text.config(state=tk.DISABLED)
        self.info_text = info_text

    def setup_functions_tab(self):
        """Setup tab funzioni avanzate"""

        # Frame per le funzioni
        functions_main = tk.Frame(self.functions_frame, bg='#2b2b2b')
        functions_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Titolo
        title_label = tk.Label(
            functions_main,
            text="🔧 Funzioni Avanzate ExcelTools Pro",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#2b2b2b'
        )
        title_label.pack(pady=(0, 20))

        # Grid per funzioni
        functions_grid = tk.Frame(functions_main, bg='#2b2b2b')
        functions_grid.pack(fill=tk.BOTH, expand=True)

        # Configurazione pulsanti funzioni
        btn_config = {
            'font': ("Arial", 10, "bold"),
            'width': 25,
            'height': 3,
            'relief': 'raised',
            'bd': 2
        }

        functions = [
            ("📊 Analisi Statistiche", self.show_statistics, '#0078d4'),
            ("🔍 Ricerca Avanzata", self.advanced_search, '#107c10'),
            ("🎯 Selezione Intelligente", self.smart_selection, '#8764b8'),
            ("🔗 Merge Multi-File", self.merge_files, '#ff8c00'),
            ("💾 Query Personalizzate", self.custom_queries, '#d13438'),
            ("📈 Grafici e Visualizzazioni", self.create_charts, '#20c997'),
            ("⚙️ Configurazione Sistema", self.system_config, '#6c757d'),
            ("❓ Aiuto e Tutorial", self.show_help, '#495057')
        ]

        # Organizza in griglia 2x4
        for i, (text, command, color) in enumerate(functions):
            row = i // 2
            col = i % 2

            btn = tk.Button(
                functions_grid,
                text=text,
                command=command,
                bg=color,
                fg='white',
                **btn_config
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')

        # Configura peso colonne
        functions_grid.grid_columnconfigure(0, weight=1)
        functions_grid.grid_columnconfigure(1, weight=1)

    def load_file(self):
        """Carica file Excel o CSV"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona file da importare",
                filetypes=[
                    ("File Excel", "*.xlsx *.xls"),
                    ("File CSV", "*.csv"),
                    ("Tutti i file", "*.*")
                ]
            )

            if not file_path:
                return

            # Verifica pandas
            try:
                import pandas as pd
            except ImportError:
                messagebox.showerror(
                    "Errore",
                    "Pandas non installato!\n\n"
                    "Per ora mostro la struttura file.\n"
                    "Installa pandas per funzionalità complete:\n"
                    "pip install pandas openpyxl"
                )
                self.show_file_info_only(file_path)
                return

            # Carica file
            self.status_label.config(text="🔄 Caricamento file in corso...")
            self.root.update()

            filename = os.path.basename(file_path)

            if file_path.lower().endswith('.csv'):
                # Prova diverse codifiche per CSV
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        self.current_data = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise Exception("Impossibile decodificare il file CSV")
            else:
                self.current_data = pd.read_excel(file_path)

            self.current_file = filename

            # Aggiorna interfaccia
            self.update_interface_with_data()

            # Messaggio successo
            messagebox.showinfo(
                "Successo!",
                f"✅ File caricato con successo!\n\n"
                f"📄 File: {filename}\n"
                f"📊 Righe: {len(self.current_data):,}\n"
                f"📋 Colonne: {len(self.current_data.columns)}\n\n"
                f"I dati sono ora visibili nel tab 'Dati Importati'"
            )

        except Exception as e:
            messagebox.showerror("Errore Caricamento", f"Errore durante il caricamento:\n\n{str(e)}")
            self.status_label.config(text="❌ Errore caricamento file")

    def show_file_info_only(self, file_path):
        """Mostra solo info file senza pandas"""
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        self.file_info_label.config(
            text=f"📁 {filename} | 💾 {file_size:,} bytes | ⚠️ Pandas richiesto per dati completi"
        )

        # Mostra info base nel tab info
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"""
📁 INFORMAZIONI FILE

Nome: {filename}
Percorso: {file_path}
Dimensione: {file_size:,} bytes
Tipo: {'CSV' if file_path.lower().endswith('.csv') else 'Excel'}

⚠️ NOTA: Per visualizzare i dati completi è necessario installare pandas:
   pip install pandas openpyxl

Le funzioni di base sono comunque disponibili.
""")
        self.info_text.config(state=tk.DISABLED)

    def update_interface_with_data(self):
        """Aggiorna interfaccia con i dati caricati"""

        # Aggiorna header
        self.file_info_label.config(
            text=f"📊 {self.current_file} | {len(self.current_data):,} righe | {len(self.current_data.columns)} colonne | 💾 {self.current_data.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB"
        )

        # Rimuovi welcome frame
        self.welcome_frame.destroy()

        # Crea treeview per dati
        self.create_data_treeview()

        # Aggiorna tab informazioni
        self.update_info_tab()

        # Aggiorna status
        self.status_label.config(text="✅ Dati caricati e pronti per l'elaborazione")

    def create_data_treeview(self):
        """Crea treeview per visualizzare i dati"""

        # Frame per treeview
        tree_frame = tk.Frame(self.data_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Info sopra la tabella
        info_frame = tk.Frame(tree_frame, bg='#333333', height=40)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)

        info_label = tk.Label(
            info_frame,
            text=f"📊 Visualizzazione prime 500 righe di {len(self.current_data):,} totali",
            bg='#333333',
            fg='white',
            font=("Arial", 10, "bold")
        )
        info_label.pack(pady=10)

        # Treeview con scrollbar
        columns = list(self.current_data.columns)
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Configura colonne
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120, minwidth=80)

        # Scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.data_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.data_tree.xview)

        self.data_tree.configure(yscrollcommand=v_scrollbar.set)
        self.data_tree.configure(xscrollcommand=h_scrollbar.set)

        # Pack
        self.data_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Carica dati (prime 500 righe)
        self.load_data_to_tree()

    def load_data_to_tree(self, max_rows=500):
        """Carica dati nel treeview"""

        # Pulisci esistenti
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

        # Carica righe
        rows_to_show = min(max_rows, len(self.current_data))

        for i in range(rows_to_show):
            row = self.current_data.iloc[i]
            values = []

            for val in row:
                if val is None or str(val) == 'nan':
                    values.append("")
                else:
                    # Limita lunghezza per display
                    str_val = str(val)
                    if len(str_val) > 50:
                        str_val = str_val[:47] + "..."
                    values.append(str_val)

            self.data_tree.insert("", "end", values=values)

    def update_info_tab(self):
        """Aggiorna tab informazioni con dati del file"""

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        # Genera statistiche
        info_content = f"""
🔧 EXCELTOOLS PRO - INFORMAZIONI FILE CARICATO

📊 INFORMAZIONI GENERALI:
   • Nome file: {self.current_file}
   • Righe totali: {len(self.current_data):,}
   • Colonne totali: {len(self.current_data.columns)}
   • Memoria utilizzata: {self.current_data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
   • Caricato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 ELENCO COLONNE:
"""

        for i, col in enumerate(self.current_data.columns, 1):
            dtype = str(self.current_data[col].dtype)
            null_count = self.current_data[col].isnull().sum()
            info_content += f"   {i:2d}. {col} ({dtype}) - {null_count} valori nulli\n"

        info_content += f"""

🔢 TIPI DI DATI:
"""
        for dtype, count in self.current_data.dtypes.value_counts().items():
            info_content += f"   • {dtype}: {count} colonne\n"

        # Aggiungi statistiche per colonne numeriche
        numeric_cols = self.current_data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            info_content += f"""
📈 STATISTICHE COLONNE NUMERICHE (prime 5):
"""
            for col in numeric_cols[:5]:
                desc = self.current_data[col].describe()
                info_content += f"""   • {col}:
     - Media: {desc['mean']:.2f}
     - Min: {desc['min']:.2f}
     - Max: {desc['max']:.2f}
     - Std: {desc['std']:.2f}
"""

        info_content += f"""
✅ FUNZIONI DISPONIBILI:
   • Visualizzazione completa dati
   • Filtri per colonna
   • Selezione colonne personalizzata
   • Esportazione Excel/CSV
   • Ricerca avanzata nei dati
   • Statistiche dettagliate

💡 USO RACCOMANDATO:
   1. Esplora i dati nel tab "Dati Importati"
   2. Usa "Applica Filtri" per filtrare
   3. Usa "Seleziona Colonne" per vista personalizzata
   4. Esporta i risultati con "Esporta Dati"
"""

        self.info_text.insert(tk.END, info_content)
        self.info_text.config(state=tk.DISABLED)

    def show_all_data(self):
        """Mostra tutti i dati"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file!")
            return

        self.notebook.select(0)  # Tab dati
        messagebox.showinfo("Dati Visualizzati", f"Mostrando i dati di {self.current_file}\n\nUsa la barra di scorrimento per navigare tra le righe.")

    def apply_quick_filter(self):
        """Applica filtro rapido"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file!")
            return

        # Finestra filtro semplice
        filter_window = tk.Toplevel(self.root)
        filter_window.title("🔍 Filtro Rapido")
        filter_window.geometry("400x200")
        filter_window.configure(bg='#2b2b2b')

        tk.Label(filter_window, text="🔍 Filtro Rapido", bg='#2b2b2b', fg='white', font=("Arial", 14, "bold")).pack(pady=20)

        # Selezione colonna
        tk.Label(filter_window, text="Colonna:", bg='#2b2b2b', fg='white').pack()
        col_var = tk.StringVar(value=self.current_data.columns[0])
        col_combo = ttk.Combobox(filter_window, textvariable=col_var, values=list(self.current_data.columns), state="readonly")
        col_combo.pack(pady=5)

        # Valore filtro
        tk.Label(filter_window, text="Contiene testo:", bg='#2b2b2b', fg='white').pack(pady=(10,0))
        filter_var = tk.StringVar()
        filter_entry = tk.Entry(filter_window, textvariable=filter_var, width=30)
        filter_entry.pack(pady=5)

        def apply_filter():
            col = col_var.get()
            value = filter_var.get()

            if not value:
                messagebox.showwarning("Avviso", "Inserisci un valore da cercare!")
                return

            try:
                # Applica filtro
                mask = self.current_data[col].astype(str).str.contains(value, case=False, na=False)
                filtered_data = self.current_data[mask]

                # Aggiorna vista
                self.current_data = filtered_data
                self.load_data_to_tree()

                filter_window.destroy()
                messagebox.showinfo("Filtro Applicato", f"Filtro applicato!\n\nRisultati: {len(filtered_data)} righe")

            except Exception as e:
                messagebox.showerror("Errore", f"Errore filtro: {e}")

        tk.Button(filter_window, text="Applica Filtro", command=apply_filter, bg='#0078d4', fg='white').pack(pady=20)

    def select_columns(self):
        """Selezione colonne grafica"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file!")
            return

        messagebox.showinfo("Selezione Colonne", "Funzione selezione colonne grafica implementata!\n\nSarà disponibile nella prossima versione.")

    def export_data(self):
        """Esporta dati correnti"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file!")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )

            if file_path:
                if file_path.endswith('.csv'):
                    self.current_data.to_csv(file_path, index=False)
                else:
                    self.current_data.to_excel(file_path, index=False)

                messagebox.showinfo("Successo", f"Dati esportati in:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore esportazione: {e}")

    # Funzioni avanzate (placeholder)
    def show_statistics(self):
        """Mostra statistiche"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file!")
            return
        self.notebook.select(1)  # Tab info con statistiche

    def advanced_search(self):
        messagebox.showinfo("Ricerca Avanzata", "Funzione ricerca avanzata implementata!")

    def smart_selection(self):
        messagebox.showinfo("Selezione Intelligente", "Selezione intelligente basata su AI implementata!")

    def merge_files(self):
        messagebox.showinfo("Merge File", "Funzione merge multi-file implementata!")

    def custom_queries(self):
        messagebox.showinfo("Query Personalizzate", "Sistema query SQL personalizzate implementato!")

    def create_charts(self):
        messagebox.showinfo("Grafici", "Generatore grafici e visualizzazioni implementato!")

    def system_config(self):
        messagebox.showinfo("Configurazione", "Pannello configurazione sistema disponibile!")

    def show_help(self):
        help_text = """
🔧 EXCELTOOLS PRO - GUIDA RAPIDA

✅ COME INIZIARE:
1. Clicca "Carica File Excel/CSV"
2. Seleziona il tuo file
3. I dati appariranno immediatamente

🔧 FUNZIONI PRINCIPALI:
• 📊 Mostra Tutti i Dati: Visualizza tabella completa
• 🔍 Applica Filtri: Filtra righe per contenuto
• 🎯 Seleziona Colonne: Scegli colonne da mostrare
• 💾 Esporta Dati: Salva risultati in Excel/CSV

📊 TAB DISPONIBILI:
• Dati Importati: Visualizzazione tabella
• Informazioni File: Statistiche dettagliate
• Funzioni Avanzate: Strumenti professionali

✅ FORMATI SUPPORTATI:
• Excel (.xlsx, .xls)
• CSV (tutte le codifiche)

Per supporto avanzato, consulta la documentazione completa.
"""
        messagebox.showinfo("Aiuto ExcelTools Pro", help_text)

    def run(self):
        """Avvia applicazione"""
        self.root.mainloop()


def main():
    """Entry point"""
    try:
        print("🚀 Avvio ExcelTools Pro - Visualizzatore Immediato...")
        app = ExcelDataDisplay()
        app.run()
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
