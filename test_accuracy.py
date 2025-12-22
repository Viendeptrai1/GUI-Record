import os
import glob
import pickle
import numpy as np
from src.signal_utils import read_wav, pre_emphasis, frame_signal, apply_window
from src.feature_extraction import compute_mfcc

MODEL_DIR = "models"
DATA_DIR = "zero_to_nine_voice"
DIGITS = list(range(10))

def load_models():
    models = {}
    for i in DIGITS:
        path = os.path.join(MODEL_DIR, f"hmm_{i}.pkl")
        if os.path.exists(path):
            with open(path, "rb") as f:
                models[i] = pickle.load(f)
    return models

def test_accuracy():
    models = load_models()
    if not models:
        print("No models found! Run train_scratch.py first.")
        return

    total = 0
    correct = 0
    
    print("Starting Accuracy Test (Using 20 samples per digit not used in training ideally)...")
    # In pro setup we split train/test. Here we iterate all or subset.
    # We used indices [:30] for training. Let's use [30:50] for testing.
    
    confusion_matrix = np.zeros((10, 10), dtype=int)
    
    for real_digit in DIGITS:
        digit_dir = os.path.join(DATA_DIR, str(real_digit))
        files = glob.glob(os.path.join(digit_dir, "*.wav"))
        
        test_files = files[30:50] # Use next 20 files
        
        for f in test_files:
            total += 1
            try:
                sr, signal = read_wav(f)
                if len(signal) == 0: continue
                
                signal = pre_emphasis(signal)
                frames = frame_signal(signal, sr)
                frames = apply_window(frames)
                mfcc = compute_mfcc(frames, sr)
                
                best_score = -float('inf')
                predicted = -1
                
                for digit, model in models.items():
                    score = model.score(mfcc)
                    if score > best_score:
                        best_score = score
                        predicted = digit
                
                if predicted == real_digit:
                    correct += 1
                
                confusion_matrix[real_digit, predicted] += 1
                
            except Exception as e:
                print(f"Error on {f}: {e}")

    accuracy = (correct / total) * 100 if total > 0 else 0
    print("-" * 30)
    print(f"Overall Accuracy: {accuracy:.2f}% ({correct}/{total})")
    print("Confusion Matrix (Row=Real, Col=Pred):")
    print(confusion_matrix)

if __name__ == "__main__":
    test_accuracy()
