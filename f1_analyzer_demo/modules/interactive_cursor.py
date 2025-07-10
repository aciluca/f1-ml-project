# File: f1_analyzer/modules/interactive_cursor.py (Versione Stabile per Tkinter)

import numpy as np

class InteractiveCursor:
    """
    Un cursore interattivo stabile e reattivo, ottimizzato per l'uso
    all'interno di un'applicazione Tkinter.
    """
    def __init__(self, fig, canvas, axes, telemetry_data, driver_codes, status_var):
        self.fig = fig
        self.canvas = canvas
        self.axes = axes
        self.telemetry_data = telemetry_data
        self.driver_codes = driver_codes
        self.status_var = status_var

        # Creiamo gli elementi una sola volta e li aggiorneremo
        self.lines = [ax.axvline(x=0, color='cyan', linestyle='--', linewidth=1, visible=False) for ax in self.axes]
        self.tooltip = self.fig.text(
            0.15, 0.92, "", ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.4', fc='#191925', ec='cyan', lw=1, alpha=0.9),
            color='white', fontsize=10, fontfamily='monospace', zorder=10, visible=False
        )
        
        self.cid_move = self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        # Evento per quando il mouse esce dal grafico
        self.cid_leave = self.canvas.mpl_connect('figure_leave_event', self.on_mouse_leave)

    def on_mouse_move(self, event):
        if not event.inaxes:
            return

        # Rendi visibili gli elementi se non lo sono già
        if not self.lines[0].get_visible():
            for line in self.lines:
                line.set_visible(True)
            self.tooltip.set_visible(True)
            
        self.update_artists(event)
        
        # Chiedi al canvas di ridisegnare quando ha un momento libero.
        # È il modo più stabile in Tkinter.
        self.canvas.draw_idle()

    def on_mouse_leave(self, event):
        """Nasconde il cursore quando il mouse esce dall'area della figura."""
        if self.lines[0].get_visible():
            for line in self.lines:
                line.set_visible(False)
            self.tooltip.set_visible(False)
            self.canvas.draw_idle()
            self.status_var.set("Pronto.") # Resetta la barra di stato

    def update_artists(self, event):
        """Calcola e aggiorna il contenuto degli elementi del cursore."""
        distance = event.xdata
        for line in self.lines:
            line.set_xdata([distance, distance])

        tel_d1 = self.telemetry_data['d1']
        tel_d2 = self.telemetry_data['d2']
        
        idx_d1 = np.searchsorted(tel_d1['Distance'], distance)
        idx_d2 = np.searchsorted(tel_d2['Distance'], distance)

        if idx_d1 >= len(tel_d1) or idx_d2 >= len(tel_d2):
            return

        data_d1 = tel_d1.iloc[idx_d1]
        data_d2 = tel_d2.iloc[idx_d2]
        
        d1_code = self.driver_codes['d1']
        d2_code = self.driver_codes['d2']
        delta = data_d2.get('DeltaTime', 0.0) # Usa .get() per sicurezza
        
        tooltip_text = (
            f"Dist: {int(distance):>5}m\n"
            f"----------------------\n"
            f"{'':<4} {'V':<4} {'RPM':<5} {'G':<2} {'Δ(s)':>6}\n"
            f"{d1_code:<4} {data_d1['Speed']:<4.0f} {data_d1['RPM']:<5.0f} {data_d1['nGear']:<2.0f} {'0.00':>6}\n"
            f"{d2_code:<4} {data_d2['Speed']:<4.0f} {data_d2['RPM']:<5.0f} {data_d2['nGear']:<2.0f} {delta: >+6.2f}"
        )
        self.tooltip.set_text(tooltip_text)
        
        status_bar_text = (
            f"Dist: {int(distance)}m | {d1_code}: V={data_d1['Speed']:.0f} | "
            f"{d2_code}: V={data_d2['Speed']:.0f} | Gap (vs {d1_code}): {delta:+.2f}s"
        )
        self.status_var.set(status_bar_text)

    def disconnect(self):
        """Disconnette tutti gli eventi per pulire la memoria."""
        if hasattr(self, 'cid_move'):
            self.canvas.mpl_disconnect(self.cid_move)
        if hasattr(self, 'cid_leave'):
            self.canvas.mpl_disconnect(self.cid_leave)