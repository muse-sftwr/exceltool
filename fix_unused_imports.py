#!/usr/bin/env python3
"""

Script per rimuovere automaticamente le importazioni non utilizzate

"""

import os
import re

import subprocess


def remove_unused_imports(content):
    """Rimuove le importazioni non utilizzate usando analisi del codice"""
    lines = content.split('\n')

    # Trova tutte le importazioni
    import_info = {}
    other_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
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

    # Trova i nomi utilizzati nel codice
    used_names = set()
    code_content = '\n'.join(other_lines)

    # Cerca i nomi utilizzati con regex più precisa
    for name in import_info.keys():
        # Pattern per trovare utilizzi reali del nome
        patterns = [
            fr'\b{re.escape(name)}\.',      # nome.metodo
            fr'\b{re.escape(name)}\(',      # nome(args)
            fr'\b{re.escape(name)}\[',      # nome[index]
            fr'=\s*{re.escape(name)}\b',    # var = nome
            fr'\(\s*{re.escape(name)}\b',   # func(nome
            fr',\s*{re.escape(name)}\b',    # arg1, nome
            fr':\s*{re.escape(name)}\b',    # type: nome
            fr'isinstance\([^)]+,\s*{re.escape(name)}\)',  # isinstance(x, nome)
            fr'raise\s+{re.escape(name)}\b',  # raise nome
            fr'except\s+{re.escape(name)}\b',  # except nome
        ]

        for pattern in patterns:
            if re.search(pattern, code_content, re.MULTILINE):
                used_names.add(name)
                break

    # Ricostruisci il file senza importazioni inutilizzate
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
                        # Ricostruisci import solo con moduli utilizzati
                        indent = len(line) - len(line.lstrip())
                        new_line = ' ' * indent + 'import ' + ', '.join(used_modules)
                        result_lines.append(new_line)
                # Se used_modules è vuoto, la riga viene omessa

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
                            indent = len(line) - len(line.lstrip())
                            new_line = f"{' ' * indent}{module_part} import {', '.join(used_imports)}"
                            result_lines.append(new_line)
                    # Se used_imports è vuoto, la riga viene omessa
                else:
                    result_lines.append(line)

            processed_lines.add(i)
        else:
            result_lines.append(line)

    return '\n'.join(result_lines)


def fix_file_unused_imports(file_path):
    """Corregge un singolo file rimuovendo importazioni non utilizzate"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Applica la correzione
        fixed_content = remove_unused_imports(content)

        # Salva solo se ci sono cambiamenti
        if fixed_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False

    except Exception as e:
        print(f"❌ Errore nel processare {file_path}: {e}")
        return False


def main():
    """Corregge le importazioni non utilizzate in tutti i file Python"""
    print("🔧 Rimozione importazioni non utilizzate...")

    # Lista dei file da correggere
    python_files = []
    for file in os.listdir('.'):
        if file.endswith('.py'):
            python_files.append(file)

    if not python_files:
        print("❌ Nessun file Python trovato nella directory corrente")
        return

    print("📁 Trovati {len(python_files)} file Python:")
    for file in python_files:
        print(f"  - {file}")

    print("\n🔄 Inizio correzione...")

    fixed_count = 0
    for file_path in python_files:
        print("\n📝 Processando {file_path}...")

        # Controlla errori F401 prima della correzione
        result = subprocess.run([
            'py',
                '-m',
                'flake8',
                '--select=F401',
                file_path
        ],
            capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✅ {file_path} - Nessuna importazione non utilizzata")
            continue

        errors_before = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print("  🔍 Trovate {errors_before} importazioni non utilizzate")

        # Applica correzione
        if fix_file_unused_imports(file_path):
            # Controlla errori dopo la correzione
            result_after = subprocess.run([
                'py',
                    '-m',
                    'flake8',
                    '--select=F401',
                    file_path
            ],
                capture_output=True, text=True)

            errors_after = len(result_after.stdout.strip().split('\n')) if result_after.stdout.strip() else 0

            if errors_after == 0:
                print(f"  ✅ {file_path} - Tutte le importazioni non \
                    utilizzate rimosse!")
                fixed_count += 1
            else:
                print("  ⚠️  {file_path} - Rimangono {errors_after} \
                    importazioni non utilizzate")
                # Mostra gli errori rimanenti
                if result_after.stdout.strip():
                    print("     Errori rimanenti:")
                    for error in result_after.stdout.strip().split('\n'):
                        print(f"     {error}")
        else:
            print("  ❌ Errore nella correzione di {file_path}")

    print("\n✅ Processo completato!")
    print(f"📊 File corretti: {fixed_count}/{len(python_files)}")

    # Verifica finale
    print("\n🔍 Verifica finale degli errori F401...")
    result = subprocess.run(['py', '-m', 'flake8', '--select=F401', '.'],
        capture_output=True, text=True)

    if result.returncode == 0:
        print("🎉 Tutte le importazioni non utilizzate sono state rimosse!")
    else:
        print("⚠️  Alcuni errori F401 potrebbero persistere:")
        print(result.stdout)


if __name__ == "__main__":
    main()
