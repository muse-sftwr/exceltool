"""
🎯 LAUNCHER DEFINITIVO - NASA EXCELTOOLS COMPLETE
=================================================
Test finale e avvio della piattaforma completa
"""


def main():
    print("🚀 NASA EXCELTOOLS COMPLETE - FINAL LAUNCHER")
    print("=" * 55)
    print()

    # Test 1: Pandas
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} - Ready")
    except ImportError:
        print("❌ Pandas missing - please install: pip install pandas")
        return False

    # Test 2: Tkinter

    # Test 3: AI Module
    try:
        from ai_query_interpreter import AdvancedAIQueryInterpreter
        ai = AdvancedAIQueryInterpreter()
        result = ai.interpret_query("mostra colonna 1")
        print(f"✅ AI Module - Ready ({result[:30]}...)")
    except Exception as e:
        print(f"⚠️ AI Module issue: {e}")

    # Test 4: Database
    try:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.close()
        print("✅ SQLite Database - Ready")
    except Exception:
        print("❌ Database error")
        return False

    print()
    print("🔥 ALL SYSTEMS GO - LAUNCHING COMPLETE PLATFORM!")
    print("=" * 55)
    print()

    # LAUNCH MAIN APP
    try:
        from exceltools_unified_complete import ExcelToolsUnifiedComplete

        print("🚀 Initializing NASA ExcelTools Complete...")
        app = ExcelToolsUnifiedComplete()

        print("✅ Application initialized successfully!")
        print("🎯 Features available:")
        print("   • AI-powered query generation")
        print("   • Advanced data import/export")
        print("   • Real-time filtering and analysis")
        print("   • Database management")
        print("   • Multi-file merge operations")
        print("   • Saved views and templates")
        print()
        print("🌟 Starting GUI interface...")

        app.run()

    except Exception as e:
        print(f"❌ Launch error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()
