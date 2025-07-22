#!/usr/bin/env python3
# cSpell:disable

"""

Script per correggere tutti i file Python del progetto

"""

import glob
import subprocess


def fix_all_python_files():
    """Corregge tutti i file Python nel progetto"""
    print("🔧 Correzione automatica di tutti i file Python...")

    # Trova tutti i file Python
    python_files = glob.glob("*.py")
    python_files = [f for f in python_files if not f.startswith('fix_')]

    print(f"📁 Trovati {len(python_files)} file Python da correggere")

    for file_path in python_files:
        print(f"🔧 Correzione: {file_path}")

        try:
            # Leggi il file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Aggiungi commento per disabilitare spell checker
            if not content.startswith('  #!/usr/bin/env python3\n# cSpell:disable'):
                if content.startswith('  #!/usr/bin/env python3'):
                    content = content.replace(
                        '  #!/usr/bin/env python3',
                            '  #!/usr/bin/env python3\n# cSpell:disable',
                                1
                    )
                elif content.startswith('  #'):
                    lines = content.split('\n')
                    lines.insert(1, '  # cSpell:disable')
                    content = '\n'.join(lines)
                else:
                    content = '  # cSpell:disable\n' + content

            # Salva il file modificato
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Usa autopep8 per la correzione automatica
            try:
                subprocess.run([
                    'py',
                        '-m',
            'autopep8',
            '--in-place',
            '--max-line-length=79',
            '--aggressive',
            '--aggressive',
            file_path
], check=True, capture_output=True)
                print(f"  ✅ {file_path} corretto")
            except subprocess.CalledProcessError:
                print(f"  ⚠️  {file_path} - autopep8 non disponibile")
                # Fallback: correzioni manuali basic
                fix_basic_issues(file_path)

        except Exception as e:
            print(f"  ❌ Errore con {file_path}: {e}")


def fix_basic_issues(file_path):
    """Correzioni basic senza autopep8"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Rimuovi spazi bianchi finali
        lines = content.split('\n')
        lines = [line.rstrip() for line in lines]

        # Rimuovi righe vuote multiple
        cleaned_lines = []
        prev_empty = False

        for line in lines:
            if line.strip() == '':
                if not prev_empty:
                    cleaned_lines.append(line)
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False

        # Salva il file pulito
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))

    except Exception as e:
        print(f"    ❌ Errore correzione basic: {e}")


def install_autopep8():
    """Installa autopep8 se non presente"""
    try:
        print("📦 Installazione autopep8...")
        subprocess.run([
            'py',
                '-m',
            'pip',
            'install',
            'autopep8'
], check=True, capture_output=True)
        print("✅ autopep8 installato")
        return True
    except subprocess.CalledProcessError:
        print("❌ Impossibile installare autopep8")
        return False


def main():
    """Funzione principale"""
    print("=" * 50)
    print("    CORREZIONE AUTOMATICA PROGETTO")
    print("=" * 50)

    # Verifica e installa autopep8
    try:
        subprocess.run([
            'py', '-c', 'import autopep8'
        ], check=True, capture_output=True)
        print("✅ autopep8 disponibile")
    except subprocess.CalledProcessError:
        if not install_autopep8():
            print("⚠️  Procedo senza autopep8")

    # Correggi tutti i file
    fix_all_python_files()

    # Verifica finale
    print("\n🔍 Verifica finale...")
    try:
        result = subprocess.run([
            'py', '-m', 'flake8', '.', '--count'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Tutti i file sono conformi a PEP8!")
        else:
            error_count = result.stdout.strip().split('\n')[-1]
            print(f"⚠️  Rimangono {error_count} errori")

    except subprocess.CalledProcessError:
        print("❌ Impossibile verificare con flake8")

    print("\n✅ Correzione completata!")


if __name__ == "__main__":
    main()
