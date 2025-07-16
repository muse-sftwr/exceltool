#!/usr/bin/env python3
"""
🚀 EXCELTOOLS PRO - ADVANCED SYSTEM LAUNCHER
=============================================

Launcher principale per il sistema avanzato con controllo dipendenze,
inizializzazione database e avvio interfaccia grafica professionale.

Autore: Senior System Administrator & DevOps Engineer
Data: 2025-07-16
Versione: Enterprise 4.0
"""

import os
import sys
import sqlite3
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Configurazione sistema
SYSTEM_NAME = "ExcelTools Pro Advanced"
VERSION = "4.0 Enterprise"
MIN_PYTHON_VERSION = (3, 8)

# Dipendenze richieste
REQUIRED_PACKAGES = {
    'pandas': '2.0.0',
    'openpyxl': '3.1.0',
    'customtkinter': '5.0.0'
}

# Dipendenze opzionali
OPTIONAL_PACKAGES = {
    'numpy': '1.20.0',
    'xlsxwriter': '3.0.0',
    'matplotlib': '3.5.0'
}

# Paths di sistema
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "exceltools_advanced.db"
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"


class SystemValidator:
    """Validatore sistema e dipendenze"""

    def __init__(self):
        self.validation_results = {}
        self.setup_directories()

    def setup_directories(self):
        """Crea directory necessarie"""
        for directory in [CONFIG_DIR, LOGS_DIR]:
            directory.mkdir(exist_ok=True)

    def check_python_version(self) -> Tuple[bool, str]:
        """Verifica versione Python"""
        current_version = sys.version_info[:2]

        if current_version >= MIN_PYTHON_VERSION:
            return True, f"Python {'.'.join(map(str, current_version))} ✅"
        else:
            required = '.'.join(map(str, MIN_PYTHON_VERSION))
            current = '.'.join(map(str, current_version))
            return False, f"Python {current} ❌ (richiesto >= {required})"

    def check_package_availability(self, package_name: str,
                                  min_version: str = None) -> Tuple[bool, str]:
        """Verifica disponibilità pacchetto"""
        try:
            __import__(package_name)
            if min_version:
                pkg = __import__(package_name)
                if hasattr(pkg, '__version__'):
                    return True, f"{package_name} {pkg.__version__} ✅"
                else:
                    return True, f"{package_name} (versione sconosciuta) ✅"
            else:
                return True, f"{package_name} ✅"
        except ImportError:
            return False, f"{package_name} ❌ (non installato)"

    def check_database_connectivity(self) -> Tuple[bool, str]:
        """Verifica connettività database"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()

            size_mb = DATABASE_PATH.stat().st_size / (1024 * 1024) if DATABASE_PATH.exists() else 0
            return True, f"Database SQLite ✅ ({size_mb:.2f} MB)"
        except Exception as e:
            return False, f"Database SQLite ❌ ({str(e)})"

    def check_file_permissions(self) -> Tuple[bool, str]:
        """Verifica permessi file system"""
        try:
            # Test scrittura
            test_file = BASE_DIR / "test_permissions.tmp"
            test_file.write_text("test")
            test_file.unlink()

            return True, "Permessi file system ✅"
        except Exception as e:
            return False, f"Permessi file system ❌ ({str(e)})"

    def validate_system(self) -> Dict[str, Tuple[bool, str]]:
        """Esegue validazione completa sistema"""
        print(f"🔍 Validazione sistema {SYSTEM_NAME} v{VERSION}")
        print("=" * 60)

        # Validazioni base
        validations = {
            'python_version': self.check_python_version(),
            'database': self.check_database_connectivity(),
            'file_permissions': self.check_file_permissions()
        }

        # Verifica pacchetti richiesti
        print("\n📦 Pacchetti richiesti:")
        for package, min_version in REQUIRED_PACKAGES.items():
            result = self.check_package_availability(package, min_version)
            validations[f'package_{package}'] = result
            print(f"  {result[1]}")

        # Verifica pacchetti opzionali
        print("\n📦 Pacchetti opzionali:")
        for package, min_version in OPTIONAL_PACKAGES.items():
            result = self.check_package_availability(package, min_version)
            validations[f'optional_{package}'] = result
            print(f"  {result[1]}")

        # Summary validazioni
        print(f"\n🖥️ Sistema:")
        for key, (status, message) in validations.items():
            if not key.startswith(('package_', 'optional_')):
                print(f"  {message}")

        return validations

    def install_missing_packages(self, validation_results: Dict) -> bool:
        """Installa pacchetti mancanti"""
        missing_required = []

        for package in REQUIRED_PACKAGES:
            key = f'package_{package}'
            if key in validation_results and not validation_results[key][0]:
                missing_required.append(package)

        if missing_required:
            print(f"\n📥 Installazione pacchetti mancanti: {missing_required}")

            for package in missing_required:
                try:
                    print(f"  Installando {package}...")
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", package
                    ], capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"  ✅ {package} installato con successo")
                    else:
                        print(f"  ❌ Errore installazione {package}: {result.stderr}")
                        return False

                except Exception as e:
                    print(f"  ❌ Errore installazione {package}: {e}")
                    return False

            return True

        return True

    def get_system_status(self) -> str:
        """Restituisce stato sistema"""
        validation_results = self.validate_system()

        required_ok = all(
            validation_results.get(f'package_{pkg}', (False, ''))[0]
            for pkg in REQUIRED_PACKAGES
        )

        basic_ok = all(
            validation_results[key][0]
            for key in ['python_version', 'database', 'file_permissions']
        )

        if basic_ok and required_ok:
            return "🟢 SISTEMA PRONTO"
        elif basic_ok:
            return "🟡 SISTEMA PARZIALE (pacchetti mancanti)"
        else:
            return "🔴 SISTEMA NON FUNZIONANTE"


class DatabaseInitializer:
    """Inizializzatore database avanzato"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path

    def initialize_database(self) -> bool:
        """Inizializza database con schema completo"""
        try:
            print(f"🗄️ Inizializzazione database: {self.db_path}")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Schema viste salvate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_views (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    table_name TEXT,
                    selected_columns TEXT,
                    filters TEXT,
                    query TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    is_favorite BOOLEAN DEFAULT 0,
                    view_type TEXT DEFAULT 'custom',
                    tags TEXT
                )
            """)

            # Schema configurazioni merge
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS merge_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    source_tables TEXT,
                    join_conditions TEXT,
                    merge_type TEXT,
                    output_columns TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_executed TIMESTAMP,
                    execution_count INTEGER DEFAULT 0
                )
            """)

            # Schema filtri predefiniti
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS filter_presets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    table_name TEXT,
                    filter_conditions TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    usage_count INTEGER DEFAULT 0
                )
            """)

            # Schema configurazioni sistema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Schema log attività
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action TEXT,
                    details TEXT,
                    user_data TEXT,
                    status TEXT
                )
            """)

            # Inserisci configurazioni default
            default_configs = [
                ('theme', 'dark', 'Tema interfaccia (dark/light)'),
                ('auto_backup', 'true', 'Backup automatico database'),
                ('max_preview_rows', '1000', 'Righe massime in preview'),
                ('export_format', 'xlsx', 'Formato export default'),
                ('language', 'it', 'Linguaggio interfaccia')
            ]

            for key, value, desc in default_configs:
                cursor.execute("""
                    INSERT OR IGNORE INTO system_config (key, value, description)
                    VALUES (?, ?, ?)
                """, (key, value, desc))

            # Indici per performance
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_views_name ON saved_views(name)",
                "CREATE INDEX IF NOT EXISTS idx_views_favorite ON saved_views(is_favorite)",
                "CREATE INDEX IF NOT EXISTS idx_merge_name ON merge_configs(name)",
                "CREATE INDEX IF NOT EXISTS idx_filters_table ON filter_presets(table_name)",
                "CREATE INDEX IF NOT EXISTS idx_activity_timestamp ON activity_log(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_config_key ON system_config(key)"
            ]

            for index_sql in indices:
                cursor.execute(index_sql)

            conn.commit()
            conn.close()

            print("  ✅ Database inizializzato con successo")
            return True

        except Exception as e:
            print(f"  ❌ Errore inizializzazione database: {e}")
            return False

    def create_sample_data(self) -> bool:
        """Crea dati di esempio per demo"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Viste di esempio
            sample_views = [
                ("Vista Vendite Q1", "Vendite primo trimestre", "vendite",
                 '["prodotto", "quantita", "ricavo"]',
                 '[{"column": "trimestre", "operator": "=", "value": "Q1"}]',
                 "SELECT prodotto, quantita, ricavo FROM vendite WHERE trimestre = 'Q1'",
                 1),
                ("Clienti Attivi", "Clienti con ordini recenti", "clienti",
                 '["nome", "email", "ultimo_ordine"]',
                 '[{"column": "status", "operator": "=", "value": "attivo"}]',
                 "SELECT nome, email, ultimo_ordine FROM clienti WHERE status = 'attivo'",
                 1),
                ("Prodotti Top", "Prodotti più venduti", "prodotti",
                 '["nome", "categoria", "vendite_totali"]',
                 '[{"column": "vendite_totali", "operator": ">", "value": "1000"}]',
                 "SELECT nome, categoria, vendite_totali FROM prodotti WHERE vendite_totali > 1000",
                 0)
            ]

            for view_data in sample_views:
                cursor.execute("""
                    INSERT OR IGNORE INTO saved_views
                    (name, description, table_name, selected_columns,
                     filters, query, is_favorite)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, view_data)

            # Configurazioni merge di esempio
            sample_merges = [
                ("Vendite Complete", "Join vendite + clienti + prodotti",
                 '["vendite", "clienti", "prodotti"]',
                 '[{"left_table": "vendite", "right_table": "clienti", "left_column": "cliente_id", "right_column": "id", "join_type": "inner"}, {"left_table": "vendite", "right_table": "prodotti", "left_column": "prodotto_id", "right_column": "id", "join_type": "inner"}]',
                 "inner",
                 '["cliente_nome", "prodotto_nome", "quantita", "prezzo", "data_vendita"]'),
                ("Analisi Clienti", "Clienti con dettagli vendite",
                 '["clienti", "vendite"]',
                 '[{"left_table": "clienti", "right_table": "vendite", "left_column": "id", "right_column": "cliente_id", "join_type": "left"}]',
                 "left",
                 '["nome", "email", "totale_acquisti", "ultima_data"]')
            ]

            for merge_data in sample_merges:
                cursor.execute("""
                    INSERT OR IGNORE INTO merge_configs
                    (name, description, source_tables, join_conditions,
                     merge_type, output_columns)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, merge_data)

            # Filtri predefiniti
            sample_filters = [
                ("Anno Corrente", "vendite",
                 '[{"column": "data_vendita", "operator": ">=", "value": "2025-01-01"}]',
                 "Vendite dell'anno corrente"),
                ("Clienti Premium", "clienti",
                 '[{"column": "tipo", "operator": "=", "value": "premium"}]',
                 "Solo clienti premium"),
                ("Prodotti Attivi", "prodotti",
                 '[{"column": "status", "operator": "=", "value": "attivo"}]',
                 "Prodotti attualmente attivi")
            ]

            for filter_data in sample_filters:
                cursor.execute("""
                    INSERT OR IGNORE INTO filter_presets
                    (name, table_name, filter_conditions, description)
                    VALUES (?, ?, ?, ?)
                """, filter_data)

            conn.commit()
            conn.close()

            print("  ✅ Dati di esempio creati")
            return True

        except Exception as e:
            print(f"  ❌ Errore creazione dati esempio: {e}")
            return False


class AdvancedLauncher:
    """Launcher principale sistema avanzato"""

    def __init__(self):
        self.validator = SystemValidator()
        self.db_initializer = DatabaseInitializer()

    def show_welcome_banner(self):
        """Mostra banner di benvenuto"""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🏢 {SYSTEM_NAME:<50} v{VERSION:<15} ║
║                                                                              ║
║  Sistema avanzato di gestione database Excel con interfaccia grafica        ║
║  professionale per selezione dati, viste salvate e merge configurabile.     ║
║                                                                              ║
║  Funzionalità principali:                                                   ║
║  • 🎨 Interfaccia grafica per selezione dati                               ║
║  • 👁️ Viste salvate con sistema preferiti                                  ║
║  • 🔗 Merge configurabile di tabelle multiple                               ║
║  • 🔍 Query builder visuale avanzato                                        ║
║  • 📊 Esportazione flessibile multi-formato                                ║
║  • ⚡ Ottimizzazione database automatica                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def run_startup_checks(self) -> bool:
        """Esegue controlli di avvio"""
        print("🔧 Controlli di avvio...")

        # Validazione sistema
        validation_results = self.validator.validate_system()
        status = self.validator.get_system_status()

        print(f"\n{status}")

        # Controlla se sistema pronto
        if "🔴" in status:
            print("\n❌ Sistema non pronto per l'avvio")
            return False

        # Installa pacchetti mancanti se necessario
        if "🟡" in status:
            print("\n📥 Tentativo installazione pacchetti mancanti...")
            if not self.validator.install_missing_packages(validation_results):
                print("❌ Impossibile installare tutti i pacchetti richiesti")
                return False

        # Inizializza database
        if not self.db_initializer.initialize_database():
            print("❌ Impossibile inizializzare database")
            return False

        # Crea dati di esempio se database vuoto
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM saved_views")
            views_count = cursor.fetchone()[0]
            conn.close()

            if views_count == 0:
                print("📋 Creazione dati di esempio...")
                self.db_initializer.create_sample_data()

        except Exception:
            pass

        return True

    def launch_application(self) -> bool:
        """Avvia applicazione principale"""
        try:
            print("\n🚀 Avvio interfaccia grafica...")

            # Import e avvio GUI
            try:
                from advanced_excel_tools_gui import AdvancedExcelToolsGUI
                app = AdvancedExcelToolsGUI()
                app.run()
                return True

            except ImportError as e:
                print(f"❌ Errore import GUI: {e}")
                print("🔄 Tentativo avvio interfaccia base...")

                # Fallback a interfaccia base
                import tkinter as tk
                from tkinter import messagebox

                root = tk.Tk()
                root.withdraw()

                messagebox.showinfo(
                    "ExcelTools Pro Advanced",
                    "Sistema avviato con successo!\n\n"
                    "L'interfaccia grafica avanzata non è disponibile.\n"
                    "Utilizzare i moduli Python direttamente."
                )

                return True

        except Exception as e:
            print(f"❌ Errore avvio applicazione: {e}")
            return False

    def show_troubleshooting_info(self):
        """Mostra informazioni risoluzione problemi"""
        troubleshooting = """
🔧 RISOLUZIONE PROBLEMI
========================

Problemi comuni e soluzioni:

1. Errore pacchetti mancanti:
   - Eseguire: pip install pandas openpyxl customtkinter
   - Verificare versione Python >= 3.8

2. Errore database:
   - Verificare permessi scrittura nella cartella
   - Eliminare file database per reset completo

3. Errore interfaccia grafica:
   - Installare: pip install customtkinter
   - Su Linux: sudo apt-get install python3-tk

4. Prestazioni lente:
   - Ottimizzare database dal menu Strumenti
   - Ridurre numero righe preview

5. Errori import Excel:
   - Verificare formato file (.xlsx supportato)
   - Controllare che file non sia in uso

Per supporto tecnico, verificare:
- Versione Python corretta
- Tutte le dipendenze installate
- Permessi file system
- Log errori dettagliati
"""
        print(troubleshooting)

    def run(self):
        """Esegue launcher completo"""
        try:
            # Banner benvenuto
            self.show_welcome_banner()

            # Controlli avvio
            if not self.run_startup_checks():
                print("\n💡 Consultare la guida alla risoluzione problemi:")
                self.show_troubleshooting_info()
                return False

            # Avvio applicazione
            if not self.launch_application():
                print("\n❌ Impossibile avviare l'applicazione")
                return False

            print("\n✅ ExcelTools Pro Advanced terminato correttamente")
            return True

        except KeyboardInterrupt:
            print("\n\n⚠️ Applicazione interrotta dall'utente")
            return False
        except Exception as e:
            print(f"\n❌ Errore critico: {e}")
            return False


def main():
    """Funzione principale"""
    launcher = AdvancedLauncher()
    success = launcher.run()

    if not success:
        print("\n🆘 Per assistenza, eseguire la diagnostica sistema")
        sys.exit(1)


if __name__ == "__main__":
    main()
