import tkinter as tk
import json
import threading
from Files.scripts import assets

# Variabile globale per il widget dello slider del volume
volume_slider = None

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"volume": 50}

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def apply_settings(): 
    global volume_slider
    assets.volume = volume_slider.get()
    save_settings({"volume": assets.volume})  # Corretto per salvare come dizionario

def open_settings_window():
    global volume_slider

    settings = load_settings()

    settings_window = tk.Tk()
    settings_window.title("Impostazioni del Gioco")

    tk.Label(settings_window, text="Volume:").pack()
    volume_slider = tk.Scale(settings_window, from_=0, to=100, orient=tk.HORIZONTAL)
    volume_slider.set(settings["volume"])  # Corretto per usare il valore del volume
    volume_slider.pack()

    apply_button = tk.Button(settings_window, text="Applica", command=apply_settings)
    apply_button.pack()

    settings_window.mainloop()