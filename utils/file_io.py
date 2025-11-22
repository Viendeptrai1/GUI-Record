import soundfile as sf
import numpy as np

def save_wav(filename, data, fs):
    """
    Save audio data to a WAV file.
    
    Args:
        filename (str): Path to save the file.
        data (numpy.ndarray): Audio data.
        fs (int): Sampling rate.
    """
    sf.write(filename, data, fs)

def load_wav(filename):
    """
    Load audio data from a WAV file.
    
    Args:
        filename (str): Path to the WAV file.
        
    Returns:
        tuple: (data, fs)
            data (numpy.ndarray): Audio data.
            fs (int): Sampling rate.
    """
    data, fs = sf.read(filename)
    return data, fs
