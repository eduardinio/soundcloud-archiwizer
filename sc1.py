import customtkinter as ctk
import subprocess
import threading
import json
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("green") 

def get_track_count(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-single-json", url],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        if "tracks" in data:
            return len(data["tracks"])
        elif "entries" in data:
            return len(data["entries"])
        else:
            return 0
    except Exception:
        return None

def download_songs():
    artist = entry_artist.get().strip()
    if not artist:
        messagebox.showerror("Błąd", "Wpisz nazwę wykonawcy!")
        return
    
    url = f"https://soundcloud.com/{artist}"
    track_count = get_track_count(url)
    if track_count is None:
        messagebox.showerror("Błąd", "Nie udało się pobrać informacji o utworach.")
        return
    elif track_count == 0:
        messagebox.showinfo("Info", "Nie znaleziono żadnych utworów dla tego wykonawcy.")
        return
    
    proceed = messagebox.askyesno("Potwierdzenie", f"Profil ma {track_count} utworów.\nCzy chcesz rozpocząć pobieranie?")
    if not proceed:
        return
    
    output_dir = filedialog.askdirectory(title="Wybierz folder zapisu")
    if not output_dir:
        return
    
    log_area.configure(state="normal")
    log_area.delete("0.0", "end")
    log_area.insert("end", f"Szukam profilu dla: {artist}...\n")
    log_area.insert("end", f"Znaleziono: {url}\n")
    log_area.insert("end", f"Liczba utworów: {track_count}\n")
    log_area.insert("end", "Rozpoczynam pobieranie...\n")
    log_area.configure(state="disabled")

    def run_download():
        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            log_area.configure(state="normal")
            log_area.insert("end", line)
            log_area.see("end")
            log_area.configure(state="disabled")
        process.wait()
        log_area.configure(state="normal")
        log_area.insert("end", "\nPobieranie zakończone!\n")
        log_area.configure(state="disabled")

    threading.Thread(target=run_download, daemon=True).start()


app = ctk.CTk()
app.title("soundcloud archiwizer v1")
app.geometry("700x480")
app.minsize(600, 400)


FONT = ("Segoe UI", 12)

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Nazwa wykonawcy :", font=FONT)
label.pack(anchor="w", pady=(0,8))

entry_artist = ctk.CTkEntry(frame, font=FONT)
entry_artist.pack(fill="x", pady=(0,15))

btn_download = ctk.CTkButton(frame, text="Pobierz utwory", font=FONT, command=download_songs)
btn_download.pack(pady=(0,15))

log_area = ctk.CTkTextbox(frame, font=("Consolas", 11), corner_radius=10)
log_area.pack(fill="both", expand=True)
log_area.configure(state="disabled")

app.mainloop()