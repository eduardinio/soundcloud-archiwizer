import customtkinter as ctk
import subprocess
import threading
import os
import sys
from tkinter import filedialog, messagebox
import json

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

FONT = ("Segoe UI Variable", 13)

def get_startupinfo():
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return si
    return None

def get_track_count(url):
    try:
        result = subprocess.run(
            [os.path.join(os.getcwd(), "yt-dlp.exe"), "--dump-single-json", url],
            capture_output=True,
            text=True,
            startupinfo=get_startupinfo()
        )
        data = json.loads(result.stdout)
        return len(data.get("tracks", data.get("entries", [])))
    except Exception as e:
        print(e)
        return None

def download_songs():
    artist = entry_artist.get().strip()
    if not artist:
        messagebox.showerror("Błąd", "Wpisz nazwę wykonawcy!")
        return

    url = f"https://soundcloud.com/{artist}"
    count = get_track_count(url)

    if count is None:
        messagebox.showerror("Błąd", "Nie udało się uzyskać danych o utworach.")
        return
    if count == 0:
        messagebox.showinfo("Brak utworów", "Nie znaleziono żadnych utworów na profilu.")
        return

    if not messagebox.askyesno("Potwierdź", f"Znaleziono {count} utworów.\nRozpocząć pobieranie?"):
        return

    output_dir = filedialog.askdirectory(title="Wybierz folder do zapisu")
    if not output_dir:
        return

    log_area.configure(state="normal")
    log_area.delete("0.0", "end")
    log_area.insert("end", f"Pobieram z: {url}\n")
    log_area.configure(state="disabled")

    def run_download():
        command = [
            os.path.join(os.getcwd(), "yt-dlp.exe"),
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--force-overwrites",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            startupinfo=get_startupinfo()
        )

        for line in process.stdout:
            log_area.configure(state="normal")
            log_area.insert("end", line)
            log_area.see("end")
            log_area.configure(state="disabled")

        process.wait()
        log_area.configure(state="normal")
        log_area.insert("end", "\n✅ Pobieranie zakończone!\n")
        log_area.configure(state="disabled")

    threading.Thread(target=run_download, daemon=True).start()

# GUI
app = ctk.CTk()
app.title("soundcloud archiwizer")
app.geometry("700x500")
app.minsize(600, 400)

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Nazwa użytkownika SoundCloud:", font=FONT).pack(anchor="w", pady=(0, 10))
entry_artist = ctk.CTkEntry(frame, font=FONT)
entry_artist.pack(fill="x", pady=(0, 15))

ctk.CTkButton(frame, text="Pobierz utwory", font=FONT, command=download_songs).pack(pady=(0, 15))

log_area = ctk.CTkTextbox(frame, font=("Consolas", 11), corner_radius=10)
log_area.pack(fill="both", expand=True)
log_area.configure(state="disabled")

app.mainloop()
