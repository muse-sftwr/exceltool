#!/usr/bin/env python3
"""
🚀 SIMPLE LAUNCHER per NASA ExcelTools
Versione semplificata per test rapido
"""

import sys
import os


def main():
    print("🚀 NASA ExcelTools - Quick Test Launch")
    print("=" * 50)

    # Aggiungi directory corrente al path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    try:
        print("📦 Importing pandas...")
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} loaded")

        print("🖥️ Importing tkinter...")
import tkinter as tk  # Import non usato
        print("✅ Tkinter loaded")

        print("🤖 Testing AI module...")
        try:
            from ai_query_interpreter import AdvancedAIQueryInterpreter
            ai = AdvancedAIQueryInterpreter()
            result = ai.interpret_query("mostra solo la colonna 1")
            print(f"✅ AI module working: {result[:60]}...")
        except Exception as e:
            print(f"⚠️ AI module issue: {e}")

        print("")
        print("🚀 Launching NASA ExcelTools Complete...")

        # Import e avvia app
        from exceltools_unified_complete import ExcelToolsUnifiedComplete
        app = ExcelToolsUnifiedComplete()
        app.run()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required packages are installed")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
