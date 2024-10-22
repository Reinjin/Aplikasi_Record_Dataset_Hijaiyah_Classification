import os
import shutil
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

# Fungsi untuk menduplikasi file
def duplicate_file(file_path, new_file_path):
    shutil.copy2(file_path, new_file_path)

# Menduplikasi file dalam setiap folder
for folder_name in daftar_nama_folder:
    folder_path = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_name_without_ext, file_extension = os.path.splitext(file_name)
                for i in range(1, 4):  # Duplikasi 3 kali
                    new_file_name = f"{file_name_without_ext}_{i}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_file_name)
                    
                    # Cek jika file dengan nama yang sama sudah ada
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_name = f"{file_name_without_ext}_{i}_{counter}{file_extension}"
                        new_file_path = os.path.join(folder_path, new_file_name)
                        counter += 1
                    
                    duplicate_file(file_path, new_file_path)
                    print(f"File {new_file_name} berhasil dibuat di folder {folder_name}")

print("Proses duplikasi file selesai.")

