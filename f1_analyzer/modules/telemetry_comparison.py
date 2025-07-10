import matplotlib.pyplot as plt
import fastf1.plotting
import fastf1.utils
import pandas as pd
import mplcyberpunk

def create_plot(session, driver1_code, driver2_code):
    """
    Funzione che crea il confronto telemetrico usando i dati di telemetria
    restituiti direttamente da `delta_time` per garantire un allineamento perfetto.
    """
    plt.style.use("cyberpunk")
    
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
        
        # `delta_time` calcola il gap, `ref_tel` è la telemetria allineata del pilota 1,
        # `com_tel` è la telemetria allineata del pilota 2.
        # Questi dataframe contengono già tutti i canali (Speed, RPM, etc.)
        delta_time, ref_tel, com_tel = fastf1.utils.delta_time(fastest_d1, fastest_d2)
        
        # Aggiungiamo il delta time calcolato al dataframe del pilota di confronto
        # per averlo a disposizione nel tooltip interattivo.
        com_tel['DeltaTime'] = delta_time

        team_d1_color = fastf1.plotting.get_team_color(fastest_d1['Team'], session)
        team_d2_color = fastf1.plotting.get_team_color(fastest_d2['Team'], session)

        linestyle_d2 = '--' if fastest_d1['Team'] == fastest_d2['Team'] else 'solid'
        
        plot_ratios = [1, 3, 2, 1, 1, 2, 1]
        fig, axes = plt.subplots(7, 1, figsize=(16, 18), 
                                 gridspec_kw={'height_ratios': plot_ratios}, 
                                 sharex=True)

        plot_title = (f"{session.event.year} {session.event.EventName} - {session.name}\n"
                      f"{driver1_code} ({str(fastest_d1.LapTime).split(' ')[-1][:-3]}) vs "
                      f"{driver2_code} ({str(fastest_d2.LapTime).split(' ')[-1][:-3]})")
        axes[0].set_title(plot_title, fontsize=16)

        # 1. Delta Time
        axes[0].plot(ref_tel['Distance'], delta_time, color='yellow')
        axes[0].axhline(0, color='white', linestyle='--', linewidth=0.8)
        axes[0].set_ylabel(f"Gap (s)")

        # --- USA I DATAFRAME CORRETTI PER IL PLOTTING ---
        # 2. Velocità
        axes[1].plot(ref_tel['Distance'], ref_tel['Speed'], label=driver1_code, color=team_d1_color)
        axes[1].plot(com_tel['Distance'], com_tel['Speed'], label=driver2_code, color=team_d2_color, linestyle=linestyle_d2)
        axes[1].set_ylabel('Velocità')
        axes[1].legend(loc="lower right", frameon=True, facecolor='black', framealpha=0.7)

        # 3. Acceleratore
        axes[2].plot(ref_tel['Distance'], ref_tel['Throttle'], color=team_d1_color)
        axes[2].plot(com_tel['Distance'], com_tel['Throttle'], color=team_d2_color, linestyle=linestyle_d2)
        axes[2].set_ylabel('Acceleratore')

        # 4. Freno
        axes[3].plot(ref_tel['Distance'], ref_tel['Brake'], color=team_d1_color)
        axes[3].plot(com_tel['Distance'], com_tel['Brake'], color=team_d2_color, linestyle=linestyle_d2)
        axes[3].set_ylabel('Freno')
        
        # 5. Marcia
        axes[4].plot(ref_tel['Distance'], ref_tel['nGear'], color=team_d1_color)
        axes[4].plot(com_tel['Distance'], com_tel['nGear'], color=team_d2_color, linestyle=linestyle_d2)
        axes[4].set_ylabel('Marcia')
        
        # 6. RPM
        axes[5].plot(ref_tel['Distance'], ref_tel['RPM'], color=team_d1_color)
        axes[5].plot(com_tel['Distance'], com_tel['RPM'], color=team_d2_color, linestyle=linestyle_d2)
        axes[5].set_ylabel('RPM')

        # 7. DRS
        axes[6].plot(ref_tel['Distance'], ref_tel['DRS'].apply(lambda x: 1 if x >= 10 else 0), color=team_d1_color)
        axes[6].plot(com_tel['Distance'], com_tel['DRS'].apply(lambda x: 1 if x >= 10 else 0), color=team_d2_color, linestyle=linestyle_d2)
        axes[6].set_ylabel('DRS')
        axes[6].set_yticks([0, 1]); axes[6].set_yticklabels(['OFF', 'ON'])

        axes[6].set_xlabel('Distanza (m)')
        plt.tight_layout()
        
        # Restituisci i dataframe corretti e allineati per l'interattività
        return fig, ref_tel, com_tel
        
    except Exception as e:
        print(f"Errore durante la creazione del grafico di telemetria: {e}")
        plt.style.use("cyberpunk")
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.text(0.5, 0.5, f"Impossibile generare il grafico:\n{e}", 
                ha='center', va='center', fontsize=16, wrap=True)
        return fig, None, None