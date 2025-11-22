import sounddevice as sd
import numpy as np
import threading

class AudioRecorder:
    def __init__(self, fs=16000, channels=1):
        self.fs = fs
        self.channels = channels
        self.recording = False
        self.frames = []
        self.stream = None
        self.thread = None

    def start_recording(self):
        if self.recording:
            return
        
        self.recording = True
        self.frames = []
        
        # Start a new thread for recording to avoid blocking the GUI
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        """Internal method to run in a separate thread."""
        with sd.InputStream(samplerate=self.fs, channels=self.channels, callback=self._callback):
            while self.recording:
                sd.sleep(100)

    def _callback(self, indata, frames, time, status):
        """Callback function for sounddevice InputStream."""
        if status:
            print(status, flush=True)
        if self.recording:
            self.frames.append(indata.copy())

    def stop_recording(self):
        self.recording = False
        if self.thread:
            self.thread.join()
        
        if not self.frames:
            return np.array([])
            
        return np.concatenate(self.frames, axis=0)

    def get_data(self):
        if not self.frames:
            return np.array([])
        return np.concatenate(self.frames, axis=0)
