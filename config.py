"""
Cấu hình cho ứng dụng ghi âm
"""

# Cấu hình âm thanh mặc định
DEFAULT_SAMPLE_RATE = 44100  # Hz
DEFAULT_CHANNELS = 1  # Mono
DEFAULT_DTYPE = 'float32'
CHUNK_SIZE = 1024

# Các tùy chọn cấu hình âm thanh
SAMPLE_RATE_OPTIONS = {
    "16000 Hz - Chất lượng giọng nói": 16000,
    "22050 Hz - Chất lượng trung bình": 22050,
    "44100 Hz - Chất lượng CD (Khuyến nghị)": 44100,
    "48000 Hz - Chất lượng Studio": 48000,
}

CHANNELS_OPTIONS = {
    "Mono (1 kênh) - Giọng nói, tiết kiệm dung lượng": 1,
    "Stereo (2 kênh) - Âm nhạc, không gian": 2,
}

DTYPE_OPTIONS = {
    "16-bit - Tiêu chuẩn, tiết kiệm": 'int16',
    "32-bit Float - Chất lượng cao": 'float32',
}

# Cấu hình giao diện
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BG_COLOR = "#2C3E50"
TEXT_COLOR = "#ECF0F1"
PRIMARY_COLOR = "#3498DB"
SUCCESS_COLOR = "#27AE60"
DANGER_COLOR = "#E74C3C"
WARNING_COLOR = "#F39C12"
SECONDARY_COLOR = "#95A5A6"

# Font
FONT_FAMILY = "Helvetica"
TITLE_FONT_SIZE = 20
LABEL_FONT_SIZE = 14
BUTTON_FONT_SIZE = 12
TIMER_FONT_SIZE = 32
INFO_FONT_SIZE = 9

# Cấu hình lưu trữ
RECORDINGS_FOLDER = "recordings"
AUTO_SAVE = True

