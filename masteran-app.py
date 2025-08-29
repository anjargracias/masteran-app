import os
import random
from pytube import YouTube, Channel
from pydub import AudioSegment
from pydub.effects import normalize
import pygame

TEMP_DIR = "temp_masteran"
os.makedirs(TEMP_DIR, exist_ok=True)

# ---------------- Fungsi ----------------
def download_audio_from_video(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    filename = os.path.join(TEMP_DIR, yt.title + ".mp4")
    print(f"Downloading: {yt.title}")
    audio_stream.download(filename=filename)
    return filename

def load_audio_files(file_list):
    segments = []
    for f in file_list:
        seg = AudioSegment.from_file(f)
        segments.append(seg)
    return segments

def make_masteran(segments, target_minutes):
    combined = AudioSegment.silent(duration=0)
    random.shuffle(segments)
    for seg in segments:
        combined += seg
        if len(combined) >= target_minutes*60*1000:
            break
    while len(combined) < target_minutes*60*1000:
        combined += combined
    return combined[:target_minutes*60*1000]

def adjust_volume(seg, target_db=-15.0):
    seg = normalize(seg)
    change_db = target_db - seg.max_dBFS
    return seg.apply_gain(change_db)

def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    print("Playing audio...")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ---------------- Main ----------------
def main():
    print("=== MASTERAN MURAI 1 KLIK ===")
    # Tinggal ganti link YouTube di sini 👇
    urls = [
        "https://www.youtube.com/watch?v=xxxxxx",
        "https://www.youtube.com/watch?v=yyyyyy"
    ]

    all_files = []
    for url in urls:
        f = download_audio_from_video(url)
        all_files.append(f)

    segments = load_audio_files(all_files)
    masteran = make_masteran(segments, 5)   # 5 menit
    masteran = adjust_volume(masteran, -15)

    output_file = os.path.join(TEMP_DIR, "masteran_final.wav")
    masteran.export(output_file, format="wav")
    print(f"Masteran siap: {output_file}")
    play_audio(output_file)

    # bersihkan file sementara
    for f in all_files + [output_file]:
        try:
            os.remove(f)
        except:
            pass
    print("Selesai ✔")

if __name__ == "__main__":
    main()
