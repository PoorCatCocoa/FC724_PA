import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class MusicPlayer:      #Creat the main class using OOP
    def __init__(self):
        # Initialize Pygame and Pygame mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize Tkinter window
        self.window = tk.Tk()
        self.window.title("Music Player")
        self.window.geometry("350x200")
        self.window.resizable(False, False)

        # Using ttk style
        win_style = ttk.Style()

        # Current playback state and audio file
        self.current_file = None
        self.paused = False

        # All widgets are using ttk style, and using grid to place them
        # Play/Pause button
        self.play_button = ttk.Button(self.window, text="Play", command=self.play_music)
        self.play_button.grid(row=5, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)

        # Volume slider
        # using hand2 to change the style of the mouse while touch the bar
        ttk.Label(self.window, text="Volume", anchor="center").grid(row=6, column=1, columnspan=2)
        self.volume_slider = ttk.Scale(self.window, from_=0, to=1, orient="horizontal", command=self.set_volume,
                                       cursor="hand2", value=0.5)
        self.volume_slider.grid(row=6, column=3, columnspan=2, ipadx=12, ipady=2)

        # Load music button
        self.load_button = ttk.Button(self.window, text="Load Music", command=self.load_music)
        self.load_button.grid(row=7, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)

        # Skip forward and skip back buttons
        self.skip_forward_button = ttk.Button(self.window, text="⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=5, column=5, columnspan=2, pady=10, ipadx=12, ipady=2)

        self.skip_back_button = ttk.Button(self.window, text="⏪", command=self.skip_back)
        self.skip_back_button.grid(row=5, column=1, columnspan=2, pady=10, ipadx=12, ipady=2)

        # Time display label
        self.time_label = ttk.Label(self.window, text="00:00 / 00:00", font=("Helvetica", 12))
        self.time_label.grid(row=0, column=3, columnspan=2, pady=5)

        # Progress bar
        self.progress = ttk.Scale(self.window, from_=0, to=500, orient="horizontal", command=self.update_progress, cursor="hand2")
        self.progress.grid(row=2, column=3, columnspan=2, padx=20, pady=10, sticky="ew")

    def load_music(self):
        # Open file dialog to select music file
        self.current_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3;*.wav")])
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
        return self.current_file

    def play_music(self):
        # Play or pause the music
        if self.current_file:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
                self.update_progress_bar() #the only way I thought to keeping update the progress bar & time, may cause a little bit delay of music
                self.play_button = ttk.Button(self.window, text="Pause", command=self.play_music)
                self.play_button.grid(row=5, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.update_progress_bar()
            elif pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.paused = True
                self.play_button = ttk.Button(self.window, text="Play", command=self.play_music)
                self.play_button.grid(row=5, column=3, columnspan=2, pady=10, ipadx=12, ipady=2)

    def set_volume(self, volume):
        # Set the volume of the music
        pygame.mixer.music.set_volume(float(volume))

    def skip_forward(self):
        # Skip forward 10 seconds in the music
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(start=int(current_pos) + 10)

    def skip_back(self):
        # Skip backward 10 seconds in the music
        if self.current_file:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            new_pos = max(0, int(current_pos) - 10)
            pygame.mixer.music.play(start=new_pos)

    def update_progress_bar(self):
        # Update the progress bar and time label
        if pygame.mixer.music.get_busy() and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.progress.set(current_time)
            self.update_time_label(current_time)
            self.window.after(1000, self.update_progress_bar)

    def update_time_label(self, current_time):
        # Update the time label to show the current time and total duration
        song_length = pygame.mixer.Sound(self.current_file).get_length()
        elapsed_minutes, elapsed_seconds = divmod(int(current_time), 60)       #Use divmod to deal the timer
        total_minutes, total_seconds = divmod(int(song_length), 60)
        self.time_label.config(
            text=f"{elapsed_minutes:02}:{elapsed_seconds:02} / {total_minutes:02}:{total_seconds:02}")

    def update_progress(self, value):
        # Update the progress of the music based on the progress bar
        if self.current_file and pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(value))
            self.update_time_label(float(value))

# Create and run the music player window
MusicPlayer().window.mainloop()