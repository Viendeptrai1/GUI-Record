import numpy as np
from scipy.io import wavfile

def read_wav(file_path):
    """
    Read a WAV file.
    Returns: (sample_rate, signal)
    """
    sr, signal = wavfile.read(file_path)
    # Convert to float to avoid overflow during processing
    signal = signal.astype(float)
    return sr, signal

def pre_emphasis(signal, alpha=0.97):
    """
    Apply pre-emphasis filter: y[t] = x[t] - alpha * x[t-1]
    """
    # Simple numpy slicing: signal[1:] - alpha * signal[:-1]
    # We append the first sample to match length
    emphasized_signal = np.append(signal[0], signal[1:] - alpha * signal[:-1])
    return emphasized_signal

def frame_signal(signal, sample_rate, frame_size=0.025, frame_stride=0.010):
    """
    Split signal into frames.
    frame_size: length of frame in seconds (default 25ms)
    frame_stride: step between frames in seconds (default 10ms)
    """
    signal_length = len(signal)
    frame_length = int(round(frame_size * sample_rate))
    frame_step = int(round(frame_stride * sample_rate))
    
    # Calculate number of frames
    num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step))
    
    # Pad Signal to make sure that all frames have equal number of samples
    pad_signal_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_signal_length - signal_length))
    pad_signal = np.append(signal, z)
    
    # Indices
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + \
              np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
              
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    return frames

def apply_window(frames, window_func=np.hamming):
    """
    Apply a window function (default Hamming) to each frame.
    w[n] = 0.54 - 0.46 * cos(2*pi*n / (N-1))
    """
    frame_length = frames.shape[1]
    # np.hamming returns the window
    window = window_func(frame_length)
    return frames * window
