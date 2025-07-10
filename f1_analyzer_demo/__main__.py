# File: f1_analyzer/__main__.py

import tkinter as tk
from .app_streamlit import F1AnalyzerApp  # Importa la classe GUI dal file app.py

def main():
    """Funzione principale per lanciare l'applicazione."""
    root = tk.Tk()
    app = F1AnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()