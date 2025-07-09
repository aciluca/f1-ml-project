# File: analyses/box_plot.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Le costanti usate da questa specifica analisi
from ..config import COMPOUND_COLORS, CANONICAL_COMPOUND_ORDER

def create_plot(session):
    """
    Funzione specializzata: prende un oggetto sessione, analizza i dati
    e ritorna una figura Matplotlib con i box plot.
    """
    laps = session.laps
    if laps.empty:
        print("Dati dei giri non disponibili per questa analisi.")
        return None

    # Preparazione dati
    laps_clean = laps.dropna(subset=['LapTime']).copy()
    laps_clean['LapTimeSeconds'] = laps_clean['LapTime'].dt.total_seconds()

    def filter_outliers(df):
        fastest_lap = df['LapTimeSeconds'].min()
        return df[df['LapTimeSeconds'] <= fastest_lap * 1.07]

    laps_filtered = laps_clean.groupby(['Driver', 'Compound']).apply(filter_outliers).reset_index(drop=True)

    if laps_filtered.empty:
        print("Nessun giro consistente trovato dopo il filtraggio.")
        return None

    # Creazione della griglia di grafici
    drivers_to_plot = laps_filtered['Driver'].unique()
    ncols = 4
    nrows = (len(drivers_to_plot) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 4 * nrows), sharey=True)
    axes_flat = axes.flatten()

    for i, driver in enumerate(drivers_to_plot):
        ax = axes_flat[i]
        driver_laps = laps_filtered[laps_filtered['Driver'] == driver]
        compounds_used = driver_laps['Compound'].unique()
        dynamic_order = [c for c in CANONICAL_COMPOUND_ORDER if c in compounds_used]
        
        # --- MODIFICA CHIAVE QUI ---
        sns.boxplot(
            data=driver_laps,
            x='Compound',
            y='LapTimeSeconds',
            ax=ax,
            palette=COMPOUND_COLORS,
            order=dynamic_order,
            width=0.6  # <-- Imposta la larghezza dei box plot. Il default è 0.8.
                       #     Un valore più piccolo li stringe.
        )
        
        ax.set_title(driver, fontsize=12, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')
        # Non modifichiamo più le etichette qui, le lasciamo orizzontali
        ax.tick_params(axis='x', labelsize=9)

    for i in range(len(drivers_to_plot), len(axes_flat)):
        axes_flat[i].set_visible(False)

    fig.suptitle(f"{session.event['EventName']} {session.event.year} - {session.name}\nDistribuzione Tempi sul Giro", fontsize=14, y=1.0)
    fig.text(0.01, 0.5, 'Tempo sul Giro (secondi)', va='center', rotation='vertical', fontsize=12)
    
    # Manteniamo comunque uno spazio verticale generoso tra i grafici
    fig.subplots_adjust(hspace=0.6)
    
    fig.tight_layout(rect=[0.02, 0, 1, 0.96])
    
    return fig