# Strumento di Analisi Sessione Formula 1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Questo repository ospita un'applicazione desktop per l'analisi dei dati ufficiali delle gare di Formula 1. L'applicazione, sviluppata in Python con una GUI basata su Tkinter, permette agli utenti di visualizzare e confrontare le prestazioni dei piloti attraverso analisi dettagliate.

Attualmente in fase iniziale di sviluppo, questo strumento offre una base solida per analisi più complesse dei dati F1 e una futura integrazione con applicazioni di machine learning.  
Il progetto sfrutta la potenza della libreria [fastf1](https://github.com/theOehrly/Fast-F1) per l’accesso ai dati e utilizza le principali librerie di data science come Pandas, Matplotlib e Seaborn per l’analisi e la visualizzazione.

---

## ⭐️ Stato del Progetto & Roadmap

### Versione Attuale: v0.2 - Alpha dello Strumento di Analisi

Il progetto si trova attualmente alla **Versione 0.2**. In questa fase, l'architettura principale è completa e l'applicazione offre uno strumento solido per un tipo specifico di analisi visiva.

**Cosa include la v0.2:**
* Una **applicazione desktop** autonoma e funzionante con un'interfaccia pulita basata su Tkinter.
* **Motore dinamico di caricamento dati** che recupera i dati delle sessioni in base alla selezione dell’utente.
* Un singolo e potente **modulo di analisi**: Box Plot della Distribuzione dei Tempi sul Giro.
* Una **struttura del codice modulare e professionale**, che separa GUI, configurazioni e logica di analisi, rendendo il progetto facile da mantenere ed estendere.

### Obiettivi Futuri (Roadmap)

La visione di questo progetto va oltre le funzionalità attuali. Le prossime versioni si focalizzeranno su:
* **Nuovi Moduli di Analisi:** Integrazione di nuovi grafici, tra cui:
  * Visualizzazione delle strategie gomme (grafico a barre tipo Gantt).
  * Confronti di telemetria testa a testa.
  * Analisi del passo gara su diversi stint.
* **Esportazione Dati:** Aggiunta di funzionalità per salvare i grafici come immagini o esportare i dati elaborati in file CSV.
* **Base per Machine Learning:** Costruzione di script per il preprocessing dei dati al fine di ottenere dataset puliti, primo passo verso obiettivi ML (es. predizione del tempo sul giro).
* **Miglioramenti UI/UX:** Miglioramento dell’interfaccia utente con funzionalità come barre di progresso, temi, e aggiornamenti di stato più dettagliati.

---

## ✨ Funzionalità Principali (in v0.2)

* **Interfaccia Desktop:** Applicazione semplice da usare, costruita con Tkinter.
* **Selezione Dinamica della Sessione:** Scegli un anno e il menù a tendina si aggiorna automaticamente con il calendario corretto.
* **Analisi Distribuzione Tempi sul Giro:** Genera un box plot per ogni pilota per visualizzare la costanza e il passo gara.
* **Confronto per Mescola:** All’interno del grafico di ogni pilota, i tempi sono suddivisi per la mescola di pneumatici usata.
* **Filtro Intelligente degli Outlier:** I giri insolitamente lenti vengono filtrati per mescola per offrire una visione più realistica del passo reale.

---

## 🛠️ Stack Tecnologico

* **GUI:** [`Tkinter`](https://docs.python.org/3/library/tkinter.html) (Libreria standard di Python)  
* **Accesso Dati:** [`fastf1`](https://docs.fastf1.dev/)  
* **Manipolazione Dati:** [`Pandas`](https://pandas.pydata.org/), [`NumPy`](https://numpy.org/)  
* **Visualizzazione Dati:** [`Matplotlib`](https://matplotlib.org/), [`Seaborn`](https://seaborn.pydata.org/)

---

## 🚀 Come Iniziare

Segui questi passaggi per configurare e avviare l'applicazione localmente.

### Prerequisiti

* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

### Installazione

1. **Clona il repository:**
    ```sh
    git clone https://github.com/aciluca/f1-ml-project.git
    cd f1-ml-project
    ```

2. **Crea e attiva un ambiente virtuale:**
    ```sh
    # Crea l’ambiente virtuale
    python -m venv venv

    # Attivalo (Windows PowerShell)
    .\venv\Scripts\activate

    # Attivalo (macOS/Linux)
    # source venv/bin/activate
    ```

3. **Installa le dipendenze:**
    ```sh
    pip install -r requirements.txt
    ```

---

## 📂 Struttura del Progetto

Il progetto è organizzato come un pacchetto Python installabile per garantire modularità e pulizia del codice.

```
f1-ml-project/
│
├── f1_analyzer/ # The main application source package
│ ├── init.py
│ ├── main.py # The application's entry point
│ ├── app.py # GUI logic (the "parent")
│ ├── config.py # Shared constants and configurations
│ └── modules/ # Specialized analysis modules (the "children")
│ ├── init.py
│ └── box_plot.py
│
├── cache/ # Cached data from fastf1 (ignored by Git)
├── venv/ # Virtual environment (ignored by Git)
├── .gitignore
├── README.md # This file
└── requirements.txt # List of Python dependencies
```

---

## 📈 Utilizzo


---

## 📈 Utilizzo

Per avviare l'applicazione, assicurati che l’ambiente virtuale sia attivo, vai nella directory principale del progetto (`f1-ml-project`) e lancia il comando:

```sh
python -m f1_analyzer
Il flag -m dice a Python di eseguire il pacchetto f1_analyzer come applicazione, eseguendo automaticamente il file __main__.py.

Una volta avviata l’app:

    Seleziona anno, evento e sessione dai menu a tendina.

    Clicca il pulsante "Genera Box Plot".

    Attendi il caricamento dei dati e la generazione del grafico, che apparirà direttamente nella finestra principale.
```
---

## 📄 Licenza

Questo progetto è rilasciato sotto la Licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

---

## ✍️ Autore

*   **[Luca Acerbi]** - [aciluca](https://github.com/aciluca)

---
