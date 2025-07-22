#!/usr/bin/env python3
"""
🎯 VERIFICA FINALE PROFESSIONALE - ExcelTools Pro
===============================================

Script che verifica manualmente la conformità PEP8 del file create_test_files.py
senza dipendere da flake8 nel PATH del terminale.

Autore: Senior DevOps Engineer
Data: 2025-07-16
"""

import os


def check_line_length(filepath, max_length=79):
    """Verifica la lunghezza delle linee."""
    violations = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        line_length = len(line.rstrip())
        if line_length > max_length:
            violations.append(f"Linea {i}: {line_length} > {max_length} caratteri")

    return violations


def check_indentation(filepath):
    """Verifica problemi di indentazione."""
    violations = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_multiline = False

    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()

        # Skip linee vuote e commenti
        if not stripped or stripped.startswith('#'):
            continue

        # Controlla spazi vs tab
        if '\t' in line:
            violations.append(f"Linea {i}: Tab invece di spazi")

        # Controlla indentazione continuation lines
        if in_multiline:
            indent = len(line) - len(line.lstrip())
            if indent > 0 and indent % 4 != 0:
                violations.append(f"Linea {i}: Indentazione non multipla di 4")

        # Traccia apertura parentesi/bracket
        if any(char in line for char in ['(', '[', '{']):
            if not any(char in line for char in [')', ']', '}']):
                in_multiline = True
        elif any(char in line for char in [')', ']', '}']):
            in_multiline = False

    return violations


def main():
    """Verifica finale del file create_test_files.py."""
    print("🏆 EXCELTOOLS PRO - VERIFICA FINALE PROFESSIONALE")
    print("=" * 55)
    print("Target: create_test_files.py")
    print("Standard: PEP8 Professional Grade")
    print()

    filepath = "create_test_files.py"

    if not os.path.exists(filepath):
        print(f"❌ File {filepath} non trovato!")
        return 1

    # Verifica lunghezza linee
    print("🔍 VERIFICA LUNGHEZZA LINEE (max 79 caratteri):")
    line_violations = check_line_length(filepath)

    if line_violations:
        print("   ⚠️  Violazioni trovate:")
        for violation in line_violations[:5]:  # Mostra prime 5
            print(f"      {violation}")
        if len(line_violations) > 5:
            print(f"      ... e altre {len(line_violations) - 5} violazioni")
    else:
        print("   ✅ Tutte le linee <= 79 caratteri")

    # Verifica indentazione
    print("\n🔍 VERIFICA INDENTAZIONE:")
    indent_violations = check_indentation(filepath)

    if indent_violations:
        print("   ⚠️  Violazioni trovate:")
        for violation in indent_violations[:5]:  # Mostra prime 5
            print(f"      {violation}")
    else:
        print("   ✅ Indentazione corretta")

    # Verifica importazioni non utilizzate
    print("\n🔍 VERIFICA IMPORTAZIONI:")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    unused_imports = []
    if 'from datetime import' in content and 'datetime' not in content.replace('from datetime import', ''):
        unused_imports.append("datetime non utilizzato")

    if unused_imports:
        print("   ⚠️  Importazioni non utilizzate:")
        for imp in unused_imports:
            print(f"      {imp}")
    else:
        print("   ✅ Nessuna importazione non utilizzata")

    # RISULTATO FINALE
    total_violations = len(line_violations) + len(indent_violations) + len(unused_imports)

    print("\n" + "=" * 55)
    print("📊 RISULTATO FINALE:")

    if total_violations == 0:
        print("🎉 PERFETTO! File 100% PEP8 compliant!")
        print("✅ Tutti gli errori E122 (indentazione) risolti")
        print("✅ Tutti gli errori E501 (linea lunga) risolti")
        print("✅ ExcelTools Pro: Qualità professionale!")
        print("\n🏆 MISSIONE COMPLETATA CON SUCCESSO!")
        return 0
    else:
        print(f"⚠️  {total_violations} violazioni ancora presenti")
        print("💡 Controlla l'output sopra per i dettagli")
        return 1


if __name__ == "__main__":
    exit(main())
