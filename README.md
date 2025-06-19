# soundcloud archiwizer

A simple and modern desktop application for downloading **all audio tracks** from a SoundCloud user profile in **MP3** format. Perfect for archiving underground and independent artists' music collections.

## Features

* Download all tracks from any public SoundCloud user profile
* Automatic audio extraction and conversion to high-quality MP3 using `yt-dlp` and `ffmpeg`
* Clean and responsive graphical user interface built with CustomTkinter
* Cross-platform Python app (Windows focused, requires `yt-dlp.exe` and `ffmpeg.exe` binaries)
* No command-line knowledge required; just enter the username and select output folder
* Real-time log output in the GUI during downloads

## Requirements

* Python 3.7+
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) executable (`yt-dlp.exe` for Windows)
* [ffmpeg](https://ffmpeg.org/) executable (`ffmpeg.exe` for Windows)
* `customtkinter` Python package

## Installation

1. Clone this repository or download the source code
2. Download `yt-dlp.exe` and `ffmpeg.exe` and place them in the same directory as the script or compiled `.exe`
3. Install required Python packages:

```bash
pip install customtkinter
```

4. Run the script:

```bash
python soundcloud_downloader.py
```
(Or download release)

## Usage

1. Enter the SoundCloud username (e.g., `uglycrbnr`)
2. Click **Download Tracks**
3. Choose the destination folder
4. Wait for the download and conversion to complete
5. Find all tracks saved as `.mp3` files in the selected folder

## Notes

* The app uses `yt-dlp` under the hood to scrape SoundCloud profiles and download tracks
* `ffmpeg` is required for converting audio to MP3 format
* The app is packaged with PyInstaller to create a standalone `.exe` for Windows
* Make sure to place `yt-dlp.exe` and `ffmpeg.exe` alongside the `.exe` file when distributing
* App is in Polish language
