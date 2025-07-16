# ExcelTools Pro

## 📊 Strumento Professionale per Analisi Excel

ExcelTools Pro è un'applicazione Python completa per l'analisi, manipolazione e visualizzazione di file Excel con interfaccia grafica moderna e funzionalità avanzate.

### ✨ Caratteristiche Principali

- � **Analisi Dati**: Statistiche automatiche e insights sui dati Excel
- 📈 **Visualizzazioni**: Grafici interattivi e dashboard personalizzabili
- 🧹 **Pulizia Dati**: Rimozione duplicati, gestione valori mancanti
- 🔄 **Trasformazioni**: Filtri, ordinamenti e operazioni avanzate
- 💾 **Export Multi-formato**: Supporto Excel, CSV, JSON
- 🎨 **Interfaccia Moderna**: GUI intuitiva con tema scuro/chiaro
- ⚡ **Performance**: Ottimizzato per file di grandi dimensioni (50k+ righe)

### 🚀 Installazione Rapida

```bash
# Clone del repository
git clone https://github.com/muse-sftwr/exceltool.git
cd exceltool

# Installazione dipendenze
pip install -r requirements.txt

# Avvio applicazione
python app.py
```

### 📋 Requisiti

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0
- tkinter (incluso con Python)
- matplotlib >= 3.5.0
- openpyxl >= 3.0.0
- Tema scuro ottimizzato
- Layout responsive e intuitivo
- Progress bar e feedback in tempo reale

🔄 **Automazione**
- Monitoraggio automatico cartelle
- Rilevamento modifiche file in tempo reale
- Schedulazione elaborazioni
- Logging dettagliato

## Installazione

1. **Requisiti di Sistema**
   - Python 3.8+
   - Windows 10/11 (ottimizzato)
   - RAM consigliata: 4GB+

2. **Installazione Dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvio Applicazione**
   ```bash
   python app.py
   ```

## Utilizzo Rapido

### 1. Importazione File
- **Seleziona File Excel**: Carica uno o più file .xlsx/.xls
- **Monitora Cartella**: Attiva il monitoraggio automatico

### 2. Elaborazione Dati
- **Merge File**: Unisce automaticamente i file caricati
- **Salva in Database**: Memorizza per elaborazioni future

### 3. Esportazione
- **Esporta Excel**: Salva i risultati elaborati
- **Statistiche**: Visualizza analisi dettagliate

## Caratteristiche Tecniche

### Ottimizzazioni Performance
- **Lettura Chunk**: Per file >50MB utilizza lettura a blocchi
- **Dtype Optimization**: Riduce l'uso memoria fino al 70%
- **Database SQLite**: Velocità di accesso superiore
- **Threading**: Operazioni asincrone non bloccanti

### Gestione Memoria
- Auto-detection tipo dati ottimali
- Compressione automatica stringhe
- Garbage collection intelligente
- Monitoraggio uso memoria in tempo reale

### Database Integrato
- Schema ottimizzato per grandi dataset
- Indici automatici per performance
- Backup automatico
- Query ottimizzate

## Architettura Software

```
ExcelTools/
├── app.py              # Applicazione principale
├── requirements.txt    # Dipendenze Python
├── config.ini         # Configurazioni
├── excel_data.db      # Database SQLite (auto-generato)
└── logs/              # File di log (auto-generato)
```

### Componenti Principali

1. **ExcelProcessor**: Engine di elaborazione ottimizzato
2. **FileWatcher**: Monitoraggio automatico file system
3. **ExcelToolGUI**: Interfaccia grafica moderna
4. **Database Layer**: Gestione persistenza dati

## Funzionalità Avanzate

### Merge Intelligente
- Concatenazione automatica
- Rimozione duplicati
- Merge personalizzato per colonne comuni
- Validazione consistenza dati

### Monitoraggio Real-time
- Rilevamento modifiche istantaneo
- Auto-reload file modificati
- Notifiche stato operazioni
- Logging completo attività

### Esportazione Flessibile
- Multi-sheet Excel
- Ottimizzazione automatica grandi file
- Preservazione formattazione
- Export CSV/Database

## Configurazione Avanzata

Modifica `config.ini` per personalizzare:

```ini
[PERFORMANCE]
chunk_size = 10000          # Dimensione blocchi lettura
memory_limit_mb = 2048      # Limite memoria
max_threads = 4             # Thread paralleli

[UI]
preview_rows = 100          # Righe anteprima
max_columns_display = 10    # Colonne visualizzate
```

## Risoluzione Problemi

### File Molto Grandi (>100MB)
1. Aumenta `chunk_size` in config.ini
2. Incrementa `memory_limit_mb`
3. Usa SSD per migliori performance

### Errori Memory
1. Chiudi altre applicazioni
2. Riduci `preview_rows`
3. Usa elaborazione batch

### Performance Lente
1. Abilita `parallel_processing`
2. Aumenta `max_threads`
3. Verifica spazio disco disponibile

## Best Practices

1. **File Grandi**: Usa sempre la lettura ottimizzata
2. **Memoria**: Monitora l'uso RAM con grandi dataset
3. **Backup**: Salva regolarmente in database
4. **Pulizia**: Rimuovi file temporanei periodicamente

## Supporto

Per problemi o suggerimenti:
- Controlla i log in `logs/excel_tool_YYYYMMDD.log`
- Verifica la tab "Log Operazioni" nell'app
- Consulta le statistiche per info performance

## Licenza

Strumento sviluppato per uso interno aziendale.
Ottimizzato per l'elaborazione di grandi volumi di dati Excel.
