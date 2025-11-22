import sounddevice as sd

class AudioPlayer:
    def play(self, data, fs):
        """
        Play audio data.
        
        Args:
            data (numpy.ndarray): Audio data.
            fs (int): Sampling rate.
        """
        sd.play(data, fs)
        # We don't wait for playback to finish here to keep UI responsive, 
        # but we could add a wait method if needed.

    def stop(self):
        sd.stop()
