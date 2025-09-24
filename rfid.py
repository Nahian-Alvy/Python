import serial
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
 
# --- CONFIG ---
SERIAL_PORT = "COM5"
BAUDRATE = 115200
 
# Song library: UID → details
songs = {
    "B9 71 F9 03": {
        "file": "0001.mp3",
        "title": "Song One",
        "artist": "Artist A",
        "cover": "cover1.jpg"
    },
    "3A 9F 7C 21": {
        "file": "0002.mp3",
        "title": "Song Two",
        "artist": "Artist B",
        "cover": "cover2.jpg"
    }
}
 
# --- INIT MUSIC PLAYER ---
pygame.mixer.init()
 
# --- TKINTER GUI ---
root = tk.Tk()
root.title("RFID Music Player")
root.geometry("500x600")
root.configure(bg="#121212")
 
# Album cover
cover_label = tk.Label(root, bg="#121212")
cover_label.pack(pady=20)
 
# Song title
title_label = tk.Label(root, text="No Song", fg="white", bg="#121212", font=("Helvetica", 18, "bold"))
title_label.pack()
 
# Artist
artist_label = tk.Label(root, text="", fg="grey", bg="#121212", font=("Helvetica", 14))
artist_label.pack()
 
# Status
status_label = tk.Label(root, text="Place a card...", fg="lightgreen", bg="#121212", font=("Helvetica", 12))
status_label.pack(pady=10)
 
# Play/Pause button
is_playing = False
def toggle_play():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        play_button.config(text="▶ Play")
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        play_button.config(text="⏸ Pause")
        is_playing = True
 
play_button = ttk.Button(root, text="▶ Play", command=toggle_play)
play_button.pack(pady=20)
 
# --- Functions ---
def update_song(uid):
    if uid in songs:
        song = songs[uid]
 
        # Load music
        pygame.mixer.music.load(song["file"])
        pygame.mixer.music.play()
        global is_playing
        is_playing = True
        play_button.config(text="⏸ Pause")
 
        # Update labels
        title_label.config(text=song["title"])
        artist_label.config(text=song["artist"])
        status_label.config(text=f"Now Playing: {uid}")
 
        # Update cover
        img = Image.open(song["cover"]).resize((300, 300))
        img = ImageTk.PhotoImage(img)
        cover_label.config(image=img)
        cover_label.image = img
    else:
        status_label.config(text=f"Unknown UID: {uid}")
 
# --- SERIAL READER THREAD ---
def read_serial():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if line.startswith("Card UID:"):
                uid = line.replace("Card UID:", "").strip().upper()
                print("Detected UID:", uid)
                root.after(0, update_song, uid)
        except Exception as e:
            print("Serial error:", e)
            break
 
threading.Thread(target=read_serial, daemon=True).start()
 
# --- START GUI LOOP ---
root.mainloop()
