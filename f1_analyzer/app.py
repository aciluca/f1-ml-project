# File: f1_analyzer/app.py

import tkinter as tk
from tkinter import ttk, messagebox
import fastf1 as ff1
import threading
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

from .modules.box_plot import create_plot as create_box_plot

class F1AnalyzerApp:
    def __init__(self, root):
        """
        Il costruttore della classe. Questo metodo costruisce l'intera interfaccia grafica.
        """
        self.root = root
        self.root.title("Analizzatore Dati Formula 1 (v0.3 Ottimizzato)")
        self.root.geometry("1900x1000")

        # Variabile di istanza per memorizzare lo schedule dell'anno
        self.schedule = None

        # --- Frame per i controlli (la barra in alto) ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side="top", fill="x")

        # --- Creazione di TUTTI i Widget ---
        ttk.Label(control_frame, text="Anno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.year_var = tk.IntVar(value=datetime.now().year)
        # NOTA: Usare `command` è più affidabile per lo Spinbox rispetto a `trace_add`
        self.year_spinbox = ttk.Spinbox(control_frame, from_=1950, to=datetime.now().year, textvariable=self.year_var, width=10, command=self.update_event_list)
        self.year_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Evento:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.event_var = tk.StringVar()
        self.event_combo = ttk.Combobox(control_frame, textvariable=self.event_var, state="disabled")
        self.event_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Sessione:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.session_var = tk.StringVar()
        self.session_combo = ttk.Combobox(control_frame, textvariable=self.session_var, state="disabled")
        # I valori verranno impostati dinamicamente
        self.session_combo.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        self.analyze_button = ttk.Button(control_frame, text="Genera Box Plot", command=self.start_analysis_thread)
        self.analyze_button.grid(row=0, column=6, padx=10, pady=5, sticky="ew")
        
        # --- Status bar in basso ---
        self.status_var = tk.StringVar(value="Pronto. Seleziona un anno.")
        ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w").pack(side="bottom", fill="x")

        # --- Frame per il grafico (l'area grande) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side="top", fill="both", expand=True)
        self.canvas = None

        # --- Collegamento Eventi ---
        # `trace_add` è più adatto per il Combobox, `command` per lo Spinbox
        self.year_var.trace_add("write", self.update_event_list)
        self.event_var.trace_add("write", self.update_session_list)
        
        # Inizializza la lista eventi per l'anno corrente all'avvio
        self.update_event_list()

    # --- METODI LOGICI (MODIFICATI E OTTIMIZZATI) ---

    def update_event_list(self, *args):
        """
        Recupera il calendario eventi per l'anno selezionato e popola
        il dropdown degli eventi. Questa funzione viene chiamata quando l'anno cambia.
        """
        try:
            year = int(self.year_var.get())
            self.status_var.set(f"Recupero calendario per il {year}...")
            
            # Memorizziamo lo schedule per non doverlo richiamare
            self.schedule = ff1.get_event_schedule(year, include_testing=False)
            
            event_names = self.schedule['EventName'].tolist()
            
            self.event_combo['values'] = event_names
            
            if event_names:
                self.event_var.set(event_names[0]) # Imposta il primo evento e scatena update_session_list
                self.event_combo['state'] = 'readonly'
            else:
                self.status_var.set(f"Nessun evento trovato per il {year}.")
                self.event_combo['values'] = []
                self.event_combo['state'] = 'disabled'
                self.session_combo['values'] = []
                self.session_combo['state'] = 'disabled'

            # La status bar verrà aggiornata dalla funzione successiva
        except Exception as e:
            self.status_var.set(f"Errore nel recupero calendario per il {year}.")
            self.event_combo['values'] = []
            self.event_combo['state'] = 'disabled'
            self.session_combo['values'] = []
            self.session_combo['state'] = 'disabled'

    def update_session_list(self, *args):
        """
        Controlla il formato dell'evento (sprint o convenzionale) e aggiorna
        il dropdown delle sessioni di conseguenza.
        """
        try:
            event_name = self.event_var.get()
            
            if not event_name or self.schedule is None:
                return

            self.status_var.set(f"Controllo formato per {event_name}...")
            
            event_info = self.schedule.loc[self.schedule['EventName'] == event_name].iloc[0]
            event_format = event_info['EventFormat']
            
            testing_sessions =
            sprint_sessions = ['R', 'Q', 'S', 'SQ', 'FP1']
            regular_sessions = ['R', 'Q', 'FP1', 'FP2', 'FP3']

            if 'sprint' in event_format:
                self.session_combo['values'] = sprint_sessions
            else: # 'conventional'
                self.session_combo['values'] = regular_sessions
            
            if self.session_combo['values']:
                self.session_var.set(self.session_combo['values'][0])
                self.session_combo['state'] = 'readonly'
            else:
                self.session_combo['state'] = 'disabled'

            self.status_var.set("Pronto.")
            
        except (IndexError, KeyError):
             # Questo può accadere se il nome evento non è nello schedule (caso raro)
            self.status_var.set(f"Formato per '{event_name}' non trovato.")
            self.session_combo['values'] = []
            self.session_combo['state'] = 'disabled'
        except Exception as e:
            self.status_var.set(f"Errore: {e}")
            self.session_combo['values'] = []
            self.session_combo['state'] = 'disabled'
            
    def start_analysis_thread(self):
        # Disabilita i controlli per evitare input multipli
        self.analyze_button['state'] = 'disabled'
        self.year_spinbox['state'] = 'disabled'
        self.event_combo['state'] = 'disabled'
        self.session_combo['state'] = 'disabled'
        
        self.status_var.set("Caricamento dati in corso...")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            year = self.year_var.get()
            event = self.event_var.get()
            session_type = self.session_var.get()
            
            session = ff1.get_session(year, event, session_type)
            # Abilita il caching per non scaricare sempre gli stessi dati
            current_dir = os.path.dirname(os.path.abspath(__file__))
            cache_dir = os.path.join(current_dir, '..', 'cache') # Vai su di un livello e poi entra in 'cache'
        
        # Normalizza il percorso per risolvere i '..' e renderlo pulito
            cache_dir = os.path.normpath(cache_dir)
        
        # Crea la directory se non esiste
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            
            ff1.Cache.enable_cache(cache_dir)
            session.load()
            
            fig = create_box_plot(session)
            
            if fig is None:
                messagebox.showerror("Analisi Fallita", "La funzione di analisi non ha restituito un grafico. Potrebbero mancare dati sufficienti.")
                self.status_var.set("Analisi fallita. Dati insufficienti.")
            else:
                self.display_plot(fig)
                self.status_var.set("Grafico generato con successo.")

        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante l'analisi:\n{e}")
            self.status_var.set("Errore durante l'analisi.")
        
        # Riabilita i controlli una volta finito
        self.analyze_button['state'] = 'normal'
        self.year_spinbox['state'] = 'normal'
        self.event_combo['state'] = 'readonly' # Mantiene lo stato corretto
        self.session_combo['state'] = 'readonly'

    def display_plot(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        # È buona norma chiudere la figura per liberare memoria dopo averla disegnata
        plt.close(fig)