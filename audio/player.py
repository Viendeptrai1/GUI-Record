import sounddevice as sd
import time
import threading

class AudioPlayer:
    def __init__(self):
        self.is_playing = False
        self.start_time = 0
        self.thread = None

    def play(self, data, fs):
        self.stop()
        self.is_playing = True
        self.start_time = time.time()
        
        def playback_thread():
            sd.play(data, fs)
            sd.wait()
            self.is_playing = False
            
        self.thread = threading.Thread(target=playback_thread)
        self.thread.start()

    def stop(self):
        if self.is_playing:
            sd.stop()
            self.is_playing = False
            if self.thread:
                self.thread.join()
                
    def get_current_time(self):
        if self.is_playing:
            return time.time() - self.start_time
        return 0
