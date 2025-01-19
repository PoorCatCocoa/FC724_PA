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
		self.window.geometry("400x600")

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

		self.playlist_frame = tk.Frame(self.window)
		self.playlist_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

		self.playlist = tk.Listbox(self.playlist_frame, width=50, height=20)
		self.playlist.pack(fill='both', expand=True)
		self.playlist.bind("<<ListboxSelect>>", self.play_selected)

		self.control_frame = ttk.Frame(self.window)
		self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
		self.control_frame.configure(border=1, relief="groove", borderwidth=2)

		self.play_var = tk.StringVar()
		self.play_var.set("Play")
		self.pause_button = ttk.Button(self.control_frame, textvariable=self.play_var, command=self.play_pause)
		self.pause_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

		self.skip_back_btn = ttk.Button(self.control_frame, text="⏪", command=self.skip_back)
		self.skip_back_btn.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

		self.skip_forward_btn = ttk.Button(self.control_frame, text="⏩", command=self.skip_forward)
		self.skip_forward_btn.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

		self.status_var = tk.StringVar()
		self.status_var.set("Volume Control")
		self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var)
		self.status_label.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

		self.volume_var = tk.DoubleVar()
		self.volume_scale = ttk.Scale(self.control_frame, orient="horizontal", from_=0, to=1, variable=self.volume_var, command=self.set_volume)
		self.volume_scale.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')

		self.import_btn = ttk.Button(self.control_frame, text="Import Music", command=self.import_music)
		self.import_btn.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

		self.progress_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=325, mode="determinate")
		self.progress_bar.grid(row=7, column=0, padx=10, pady=10, sticky='nsew')

		self.elapsed_time = ttk.Label(self.control_frame, text="00:00:00")
		self.elapsed_time.grid(row=8, column=0, padx=10, pady=10, sticky='nsew')

		self.current_song = ""

		self.paused = False

	def play_selected(self, event):
		selected_song = self.playlist.get(self.playlist.curselection())
		self.current_song = selected_song
		print(f"Selected song: {self.current_song}")
		pygame.mixer.music.load(self.current_song)
		self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[:40] + "...")
		song_length = pygame.mixer.Sound(self.current_song).get_length()
		print(f"Song length: {song_length}")
		self.progress_bar["maximum"] = song_length
		self.update_progressbar()
		pygame.mixer.music.play()
		self.play_var.set("Pause")

	def play_pause(self):
		if self.paused:
			pygame.mixer.music.unpause()
			self.paused = False
			self.play_var.set("Pause")
		else:
			pygame.mixer.music.pause()
			self.paused = True
			self.play_var.set("Play")

	def skip_back(self):
		selection = self.playlist.curselection()
		if selection:
			previous_song_index = int(selection[0])-1
			if previous_song_index >= 0:
				previous_song = self.playlist.get(previous_song_index)
				self.current_song = previous_song
				pygame.mixer.music.load(self.current_song)
				self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[:40] + "...")
				pygame.mixer.music.play()
				self.play_var.set("Pause")
			else:
				messagebox.showwarning("Warning", "This is the first song")
		else:
			messagebox.showwarning("Error", "No songs selected")

	def skip_forward(self):
		selection = self.playlist.curselection()
		if selection:
			next_song_index = int(selection[0])+1
			if next_song_index < self.playlist.size():
				next_song = self.playlist.get(next_song_index)
				self.current_song = next_song
				pygame.mixer.music.load(self.current_song)
				self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[:40] + "...")
				pygame.mixer.music.play()
				self.play_var.set("Pause")
			else:
				messagebox.showwarning("Warning", "This is the last song")

	def set_volume(self, val):
		volume = float(val)
		pygame.mixer.music.set_volume(volume)

	def import_music(self):
		current_song = filedialog.askopenfilenames()
		if self.current_song:
			pygame.mixer.music.load(self.current_song)
			print(f"Loaded: {self.current_song}")

	def update_progressbar(self):
		if pygame.mixer.music.get_busy():
			current_time = pygame.mixer.music.get_pos() / 1000
			print(f"Current time: {current_time}")
			self.progress_bar["value"] = current_time
			minutes, seconds = divmod(current_time, 60)
			hours, minutes = divmod(minutes, 60)
			self.elapsed_time.config(text="{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
			self.window.after(1000, self.update_progressbar)
		else:
			self.progress_bar["value"] = 0
			self.elapsed_time.config(text="00:00:00")


MusicPlayer().window.mainloop()