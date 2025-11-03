"""
Ứng dụng ghi âm - Entry Point
"""
import tkinter as tk
from app import AudioRecorderApp


def main():
    """Hàm khởi động ứng dụng"""
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
