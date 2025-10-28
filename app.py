# app.py

import streamlit as st
import os
from src.core.engine import encrypt, decrypt, encrypt_headerless, decrypt_headerless, encrypt_steganography, decrypt_steganography

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Enkripsi Puitis",
    page_icon="📜",
    layout="centered"
)

# --- Daftar Tema/Codebook ---
THEME_DIR = "data"
try:
    # Cari semua file .json di dalam direktori data
    AVAILABLE_THEMES = [f for f in os.listdir(THEME_DIR) if f.endswith('.json')]
except FileNotFoundError:
    AVAILABLE_THEMES = []

# --- Tampilan Antarmuka (UI) ---
st.title("📜 Enkripsi Puitis")
st.write("Sebuah aplikasi untuk mengubah teks menjadi ciphertext puitis menggunakan Kriptografi Klasik dan Steganografi.")
# st.image("https://i.imgur.com/g0y2jV8.jpeg", caption="Seni Enkripsi dan Sastra")
st.image("https://avatars.githubusercontent.com/u/234149534?", caption="Seni Enkripsi dan Sastra")


# --- Sidebar untuk Kontrol ---
st.sidebar.header("⚙️ Pengaturan")

mode = st.sidebar.selectbox(
    "Pilih Mode Enkripsi:",
    ("Standar (Dengan Header)", "Headerless (Tanpa Header, Trade-Off)", "Steganografi (Tanpa Header, Akurat)")
)

key = st.sidebar.text_input("Masukkan Kunci Enkripsi:", placeholder="Contoh: RAHASIA")

if not AVAILABLE_THEMES:
    st.sidebar.error(f"Direktori tema '{THEME_DIR}' tidak ditemukan.")
    selected_theme = None
else:
    selected_theme = st.sidebar.selectbox(
        "Pilih Tema Puisi (Codebook):",
        AVAILABLE_THEMES
    )
    theme_path = os.path.join(THEME_DIR, selected_theme)


# --- Area Input dan Tombol Aksi ---
st.header("Masukkan Teks Anda")
text_input = st.text_area("Plaintext atau Ciphertext Puitis", height=200, placeholder="Ketik atau tempel teks di sini...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Enkripsi", use_container_width=True):
        if not text_input or not key or not selected_theme:
            st.error("Harap isi semua kolom: Teks, Kunci, dan pilih Tema.")
        else:
            try:
                with st.spinner("Merangkai kata menjadi rahasia..."):
                    if mode == "Standar (Dengan Header)":
                        result = encrypt(text_input, key, theme_path)
                    elif mode == "Headerless (Tanpa Header, Trade-Off)":
                        result = encrypt_headerless(text_input, key, theme_path)
                    else: # Steganografi
                        result = encrypt_steganography(text_input, key, theme_path)
                st.success("Enkripsi Berhasil!")
                st.text_area("Hasil Ciphertext Puitis:", value=result, height=300)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat enkripsi: {e}")

with col2:
    if st.button("🔓 Dekripsi", use_container_width=True):
        if not text_input or not key or not selected_theme:
            st.error("Harap isi semua kolom: Teks, Kunci, dan pilih Tema.")
        else:
            try:
                with st.spinner("Mengungkap rahasia dari kata..."):
                    if mode == "Standar (Dengan Header)":
                        result = decrypt(text_input, key, theme_path)
                    elif mode == "Headerless (Tanpa Header, Trade-Off)":
                        result = decrypt_headerless(text_input, key, theme_path)
                    else: # Steganografi
                        result = decrypt_steganography(text_input, key, theme_path)
                st.success("Dekripsi Berhasil!")
                st.text_area("Hasil Plaintext Asli:", value=result, height=300)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat dekripsi: {e}")