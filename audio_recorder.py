"""
Module xử lý ghi âm
"""
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading
import time
from datetime import datetime
from config import CHUNK_SIZE


class AudioRecorder:
    """Class quản lý việc ghi âm"""
    
    def __init__(self, audio_config):
        self.config = audio_config
        self.is_recording = False
        self.audio_data = []
        self.recording_thread = None
        self.recording_start_time = 0
    
    def start_recording(self):
        """Bắt đầu ghi âm"""
        self.is_recording = True
        self.audio_data = []
        self.recording_start_time = time.time()
        
        # Khởi động thread ghi âm
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def stop_recording(self):
        """Dừng ghi âm"""
        self.is_recording = False
        
        # Đợi thread kết thúc
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
    
    def _record_audio(self):
        """Hàm ghi âm chạy trong thread riêng"""
        try:
            with sd.InputStream(
                samplerate=self.config.sample_rate, 
                channels=self.config.channels, 
                dtype=self.config.dtype
            ) as stream:
                while self.is_recording:
                    data, _ = stream.read(CHUNK_SIZE)
                    self.audio_data.append(data.copy())
        except Exception as e:
            raise Exception(f"Lỗi khi ghi âm: {str(e)}")
    
    def get_elapsed_time(self):
        """Lấy thời gian đã ghi"""
        if not self.is_recording:
            return 0
        return time.time() - self.recording_start_time
    
    def has_data(self):
        """Kiểm tra có dữ liệu âm thanh không"""
        return len(self.audio_data) > 0
    
    def save_to_file(self, file_path):
        """Lưu file âm thanh"""
        if not self.has_data():
            raise ValueError("Không có dữ liệu âm thanh để lưu")
        
        try:
            # Ghép các đoạn audio lại
            audio_array = np.concatenate(self.audio_data, axis=0)
            
            # Chuyển đổi dữ liệu dựa trên dtype
            if self.config.dtype == 'int16':
                audio_data = audio_array
            else:  # float32
                # Chuẩn hóa và chuyển sang int16
                audio_data = np.int16(audio_array * 32767)
            
            # Lưu file WAV
            write(file_path, self.config.sample_rate, audio_data)
        except Exception as e:
            raise Exception(f"Lỗi khi lưu file: {str(e)}")
    
    def clear_data(self):
        """Xóa dữ liệu âm thanh"""
        self.audio_data = []
    
    @staticmethod
    def get_default_filename():
        """Tạo tên file mặc định"""
        return f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

