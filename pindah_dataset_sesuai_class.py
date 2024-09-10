import os
import shutil

# Daftar huruf hijaiyah
huruf_hijaiyah = [
    'alif', 'ba', 'ta', 'tsa', 'jim', 'hah', 'kha', 'dal', 'dzal', 'ra', 
    'zay', 'sin', 'shin', 'sad', 'dad', 'tah', 'zah', 'ain', 'ghain', 
    'fa', 'qaf', 'kaf', 'lam', 'mim', 'nun', 'Ha', 'waw', 'ya'
]

# Kondisi suara
kondisi = ['fathah', 'kasroh', 'dommah']

# Membuat list untuk kombinasi huruf dan kondisi
daftar_huruf_kondisi = [f"{huruf}_{k}" for huruf in huruf_hijaiyah for k in kondisi]

# Menampilkan hasil
print(daftar_huruf_kondisi)
print(f"Jumlah isian: {len(daftar_huruf_kondisi)}")

# Path sumber file audio
source_path = r"E:/Contoh Dataset Skripsi/Dataset_Record_Baru/Record_Mentah_Dikumpulkan"

# Membuat 84 folder dan memindahkan file yang sesuai
for i, nama_folder in enumerate(daftar_huruf_kondisi, start=1):
    folder_name = f"{i:02d}. {nama_folder}"
    try:
        os.mkdir(folder_name)
        print(f"Folder {folder_name} berhasil dibuat")
    except FileExistsError:
        print(f"Folder {folder_name} sudah ada")
    
    # Mencari dan memindahkan file yang sesuai
    for filename in os.listdir(source_path):
        if filename.endswith(f"{nama_folder}.wav"):
            source_file = os.path.join(source_path, filename)
            destination_file = os.path.join(folder_name, filename)
            
            # Cek apakah file dengan nama yang sama sudah ada
            counter = 1
            while os.path.exists(destination_file):
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{counter}{ext}"
                destination_file = os.path.join(folder_name, new_filename)
                counter += 1
            
            shutil.move(source_file, destination_file)
            print(f"File {os.path.basename(destination_file)} dipindahkan ke folder {folder_name}")

print("Proses pembuatan folder dan pemindahan file selesai.")