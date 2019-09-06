import tkinter as tk
from tkinter import filedialog
from bayesian import main_loop
from osc_client import run_client
from process_audio import audio_to_array

def open_file():
    root.filename = filedialog.askopenfilename(initialdir="C:/", title="Select a file", filetypes=(("wav files", ".wav"), ("All files", "*.*")))
    file_location = tk.Label(root, text=root.filename)
    file_location.pack()

def run_optimization():
    main_loop(root.filename)


#filename = ''
root = tk.Tk()
root.geometry("700x500")
root.title("Synth machine learning app")
root.filename = "synth_samples/synth1.wav"

instruction_label = tk.Label(root,text="Load in your sound (1s) and let the program choose the optimal synth settings", font=("arial",13,"bold")).pack()

open_file_button = tk.Button(root, text='Open', command=open_file)
open_file_button.pack()

start_button = tk.Button(root, text='Start', command=run_optimization)
start_button.pack()
root.mainloop()