import os
import glob
import numpy as np
import pickle
from src.signal_utils import read_wav, pre_emphasis, frame_signal, apply_window
from src.feature_extraction import compute_mfcc
from src.hmm_core import HMMManual

DATA_DIR = "zero_to_nine_voice"
MODEL_DIR = "models"
DIGITS = list(range(10))

def get_mfcc(file_path):
    sr, signal = read_wav(file_path)
    if len(signal) == 0:
        return None
    signal = pre_emphasis(signal)
    frames = frame_signal(signal, sr)
    frames = apply_window(frames)
    mfcc = compute_mfcc(frames, sr)
    return mfcc

def train_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    models = {}
    
    for digit in DIGITS:
        print(f"Loading data for digit {digit}...")
        digit_dir = os.path.join(DATA_DIR, str(digit))
        files = glob.glob(os.path.join(digit_dir, "*.wav"))
        
        # Limit mainly for speed during debugging? Or full? 
        # Let's take first 50 files for a quick first pass, user can scale up.
        # Hardcore mode: Use all!
        train_data = []
        for f in files[:30]: # Limit to 30 for quick Turn validation, user can remove limit
            mfcc = get_mfcc(f)
            if mfcc is not None and mfcc.shape[0] > 0:
                train_data.append(mfcc)
        
        if not train_data:
            print(f"No data for {digit}")
            continue
            
        print(f"Training HMM for {digit} with {len(train_data)} samples...")
        hmm = HMMManual(n_states=5, n_iter=5) # 5 states, 5 iters for test
        hmm.train(train_data)
        
        models[digit] = hmm
        
        # Save
        with open(os.path.join(MODEL_DIR, f"hmm_{digit}.pkl"), "wb") as f:
            pickle.dump(hmm, f)
            
    print("Training Complete!")

if __name__ == "__main__":
    train_models()
