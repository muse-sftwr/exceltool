#!/usr/bin/env python3
"""
Script per correggere definitivamente tutti gli errori rimanenti
"""

import os
import re
import subprocess


def fix_syntax_error_in_file(file_path):
    """Corregge errore di sintassi f-string"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Corregge f-string non terminata
        content = re.sub(r'f"([^"]*)"([^{]*)', r'"\1"\2', content)
        content = re.sub(r"f'([^']*)'([^{]*)", r"'\1'\2", content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Corretta sintassi in {file_path}")

    except Exception as e:
        print(f"❌ Errore in {file_path}: {e}")


def apply_autopep8_aggressive():
    """Applica correzioni aggressive con autopep8"""
    print("🔧 Applicando correzioni autopep8 aggressive...")

    try:
        # Installa autopep8 se non presente
        subprocess.run(['pip', 'install', 'autopep8'], check=True, capture_output=True)

        # Applica correzioni aggressive
        result = subprocess.run([
            'autopep8', '--in-place', '--aggressive', '--aggressive',
            '--max-line-length=79', '*.py'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Correzioni autopep8 applicate")
        else:
            print(f"⚠️  Autopep8 warning: {result.stderr}")

    except subprocess.CalledProcessError:
        print("⚠️  Autopep8 non disponibile, continuando con correzioni manuali")
    except Exception as e:
        print(f"❌ Errore autopep8: {e}")


def manual_fix_remaining():
    """Correzioni manuali finali"""
    print("🛠️  Applicando correzioni manuali finali...")

    files_to_fix = [
        'create_test_files.py',
        'fix_all_complete.py',
        'fix_all_files.py',
        'fix_unused_imports.py',
        'generate_test_data.py',
        'simple_app.py',
        'fix_final.py'
    ]

    for file_path in files_to_fix:
        if os.path.exists(file_path):
            fix_specific_file_issues(file_path)


def fix_specific_file_issues(file_path):
    """Corregge problemi specifici per file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip() + '\n'

            # Rimuovi righe vuote eccessive (E303)
            if line.strip() == '':
                # Conta righe vuote consecutive
                blank_count = 1
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    blank_count += 1
                    j += 1

                # Mantieni massimo 2 righe vuote
                for _ in range(min(2, blank_count)):
                    fixed_lines.append('\n')

                i = j
                continue

            # Correggi indentazione problematica (E131, E128, E122)
            if i > 0 and line.startswith(' '):
                prev_line = lines[i-1].rstrip()

                # Se la linea precedente termina con continuazione
                if prev_line.endswith(('(', '[', '{', '\\', ',')):
                    # Calcola indentazione corretta
                    prev_indent = len(prev_line) - len(prev_line.lstrip())

                    # Standard: +4 spazi per continuazione
                    correct_indent = prev_indent + 4
                    current_indent = len(line) - len(line.lstrip())

                    if current_indent != correct_indent and line.strip():
                        fixed_line = ' ' * correct_indent + line.lstrip()
                        fixed_lines.append(fixed_line)
                        i += 1
                        continue

            # Spezza righe troppo lunghe rimanenti (E501)
            if len(line.rstrip()) > 79:
                # Strategia semplice: spezza alla prima virgola dopo pos 60
                if ',' in line:
                    for pos in range(60, 79):
                        if pos < len(line) and line[pos] == ',':
                            indent = len(line) - len(line.lstrip())
                            part1 = line[:pos+1] + '\n'
                            part2 = ' ' * (indent + 4) + line[pos+1:].lstrip()
                            fixed_lines.append(part1)
                            fixed_lines.append(part2)
                            i += 1
                            break
                    else:
                        fixed_lines.append(line)
                        i += 1
                else:
                    fixed_lines.append(line)
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1

        # Scrivi file corretto
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)

        print(f"✅ Corretto {file_path}")

    except Exception as e:
        print(f"❌ Errore correggendo {file_path}: {e}")


def main():
    """Funzione principale per correzione finale"""
    print("🎯 CORREZIONE FINALE DEFINITIVA")
    print("==============================")

    # 1. Correggi errore di sintassi in fix_unused_imports.py
    if os.path.exists('fix_unused_imports.py'):
        fix_syntax_error_in_file('fix_unused_imports.py')

    # 2. Prova autopep8 aggressivo
    apply_autopep8_aggressive()

    # 3. Correzioni manuali specifiche
    manual_fix_remaining()

    # 4. Verifica finale
    print("\n🔍 Verifica finale...")

    try:
        result = subprocess.run(['py', '-m', 'flake8', '.', '--count'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("🎉 SUCCESSO TOTALE: Tutti i file sono conformi PEP8!")
        else:
            errors = result.stdout.strip()
            if errors.isdigit():
                print(f"⚠️  Rimangono {errors} errori")
            else:
                print("⚠️  Alcuni errori persistono")
                # Mostra solo i primi 10 errori
                error_lines = result.stdout.strip().split('\n')[:10]
                for error in error_lines:
                    if error.strip():
                        print(f"   {error}")

    except Exception as e:
        print(f"❌ Errore nella verifica: {e}")

    # 5. Verifica file principali
    print(f"\n📋 Status file principali:")
    main_files = ['app.py', 'fix_code.py']

    for file in main_files:
        if os.path.exists(file):
            try:
                result = subprocess.run(['py', '-m', 'flake8', file],
                                      capture_output=True, text=True)
                status = "✅ PERFETTO" if result.returncode == 0 else "⚠️  Ha errori"
                print(f"  {file}: {status}")
            except:
                print(f"  {file}: ❌ Errore verifica")


if __name__ == "__main__":
    main()
