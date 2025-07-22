#!/usr/bin/env python3
# cSpell:disable
"""
Script per correggere automaticamente tutti gli errori di formattazione PEP8
"""

import re
import ast


def remove_unused_imports(content):
    """Rimuove le importazioni non utilizzate"""
    lines = content.split('\n')

    # Trova tutte le importazioni
    import_lines = []
    import_info = {}
    other_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            import_lines.append((i, line))

            # Estrai i nomi importati
            if stripped.startswith('import '):
                # import module as alias, module2
                import_part = stripped[7:].strip()
                modules = [m.strip() for m in import_part.split(',')]
                for module in modules:
                    if ' as ' in module:
                        module_name = module.split(' as ')[1].strip()
                    else:
                        module_name = module.split('.')[0]
                    import_info[module_name] = (i, line)

            elif stripped.startswith('from '):
                # from module import name1, name2 as alias
                parts = stripped.split(' import ')
                if len(parts) == 2:
                    imports = parts[1].strip()
                    names = [n.strip() for n in imports.split(',')]
                    for name in names:
                        if ' as ' in name:
                            import_name = name.split(' as ')[1].strip()
                        else:
                            import_name = name.strip()
                        import_info[import_name] = (i, line)
        else:
            other_lines.append((i, line))

    # Trova i nomi utilizzati nel codice
    used_names = set()
    code_content = '\n'.join([line for _, line in other_lines])

    # Cerca i nomi utilizzati con regex semplice
    for name in import_info.keys():
        # Cerca pattern come: nome.qualcosa, nome(, nome[, nome =, nome,
        patterns = [
            rf'\b{re.escape(name)}\.',  # nome.metodo
            rf'\b{re.escape(name)}\(',  # nome(args)
            rf'\b{re.escape(name)}\[',  # nome[index]
            rf'\b{re.escape(name)}\s*=',  # nome = value
            rf'\b{re.escape(name)}\s*,',  # nome, altro
            rf'\b{re.escape(name)}\s*\)',  # func(nome)
            rf'\b{re.escape(name)}$',  # nome alla fine di riga
            rf'^\s*{re.escape(name)}\s*$',  # nome da solo
        ]

        for pattern in patterns:
            if re.search(pattern, code_content, re.MULTILINE):
                used_names.add(name)
                break

    # Ricostruisci il file senza importazioni inutilizzate
    result_lines = []

    for i, line in lines:
        if i in [info[0] for info in import_info.values()]:
            # È una riga di import, controlla se è utilizzata
            stripped = line.strip()
            should_keep = False

            if stripped.startswith('import '):
                import_part = stripped[7:].strip()
                modules = [m.strip() for m in import_part.split(',')]
                used_modules = []

                for module in modules:
                    if ' as ' in module:
                        module_name = module.split(' as ')[1].strip()
                    else:
                        module_name = module.split('.')[0]

                    if module_name in used_names:
                        used_modules.append(module)

                if used_modules:
                    if len(used_modules) == len(modules):
                        result_lines.append(line)
                    else:
                        # Ricostruisci import solo con moduli utilizzati
                        new_import = 'import ' + ', '.join(used_modules)
                        indent = len(line) - len(line.lstrip())
                        result_lines.append(' ' * indent + new_import)

            elif stripped.startswith('from '):
                parts = stripped.split(' import ')
                if len(parts) == 2:
                    module_part = parts[0]
                    imports = parts[1].strip()
                    names = [n.strip() for n in imports.split(',')]
                    used_imports = []

                    for name in names:
                        if ' as ' in name:
                            import_name = name.split(' as ')[1].strip()
                        else:
                            import_name = name.strip()

                        if import_name in used_names:
                            used_imports.append(name)

                    if used_imports:
                        if len(used_imports) == len(names):
                            result_lines.append(line)
                        else:
                            # Ricostruisci from import solo con nomi utilizzati
                            new_import = f"{module_part} import {', '.join(used_imports)}"
                            indent = len(line) - len(line.lstrip())
                            result_lines.append(' ' * indent + new_import)
        else:
            result_lines.append(line)

    return '\n'.join(result_lines)


def fix_line_length(content):
    """Corregge righe troppo lunghe"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if len(line) <= 79:
            fixed_lines.append(line)
            continue

        # Se è una stringa lunga, spezzala
        if '"""' in line or "'''" in line:
            fixed_lines.append(line)
            continue

        # Se è un commento, spezzalo
        if line.strip().startswith('#'):
            if len(line) > 79:
                # Spezza il commento
                indent = len(line) - len(line.lstrip())
                comment_text = line.strip()[1:].strip()

                # Spezza in parole
                words = comment_text.split()
                current_line = ' ' * indent + '#'

                for word in words:
                    if len(current_line + ' ' + word) <= 79:
                        current_line += ' ' + word
                    else:
                        fixed_lines.append(current_line)
                        current_line = ' ' * indent + '# ' + word

                if current_line.strip() != '#':
                    fixed_lines.append(current_line)
            else:
                fixed_lines.append(line)
            continue

        # Se è codice, cerca di spezzarlo intelligentemente
        indent = len(line) - len(line.lstrip())
        content_line = line.strip()

        # Funzioni con parametri lunghi
        if '(' in content_line and ')' in content_line:
            # Spezza parametri di funzione
            parts = content_line.split('(', 1)
            if len(parts) == 2:
                func_part = parts[0]
                params_part = parts[1].rsplit(')', 1)[0]
                closing_part = parts[1].rsplit(')', 1)[1]
                end_part = ')' + closing_part if ')' in parts[1] else ''

                if ',' in params_part:
                    # Spezza i parametri
                    params = [p.strip() for p in params_part.split(',')]

                    fixed_lines.append(' ' * indent + func_part + '(')

                    for i, param in enumerate(params):
                        if param:
                            comma = ',' if i < len(params) - 1 else ''
                            param_line = ' ' * (indent + 4) + param + comma
                            fixed_lines.append(param_line)

                    fixed_lines.append(' ' * indent + end_part)
                    continue

        # Operazioni lunghe
        operators = [' and ', ' or ', ' + ', ' - ', ' * ', ' / ']
        if any(op in content_line for op in operators):
            # Trova l'operatore per spezzare
            for op in operators:
                if op in content_line:
                    parts = content_line.split(op)
                    if len(parts) > 1:
                        fixed_lines.append(' ' * indent + parts[0] + ' \\')
                        for i, part in enumerate(parts[1:], 1):
                            if i == len(parts) - 1:
                                line_part = ' ' * (indent + 4) + op.strip()
                                line_part += ' ' + part
                                fixed_lines.append(line_part)
                            else:
                                line_part = ' ' * (indent + 4) + op.strip()
                                line_part += ' ' + part + ' \\'
                                fixed_lines.append(line_part)
                        break
            else:
                # Non trovato operatore, spezza alla metà
                mid = len(content_line) // 2
                space_pos = content_line.rfind(' ', 0, mid)
                if space_pos > 0:
                    first_part = ' ' * indent + content_line[:space_pos]
                    first_part += ' \\'
                    fixed_lines.append(first_part)
                    second_part = ' ' * (indent + 4)
                    second_part += content_line[space_pos:].strip()
                    fixed_lines.append(second_part)
                else:
                    # Non modificare se non si può spezzare
                    fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def remove_trailing_whitespace(content):
    """Rimuove spazi bianchi finali"""
    lines = content.split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def fix_blank_lines(content):
    """Corregge le righe vuote secondo PEP8"""
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        # Rimuovi righe vuote multiple consecutive
        if line.strip() == '':
            # Controlla se la riga precedente è anche vuota
            if i > 0 and fixed_lines and fixed_lines[-1].strip() == '':
                continue  # Salta riga vuota duplicata

        # Aggiungi 2 righe vuote prima delle definizioni di classe
        if line.strip().startswith('class '):
            if i > 0 and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
                fixed_lines.append('')

        # Aggiungi 1 riga vuota prima delle definizioni di funzione
        elif line.strip().startswith('def '):
            if i > 0 and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_imports(content):
    """Ottimizza le importazioni"""
    lines = content.split('\n')

    # Trova le sezioni di import
    import_lines = []
    other_lines = []
    in_import_section = True

    for line in lines:
        line_starts = ('import ', 'from ')
        if (line.strip().startswith(line_starts) or
                (line.strip() == '' and in_import_section)):
            import_lines.append(line)
        else:
            if line.strip() and not line.strip().startswith('#'):
                in_import_section = False
            other_lines.append(line)

    # Raggruppa import
    std_imports = []
    third_party_imports = []
    local_imports = []

    for line in import_lines:
        if line.strip() == '' or line.strip().startswith('#'):
            continue

        std_modules = ['os', 'sys', 'datetime', 'threading',
                       'logging', 'sqlite3']
        if any(mod in line for mod in std_modules):
            std_imports.append(line)
        elif 'from typing' in line:
            std_imports.append(line)
        else:
            third_party_imports.append(line)

    # Ricostruisci import organizzati
    organized_imports = []

    if std_imports:
        organized_imports.extend(sorted(std_imports))
        organized_imports.append('')

    if third_party_imports:
        organized_imports.extend(sorted(third_party_imports))
        organized_imports.append('')

    if local_imports:
        organized_imports.extend(sorted(local_imports))
        organized_imports.append('')

    # Rimuovi l'ultima riga vuota se presente
    if organized_imports and organized_imports[-1] == '':
        organized_imports.pop()

    return '\n'.join(organized_imports + other_lines)


def fix_spacing(content):
    """Corregge la spaziatura"""
    # Corregge spazi intorno agli operatori
    content = re.sub(r'([^=!<>])=([^=])', r'\1 = \2', content)
    content = re.sub(r'([^=!<>])==([^=])', r'\1 == \2', content)
    content = re.sub(r'([^=!<>])!=([^=])', r'\1 != \2', content)
    content = re.sub(r'([^<])<=([^<])', r'\1 <= \2', content)
    content = re.sub(r'([^>])>=([^>])', r'\1 >= \2', content)

    # Corregge spazi dopo virgole
    content = re.sub(r',([^\s])', r', \1', content)

    return content


def main():
    """Corregge tutti gli errori di formattazione"""
    file_path = "app.py"

    print("🔧 Inizio correzione automatica errori PEP8...")

    # Leggi il file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("📝 Applicazione correzioni...")

    # Applica tutte le correzioni
    content = remove_trailing_whitespace(content)
    print("  ✅ Rimossi spazi bianchi finali")

    content = fix_line_length(content)
    print("  ✅ Corrette righe troppo lunghe")

    content = fix_blank_lines(content)
    print("  ✅ Corrette righe vuote")

    content = fix_imports(content)
    print("  ✅ Ottimizzate importazioni")

    content = fix_spacing(content)
    print("  ✅ Corretta spaziatura")

    content = remove_unused_imports(content)
    print("  ✅ Rimosse importazioni non utilizzate")

    # Salva il file corretto
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Correzioni completate!")
    print(f"📁 File aggiornato: {file_path}")


if __name__ == "__main__":
    main()
