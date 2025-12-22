import tkinter as tk
from tkinter import messagebox
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os
import pickle
import threading
import time
from src.signal_utils import read_wav, pre_emphasis, frame_signal, apply_window
from src.feature_extraction import compute_mfcc

# Constants
MODEL_DIR = "models"
TEMP_FILE = "temp_recording.wav"
SAMPLE_RATE = 22050 # Standard for the project files
DURATION = 1.0 # 1 second recording is usually enough for digits

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vietnamese Digit Recognition - Numpy Edition")
        self.root.geometry("600x400")
        
        self.models = {}
        self.load_models()
        
        self.is_recording = False
        
        self.create_widgets()
        
    def load_models(self):
        print("Loading models...")
        for i in range(10):
            model_path = os.path.join(MODEL_DIR, f"hmm_{i}.pkl")
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    self.models[i] = pickle.load(f)
        print(f"Loaded {len(self.models)} models.")

    def create_widgets(self):
        # Header
        lbl_title = tk.Label(self.root, text="Hệ Thống Nhận Diện Tiếng Nói (0-9)", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=10)
        
        # Bulbs Area
        frame_bulbs = tk.Frame(self.root)
        frame_bulbs.pack(pady=20)
        
        self.bulbs = []
        self.bulb_canvases = []
        
        # Create 2 rows of 5 bulbs
        for i in range(10):
            f = tk.Frame(frame_bulbs)
            f.grid(row=i//5, column=i%5, padx=10, pady=10)
            
            c = tk.Canvas(f, width=50, height=50, bg="white", highlightthickness=0)
            c.pack()
            # Draw gray circle initially
            c.create_oval(5, 5, 45, 45, fill="#DDDDDD", tags="bulb")
            
            l = tk.Label(f, text=str(i), font=("Arial", 12, "bold"))
            l.pack()
            
            self.bulb_canvases.append(c)
        
        # Controls
        self.btn_shutdown = tk.Frame(self.root) 
        self.btn_shutdown.pack(pady=20)
        
        self.btn_record = tk.Button(self.btn_shutdown, text="GHI ÂM (Giữ để nói)", bg="#ffcccc", font=("Arial", 14))
        self.btn_record.pack(side=tk.LEFT, padx=10)
        # Bind mouse press/release
        self.btn_record.bind('<ButtonPress-1>', self.start_record)
        self.btn_record.bind('<ButtonRelease-1>', self.stop_record)

        self.btn_reset = tk.Button(self.btn_shutdown, text="RESET", bg="#ccffcc", font=("Arial", 14), command=self.reset_app)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        self.lbl_status = tk.Label(self.root, text="Ready", fg="blue")
        self.lbl_status.pack()

    def reset_app(self):
        """Reset all bulbs to gray and status to Ready"""
        for canvas in self.bulb_canvases:
            canvas.itemconfig("bulb", fill="#DDDDDD")
        self.lbl_status.config(text="Ready", fg="blue")


    def start_record(self, event):
        self.is_recording = True
        self.lbl_status.config(text="Recording...", fg="red")
        self.record_thread = threading.Thread(target=self.record_audio)
        self.record_thread.start()

    def stop_record(self, event):
        self.is_recording = False
        self.lbl_status.config(text="Processing...", fg="orange")
        # Thread will finish naturally when is_recording flag check loop breaks or duration ends?
        # Using sounddevice.rec is non-blocking, but we need to stop it.
        # Actually simplest approach for "Hold" is fixed block, but let's do: 
        # Since sounddevice rec is fixed duration usually, let's just record fixed 1.5s for simplicity
        # User holds -> We trigger a 1.5s record. If they release early, proper hold logic is complex.
        pass

    def record_audio(self):
        # Record fixed 1.5 seconds
        try:
            duration = 1.5
            recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
            sd.wait()
            
            # Save
            # Scale to int16
            recording_int16 = (recording * 32767).astype(np.int16)
            wavfile.write(TEMP_FILE, SAMPLE_RATE, recording_int16)
            
            # Predict
            self.root.after(100, self.predict)
        except Exception as e:
            print(f"Error recording: {e}")
            self.root.after(0, lambda: self.lbl_status.config(text="Record Error", fg="red"))

    def predict(self):
        # 1. Pipeline
        try:
            sr, signal = read_wav(TEMP_FILE)
            if len(signal) == 0: 
                raise ValueError("Empty audio")
            
            # Normalize?
            
            signal = pre_emphasis(signal)
            frames = frame_signal(signal, sr)
            frames = apply_window(frames)
            mfcc = compute_mfcc(frames, sr)
            
            # 2. Score with HMMs
            best_score = -float('inf')
            best_digit = -1
            
            scores = {}
            for digit, model in self.models.items():
                try:
                    score = model.score(mfcc)
                    scores[digit] = score
                    if score > best_score:
                        best_score = score
                        best_digit = digit
                except:
                    scores[digit] = -float('inf')
            
            print("Scores:", scores)
            
            # 3. Update UI
            self.update_bulbs(best_digit)
            self.lbl_status.config(text=f"Detected: {best_digit}", fg="green")
            
        except Exception as e:
            print(f"Prediction Error: {e}")
            self.lbl_status.config(text="Error processing audio", fg="red")

    def update_bulbs(self, active_digit):
        for i, canvas in enumerate(self.bulb_canvases):
            color = "#DDDDDD" # Grey
            if i == active_digit:
                color = "#FFFF00" # Yellow ON
                # Add glow effect?
                
            canvas.itemconfig("bulb", fill=color)

if __name__ == "__main__":
    # Check sounddevice
    try:
        sd.query_devices()
    except:
        print("Warning: Sounddevice not working or no input found.")
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()
