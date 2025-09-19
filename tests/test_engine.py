# tests/test_modes.py

import unittest
import os
from src.core.engine import (
    encrypt,
    decrypt,
    encrypt_headerless, 
    decrypt_headerless,
    encrypt_steganography,
    decrypt_steganography
)

class TestEncryptionModes(unittest.TestCase):
    """
    Kelas tes untuk memvalidasi semua mode dengan urutan yang diatur.
    """
    def setUp(self):
        self.key = "RAHASIA"
        self.wrong_key = "SALAH"
        self.theme_path = os.path.join("data", "parikan_jowo_final.json")
        self.assertTrue(os.path.exists(self.theme_path), f"File codebook tidak ditemukan di {self.theme_path}")

    def test_01_standard_mode_success(self):
        """Memastikan mode Standar (dengan header) berhasil untuk teks kompleks."""
        print("\n--- [Tes 1] Mode Standar (Sukses) ---")

        original_text = "Teks standar dengan header, angka 1!"

        encrypted_output = encrypt(original_text, self.key, self.theme_path)
        decrypted_text = decrypt(encrypted_output, self.key, self.theme_path)

        print(f"  Plaintext Asli : '{original_text}'")
        print(f"  Hasil Enkripsi (Dengan Header):\n{encrypted_output}")
        print(f"  Hasil Dekripsi : '{decrypted_text}'")
        self.assertEqual(decrypted_text, original_text)

    def test_02_simple_mode_success(self):
        """Memastikan mode Sederhana berhasil untuk input yang valid."""
        print("\n--- [Tes 2] Mode Sederhana (Sukses) ---")

        original_text = "HARUSGENAP"
        
        encrypted_output = encrypt_headerless(original_text, self.key, self.theme_path)
        decrypted_text = decrypt_headerless(encrypted_output, self.key, self.theme_path)
        
        print(f"  Plaintext Asli : '{original_text}'")
        print(f"  Hasil Enkripsi :\n{encrypted_output}")
        print(f"  Hasil Dekripsi : '{decrypted_text}'")
        self.assertEqual(decrypted_text, original_text)

    def test_03_simple_mode_odd_length_fail(self):
        """Memastikan mode Sederhana GAGAL untuk input ganjil."""
        print("\n--- [Tes 3] Mode Sederhana (Gagal - Teks Ganjil) ---")

        original_text = "AMBAT"
        
        print(f"  Plaintext Asli : '{original_text}'")
        print("  -> Mengharapkan program untuk menghasilkan ValueError...")
        with self.assertRaises(ValueError):
            encrypt_headerless(original_text, self.key, self.theme_path)
        print("  -> Perilaku Sesuai Harapan: ValueError berhasil muncul.")

    def test_04_steganography_mode_success(self):
        """Memastikan mode Steganografi berhasil untuk round-trip teks kompleks."""
        print("\n--- [Tes 4] Mode Steganografi (Sukses) ---")

        original_text = "Ini adalah teks kompleks dengan angka 123 dan simbol 😎!"
        
        encrypted_output = encrypt_steganography(original_text, self.key, self.theme_path)
        decrypted_text = decrypt_steganography(encrypted_output, self.key, self.theme_path)
        
        print(f"  Plaintext Asli : '{original_text}'")
        print(f"  Hasil Enkripsi (Puisi Bersih):\n{encrypted_output}")
        print(f"  Hasil Dekripsi : '{decrypted_text}'")
        self.assertEqual(decrypted_text, original_text)

    def test_05_decryption_with_wrong_key(self):
        """Memastikan dekripsi dengan kunci yang salah TIDAK menghasilkan plaintext asli."""
        print("\n--- [Tes 5] Kegagalan Dekripsi (Kunci Salah) ---")

        original_text = "Ini teks asli"
        
        encrypted_output = encrypt_steganography(original_text, self.key, self.theme_path)
        decrypted_text = decrypt_steganography(encrypted_output, self.wrong_key, self.theme_path)
        
        print(f"  Plaintext Asli      : '{original_text}'")
        print(f"  Hasil Dekripsi Salah: '{decrypted_text}'")
        self.assertNotEqual(decrypted_text, original_text)
        print("  -> Perilaku Sesuai Harapan: Hasil dekripsi tidak sama dengan teks asli.")

    def test_06_steganography_decryption_corrupt_data_fail(self):
        """Memastikan dekripsi Steganografi GAGAL jika data tak kasat mata dihilangkan."""
        print("\n--- [Tes 6] Kegagalan Dekripsi (Ciphertext Stego Rusak) ---")
        
        corrupt_ciphertext = "Rembulane katon ayu\nKudu ngguyu ben ora rekoso"
        
        print(f"  Ciphertext Rusak:\n{corrupt_ciphertext}")
        print("  -> Mengharapkan program untuk menghasilkan ValueError...")
        with self.assertRaises(ValueError):
            decrypt_steganography(corrupt_ciphertext, self.key, self.theme_path)
        print("  -> Perilaku Sesuai Harapan: ValueError berhasil muncul.")

if __name__ == '__main__':
    unittest.main()