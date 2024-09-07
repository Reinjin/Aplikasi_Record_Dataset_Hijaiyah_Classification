import os

# Daftar huruf hijaiyah
huruf_hijaiyah = [
    'alif', 'ba', 'ta', 'tsa', 'jim', 'ha', 'kha', 'dal', 'dzal', 'ra', 
    'zay', 'sin', 'shin', 'sad', 'dad', 'tah', 'zah', 'ain', 'ghain', 
    'fa', 'qaf', 'kaf', 'lam', 'mim', 'nun', 'ha', 'waw', 'ya'
]

# Kondisi suara
kondisi = ['fathah', 'kasroh', 'dommah']

# Membuat list untuk kombinasi huruf dan kondisi
daftar_huruf_kondisi = [f"{huruf}_{k}" for huruf in huruf_hijaiyah for k in kondisi]

# Menampilkan hasil
print(daftar_huruf_kondisi)
print(f"Jumlah isian: {len(daftar_huruf_kondisi)}")

# Membuat 84 folder kosong yang baru
for i, nama_folder in enumerate(daftar_huruf_kondisi, start=1):
    nama_folder = f"{i:02d}. {nama_folder}"
    try:
        os.mkdir(nama_folder)
        print(f"Folder {nama_folder} berhasil dibuat")
    except FileExistsError:
        print(f"Folder {nama_folder} sudah ada")

print("Proses pembuatan folder selesai.")