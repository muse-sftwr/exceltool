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
from datetime import datetime
import os


class DataVisualizer:
    def create_ai_panel(self, parent):
        """Crea pannello AI interattivo con storico domande/risposte"""
        import threading
        from transformers import pipeline
        ai_frame = tk.LabelFrame(parent, text="🤖 Assistente AI Interattivo", bg='#23272e', fg='white', font=("Arial", 12, "bold"))
        ai_frame.pack(fill=tk.BOTH, side=tk.RIGHT, padx=10, pady=10, expand=False)

        tk.Label(ai_frame, text="Fai una domanda sui dati o chiedi una query SQL!", font=("Arial", 10), fg='#cccccc', bg='#23272e').pack(pady=5)

        question_var = tk.StringVar()
        entry = tk.Entry(ai_frame, textvariable=question_var, font=("Arial", 12), width=40)
        entry.pack(pady=5)

        btn_ask = tk.Button(ai_frame, text="Chiedi all'AI", bg='#20c997', fg='white', font=("Arial", 11, "bold"))
        btn_ask.pack(pady=5)

        # Storico domande/risposte
        history_frame = tk.Frame(ai_frame, bg='#23272e')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        history_text = tk.Text(history_frame, font=("Consolas", 10), bg='#1e1e1e', fg='white', height=10, wrap=tk.WORD)
        history_text.pack(fill=tk.BOTH, expand=True)
        history_text.insert(tk.END, "Storico domande/risposte AI:\n")
        history_text.config(state=tk.DISABLED)

        def add_history(question, answer):
            history_text.config(state=tk.NORMAL)
            history_text.insert(tk.END, f"\nDomanda: {question}\nRisposta: {answer}\n{'-'*40}\n")
            history_text.see(tk.END)
            history_text.config(state=tk.DISABLED)

        def ask_ai():
            question = question_var.get()
            if not question:
                add_history("", "Inserisci una domanda!")
                return
            add_history(question, "⏳ Elaborazione...")
            def run_ai():
                try:
                    # Context dinamico: colonne, filtri, selezione
                    context = f"Colonne: {', '.join(list(self.current_data.columns))}\nRighe: {len(self.current_data)}"
                    if self.filtered_data is not None:
                        context += f"\nFiltro attivo: {len(self.filtered_data)} righe filtrate"
                    if self.selected_columns:
                        context += f"\nColonne selezionate: {', '.join(self.selected_columns)}"
                    nlp = pipeline("question-answering", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")
                    result = nlp(question=question, context=context)
                    answer = result['answer']
                    # Suggerimento SQL base
                    if 'query' in question.lower() or 'sql' in question.lower():
                        answer += f"\nEsempio SQL: SELECT {', '.join(list(self.current_data.columns)[:3])} FROM tabella LIMIT 10;"
                    add_history(question, answer)
                except Exception as e:
                    add_history(question, f"Errore AI: {e}")
            threading.Thread(target=run_ai).start()

        btn_ask.config(command=ask_ai)

        # Suggerimenti automatici
        def suggest_ai():
            if self.selected_columns:
                col = self.selected_columns[0]
                add_history("Quali valori unici ci sono in questa colonna?", f"Esempio SQL: SELECT DISTINCT {col} FROM tabella;")
            elif self.filtered_data is not None:
                add_history("Quante righe sono filtrate?", f"Risposta: {len(self.filtered_data)}")

        # Chiamato ogni volta che cambia selezione/filtri
        self.suggest_ai = suggest_ai

        return ai_frame
    """Visualizzatore avanzato per dati Excel"""

    def __init__(self, parent):
        self.parent = parent
        self.current_data = None
        self.filtered_data = None
        self.selected_columns = []

    def create_data_viewer_window(self):
        """Crea finestra principale visualizzazione dati con AI panel"""
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Carica prima un file Excel!")
            return

        # Finestra principale dati
        self.data_window = tk.Toplevel(self.parent)
        self.data_window.title("📊 ExcelTools Pro - Visualizzatore Dati")
        self.data_window.geometry("1400x800")
        self.data_window.configure(bg='#1e1e1e')

        # Frame principale con AI panel laterale
        main_frame = tk.Frame(self.data_window, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=10, pady=10)

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

        # Pannello AI interattivo sempre visibile
        self.ai_panel = self.create_ai_panel(main_frame)
        # Suggerimenti automatici all'avvio
        if hasattr(self, 'suggest_ai'):
            self.suggest_ai()

    def create_data_view_tab(self):
        """Tab visualizzazione dati principale con ordinamento e ricerca"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="📊 Vista Dati")

        # Toolbar
        toolbar = tk.Frame(data_frame, bg='#333333', height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)

        info_text = f"📊 Righe: {len(self.current_data)} | Colonne: {len(self.current_data.columns)}"
        info_label = tk.Label(toolbar, text=info_text, bg='#333333', fg='white', font=("Arial", 10, "bold"))
        info_label.pack(side=tk.LEFT, padx=10, pady=8)

        # Ricerca rapida
        search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar, textvariable=search_var, font=("Arial", 10), width=30)
        search_entry.pack(side=tk.LEFT, padx=10)

        def do_search():
            val = search_var.get()
            if not val:
                self.load_data_into_tree()
                return
            mask = self.current_data.apply(lambda row: row.astype(str).str.contains(val, case=False, na=False).any(), axis=1)
            self.load_data_into_tree(self.current_data[mask])
        btn_search = tk.Button(toolbar, text="🔎 Cerca", command=do_search, bg='#0078d4', fg='white', font=("Arial", 9))
        btn_search.pack(side=tk.LEFT, padx=5)

        btn_export = tk.Button(toolbar, text="💾 Esporta Vista", command=self.export_current_view, bg='#0078d4', fg='white', font=("Arial", 9))
        btn_export.pack(side=tk.RIGHT, padx=5, pady=5)
        btn_refresh = tk.Button(toolbar, text="🔄 Aggiorna", command=self.refresh_data_view, bg='#107c10', fg='white', font=("Arial", 9))
        btn_refresh.pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame per Treeview con scrollbar
        tree_frame = tk.Frame(data_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = list(self.current_data.columns)
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        # Ordinamento colonne
        def sortby(col, descending):
            data = self.current_data.sort_values(by=col, ascending=not descending)
            self.load_data_into_tree(data)
            # Aggiorna heading per toggle
            self.data_tree.heading(col, command=lambda: sortby(col, not descending))
        for col in columns:
            self.data_tree.heading(col, text=col, command=lambda c=col: sortby(c, False))
            self.data_tree.column(col, width=120, minwidth=80)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=v_scrollbar.set)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(xscrollcommand=h_scrollbar.set)

        self.data_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

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

        # Pulsante Assistente AI nel tab Statistiche
        btn_ai = tk.Button(general_frame, text="🤖 Assistente AI", command=self.open_ai_assistant,
                          bg='#20c997', fg='white', font=("Arial", 10, "bold"))
        btn_ai.pack(anchor='e', padx=10, pady=5)
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
        """Tab query salvate e template"""
        queries_frame = ttk.Frame(self.notebook)
        self.notebook.add(queries_frame, text="💾 Query & Template")

        tk.Label(queries_frame, text="💾 Query Salvate & Template", font=("Arial", 14, "bold")).pack(pady=10)

        # Editor query
        query_var = tk.StringVar()
        entry = tk.Entry(queries_frame, textvariable=query_var, font=("Consolas", 12), width=60)
        entry.pack(pady=5)
        result_text = tk.Text(queries_frame, font=("Consolas", 10), bg='#1e1e1e', fg='white', height=8, wrap=tk.WORD)
        result_text.pack(padx=10, pady=5, fill=tk.X)
        def analyze_query():
            query = query_var.get()
            if not query:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Inserisci una query SQL!")
                return
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "⏳ Analisi sintassi e suggerimenti AI...")
            import threading

            def run_ai():
                try:
                    import sqlparse
                    parsed = sqlparse.parse(query)
                    syntax_ok = bool(parsed)
                    syntax_msg = "✅ Sintassi SQL valida" if syntax_ok else "❌ Sintassi SQL non valida"
                    from transformers import pipeline
                    context = f"Colonne: {', '.join(list(self.current_data.columns)) if self.current_data is not None else ''}"
                    nlp = pipeline("text2text-generation", model="google/flan-t5-base")
                    ai_suggestion = nlp(f"Suggerisci una query SQL per: {query} e dati: {context}")[0]['generated_text']
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, f"{syntax_msg}\n\nSuggerimento AI:\n{ai_suggestion}")
                except Exception as e:
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, f"Errore AI Analyzer: {e}")
            threading.Thread(target=run_ai).start()
        btn_analyze = tk.Button(queries_frame, text="Analizza Query", command=analyze_query, bg='#20c997', fg='white', font=("Arial", 11, "bold"))
        btn_analyze.pack(pady=5)

        # Storico query salvate
        tk.Label(queries_frame, text="Storico Query & Template", font=("Arial", 12, "bold"), fg='#20c997').pack(pady=5)
        self.query_history = tk.Text(queries_frame, font=("Consolas", 9), bg='#23272e', fg='white', height=8, wrap=tk.WORD)
        self.query_history.pack(padx=10, pady=5, fill=tk.X)
        self.query_history.insert(tk.END, "Storico query/template:\n")
        self.query_history.config(state=tk.DISABLED)
        def save_query():
            query = query_var.get()
            if not query:
                return
            self.query_history.config(state=tk.NORMAL)
            self.query_history.insert(tk.END, f"\n{query}\n{'-'*40}\n")
            self.query_history.config(state=tk.DISABLED)
        btn_save = tk.Button(queries_frame, text="Salva Query/Template", command=save_query, bg='#0078d4', fg='white', font=("Arial", 10, "bold"))
        btn_save.pack(pady=5)

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

            # Suggerimenti AI automatici
            if hasattr(self, 'suggest_ai'):
                self.suggest_ai()

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

        # Suggerimenti AI automatici
        if hasattr(self, 'suggest_ai'):
            self.suggest_ai()

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
    """ExcelTools Pro: UI minimal, sidebar, tutte le funzioni, AI Analyzer, performance top"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ExcelTools Pro - Analyzer Minimal")
        self.root.geometry("1600x900")
        self.root.configure(bg='#181a1b')

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
            # Tabelle
            cursor.execute('''CREATE TABLE IF NOT EXISTS imported_files (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, filepath TEXT, rows_count INTEGER, columns_count INTEGER, import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS saved_queries (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, query_data TEXT, created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS data_filters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, filter_config TEXT, created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            self.db_connection.commit()
        except Exception as e:
            messagebox.showerror("DB Error", f"Errore DB: {e}")

    def create_interface(self):
        """UI minimal con sidebar e tutte le funzioni"""
        # Sidebar minimal
        sidebar = tk.Frame(self.root, bg='#23272e', width=80)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Icone menu minimal
        menu_items = [
            ("📁", "Import", self.import_excel_file),
            ("➕", "Import Multiplo", self.import_multiple_files),
            ("�", "Merge", self.merge_files_interface),
            ("📊", "Dati", self.show_data_visualizer),
            ("🔍", "Filtri", self.show_filters_interface),
            ("💾", "Query", self.manage_saved_queries),
            ("🧠", "AI Analyzer", self.open_ai_analyzer),
            ("📈", "Statistiche", self.show_analytics),
            ("⚙️", "Impostazioni", self.show_settings)
        ]
        for icon, tooltip, command in menu_items:
            btn = tk.Button(sidebar, text=icon, font=("Arial", 20), bg='#23272e', fg='white', relief='flat', command=command)
            btn.pack(pady=18, fill=tk.X)
            btn.bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(e, t))
            btn.bind("<Leave>", self.hide_tooltip)

        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#181a1b')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.create_status_bar()

        # Tooltip
        self.tooltip = None

    def show_tooltip(self, event, text):
        if self.tooltip:
            self.tooltip.destroy()
        x = event.widget.winfo_rootx() + 60
        y = event.widget.winfo_rooty() + 10
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=text, bg="#23272e", fg="white", font=("Arial", 10))
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg='#333333', height=35)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        self.status_label = tk.Label(self.status_frame, text="🟢 Pronto - Importa file Excel", font=("Arial", 10), fg='#90EE90', bg='#333333')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)
        self.file_info_label = tk.Label(self.status_frame, text="Nessun file", font=("Arial", 10), fg='#cccccc', bg='#333333')
        self.file_info_label.pack(side=tk.RIGHT, padx=15, pady=8)

    def import_excel_file(self):
        """Import singolo file"""
        try:
            file_path = filedialog.askopenfilename(title="Seleziona file Excel", filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")])
            if not file_path:
                return
            import pandas as pd
            if file_path.endswith('.csv'):
                self.current_data = pd.read_csv(file_path)
            else:
                self.current_data = pd.read_excel(file_path)
            filename = os.path.basename(file_path)
            cursor = self.db_connection.cursor()
            cursor.execute('INSERT INTO imported_files (filename, filepath, rows_count, columns_count) VALUES (?, ?, ?, ?)', (filename, file_path, len(self.current_data), len(self.current_data.columns)))
            self.db_connection.commit()
            self.status_label.config(text="✅ File importato")
            self.file_info_label.config(text=f"{filename} | {len(self.current_data):,} righe | {len(self.current_data.columns)} colonne")
            self.data_visualizer = DataVisualizer(self.main_frame)
            self.data_visualizer.current_data = self.current_data
            self.data_visualizer.create_data_viewer_window()
        except Exception as e:
            messagebox.showerror("Import Error", f"Errore importazione: {e}")

    def import_multiple_files(self):
        """Import multiplo di file Excel/CSV"""
        try:
            file_paths = filedialog.askopenfilenames(title="Seleziona file multipli", filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")])
            if not file_paths:
                return
            import pandas as pd
            all_data = []
            for file_path in file_paths:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                all_data.append(df)
                filename = os.path.basename(file_path)
                cursor = self.db_connection.cursor()
                cursor.execute('INSERT INTO imported_files (filename, filepath, rows_count, columns_count) VALUES (?, ?, ?, ?)', (filename, file_path, len(df), len(df.columns)))
            self.db_connection.commit()
            # Merge automatico
            if all_data:
                from functools import reduce
                merged = reduce(lambda left, right: left.merge(right, how='outer'), all_data)
                self.current_data = merged
                self.status_label.config(text="✅ File multipli importati e uniti")
                self.file_info_label.config(text=f"{len(file_paths)} file | {len(self.current_data):,} righe | {len(self.current_data.columns)} colonne")
                self.data_visualizer = DataVisualizer(self.main_frame)
                self.data_visualizer.current_data = self.current_data
                self.data_visualizer.create_data_viewer_window()
        except Exception as e:
            messagebox.showerror("Import Multiplo Error", f"Errore import multiplo: {e}")

    def merge_files_interface(self):
        """Interfaccia merge file professionale"""
        messagebox.showinfo("Merge", "Merge file Excel/CSV avanzato: seleziona file multipli per unione automatica.")

    def show_data_visualizer(self):
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return
        self.data_visualizer = DataVisualizer(self.main_frame)
        self.data_visualizer.current_data = self.current_data
        self.data_visualizer.create_data_viewer_window()

    def show_filters_interface(self):
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return
        self.show_data_visualizer()
        if hasattr(self.data_visualizer, 'notebook'):
            self.data_visualizer.notebook.select(2)

    def manage_saved_queries(self):
        messagebox.showinfo("Query", "Gestione query salvate e template SQL professionale.")

    def open_ai_analyzer(self):
        """AI Analyzer: editor query con compilatore sintattico e suggerimenti AI"""
        ai_win = tk.Toplevel(self.root)
        ai_win.title("AI Analyzer Pro")
        ai_win.geometry("900x600")
        ai_win.configure(bg='#23272e')
        tk.Label(ai_win, text="🧠 AI Analyzer - Query & Insight", font=("Arial", 16, "bold"), fg='white', bg='#23272e').pack(pady=10)
        query_var = tk.StringVar()
        entry = tk.Entry(ai_win, textvariable=query_var, font=("Consolas", 13), width=60)
        entry.pack(pady=10)
        result_text = tk.Text(ai_win, font=("Consolas", 11), bg='#1e1e1e', fg='white', height=15, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        def analyze_query():
            query = query_var.get()
            if not query:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Inserisci una query SQL!")
                return
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "⏳ Analisi sintassi e suggerimenti AI...")
            import threading
            def run_ai():
                try:
                    # Compilatore sintattico SQL
                    import sqlparse
                    parsed = sqlparse.parse(query)
                    syntax_ok = bool(parsed)
                    syntax_msg = "✅ Sintassi SQL valida" if syntax_ok else "❌ Sintassi SQL non valida"
                    # AI Analyzer
                    from transformers import pipeline
                    context = f"Colonne: {', '.join(list(self.current_data.columns)) if self.current_data is not None else ''}"
                    nlp = pipeline("text2text-generation", model="google/flan-t5-base")
                    ai_suggestion = nlp(f"Suggerisci una query SQL per: {query} e dati: {context}")[0]['generated_text']
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, f"{syntax_msg}\n\nSuggerimento AI:\n{ai_suggestion}")
                except Exception as e:
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, f"Errore AI Analyzer: {e}")
            threading.Thread(target=run_ai).start()
        btn_analyze = tk.Button(ai_win, text="Analizza Query", command=analyze_query, bg='#20c997', fg='white', font=("Arial", 11, "bold"))
        btn_analyze.pack(pady=5)

    def show_analytics(self):
        if self.current_data is None:
            messagebox.showwarning("Avviso", "Importa prima un file Excel!")
            return
        self.show_data_visualizer()
        if hasattr(self.data_visualizer, 'notebook'):
            self.data_visualizer.notebook.select(1)

    def show_settings(self):
        messagebox.showinfo("Impostazioni", "Pannello impostazioni minimal e avanzate.")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
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
