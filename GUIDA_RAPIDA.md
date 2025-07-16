# Guida Rapida - ExcelTools Pro

## 🚀 Avvio Rapido

### 1. Installazione
```bash
# Naviga nella cartella del progetto
cd "d:\Users\C3602943\OneDrive - ARÇELİK A.Ş\Documents\Myproject\ExcelTools"

# Installa le dipendenze
pip install pandas openpyxl customtkinter watchdog

# Avvia l'applicazione
python app.py
```

### 2. Versione di Test Semplificata
Se hai problemi con l'applicazione principale, usa la versione semplificata:
```bash
python simple_app.py
```

## 📊 Funzionalità Principali

### Caricamento File
- **File Singoli**: Clicca "Carica File Excel" e seleziona il file
- **File Multipli**: Seleziona più file contemporaneamente (Ctrl+Click)
- **Monitoraggio**: Attiva il monitoraggio di una cartella per rilevamento automatico

### Elaborazione Dati
- **Merge**: Unisce automaticamente file multipli
- **Statistiche**: Visualizza info dettagliate sui dataset
- **Anteprima**: Mostra le prime righe dei dati caricati

### Esportazione
- **Excel**: Salva i dati elaborati in nuovo file Excel
- **Database**: Memorizza in SQLite per elaborazioni future
- **Statistiche**: Genera report dettagliati

## ⚡ Ottimizzazioni Performance

### File Grandi (>50MB)
- L'applicazione usa lettura a chunk automatica
- Ottimizzazione tipi di dati per ridurre memoria
- Processing asincrono per UI reattiva

### Memoria
- Monitoraggio automatico uso RAM
- Garbage collection intelligente
- Compressione dati automatica

## 🔧 Configurazione

Modifica `config.ini` per personalizzare:

```ini
[PERFORMANCE]
chunk_size = 10000          # Dimensione blocchi lettura
memory_limit_mb = 2048      # Limite memoria (MB)
max_threads = 4             # Thread paralleli

[UI]
preview_rows = 100          # Righe mostrate in anteprima
max_columns_display = 10    # Colonne visualizzate
```

## 📁 File di Test Inclusi

1. **test_vendite.xlsx** - Dati vendite esempio
2. **test_10k.xlsx** - Dataset grande (10k righe)
3. **test_financial.xlsx** - Dati finanziari

## 🛠️ Risoluzione Problemi

### Errore "Module not found"
```bash
pip install --upgrade pandas openpyxl customtkinter
```

### Performance Lente
1. Chiudi altre applicazioni pesanti
2. Aumenta `memory_limit_mb` in config.ini
3. Usa SSD se disponibile

### File Troppo Grande
1. Aumenta `chunk_size` in configurazione
2. Elabora file in batch più piccoli
3. Usa lettura ottimizzata automatica

### Interfaccia Non Risponde
- L'app usa processing asincrono
- Attendi completamento operazioni lunghe
- Controlla progress bar per stato

## 📈 Best Practices

### Performance
- ✅ Usa l'applicazione per file >1MB
- ✅ Salva in database per riutilizzo
- ✅ Chiudi file Excel aperti in altre app
- ❌ Non aprire file >100MB in Excel contemporaneamente

### Workflow Consigliato
1. **Import** → Carica file Excel
2. **Analyze** → Visualizza statistiche
3. **Process** → Merge/elabora se necessario
4. **Export** → Salva risultati

### Sicurezza Dati
- Il database SQLite è locale
- Backup automatico ogni ora
- Log dettagliato di tutte le operazioni

## 🆘 Supporto

### Log Operazioni
- File log automatici in cartella del progetto
- Tab "Log Operazioni" nell'interfaccia
- Livello dettaglio configurabile

### Debug
1. Controlla log file `excel_tool_YYYYMMDD.log`
2. Verifica tab "Statistiche" per info performance
3. Usa versione semplificata per test base

### Contatti
Per problemi specifici:
- Controlla README.md per documentazione completa
- Verifica configurazione in config.ini
- Usa versione simple_app.py per diagnostica

---

## 🎯 Esempi di Utilizzo

### Caso 1: Merge File Vendite
1. Carica file vendite mensili
2. Clicca "Merge File"
3. Visualizza statistiche unificate
4. Esporta file consolidato

### Caso 2: Analisi Grandi Dataset
1. Carica file >50k righe
2. L'app attiva automaticamente ottimizzazioni
3. Visualizza statistiche per insight
4. Salva in database per accesso veloce

### Caso 3: Monitoraggio Automatico
1. Seleziona cartella da monitorare
2. L'app rileva nuovi file automaticamente
3. Processing automatico dei cambiamenti
4. Notifiche in tempo reale

---
**ExcelTools Pro** - Gestione professionale di file Excel di grandi dimensioni
