#!/usr/bin/env python3
"""
🧪 EXCELTOOLS PRO ADVANCED - COMPREHENSIVE TEST SUITE
======================================================

Suite di test completa per il sistema avanzato con validazione
di tutti i componenti e funzionalità integrate.

Autore: Senior Quality Assurance Engineer
Data: 2025-07-16
Versione: Test 4.0
"""

import os
import sys
import sqlite3
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Configurazione test
TEST_DB_PATH = "test_advanced.db"
SAMPLE_DATA_SIZE = 100


class AdvancedSystemTester:
    """Tester completo sistema avanzato"""

    def __init__(self):
        self.test_results = {}
        self.temp_files = []
        self.setup_test_environment()

    def setup_test_environment(self):
        """Configura ambiente di test"""
        print("🛠️ Configurazione ambiente di test...")

        # Pulizia file test precedenti
        for file_path in [TEST_DB_PATH]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_imports(self) -> Tuple[bool, str]:
        """Test import moduli"""
        try:
            print("📦 Test import moduli...")

            import_tests = []

            # Test import base
            try:
                import pandas as pd
                import_tests.append(("pandas", True, pd.__version__))
            except ImportError as e:
                import_tests.append(("pandas", False, str(e)))

            try:
                import openpyxl
                import_tests.append(("openpyxl", True, openpyxl.__version__))
            except ImportError as e:
                import_tests.append(("openpyxl", False, str(e)))

            try:
                import customtkinter as ctk
                import_tests.append(("customtkinter", True, ctk.__version__))
            except ImportError as e:
                import_tests.append(("customtkinter", False, str(e)))

            # Test import moduli avanzati
            try:
                from advanced_database_manager import AdvancedDatabaseManager
                import_tests.append(("AdvancedDatabaseManager", True, "OK"))
            except ImportError as e:
                import_tests.append(("AdvancedDatabaseManager", False, str(e)))

            try:
                from advanced_excel_tools_gui import AdvancedExcelToolsGUI
                import_tests.append(("AdvancedExcelToolsGUI", True, "OK"))
            except ImportError as e:
                import_tests.append(("AdvancedExcelToolsGUI", False, str(e)))

            try:
                from launch_advanced_system import AdvancedLauncher
                import_tests.append(("AdvancedLauncher", True, "OK"))
            except ImportError as e:
                import_tests.append(("AdvancedLauncher", False, str(e)))

            # Risultati
            successful = sum(1 for _, success, _ in import_tests if success)
            total = len(import_tests)

            details = "\n".join([
                f"  {'✅' if success else '❌'} {module}: {version}"
                for module, success, version in import_tests
            ])

            success_rate = successful / total
            if success_rate >= 0.8:
                return True, f"Import: {successful}/{total} ✅\n{details}"
            else:
                return False, f"Import: {successful}/{total} ❌\n{details}"

        except Exception as e:
            return False, f"Errore test import: {e}"

    def test_database_manager(self) -> Tuple[bool, str]:
        """Test AdvancedDatabaseManager"""
        try:
            print("🗄️ Test AdvancedDatabaseManager...")

            # Import manager
            from advanced_database_manager import AdvancedDatabaseManager

            # Crea manager test
            db_manager = AdvancedDatabaseManager(TEST_DB_PATH)

            # Test creazione tabelle
            conn = sqlite3.connect(TEST_DB_PATH)
            cursor = conn.cursor()

            # Verifica tabelle create
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name IN (
                    'saved_views', 'merge_configs', 'filter_presets'
                )
            """)
            tables = cursor.fetchall()

            if len(tables) != 3:
                return False, f"Tabelle sistema: {len(tables)}/3 ❌"

            # Test salvataggio vista
            test_columns = ["col1", "col2", "col3"]
            test_filters = [
                {"column": "col1", "operator": "=", "value": "test"}
            ]

            success = db_manager.save_view(
                "test_view", "test_table", test_columns,
                test_filters, "Vista di test", True
            )

            if not success:
                return False, "Salvataggio vista fallito ❌"

            # Test recupero viste
            views = db_manager.get_saved_views()
            if not views or views[0]['name'] != 'test_view':
                return False, "Recupero viste fallito ❌"

            # Test configurazione merge
            merge_success = db_manager.save_merge_config(
                "test_merge", ["table1", "table2"],
                [{"left_table": "table1", "right_table": "table2",
                  "left_column": "id", "right_column": "id",
                  "join_type": "inner"}],
                "inner", ["col1", "col2"], "Test merge"
            )

            if not merge_success:
                return False, "Salvataggio merge config fallito ❌"

            # Test build query
            query = db_manager.build_query_from_config(
                "test_table", test_columns, test_filters
            )

            expected_parts = ["SELECT", "[col1]", "[col2]", "[col3]",
                             "FROM [test_table]", "WHERE", "[col1] = 'test'"]

            if not all(part in query for part in expected_parts):
                return False, f"Query building fallito ❌\nQuery: {query}"

            conn.close()

            return True, "AdvancedDatabaseManager: Tutti i test passati ✅"

        except Exception as e:
            return False, f"Errore test DatabaseManager: {e}"

    def test_graphical_selector(self) -> Tuple[bool, str]:
        """Test GraphicalDataSelector"""
        try:
            print("🎨 Test GraphicalDataSelector...")

            # Test solo se CustomTkinter disponibile
            try:
                import customtkinter as ctk
                from advanced_database_manager import (
                    AdvancedDatabaseManager, GraphicalDataSelector
                )
            except ImportError:
                return True, "GraphicalDataSelector: Skip (dipendenze opzionali) ⏭️"

            # Setup test database con dati
            db_manager = AdvancedDatabaseManager(TEST_DB_PATH)
            conn = sqlite3.connect(TEST_DB_PATH)
            cursor = conn.cursor()

            # Crea tabella test
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_data (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    value REAL,
                    category TEXT
                )
            """)

            # Inserisci dati test
            test_data = [
                (1, "Item1", 10.5, "A"),
                (2, "Item2", 20.3, "B"),
                (3, "Item3", 15.7, "A")
            ]

            cursor.executemany(
                "INSERT INTO test_data VALUES (?, ?, ?, ?)", test_data
            )
            conn.commit()
            conn.close()

            # Test creazione interfaccia (senza GUI effettiva)
            root = ctk.CTk()
            root.withdraw()  # Nasconde finestra

            selector = GraphicalDataSelector(
                root, db_manager, lambda x: None
            )

            # Test metodi principali
            tables = db_manager.get_all_tables_with_details()
            if not any(t['name'] == 'test_data' for t in tables):
                return False, "Tabella test non trovata ❌"

            unique_values = db_manager.get_column_unique_values(
                'test_data', 'category'
            )
            if set(unique_values) != {'A', 'B'}:
                return False, f"Valori unici errati: {unique_values} ❌"

            root.destroy()

            return True, "GraphicalDataSelector: Test base passati ✅"

        except Exception as e:
            return False, f"Errore test GraphicalSelector: {e}"

    def test_gui_components(self) -> Tuple[bool, str]:
        """Test componenti GUI"""
        try:
            print("🖥️ Test componenti GUI...")

            # Test import GUI
            try:
                from advanced_excel_tools_gui import AdvancedExcelToolsGUI
            except ImportError as e:
                return False, f"Import GUI fallito: {e} ❌"

            # Test creazione GUI (senza avvio)
            try:
                import customtkinter as ctk
                has_ctk = True
            except ImportError:
                has_ctk = False

            # Test inizializzazione base
            gui = AdvancedExcelToolsGUI()

            # Verifica attributi principali
            required_attrs = [
                'root', 'db_manager', 'saved_views', 'merge_configs'
            ]

            missing_attrs = [
                attr for attr in required_attrs
                if not hasattr(gui, attr)
            ]

            if missing_attrs:
                return False, f"Attributi mancanti: {missing_attrs} ❌"

            # Test database manager
            if gui.db_manager is None:
                return False, "Database manager non inizializzato ❌"

            # Verifica metodi principali
            required_methods = [
                'load_saved_views', 'update_statistics', 'create_menu_bar'
            ]

            missing_methods = [
                method for method in required_methods
                if not hasattr(gui, method)
            ]

            if missing_methods:
                return False, f"Metodi mancanti: {missing_methods} ❌"

            gui.root.destroy()

            return True, f"GUI Components: Test passati ✅ (CustomTkinter: {'Sì' if has_ctk else 'No'})"

        except Exception as e:
            return False, f"Errore test GUI: {e}"

    def test_launcher_system(self) -> Tuple[bool, str]:
        """Test sistema launcher"""
        try:
            print("🚀 Test sistema launcher...")

            from launch_advanced_system import (
                SystemValidator, DatabaseInitializer, AdvancedLauncher
            )

            # Test SystemValidator
            validator = SystemValidator()

            # Test validazione Python
            python_ok, python_msg = validator.check_python_version()
            if not python_ok:
                return False, f"Validazione Python fallita: {python_msg} ❌"

            # Test validazione database
            db_ok, db_msg = validator.check_database_connectivity()
            if not db_ok:
                return False, f"Validazione database fallita: {db_msg} ❌"

            # Test DatabaseInitializer
            db_init = DatabaseInitializer(Path(TEST_DB_PATH))
            init_success = db_init.initialize_database()

            if not init_success:
                return False, "Inizializzazione database fallita ❌"

            # Test creazione dati esempio
            sample_success = db_init.create_sample_data()
            if not sample_success:
                return False, "Creazione dati esempio fallita ❌"

            # Verifica dati esempio
            conn = sqlite3.connect(TEST_DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM saved_views")
            views_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM merge_configs")
            merge_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM filter_presets")
            filter_count = cursor.fetchone()[0]

            conn.close()

            if views_count == 0 or merge_count == 0 or filter_count == 0:
                return False, f"Dati esempio insufficienti: V{views_count} M{merge_count} F{filter_count} ❌"

            # Test AdvancedLauncher (senza GUI)
            launcher = AdvancedLauncher()

            required_launcher_attrs = [
                'validator', 'db_initializer'
            ]

            missing_launcher_attrs = [
                attr for attr in required_launcher_attrs
                if not hasattr(launcher, attr)
            ]

            if missing_launcher_attrs:
                return False, f"Launcher attributi mancanti: {missing_launcher_attrs} ❌"

            return True, f"Launcher System: Tutti i test passati ✅ (V:{views_count} M:{merge_count} F:{filter_count})"

        except Exception as e:
            return False, f"Errore test launcher: {e}"

    def test_integration(self) -> Tuple[bool, str]:
        """Test integrazione completa"""
        try:
            print("🔗 Test integrazione sistema...")

            # Test workflow completo
            from advanced_database_manager import AdvancedDatabaseManager
            from advanced_excel_tools_gui import AdvancedExcelToolsGUI

            # Scenario: Crea vista -> Carica in GUI -> Esporta configurazione
            db_manager = AdvancedDatabaseManager(TEST_DB_PATH)

            # 1. Crea vista complessa
            complex_filters = [
                {"column": "value", "operator": ">", "value": "10"},
                {"column": "category", "operator": "=", "value": "A"}
            ]

            vista_success = db_manager.save_view(
                "vista_integrazione", "test_data",
                ["name", "value"], complex_filters,
                "Vista per test integrazione", False
            )

            if not vista_success:
                return False, "Creazione vista integrazione fallita ❌"

            # 2. Test query generata
            query = db_manager.build_query_from_config(
                "test_data", ["name", "value"], complex_filters
            )

            # Verifica query complessa
            query_checks = [
                "SELECT [name], [value]" in query,
                "FROM [test_data]" in query,
                "WHERE" in query,
                "[value] > 10" in query,
                "[category] = 'A'" in query,
                "AND" in query
            ]

            if not all(query_checks):
                return False, f"Query complessa errata ❌\nQuery: {query}"

            # 3. Test esecuzione query su dati reali
            conn = sqlite3.connect(TEST_DB_PATH)
            try:
                import pandas as pd
                df = pd.read_sql_query(query, conn)

                if df.empty:
                    return False, "Query non restituisce risultati ❌"

                # Verifica filtri applicati
                if len(df) != 1 or df.iloc[0]['name'] != 'Item3':
                    return False, f"Filtri non applicati correttamente ❌\nRisultati: {df}"

            except ImportError:
                # Fallback senza pandas
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()

                if not results:
                    return False, "Query non restituisce risultati (no pandas) ❌"

            finally:
                conn.close()

            # 4. Test GUI inizializzazione con dati
            gui = AdvancedExcelToolsGUI()
            gui.load_saved_views()

            if not gui.saved_views:
                return False, "GUI non carica viste salvate ❌"

            vista_trovata = any(
                v['name'] == 'vista_integrazione'
                for v in gui.saved_views
            )

            if not vista_trovata:
                return False, "Vista integrazione non trovata in GUI ❌"

            gui.root.destroy()

            return True, "Integration Test: Workflow completo passato ✅"

        except Exception as e:
            return False, f"Errore test integrazione: {e}"

    def test_performance(self) -> Tuple[bool, str]:
        """Test performance sistema"""
        try:
            print("⚡ Test performance...")

            import time
            from advanced_database_manager import AdvancedDatabaseManager

            db_manager = AdvancedDatabaseManager(TEST_DB_PATH)

            # Test 1: Creazione viste multiple
            start_time = time.time()

            for i in range(10):
                db_manager.save_view(
                    f"perf_test_{i}", "test_data",
                    ["name", "value"],
                    [{"column": "id", "operator": ">", "value": str(i)}],
                    f"Vista performance {i}", False
                )

            creation_time = time.time() - start_time

            # Test 2: Recupero viste multiple
            start_time = time.time()

            for _ in range(5):
                views = db_manager.get_saved_views()

            retrieval_time = time.time() - start_time

            # Test 3: Query building multiple
            start_time = time.time()

            for i in range(20):
                query = db_manager.build_query_from_config(
                    "test_data", ["name", "value"],
                    [{"column": "id", "operator": "=", "value": str(i)}]
                )

            query_time = time.time() - start_time

            # Verifica limiti performance
            performance_checks = [
                creation_time < 2.0,    # Creazione < 2s
                retrieval_time < 1.0,   # Recupero < 1s
                query_time < 0.5        # Query building < 0.5s
            ]

            if not all(performance_checks):
                return False, f"Performance insoddisfacenti ❌\nCreazione: {creation_time:.2f}s, Recupero: {retrieval_time:.2f}s, Query: {query_time:.2f}s"

            return True, f"Performance: Tutti i test passati ✅\nCreazione: {creation_time:.2f}s, Recupero: {retrieval_time:.2f}s, Query: {query_time:.2f}s"

        except Exception as e:
            return False, f"Errore test performance: {e}"

    def cleanup_test_environment(self):
        """Pulisce ambiente di test"""
        print("🧹 Pulizia ambiente test...")

        # Rimuovi file temporanei
        for file_path in [TEST_DB_PATH] + self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"  ⚠️ Impossibile rimuovere {file_path}: {e}")

    def run_all_tests(self) -> Dict[str, Tuple[bool, str]]:
        """Esegue tutti i test"""
        print("🧪 Avvio Test Suite Completa ExcelTools Pro Advanced")
        print("=" * 70)

        # Lista test da eseguire
        tests = [
            ("Imports", self.test_imports),
            ("Database Manager", self.test_database_manager),
            ("Graphical Selector", self.test_graphical_selector),
            ("GUI Components", self.test_gui_components),
            ("Launcher System", self.test_launcher_system),
            ("Integration", self.test_integration),
            ("Performance", self.test_performance)
        ]

        results = {}

        # Esegui ogni test
        for test_name, test_func in tests:
            try:
                print(f"\n{'='*10} {test_name} {'='*10}")
                success, message = test_func()
                results[test_name] = (success, message)

                status_icon = "✅" if success else "❌"
                print(f"{status_icon} {test_name}: {message}")

            except Exception as e:
                error_msg = f"Errore critico: {e}\n{traceback.format_exc()}"
                results[test_name] = (False, error_msg)
                print(f"❌ {test_name}: {error_msg}")

        return results

    def generate_test_report(self, results: Dict[str, Tuple[bool, str]]):
        """Genera report test"""
        print("\n" + "="*70)
        print("📊 REPORT TEST FINALE")
        print("="*70)

        passed = sum(1 for success, _ in results.values() if success)
        total = len(results)
        success_rate = (passed / total) * 100

        print(f"\n🎯 RISULTATI GENERALI:")
        print(f"   Test Passati: {passed}/{total} ({success_rate:.1f}%)")

        if success_rate >= 90:
            status = "🟢 ECCELLENTE"
        elif success_rate >= 75:
            status = "🟡 BUONO"
        elif success_rate >= 50:
            status = "🟠 SUFFICIENTE"
        else:
            status = "🔴 INSUFFICIENTE"

        print(f"   Status Globale: {status}")

        print(f"\n📋 DETTAGLI TEST:")
        for test_name, (success, message) in results.items():
            icon = "✅" if success else "❌"
            print(f"   {icon} {test_name}")
            if not success:
                # Mostra solo prima riga del messaggio di errore
                error_summary = message.split('\n')[0]
                print(f"      └─ {error_summary}")

        print(f"\n🔧 RACCOMANDAZIONI:")
        if success_rate < 100:
            print("   • Verificare dipendenze mancanti")
            print("   • Controllare permessi file system")
            print("   • Aggiornare pacchetti Python")
        else:
            print("   • Sistema completamente funzionante")
            print("   • Pronto per uso in produzione")

        print(f"\n🏢 ExcelTools Pro Advanced v4.0 - Test Suite Completata")
        print("="*70)

        return success_rate >= 75


def main():
    """Funzione principale test"""
    tester = AdvancedSystemTester()

    try:
        # Esegui tutti i test
        results = tester.run_all_tests()

        # Genera report
        success = tester.generate_test_report(results)

        return success

    finally:
        # Pulizia sempre eseguita
        tester.cleanup_test_environment()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
