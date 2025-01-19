import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class PygameMusicPlayer:
	def __init__(self):
		# 初始化 Pygame Mixer
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

		# 暂停按钮
		self.pause_button = ttk.Button(self.window, text="Pause", command=self.pause_music)
		self.pause_button.grid(ipadx=12, ipady=2, pady=10)

		# 停止按钮
		self.stop_button = ttk.Button(self.window, text="Stop", command=self.stop_music)
		self.stop_button.grid(ipadx=12, ipady=2, pady=10)

		# 音量滑块
		self.volume_slider = tk.Scale(self.window, from_=0, to=1, resolution=0.01, orient="horizontal", label="Volume",
									  command=self.set_volume)
		self.volume_slider.set(0.5)  # 默认音量
		self.volume_slider.grid(pady=10)

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
				print("Playing music...")
			elif self.paused:
				pygame.mixer.music.unpause()
				self.paused = False
				print("Resumed music!")

	def pause_music(self):
		"""暂停音乐"""
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.pause()
			self.paused = True
			print("Music paused.")

	def stop_music(self):
		"""停止音乐"""
		pygame.mixer.music.stop()
		self.paused = False
		print("Music stopped.")

	def set_volume(self, volume):
		"""设置音乐音量"""
		pygame.mixer.music.set_volume(float(volume))
		print(f"Volume set to: {volume}")


# 创建并运行播放器
if __name__ == "__main__":
	PygameMusicPlayer()
