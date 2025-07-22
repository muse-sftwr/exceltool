#!/usr/bin/env python3
"""
🧪 TEST AI QUERY INTERPRETER
============================

Test delle capacità dell'AI per generare SQL da linguaggio naturale.
"""

from ai_query_interpreter import AdvancedAIQueryInterpreter
import pandas as pd


def test_ai_queries():
    """Test delle funzionalità AI"""
    print("🤖 TEST AI QUERY INTERPRETER")
    print("=" * 50)

    # Crea dati di esempio
    sample_data = pd.DataFrame({
        'Nome': ['Mario', 'Luigi', 'Peach', 'Bowser', 'Yoshi'],
        'Età': [35, 32, 28, 45, 25],
        'Punteggio': [1500, 1200, 1800, 800, 1300],
        'Categoria': ['Idraulico', 'Idraulico', 'Principessa', 'Nemico', 'Dinosauro']
    })

    # Inizializza AI
    ai = AdvancedAIQueryInterpreter()
    ai.set_data_context(sample_data, {'giocatori': sample_data})

    # Test query
    test_queries = [
        "mostra solo la colonna Nome",
        "seleziona Nome e Età",
        "fammi vedere tutti i dati",
        "filtra dove Età maggiore di 30",
        "raggruppa per Categoria",
        "ordina per Punteggio decrescente",
        "primi 3 giocatori",
        "conta quanti sono",
        "media del Punteggio",
        "trova duplicati",
        "valori unici in Categoria"
    ]

    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        result = ai.interpret_query(query)
        print(f"🔍 SQL generato:")
        print(result)
        print("-" * 40)


if __name__ == "__main__":
    test_ai_queries()
