import tkinter as tk
from tkinter import ttk, messagebox
import fastf1 as ff1
import threading
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Importa i moduli delle analisi e il nuovo cursore interattivo
from .modules.box_plot import create_plot as create_box_plot
from .modules.telemetry_comparison import create_plot as create_telemetry_plot
from .modules.interactive_cursor import InteractiveCursor

# --- NUOVO BLOCCO PER L'ICONA SULLA BARRA DELLE APPLICAZIONI (SOLO PER WINDOWS) ---
try:
    from ctypes import windll
    # Scegli un ID unico per la tua app. Può essere qualsiasi cosa, ma questo formato è standard.
    myappid = 'mycompany.myproduct.subproduct.version' 
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    # Se non siamo su Windows o ctypes non è disponibile, ignora semplicemente
    pass
# --- FINE NUOVO BLOCCO ---


class F1AnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Analysis Hub (v5.1 - Icona Finale)")
        self.root.geometry("1900x1000")

        # --- IMPOSTA ICONA PERSONALIZZATA (Metodo Robusto con Pathlib) ---
        try:
            project_root = Path(__file__).resolve().parent.parent
            icon_path = project_root / "assets" / "logo.ico"
            
            if not icon_path.is_file():
                raise FileNotFoundError(f"Icona non trovata al percorso: {icon_path}")
            
            # Questa imposta l'icona della finestra E, grazie al blocco sopra,
            # anche quella sulla barra delle applicazioni.
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Errore nel caricamento dell'icona: {e}")
        # --- FINE BLOCCO ICONA ---
        
        try:
            self.root.state('zoomed')
        except tk.TclError:
            print("Impossibile avviare la finestra massimizzata.")

        # ... (TUTTO IL RESTO DEL CODICE DA QUI IN POI RIMANE IDENTICO) ...
        # ... (assicurati di avere tutto il resto del tuo codice qui) ...
        self.schedule = None
        self.session = None
        self.loaded_session_details = None
        self.driver_list = []
        self.loading_thread = None
        self.analysis_functions = {
            "Lap Time Distribution (Box Plot)": create_box_plot,
            "Telemetry Comparison": create_telemetry_plot,
        }

        # Stile UI
        style = ttk.Style()
        try: style.theme_use('clam')
        except tk.TclError: print("Tema 'clam' non disponibile.")
        font_style = ('Calibri', 14)
        style.configure('TLabel', font=font_style, padding=5)
        style.configure('TButton', font=(font_style[0], font_style[1], 'bold'), padding=10)
        style.configure('TCombobox', font=font_style)
        self.root.option_add("*TSpinbox*Font", font_style)

        # FRAME CONTROLLI PRINCIPALI
        control_frame = ttk.Frame(root, padding="10 20 10 10")
        control_frame.pack(side="top", fill="x")
        control_frame.grid_columnconfigure((0, 8), weight=1)

        ttk.Label(control_frame, text="Anno:").grid(row=0, column=1, sticky="w")
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.year_spinbox = ttk.Spinbox(control_frame, from_=1950, to=datetime.now().year, textvariable=self.year_var, width=8, command=self.on_year_change)
        self.year_spinbox.grid(row=0, column=2, padx=5, sticky="ew")

        ttk.Label(control_frame, text="Evento:").grid(row=0, column=3, sticky="w")
        self.event_var = tk.StringVar()
        self.event_combo = ttk.Combobox(control_frame, textvariable=self.event_var, state="disabled", width=30)
        self.event_combo.grid(row=0, column=4, padx=5, sticky="ew")

        ttk.Label(control_frame, text="Sessione:").grid(row=0, column=5, sticky="w")
        self.session_var = tk.StringVar()
        self.session_combo = ttk.Combobox(control_frame, textvariable=self.session_var, state="disabled", width=12)
        self.session_combo.grid(row=0, column=6, padx=5, sticky="w")
        
        self.load_button = ttk.Button(control_frame, text="Carica Dati", command=self.load_session_data, state='disabled')
        self.load_button.grid(row=0, column=7, padx=10, sticky="ew")

        # FRAME CONTROLLI ANALISI
        self.analysis_options_frame = ttk.Frame(root, padding="10 10 10 20")
        self.analysis_options_frame.pack(side="top", fill="x")
        self.analysis_options_frame.grid_columnconfigure((0, 5), weight=1)

        ttk.Label(self.analysis_options_frame, text="Analisi:").grid(row=0, column=1, sticky="w")
        self.analysis_var = tk.StringVar()
        analysis_options = list(self.analysis_functions.keys())
        self.analysis_combo = ttk.Combobox(self.analysis_options_frame, textvariable=self.analysis_var, state="readonly", width=30, values=analysis_options)
        self.analysis_combo.grid(row=0, column=2, padx=5, sticky="ew")

        self.driver1_label = ttk.Label(self.analysis_options_frame, text="Pilota 1:")
        self.driver1_var = tk.StringVar()
        self.driver1_combo = ttk.Combobox(self.analysis_options_frame, textvariable=self.driver1_var, state="disabled", width=10)
        self.driver2_label = ttk.Label(self.analysis_options_frame, text="Pilota 2:")
        self.driver2_var = tk.StringVar()
        self.driver2_combo = ttk.Combobox(self.analysis_options_frame, textvariable=self.driver2_var, state="disabled", width=10)
        
        self.analyze_button = ttk.Button(self.analysis_options_frame, text="Genera Analisi", command=self.start_analysis_thread, state='disabled')
        self.analyze_button.grid(row=0, column=4, padx=20, sticky="ew")
        
        # BARRA DI STATO, FRAME GRAFICO E VARIABILI INTERATTIVE
        self.status_var = tk.StringVar(value="Benvenuto! Seleziona un anno per iniziare.")
        ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", font=('Calibri', 11), padding=5).pack(side="bottom", fill="x")
        
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.canvas = None
        
        self.current_fig = None
        self.interactive_cursor = None
        self.interactive_data = None
        self.driver_codes = None

        # COLLEGAMENTO EVENTI
        self.event_var.trace_add("write", self.on_event_change)
        self.session_var.trace_add("write", self.on_session_change)
        self.analysis_var.trace_add("write", self.on_analysis_selected)
        
        self.on_year_change()

    # --- INIZIO SEZIONE METODI ---

    def display_plot(self, fig):
        if self.canvas:
            if self.interactive_cursor:
                self.interactive_cursor.disconnect()
                self.interactive_cursor = None
            self.canvas.get_tk_widget().destroy()
        if self.current_fig:
            plt.close(self.current_fig)

        self.current_fig = fig
        self.canvas = FigureCanvasTkAgg(self.current_fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        if self.interactive_data and self.analysis_var.get() == "Telemetry Comparison":
            self.interactive_cursor = InteractiveCursor(
                fig=self.current_fig, # <-- PASSA L'INTERA FIGURA
                canvas=self.canvas,
                axes=self.current_fig.get_axes(),
                telemetry_data=self.interactive_data,
                driver_codes=self.driver_codes,
                status_var=self.status_var
            )

    def run_analysis(self):
        try:
            if not self.session or not self.loaded_session_details:
                raise ValueError("Dati della sessione non caricati.")
            
            analysis_name = self.analysis_var.get()
            if not analysis_name: raise ValueError("Seleziona un'analisi.")
            
            plot_function = self.analysis_functions[analysis_name]
            fig = None
            self.interactive_data = None

            if analysis_name == "Telemetry Comparison":
                d1, d2 = self.driver1_var.get(), self.driver2_var.get()
                if not d1 or not d2 or d1 == d2: raise ValueError("Seleziona due piloti diversi.")
                fig, tel_d1, tel_d2 = plot_function(self.session, d1, d2)
                
                if tel_d1 is not None and tel_d2 is not None:
                    self.interactive_data = {'d1': tel_d1, 'd2': tel_d2}
                    self.driver_codes = {'d1': d1, 'd2': d2}
            else:
                result = plot_function(self.session)
                if isinstance(result, tuple): fig = result[0]
                else: fig = result

            if fig:
                self.root.after(0, self.display_plot, fig)
                status_msg = "Grafico generato. Muovi il mouse per i dettagli." if self.interactive_data else "Grafico generato."
                self.root.after(0, self.status_var.set, status_msg)
            else:
                raise ValueError("L'analisi non ha prodotto un grafico.")
        except Exception as e:
            self.root.after(0, lambda: messagebox.showwarning("Analisi Fallita", f"{e}"))
            self.root.after(0, self.status_var.set, "Analisi fallita.")
        finally:
            self.root.after(0, self.update_button_states)

    def update_button_states(self):
        data_loaded = self.loaded_session_details == (self.year_var.get(), self.event_var.get(), self.session_var.get())
        can_load = bool(self.session_var.get()) and not data_loaded
        self.load_button.config(state='normal' if can_load else 'disabled')
        self.analyze_button.config(state='normal' if data_loaded else 'disabled')

    def on_year_change(self, *args):
        self.status_var.set(f"Recupero calendario per il {self.year_var.get()}...")
        threading.Thread(target=self._update_event_list_thread, daemon=True).start()

    def _update_event_list_thread(self):
        try:
            self.schedule = ff1.get_event_schedule(self.year_var.get(), include_testing=True)
            event_names = self.schedule['EventName'].tolist()
            self.root.after(0, self.update_event_ui, event_names)
        except Exception as e:
            self.root.after(0, self.status_var.set, f"Errore calendario: {e}")

    def update_event_ui(self, event_names):
        if event_names:
            self.event_combo.config(values=event_names, state='readonly')
            self.event_var.set(event_names[0])
        else:
            self.event_combo.config(values=[], state='disabled'); self.event_var.set('')
            self.session_combo.config(values=[], state='disabled'); self.session_var.set('')
        self.update_button_states()

    def on_event_change(self, *args):
        event_name = self.event_var.get()
        if not event_name: return
        self.status_var.set(f"Caricamento sessioni per {event_name}...")
        threading.Thread(target=self._get_sessions_thread, daemon=True).start()

    def _get_sessions_thread(self):
        try:
            event_name = self.event_var.get()
            sessions = []
            if 'pre-season' in event_name.lower():
                sessions = ['Day 1', 'Day 2', 'Day 3']
            else:
                if self.schedule is not None and not self.schedule.empty:
                    event_row = self.schedule.loc[self.schedule['EventName'] == event_name].iloc[0]
                    session_columns = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
                    for col in session_columns:
                        if pd.notna(event_row[col]) and event_row[col]:
                            sessions.append(event_row[col])
            self.root.after(0, self._update_session_ui, sessions)
        except Exception as e:
            print(f"ERRORE CRITICO nel caricare le sessioni: {e}")
            self.root.after(0, self._update_session_ui, [])

    def _update_session_ui(self, sessions):
        if sessions:
            self.session_combo.config(values=sessions, state='readonly')
            self.session_var.set(sessions[-1])
        else:
            self.session_combo.config(values=[], state='disabled'); self.session_var.set('')
        self.on_session_change()

    def on_session_change(self, *args):
        self.session = None; self.driver_list = []
        self.driver1_combo.config(state='disabled', values=[]); self.driver1_var.set('')
        self.driver2_combo.config(state='disabled', values=[]); self.driver2_var.set('')
        if self.loaded_session_details != (self.year_var.get(), self.event_var.get(), self.session_var.get()):
            self.loaded_session_details = None
        self.update_button_states()
        self.on_analysis_selected()

    def on_analysis_selected(self, *args):
        is_telemetry = self.analysis_var.get() == "Telemetry Comparison"
        if is_telemetry:
            self.driver1_label.grid(row=1, column=1, pady=10, sticky="w"); self.driver1_combo.grid(row=1, column=2, padx=5, pady=10, sticky="ew")
            self.driver2_label.grid(row=2, column=1, sticky="w"); self.driver2_combo.grid(row=2, column=2, padx=5, sticky="ew")
        else:
            self.driver1_label.grid_forget(); self.driver1_combo.grid_forget()
            self.driver2_label.grid_forget(); self.driver2_combo.grid_forget()

    def load_session_data(self):
        if self.loading_thread and self.loading_thread.is_alive(): return
        self.load_button.config(state='disabled'); self.analyze_button.config(state='disabled')
        self.status_var.set("Caricamento dati in corso...")
        self.loading_thread = threading.Thread(target=self._load_session_thread, daemon=True)
        self.loading_thread.start()

    def _load_session_thread(self):
        try:
            year, event, session_type = self.year_var.get(), self.event_var.get(), self.session_var.get()
            ff1.Cache.enable_cache(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cache'))
            self.session = ff1.get_session(year, event, session_type)
            self.session.load(laps=True, telemetry=True, weather=False, messages=False)
            if self.session.laps is None or self.session.laps.empty:
                raise ValueError(f"Dati non trovati per {event} - {session_type}.")
            self.loaded_session_details = (year, event, session_type)
            self.driver_list = sorted(self.session.laps['Driver'].unique())
            self.root.after(0, self.on_load_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_load_fail(e))

    def on_load_success(self):
        self.update_driver_combos()
        self.status_var.set("Dati caricati. Seleziona un'analisi e genera il grafico.")
        self.update_button_states()

    def on_load_fail(self, exc):
        messagebox.showerror("Errore di Caricamento", f"Impossibile caricare i dati: {exc}")
        self.status_var.set("Caricamento fallito.")
        self.loaded_session_details = None
        self.update_button_states()

    def update_driver_combos(self):
        self.driver1_combo['values'] = self.driver_list; self.driver2_combo['values'] = self.driver_list
        if self.driver_list:
            self.driver1_combo.config(state='readonly'); self.driver2_combo.config(state='readonly')
            if len(self.driver_list) > 0: self.driver1_var.set(self.driver_list[0])
            if len(self.driver_list) > 1: self.driver2_var.set(self.driver_list[1])

    def start_analysis_thread(self):
        self.analyze_button['state'] = 'disabled'
        self.status_var.set("Generazione grafico in corso...")
        threading.Thread(target=self.run_analysis, daemon=True).start()