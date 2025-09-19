# Enkripsi Puitis

Selamat datang di proyek Enkripsi Puitis. Aplikasi ini adalah implementasi unik dari kriptografi klasik yang mengubah pesan rahasia menjadi ciphertext yang berbentuk seperti puisi atau parikan Jawa. Alih-alih menghasilkan teks acak yang tidak bisa dibaca, aplikasi ini menyamarkan pesan terenkripsi Anda dalam bentuk karya sastra.

> Ini adalah sebuah karya yang sangat unik, bisa kita sebut sebagai **"puisi kriptografis"**. Aturan dan strukturnya tidak ditentukan oleh kaidah sastra, melainkan oleh logika matematis dari algoritma enkripsi yang mendasarinya.



## Fitur Utama
- **Enkripsi Vigenère:** Menggunakan algoritma Vigenère Cipher sebagai dasar kriptografi yang solid.
- **Codebook Puitis:** Memetakan hasil ciphertext ke dalam 676 frasa parikan Jawa yang unik untuk menghasilkan output puitis.
- **Tiga Mode Operasi:**
    1.  **Mode Standar:** Mode paling akurat, menggunakan header untuk memastikan dekripsi 100% sempurna untuk teks kompleks (termasuk spasi, angka, tanda baca, dan huruf kapital).
    2.  **Mode Sederhana:** Menghasilkan output puisi murni tanpa header, dengan syarat plaintext hanya berisi huruf dan berjumlah genap.
    3.  **Mode Steganografi:** Teknik paling canggih yang menyembunyikan header secara tak kasat mata di dalam puisi, menghasilkan output bersih dengan fungsionalitas penuh dari mode standar.
- **Dua Antarmuka:**
    1.  **GUI (Graphical User Interface):** Antarmuka web yang interaktif dan mudah digunakan, dibangun dengan Streamlit.
    2.  **CLI (Command-Line Interface):** Antarmuka berbasis terminal untuk pengguna mahir dan otomatisasi.

---

## Instalasi (Panduan untuk Pemula)
Ikuti langkah-langkah ini untuk menjalankan aplikasi di komputer Anda.

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python 3** (versi 3.7 atau lebih baru). Jika belum, unduh dari [python.org](https://www.python.org/downloads/).

### 2. Dapatkan Kode Proyek
Buka terminal (CMD, PowerShell, atau Terminal di Linux/Mac) dan jalankan perintah ini untuk mengunduh proyek:
```bash
git clone https://github.com/syaddadSmiley/Wayang-Cipher.git
```

Setelah selesai, masuk ke direktori proyek:
```bash
cd Wayang-Cipher
```

### 3. Buat dan Aktifkan Virtual Environment
Ini adalah langkah penting untuk menjaga agar library proyek ini tidak tercampur dengan proyek lain.

**Untuk Pengguna Windows (CMD/PowerShell):**
```bash
# Membuat environment bernama .venv
python -m venv .venv

# Mengaktifkan environment
.\.venv\Scripts\Activate
```
Setelah aktif, nama terminal Anda akan diawali dengan `(.venv)`.

**Untuk Pengguna macOS / Linux:**
```bash
# Membuat environment bernama .venv
python3 -m venv .venv

# Mengaktifkan environment
source .venv/bin/activate
```
Setelah aktif, nama terminal Anda akan diawali dengan `(.venv)`.

### 4. Instalasi Library
Dengan virtual environment yang sudah aktif, jalankan perintah ini untuk menginstal semua library yang dibutuhkan (yaitu Streamlit):
```bash
pip install -r requirements.txt
```
Tunggu hingga proses instalasi selesai. Sekarang, aplikasi Anda siap dijalankan!

---

## Cara Penggunaan

Anda bisa menjalankan aplikasi ini melalui GUI (cara termudah) atau CLI.

### Menggunakan GUI (Antarmuka Web) - Direkomendasikan
Ini adalah cara paling mudah dan interaktif untuk menggunakan aplikasi.

1.  Pastikan virtual environment Anda aktif.
2.  Jalankan perintah berikut di terminal:
    ```bash
    streamlit run app.py
    ```
3.  Sebuah tab baru akan otomatis terbuka di browser Anda, menampilkan antarmuka aplikasi.
4.  **Cara Pakai:**
    - Di sidebar kiri, pilih **Mode**, masukkan **Kunci**, dan pilih **Tema**.
    - Di area teks utama, masukkan pesan Anda.
    - Klik tombol **"Enkripsi"** atau **" Dekripsi"**.
    - Hasilnya akan muncul di kotak di bawahnya.

### Menggunakan CLI (Terminal)
Untuk pengguna yang lebih mahir.

**Format Perintah Dasar:**
`python main.py [perintah] "[teks]" -k [kunci] -t [path_tema] [mode]`

**Contoh-contoh:**

* **Enkripsi Mode Standar:**
    ```bash
    python main.py encrypt "Ini pesan rahasia, nomor 1!" -k JAWA -t data/parikan_jowo_final.json
    ```

* **Enkripsi Mode Sederhana (Teks harus genap & hanya huruf):**
    ```bash
    python main.py encrypt "INIRAHASIASEKALI" -k JAWA -t data/parikan_jowo_final.json --simple
    ```

* **Enkripsi Mode Steganografi (Output bersih, akurasi penuh):**
    ```bash
    python main.py encrypt "Ini pesan rahasia, nomor 1!" -k JAWA -t data/parikan_jowo_final.json --steganography
    ```

* **Dekripsi dari File (Contoh Steganografi):**
    ```bash
    # Enkripsi dan simpan hasilnya ke file output.txt
    python main.py encrypt "Teks super rahasia" -k JAWA -t data/parikan_jowo_final.json --steganography -o output.txt

    # Dekripsi dari file output.txt
    python main.py decrypt output.txt -k JAWA -t data/parikan_jowo_final.json --steganography
    ```
* **Menjalankan Unit Test:**
    ```bash
    python main.py test
    ```
---

## Struktur Proyek
```
.
├── data/
│   └── parikan_jowo_final.json  # File codebook
├── src/
│   └── core/
│       ├── __init__.py
│       └── engine.py            # Logika inti enkripsi/dekripsi
├── tests/
│   ├── __init__.py
│   └── test_engine.py           # Unit test
├── .gitignore
├── app.py                       # Kode untuk GUI Streamlit
├── generate_codebook.py         # Skrip untuk membuat codebook
├── main.py                      # Kode untuk CLI
├── README.md                    # Dokumentasi ini
└── requirements.txt             # Daftar library
```