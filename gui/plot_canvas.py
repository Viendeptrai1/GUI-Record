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
        # Overlay pitch contour
        # We need to create a twin axis for pitch if we want a different scale, 
        # but for simplicity, let's just plot it on the same axis or a twinx
        # Since spectrogram is freq vs time, we can plot pitch (Hz) directly on it.
        self.ax.plot(times, f0s, color='cyan', linewidth=2, label='Pitch (F0)')
        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def plot_lpc(self, freqs, envelope, formants):
        for i, f in enumerate(formants[:3]): # Show first 3 formants
            self.ax.axvline(x=f, color='blue', linestyle='--', alpha=0.7)
            self.ax.text(f, np.max(envelope), f"F{i+1}={int(f)}", rotation=90, verticalalignment='top')
            
        self.ax.set_title("LPC Spectral Envelope")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude (dB)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def draw_cursor(self, time):
        # Remove previous cursor if exists
        if hasattr(self, 'cursor_line') and self.cursor_line:
            try:
                self.cursor_line.remove()
            except:
                pass
        
        # Draw new cursor
        self.cursor_line = self.ax.axvline(x=time, color='red', linewidth=1.5)
        self.canvas.draw()
        
    def clear_cursor(self):
        if hasattr(self, 'cursor_line') and self.cursor_line:
            try:
                self.cursor_line.remove()
                self.cursor_line = None
                self.canvas.draw()
            except:
                pass
