import os
import librosa
import soundfile as sf

from utils import huruf_hijaiyah as hh
from utils import kondisi as ksi

# Daftar huruf hijaiyah
huruf_hijaiyah = hh

# Kondisi suara
kondisi = ksi

# Membuat list untuk kombinasi huruf dan kondisi
daftar_huruf_kondisi = [f"{huruf}_{k}" for huruf in huruf_hijaiyah for k in kondisi]

daftar_nama_folder = []

for i, nama_folder in enumerate(daftar_huruf_kondisi, start=1):
    folder_name = f"{i:02d}. {nama_folder}"
    daftar_nama_folder.append(folder_name)


# Menggunakan current working directory sebagai main directory
main_directory = os.getcwd()  # Ini akan menjadi direktori di mana skrip dijalankan

# Target sample rate
target_sample_rate = 16000

# Proses pengubahan sample rate untuk setiap folder dan file audio di dalamnya
for folder_name in daftar_nama_folder:
    folder_path = os.path.join(main_directory, folder_name)
    
    # Periksa apakah folder ada
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.wav'):  # Hanya memproses file .wav
                input_path = os.path.join(folder_path, file_name)
                
                # Memuat file audio
                audio, sr = librosa.load(input_path, sr=44100)
                
                # Mengubah sample rate menjadi 16000 Hz
                audio_16000 = librosa.resample(audio, orig_sr=sr, target_sr=target_sample_rate)
                
                # Simpan file dengan sample rate baru (overwrite file asli)
                sf.write(input_path, audio_16000, target_sample_rate)
                print(f"Processed {file_name} in folder {folder_name} - Sample rate changed from {sr} to {target_sample_rate}")
    else:
        print(f"Folder {folder_name} tidak ditemukan.")

