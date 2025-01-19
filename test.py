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
		win_style.theme_use('clam')
		# win_style.configure('.', background='black', foreground='black')
		# win_style.configure('TFrame', background='white', foreground='white')
		# win_style.configure('TButton', font=('Arial', 12), background='black', foreground='white',
		# 					activebackground='brown', activeforeground='white')
		# win_style.configure('TLabel', font=('Arial', 12), background='black', foreground='white')
		# win_style.configure('TScale', background='white')

		# 当前播放状态和音频文件
		self.current_file = None
		self.paused = False

		# 播放按钮
		self.play_button = ttk.Button(self.window, text="Play", command=self.play_music)
		self.play_button.grid(ipadx=12, ipady=2, pady=10)

		# 音量滑块
		self.volume_slider = ttk.Label(self.window, text="Volume", anchor="center")
		self.volume_slider.grid()
		self.volume_slider = ttk.Scale(self.window, from_=0, to=1, orient="horizontal", command=self.set_volume,
									   cursor="hand2", value=0.5)
		self.volume_slider.grid(ipadx=12, ipady=2)

		# 加载音乐按钮
		self.load_button = ttk.Button(self.window, text="Load Music", command=self.load_music)
		self.load_button.grid(ipadx=12, ipady=2, pady=10)

		# 运行 Tkinter 窗口
		self.window.mainloop()

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
				#print("Playing music...")
			elif self.paused:
				pygame.mixer.music.unpause()
				self.paused = False
				#print("Resumed music!")
			elif pygame.mixer.music.get_busy():
				pygame.mixer.music.pause()
				self.paused = True
				# print("Music paused.")

	def set_volume(self, volume):
		"""设置音乐音量"""
		pygame.mixer.music.set_volume(float(volume))
		print(f"Volume set to: {volume}")

MusicPlayer().window.mainloop()