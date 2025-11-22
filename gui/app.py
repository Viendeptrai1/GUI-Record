import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from .toolbar import Toolbar
from .plot_canvas import PlotCanvas
from audio.recorder import AudioRecorder
from audio.player import AudioPlayer
from utils.file_io import save_wav, load_wav

from analysis.spectrogram import SpectrogramAnalyzer
from analysis.pitch import PitchAnalyzer
from analysis.lpc import LPCAnalyzer
from annotation.textgrid import TextGrid
from gui.annotation_canvas import AnnotationCanvas

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Processing App (Mini-Praat)")
        self.geometry("800x700") # Increased height
        
        # Audio components
        self.recorder = AudioRecorder()
        self.player = AudioPlayer()
        self.analyzer = SpectrogramAnalyzer()
        self.pitch_analyzer = PitchAnalyzer()
        self.lpc_analyzer = LPCAnalyzer()
        
        self.audio_data = None
        self.fs = 16000
        self.textgrid = None
        
        self.current_view = 'waveform' # 'waveform', 'wideband', 'narrowband'
        self.show_pitch = tk.BooleanVar(value=False)
        
        self.view_start = 0
        self.view_end = 0 # Will be set when data is loaded
        
        # GUI Layout
        self.create_menu()
        self.create_widgets()
        
        # Bind events
        self.plot_canvas.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open TextGrid...", command=self.load_textgrid)
        file_menu.add_command(label="Save TextGrid...", command=self.save_textgrid)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Analysis Menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Show Waveform", command=lambda: self.switch_view('waveform'))
        analysis_menu.add_command(label="Show Wideband Spectrogram", command=lambda: self.switch_view('wideband'))
        analysis_menu.add_command(label="Show Narrowband Spectrogram", command=lambda: self.switch_view('narrowband'))
        analysis_menu.add_separator()
        analysis_menu.add_checkbutton(label="Show Pitch Contour", onvalue=True, offvalue=False, 
                                      variable=self.show_pitch, command=self.update_plot)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        
        self.config(menu=menubar)

    def create_widgets(self):
        # Toolbar
        callbacks = {
            'record': self.start_recording,
            'stop': self.stop_recording,
            'play': self.play_audio,
            'save': self.save_audio,
            'zoom_in': self.zoom_in,
            'zoom_out': self.zoom_out,
            'reset_view': self.reset_view,
            'pan_left': self.pan_left,
            'pan_right': self.pan_right
        }
        self.toolbar = Toolbar(self, callbacks)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar.set_state('idle')
        
        # Plot Area
        self.plot_canvas = PlotCanvas(self)
        self.plot_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Annotation Area
        self.annotation_canvas = AnnotationCanvas(self, None, 0)
        self.annotation_canvas.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        # Bind Shift+Click for editing label
        self.annotation_canvas.bind("<Shift-Button-1>", self.on_annotation_shift_click)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_annotation_shift_click(self, event):
        if self.textgrid:
            time = self.annotation_canvas.x_to_time(event.x)
            self.annotation_canvas.edit_label(time)

    def switch_view(self, view_type):
        self.current_view = view_type
        self.update_plot()

    def update_plot(self):
        if self.audio_data is None:
            return
            
        xlim = (self.view_start, self.view_end)
        
        if self.current_view == 'waveform':
            self.plot_canvas.plot_waveform(self.audio_data, self.fs, xlim=xlim)
        elif self.current_view in ['wideband', 'narrowband']:
            # Compute Spectrogram
            if self.current_view == 'wideband':
                params = self.analyzer.get_wideband_params()
            else:
                params = self.analyzer.get_narrowband_params()
                
            spec = self.analyzer.compute_spectrogram(self.audio_data, **params)
            self.plot_canvas.plot_spectrogram(spec, self.fs, params['hop_length'], xlim=xlim)
            
            # Compute and Overlay Pitch if enabled
            if self.show_pitch.get():
                times, f0s = self.pitch_analyzer.compute_pitch(self.audio_data)
                self.plot_canvas.plot_pitch(times, f0s)
        
        # Update Annotation Canvas View
        self.annotation_canvas.set_view(self.view_start, self.view_end)

    def zoom_in(self):
        center = (self.view_start + self.view_end) / 2
        duration = self.view_end - self.view_start
        new_duration = duration * 0.8
        self.view_start = max(0, center - new_duration / 2)
        self.view_end = min(len(self.audio_data)/self.fs, center + new_duration / 2)
        self.update_plot()

    def zoom_out(self):
        center = (self.view_start + self.view_end) / 2
        duration = self.view_end - self.view_start
        new_duration = duration * 1.25
        max_duration = len(self.audio_data)/self.fs
        self.view_start = max(0, center - new_duration / 2)
        self.view_end = min(max_duration, center + new_duration / 2)
        self.update_plot()

    def reset_view(self):
        self.view_start = 0
        self.view_end = len(self.audio_data)/self.fs
        self.update_plot()

    def pan_left(self):
        duration = self.view_end - self.view_start
        shift = duration * 0.2
        self.view_start = max(0, self.view_start - shift)
        self.view_end = self.view_start + duration
        self.update_plot()

    def pan_right(self):
        duration = self.view_end - self.view_start
        shift = duration * 0.2
        max_duration = len(self.audio_data)/self.fs
        self.view_end = min(max_duration, self.view_end + shift)
        self.view_start = self.view_end - duration
        self.update_plot()

    def on_canvas_click(self, event):
        if self.audio_data is None or event.xdata is None:
            return
            
        # Only trigger LPC if we are in Spectrogram view
        if self.current_view in ['wideband', 'narrowband']:
            time_point = event.xdata
            sample_idx = int(time_point * self.fs)
            
            # Extract a small frame around the click (e.g., 30ms)
            frame_len = int(0.03 * self.fs)
            start = max(0, sample_idx - frame_len // 2)
            end = min(len(self.audio_data), start + frame_len)
            frame = self.audio_data[start:end]
            
            if len(frame) < frame_len:
                return
                
            # Compute LPC
            a, g = self.lpc_analyzer.compute_lpc(frame)
            freqs, envelope = self.lpc_analyzer.get_spectral_envelope(a, g)
            formants = self.lpc_analyzer.get_formants(a)
            
            # Open a new window or plot on the same canvas?
            # For now, let's plot on the same canvas but replace the view temporarily
            # Or better, create a popup window for LPC slice
            self.show_lpc_popup(freqs, envelope, formants, time_point)

    def show_lpc_popup(self, freqs, envelope, formants, time_point):
        popup = tk.Toplevel(self)
        popup.title(f"LPC Analysis at {time_point:.3f}s")
        popup.geometry("600x400")
        
        canvas = PlotCanvas(popup)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.plot_lpc(freqs, envelope, formants)

    def start_recording(self):
        self.status_var.set("Recording...")
        self.toolbar.set_state('recording')
        self.recorder.start_recording()

    def stop_recording(self):
        self.status_var.set("Processing...")
        self.audio_data = self.recorder.stop_recording()
        self.toolbar.set_state('has_data')
        duration = len(self.audio_data)/self.fs
        self.status_var.set(f"Recorded {duration:.2f}s")
        
        # Initialize View
        self.view_start = 0
        self.view_end = duration
        
        # Initialize TextGrid
        self.textgrid = TextGrid(0, duration)
        self.annotation_canvas.set_textgrid(self.textgrid, duration)
        
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

    def load_textgrid(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                self.textgrid = TextGrid.from_json(filename)
                # We need to know duration to set up canvas properly. 
                # Assuming loaded textgrid matches current audio or just use textgrid's max
                duration = self.textgrid.xmax
                self.annotation_canvas.set_textgrid(self.textgrid, duration)
                self.status_var.set(f"Loaded TextGrid from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load TextGrid: {e}")

    def save_textgrid(self):
        if self.textgrid:
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filename:
                try:
                    self.textgrid.to_json(filename)
                    self.status_var.set(f"Saved TextGrid to {filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save TextGrid: {e}")
        else:
            messagebox.showwarning("Warning", "No TextGrid to save!")
