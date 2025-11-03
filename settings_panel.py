"""
Module panel cài đặt âm thanh
"""
import tkinter as tk
from tkinter import ttk
from config import (
    BG_COLOR, TEXT_COLOR, PRIMARY_COLOR, FONT_FAMILY,
    SAMPLE_RATE_OPTIONS, CHANNELS_OPTIONS, DTYPE_OPTIONS
)


class SettingsPanel:
    """Panel cài đặt cấu hình âm thanh"""
    
    def __init__(self, parent, audio_config, on_config_change):
        self.audio_config = audio_config
        self.on_config_change = on_config_change
        self.frame = None
        self._create_panel(parent)
    
    def _create_panel(self, parent):
        """Tạo panel cài đặt"""
        # Frame chính với border
        self.frame = tk.LabelFrame(
            parent,
            text="⚙️ CÀI ĐẶT ÂM THANH",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            relief="groove",
            borderwidth=2
        )
        
        # Tần số mẫu
        self._create_setting_row(
            "Tần số mẫu (Sample Rate):",
            SAMPLE_RATE_OPTIONS,
            self.audio_config.sample_rate,
            self._on_sample_rate_change
        )
        
        # Số kênh
        self._create_setting_row(
            "Số kênh (Channels):",
            CHANNELS_OPTIONS,
            self.audio_config.channels,
            self._on_channels_change
        )
        
        # Bit depth
        self._create_setting_row(
            "Độ sâu bit (Bit Depth):",
            DTYPE_OPTIONS,
            self.audio_config.dtype,
            self._on_dtype_change
        )
        
        # Thông tin ước tính
        self.info_label = tk.Label(
            self.frame,
            text="",
            font=(FONT_FAMILY, 9, "italic"),
            bg=BG_COLOR,
            fg="#95A5A6",
            justify="left"
        )
        self.info_label.pack(pady=(5, 0), padx=10, anchor="w")
        self._update_info_label()
    
    def _create_setting_row(self, label_text, options, current_value, callback):
        """Tạo một hàng cài đặt với dropdown"""
        row_frame = tk.Frame(self.frame, bg=BG_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        
        # Label
        label = tk.Label(
            row_frame,
            text=label_text,
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        )
        label.pack(anchor="w")
        
        # Combobox
        selected_key = self._find_key_by_value(options, current_value)
        combo_var = tk.StringVar(value=selected_key)
        
        combo = ttk.Combobox(
            row_frame,
            textvariable=combo_var,
            values=list(options.keys()),
            state="readonly",
            width=45,
            font=(FONT_FAMILY, 9)
        )
        combo.pack(pady=(2, 0))
        combo.bind("<<ComboboxSelected>>", lambda e: callback(options[combo_var.get()]))
        
        return combo
    
    def _find_key_by_value(self, options_dict, value):
        """Tìm key từ value trong dictionary"""
        for key, val in options_dict.items():
            if val == value:
                return key
        return list(options_dict.keys())[0]
    
    def _on_sample_rate_change(self, value):
        """Callback khi thay đổi sample rate"""
        self.audio_config.update(sample_rate=value)
        self._update_info_label()
        self.on_config_change()
    
    def _on_channels_change(self, value):
        """Callback khi thay đổi channels"""
        self.audio_config.update(channels=value)
        self._update_info_label()
        self.on_config_change()
    
    def _on_dtype_change(self, value):
        """Callback khi thay đổi dtype"""
        self.audio_config.update(dtype=value)
        self._update_info_label()
        self.on_config_change()
    
    def _update_info_label(self):
        """Cập nhật label thông tin ước tính"""
        size_mb = self.audio_config.estimate_file_size_per_minute()
        info_text = f"📊 Ước tính: ~{size_mb:.1f} MB/phút"
        self.info_label.config(text=info_text)
    
    def pack(self, **kwargs):
        """Pack frame"""
        self.frame.pack(**kwargs)
    
    def disable(self):
        """Vô hiệu hóa tất cả controls (khi đang ghi âm)"""
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Combobox):
                        subchild.config(state="disabled")
    
    def enable(self):
        """Kích hoạt lại controls"""
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Combobox):
                        subchild.config(state="readonly")

