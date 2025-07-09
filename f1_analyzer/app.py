# File: f1_analyzer/app.py

import tkinter as tk
from tkinter import ttk, messagebox
import fastf1 as ff1
import threading
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa dal pacchetto locale
from .modules.box_plot import create_plot as create_box_plot

class F1AnalyzerApp:
    def __init__(self, root):
        """
        Il costruttore della classe. Questo metodo costruisce l'intera interfaccia grafica.
        """
        self.root = root
        self.root.title("Analizzatore Dati Formula 1 (v3.0 Strutturato)")
        self.root.geometry("1200x800")

        # --- Frame per i controlli (la barra in alto) ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side="top", fill="x")

        # --- Creazione di TUTTI i Widget ---
        ttk.Label(control_frame, text="Anno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.year_spinbox = ttk.Spinbox(control_frame, from_=1950, to=datetime.now().year, textvariable=self.year_var, width=10)
        self.year_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Evento:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.event_var = tk.StringVar()
        self.event_combo = ttk.Combobox(control_frame, textvariable=self.event_var, state="disabled")
        self.event_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Sessione:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.session_var = tk.StringVar()
        self.session_combo = ttk.Combobox(control_frame, textvariable=self.session_var, values=['R', 'Q', 'S', 'FP1', 'FP2', 'FP3'])
        self.session_combo.set('R')
        self.session_combo.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        self.analyze_button = ttk.Button(control_frame, text="Genera Box Plot", command=self.start_analysis_thread)
        self.analyze_button.grid(row=0, column=6, padx=10, pady=5, sticky="ew")
        
        # --- Status bar in basso ---
        self.status_var = tk.StringVar(value="Pronto. Seleziona una sessione.")
        ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w").pack(side="bottom", fill="x")

        # --- Frame per il grafico (l'area grande) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side="top", fill="both", expand=True) # "top" dopo la status bar in "bottom" riempie lo spazio centrale
        self.canvas = None

        # --- Collegamento Eventi ---
        self.year_var.trace_add("write", self.update_event_dropdown)
        
        # Inizializza la lista eventi per l'anno corrente all'avvio
        self.update_event_dropdown()

    def update_event_dropdown(self, *args):
        # Il resto dei metodi della classe sono invariati...
        try:
            year = self.year_var.get()
            self.status_var.set(f"Recupero calendario per il {year}...")
            schedule = ff1.get_event_schedule(year)
            self.event_combo['values'] = schedule['EventName'].tolist()
            if schedule['EventName'].tolist(): # Controlla se la lista non è vuota
                self.event_combo.set(schedule['EventName'].iloc[0])
            self.event_combo['state'] = 'readonly'
            self.status_var.set("Pronto.")
        except Exception as e:
            self.status_var.set(f"Errore nel recupero calendario per il {year}.")
            self.event_combo['values'] = []
            self.event_combo['state'] = 'disabled'

    def start_analysis_thread(self):
        self.analyze_button['state'] = 'disabled'
        self.status_var.set("Caricamento dati...")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            year = self.year_var.get()
            event = self.event_var.get()
            session_type = self.session_var.get()
            
            session = ff1.get_session(year, event, session_type)
            session.load()
            
            fig = create_box_plot(session)
            
            if fig is None:
                messagebox.showerror("Analisi Fallita", "La funzione di analisi non ha restituito un grafico. Potrebbero mancare dati sufficienti.")
            else:
                self.display_plot(fig)
                self.status_var.set("Grafico generato con successo.")

        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante l'analisi:\n{e}")
            self.status_var.set("Errore durante l'analisi.")
        
        self.analyze_button['state'] = 'normal'

    def display_plot(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)