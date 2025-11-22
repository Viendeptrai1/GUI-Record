import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from .toolbar import Toolbar
from .plot_canvas import PlotCanvas
from audio.recorder import AudioRecorder
from audio.player import AudioPlayer
from utils.file_io import save_wav, load_wav

from analysis.spectrogram import SpectrogramAnalyzer

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Processing App (Mini-Praat)")
        self.geometry("800x600")
        
        # Audio components
        self.recorder = AudioRecorder()
        self.player = AudioPlayer()
        self.analyzer = SpectrogramAnalyzer()
        
        self.audio_data = None
        self.fs = 16000
        self.current_view = 'waveform' # 'waveform', 'wideband', 'narrowband'
        
        # GUI Layout
        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Analysis Menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Show Waveform", command=lambda: self.switch_view('waveform'))
        analysis_menu.add_command(label="Show Wideband Spectrogram", command=lambda: self.switch_view('wideband'))
        analysis_menu.add_command(label="Show Narrowband Spectrogram", command=lambda: self.switch_view('narrowband'))
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        
        self.config(menu=menubar)

    def create_widgets(self):
        # Toolbar
        callbacks = {
            'record': self.start_recording,
            'stop': self.stop_recording,
            'play': self.play_audio,
            'save': self.save_audio
        }
        self.toolbar = Toolbar(self, callbacks)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar.set_state('idle')
        
        # Plot Area
        self.plot_canvas = PlotCanvas(self)
        self.plot_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def switch_view(self, view_type):
        self.current_view = view_type
        self.update_plot()

    def update_plot(self):
        if self.audio_data is None:
            return
            
        if self.current_view == 'waveform':
            self.plot_canvas.plot_waveform(self.audio_data, self.fs)
        elif self.current_view == 'wideband':
            params = self.analyzer.get_wideband_params()
            spec = self.analyzer.compute_spectrogram(self.audio_data, **params)
            self.plot_canvas.plot_spectrogram(spec, self.fs, params['hop_length'])
        elif self.current_view == 'narrowband':
            params = self.analyzer.get_narrowband_params()
            spec = self.analyzer.compute_spectrogram(self.audio_data, **params)
            self.plot_canvas.plot_spectrogram(spec, self.fs, params['hop_length'])

    def start_recording(self):
        self.status_var.set("Recording...")
        self.toolbar.set_state('recording')
        self.recorder.start_recording()

    def stop_recording(self):
        self.status_var.set("Processing...")
        self.audio_data = self.recorder.stop_recording()
        self.toolbar.set_state('has_data')
        self.status_var.set(f"Recorded {len(self.audio_data)/self.fs:.2f}s")
        
        # Update Plot
        self.update_plot()

    def play_audio(self):
        if self.audio_data is not None:
            self.status_var.set("Playing...")
            self.player.play(self.audio_data, self.fs)
            self.status_var.set("Ready")

    def save_audio(self):
        if self.audio_data is not None:
            filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if filename:
                save_wav(filename, self.audio_data, self.fs)
                self.status_var.set(f"Saved to {filename}")
