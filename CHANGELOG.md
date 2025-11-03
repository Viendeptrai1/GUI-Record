# Changelog

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại ở đây.

## [2.0.0] - 2025-11-03

### 🚀 Tính năng mới (Major Update)

- **Giao diện 2 cột**: Tách biệt rõ ràng giữa ghi âm và quản lý bản ghi
- **Tự động lưu**: File tự động lưu vào folder `recordings/` khi dừng ghi âm
- **Quản lý bản ghi**: 
  - Hiển thị danh sách bản ghi gần đây
  - Format thời gian dễ đọc (DD/MM/YYYY HH:MM:SS)
  - Tự động cập nhật sau mỗi lần ghi
- **Phát lại trực tiếp**:
  - Double-click hoặc nút "Phát" để nghe lại
  - Hiển thị trạng thái đang phát
  - Nút dừng phát riêng biệt
- **Xóa bản ghi**: Xóa file với xác nhận
- **Audio Player mới**: Module `audio_player.py` để phát WAV files
- **Recordings Panel**: Component quản lý danh sách bản ghi

### ✨ Cải tiến

- Tăng kích thước cửa sổ lên 900x700 để chứa 2 panels
- Loại bỏ nút "Lưu file" (tự động lưu)
- Thêm `.gitignore` để bỏ qua folder recordings và __pycache__
- Cập nhật README với hướng dẫn chi tiết
- Cấu trúc code module hóa tốt hơn

### 🐛 Sửa lỗi

- Sửa lỗi closure trong lambda callback
- Xử lý cả int16 và float32 khi phát audio

## [1.0.0] - 2025-11-03

### ✨ Tính năng ban đầu

- Ghi âm cơ bản với giao diện tkinter
- Cấu hình âm thanh trực tiếp trên UI:
  - Tần số mẫu: 16kHz - 48kHz
  - Số kênh: Mono/Stereo
  - Độ sâu bit: 16-bit/32-bit Float
- Hiển thị thời gian ghi âm real-time
- Ước tính dung lượng file
- Lưu file WAV với dialog chọn vị trí
- Module hóa code:
  - `config.py` - Cấu hình
  - `audio_config.py` - Quản lý config động
  - `audio_recorder.py` - Logic ghi âm
  - `ui_components.py` - UI components
  - `settings_panel.py` - Panel cài đặt
  - `app.py` - Ứng dụng chính
  - `main.py` - Entry point

### 🔧 Kỹ thuật

- Python 3.13 compatible
- Virtual environment support
- Tương thích với macOS Sequoia 15.x
- Threading cho ghi âm không blocking UI

