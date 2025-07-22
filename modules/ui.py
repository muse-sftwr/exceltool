"""
Modulo UI: componenti CustomTkinter per ExcelTools,
inclusi filtri rapidi, query, AI, gestione DataFrame.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class ExcelToolsUI(ctk.CTkFrame):
    def __init__(self, master, excel_handler, query_handler, ai_query_engine):
        super().__init__(master)
        self.excel_handler = excel_handler
        self.query_handler = query_handler
        self.ai_query_engine = ai_query_engine
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # File controls
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkButton(
            file_frame, text='Importa Excel', command=self.import_excel
        ).pack(side='left', padx=5)
        ctk.CTkButton(
            file_frame, text='Salva Excel', command=self.save_excel
        ).pack(side='left', padx=5)
        ctk.CTkButton(
            file_frame, text='Gestione Filtri', command=self.open_filter_dialog
        ).pack(side='left', padx=5)
        ctk.CTkButton(
            file_frame, text='Reset Filtri', command=self.reset_filters
        ).pack(side='left', padx=5)
        self.filter_counter = ctk.CTkLabel(file_frame, text='Filtri attivi: 0')
        self.filter_counter.pack(side='left', padx=10)

        # Query controls
        query_frame = ctk.CTkFrame(self)
        query_frame.pack(fill='x', padx=10, pady=5)
        self.query_entry = ctk.CTkEntry(query_frame, width=400)
        self.query_entry.pack(side='left', padx=5)
        ctk.CTkButton(
            query_frame, text='Esegui Query SQL', command=self.run_query
        ).pack(side='left', padx=5)
        ctk.CTkButton(
            query_frame, text='Esegui Query AI', command=self.run_ai_query
        ).pack(side='left', padx=5)
        self.sql_label = ctk.CTkLabel(query_frame, text='')
        self.sql_label.pack(side='left', padx=10)

        # Data table
        self.tree = ttk.Treeview(self, show='headings')
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

    def import_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Excel Files', '*.xlsx *.xls')]
        )
        if file_path:
            self.excel_handler.load_excel(file_path)
            self.update_table(self.excel_handler.df)
            self.update_filter_counter()

    def save_excel(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel Files', '*.xlsx *.xls')]
        )
        if file_path:
            self.excel_handler.save_excel(file_path)
            messagebox.showinfo('Salvataggio', 'File salvato correttamente.')

    def run_query(self):
        query = self.query_entry.get()
        result, error = self.query_handler.run_query(query)
        if error:
            messagebox.showerror('Errore Query', error)
        else:
            self.update_table(result)
            self.sql_label.configure(text='')

    def run_ai_query(self):
        user_query = self.query_entry.get()
        sql, result, error = self.ai_query_engine.run_ai_query(user_query)
        self.sql_label.configure(text=sql)
        if error:
            messagebox.showerror('Errore Query AI', error)
        else:
            self.update_table(result)

    def update_table(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        for _, row in df.iterrows():
            self.tree.insert('', 'end', values=list(row))

    def open_filter_dialog(self):
        FilterDialog(self, self.excel_handler)
        self.update_table(self.excel_handler.filtered_df)
        self.update_filter_counter()

    def reset_filters(self):
        self.excel_handler.clear_filters()
        self.update_table(self.excel_handler.df)
        self.update_filter_counter()

    def update_filter_counter(self):
        n = len(self.excel_handler.filters)
        self.filter_counter.configure(text=f'Filtri attivi: {n}')


class FilterDialog(ctk.CTkToplevel):
    def __init__(self, parent, excel_handler):
        super().__init__(parent)
        self.title('Gestione Filtri')
        self.excel_handler = excel_handler
        self.geometry('400x300')
        self.create_widgets()

    def create_widgets(self):
        cols = (
            self.excel_handler.df.columns
            if self.excel_handler.df is not None else []
        )
        self.col_var = tk.StringVar()
        self.op_var = tk.StringVar()
        self.val_var = tk.StringVar()
        ctk.CTkLabel(self, text='Colonna').pack(pady=5)
        col_menu = ctk.CTkOptionMenu(
            self, variable=self.col_var, values=list(cols)
        )
        col_menu.pack(pady=5)
        ctk.CTkLabel(self, text='Operatore').pack(pady=5)
        op_menu = ctk.CTkOptionMenu(
            self, variable=self.op_var,
            values=[
                '=', '!=', '>', '<', '>=', '<=',
                'contiene', 'non contiene'
            ]
        )
        op_menu.pack(pady=5)
        ctk.CTkLabel(self, text='Valore').pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.val_var).pack(pady=5)
        ctk.CTkButton(
            self, text='Aggiungi Filtro', command=self.add_filter
        ).pack(pady=10)
        ctk.CTkButton(
            self, text='Rimuovi Ultimo Filtro', command=self.remove_last_filter
        ).pack(pady=5)
        ctk.CTkButton(self, text='Chiudi', command=self.destroy).pack(pady=10)

    def add_filter(self):
        col = self.col_var.get()
        op = self.op_var.get()
        val = self.val_var.get()
        if col and op and val:
            self.excel_handler.filters.append((col, op, val))
            self.excel_handler.apply_filters(self.excel_handler.filters)

    def remove_last_filter(self):
        if self.excel_handler.filters:
            self.excel_handler.filters.pop()
            self.excel_handler.apply_filters(self.excel_handler.filters)
