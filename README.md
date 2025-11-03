# 🎙️ Ứng Dụng Ghi Âm Nâng Cao

Ứng dụng ghi âm chuyên nghiệp với giao diện đồ họa, hỗ trợ tùy chỉnh cấu hình, quản lý và phát lại bản ghi.

## ✨ Tính năng

- ✅ Ghi âm với giao diện đẹp mắt, dễ sử dụng
- ✅ Tùy chỉnh cấu hình âm thanh trực tiếp trên giao diện
- ✅ Hiển thị thời gian ghi âm real-time
- ✅ **Tự động lưu** file vào folder `recordings/`
- ✅ **Quản lý bản ghi**: Xem danh sách các bản ghi gần đây
- ✅ **Phát lại trực tiếp**: Nghe lại bản ghi ngay trên ứng dụng
- ✅ **Xóa bản ghi**: Quản lý không gian lưu trữ
- ✅ Ước tính dung lượng file trước khi ghi

## 🎛️ Cấu hình âm thanh

### 1. Tần số mẫu (Sample Rate)

| Tùy chọn | Khi nào dùng | Chất lượng | Dung lượng |
|----------|--------------|------------|------------|
| **16000 Hz** | Ghi âm giọng nói, podcast, ghi chú | Đủ dùng | Nhỏ nhất |
| **22050 Hz** | Giọng nói chất lượng cao | Tốt | Trung bình |
| **44100 Hz** | Âm nhạc, chất lượng CD (Khuyến nghị) | Rất tốt | Lớn |
| **48000 Hz** | Studio, sản xuất chuyên nghiệp | Xuất sắc | Lớn nhất |

💡 **Gợi ý**: 
- Ghi giọng nói → 16000-22050 Hz
- Ghi âm nhạc → 44100-48000 Hz

### 2. Số kênh (Channels)

| Tùy chọn | Khi nào dùng | Dung lượng |
|----------|--------------|------------|
| **Mono (1 kênh)** | Giọng nói, podcast, ghi chú thoại | 50% so với Stereo |
| **Stereo (2 kênh)** | Âm nhạc, cần âm thanh không gian | 100% (gấp đôi Mono) |

💡 **Gợi ý**:
- Ghi giọng nói → Mono (tiết kiệm, đủ dùng)
- Ghi nhạc, môi trường → Stereo (có độ sâu)

### 3. Độ sâu bit (Bit Depth)

| Tùy chọn | Khi nào dùng | Chất lượng | Dung lượng |
|----------|--------------|------------|------------|
| **16-bit** | Tiêu chuẩn, phù hợp hầu hết trường hợp | Chuẩn CD | Nhỏ hơn |
| **32-bit Float** | Chỉnh sửa, xử lý âm thanh chuyên nghiệp | Cao nhất | Gấp đôi 16-bit |

💡 **Gợi ý**:
- Sử dụng thông thường → 16-bit
- Cần chỉnh sửa, xử lý sau → 32-bit Float

## 📊 Ước tính dung lượng

Dung lượng file tùy thuộc vào cấu hình:

| Cấu hình | Dung lượng/phút |
|----------|-----------------|
| 16000 Hz, Mono, 16-bit | ~1.8 MB |
| 22050 Hz, Mono, 16-bit | ~2.5 MB |
| 44100 Hz, Mono, 16-bit | ~5.0 MB |
| 44100 Hz, Stereo, 16-bit | ~10.0 MB |
| 48000 Hz, Stereo, 32-bit | ~22.0 MB |

💡 Ứng dụng sẽ hiển thị ước tính dung lượng khi bạn thay đổi cấu hình!

## 🚀 Cài đặt

```bash
# Clone hoặc tải project
cd xu-ly-tieng-noi

# Tạo virtual environment
python3 -m venv .venv

# Kích hoạt virtual environment
source .venv/bin/activate  # macOS/Linux
# hoặc
.venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python3 main.py
```

## 📁 Cấu trúc project

```
xu-ly-tieng-noi/
├── main.py              # Entry point - Khởi động ứng dụng
├── app.py               # Class ứng dụng chính
├── audio_recorder.py    # Logic ghi âm
├── audio_player.py      # Logic phát âm thanh
├── audio_config.py      # Quản lý cấu hình âm thanh
├── ui_components.py     # Các UI components
├── settings_panel.py    # Panel cài đặt âm thanh
├── recordings_panel.py  # Panel quản lý bản ghi
├── config.py            # Cấu hình constants
├── requirements.txt     # Python dependencies
├── recordings/          # Folder chứa bản ghi (tự động tạo)
└── README.md           # Tài liệu này
```

## 🎯 Hướng dẫn sử dụng

### Ghi âm

1. **Khởi động ứng dụng**: Chạy `python3 main.py`

2. **Chọn cấu hình** (bên trái, trước khi ghi):
   - Chọn tần số mẫu phù hợp (16kHz - 48kHz)
   - Chọn Mono/Stereo
   - Chọn độ sâu bit (16-bit/32-bit)
   - Xem ước tính dung lượng

3. **Bắt đầu ghi âm**: 
   - Bấm nút "🔴 BẮT ĐẦU GHI ÂM"
   - Các cài đặt sẽ bị khóa khi đang ghi
   - Thời gian ghi âm hiển thị real-time

4. **Dừng và Lưu**: 
   - Bấm nút "⏹️ DỪNG GHI ÂM"
   - File sẽ **tự động lưu** vào folder `recordings/`
   - Tên file: `recording_YYYYMMDD_HHMMSS.wav`

### Quản lý và phát lại

5. **Xem bản ghi** (bên phải):
   - Danh sách tự động cập nhật sau mỗi lần ghi
   - Hiển thị ngày giờ ghi âm

6. **Phát lại bản ghi**:
   - **Cách 1**: Double-click vào bản ghi
   - **Cách 2**: Chọn bản ghi → Bấm nút "▶️ Phát"
   - Trạng thái hiển thị "Đang phát bản ghi..."

7. **Dừng phát**:
   - Bấm nút "⏹️ Dừng" (trong panel bản ghi)

8. **Xóa bản ghi**:
   - Chọn bản ghi cần xóa
   - Bấm nút "🗑️ Xóa"
   - Xác nhận xóa

## 💻 Yêu cầu hệ thống

- Python 3.9+
- macOS 11+ (hoặc Windows/Linux với Python tương thích)
- Microphone được kết nối

## 🔧 Dependencies

- `sounddevice` - Ghi âm
- `numpy` - Xử lý dữ liệu âm thanh
- `scipy` - Lưu file WAV
- `tkinter` - Giao diện (built-in với Python)

## 🎨 Giao diện

```
┌───────────────────────────────────────────────────────────────┐
│              🎙️ ỨNG DỤNG GHI ÂM NÂNG CAO                      │
├─────────────────────────────┬─────────────────────────────────┤
│  ⚙️ CÀI ĐẶT ÂM THANH       │  📼 BẢN GHI ÂM GẦN ĐÂY          │
│  Tần số mẫu: [44100 Hz ▼]  │  ┌─────────────────────────────┐│
│  Số kênh: [Mono ▼]          │  │ 📌 03/11/2025 14:05:30     ││
│  Bit depth: [32-bit ▼]      │  │ 📌 03/11/2025 13:45:12     ││
│  📊 ~10.0 MB/phút            │  │ 📌 03/11/2025 12:30:45     ││
│                              │  │ 📌 02/11/2025 18:20:00     ││
│  Sẵn sàng ghi âm             │  └─────────────────────────────┘│
│                              │                                 │
│      00:00:00                │  [▶️ Phát] [⏹️ Dừng] [🗑️ Xóa]  │
│                              │                                 │
│  [🔴 BẮT ĐẦU GHI ÂM]        │  Tổng: 4 bản ghi                │
│                              │                                 │
│  WAV | 44100 Hz | Mono...   │                                 │
└─────────────────────────────┴─────────────────────────────────┘
```

## 🐛 Xử lý lỗi thường gặp

### "Invalid number of channels"
- **Nguyên nhân**: Microphone không hỗ trợ Stereo
- **Giải pháp**: Chọn "Mono (1 kênh)" trong cài đặt

### "OSStatus -26276" hoặc lỗi SSL
- **Nguyên nhân**: Python cũ hoặc thiếu certificates
- **Giải pháp**: Nâng cấp Python lên 3.10+ (khuyến nghị 3.13)

### Ứng dụng không khởi động
- Kiểm tra quyền microphone: System Settings → Privacy → Microphone
- Đảm bảo đã kích hoạt virtual environment
- Chạy: `python3 main.py` trong folder project

### Không phát được âm thanh
- Kiểm tra quyền speaker/audio output
- Đảm bảo file WAV tồn tại trong folder `recordings/`
- Thử với file ghi âm mới

### Folder recordings không tự động tạo
- Chạy lại ứng dụng, folder sẽ tự động được tạo
- Hoặc tạo thủ công: `mkdir recordings`

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa!

---

Made with ❤️ using Python & Tkinter
