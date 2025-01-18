import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import pygame

class MusicPlayer:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Music Player")
		self.window.geometry("750x400")

		"""		设置背景图片
		self.bg_image = tk.PhotoImage(file=os.path.join(os.getcwd(), "MusicPlayer/images", "bg_con.png"))
		self.bg_label = ttk.Label(self.root, image=self.bg_image)
		self.bg_label.place(relx=0, depend=- 0, relwidth=1, relheight=1) 
		"""

		win_style = ttk.Style()
		win_style.theme_use('classic')
		win_style.configure('.', background='black', foreground='black')
		win_style.configure('TFrame', background='white', foreground='white')
		win_style.configure('TButton', font=('Arial', 12), background='black', foreground='white',
		activebackground='brown', activeforeground='white')
		win_style.configure('TLabel', font=('Arial', 12), background='black', foreground='white')
		win_style.configure('TScale', background='white')

		pygame.init()
		pygame.mixer.init()





a = MusicPlayer()
a.window.mainloop()