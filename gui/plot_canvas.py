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

    def plot_waveform(self, data, fs, xlim=None):
        self.clear_plot()
        time = np.arange(len(data)) / fs
        self.ax.plot(time, data)
        self.ax.set_title("Waveform")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        if xlim:
            self.ax.set_xlim(xlim)
        self.canvas.draw()

    def plot_spectrogram(self, spec_db, fs, hop_length, xlim=None):
        self.clear_plot()
        
        # Calculate time and frequency axes
        num_frames = spec_db.shape[1]
        num_freqs = spec_db.shape[0]
        
        # Time axis
        duration = (num_frames * hop_length) / fs
        
        # Display using imshow
        img = self.ax.imshow(spec_db, origin='lower', aspect='auto', 
                             extent=[0, duration, 0, fs/2], cmap='inferno')
        
        self.ax.set_title("Spectrogram")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Frequency (Hz)")
        
        if xlim:
            self.ax.set_xlim(xlim)
            
        # Add colorbar
        self.cbar = self.figure.colorbar(img, ax=self.ax, format='%+2.0f dB')
        
        self.canvas.draw()

    def plot_pitch(self, times, f0s):
        # Filter unvoiced (0)
        times_v = times[f0s > 0]
        f0s_v = f0s[f0s > 0]
        
        # Plot on a secondary axis if needed, or just overlay
        # For simplicity, overlaying on Spectrogram (which is Hz vs Time)
        self.ax.plot(times_v, f0s_v, color='cyan', linewidth=2, label='Pitch (F0)')
        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def plot_lpc(self, freqs, envelope, formants):
        # Plot LPC envelope on a new figure or overlay?
        # Usually LPC is a slice at a specific time, so it's Amplitude vs Frequency
        # We should probably clear and draw this as a 2D plot
        self.clear_plot()
        
        self.ax.plot(freqs, envelope, color='red', linewidth=2, label='LPC Envelope')
        
        # Mark formants
        for i, f in enumerate(formants[:3]): # Show first 3 formants
            self.ax.axvline(x=f, color='blue', linestyle='--', alpha=0.7)
            self.ax.text(f, np.max(envelope), f"F{i+1}={int(f)}", rotation=90, verticalalignment='top')
            
        self.ax.set_title("LPC Spectral Envelope")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude (dB)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
