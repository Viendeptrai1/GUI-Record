import numpy as np
from scipy.signal import correlate

class PitchAnalyzer:
    def __init__(self, fs=16000):
        self.fs = fs

    def compute_pitch(self, waveform, frame_size=0.03, hop_size=0.01, min_f0=50, max_f0=500):
        """
        Estimate pitch (F0) using Autocorrelation.
        
        Args:
            waveform (numpy.ndarray): Audio data.
            frame_size (float): Frame size in seconds.
            hop_size (float): Hop size in seconds.
            min_f0 (float): Minimum expected pitch.
            max_f0 (float): Maximum expected pitch.
            
        Returns:
            times (numpy.ndarray): Time points.
            f0s (numpy.ndarray): Estimated F0 values (0 for unvoiced).
        """
        if waveform.ndim > 1:
            waveform = waveform.squeeze()
            
        frame_length = int(frame_size * self.fs)
        hop_length = int(hop_size * self.fs)
        
        num_frames = (len(waveform) - frame_length) // hop_length
        f0s = np.zeros(num_frames)
        times = np.arange(num_frames) * hop_size + frame_size / 2
        
        for i in range(num_frames):
            start = i * hop_length
            end = start + frame_length
            frame = waveform[start:end]
            
            # Simple Voice Activity Detection (VAD) based on energy
            if np.sum(frame**2) < 0.001:
                f0s[i] = 0
                continue
                
            # Autocorrelation
            corr = correlate(frame, frame, mode='full')
            corr = corr[len(corr)//2:] # Keep positive lags
            
            # Find peak within expected range
            min_lag = int(self.fs / max_f0)
            max_lag = int(self.fs / min_f0)
            
            if max_lag >= len(corr):
                max_lag = len(corr) - 1
                
            if min_lag >= max_lag:
                 f0s[i] = 0
                 continue

            # Find peak in the lag range
            peak_idx = np.argmax(corr[min_lag:max_lag]) + min_lag
            
            # Threshold for voicing (peak strength)
            if corr[peak_idx] > 0.3 * corr[0]: # Heuristic threshold
                f0s[i] = self.fs / peak_idx
            else:
                f0s[i] = 0
                
        return times, f0s
