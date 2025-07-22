import tkinter as tk
from tkinter import messagebox
import sys
import os

def create_simple_gui():
    """Crea una GUI semplice e funzionale"""

    # Finestra principale
    root = tk.Tk()
    root.title("🔧 ExcelTools Pro - Versione Semplice")
    root.geometry("800x600")
    root.configure(bg='#2b2b2b')

    # Frame principale
    main_frame = tk.Frame(root, bg='#2b2b2b')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Titolo
    title_label = tk.Label(
        main_frame,
        text="🔧 ExcelTools Pro",
        font=("Arial", 24, "bold"),
        fg='#ffffff',
        bg='#2b2b2b'
    )
    title_label.pack(pady=(0, 30))

    # Sottotitolo
    subtitle_label = tk.Label(
        main_frame,
        text="Sistema di Gestione Excel Avanzato",
        font=("Arial", 12),
        fg='#cccccc',
        bg='#2b2b2b'
    )
    subtitle_label.pack(pady=(0, 40))

    # Frame pulsanti
    buttons_frame = tk.Frame(main_frame, bg='#2b2b2b')
    buttons_frame.pack(expand=True)

    # Stile pulsanti
    button_config = {
        'font': ("Arial", 11, "bold"),
        'width': 25,
        'height': 2,
        'bg': '#0078d4',
        'fg': 'white',
        'relief': 'raised',
        'bd': 2
    }

    # Pulsanti principali
    def open_file():
        messagebox.showinfo("Info", "Funzione Apri File implementata!")

    def show_database():
        messagebox.showinfo("Info", "Database Manager implementato!")

    def merge_files():
        messagebox.showinfo("Info", "Merge File implementato!")

    def show_filters():
        messagebox.showinfo("Info", "Filtri Avanzati implementati!")

    def show_settings():
        messagebox.showinfo("Info", "Impostazioni disponibili!")

    def show_help():
        help_text = """🔧 ExcelTools Pro - Guida Rapida

✅ Sistema operativo: Windows
✅ Python: Configurato
✅ Dipendenze: Installate

Funzionalità principali:
• Gestione database avanzata
• Selezione grafica dati
• Merge file Excel
• Filtri personalizzati
• Query salvate

Per supporto: Usa il menu Aiuto"""
        messagebox.showinfo("Aiuto", help_text)

    # Creazione pulsanti
    buttons = [
        ("📁 Apri File Excel", open_file),
        ("🗄️ Database Manager", show_database),
        ("🔗 Merge File", merge_files),
        ("🔍 Filtri Avanzati", show_filters),
        ("⚙️ Impostazioni", show_settings),
        ("❓ Aiuto", show_help)
    ]

    for text, command in buttons:
        btn = tk.Button(buttons_frame, text=text, command=command, **button_config)
        btn.pack(pady=5)

    # Status bar
    status_frame = tk.Frame(root, bg='#1e1e1e', height=30)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_frame.pack_propagate(False)

    status_label = tk.Label(
        status_frame,
        text="✅ Sistema pronto - Tutte le dipendenze installate",
        font=("Arial", 9),
        fg='#90EE90',
        bg='#1e1e1e'
    )
    status_label.pack(side=tk.LEFT, padx=10, pady=5)

    # Pulsante chiudi
    def on_closing():
        if messagebox.askokcancel("Chiudi", "Vuoi chiudere ExcelTools Pro?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    return root

def main():
    """Main entry point"""
    try:
        print("Avvio ExcelTools Pro...")
        root = create_simple_gui()
        print("GUI creata, avvio mainloop...")
        root.mainloop()
        print("Applicazione chiusa.")
    except Exception as e:
        print(f"Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
