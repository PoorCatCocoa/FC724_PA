from logging import setLogRecordFactory
from operator import length_hint

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
        self.window.geometry("200x400")

        win_style = ttk.Style()

        # 当前播放状态和音频文件
        self.current_file = None
        self.paused = False

        # 播放按钮
        self.play_button = ttk.Button(
            self.window, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, columnspan=2, pady=10, ipadx=12, ipady=2)

        # 音量滑块
        ttk.Label(self.window, text="Volume",
                  anchor="center").grid(row=1, column=0, columnspan=2)
        self.volume_slider = ttk.Scale(self.window, from_=0, to=1, orient="horizontal", command=self.set_volume,
                                       cursor="hand2", value=0.5)
        self.volume_slider.grid(row=2, column=0, columnspan=2, ipadx=12, ipady=2)

        # 加载音乐按钮
        self.load_button = ttk.Button(self.window, text="Load Music", command=self.load_music)
        self.load_button.grid(row=3, column=0, columnspan=2, pady=10, ipadx=12, ipady=2)

        # Skip Forward and Skip Back buttons
        self.skip_forward_button = ttk.Button(self.window, text="Skip Forward", command=self.skip_forward)
        self.skip_forward_button.grid(row=4, column=0, columnspan=1, pady=10, ipadx=12, ipady=2)

        self.skip_back_button = ttk.Button(self.window, text="Skip Back", command=self.skip_back)
        self.skip_back_button.grid(row=4, column=1, columnspan=1, pady=10, ipadx=12, ipady=2)

        # 显示时间标签
        self.time_label = ttk.Label(self.window, text="00:00 / 00:00", font=("Helvetica", 12))
        self.time_label.grid(row=5, column=0, columnspan=2, pady=5)

        # 进度条
        self.progress = ttk.Scale(self.window, from_=0, to=200, orient="horizontal", command=self.update_progress, cursor="hand2")
        self.progress.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def load_music(self):
        """从文件对话框中选择并加载音乐文件"""
        self.current_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3;*.wav")])
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
            print(f"Loaded: {self.current_file}")

    def play_music(self):
        """播放音乐"""
        if self.current_file:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            elif pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.paused = True

    def set_volume(self, volume):
        """设置音乐音量"""
        pygame.mixer.music.set_volume(float(volume))

    def skip_forward(self):
        """跳到音乐的下一个位置"""
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.play(start=current_pos + 10.0)
            self.update_time_label(current_pos)

    def skip_back(self):
        """跳到音乐的上一个位置"""
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            new_pos = max(0, int(current_pos) - 10)
            pygame.mixer.music.play(start=new_pos)
            self.update_time_label(current_pos)

    def update_progress_bar(self):
        """更新进度条和时间显示"""
        if pygame.mixer.music.get_busy() and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.progress.set(current_time)

            self.update_time_label(current_time)

            self.window.after(50, self.update_progress_bar)

    def update_time_label(self, current_time):
        """更新时间标签"""
        song_length = pygame.mixer.Sound(self.current_file).get_length()
        elapsed_minutes, elapsed_seconds = divmod(int(current_time), 60)
        total_minutes, total_seconds = divmod(int(song_length), 60)

        self.time_label.config(
            text=f"{elapsed_minutes:02}:{elapsed_seconds:02} / {total_minutes:02}:{total_seconds:02}")

    def update_progress(self, value):
        """通过拖动进度条来跳转播放时间"""
        if self.current_file and pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(value))
            self.update_time_label(float(value))

MusicPlayer().window.mainloop()
