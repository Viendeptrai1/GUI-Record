"""
Module chính của ứng dụng
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from audio_config import AudioConfig
from audio_recorder import AudioRecorder
from audio_player import AudioPlayer
from ui_components import (
    TitleLabel, StatusLabel, TimerLabel,
    RecordButton, InfoLabel
)
from settings_panel import SettingsPanel
from recordings_panel import RecordingsPanel
from config import *


class AudioRecorderApp:
    """Ứng dụng ghi âm chính"""
    
    def __init__(self, root):
        self.root = root
        self.audio_config = AudioConfig()
        self.recorder = AudioRecorder(self.audio_config)
        self.player = AudioPlayer()
        self.recordings_folder = os.path.join(os.path.dirname(__file__), RECORDINGS_FOLDER)
        self._ensure_recordings_folder()
        self._setup_window()
        self._create_ui()
    
    def _ensure_recordings_folder(self):
        """Đảm bảo folder recordings tồn tại"""
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)
    
    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Ứng Dụng Ghi Âm Nâng Cao")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
    
    def _create_ui(self):
        """Tạo giao diện người dùng"""
        # Tiêu đề
        title = TitleLabel(self.root)
        title.pack(pady=15)
        
        # Frame container chính (2 cột)
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Cột trái - Ghi âm
        left_column = tk.Frame(container, bg=BG_COLOR)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Panel cài đặt âm thanh
        self.settings_panel = SettingsPanel(
            left_column, 
            self.audio_config,
            self._on_config_change
        )
        self.settings_panel.pack(pady=(0, 10), fill="x")
        
        # Frame điều khiển ghi âm
        record_frame = tk.Frame(left_column, bg=BG_COLOR)
        record_frame.pack(fill="both", expand=True)
        
        # Trạng thái
        self.status_label = StatusLabel(record_frame)
        self.status_label.pack(pady=10)
        
        # Thời gian
        self.timer_label = TimerLabel(record_frame)
        self.timer_label.pack(pady=15)
        
        # Frame nút điều khiển
        button_frame = tk.Frame(record_frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        # Nút ghi âm
        self.record_button = RecordButton(button_frame, self.toggle_recording)
        self.record_button.pack(pady=5)
        
        # Thông tin
        self.info_label = InfoLabel(record_frame, self.audio_config)
        self.info_label.pack(side="bottom", pady=10)
        
        # Cột phải - Danh sách bản ghi
        right_column = tk.Frame(container, bg=BG_COLOR)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Panel bản ghi
        self.recordings_panel = RecordingsPanel(
            right_column,
            self.recordings_folder,
            self._on_play_recording,
            self._on_stop_or_delete_recording
        )
        self.recordings_panel.pack(fill="both", expand=True)
    
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
            self.settings_panel.disable()  # Khóa cài đặt khi ghi âm
            self._update_timer()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _stop_recording(self):
        """Dừng ghi âm"""
        self.recorder.stop_recording()
        self.record_button.set_recording_state(False)
        self.status_label.set_text("Đã dừng ghi âm", WARNING_COLOR)
        self.settings_panel.enable()  # Mở lại cài đặt
        
        # Tự động lưu nếu có dữ liệu
        if self.recorder.has_data():
            self.save_recording()
    
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
        """Lưu file ghi âm tự động"""
        if not self.recorder.has_data():
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu âm thanh để lưu!")
            return
        
        try:
            # Tạo tên file tự động
            filename = AudioRecorder.get_default_filename()
            file_path = os.path.join(self.recordings_folder, filename)
            
            # Lưu file
            self.recorder.save_to_file(file_path)
            
            # Refresh danh sách
            self.recordings_panel.refresh()
            
            # Thông báo
            messagebox.showinfo(
                "Thành công", 
                f"Đã lưu bản ghi thành công!\n📁 {filename}"
            )
            
            self._reset_ui()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _reset_ui(self):
        """Reset giao diện về trạng thái ban đầu"""
        self.recorder.clear_data()
        self.timer_label.reset()
        self.status_label.set_text("Sẵn sàng ghi âm", PRIMARY_COLOR)
    
    def _on_config_change(self):
        """Callback khi thay đổi cấu hình"""
        self.info_label.update_text()
    
    def _on_play_recording(self, filepath):
        """Callback khi phát bản ghi"""
        try:
            # Dừng player hiện tại nếu đang chạy
            if self.player.is_playing:
                self.player.stop()
            
            # Load và phát file mới
            self.player.load_file(filepath)
            self.player.play()
            
            self.status_label.set_text("Đang phát bản ghi...", SUCCESS_COLOR)
            self.recordings_panel.enable_stop_button()
            
            # Monitor khi phát xong
            self._monitor_playback()
            
        except Exception as e:
            messagebox.showerror("Lỗi phát", str(e))
    
    def _on_stop_or_delete_recording(self, action="stop"):
        """Callback khi dừng phát"""
        try:
            self.player.stop()
            self.status_label.set_text("Sẵn sàng ghi âm", PRIMARY_COLOR)
            self.recordings_panel.disable_stop_button()
        except Exception as e:
            pass
    
    def _monitor_playback(self):
        """Theo dõi quá trình phát"""
        if self.player.is_playing:
            # Cập nhật thời gian phát
            position = self.player.get_position()
            duration = self.player.get_duration()
            
            mins = int(position // 60)
            secs = int(position % 60)
            
            self.root.after(100, self._monitor_playback)
        else:
            # Phát xong
            self.status_label.set_text("Sẵn sàng ghi âm", PRIMARY_COLOR)
            self.recordings_panel.disable_stop_button()

