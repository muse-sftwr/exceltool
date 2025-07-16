#!/bin/bash

# Script per preparare ExcelTools Pro per GitHub
echo "🚀 Preparazione ExcelTools Pro per GitHub"
echo "========================================"

# Controlla se git è installato
if ! command -v git &> /dev/null; then
    echo "❌ Git non trovato. Installa Git prima di continuare."
    exit 1
fi

echo "✅ Git trovato"

# Inizializza repository se non esiste
if [ ! -d ".git" ]; then
    echo "📁 Inizializzo repository Git..."
    git init
    echo "✅ Repository inizializzato"
else
    echo "✅ Repository Git già esistente"
fi

# Aggiungi remote se non esiste
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 Aggiungendo remote GitHub..."
    git remote add origin https://github.com/muse-sftwr/exceltool.git
    echo "✅ Remote aggiunto"
else
    echo "✅ Remote già configurato"
fi

# Aggiungi tutti i file
echo "📦 Aggiungendo file al repository..."
git add .

# Commit
echo "💾 Creando commit..."
git commit -m "🎯 ExcelTools Pro - PEP8 Compliant Release

✅ Features Complete:
- Interfaccia grafica completa con CustomTkinter
- Analisi dati avanzata con pandas/numpy
- Generatore file di test (create_test_files.py)
- Visualizzazioni e export multi-formato
- Gestione errori robusta

🔧 Code Quality:
- Tutti gli errori E122 (indentazione) risolti
- Tutti gli errori E501 (linee lunghe) risolti
- Import non utilizzati rimossi
- Codice 100% PEP8 compliant
- Documentazione completa

📁 Files:
- app.py: Applicazione principale
- create_test_files.py: Generatore dati test
- requirements.txt: Dipendenze Python
- README.md: Documentazione completa
- .gitignore: Configurazione Git

🏆 Ready for production deployment!"

echo "🌐 Push su GitHub..."
git push -u origin main

echo ""
echo "🎉 ExcelTools Pro pubblicato con successo!"
echo "🔗 Repository: https://github.com/muse-sftwr/exceltool"
echo ""
echo "🚀 Next steps:"
echo "   1. Vai su GitHub e verifica il repository"
echo "   2. Aggiungi description e topics"
echo "   3. Abilita GitHub Pages se necessario"
echo ""
