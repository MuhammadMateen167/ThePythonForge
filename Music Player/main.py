import os
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class MusicPlayer:
    path = "/home/" + os.getlogin() + "/Music"

    def __init__(self):
        pygame.mixer.init()

        self.window = tk.Tk()
        self.window.title("Music Player")
        self.window.geometry("500x500")
        self.window.config(bg="#F0E1D2")

        self.listBox = tk.Listbox(
            self.window,
            background="#D4F1F4",
            foreground="black",
            selectbackground="#A7C7E7",
            height=15,
            width=30,
            font=("Helvetica", 12),
            bd=0,
            highlightthickness=0,
        )
        self.listBox.pack(pady=20)

        self.updateMusicList()

        self.frame = tk.Frame(self.window, bg="#F0E1D2")
        self.frame.pack()

        self.playButton = ttk.Button(self.frame, text="Play", style="TButton", command=self.playMusic)
        self.playButton.grid(row=0, column=0, padx=10, pady=10)

        self.pauseButton = ttk.Button(self.frame, text="Pause", style="TButton", command=self.pauseMusic)
        self.pauseButton.grid(row=0, column=1, padx=10, pady=10)

        self.stopButton = ttk.Button(self.frame, text="Stop", style="TButton", command=self.stopMusic)
        self.stopButton.grid(row=0, column=2, padx=10, pady=10)

        self.chooseFolderButton = ttk.Button(self.frame, text="Choose Folder", style="TButton", command=self.loadMusic)
        self.chooseFolderButton.grid(row=1, column=0, columnspan=3, pady=10)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#A7C7E7", font=("Helvetica", 12))

        self.window.mainloop()

    def updateMusicList(self):
        self.listBox.delete(0, tk.END)
        try:
            music_files = [
                file for file in os.listdir(self.path) if file.endswith(".mp3")
            ]
            for idx, music in enumerate(music_files, start=1):
                self.listBox.insert(tk.END, f"{idx}. {music}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Directory {self.path} not found.")

    def loadMusic(self):
        self.path = filedialog.askdirectory(initialdir=self.path)
        if self.path:
            self.updateMusicList()

    def playMusic(self):
        try:
            selection = self.listBox.curselection()
            if selection:
                idx = selection[0]
                music_files = [
                    file for file in os.listdir(self.path) if file.endswith(".mp3")
                ]
                music = music_files[idx]
                music_path = os.path.join(self.path, music)
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play()
            else:
                messagebox.showerror("Error", "Please select a music file to play.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def pauseMusic(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pauseButton.config(state=tk.DISABLED)
            self.playButton.config(state=tk.NORMAL)

    def stopMusic(self):
        pygame.mixer.music.stop()
        self.pauseButton.config(state=tk.DISABLED)
        self.playButton.config(state=tk.NORMAL)


def main():
    app = MusicPlayer()


if __name__ == "__main__":
    main()