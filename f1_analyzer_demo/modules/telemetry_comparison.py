# File: f1_analyzer/modules/telemetry_comparison.py (Versione Plotly per App Desktop)

import fastf1.plotting
import fastf1.utils
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_plot(session, driver1_code, driver2_code):
    """
    Crea un grafico di telemetria con Plotly, ottimizzato per l'integrazione
    in un'app desktop e con tooltip personalizzati.
    """
    try:
        fastf1.plotting.setup_mpl()
        laps_d1 = session.laps.pick_driver(driver1_code)
        laps_d2 = session.laps.pick_driver(driver2_code)
        
        fastest_d1 = laps_d1.pick_fastest()
        fastest_d2 = laps_d2.pick_fastest()

        if fastest_d1 is None or pd.isna(fastest_d1.LapTime):
            raise ValueError(f"{driver1_code} non ha un giro veloce valido.")
        if fastest_d2 is None or pd.isna(fastest_d2.LapTime):
            raise ValueError(f"{driver2_code} non ha un giro veloce valido.")

        telemetry_d1 = fastest_d1.get_car_data().add_distance()
        telemetry_d2 = fastest_d2.get_car_data().add_distance()
        
        delta_time, ref_tel, _ = fastf1.utils.delta_time(fastest_d1, fastest_d2)
        
        team_d1_color = fastf1.plotting.get_team_color(fastest_d1['Team'], session) or '#FFFFFF'
        team_d2_color = fastf1.plotting.get_team_color(fastest_d2['Team'], session) or '#C0C0C0'

        # --- PREPARAZIONE DATI PER TOOLTIP PERSONALIZZATO ---
        # Uniamo tutti i dati in un unico DataFrame per facilitare la creazione dei tooltip
        telemetry_d1['Driver'] = driver1_code
        telemetry_d2['Driver'] = driver2_code
        
        # Aggiungiamo il delta time interpolato
        telemetry_d2['Delta'] = pd.to_numeric(delta_time, errors='coerce')
        telemetry_d1['Delta'] = 0.0 # Il pilota di riferimento ha sempre delta 0
        
        # Uniamo i due dataframe
        full_telemetry = pd.concat([telemetry_d1, telemetry_d2])

        plot_ratios = [0.1, 0.3, 0.2, 0.1, 0.1, 0.2, 0.1]
        subplot_titles = ("Gap (s)", "Velocità", "Acceleratore", "Freno", "Marcia", "RPM", "DRS")
        
        fig = make_subplots(rows=7, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03, row_heights=plot_ratios,
                            subplot_titles=subplot_titles)

        # --- Aggiungiamo le tracce usando i dati preparati ---
        
        # Grafico del Delta
        fig.add_trace(go.Scatter(x=ref_tel['Distance'], y=delta_time, mode='lines', 
                                 line=dict(color='yellow'), name='Gap'), row=1, col=1)

        # Tracce per Pilota 1
        d1_data = full_telemetry[full_telemetry['Driver'] == driver1_code]
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['Speed'], name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1'), row=2, col=1)
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['Throttle'], name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1', showlegend=False), row=3, col=1)
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['Brake'], name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1', showlegend=False), row=4, col=1)
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['nGear'], name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1', showlegend=False), row=5, col=1)
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['RPM'], name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1', showlegend=False), row=6, col=1)
        fig.add_trace(go.Scatter(x=d1_data['Distance'], y=d1_data['DRS'].apply(lambda x: 1 if x >= 10 else 0), name=driver1_code, line=dict(color=team_d1_color), legendgroup='d1', showlegend=False), row=7, col=1)

        # Tracce per Pilota 2
        d2_data = full_telemetry[full_telemetry['Driver'] == driver2_code]
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['Speed'], name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2'), row=2, col=1)
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['Throttle'], name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2', showlegend=False), row=3, col=1)
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['Brake'], name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2', showlegend=False), row=4, col=1)
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['nGear'], name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2', showlegend=False), row=5, col=1)
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['RPM'], name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2', showlegend=False), row=6, col=1)
        fig.add_trace(go.Scatter(x=d2_data['Distance'], y=d2_data['DRS'].apply(lambda x: 1 if x >= 10 else 0), name=driver2_code, line=dict(color=team_d2_color), legendgroup='d2', showlegend=False), row=7, col=1)
        
        # --- Layout e Stile Finale ---
        fig.update_layout(
            template="plotly_dark",
            title=f"<b>{session.event.year} {session.event.EventName} - {session.name} | {driver1_code} vs {driver2_code}</b>",
            height=None, # Lascia che si adatti al contenitore
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # --- TOOLTIP PERSONALIZZATO ---
        fig.update_traces(
            hovertemplate="<b>Dist</b>: %{x:.0f}m<br><b>Valore</b>: %{y:.2f}"
        )

        fig.add_hline(y=0, line_dash="dash", line_color="white", row=1, col=1)
        fig.update_yaxes(tickvals=[0, 1], ticktext=['OFF', 'ON'], row=7, col=1)
        
        return fig
        
    except Exception as e:
        print(f"Errore durante la creazione del grafico Plotly: {e}")
        return None