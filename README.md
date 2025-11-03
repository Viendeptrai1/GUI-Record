# Ứng Dụng Ghi Âm

Ứng dụng GUI đơn giản để ghi âm bằng Python với giao diện thân thiện.

## Tính năng

- 🎙️ Ghi âm chất lượng cao (44100 Hz, stereo)
- ⏱️ Hiển thị thời gian ghi âm real-time
- 💾 Lưu file âm thanh định dạng WAV
- 🎨 Giao diện đẹp mắt, dễ sử dụng
- 🔴 Nút bắt đầu/dừng ghi âm trực quan

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```bash
python main.py
```

## Hướng dẫn sử dụng

1. **Bắt đầu ghi âm**: Nhấn nút "🔴 BẮT ĐẦU GHI ÂM"
2. **Dừng ghi âm**: Nhấn nút "⏹️ DỪNG GHI ÂM" khi hoàn tất
3. **Lưu file**: Nhấn nút "💾 LƯU FILE" và chọn vị trí lưu

## Yêu cầu hệ thống

- Python 3.7+
- Microphone
- Hệ điều hành: Windows, macOS, Linux

## Thư viện sử dụng

- **tkinter**: Giao diện người dùng
- **sounddevice**: Ghi âm
- **numpy**: Xử lý dữ liệu âm thanh
- **scipy**: Lưu file WAV

## Lưu ý

- File âm thanh được lưu với định dạng WAV, chất lượng cao
- Tên file mặc định: `recording_YYYYMMDD_HHMMSS.wav`
- Đảm bảo microphone đã được kết nối và cấp quyền truy cập

