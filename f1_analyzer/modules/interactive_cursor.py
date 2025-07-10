import numpy as np
import matplotlib.pyplot as plt

class InteractiveCursor:
    def __init__(self, fig, canvas, axes, telemetry_data, driver_codes, status_var):
        # Il costruttore __init__ rimane identico
        self.fig = fig
        self.canvas = canvas
        self.axes = axes
        self.telemetry_data = telemetry_data
        self.driver_codes = driver_codes
        self.status_var = status_var
        self.lines = []
        self.tooltip = self.fig.text(
            0.15, 0.85, "",
            ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.4', fc='#191925', ec='cyan', lw=1, alpha=0.9),
            color='white', fontsize=10, fontfamily='monospace', visible=False
        )
        for ax in self.axes:
            line = ax.axvline(x=0, color='cyan', linestyle='--', linewidth=1, visible=False)
            self.lines.append(line)
        self.cid = self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def on_mouse_move(self, event):
        try:
            # La prima parte di on_mouse_move rimane identica
            is_visible = self.tooltip.get_visible()
            if not event.inaxes:
                if is_visible:
                    for line in self.lines:
                        line.set_visible(False)
                    self.tooltip.set_visible(False)
                    self.canvas.draw_idle()
                return

            for line in self.lines:
                line.set_visible(True)
                line.set_xdata([event.xdata, event.xdata])

            self.tooltip.set_visible(True)
            
            distance = event.xdata
            tel_d1 = self.telemetry_data['d1'] # Dati del pilota di riferimento
            tel_d2 = self.telemetry_data['d2'] # Dati del pilota di confronto
            
            idx_d1 = np.searchsorted(tel_d1['Distance'], distance)
            idx_d2 = np.searchsorted(tel_d2['Distance'], distance)

            if idx_d1 >= len(tel_d1) or idx_d2 >= len(tel_d2):
                return

            data_d1 = tel_d1.iloc[idx_d1]
            data_d2 = tel_d2.iloc[idx_d2]
            
            d1_code = self.driver_codes['d1']
            d2_code = self.driver_codes['d2']
            
            delta = data_d2['DeltaTime']
            
            tooltip_text = (
                f"Dist: {int(distance):>5}m\n"
                f"----------------------\n"
                f"{'':<4} {'V':<4} {'RPM':<5} {'G':<2} {'Δ(s)':>6}\n"
                f"{d1_code:<4} {data_d1['Speed']:<4.0f} {data_d1['RPM']:<5.0f} {data_d1['nGear']:<2.0f} {'0.00':>6}\n"
                f"{d2_code:<4} {data_d2['Speed']:<4.0f} {data_d2['RPM']:<5.0f} {data_d2['nGear']:<2.0f} {delta: >+6.2f}"
            )
            self.tooltip.set_text(tooltip_text)

            # Anche la barra di stato ora mostra il gap correttamente
            status_bar_text = (
                f"Dist: {int(distance)}m | {d1_code}: V={data_d1['Speed']:.0f} | "
                f"{d2_code}: V={data_d2['Speed']:.0f} | Gap (vs {d1_code}): {delta:+.2f}s"
            )
            self.status_var.set(status_bar_text)
            
            self.canvas.draw_idle()
        except Exception as e:
            print(f"Errore nel cursore interattivo: {e}")

    def disconnect(self):
        if self.cid:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None