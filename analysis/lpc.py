import numpy as np
from scipy.linalg import solve_toeplitz

class LPCAnalyzer:
    def __init__(self, fs=16000, order=12):
        self.fs = fs
        self.order = order

    def compute_lpc(self, frame):
        """
        Compute LPC coefficients using Levinson-Durbin recursion (via solve_toeplitz).
        
        Args:
            frame (numpy.ndarray): Audio frame.
            
        Returns:
            a (numpy.ndarray): LPC coefficients (including a0=1).
            g (float): Gain (error).
        """
        # Windowing
        window = np.hanning(len(frame))
        frame_w = frame * window
        
        # Autocorrelation
        r = np.correlate(frame_w, frame_w, mode='full')
        r = r[len(r)//2 : len(r)//2 + self.order + 1]
        
        # Levinson-Durbin (using Toeplitz solver for stability/simplicity)
        # R * a = -r[1:]  where R is Toeplitz matrix of r[:-1]
        # a = [1, a1, a2, ...]
        
        if r[0] == 0:
            return np.zeros(self.order + 1), 0
            
        a_coeffs = solve_toeplitz((r[:-1], r[:-1]), -r[1:])
        a = np.concatenate(([1], a_coeffs))
        
        # Calculate gain (prediction error)
        # E = r[0] + sum(a_k * r_k)
        err = r[0] + np.dot(a_coeffs, r[1:])
        g = np.sqrt(np.abs(err))
        
        return a, g

    def get_formants(self, a):
        """
        Estimate formants from LPC coefficients.
        
        Args:
            a (numpy.ndarray): LPC coefficients.
            
        Returns:
            formants (list): List of formant frequencies (F1, F2, ...).
        """
        # Find roots of the polynomial A(z)
        roots = np.roots(a)
        
        # Filter roots: keep only those with positive imaginary part (upper half circle)
        roots = [r for r in roots if np.imag(r) > 0]
        
        # Calculate frequencies and bandwidths
        angles = np.angle(roots)
        freqs = angles * (self.fs / (2 * np.pi))
        
        # Sort by frequency
        freqs = sorted(freqs)
        
        # Simple filtering: Formants are usually > 90Hz
        formants = [f for f in freqs if f > 90]
        
        return formants

    def get_spectral_envelope(self, a, g, n_fft=512):
        """
        Compute spectral envelope from LPC coefficients.
        H(z) = G / A(z)
        """
        w, h = np.fft.freqz([g], a, worN=n_fft, fs=self.fs)
        return w, 20 * np.log10(np.abs(h))
