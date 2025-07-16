#!/usr/bin/env python3
"""

Script completo per correggere automaticamente tutti gli errori di linting PEP8

Risolve F401, E501, E302, E305, W293, W291, E128, E122 e altri errori comuni

"""

import os
import re

import subprocess


class CompleteLintFixer:
    """Correttore completo per tutti gli errori di linting"""

    def __init__(self):
        self.errors_fixed = {
            'F401': 0,  # Importazioni non utilizzate
            'E501': 0,  # Righe troppo lunghe
            'E302': 0,  # Righe vuote mancanti prima funzioni
            'E305': 0,  # Righe vuote mancanti dopo funzioni/classi
            'W293': 0,  # Righe vuote con spazi
            'W291': 0,  # Spazi finali
            'W292': 0,  # Newline finale mancante
            'E128': 0,  # Indentazione continuazione
            'E122': 0,  # Indentazione continuazione mancante
            'E261': 0,  # Spazi prima commenti inline
        }


    def fix_file(self, file_path):
        """Corregge tutti gli errori in un file"""
        print(f"\n🔧 Correggendo {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Applica tutte le correzioni in sequenza
            content = self.remove_unused_imports(content)
            content = self.fix_trailing_whitespace(content)
            content = self.fix_blank_lines_with_whitespace(content)
            content = self.fix_line_length(content)
            content = self.fix_blank_lines(content)
            content = self.fix_indentation_errors(content)
            content = self.fix_inline_comments(content)
            content = self.ensure_final_newline(content)

            # Salva solo se ci sono cambiamenti
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("  ✅ File corretto con successo")
                return True
            else:
                print("  ℹ️  Nessuna correzione necessaria")
                return False

        except Exception as e:
            print(f"  ❌ Errore: {e}")
            return False


    def remove_unused_imports(self, content):
        """Rimuove importazioni non utilizzate (F401)"""
        lines = content.split('\n')
        import_info = {}
        other_lines = []

        # Identifica importazioni e codice
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                if stripped.startswith('import '):
                    # import module as alias, module2
                    import_part = stripped[7:].strip()
                    modules = [m.strip() for m in import_part.split(',')]
                    for module in modules:
                        if ' as ' in module:
                            module_name = module.split(' as ')[1].strip()
                        else:
                            module_name = module.split('.')[0]
                        import_info[module_name] = (i, line, 'import', module)

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
                            import_info[import_name] = (i, line, 'from', name)
            else:
                other_lines.append(line)

        # Trova nomi utilizzati nel codice
        used_names = set()
        code_content = '\n'.join(other_lines)

        for name in import_info.keys():
            # Pattern per trovare utilizzi reali
            patterns = [
                rf'\b{re.escape(name)}\.',      # nome.metodo
                rf'\b{re.escape(name)}\(',      # nome(args)
                rf'\b{re.escape(name)}\[',      # nome[index]
                rf'=\s*{re.escape(name)}\b',    # var = nome
                rf'\(\s*{re.escape(name)}\b',   # func(nome
                rf',\s*{re.escape(name)}\b',    # arg1, nome
                rf':\s*{re.escape(name)}\b',    # type: nome
                rf'isinstance\([^]+,\s*{re.escape(name)}\)',  # isinstance
                rf'raise\s+{re.escape(name)}\b',  # raise nome
                rf'except\s+{re.escape(name)}\b',  # except nome
            ]

            for pattern in patterns:
                if re.search(pattern, code_content, re.MULTILINE):
                    used_names.add(name)
                    break

        # Ricostruisci file senza importazioni inutilizzate
        result_lines = []
        processed_lines = set()

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith('import ') or stripped.startswith('from '):
                if i in processed_lines:
                    continue

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
                            indent = len(line) - len(line.lstrip())
                            new_line = ' ' * indent + 'import ' + ',
                                '.join(used_modules)
                            result_lines.append(new_line)
                            self.errors_fixed['F401'] += len(modules) - len(used_modules)
                    else:
                        self.errors_fixed['F401'] += len(modules)

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
                                indent = len(line) - len(line.lstrip())
                                new_line = f"{' ' * indent}{module_part} import {', '.join(used_imports)}"
                                result_lines.append(new_line)
                                self.errors_fixed['F401'] += len(names) - len(used_imports)
                        else:
                            self.errors_fixed['F401'] += len(names)
                    else:
                        result_lines.append(line)

                processed_lines.add(i)
            else:
                result_lines.append(line)

        return '\n'.join(result_lines)


    def fix_trailing_whitespace(self, content):
        """Rimuove spazi bianchi finali (W291)"""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            original_line = line
            fixed_line = line.rstrip()
            if fixed_line != original_line:
                self.errors_fixed['W291'] += 1
            fixed_lines.append(fixed_line)

        return '\n'.join(fixed_lines)


    def fix_blank_lines_with_whitespace(self, content):
        """Rimuove spazi da righe vuote (W293)"""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            if line.strip() == '' and line != '':
                fixed_lines.append('')
                self.errors_fixed['W293'] += 1
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)


    def fix_line_length(self, content):
        """Corregge righe troppo lunghe (E501)"""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            if len(line) <= 79:
                fixed_lines.append(line)
                continue

            # Se è una stringa lunga o commento docstring, mantieni
            if '"""' in line or "'''" in line:
                fixed_lines.append(line)
                continue

            # Commenti
            if line.strip().startswith('  #'):
                fixed_lines.extend(self._split_comment(line))
                self.errors_fixed['E501'] += 1
                continue

            # Funzioni con parametri lunghi
            if '(' in line and ')' in line and '=' in line:
                fixed_lines.extend(self._split_function_call(line))
                self.errors_fixed['E501'] += 1
                continue

            # Stringhe lunghe
            if ('"' in line and line.count('"') >= 2) or ("'" in line and line.count("'") >= 2):
                fixed_lines.extend(self._split_string(line))
                self.errors_fixed['E501'] += 1
                continue

            # Import lunghi
            if line.strip().startswith('from ') and ' import ' in line:
                fixed_lines.extend(self._split_import(line))
                self.errors_fixed['E501'] += 1
                continue

            # Operazioni lunghe
            operators = [
                ' and ',
                    ' or ',
                    ' + ',
                    ' - ',
                    ' * ',
                    ' / ',
                    '==',
                    '!=',
                    '<=',
                    '>='
            ]
            if any(op in line for op in operators):
                fixed_lines.extend(self._split_operation(line))
                self.errors_fixed['E501'] += 1
                continue

            # Fallback: spezza alla virgola più vicina
            if ',' in line:
                fixed_lines.extend(self._split_at_comma(line))
                self.errors_fixed['E501'] += 1
            else:
                # Non modificare se non si può spezzare intelligentemente
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)


    def _split_comment(self, line):
        """Spezza commenti lunghi"""
        indent = len(line) - len(line.lstrip())
        comment_text = line.strip()[1:].strip()

        words = comment_text.split()
        lines = []
        current_line = ' ' * indent + '  #'

        for word in words:
            if len(current_line + ' ' + word) <= 79:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = ' ' * indent + '  # ' + word

        if current_line.strip() != '  #':
            lines.append(current_line)

        return lines


    def _split_function_call(self, line):
        """Spezza chiamate di funzione lunghe"""
        indent = len(line) - len(line.lstrip())
        content_line = line.strip()

        # Trova la parte prima della parentesi
        paren_pos = content_line.find('(')
        if paren_pos == -1:
            return [line]

        func_part = content_line[:paren_pos + 1]
        rest = content_line[paren_pos + 1:]

        # Trova la parentesi di chiusura
        close_paren = rest.rfind(')')
        if close_paren == -1:
            return [line]

        params_part = rest[:close_paren]
        end_part = rest[close_paren:]

        if ',' in params_part:
            # Spezza i parametri
            params = [p.strip() for p in params_part.split(',')]
            lines = [' ' * indent + func_part]

            for i, param in enumerate(params):
                if param:
                    comma = ',' if i < len(params) - 1 else ''
                    param_line = ' ' * (indent + 4) + param + comma
                    lines.append(param_line)

            lines.append(' ' * indent + end_part)
            return lines

        return [line]


    def _split_string(self, line):
        """Spezza stringhe lunghe"""
        indent = len(line) - len(line.lstrip())

        # Cerca stringhe ""
        if '"' in line or "'" in line:
            # Per f-string, prova a spezzare al punto appropriato
            if len(line) > 79:
                mid_point = 75
                space_pos = line.rfind(' ', 0, mid_point)
                if space_pos > indent + 10:
                    return [
                        line[:space_pos] + ' \\',
                            ' ' * (indent + 4) + line[space_pos:].strip()
                    ]

        return [line]


    def _split_import(self, line):
        """Spezza import lunghi"""
        indent = len(line) - len(line.lstrip())

        # from module import a, b, c, d
        if ' import ' in line:
            parts = line.split(' import ')
            if len(parts) == 2:
                from_part = parts[0].strip()
                imports_part = parts[1].strip()

                if ',' in imports_part:
                    imports = [imp.strip() for imp in imports_part.split(',')]
                    lines = [' ' * indent + from_part + ' import (']

                    for i, imp in enumerate(imports):
                        comma = ',' if i < len(imports) - 1 else ''
                        lines.append(' ' * (indent + 4) + imp + comma)

                    lines.append(' ' * indent + ')')
                    return lines

        return [line]


    def _split_operation(self, line):
        """Spezza operazioni lunghe"""
        indent = len(line) - len(line.lstrip())
        content_line = line.strip()

        operators = [
            ' and ',
                ' or ',
                ' + ',
                ' - ',
                ' * ',
                ' / ',
                ' == ',
                ' != ',
                ' <= ',
                ' >= '
        ]

        for op in operators:
            if op in content_line:
                # Trova la posizione migliore per spezzare
                parts = content_line.split(op)
                if len(parts) > 1:
                    return [
                        ' ' * indent + parts[0].strip() + ' \\',
                            ' ' * (indent + 4) + op.strip() + ' ' + op.join(parts[1:]).strip()
                    ]

        return [line]


    def _split_at_comma(self, line):
        """Spezza alla virgola più appropriata"""
        indent = len(line) - len(line.lstrip())

        # Trova la virgola più vicina al limite di 79 caratteri
        comma_positions = [i for i, char in enumerate(line) if char == ',']

        best_pos = None
        for pos in comma_positions:
            if pos <= 75:  # Lascia spazio per continuazione
                best_pos = pos

        if best_pos:
            return [
                line[:best_pos + 1],
                    ' ' * (indent + 4) + line[best_pos + 1:].strip()
            ]

        return [line]


    def fix_blank_lines(self, content):
        """Corregge le righe vuote secondo PEP8 (E302, E305)"""
        lines = content.split('\n')
        fixed_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Aggiungi 2 righe vuote prima delle definizioni di classe
            if line.strip().startswith('class '):
                # Controlla se ci sono già righe vuote prima
                blank_count = 0
                j = len(fixed_lines) - 1
                while j >= 0 and fixed_lines[j].strip() == '':
                    blank_count += 1
                    j -= 1

                if j >= 0 and fixed_lines[j].strip() != '':  # Non all'inizio del file
                    needed_blanks = 2 - blank_count
                    for _ in range(needed_blanks):
                        fixed_lines.append('')
                        if needed_blanks > 0:
                            self.errors_fixed['E302'] += 1

            # Aggiungi 2 righe vuote prima delle funzioni top-level
            elif line.strip().startswith('def ') and not any(
                prev_line.strip().startswith(('class ', 'def '))
                for prev_line in lines[max(0, i-10):i]
                if prev_line.strip() and not prev_line.strip().startswith('  #')
            ):
                # Funzione top-level
                blank_count = 0
                j = len(fixed_lines) - 1
                while j >= 0 and fixed_lines[j].strip() == '':
                    blank_count += 1
                    j -= 1

                if j >= 0 and fixed_lines[j].strip() != '':
                    needed_blanks = 2 - blank_count
                    for _ in range(needed_blanks):
                        fixed_lines.append('')
                        if needed_blanks > 0:
                            self.errors_fixed['E302'] += 1

            # Aggiungi 1 riga vuota prima delle funzioni di metodo
            elif line.strip().startswith('def '):
                blank_count = 0
                j = len(fixed_lines) - 1
                while j >= 0 and fixed_lines[j].strip() == '':
                    blank_count += 1
                    j -= 1

                if j >= 0 and fixed_lines[j].strip() != '':
                    if blank_count == 0:
                        fixed_lines.append('')
                        self.errors_fixed['E302'] += 1

            fixed_lines.append(line)
            i += 1

        # Controlla righe vuote dopo classi e funzioni (E305)
        final_lines = []
        for i, line in enumerate(fixed_lines):
            final_lines.append(line)

            # Se questa riga termina una classe o funzione
            if (line.strip() and not line.startswith(' ') and
                i > 0 and fixed_lines[i-1].strip() and
                i < len(fixed_lines) - 1):

                next_line = fixed_lines[i + 1] if i + 1 < len(fixed_lines) else ""
                if (next_line.strip() and
                    not next_line.startswith(' ') and
                    not next_line.strip().startswith('  #')):
                    # Aggiungi riga vuota dopo definizione
                    final_lines.append('')
                    self.errors_fixed['E305'] += 1

        return '\n'.join(final_lines)


    def fix_indentation_errors(self, content):
        """Corregge errori di indentazione (E128, E122)"""
        lines = content.split('\n')
        fixed_lines = []

        for i, line in enumerate(lines):
            if not line.strip():
                fixed_lines.append(line)
                continue

            # Cerca linee di continuazione malformate
            if i > 0:
                prev_line = lines[i - 1].rstrip()
                current_line = line

                # Se la linea precedente termina con una virgola, parentesi,
                    # etc.
                if prev_line.endswith((',', '(', '[', '\\', '=')):
                    # Calcola indentazione appropriata
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    current_indent = len(current_line) - len(current_line.lstrip())

                    # Se indentazione non è corretta
                    if current_indent <= prev_indent:
                        # Correggi con 4 spazi aggiuntivi
                        new_indent = prev_indent + 4
                        fixed_line = ' ' * new_indent + current_line.lstrip()
                        fixed_lines.append(fixed_line)
                        self.errors_fixed['E128'] += 1
                        continue

            fixed_lines.append(line)

        return '\n'.join(fixed_lines)


    def fix_inline_comments(self, content):
        """Corregge spaziatura commenti inline (E261)"""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # Cerca commenti inline
            if '  #' in line and not line.strip().startswith('#'):
                comment_pos = line.find('  #')
                before_comment = line[:comment_pos]
                comment_part = line[comment_pos:]

                # Controlla se ci sono almeno 2 spazi prima del commento
                if comment_pos > 0 and not before_comment.endswith('  '):
                    # Rimuovi spazi esistenti e aggiungi 2 spazi
                    before_comment = before_comment.rstrip() + '  '
                    fixed_line = before_comment + comment_part
                    fixed_lines.append(fixed_line)
                    self.errors_fixed['E261'] += 1
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)


    def ensure_final_newline(self, content):
        """Assicura newline finale (W292)"""
        if content and not content.endswith('\n'):
            self.errors_fixed['W292'] += 1
            return content + '\n'
        return content

    def get_errors_before_fix(self, file_path):
        """Ottiene il numero di errori prima della correzione"""
        try:
            result = subprocess.run(
                ['py', '-m', 'flake8', file_path],
                    capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                return len(result.stdout.strip().split('\n'))
            return 0
        except:
            return 0


    def get_errors_after_fix(self, file_path):
        """Ottiene il numero di errori dopo la correzione"""
        return self.get_errors_before_fix(file_path)

    def print_summary(self):
        """Stampa riassunto delle correzioni"""
        total_fixes = sum(self.errors_fixed.values())

        print("\n📊 RIASSUNTO CORREZIONI:")
        print(f"{'='*50}")

        if total_fixes > 0:
            for error_type, count in self.errors_fixed.items():
                if count > 0:
                    descriptions = {
                        'F401': 'Importazioni non utilizzate rimosse',
                            'E501': 'Righe troppo lunghe corrette',
                                'E302': 'Righe vuote aggiunte prima funzioni',
                                'E305': 'Righe vuote aggiunte dopo classi/funzioni',
                                'W293': 'Spazi rimossi da righe vuote',
                                'W291': 'Spazi finali rimossi',
                                'W292': 'Newline finale aggiunta',
                                'E128': 'Indentazione continuazione corretta',
                                'E122': 'Indentazione continuazione aggiunta',
                                'E261': 'Spaziatura commenti inline corretta'
                            }
                    desc = descriptions.get(error_type, f"Errori {error_type}")
                    print(f"  {error_type}: {count:3d} - {desc}")

            print(f"{'='*50}")
            print(f"  TOTALE: {total_fixes:3d} errori corretti")
        else:
            print("  Nessuna correzione necessaria")


def main():
    """Funzione principale"""
    print("🚀 CORRETTORE COMPLETO ERRORI LINTING")
    print("=====================================")

    # Trova tutti i file Python
    python_files = []
    for file in os.listdir('.'):
        if file.endswith('.py'):
            python_files.append(file)

    if not python_files:
        print("❌ Nessun file Python trovato nella directory corrente")
        return

    print(f"📁 Trovati {len(python_files)} file Python:")
    for file in python_files:
        print(f"  - {file}")

    # Crea il correttore
    fixer = CompleteLintFixer()

    print("\n🔄 Inizio correzione automatica...")

    files_fixed = 0
    total_errors_before = 0
    total_errors_after = 0

    for file_path in python_files:
        # Conta errori prima
        errors_before = fixer.get_errors_before_fix(file_path)
        total_errors_before += errors_before

        if errors_before > 0:
            print(f"\n📝 {file_path}: {errors_before} errori trovati")

            # Applica correzioni
            if fixer.fix_file(file_path):
                files_fixed += 1

                # Conta errori dopo
                errors_after = fixer.get_errors_after_fix(file_path)
                total_errors_after += errors_after

                errors_fixed = errors_before - errors_after
                if errors_fixed > 0:
                    print(f"  ✅ {errors_fixed} errori corretti")
                if errors_after > 0:
                    print(f"  ⚠️  {errors_after} errori rimanenti")
            else:
                total_errors_after += errors_before
        else:
            print(f"\n✅ {file_path}: già conforme PEP8")

    # Stampa riassunto
    fixer.print_summary()

    print("\n🎯 RISULTATO FINALE:")
    print(f"{'='*50}")
    print(f"  File processati: {len(python_files)}")
    print(f"  File corretti: {files_fixed}")
    print(f"  Errori prima: {total_errors_before}")
    print(f"  Errori dopo: {total_errors_after}")
    print(f"  Errori risolti: {total_errors_before - total_errors_after}")

    if total_errors_after == 0:
        print("\n🎉 TUTTI I FILE SONO ORA CONFORMI A PEP8!")
    elif total_errors_after < total_errors_before:
        improvement = ((total_errors_before - total_errors_after) / total_errors_before) * 100
        print(f"\n📈 Miglioramento: {improvement:.1f}%")

    # Verifica finale
    print("\n🔍 Verifica finale con flake8...")
    try:
        result = subprocess.run(
            ['py', '-m', 'flake8', '.'],
                capture_output=True, text=True, timeout=60
        )

        if result.returncode == 0:
            print("🎉 SUCCESSO: Tutti i file passano la verifica flake8!")
        else:
            remaining_errors = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"⚠️  Rimangono {remaining_errors} errori da correggere \
                manualmente")
            if remaining_errors <= 10:
                print("Errori rimanenti:")
                print(result.stdout)

    except Exception as e:
        print(f"❌ Errore nella verifica finale: {e}")


if __name__ == "__main__":
    main()
