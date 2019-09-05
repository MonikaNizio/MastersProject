import tkinter as tk
from tkinter import filedialog
from bayesian import main_loop
from osc_client import run_client
# from osc_server import run_server
from process_audio import audio_to_array

#class GUI():

# def open_file(self, event=None):
#     self.filename = filedialog.askopenfilename()
#     print('Selected:', self.filename)

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

instruction_label = tk.Label(root,text="Load in your sound and let the program choose the synth settings for you", font=("arial",14,"bold")).pack()

open_file_button = tk.Button(root, text='Open', command=open_file)
open_file_button.pack()

start_button = tk.Button(root, text='Start', command=run_optimization)
start_button.pack()
# window.filename = tk.filedialog.askopenfilename(initialdir = "C:\"",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# print (window.filename)
root.mainloop()