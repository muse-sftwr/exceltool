import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import re
from excel_logic import ExcelManager
from ai_query_engine import AIQueryEngine


class ExcelToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ExcelTools - AI Powered")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.excel_manager = ExcelManager()
        self.ai_engine = AIQueryEngine()
        self.df = None
        self.filtered_df = None
        self.file_path = None
        self.last_query = None
        self.last_sql = None
        self.last_error = None
        self.last_shown_cols = None

        self._setup_ui()
        self._reset_state()

    def _setup_ui(self):
        # Minimal UI for demonstration; expand as needed
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.query_entry = ctk.CTkEntry(self.frame, width=600)
        self.query_entry.pack(pady=10)
        self.load_btn = ctk.CTkButton(
            self.frame, text="Carica Excel",
            command=self.load_excel
        )
        self.load_btn.pack(pady=5)
        self.query_btn = ctk.CTkButton(
            self.frame, text="Esegui Query AI",
            command=self.run_query
        )
        self.query_btn.pack(pady=5)
        self.export_btn = ctk.CTkButton(
            self.frame, text="Esporta Excel",
            command=self.export_excel
        )
        self.export_btn.pack(pady=5)
        self.status_label = ctk.CTkLabel(self.frame, text="Pronto")
        self.status_label.pack(pady=5)

    def _reset_state(self):
        self.df = None
        self.filtered_df = None
        self.file_path = None
        self.last_query = None
        self.last_sql = None
        self.last_error = None
        self.last_shown_cols = None

    def load_excel(self):
        filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
        )


def main():
    root = ctk.CTk()
    ExcelToolsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

    def apply_filters(self):
        if self.data is None:
            return
        df = self.data.copy()
        for col_var, op_var, val_var, _ in self.filters:
            col, op, val = col_var.get(), op_var.get(), val_var.get()
            try:
                if op == "=":
                    df = df[df[col] == self._parse_value(df, col, val)]
                elif op == "!=":
                    df = df[df[col] != self._parse_value(df, col, val)]
                elif op == ">":
                    df = df[df[col] > self._parse_value(df, col, val)]
                elif op == "<":
                    df = df[df[col] < self._parse_value(df, col, val)]
                elif op == ">=":
                    df = df[df[col] >= self._parse_value(df, col, val)]
                elif op == "<=":
                    df = df[df[col] <= self._parse_value(df, col, val)]
                elif op == "contiene":
                    df = df[df[col].astype(str).str.contains(
                        val, case=False, na=False
                    )]
                elif op == "non contiene":
                    df = df[~df[col].astype(str).str.contains(
                        val, case=False, na=False
                    )]
                elif op == "è nullo":
                    df = df[df[col].isnull()]
                elif op == "non nullo":
                    df = df[~df[col].isnull()]
                elif op == "in intervallo":
                    rng = [
                        float(x) for x in re.split(r'[-,; ]', val) if x.strip()
                    ]
                    if len(rng) == 2:
                        df = df[(df[col] >= min(rng)) & (df[col] <= max(rng))]
            except Exception:
                continue
        self.filtered_data = df
        self.show_table(self.filtered_data)
        self.status.configure(text=f"Filtri applicati: {len(self.filters)}")
        # Cronologia filtri
        self.filter_history.append([
            (f[0].get(), f[1].get(), f[2].get()) for f in self.filters
        ])

    def show_history(self):
        win = tk.Toplevel(self)
        win.title("Cronologia Query e Filtri")
        win.geometry("600x400")
        txt = tk.Text(win, wrap="word")
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", "--- Query AI ---\n")
        for q in self.query_history:
            txt.insert("end", q+"\n")
        txt.insert("end", "\n--- Filtri ---\n")
        for fset in self.filter_history:
            txt.insert("end", str(fset)+"\n")

    def save_layout(self):
        import json
        layout = {
            "current_table": self.current_table,
            "filters": [
                (f[0].get(), f[1].get(), f[2].get()) for f in self.filters
            ],
            "theme": self.theme,
            "columns": list(self.filtered_data.columns)
            if self.filtered_data is not None else [],
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(layout, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(
                "Salva Layout", f"Layout salvato in {file_path}"
            )
            self.status.configure(text="Layout salvato")
        except Exception as e:
            messagebox.showerror("Errore salvataggio layout", str(e))
            self.status.configure(text="Errore salvataggio layout")

    def save_view(self):
        if self.filtered_data is None or self.filtered_data.empty:
            messagebox.showinfo("Salva vista", "Nessun dato da salvare.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return
        try:
            if file_path.endswith(".csv"):
                self.filtered_data.to_csv(file_path, index=False)
            else:
                self.filtered_data.to_excel(file_path, index=False)
            messagebox.showinfo("Salva vista", f"Vista salvata in {file_path}")
            self.status.configure(text="Vista salvata")
        except Exception as e:
            messagebox.showerror("Errore salvataggio", str(e))
            self.status.configure(text="Errore salvataggio")

    def _parse_value(self, df, col, val):
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            try:
                return float(val)
            except Exception:
                return 0
        return val

    def reset_filters(self):
        for _, _, _, row in self.filters:
            row.destroy()
        self.filters = []
        if self.data is not None:
            self.filtered_data = self.data.copy()
            self.show_table(self.filtered_data)
        self.status.configure(text="Filtri resettati")

    def show_stats(self):
        if self.filtered_data is None or self.filtered_data.empty:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "-- Nessun dato per statistiche.")
            self.status.configure(text="Nessun dato per statistiche")
            return
        df = self.filtered_data
        stats = [
            f"Righe: {len(df)}",
            f"Colonne: {len(df.columns)}",
            f"Colonne: {', '.join(df.columns)}",
            f"Tipi: {', '.join(str(df[c].dtype) for c in df.columns)}",
            f"Nulli: {df.isnull().sum().sum()} "
            f"({df.isnull().sum().to_dict()})",
            f"Unici: {{ "
            f"{', '.join(f'{c}: {df[c].nunique()}' for c in df.columns)} }}",
            f"Descrittive:\n{df.describe(include='all').to_string()}"
        ]
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(stats))
        self.status.configure(text="Statistiche mostrate")

    def toggle_theme(self):
        if self.theme == "system":
            ctk.set_appearance_mode("dark")
            self.theme = "dark"
        elif self.theme == "dark":
            ctk.set_appearance_mode("light")
            self.theme = "light"
        else:
            ctk.set_appearance_mode("system")
            self.theme = "system"

    def bind_shortcuts(self):
        self.bind("<Control-o>", lambda e: self.load_excel())
        self.bind("<Control-s>", lambda e: self.export_data("excel"))
        self.bind("<Control-q>", lambda e: self.run_query())
        self.bind("<Control-f>", lambda e: self.add_filter())
        self.bind("<Control-r>", lambda e: self.reset_filters())
        self.bind("<Control-t>", lambda e: self.toggle_theme())


if __name__ == "__main__":
    app = ExcelToolsApp()
    app.mainloop()
