# Progetto di Machine Learning sulla Formula 1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Questo repository contiene un progetto di analisi dati e machine learning applicato ai dati ufficiali delle gare di Formula 1. L'obiettivo è utilizzare la telemetria, i tempi sul giro e i dati meteo per costruire modelli predittivi e scoprire pattern nascosti nelle performance di piloti e scuderie.

Il progetto sfrutta la potenza della libreria [fastf1](https://github.com/theOehrly/Fast-F1) per l'accesso ai dati e le librerie standard del mondo Data Science come Pandas, Scikit-learn e (opzionalmente) TensorFlow/PyTorch per la modellazione.

---

## 🎯 Obiettivi del Progetto

*   **Analisi Esplorativa (EDA):** Visualizzare e comprendere le dinamiche di una gara (degrado gomme, strategie, performance sul giro).
*   **Feature Engineering:** Creare variabili significative a partire dai dati grezzi di telemetria e tempi.
*   **Modellazione Predittiva:** Sviluppare modelli di machine learning per predire, ad esempio:
    *   Il tempo sul giro (Lap Time Prediction).
    *   Il degrado delle mescole.
    *   Lo stile di guida di un pilota.

---

## 🛠️ Tecnologie Utilizzate

*   **Accesso ai Dati:** [`fastf1`](https://docs.fastf1.dev/)
*   **Manipolazione Dati:** [`Pandas`](https://pandas.pydata.org/), [`NumPy`](https://numpy.org/)
*   **Visualizzazione:** [`Matplotlib`](https://matplotlib.org/), [`Seaborn`](https://seaborn.pydata.org/)
*   **Machine Learning:** [`Scikit-learn`](https://scikit-learn.org/)
*   **Notebook:** [`Jupyter Lab`](https://jupyter.org/)

---

## 🚀 Come Iniziare

Segui questi passaggi per configurare l'ambiente di sviluppo in locale.

### Prerequisiti

*   [Python 3.9+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/)

### Installazione

1.  **Clona il repository:**
    ```sh
    git clone https://github.com/aciluca/f1-ml-project.git
    cd f1-ml-project
    ```

2.  **Crea e attiva un ambiente virtuale:**
    ```sh
    # Crea il venv
    python -m venv venv

    # Attivalo (Windows PowerShell)
    .\venv\Scripts\activate

    # Attivalo (macOS/Linux)
    # source venv/bin/activate
    ```

3.  **Installa le dipendenze:**
    ```sh
    pip install -r requirements.txt
    ```

---

## 📂 Struttura del Progetto

Il progetto è organizzato per separare la logica, l'analisi e i dati.

```
├── data/               # Dataset grezzi e processati
│   ├── raw/
│   └── processed/
├── models/             # Modelli allenati e salvati
├── notebooks/          # Notebook Jupyter per analisi, prototipazione e visualizzazione
├── src/                # Script Python con la logica riutilizzabile
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train.py
│   └── ...
├── .gitignore          # File da ignorare per Git
├── README.md           # Questo file
└── requirements.txt    # Lista delle dipendenze Python
```

---

## 📈 Utilizzo

1.  **Esplorazione Dati:** Apri la cartella `notebooks/` per trovare esempi di come scaricare i dati con `fastf1` e visualizzarli. Parti da `01_data_exploration.ipynb`.
2.  **Training del Modello:** Esegui gli script nella cartella `src/` per processare i dati e lanciare un training completo.
    ```sh
    python src/train.py
    ```

---

## 📄 Licenza

Questo progetto è rilasciato sotto la Licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

---

## ✍️ Autore

*   **[Luca Acerbi]** - [aciluca](https://github.com/aciluca)

---