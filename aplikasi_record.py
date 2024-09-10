import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import os
import time
import threading

# Daftar huruf hijaiyah
huruf_hijaiyah = [
    'alif', 'ba', 'ta', 'tsa', 'jim', 'hah', 'kha', 'dal', 'dzal', 'ra', 
    'zay', 'sin', 'shin', 'sad', 'dad', 'tah', 'zah', 'ain', 'ghain', 
    'fa', 'qaf', 'kaf', 'lam', 'mim', 'nun', 'Ha', 'waw', 'ya'
]

# Kondisi suara
kondisi = ['fathah', 'kasroh', 'dommah']

class AplikasiRecord:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikasi Record Huruf Hijaiyah")
        self.master.geometry("800x600")

        self.nama_pengguna = tk.StringVar()
        self.huruf_terpilih = tk.StringVar()
        self.kondisi_terpilih = tk.StringVar()
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.start_time = 0

        self.create_widgets()

    def create_widgets(self):
        # Frame untuk nama pengguna
        nama_frame = ttk.Frame(self.master)
        nama_frame.pack(pady=10)
        ttk.Label(nama_frame, text="Nama:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(nama_frame, textvariable=self.nama_pengguna).pack(side=tk.LEFT, padx=5)

        # Frame untuk huruf hijaiyah
        huruf_frame = ttk.Frame(self.master)
        huruf_frame.pack(pady=10)

        for i, huruf in enumerate(huruf_hijaiyah):
            ttk.Button(huruf_frame, text=huruf, command=lambda h=huruf: self.pilih_huruf(h)).grid(row=i//7, column=i%7, padx=5, pady=5)

        # Frame untuk kondisi
        kondisi_frame = ttk.Frame(self.master)
        kondisi_frame.pack(pady=10)

        for k in kondisi:
            ttk.Button(kondisi_frame, text=k, command=lambda c=k: self.pilih_kondisi(c)).pack(side=tk.LEFT, padx=5)

        # Tombol Record
        self.record_button = ttk.Button(self.master, text="Record", command=self.toggle_record)
        self.record_button.pack(pady=10)

        # Label waktu
        self.time_label = ttk.Label(self.master, text="00:00")
        self.time_label.pack(pady=5)

    def pilih_huruf(self, huruf):
        self.huruf_terpilih.set(huruf)

    def pilih_kondisi(self, kondisi):
        self.kondisi_terpilih.set(kondisi)

    def toggle_record(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        if not self.nama_pengguna.get() or not self.huruf_terpilih.get() or not self.kondisi_terpilih.get():
            print("Error, Isi nama, pilih huruf dan kondisi terlebih dahulu!")
            return

        self.is_recording = True
        self.record_button.config(text="Stop")
        self.frames = []
        self.start_time = time.time()

        threading.Thread(target=self.record_audio, daemon=True).start()
        self.update_time()

    def record_audio(self):
        # Menggunakan mic default sesuai OS
        default_input_device_index = self.audio.get_default_input_device_info()['index']
        stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, 
                                 input=True, frames_per_buffer=1024,
                                 input_device_index=default_input_device_index)
        while self.is_recording:
            data = stream.read(1024)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Record")

        filename = f"{self.nama_pengguna.get()}_{self.huruf_terpilih.get()}_{self.kondisi_terpilih.get()}.wav"
        filepath = os.path.join(r"E:/Contoh Dataset Skripsi/Dataset_Record_Baru/Record_Mentah", filename)

        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print("Info", f"Rekaman disimpan: {filepath}")

    def update_time(self):
        if self.is_recording:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_time)
        else:
            self.time_label.config(text="00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiRecord(root)
    root.mainloop()