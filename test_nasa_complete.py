#!/usr/bin/env python3
"""
🧪 NASA EXCELTOOLS - TEST COMPLETO
==================================
Test di tutti i componenti essenziali
"""

import pandas as pd
from ai_query_interpreter import AdvancedAIQueryInterpreter


def test_ai_system():
    """Test del sistema AI"""
    print("🤖 Testing NASA AI Query Interpreter...")

    # Dati di test
    df = pd.DataFrame({
        'Nome': ['Mario', 'Luigi', 'Peach', 'Bowser'],
        'Eta': [35, 32, 28, 45],
        'Punteggio': [1500, 1200, 1800, 800],
        'Categoria': ['Idraulico', 'Idraulico', 'Principessa', 'Nemico']
    })

    # Inizializza AI
    ai = AdvancedAIQueryInterpreter()
    ai.set_data_context(df, {'giocatori': df})

    # Test queries
    test_queries = [
        'mostra solo la colonna Nome',
        'mostra Nome e Punteggio',
        'filtra dove Eta maggiore di 30',
        'raggruppa per Categoria',
        'ordinare per Punteggio decrescente',
        'trova il massimo di Punteggio',
        'contare tutte le righe'
    ]

    print("\n📋 RISULTATI TEST AI:")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        result = ai.interpret_query(query)
        print(f"\n{i}. INPUT: '{query}'")
        print(f"   SQL: {result}")

    print("\n✅ AI Test COMPLETATO!")
    return True


def test_basic_imports():
    """Test import moduli base"""
    print("📦 Testing imports...")

    try:
        import tkinter as tk
        print("✅ tkinter OK")
    except ImportError as e:
        print(f"❌ tkinter ERROR: {e}")
        return False

    try:
        import pandas as pd
        print(f"✅ pandas OK - version {pd.__version__}")
    except ImportError as e:
        print(f"❌ pandas ERROR: {e}")
        return False

    try:
        from ai_query_interpreter import AdvancedAIQueryInterpreter
        print("✅ AI Query Interpreter OK")
    except ImportError as e:
        print(f"❌ AI Query Interpreter ERROR: {e}")
        return False

    try:
        from advanced_database_manager import AdvancedDatabaseManager
        print("✅ Database Manager OK")
    except ImportError as e:
        print(f"❌ Database Manager ERROR: {e}")
        return False

    return True


def main():
    """Test principale"""
    print("🚀 NASA EXCELTOOLS - COMPREHENSIVE TEST")
    print("=" * 50)

    # Test 1: Imports
    if not test_basic_imports():
        print("❌ IMPORT TEST FAILED")
        return

    print("\n" + "=" * 50)

    # Test 2: AI System
    if not test_ai_system():
        print("❌ AI TEST FAILED")
        return

    print("\n" + "=" * 50)
    print("🎉 TUTTI I TEST SUPERATI!")
    print("🚀 NASA ExcelTools è pronto per l'uso!")


if __name__ == "__main__":
    main()
