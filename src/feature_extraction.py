import numpy as np
from scipy.fftpack import dct

def compute_fft_power(frames, NFFT=512):
    """
    Compute Power Spectrum of each frame.
    1. Apply FFT (np.fft.rfft for real input)
    2. Compute Power: |FFT|^2 / N
    """
    # rfft returns NFFT/2 + 1 bins
    mag_frames = np.absolute(np.fft.rfft(frames, NFFT))
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
    return pow_frames

def create_mel_filterbank(sample_rate, NFFT=512, nfilt=40):
    """
    Create Mel Filterbank Matrix manually.
    """
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    
    # We want 'nfilt' banks, so we need nfilt+2 points
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
            
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
            
    return fbank

def compute_mfcc(frames, sample_rate, num_ceps=12, nfilt=26, NFFT=512):
    """
    Full pipeline: Frames -> Power Spec -> Mel Filterbank -> Log -> DCT -> MFCC
    """
    pow_frames = compute_fft_power(frames, NFFT)
    
    # Check energy to prevent log(0)
    pow_frames[pow_frames == 0] = np.finfo(float).eps
    
    fbank = create_mel_filterbank(sample_rate, NFFT, nfilt)
    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = np.log(filter_banks)
    
    # DCT to get MFCC
    # type=2 is the standard, norm='ortho' is common
    mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')
    
    # Keep only 2 to num_ceps+1 (discard 0th usually, but some keep it)
    # Let's keep 1-13 (indices 1 to 13) or 0-12 depending on preference.
    # Usually coefficient 0 is energy, we handle it separately or keep it.
    # User plan: 13 coeffs.
    mfcc = mfcc[:, :num_ceps] 
    
    # Sinusoidal liftering (optional but good for speech)
    # cep_lifter = 22
    # nframes, ncoeff = mfcc.shape
    # n = np.arange(ncoeff)
    # lift = 1 + (cep_lifter / 2) * np.sin(np.pi * n / cep_lifter)
    # mfcc *= lift
    
    return mfcc
