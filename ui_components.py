"""
Module chứa các components UI
"""
import tkinter as tk
from config import *


class TitleLabel:
    """Nhãn tiêu đề"""
    
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="🎙️ ỨNG DỤNG GHI ÂM",
            font=(FONT_FAMILY, TITLE_FONT_SIZE, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
    
    def pack(self, **kwargs):
        self.label.pack(**kwargs)


class StatusLabel:
    """Nhãn trạng thái"""
    
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="Sẵn sàng ghi âm",
            font=(FONT_FAMILY, LABEL_FONT_SIZE),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        )
    
    def pack(self, **kwargs):
        self.label.pack(**kwargs)
    
    def set_text(self, text, color=PRIMARY_COLOR):
        """Cập nhật text và màu"""
        self.label.config(text=text, fg=color)


class TimerLabel:
    """Nhãn hiển thị thời gian"""
    
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="00:00:00",
            font=("Courier", TIMER_FONT_SIZE, "bold"),
            bg=BG_COLOR,
            fg=DANGER_COLOR
        )
    
    def pack(self, **kwargs):
        self.label.pack(**kwargs)
    
    def update_time(self, elapsed_seconds):
        """Cập nhật thời gian hiển thị"""
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.label.config(text=time_str)
    
    def reset(self):
        """Reset về 00:00:00"""
        self.label.config(text="00:00:00")


class RecordButton:
    """Nút bắt đầu/dừng ghi âm"""
    
    def __init__(self, parent, command):
        self.button = tk.Button(
            parent,
            text="🔴 BẮT ĐẦU GHI ÂM",
            font=(FONT_FAMILY, BUTTON_FONT_SIZE, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            width=20,
            height=2,
            relief="raised",
            cursor="hand2",
            command=command
        )
        self.is_recording = False
    
    def pack(self, **kwargs):
        self.button.pack(**kwargs)
    
    def set_recording_state(self, is_recording):
        """Thay đổi trạng thái nút"""
        self.is_recording = is_recording
        if is_recording:
            self.button.config(
                text="⏹️ DỪNG GHI ÂM",
                bg=DANGER_COLOR
            )
        else:
            self.button.config(
                text="🔴 BẮT ĐẦU GHI ÂM",
                bg=SUCCESS_COLOR
            )




class InfoLabel:
    """Nhãn thông tin"""
    
    def __init__(self, parent, audio_config):
        self.audio_config = audio_config
        self.label = tk.Label(
            parent,
            text="",
            font=(FONT_FAMILY, INFO_FONT_SIZE),
            bg=BG_COLOR,
            fg=SECONDARY_COLOR
        )
        self.update_text()
    
    def pack(self, **kwargs):
        self.label.pack(**kwargs)
    
    def update_text(self):
        """Cập nhật text dựa trên config"""
        text = f"Định dạng: WAV | {self.audio_config.get_info_text()}"
        self.label.config(text=text)

