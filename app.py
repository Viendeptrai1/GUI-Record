"""
Module chính của ứng dụng
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from audio_config import AudioConfig
from audio_recorder import AudioRecorder
from ui_components import (
    TitleLabel, StatusLabel, TimerLabel,
    RecordButton, SaveButton, InfoLabel
)
from settings_panel import SettingsPanel
from config import *


class AudioRecorderApp:
    """Ứng dụng ghi âm chính"""
    
    def __init__(self, root):
        self.root = root
        self.audio_config = AudioConfig()
        self.recorder = AudioRecorder(self.audio_config)
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Ứng Dụng Ghi Âm")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
    
    def _create_ui(self):
        """Tạo giao diện người dùng"""
        # Tiêu đề
        title = TitleLabel(self.root)
        title.pack(pady=15)
        
        # Panel cài đặt âm thanh
        self.settings_panel = SettingsPanel(
            self.root, 
            self.audio_config,
            self._on_config_change
        )
        self.settings_panel.pack(pady=10, padx=20, fill="x")
        
        # Frame chính
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Trạng thái
        self.status_label = StatusLabel(main_frame)
        self.status_label.pack(pady=10)
        
        # Thời gian
        self.timer_label = TimerLabel(main_frame)
        self.timer_label.pack(pady=15)
        
        # Frame nút điều khiển
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        # Nút ghi âm
        self.record_button = RecordButton(button_frame, self.toggle_recording)
        self.record_button.pack(pady=5)
        
        # Nút lưu
        self.save_button = SaveButton(button_frame, self.save_recording)
        self.save_button.pack(pady=5)
        
        # Thông tin
        self.info_label = InfoLabel(main_frame, self.audio_config)
        self.info_label.pack(side="bottom", pady=10)
    
    def toggle_recording(self):
        """Bật/tắt ghi âm"""
        if not self.recorder.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Bắt đầu ghi âm"""
        try:
            self.recorder.start_recording()
            self.record_button.set_recording_state(True)
            self.status_label.set_text("Đang ghi âm...", DANGER_COLOR)
            self.save_button.disable()
            self.settings_panel.disable()  # Khóa cài đặt khi ghi âm
            self._update_timer()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _stop_recording(self):
        """Dừng ghi âm"""
        self.recorder.stop_recording()
        self.record_button.set_recording_state(False)
        self.status_label.set_text("Đã dừng ghi âm", WARNING_COLOR)
        self.save_button.enable()
        self.settings_panel.enable()  # Mở lại cài đặt
    
    def _update_timer(self):
        """Cập nhật bộ đếm thời gian"""
        if self.recorder.is_recording:
            elapsed = self.recorder.get_elapsed_time()
            self.timer_label.update_time(elapsed)
            self.root.after(100, self._update_timer)
        else:
            if not self.recorder.has_data():
                self.timer_label.reset()
    
    def save_recording(self):
        """Lưu file ghi âm"""
        if not self.recorder.has_data():
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu âm thanh để lưu!")
            return
        
        # Chọn vị trí lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            initialfile=AudioRecorder.get_default_filename(),
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.recorder.save_to_file(file_path)
                messagebox.showinfo(
                    "Thành công", 
                    f"Đã lưu file thành công!\n{file_path}"
                )
                self._reset_ui()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def _reset_ui(self):
        """Reset giao diện về trạng thái ban đầu"""
        self.recorder.clear_data()
        self.timer_label.reset()
        self.status_label.set_text("Sẵn sàng ghi âm", PRIMARY_COLOR)
        self.save_button.disable()
    
    def _on_config_change(self):
        """Callback khi thay đổi cấu hình"""
        self.info_label.update_text()

