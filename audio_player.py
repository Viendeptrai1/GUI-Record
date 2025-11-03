"""
Module phát âm thanh
"""
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
import threading


class AudioPlayer:
    """Class quản lý việc phát âm thanh"""
    
    def __init__(self):
        self.is_playing = False
        self.play_thread = None
        self.audio_data = None
        self.sample_rate = None
        self.current_position = 0
        self.stop_flag = False
    
    def load_file(self, file_path):
        """Load file âm thanh"""
        try:
            self.sample_rate, self.audio_data = read(file_path)
            self.current_position = 0
            return True
        except Exception as e:
            raise Exception(f"Không thể load file: {str(e)}")
    
    def play(self):
        """Phát âm thanh"""
        if self.audio_data is None:
            raise ValueError("Chưa load file âm thanh")
        
        if self.is_playing:
            return
        
        self.is_playing = True
        self.stop_flag = False
        self.play_thread = threading.Thread(target=self._play_audio)
        self.play_thread.daemon = True
        self.play_thread.start()
    
    def stop(self):
        """Dừng phát"""
        self.stop_flag = True
        self.is_playing = False
        self.current_position = 0
        
        if self.play_thread:
            self.play_thread.join(timeout=1)
    
    def pause(self):
        """Tạm dừng"""
        self.is_playing = False
        self.stop_flag = True
    
    def _play_audio(self):
        """Hàm phát âm thanh trong thread riêng"""
        try:
            # Chuyển đổi sang float32 nếu cần
            if self.audio_data.dtype == np.int16:
                audio_float = self.audio_data.astype(np.float32) / 32767.0
            else:
                audio_float = self.audio_data
            
            # Phát từ vị trí hiện tại
            with sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1 if len(audio_float.shape) == 1 else audio_float.shape[1],
                dtype='float32'
            ) as stream:
                chunk_size = 1024
                start = self.current_position
                
                while start < len(audio_float) and not self.stop_flag:
                    end = min(start + chunk_size, len(audio_float))
                    chunk = audio_float[start:end]
                    
                    # Đảm bảo chunk có đúng shape
                    if len(chunk.shape) == 1:
                        chunk = chunk.reshape(-1, 1)
                    
                    stream.write(chunk)
                    start = end
                    self.current_position = start
                
                # Phát xong
                if not self.stop_flag:
                    self.current_position = 0
                
                self.is_playing = False
                
        except Exception as e:
            self.is_playing = False
            raise Exception(f"Lỗi khi phát âm thanh: {str(e)}")
    
    def get_duration(self):
        """Lấy thời lượng file (giây)"""
        if self.audio_data is None:
            return 0
        return len(self.audio_data) / self.sample_rate
    
    def get_position(self):
        """Lấy vị trí hiện tại (giây)"""
        if self.audio_data is None:
            return 0
        return self.current_position / self.sample_rate

