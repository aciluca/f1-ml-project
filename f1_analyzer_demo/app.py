import streamlit as st
import fastf1 as ff1
from datetime import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Importa le tue funzioni di analisi esistenti.
# Assicurati che il percorso sia corretto. Se hai una cartella 'src',
# potrebbe essere 'from src.f1_analyzer.modules...'.
# Con la tua struttura attuale, questo dovrebbe funzionare.
from modules.box_plot import create_plot as create_box_plot
from modules.telemetry_comparison import create_plot as create_telemetry_plot

# --- Funzioni di caching per ottimizzare le prestazioni ---
# Streamlit ha un sistema di cache potentissimo. Con @st.cache_data,
# i dati vengono scaricati una sola volta e riutilizzati,
# rendendo l'app super veloce dopo il primo caricamento.

@st.cache_data(show_spinner="Recupero calendario...")
def get_schedule(year):
    """Carica il calendario per un dato anno e lo mette in cache."""
    try:
        schedule = ff1.get_event_schedule(year, include_testing=True)
        return schedule
    except Exception as e:
        st.error(f"Impossibile caricare il calendario per il {year}: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner="Caricamento dati sessione... (potrebbe richiedere tempo)")
def load_session_data(year, event, session_name):
    """Carica i dati di una specifica sessione e li mette in cache."""
    # Assicura che la cartella cache esista
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    os.makedirs(cache_path, exist_ok=True)
    ff1.Cache.enable_cache(cache_path)
    
    try:
        session = ff1.get_session(year, event, session_name)
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        if session.laps is None or session.laps.empty:
            st.warning(f"Nessun dato trovato per {event} - {session_name}.")
            return None
        return session
    except Exception as e:
        st.error(f"Errore durante il caricamento della sessione: {e}")
        return None

# --- Configurazione della Pagina ---
st.set_page_config(layout="wide", page_title="F1 Analysis Hub")
st.title("🏎️ F1 Analysis Hub")
st.markdown("---")

# --- UI Sidebar per i controlli principali ---
st.sidebar.header("Parametri di Selezione")

year = st.sidebar.number_input(
    "Anno:", 
    min_value=1980, 
    max_value=datetime.now().year, 
    value=datetime.now().year
)

schedule = get_schedule(year)

if not schedule.empty:
    # Selezione Evento
    event_name = st.sidebar.selectbox("Evento:", schedule['EventName'].unique())
    
    # Selezione Sessione
    event_details = schedule[schedule['EventName'] == event_name].iloc[0]
    session_columns = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
    sessions = [event_details[col] for col in session_columns if pd.notna(event_details[col])]
    if 'pre-season' in event_name.lower():
        sessions = ['Day 1', 'Day 2', 'Day 3']
    
    session_name = st.sidebar.selectbox("Sessione:", sessions, index=len(sessions)-1 if sessions else 0)

    # Bottone per caricare i dati. Quando cliccato, il valore di ritorno è True
    if st.sidebar.button("Carica Dati Sessione"):
        session = load_session_data(year, event_name, session_name)
        # Usiamo st.session_state per conservare i dati tra i rerun dell'app
        st.session_state['session'] = session 
else:
    st.sidebar.warning("Nessun evento trovato per l'anno selezionato.")

# --- Area di Analisi Principale ---
# Mostra questa sezione solo se una sessione è stata caricata e salvata nello stato
if 'session' in st.session_state and st.session_state['session'] is not None:
    session = st.session_state['session']
    st.header(f"Analisi per: {session.event.year} {session.event.EventName} - {session.name}")

    analysis_options = {
        "Confronto Telemetria (Plotly)": create_telemetry_plot,
        "Distribuzione Tempi (Box Plot)": create_box_plot,
    }
    
    selected_analysis_name = st.selectbox("Scegli un tipo di analisi:", analysis_options.keys())
    plot_function = analysis_options[selected_analysis_name]

    st.markdown("---")

    # Controlli dinamici basati sull'analisi scelta
    if "Telemetria" in selected_analysis_name:
        drivers = sorted(session.laps['Driver'].unique())
        
        col1, col2 = st.columns(2)
        with col1:
            driver1 = st.selectbox("Pilota 1:", drivers, index=0)
        with col2:
            driver2 = st.selectbox("Pilota 2:", drivers, index=1 if len(drivers) > 1 else 0)

        if st.button("Genera Analisi Telemetria"):
            if driver1 == driver2:
                st.error("Per favore, seleziona due piloti diversi.")
            else:
                with st.spinner("Creazione grafico telemetria..."):
                    fig = plot_function(session, driver1, driver2)
                    if isinstance(fig, go.Figure):
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Impossibile generare il grafico. Dati insufficienti o formato non corretto.")
    
    elif "Box Plot" in selected_analysis_name:
        if st.button("Genera Analisi Box Plot"):
            with st.spinner("Creazione grafico box plot..."):
                fig = plot_function(session)
                if isinstance(fig, plt.Figure):
                    st.pyplot(fig)
                else:
                    st.error("Impossibile generare il grafico. Dati insufficienti o formato non corretto.")
else:
    st.info("⬅️ Seleziona i parametri nella barra laterale e clicca 'Carica Dati Sessione' per iniziare.")