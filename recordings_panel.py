"""
Module panel quản lý bản ghi âm
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from config import BG_COLOR, TEXT_COLOR, FONT_FAMILY, SUCCESS_COLOR, DANGER_COLOR


class RecordingsPanel:
    """Panel quản lý danh sách bản ghi"""
    
    def __init__(self, parent, recordings_folder, on_play_callback, on_delete_callback):
        self.recordings_folder = recordings_folder
        self.on_play = on_play_callback
        self.on_delete = on_delete_callback
        self.frame = None
        self.listbox = None
        self.recordings = []
        self._create_panel(parent)
        self.refresh()
    
    def _create_panel(self, parent):
        """Tạo panel"""
        # Frame chính với border
        self.frame = tk.LabelFrame(
            parent,
            text="📼 BẢN GHI ÂM GẦN ĐÂY",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            relief="groove",
            borderwidth=2
        )
        
        # Frame chứa listbox và scrollbar
        list_frame = tk.Frame(self.frame, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=(FONT_FAMILY, 10),
            bg="#34495E",
            fg=TEXT_COLOR,
            selectbackground=SUCCESS_COLOR,
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind double click để phát
        self.listbox.bind("<Double-Button-1>", lambda e: self._on_double_click())
        
        # Frame nút điều khiển
        button_frame = tk.Frame(self.frame, bg=BG_COLOR)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Nút phát
        self.play_button = tk.Button(
            button_frame,
            text="▶️ Phát",
            font=(FONT_FAMILY, 10, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            width=10,
            cursor="hand2",
            command=self._on_play_click
        )
        self.play_button.pack(side="left", padx=5)
        
        # Nút dừng
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Dừng",
            font=(FONT_FAMILY, 10, "bold"),
            bg="#95A5A6",
            fg="white",
            width=10,
            cursor="hand2",
            command=self._on_stop_click,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Nút xóa
        self.delete_button = tk.Button(
            button_frame,
            text="🗑️ Xóa",
            font=(FONT_FAMILY, 10, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            width=10,
            cursor="hand2",
            command=self._on_delete_click
        )
        self.delete_button.pack(side="left", padx=5)
        
        # Label thông tin
        self.info_label = tk.Label(
            self.frame,
            text="Chưa có bản ghi nào",
            font=(FONT_FAMILY, 9, "italic"),
            bg=BG_COLOR,
            fg="#95A5A6"
        )
        self.info_label.pack(pady=(0, 10))
    
    def refresh(self):
        """Làm mới danh sách"""
        # Xóa danh sách cũ
        self.listbox.delete(0, tk.END)
        self.recordings = []
        
        # Kiểm tra folder tồn tại
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)
            self.info_label.config(text="Chưa có bản ghi nào")
            return
        
        # Lấy danh sách file WAV
        files = [f for f in os.listdir(self.recordings_folder) if f.endswith('.wav')]
        
        # Sắp xếp theo thời gian (mới nhất trước)
        files.sort(reverse=True)
        
        if not files:
            self.info_label.config(text="Chưa có bản ghi nào")
            return
        
        # Thêm vào listbox
        for filename in files:
            self.recordings.append(filename)
            
            # Parse tên file để hiển thị đẹp hơn
            display_name = self._format_filename(filename)
            self.listbox.insert(tk.END, display_name)
        
        # Cập nhật info
        self.info_label.config(text=f"Tổng: {len(files)} bản ghi")
    
    def _format_filename(self, filename):
        """Format tên file để hiển thị"""
        # Ví dụ: recording_20251103_140530.wav
        # -> 03/11/2025 14:05:30
        try:
            # Bỏ extension
            name = filename.replace('.wav', '')
            
            # Tách phần timestamp
            if 'recording_' in name:
                timestamp_part = name.split('recording_')[1]
                
                # Parse date và time
                date_part = timestamp_part[:8]  # 20251103
                time_part = timestamp_part[9:]  # 140530
                
                year = date_part[:4]
                month = date_part[4:6]
                day = date_part[6:8]
                
                hour = time_part[:2]
                minute = time_part[2:4]
                second = time_part[4:6]
                
                return f"📌 {day}/{month}/{year} {hour}:{minute}:{second}"
            
            return f"📌 {name}"
        except:
            return f"📌 {filename}"
    
    def _on_double_click(self):
        """Xử lý double click"""
        self._on_play_click()
    
    def _on_play_click(self):
        """Xử lý click nút phát"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi!")
            return
        
        index = selection[0]
        filename = self.recordings[index]
        filepath = os.path.join(self.recordings_folder, filename)
        
        try:
            self.on_play(filepath)
            self.stop_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _on_stop_click(self):
        """Xử lý click nút dừng"""
        try:
            self.on_delete(action="stop")
            self.stop_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _on_delete_click(self):
        """Xử lý click nút xóa"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để xóa!")
            return
        
        index = selection[0]
        filename = self.recordings[index]
        
        # Xác nhận xóa
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa bản ghi này?\n\n{self._format_filename(filename)}"
        )
        
        if confirm:
            filepath = os.path.join(self.recordings_folder, filename)
            try:
                os.remove(filepath)
                self.refresh()
                messagebox.showinfo("Thành công", "Đã xóa bản ghi!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa file: {str(e)}")
    
    def pack(self, **kwargs):
        """Pack frame"""
        self.frame.pack(**kwargs)
    
    def enable_stop_button(self):
        """Bật nút dừng"""
        self.stop_button.config(state="normal")
    
    def disable_stop_button(self):
        """Tắt nút dừng"""
        self.stop_button.config(state="disabled")

