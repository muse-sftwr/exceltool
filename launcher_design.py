#!/usr/bin/env python3
# flake8: noqa: E501,E302,E305,E128,E122,E131,F401,F841,F541,E231,E228,E303,E722
"""
🚀 EXCELTOOLS PRO LAUNCHER - DESIGN EDITION
==========================================

Launcher moderno e professionale per ExcelTools Pro
- Controlli sistema avanzati
- Interface elegante
- Feedback visivo premium
- Gestione dipendenze automatica

Designer: Digital Marketing & UX Engineer
Data: 2025-07-16
"""

import sys
import os
import subprocess
import importlib.util


class ModernLauncher:
    """Launcher moderno con design elegante"""

    def __init__(self):
        self.dependencies = {
            'pandas': 'pandas>=2.0.0',
            'openpyxl': 'openpyxl>=3.1.0',
            'tkinter': 'built-in'  # Built-in module
        }

    def print_banner(self):
        """Banner elegante di avvio"""
        banner = (
            "\n"
            "╔═══════════════════════════════════════════════════════════════════════════════╗\n"
            "║                                                                               ║\n"
            "║  🎨 EXCELTOOLS PRO • DESIGN EDITION                                           ║\n"
            "║                                                                               ║\n"
            "║  ✨ Sistema Avanzato di Gestione Excel                                        ║\n"
            "║  🎯 Design Minimale e Raffinato                                               ║\n"
            "║  💼 Professionale e Intuitivo                                                 ║\n"
            "║                                                                               ║\n"
            "║  Designer: Digital Marketing & UX Engineer                                    ║\n"
            "║  Versione: 3.0 Design Edition                                                 ║\n"
            "║                                                                               ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════╝\n"
        )
        print(banner)

    def check_python_version(self):
        """Verifica versione Python con styling moderno"""
        print("🐍 Controllo versione Python...")

        if sys.version_info < (3, 8):
            print("❌ ERRORE: Python 3.8+ richiesto!")
            print(f"   Versione corrente: {sys.version}")
            print("   Aggiorna Python per continuare.")
            return False

        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} OK")
        return True

    def check_tkinter(self):
        """Verifica disponibilità tkinter"""
        print("🖼️  Controllo interfaccia grafica...")

        try:
            import tkinter as tk
            # Test creazione finestra
            root = tk.Tk()
            root.withdraw()
            root.destroy()
            print("✅ Tkinter disponibile")
            return True
        except ImportError:
            print("❌ ERRORE: Tkinter non disponibile!")
            print("   Su Linux: sudo apt-get install python3-tk")
            print("   Su macOS: tkinter incluso")
            print("   Su Windows: tkinter incluso")
            return False
        except Exception as e:
            print(f"⚠️  Avviso tkinter: {e}")
            return True

    def check_dependency(self, module_name):
        """Controlla singola dipendenza"""
        if module_name == 'tkinter':
            return self.check_tkinter()

        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                return False

            # Prova import per test completo
            module = importlib.import_module(module_name)

            # Controlla versione se possibile
            if hasattr(module, '__version__'):
                version = module.__version__
                print(f"✅ {module_name} v{version} disponibile")
            else:
                print(f"✅ {module_name} disponibile")

            return True

        except ImportError:
            return False
        except Exception as e:
            print(f"⚠️  {module_name}: {e}")
            return True

    def install_dependency(self, package):
        """Installa dipendenza con feedback moderno"""
        print(f"📦 Installazione {package}...")

        try:
            # Usa subprocess per installazione pip
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=300  # 5 minuti timeout
            )

            if result.returncode == 0:
                print(f"✅ {package} installato con successo!")
                return True
            else:
                print(f"❌ Errore installazione {package}:")
                print(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout installazione {package}")
            return False
        except Exception as e:
            print(f"❌ Errore durante installazione {package}: {e}")
            return False

    def check_dependencies(self):
        """Controlla tutte le dipendenze con stile moderno"""
        print("\n📋 Controllo dipendenze...")
        print("=" * 50)

        missing_deps = []

        for module_name, package in self.dependencies.items():
            print(f"\n🔍 Controllo {module_name}...")

            if not self.check_dependency(module_name):
                print(f"❌ {module_name} non trovato")
                if package != 'built-in':
                    missing_deps.append((module_name, package))
                else:
                    print(f"   {module_name} dovrebbe essere built-in!")
                    return False

        if missing_deps:
            print(f"\n📦 Dipendenze mancanti: {len(missing_deps)}")

            # Chiedi conferma installazione
            print("\n🤔 Vuoi installare le dipendenze mancanti? (s/n): ", end="")
            try:
                response = input().lower().strip()

                if response in ['s', 'si', 'sì', 'y', 'yes']:
                    print("\n🚀 Avvio installazione automatica...")

                    failed_installs = []
                    for module_name, package in missing_deps:
                        if not self.install_dependency(package):
                            failed_installs.append(package)

                    if failed_installs:
                        print(f"\n❌ Installazione fallita per: {', '.join(failed_installs)}")
                        print("\n💡 Prova installazione manuale:")
                        for pkg in failed_installs:
                            print(f"   py -m pip install {pkg}")
                        return False
                    else:
                        print("\n✅ Tutte le dipendenze installate!")

                else:
                    print("\n⏹️  Installazione annullata")
                    print("\n💡 Installa manualmente:")
                    for _, package in missing_deps:
                        print(f"   py -m pip install {package}")
                    return False

            except KeyboardInterrupt:
                print("\n\n⏹️  Interruzione utente")
                return False

        print("\n✅ Tutte le dipendenze soddisfatte!")
        return True

    def check_system_compatibility(self):
        """Controlli sistema completi"""
        print("\n💻 Controllo compatibilità sistema...")
        print("=" * 50)

        print(f"🖥️  Sistema operativo: {os.name}")
        print(f"🗂️  Piattaforma: {sys.platform}")
        print(f"🏗️  Architettura: {sys.version}")

        # Controlla memoria disponibile (se possibile)
        try:
            import psutil
            memory = psutil.virtual_memory()
            print(f"💾 RAM: {memory.total // (1024**3)} GB totali, {memory.available // (1024**3)} GB disponibili")
        except ImportError:
            print("💾 RAM: Informazioni non disponibili (psutil non installato)")

        print("✅ Sistema compatibile")
        return True

    def find_main_application(self):
        """Trova file applicazione principale"""
        possible_files = [
            'excel_tools_design.py',
            'excel_tools_complete.py',
            'excel_tools_pro.py',
            'app.py'
        ]

        current_dir = os.path.dirname(os.path.abspath(__file__))

        for filename in possible_files:
            filepath = os.path.join(current_dir, filename)
            if os.path.exists(filepath):
                return filepath

        return None

    def launch_application(self):
        """Lancia applicazione principale"""
        print("\n🚀 Avvio ExcelTools Pro...")
        print("=" * 50)

        app_file = self.find_main_application()

        if not app_file:
            print("❌ File applicazione non trovato!")
            print("   Cerca: excel_tools_design.py, excel_tools_complete.py, app.py")
            return False

        print(f"📱 Caricamento: {os.path.basename(app_file)}")

        try:
            # Carica e esegui modulo
            spec = importlib.util.spec_from_file_location("main_app", app_file)
            app_module = importlib.util.module_from_spec(spec)

            # Aggiungi alla sys.modules per import interni
            sys.modules["main_app"] = app_module

            print("⚡ Inizializzazione moduli...")
            spec.loader.exec_module(app_module)

            # Cerca e esegui main function
            if hasattr(app_module, 'main'):
                print("🎯 Avvio interfaccia...")
                app_module.main()
            elif hasattr(app_module, 'ExcelToolsProDesign'):
                print("🎯 Avvio interfaccia design...")
                app = app_module.ExcelToolsProDesign()
                app.run()
            elif hasattr(app_module, 'ExcelToolsPro'):
                print("🎯 Avvio interfaccia...")
                app = app_module.ExcelToolsPro()
                app.run()
            else:
                print("❌ Entry point non trovato nel modulo")
                return False

            return True

        except Exception as e:
            print(f"❌ Errore durante l'avvio: {e}")
            import traceback
            print("\n📋 Dettagli errore:")
            traceback.print_exc()
            return False

    def run(self):
        """Esegue launcher completo"""
        self.print_banner()

        # Controlli preliminari
        if not self.check_python_version():
            self.wait_exit()
            return False

        if not self.check_system_compatibility():
            self.wait_exit()
            return False

        if not self.check_dependencies():
            self.wait_exit()
            return False

        # Avvio applicazione
        print("\n" + "="*80)
        print("🎉 SISTEMA PRONTO - Avvio ExcelTools Pro Design Edition")
        print("="*80)

        if self.launch_application():
            print("\n✅ Applicazione avviata con successo!")
        else:
            print("\n❌ Errore durante l'avvio dell'applicazione")
            self.wait_exit()
            return False

        return True

    def wait_exit(self):
        """Aspetta input utente prima di uscire"""
        print("\n⏸️  Premi INVIO per continuare...")
        try:
            input()
        except KeyboardInterrupt:
            pass


def main():
    """Entry point principale"""
    launcher = ModernLauncher()

    try:
        success = launcher.run()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Avvio interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Errore critico: {e}")
        import traceback
        traceback.print_exc()
        launcher.wait_exit()
        sys.exit(1)


if __name__ == "__main__":
    main()
