import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Tkinter 窗口初始化
        self.window = tk.Tk()
        self.window.title("Music Player")
        self.window.geometry("350x200")
        self.window.resizable(False, False)

        win_style = ttk.Style()

        # 当前播放状态和音频文件
        self.current_file = None
        self.paused = False

        # 播放按钮
        self.play_button = ttk.Button(
            self.window, text="Play", command=self.play_music)
        self.play_button.grid(row=5, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)

        # 音量滑块
        ttk.Label(self.window, text="Volume",
                  anchor="center").grid(row=6, column=1, columnspan=2)
        self.volume_slider = ttk.Scale(self.window, from_=0, to=1, orient="horizontal", command=self.set_volume,
                                       cursor="hand2", value=0.5)
        self.volume_slider.grid(row=6, column=3, columnspan=2, ipadx=12, ipady=2)

        # 加载音乐按钮
        self.load_button = ttk.Button(self.window, text="Load Music", command=self.load_music)
        self.load_button.grid(row=7, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)

        # Skip Forward and Skip Back buttons
        self.skip_forward_button = ttk.Button(self.window, text="⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=5, column=5, columnspan=2, pady=10, ipadx=12, ipady=2)

        self.skip_back_button = ttk.Button(self.window, text="⏪", command=self.skip_back)
        self.skip_back_button.grid(row=5, column=1, columnspan=2, pady=10, ipadx=12, ipady=2)

        # 显示时间标签
        self.time_label = ttk.Label(self.window, text="00:00 / 00:00", font=("Helvetica", 12))
        self.time_label.grid(row=0, column=3, columnspan=2, pady=5)

        # 进度条
        self.progress = ttk.Scale(self.window, from_=0, to=500, orient="horizontal", command=self.update_progress, cursor="hand2")
        self.progress.grid(row=2, column=3, columnspan=2, padx=20, pady=10, sticky="ew")

    def load_music(self):
        self.current_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3;*.wav")])
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
        return self.current_file

    def play_music(self):
        if self.current_file:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
                self.update_progress_bar()

            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.update_progress_bar()

            elif pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.paused = True

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def skip_forward(self):
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(start=int(current_pos) + 10)

    def skip_back(self):
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            new_pos = max(0, int(current_pos) - 10)
            pygame.mixer.music.play(start=new_pos)

    def update_progress_bar(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.progress.set(current_time)

            self.update_time_label(current_time)

            self.window.after(1000, self.update_progress_bar)

    def update_time_label(self, current_time):
        song_length = pygame.mixer.Sound(self.current_file).get_length()
        elapsed_minutes, elapsed_seconds = divmod(int(current_time), 60)
        total_minutes, total_seconds = divmod(int(song_length), 60)

        self.time_label.config(
            text=f"{elapsed_minutes:02}:{elapsed_seconds:02} / {total_minutes:02}:{total_seconds:02}")

    def update_progress(self, value):
        if self.current_file and pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(value))
            self.update_time_label(float(value))

MusicPlayer().window.mainloop()
