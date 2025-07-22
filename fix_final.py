#!/usr/bin/env python3
"""
Script finale per correggere gli errori rimanenti più complessi
"""

import os
import re
import subprocess


def fix_remaining_errors():
    """Corregge manualmente gli errori più complessi rimasti"""

    # Lista dei file con errori rimanenti
    problem_files = [
        'create_test_files.py',
            'fix_all_complete.py',
            'fix_all_files.py',
            'fix_unused_imports.py',
            'generate_test_data.py',
            'simple_app.py'
    ]

    print("🔧 Correggendo errori complessi rimanenti...")

    for file_path in problem_files:
        if os.path.exists(file_path):
            print(f"\n📝 Correggendo {file_path}...")
            fix_complex_file_errors(file_path)

    print("\n✅ Correzioni finali completate!")


def fix_complex_file_errors(file_path):
    """Corregge errori complessi specifici per file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Correzioni specifiche per tipo di errore
        content = fix_f_strings_without_placeholders(content)
        content = fix_complex_line_breaks(content)
        content = fix_continuation_alignment(content)
        content = remove_trailing_commas_in_lists(content)

        # Salva se modificato
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {file_path} corretto")
        else:
            print(f"  ℹ️  {file_path} non necessita modifiche")

    except Exception as e:
        print(f"  ❌ Errore con {file_path}: {e}")


def fix_f_strings_without_placeholders(content):
    """Corregge f-string senza placeholder (F541)"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Cerca f-string senza {}
        if re.search(r'f["\'][^{}"\']*["\']', line) and '{' not in line:
            # Rimuovi f prefix se non ci sono placeholder
            fixed_line = re.sub(r'f(["\'][^{}"\']*["\'])', r'\1', line)
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_complex_line_breaks(content):
    """Corregge interruzioni di riga complesse per E501"""
    lines = content.split('\n')
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if len(line) > 79:
            # Casi specifici di righe lunghe difficili

            # 1. Dizionari/liste con molti elementi
            if ('{' in line and '}' in line) or ('[' in line and ']' in line):
                fixed_lines.extend(fix_dict_or_list_line(line))
                i += 1
                continue

            # 2. Messaggi di errore lunghi
            if 'error_msg =' in line or 'message =' in line:
                fixed_lines.extend(fix_message_assignment(line))
                i += 1
                continue

            # 3. Chiamate con molti parametri booleani
            if line.count('=') > 2 and ('True' in line or 'False' in line):
                fixed_lines.extend(fix_parameter_line(line))
                i += 1
                continue

        fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines)


def fix_dict_or_list_line(line):
    """Spezza righe con dizionari o liste"""
    indent = len(line) - len(line.lstrip())

    # Per dizionari
    if '{' in line and '}' in line and ':' in line:
        # Trova il contenuto del dizionario
        brace_start = line.find('{')
        brace_end = line.rfind('}')

        before = line[:brace_start + 1]
        content = line[brace_start + 1:brace_end]
        after = line[brace_end:]

        if ',' in content:
            items = [item.strip() for item in content.split(',') if item.strip()]

            lines = [before]
            for i, item in enumerate(items):
                comma = ',' if i < len(items) - 1 else ''
                lines.append(' ' * (indent + 4) + item + comma)
            lines.append(' ' * indent + after)

            return lines

    # Per liste
    elif '[' in line and ']' in line:
        bracket_start = line.find('[')
        bracket_end = line.rfind(']')

        before = line[:bracket_start + 1]
        content = line[bracket_start + 1:bracket_end]
        after = line[bracket_end:]

        if ',' in content:
            items = [item.strip() for item in content.split(',') if item.strip()]

            lines = [before]
            for i, item in enumerate(items):
                comma = ',' if i < len(items) - 1 else ''
                lines.append(' ' * (indent + 4) + item + comma)
            lines.append(' ' * indent + after)

            return lines

    return [line]


def fix_message_assignment(line):
    """Spezza assegnazioni di messaggi lunghi"""
    indent = len(line) - len(line.lstrip())

    # Trova il pattern var = "messaggio lungo"
    if '=' in line and ('"' in line or "'" in line):
        parts = line.split('=', 1)
        if len(parts) == 2:
            var_part = parts[0].strip()
            value_part = parts[1].strip()

            # Se il valore è una stringa lunga
            if len(line) > 79:
                return [
                    ' ' * indent + var_part + ' = (',
                        ' ' * (indent + 4) + value_part,
                        ' ' * indent + ')'
                ]

    return [line]


def fix_parameter_line(line):
    """Spezza righe con molti parametri"""
    indent = len(line) - len(line.lstrip())

    # Trova chiamate di funzione con molti parametri
    if '(' in line and ')' in line:
        paren_start = line.find('(')
        paren_end = line.rfind(')')

        before = line[:paren_start + 1]
        params = line[paren_start + 1:paren_end]
        after = line[paren_end:]

        if ',' in params and len(line) > 79:
            param_list = [p.strip() for p in params.split(',') if p.strip()]

            lines = [before]
            for i, param in enumerate(param_list):
                comma = ',' if i < len(param_list) - 1 else ''
                lines.append(' ' * (indent + 4) + param + comma)
            lines.append(' ' * indent + after)

            return lines

    return [line]


def fix_continuation_alignment(content):
    """Corregge allineamento delle continuazioni (E128)"""
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        if i == 0:
            fixed_lines.append(line)
            continue

        prev_line = lines[i - 1]

        # Se la linea precedente termina con continuazione
        if prev_line.rstrip().endswith(('(', '[', '{')):
            # Calcola l'indentazione corretta
            prev_indent = len(prev_line) - len(prev_line.lstrip())
            current_indent = len(line) - len(line.lstrip())

            # L'indentazione dovrebbe essere +4 dalla linea precedente
            correct_indent = prev_indent + 4

            if current_indent != correct_indent and line.strip():
                fixed_line = ' ' * correct_indent + line.lstrip()
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def remove_trailing_commas_in_lists(content):
    """Rimuove virgole finali problematiche"""
    # Rimuovi virgole prima di parentesi/bracket chiusi
    content = re.sub(r',(\s*[)\]}])', r'\1', content)
    return content


def main():
    """Funzione principale"""
    print("🎯 CORREZIONE FINALE ERRORI COMPLESSI")
    print("====================================")

    # Conta errori prima
    try:
        result = subprocess.run(['py', '-m', 'flake8', '.', '--count'],
            capture_output=True, text=True)
        errors_before = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        print(f"📊 Errori prima della correzione: {errors_before}")
    except:
        errors_before = 0

    # Applica correzioni
    fix_remaining_errors()

    # Conta errori dopo
    try:
        result = subprocess.run(['py', '-m', 'flake8', '.', '--count'],
            capture_output=True, text=True)
        errors_after = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        print(f"📊 Errori dopo la correzione: {errors_after}")

        if errors_after < errors_before:
            fixed = errors_before - errors_after
            print(f"✅ {fixed} errori corretti!")

        if errors_after == 0:
            print("🎉 TUTTI GLI ERRORI SONO STATI RISOLTI!")

    except Exception as e:
        print(f"⚠️  Errore nel conteggio finale: {e}")

    # Verifica dettagliata file principali
    print(f"\n📋 Verifica file principali:")
    main_files = ['app.py', 'fix_code.py', 'create_test_files.py']

    for file in main_files:
        if os.path.exists(file):
            try:
                result = subprocess.run(['py', '-m', 'flake8',
                    file, '--count'],
                    capture_output=True, text=True)
                file_errors = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                status = "✅ PULITO" if file_errors == 0 else f"⚠️  {file_errors} errori"
                print(f"  {file}: {status}")
            except:
                print(f"  {file}: ❌ Errore verifica")


if __name__ == "__main__":
    main()
