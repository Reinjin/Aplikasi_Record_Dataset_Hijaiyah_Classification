import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText
import pyaudio
import wave
import os
import time
import threading

from utils import huruf_hijaiyah as hh
from utils import huruf_hijaiyah_arab as hja
from utils import kondisi as ksi

from otomatisasi_file_dan_folder import create_folder_and_move_file

# Daftar huruf hijaiyah
huruf_hijaiyah = hh

# Daftar huruf hijaiyah dengan font Arab
huruf_hijaiyah_arab = hja

# Kondisi suara
kondisi = ksi

class AplikasiRecord:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikasi Record Huruf Hijaiyah")
        self.master.geometry("800x600")
        self.master.resizable(False, False)  # Menonaktifkan perubahan ukuran jendela

        self.nama_pengguna = tk.StringVar()
        self.huruf_terpilih = tk.StringVar()
        self.kondisi_terpilih = tk.StringVar()
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.start_time = 0

        self.huruf_buttons = {}
        self.kondisi_buttons = {}

        # Bind keyboard events
        self.master.bind('<Left>', lambda e: self.back_selection())
        self.master.bind('<Right>', lambda e: self.next_selection())
        self.master.bind('<Return>', lambda e: self.toggle_record())
        self.master.bind('<space>', lambda e: self.space_handler())

        self.create_widgets()

    def space_handler(self):
        # Simulasi menekan Enter (stop rekam)
        self.toggle_record()
        # Setelah rekaman selesai, pindah ke selanjutnya
        time.sleep(0.1)  # Delay 
        self.next_selection()  # Pindah ke selanjutnya
        time.sleep(0.1)  # Delay 
        self.toggle_record()  # Lanjut rekaman

    def create_widgets(self):
        # Frame untuk nama pengguna
        nama_frame = ttk.Frame(self.master)
        nama_frame.pack(pady=10)
        ttk.Label(nama_frame, text="Nama:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(nama_frame, textvariable=self.nama_pengguna).pack(side=tk.LEFT, padx=5)

        # Frame untuk huruf hijaiyah
        ttk.Separator(self.master, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        huruf_frame = ttk.Frame(self.master)
        huruf_frame.pack(pady=10)

        for i, (huruf, huruf_arab) in enumerate(zip(huruf_hijaiyah, huruf_hijaiyah_arab)):
            button = ttk.Button(huruf_frame, text=f"{huruf}\n {huruf_arab}", command=lambda h=huruf: self.pilih_huruf(h))
            button.grid(row=i//7, column=i%7, padx=5, pady=5)
            self.huruf_buttons[huruf] = button

        # Frame untuk kondisi dengan garis pemisah di atas
        ttk.Separator(self.master, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        kondisi_frame = ttk.Frame(self.master)
        kondisi_frame.pack(pady=10)

        for k in kondisi:
            button = ttk.Button(kondisi_frame, text=k, command=lambda c=k: self.pilih_kondisi(c))
            button.pack(side=tk.LEFT, padx=5)
            self.kondisi_buttons[k] = button

        # Frame untuk tombol navigasi dan record
        ttk.Separator(self.master, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        nav_frame = ttk.Frame(self.master)
        nav_frame.pack(pady=10)
        
        # Tombol Back
        self.back_button = ttk.Button(nav_frame, text="Back", command=self.back_selection)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        # Tombol Record
        self.record_button = ttk.Button(nav_frame, text="Record", command=self.toggle_record)
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Tombol Next
        self.next_button = ttk.Button(nav_frame, text="Next", command=self.next_selection)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Label waktu
        self.time_label = ttk.Label(self.master, text="00:00")
        self.time_label.pack(pady=5)

        # Scroll layout kosong
        self.scroll_layout = ScrolledText(self.master, width=75, height=10, state='disabled')
        self.scroll_layout.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        # Tombol Sesuaikan
        self.sesuaikan_button = ttk.Button(self.master, text="Sesuaikan File", command=self.confirm_sesuaikan, style='Red.TButton')
        self.sesuaikan_button.pack(side=tk.RIGHT, padx=(10,30), pady=10)

    def next_selection(self):
        if not self.is_recording:
            current_huruf = self.huruf_terpilih.get()
            current_kondisi = self.kondisi_terpilih.get()
            
            if not current_huruf:
                self.pilih_huruf(huruf_hijaiyah[0])
                self.pilih_kondisi(kondisi[0])
                return
                
            if not current_kondisi:
                self.pilih_kondisi(kondisi[0])
                return
                
            kondisi_idx = kondisi.index(current_kondisi)
            if kondisi_idx < len(kondisi) - 1:
                # Pindah ke kondisi berikutnya
                self.pilih_kondisi(kondisi[kondisi_idx + 1])
            else:
                # Pindah ke huruf berikutnya dan reset kondisi ke fathah
                huruf_idx = huruf_hijaiyah.index(current_huruf)
                if huruf_idx < len(huruf_hijaiyah) - 1:
                    self.pilih_huruf(huruf_hijaiyah[huruf_idx + 1])
                    self.pilih_kondisi(kondisi[0])
                else:
                    # Jika sudah di huruf terakhir, kembali ke huruf pertama
                    self.pilih_huruf(huruf_hijaiyah[0])
                    self.pilih_kondisi(kondisi[0])

    def back_selection(self):
        if not self.is_recording:
            current_huruf = self.huruf_terpilih.get()
            current_kondisi = self.kondisi_terpilih.get()
            
            if not current_huruf or not current_kondisi:
                return
                
            kondisi_idx = kondisi.index(current_kondisi)
            if kondisi_idx > 0:
                # Pindah ke kondisi sebelumnya
                self.pilih_kondisi(kondisi[kondisi_idx - 1])
            else:
                # Pindah ke huruf sebelumnya dan set kondisi ke dhommah
                huruf_idx = huruf_hijaiyah.index(current_huruf)
                if huruf_idx > 0:
                    self.pilih_huruf(huruf_hijaiyah[huruf_idx - 1])
                    self.pilih_kondisi(kondisi[-1])
                else:
                    # Jika sudah di huruf pertama, pindah ke huruf terakhir
                    self.pilih_huruf(huruf_hijaiyah[-1])
                    self.pilih_kondisi(kondisi[-1])

    def pilih_huruf(self, huruf):
        if not self.is_recording:
            self.huruf_terpilih.set(huruf)
            for h, button in self.huruf_buttons.items():
                if h == huruf:
                    button.configure(style='Selected.TButton')
                else:
                    button.configure(style='TButton')

    def pilih_kondisi(self, kondisi):
        if not self.is_recording:
            self.kondisi_terpilih.set(kondisi)
            for k, button in self.kondisi_buttons.items():
                if k == kondisi:
                    button.configure(style='Selected.TButton')
                else:
                    button.configure(style='TButton')

    def toggle_record(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        if not self.nama_pengguna.get() or not self.huruf_terpilih.get() or not self.kondisi_terpilih.get():
            messagebox.showerror("Error", "Isi nama, pilih huruf dan kondisi terlebih dahulu!")
            return

        self.is_recording = True
        self.record_button.config(text="Stop")
        self.frames = []
        self.start_time = time.time()

        # Menonaktifkan tombol huruf dan kondisi
        for button in self.huruf_buttons.values():
            button.config(state='disabled')
        for button in self.kondisi_buttons.values():
            button.config(state='disabled')

        # Menonaktifkan tombol Sesuaikan dan navigasi
        self.sesuaikan_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.back_button.config(state='disabled')

        threading.Thread(target=self.record_audio, daemon=True).start()
        self.update_time()

    def record_audio(self):
        # Menggunakan mic default sesuai OS
        default_input_device_index = self.audio.get_default_input_device_info()['index']
        stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, 
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

        # Mengaktifkan kembali tombol huruf dan kondisi
        for button in self.huruf_buttons.values():
            button.config(state='normal')
        for button in self.kondisi_buttons.values():
            button.config(state='normal')
        
        # Mengaktifkan kembali tombol Sesuaikan dan navigasi
        self.sesuaikan_button.config(state='normal')
        self.next_button.config(state='normal')
        self.back_button.config(state='normal')

        filename = f"{self.nama_pengguna.get()}_{self.huruf_terpilih.get()}_{self.kondisi_terpilih.get()}.wav"
        simpan_dir = "Record_Mentah"
        record_mentah_dir = os.path.join(os.getcwd(), simpan_dir)
        os.makedirs(record_mentah_dir, exist_ok=True)
        filepath = os.path.join(record_mentah_dir, filename)

        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print("Info", f"Rekaman disimpan: {filepath}")
        message_save = f"Rekaman disimpan: {simpan_dir}/{filename}\n"
        self.write_to_scroll_layout(message_save)

    def update_time(self):
        if self.is_recording:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_time)
        else:
            self.time_label.config(text="00:00")

    def sesuaikan(self):
        #subprocess.run(["python", "otomatisasi_file_dan_folder.py"])
        messages = create_folder_and_move_file()
        for message in messages:
            self.write_to_scroll_layout(message + '\n')

    def write_to_scroll_layout(self, text):
        self.scroll_layout.config(state='normal')
        self.scroll_layout.insert(tk.END, text)
        self.scroll_layout.see(tk.END)
        self.scroll_layout.config(state='disabled')

    def confirm_sesuaikan(self):
        confirm = messagebox.askquestion("Konfirmasi", "Apakah Kamu Yakin Sudah melakukan pengecekan file record?")
        if confirm == 'yes':
            input_password = simpledialog.askstring("Konfirmasi", "Masukkan password untuk melanjutkan")
            if input_password is None:
                return
            elif input_password == "YES":
                self.sesuaikan()
            else:
                messagebox.showerror("Error", "Password salah!")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TButton', font=('Times New Roman', 11))
    style.configure('Selected.TButton', background='#90EE90', font=('Times New Roman', 11, 'bold'))
    style.configure('Red.TButton', background='red', font=('Times New Roman', 11, 'bold'))
    app = AplikasiRecord(root)
    root.mainloop()