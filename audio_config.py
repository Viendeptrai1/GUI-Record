"""
Module quản lý cấu hình âm thanh
"""
from config import DEFAULT_SAMPLE_RATE, DEFAULT_CHANNELS, DEFAULT_DTYPE


class AudioConfig:
    """Class lưu trữ cấu hình âm thanh"""
    
    def __init__(self):
        self.sample_rate = DEFAULT_SAMPLE_RATE
        self.channels = DEFAULT_CHANNELS
        self.dtype = DEFAULT_DTYPE
    
    def update(self, sample_rate=None, channels=None, dtype=None):
        """Cập nhật cấu hình"""
        if sample_rate is not None:
            self.sample_rate = sample_rate
        if channels is not None:
            self.channels = channels
        if dtype is not None:
            self.dtype = dtype
    
    def get_info_text(self):
        """Lấy text thông tin cấu hình hiện tại"""
        channel_text = "Mono" if self.channels == 1 else "Stereo"
        dtype_text = "16-bit" if self.dtype == 'int16' else "32-bit Float"
        return f"Tần số: {self.sample_rate} Hz | {channel_text} | {dtype_text}"
    
    def estimate_file_size_per_minute(self):
        """Ước tính dung lượng file mỗi phút (MB)"""
        # Tính bytes per second
        bytes_per_sample = 2 if self.dtype == 'int16' else 4
        bytes_per_second = self.sample_rate * self.channels * bytes_per_sample
        
        # Tính MB per minute
        mb_per_minute = (bytes_per_second * 60) / (1024 * 1024)
        return mb_per_minute

