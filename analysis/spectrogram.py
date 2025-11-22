import torch
import torchaudio
import numpy as np

class SpectrogramAnalyzer:
    def __init__(self, fs=16000):
        self.fs = fs

    def compute_spectrogram(self, waveform, n_fft=400, win_length=None, hop_length=None):
        """
        Compute spectrogram using torchaudio.
        
        Args:
            waveform (numpy.ndarray): Audio data (1D array).
            n_fft (int): Size of FFT.
            win_length (int): Window size.
            hop_length (int): Hop length.
            
        Returns:
            numpy.ndarray: Spectrogram magnitude in dB.
        """
        if win_length is None:
            win_length = n_fft
        if hop_length is None:
            hop_length = win_length // 2
            
        # Convert numpy to torch tensor
        waveform_tensor = torch.from_numpy(waveform).float()
        
        # Ensure shape is (channels, time) or just (time)
        # sounddevice returns (N, 1), but torchaudio expects (..., time)
        if waveform_tensor.dim() == 2 and waveform_tensor.shape[1] == 1:
            waveform_tensor = waveform_tensor.t() # Convert (N, 1) -> (1, N)
        
        # Create Spectrogram transform
        spectrogram_transform = torchaudio.transforms.Spectrogram(
            n_fft=n_fft,
            win_length=win_length,
            hop_length=hop_length,
            power=2.0 # Power spectrogram
        )
        
        # Compute spectrogram
        spec = spectrogram_transform(waveform_tensor)
        
        # Convert to dB
        db_transform = torchaudio.transforms.AmplitudeToDB(stype="power", top_db=80)
        spec_db = db_transform(spec)
        
        # Remove channel dimension if present to return (Freq, Time)
        if spec_db.dim() == 3:
            spec_db = spec_db.squeeze(0)
            
        return spec_db.numpy()

    def get_wideband_params(self):
        """
        Wideband: Short window (~5ms) -> Good time resolution, poor frequency resolution.
        Used to see formants (vertical striations).
        """
        # For 16kHz, 5ms is 80 samples.
        # Let's use slightly larger for visibility, e.g., 8ms -> 128 samples
        # Or standard 256 (~16ms) is often used as a balance, but strict wideband is shorter.
        # Praat Wideband standard: 0.005s (5ms)
        win_size_sec = 0.005
        win_length = int(self.fs * win_size_sec)
        n_fft = 2 ** int(np.ceil(np.log2(win_length))) # Next power of 2
        if n_fft < win_length: n_fft *= 2
        
        return {
            'n_fft': n_fft,
            'win_length': win_length,
            'hop_length': win_length // 4 # 75% overlap
        }

    def get_narrowband_params(self):
        """
        Narrowband: Long window (~30ms) -> Good frequency resolution, poor time resolution.
        Used to see harmonics (horizontal lines).
        """
        # Praat Narrowband standard: 0.03s (30ms)
        win_size_sec = 0.03
        win_length = int(self.fs * win_size_sec)
        n_fft = 2 ** int(np.ceil(np.log2(win_length)))
        
        return {
            'n_fft': n_fft,
            'win_length': win_length,
            'hop_length': win_length // 4
        }
