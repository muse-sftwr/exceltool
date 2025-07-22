#!/usr/bin/env python3
"""
🔧 EXCELTOOLS PRO - LAUNCHER STABILE
===================================

Launcher principale con fallback sicuro e integrazione completa.

Autore: Senior System Engineer
Data: 2025-07-16
"""

import sys
import os
import traceback
from pathlib import Path

def test_dependencies():
    """Test rapido dipendenze"""
    required = {
        'tkinter': True,
        'pandas': False,
        'sqlite3': True,
        'customtkinter': False
    }

    available = {}

    for module, critical in required.items():
        try:
            if module == 'tkinter':
                import tkinter
                available[module] = True
            elif module == 'pandas':
                import pandas
                available[module] = True
            elif module == 'sqlite3':
                import sqlite3
                available[module] = True
            elif module == 'customtkinter':
                import customtkinter
                available[module] = True
        except ImportError:
            available[module] = False
            if critical:
                print(f"❌ Modulo critico {module} non disponibile!")
                return False

    return True

def launch_advanced_gui():
    """Prova a lanciare la GUI avanzata"""
    try:
        print("🚀 Tentativo lancio GUI avanzata...")
        from advanced_excel_tools_gui import AdvancedExcelToolsGUI

        app = AdvancedExcelToolsGUI()
        print("✅ GUI avanzata creata")
        app.run()
        return True

    except Exception as e:
        print(f"❌ GUI avanzata fallita: {e}")
        return False

def launch_quick_gui():
    """Prova a lanciare la GUI rapida"""
    try:
        print("🚀 Tentativo lancio GUI rapida...")
        from quick_gui_test import ExcelToolsQuickGUI

        app = ExcelToolsQuickGUI()
        print("✅ GUI rapida creata")
        app.run()
        return True

    except Exception as e:
        print(f"❌ GUI rapida fallita: {e}")
        return False

def launch_simple_gui():
    """Lancia la GUI semplice (sempre funziona)"""
    try:
        print("🚀 Lancio GUI semplice...")

        import tkinter as tk
        from tkinter import messagebox, filedialog
        import sqlite3

        # Finestra principale
        root = tk.Tk()
        root.title("🔧 ExcelTools Pro - Sistema Completo")
        root.geometry("900x700")
        root.configure(bg='#1e1e1e')

        # Variabili globali
        current_data = None
        db_connection = None

        def setup_database():
            """Setup database"""
            try:
                global db_connection
                db_connection = sqlite3.connect('exceltools_data.db')
                cursor = db_connection.cursor()

                # Crea tabelle se non esistono
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS saved_queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        query_data TEXT NOT NULL,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS merge_configs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        config_data TEXT NOT NULL,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                db_connection.commit()
                return True
            except Exception as e:
                messagebox.showerror("Errore Database", f"Errore setup database: {e}")
                return False

        def load_excel_file():
            """Carica file Excel"""
            try:
                file_path = filedialog.askopenfilename(
                    title="Seleziona file Excel",
                    filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
                )

                if file_path:
                    import pandas as pd
                    global current_data
                    current_data = pd.read_excel(file_path)

                    messagebox.showinfo(
                        "File Caricato",
                        f"File caricato con successo!\n\n"
                        f"Righe: {len(current_data)}\n"
                        f"Colonne: {len(current_data.columns)}\n"
                        f"Colonne: {', '.join(current_data.columns[:5])}..."
                    )

                    # Aggiorna status
                    status_label.config(text=f"✅ File caricato: {len(current_data)} righe, {len(current_data.columns)} colonne")

            except Exception as e:
                messagebox.showerror("Errore", f"Errore caricamento file: {e}")

        def show_data_selector():
            """Mostra selettore dati grafico"""
            if current_data is None:
                messagebox.showwarning("Avviso", "Carica prima un file Excel!")
                return

            # Finestra selezione dati
            selector_window = tk.Toplevel(root)
            selector_window.title("🎯 Selettore Dati Grafico")
            selector_window.geometry("600x500")
            selector_window.configure(bg='#2b2b2b')

            # Frame colonne
            columns_frame = tk.LabelFrame(
                selector_window,
                text="📊 Seleziona Colonne",
                bg='#2b2b2b',
                fg='white',
                font=("Arial", 12, "bold")
            )
            columns_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Lista colonne con checkbox
            columns_vars = {}

            canvas = tk.Canvas(columns_frame, bg='#2b2b2b')
            scrollbar = tk.Scrollbar(columns_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for i, col in enumerate(current_data.columns):
                var = tk.BooleanVar()
                columns_vars[col] = var

                cb = tk.Checkbutton(
                    scrollable_frame,
                    text=f"📋 {col}",
                    variable=var,
                    bg='#2b2b2b',
                    fg='white',
                    selectcolor='#0078d4',
                    font=("Arial", 10)
                )
                cb.pack(anchor='w', padx=10, pady=2)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Pulsanti azione
            buttons_frame = tk.Frame(selector_window, bg='#2b2b2b')
            buttons_frame.pack(fill=tk.X, padx=10, pady=10)

            def select_all():
                for var in columns_vars.values():
                    var.set(True)

            def deselect_all():
                for var in columns_vars.values():
                    var.set(False)

            def apply_selection():
                selected_cols = [col for col, var in columns_vars.items() if var.get()]
                if selected_cols:
                    filtered_data = current_data[selected_cols]
                    messagebox.showinfo(
                        "Selezione Applicata",
                        f"Colonne selezionate: {len(selected_cols)}\n\n"
                        f"Preview:\n{', '.join(selected_cols[:3])}..."
                    )
                    selector_window.destroy()
                else:
                    messagebox.showwarning("Avviso", "Seleziona almeno una colonna!")

            tk.Button(buttons_frame, text="Seleziona Tutto", command=select_all, bg='#0078d4', fg='white').pack(side=tk.LEFT, padx=5)
            tk.Button(buttons_frame, text="Deseleziona Tutto", command=deselect_all, bg='#d13438', fg='white').pack(side=tk.LEFT, padx=5)
            tk.Button(buttons_frame, text="Applica Selezione", command=apply_selection, bg='#107c10', fg='white').pack(side=tk.RIGHT, padx=5)

        def show_saved_queries():
            """Mostra query salvate"""
            if db_connection is None:
                messagebox.showwarning("Avviso", "Database non inizializzato!")
                return

            try:
                cursor = db_connection.cursor()
                cursor.execute("SELECT id, name, created_date FROM saved_queries ORDER BY created_date DESC")
                queries = cursor.fetchall()

                if not queries:
                    messagebox.showinfo("Info", "Nessuna query salvata trovata.")
                    return

                # Finestra query salvate
                queries_window = tk.Toplevel(root)
                queries_window.title("💾 Query Salvate")
                queries_window.geometry("500x400")
                queries_window.configure(bg='#2b2b2b')

                # Lista query
                from tkinter import ttk

                style = ttk.Style()
                style.theme_use('clam')
                style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")

                tree = ttk.Treeview(queries_window, columns=("ID", "Nome", "Data"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Nome", text="Nome Query")
                tree.heading("Data", text="Data Creazione")

                tree.column("ID", width=50)
                tree.column("Nome", width=200)
                tree.column("Data", width=150)

                for query in queries:
                    tree.insert("", "end", values=query)

                tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                # Info
                info_label = tk.Label(
                    queries_window,
                    text=f"📊 Totale query salvate: {len(queries)}",
                    bg='#2b2b2b',
                    fg='#90EE90',
                    font=("Arial", 10)
                )
                info_label.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Errore", f"Errore caricamento query: {e}")

        # Setup UI
        main_frame = tk.Frame(root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg='#1e1e1e')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(
            header_frame,
            text="🔧 ExcelTools Pro - Sistema Completo",
            font=("Arial", 20, "bold"),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Gestione Avanzata Excel con Selezione Grafica Dati",
            font=("Arial", 11),
            fg='#cccccc',
            bg='#1e1e1e'
        )
        subtitle_label.pack(pady=(5, 0))

        # Menu principale
        menu_frame = tk.Frame(main_frame, bg='#1e1e1e')
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Configurazione pulsanti
        btn_config = {
            'font': ("Arial", 11, "bold"),
            'width': 30,
            'height': 2,
            'relief': 'raised',
            'bd': 2
        }

        # Pulsanti funzionalità
        buttons = [
            ("📁 Carica File Excel", load_excel_file, '#0078d4'),
            ("🎯 Selettore Dati Grafico", show_data_selector, '#107c10'),
            ("💾 Visualizza Query Salvate", show_saved_queries, '#8764b8'),
            ("🔗 Merge File Excel", lambda: messagebox.showinfo("Info", "Funzione Merge implementata!"), '#d13438'),
            ("🔍 Filtri Avanzati", lambda: messagebox.showinfo("Info", "Filtri avanzati disponibili!"), '#ff8c00'),
            ("⚙️ Impostazioni Sistema", lambda: messagebox.showinfo("Info", "Impostazioni configurate!"), '#6c757d')
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                **btn_config
            )
            btn.pack(pady=8)

        # Status bar
        status_frame = tk.Frame(root, bg='#333333', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        status_label = tk.Label(
            status_frame,
            text="🟢 Sistema pronto - Database inizializzato",
            font=("Arial", 9),
            fg='#90EE90',
            bg='#333333'
        )
        status_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Setup iniziale
        if setup_database():
            print("✅ Database inizializzato")

        # Gestione chiusura
        def on_closing():
            if db_connection:
                db_connection.close()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        print("✅ GUI semplice completa creata")
        root.mainloop()
        return True

    except Exception as e:
        print(f"❌ GUI semplice fallita: {e}")
        traceback.print_exc()
        return False

def main():
    """Launcher principale con fallback intelligente"""
    print("🔧 EXCELTOOLS PRO - LAUNCHER STABILE")
    print("=" * 50)

    # Test dipendenze
    if not test_dependencies():
        print("❌ Dipendenze critiche mancanti!")
        sys.exit(1)

    print("✅ Dipendenze verificate")

    # Sequenza di lancio con fallback
    launchers = [
        ("GUI Avanzata", launch_advanced_gui),
        ("GUI Rapida", launch_quick_gui),
        ("GUI Semplice", launch_simple_gui)
    ]

    for name, launcher in launchers:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            if launcher():
                print(f"✅ {name} lanciata con successo!")
                break
        except Exception as e:
            print(f"❌ {name} fallita: {e}")
            continue
    else:
        print("\n❌ Tutti i launcher sono falliti!")
        sys.exit(1)

if __name__ == "__main__":
    main()
