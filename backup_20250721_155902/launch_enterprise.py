#!/usr/bin/env python3
"""
🚀 EXCELTOOLS PRO ENTERPRISE - LAUNCHER PRINCIPALE
=================================================

Launcher principale per il sistema database enterprise
con interfaccia professionale e funzionalità complete.

Autore: Senior DB Manager IT DEV
Data: 2025-07-16
Versione: Enterprise Launcher 3.0
"""

import sys
import os
import logging
from datetime import datetime

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('exceltools_enterprise_launcher.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ExcelToolsEnterpriseLauncher")


def check_dependencies():
    """Verifica dipendenze del sistema"""
    logger.info("🔍 Verificando dipendenze sistema...")

    missing_deps = []
    dep_status = {}

    # Verifica pandas
    try:
        import pandas as pd
        dep_status['pandas'] = f"✅ pandas {pd.__version__}"
        logger.info(f"✅ pandas {pd.__version__} disponibile")
    except ImportError:
        missing_deps.append('pandas')
        dep_status['pandas'] = "❌ pandas NON DISPONIBILE"
        logger.error("❌ pandas non disponibile")

    # Verifica openpyxl
    try:
        import openpyxl
        dep_status['openpyxl'] = f"✅ openpyxl {openpyxl.__version__}"
        logger.info(f"✅ openpyxl {openpyxl.__version__} disponibile")
    except ImportError:
        missing_deps.append('openpyxl')
        dep_status['openpyxl'] = "❌ openpyxl NON DISPONIBILE"
        logger.error("❌ openpyxl non disponibile")

    # Verifica customtkinter (opzionale)
    try:
        import customtkinter as ctk
        dep_status['customtkinter'] = f"✅ customtkinter {ctk.__version__}"
        logger.info(f"✅ customtkinter {ctk.__version__} disponibile")
    except ImportError:
        dep_status['customtkinter'] = "⚠️ customtkinter non disponibile (interfaccia classica)"
        logger.warning("⚠️ customtkinter non disponibile - uso interfaccia classica")

    # Verifica tkinter (built-in)
    try:
        import tkinter
        dep_status['tkinter'] = "✅ tkinter disponibile"
        logger.info("✅ tkinter disponibile")
    except ImportError:
        missing_deps.append('tkinter')
        dep_status['tkinter'] = "❌ tkinter NON DISPONIBILE"
        logger.error("❌ tkinter non disponibile")

    # Verifica sqlite3 (built-in)
    try:
        import sqlite3
        dep_status['sqlite3'] = "✅ sqlite3 disponibile"
        logger.info("✅ sqlite3 disponibile")
    except ImportError:
        missing_deps.append('sqlite3')
        dep_status['sqlite3'] = "❌ sqlite3 NON DISPONIBILE"
        logger.error("❌ sqlite3 non disponibile")

    return missing_deps, dep_status


def install_missing_dependencies(missing_deps):
    """Suggerisce installazione dipendenze mancanti"""
    if not missing_deps:
        return True

    print("\n" + "="*60)
    print("⚠️  DIPENDENZE MANCANTI RILEVATE")
    print("="*60)

    for dep in missing_deps:
        if dep == 'pandas':
            print("📦 Per installare pandas:")
            print("   pip install pandas")
        elif dep == 'openpyxl':
            print("📦 Per installare openpyxl:")
            print("   pip install openpyxl")
        elif dep == 'tkinter':
            print("📦 tkinter dovrebbe essere incluso con Python")
            print("   Su Ubuntu/Debian: sudo apt-get install python3-tk")
        elif dep == 'sqlite3':
            print("📦 sqlite3 dovrebbe essere incluso con Python")

    print("\n💡 Installazione rapida di tutte le dipendenze:")
    print("   pip install pandas openpyxl customtkinter")

    print("\n" + "="*60)

    return False


def show_system_info():
    """Mostra informazioni sistema"""
    print("\n" + "="*60)
    print("🏢 EXCELTOOLS PRO ENTERPRISE - SISTEMA INFORMAZIONI")
    print("="*60)
    print(f"📅 Data avvio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Piattaforma: {sys.platform}")
    print(f"📁 Directory lavoro: {os.getcwd()}")
    print("="*60)


def launch_enterprise_system():
    """Lancia sistema enterprise"""
    logger.info("🚀 Avviando sistema enterprise...")

    try:
        # Import del sistema principale
        from excel_tools_pro_gui import ExcelToolsProGUI

        logger.info("✅ Moduli sistema caricati con successo")

        # Crea e avvia applicazione
        print("\n🎯 Inizializzando interfaccia utente...")
        app = ExcelToolsProGUI()

        logger.info("🖥️ Interfaccia grafica inizializzata")
        print("✅ Sistema pronto!")
        print("\n" + "="*60)
        print("🏢 EXCELTOOLS PRO ENTERPRISE - AVVIATO CON SUCCESSO")
        print("="*60)
        print("📋 Funzionalità disponibili:")
        print("   • 📁 Importazione Excel multi-sheet")
        print("   • 🔍 Query SQL avanzate con filtri")
        print("   • 💾 Esportazione flessibile (Excel, CSV, JSON, HTML)")
        print("   • 📊 Statistiche database professionali")
        print("   • 🗑️ Eliminazione dati con condizioni")
        print("   • 📚 Gestione query salvate")
        print("   • 🔧 Ottimizzazione database automatica")
        print("   • 🎨 Interfaccia user-friendly moderna")
        print("="*60)

        # Avvia GUI
        app.run()

    except ImportError as e:
        logger.error(f"❌ Errore import moduli: {e}")
        print(f"\n❌ Errore caricamento sistema: {e}")
        print("💡 Assicurati che tutti i file del sistema siano presenti:")
        print("   • excel_database_enterprise_complete.py")
        print("   • excel_tools_pro_gui.py")
        return False

    except Exception as e:
        logger.error(f"❌ Errore avvio sistema: {e}")
        print(f"\n❌ Errore inatteso: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


def show_help():
    """Mostra help del sistema"""
    help_text = """
🏢 EXCELTOOLS PRO ENTERPRISE - GUIDA RAPIDA
==========================================

🎯 COME INIZIARE:
1. Clicca "📁 Importa Excel" per caricare i tuoi file
2. Seleziona una tabella dal pannello sinistro
3. Usa il Query Builder per interrogare i dati
4. Esporta i risultati in vari formati

🔧 FUNZIONALITÀ PRINCIPALI:

📊 GESTIONE DATABASE:
• Import automatico di file Excel multi-sheet
• Database SQLite integrato e ottimizzato
• Supporto colonne dinamiche
• Metadata tracking automatico

🔍 QUERY E FILTRI:
• Editor SQL professionale con syntax highlighting
• Query builder visuale
• Filtri avanzati per colonne
• Query salvate e preferiti
• Statistiche colonne automatiche

💾 ESPORTAZIONE:
• Excel (.xlsx) con formattazione
• CSV con separatori personalizzabili
• JSON in vari formati
• HTML per web

🛠️ STRUMENTI AVANZATI:
• Ottimizzazione database automatica
• Eliminazione dati con condizioni
• Statistiche comprehensive
• Logging professionale

🎨 INTERFACCIA:
• Tema scuro moderno (se customtkinter disponibile)
• Layout a 3 pannelli ottimizzato
• Tabelle results con scrolling
• Status bar informativi

📚 QUERY ESEMPI:
• SELECT * FROM tabella LIMIT 100
• SELECT colonna1, colonna2 FROM tabella WHERE colonna1 > 100
• SELECT categoria, COUNT(*) FROM tabella GROUP BY categoria
• DELETE FROM tabella WHERE condizione = 'valore'

🔗 SUPPORTO:
Per assistenza tecnica, controlla i log in:
• exceltools_enterprise_launcher.log
• database_enterprise.log
"""
    print(help_text)


def main():
    """Funzione principale launcher"""
    print("🚀 ExcelTools Pro Enterprise - Launcher")
    print("=" * 50)

    # Mostra informazioni sistema
    show_system_info()

    # Verifica dipendenze
    missing_deps, dep_status = check_dependencies()

    # Mostra status dipendenze
    print("\n📦 STATUS DIPENDENZE:")
    print("-" * 30)
    for dep, status in dep_status.items():
        print(f"   {status}")

    # Gestisci dipendenze mancanti
    if missing_deps:
        if not install_missing_dependencies(missing_deps):
            print("\n❌ Impossibile avviare: dipendenze mancanti")
            print("💡 Installa le dipendenze richieste e riprova")
            return 1

    # Verifica disponibilità file sistema
    required_files = [
        'excel_database_enterprise_complete.py',
        'excel_tools_pro_gui.py'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"\n❌ File sistema mancanti: {', '.join(missing_files)}")
        return 1

    # Tutto OK - avvia sistema
    print("\n✅ Tutte le verifiche completate con successo!")

    # Opzioni avvio
    print("\n🎯 OPZIONI DISPONIBILI:")
    print("1. 🚀 Avvia Sistema Enterprise (default)")
    print("2. ❓ Mostra Guida")
    print("3. 🚪 Esci")

    try:
        choice = input("\nScegli opzione (1-3) [default=1]: ").strip()

        if choice == '2':
            show_help()
            return 0
        elif choice == '3':
            print("👋 Arrivederci!")
            return 0
        else:
            # Default: avvia sistema
            success = launch_enterprise_system()
            return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\n👋 Avvio interrotto dall'utente")
        return 0
    except Exception as e:
        logger.error(f"❌ Errore launcher: {e}")
        print(f"\n❌ Errore launcher: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
