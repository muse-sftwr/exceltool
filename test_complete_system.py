#!/usr/bin/env python3
"""
🧪 TEST COMPLETO NASA EXCELTOOLS
Sistema di test per verificare tutte le funzionalità
"""

import sys
import os


def test_basic_imports():
    """Testa import di base"""
    print("🧪 Testing basic imports...")

    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} - OK")
    except ImportError:
        print("❌ Pandas not available")
        return False

    try:
        import tkinter as tk
        print("✅ Tkinter - OK")
    except ImportError:
        print("❌ Tkinter not available")
        return False

    try:
        import sqlite3
        print("✅ SQLite3 - OK")
    except ImportError:
        print("❌ SQLite3 not available")
        return False

    return True


def test_ai_module():
    """Testa modulo AI"""
    print("\n🤖 Testing AI module...")

    try:
        from ai_query_interpreter import AdvancedAIQueryInterpreter
        ai = AdvancedAIQueryInterpreter()

        # Test query
        test_queries = [
            "mostra solo la colonna 1",
            "conta tutte le righe",
            "filtra valori maggiori di 100"
        ]

        for query in test_queries:
            result = ai.interpret_query(query)
            print(f"✅ '{query}' → {result[:50]}...")

        return True

    except Exception as e:
        print(f"❌ AI module error: {e}")
        return False


def test_gui_creation():
    """Testa creazione GUI base"""
    print("\n🖥️ Testing GUI creation...")

    try:
        import tkinter as tk

        # Crea finestra test
        root = tk.Tk()
        root.title("NASA ExcelTools Test")
        root.geometry("400x300")

        label = tk.Label(root, text="✅ GUI Test OK")
        label.pack(pady=20)

        # Distruggi subito
        root.after(1000, root.destroy)
        root.mainloop()

        print("✅ GUI creation - OK")
        return True

    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False


def test_database():
    """Testa database"""
    print("\n💾 Testing database...")

    try:
        import sqlite3
        import pandas as pd

        # Crea database test
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Crea tabella test
        cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER
            )
        """)

        # Inserisci dati test
        test_data = [
            (1, "Test1", 100),
            (2, "Test2", 200),
            (3, "Test3", 300)
        ]

        cursor.executemany(
            "INSERT INTO test_table VALUES (?, ?, ?)",
            test_data)
        conn.commit()

        # Test query
        df = pd.read_sql_query("SELECT * FROM test_table", conn)
        print(f"✅ Database test - {len(df)} rows retrieved")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_complete_app():
    """Testa app completa"""
    print("\n🚀 Testing complete app...")

    try:
        from exceltools_unified_complete import ExcelToolsUnifiedComplete

        # Crea istanza ma non avviare GUI
        app = ExcelToolsUnifiedComplete()

        # Verifica attributi principali
        assert hasattr(app, 'db_path')
        assert hasattr(app, 'current_data')
        assert hasattr(app, 'ai_interpreter')

        print("✅ Complete app initialization - OK")
        return True

    except Exception as e:
        print(f"❌ Complete app error: {e}")
        return False


def main():
    """Funzione principale"""
    print("🧪 NASA EXCELTOOLS - COMPLETE TEST SUITE")
    print("=" * 50)

    tests = [
        ("Basic Imports", test_basic_imports),
        ("AI Module", test_ai_module),
        ("GUI Creation", test_gui_creation),
        ("Database", test_database),
        ("Complete App", test_complete_app)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n▶️ Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")

    print("\n" + "=" * 50)
    print(f"🏁 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED - NASA ExcelTools ready for launch!")

        # Chiedi se avviare l'app
        try:
            response = input("\n🚀 Launch NASA ExcelTools now? (y/N): ")
            if response.lower() == 'y':
                print("\n🚀 Launching NASA ExcelTools Complete...")
                from exceltools_unified_complete import ExcelToolsUnifiedComplete
                app = ExcelToolsUnifiedComplete()
                app.run()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    else:
        print("⚠️ Some tests failed - please check the issues above")


if __name__ == "__main__":
    main()
