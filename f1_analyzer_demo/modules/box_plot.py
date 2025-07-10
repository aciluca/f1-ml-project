import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import mplcyberpunk

# Le costanti usate da questa specifica analisi
from ..config import COMPOUND_COLORS, CANONICAL_COMPOUND_ORDER

def create_plot(session):
    """
    Funzione specializzata: prende un oggetto sessione, analizza i dati
    e ritorna una figura Matplotlib con i box plot in stile "neon".
    """
    plt.style.use("cyberpunk")
    
    try:
        laps = session.laps
        if laps.empty:
            raise ValueError("Dati dei giri non disponibili per questa analisi.")

        # Preparazione dati
        laps_clean = laps.dropna(subset=['LapTime']).copy()
        laps_clean['LapTimeSeconds'] = laps_clean['LapTime'].dt.total_seconds()

        def filter_outliers(df):
            fastest_lap = df['LapTimeSeconds'].min()
            return df[df['LapTimeSeconds'] <= fastest_lap * 1.07]

        laps_filtered = laps_clean.groupby(['Driver', 'Compound']).apply(filter_outliers).reset_index(drop=True)

        if laps_filtered.empty:
            raise ValueError("Nessun giro consistente trovato dopo il filtraggio.")

        # Creazione della griglia di grafici
        drivers_to_plot = sorted(laps_filtered['Driver'].unique()) # Ordina i piloti alfabeticamente
        ncols = 4
        nrows = (len(drivers_to_plot) + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 4 * nrows), sharey=True)
        axes_flat = axes.flatten()

        for i, driver in enumerate(drivers_to_plot):
            ax = axes_flat[i]
            driver_laps = laps_filtered[laps_filtered['Driver'] == driver]
            compounds_used = driver_laps['Compound'].unique()
            dynamic_order = [c for c in CANONICAL_COMPOUND_ORDER if c in compounds_used]
            
            for compound in dynamic_order:
                compound_laps = driver_laps[driver_laps['Compound'] == compound]
                color = COMPOUND_COLORS.get(compound, 'white') # Prende il colore dal dizionario
                
                sns.boxplot(
                    data=compound_laps,
                    x='Compound',
                    y='LapTimeSeconds',
                    ax=ax,
                    # Proprietà per creare l'effetto "neon outline"
                    boxprops={'facecolor':'none', 'edgecolor':color, 'linewidth':1.5},
                    whiskerprops={'color':color, 'linewidth':1.5},
                    capprops={'color':color, 'linewidth':1.5},
                    medianprops={'color':'#FF55A3', 'linewidth':2}, # Mediana di un colore diverso per risaltare
                    # Non mostriamo gli outlier individuali, il box plot è sufficiente
                    showfliers=False 
                )
            
            ax.set_title(driver, fontsize=12, fontweight='bold')
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.tick_params(axis='x', labelsize=9)
            # Assicura che l'ordine sull'asse X sia corretto anche se disegniamo uno alla volta
            ax.set_xlim(-0.5, len(dynamic_order) - 0.5)
            ax.set_xticks(range(len(dynamic_order)))
            ax.set_xticklabels(dynamic_order)

        for i in range(len(drivers_to_plot), len(axes_flat)):
            axes_flat[i].set_visible(False)

        fig.suptitle(f"{session.event['EventName']} {session.event.year} - {session.name}\nDistribuzione Tempi sul Giro", fontsize=14, y=1.0)
        fig.text(0.01, 0.5, 'Tempo sul Giro (secondi)', va='center', rotation='vertical', fontsize=12)
        
        fig.subplots_adjust(hspace=0.6)
        fig.tight_layout(rect=[0.02, 0, 1, 0.96])
        
        return fig

    except Exception as e:
        print(f"Errore durante la creazione del box plot: {e}")
        # Ritorna una figura vuota con un messaggio per evitare crash
        plt.style.use("cyberpunk")
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.text(0.5, 0.5, f"Errore nella creazione del grafico:\n{e}", ha='center', va='center', fontsize=16, wrap=True)

        return fig