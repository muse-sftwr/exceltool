#!/usr/bin/env python3
# cSpell:disable

"""

ExcelTools - Versione semplificata per test

"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

import threading

import os


class SimpleExcelTool:

    def __init__(self):
        self.setup_gui()
        self.current_data = None

    def setup_gui(self):
        """Inizializza l'interfaccia grafica semplice"""
        self.root = tk.Tk()
        self.root.title("ExcelTools - Test Version")
        self.root.geometry("800x600")

        # Frame principale
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bottoni di controllo
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Carica File Excel",
            command=self.load_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Mostra Statistiche",
            command=self.show_stats).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Esporta Excel",
            command=self.export_file).pack(side="left", padx=5)

        # Area di visualizzazione
        self.text_area = tk.Text(main_frame, height=30, width=100)
        self.text_area.pack(fill="both", expand=True, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_area.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")


    def load_file(self):
        """Carica un file Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
                filetypes=[
                    ("Excel files",
                        "*.xlsx *.xls"),
                        ("All files",
                        "*.*")
                ]
        )

        if file_path:

            def load_worker():
                try:
                    self.status_var.set("Caricamento in corso...")

                    # Carica il file Excel
                    df = pd.read_excel(file_path, engine='openpyxl')
                    self.current_data = df

                    # Mostra informazioni nel text area
                    info_text = f"File caricato: {
                        os.path.basename(file_path)}\n"
                    info_text += f"Righe: {len(df):}\n"
                    info_text += f"Colonne: {len(df.columns)}\n\n"
                    info_text += "Prime 10 righe:\n"
                    info_text += str(df.head(10))
                    info_text += "\n\nColonne disponibili:\n"
                    info_text += str(list(df.columns))

                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, info_text)

                    self.status_var.set(f"File caricato: {len(df)} righe")

                except Exception as e:
                    messagebox.showerror(
                        "Errore", f"Errore nel caricamento: {str(e)}")
                    self.status_var.set("Errore nel caricamento")

            threading.Thread(target=load_worker, daemon=True).start()


    def show_stats(self):
        """Mostra statistiche del dataset"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Carica prima un file Excel")
            return

        df = self.current_data

        stats_text = "=== STATISTICHE DATASET ===\n\n"
        stats_text += f"Dimensioni: {
            df.shape[0]} righe x {
                df.shape[1]} colonne\n"
        stats_text += f"Memoria utilizzata: {
            df.memory_usage(
                deep=True).sum() /
            1024 /
            1024:.2f} MB\n\n"

        stats_text += "Informazioni colonne:\n"
        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            stats_text += f"- {col}: {dtype}, Nulli: {null_count}, Unici: \
                {unique_count}\n"

        stats_text += "\nStatistiche numeriche:\n"
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats_text += str(df[numeric_cols].describe())

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, stats_text)

        self.status_var.set("Statistiche calcolate")


    def export_file(self):
        """Esporta i dati in un nuovo file Excel"""
        if self.current_data is None:
            messagebox.showwarning("Attenzione", "Carica prima un file Excel")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salva file Excel",
                defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if file_path:
            try:
                self.status_var.set("Esportazione in corso...")
                self.current_data.to_excel(
                    file_path, index=False, engine='openpyxl')
                self.status_var.set(
                    f"File esportato: {os.path.basename(file_path)}")
                messagebox.showinfo(
                    "Successo", f"File esportato con successo:\n{file_path}")
            except Exception as e:
                messagebox.showerror(
                    "Errore", f"Errore nell'esportazione: {str(e)}")
                self.status_var.set("Errore nell'esportazione")


    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    app = SimpleExcelTool()
    app.run()


if __name__ == "__main__":
    main()
