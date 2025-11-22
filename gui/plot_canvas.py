import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class PlotCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Waveform")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_plot(self):
        if hasattr(self, 'cbar'):
            try:
                self.cbar.remove()
            except Exception:
                pass # Handle cases where it might already be gone or invalid
            del self.cbar
        self.ax.clear()

    def plot_waveform(self, data, fs):
        self.clear_plot()
        time = np.arange(len(data)) / fs
        self.ax.plot(time, data)
        self.ax.set_title("Waveform")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_spectrogram(self, spec_db, fs, hop_length):
        self.clear_plot()
        
        # Calculate time and frequency axes
        num_frames = spec_db.shape[1]
        num_freqs = spec_db.shape[0]
        
        # Time axis
        duration = (num_frames * hop_length) / fs
        
        # Display using imshow
        # origin='lower' puts low frequencies at the bottom
        # aspect='auto' scales the image to fit the axes
        img = self.ax.imshow(spec_db, origin='lower', aspect='auto', 
                             extent=[0, duration, 0, fs/2], cmap='inferno')
        
        self.ax.set_title("Spectrogram")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Frequency (Hz)")
        
        # Add colorbar
        self.cbar = self.figure.colorbar(img, ax=self.ax, format='%+2.0f dB')
        
        self.canvas.draw()
