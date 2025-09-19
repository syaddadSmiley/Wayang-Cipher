# tests/test_engine.py

import unittest
import os
from src.core.engine import encrypt, decrypt 

class TestEncryptionEngine(unittest.TestCase):
    def setUp(self):
        self.key = "RAHASIA"
        self.theme_path = os.path.join("data", "parikan_jowo_final.json")

    def test_all_scenarios(self):
        scenarios = {
            "Plaintext Pendek": "SERBU",
            "Plaintext Panjang": "INI ADALAH CONTOH TEKS YANG SANGAT PANJANG UNTUK DIUJI",
            "Karakter Non-Alfabet": "Pesan rahasia dikirim jam 19:00, kodenya adalah 'Elang-1'!",
            "Teks Multiline": "Baris pertama dari pesan.\nIni adalah baris kedua.\nDan ini baris terakhir.",
            "Emoji dan Akronim": "Misi kita adalah ASAP (As Soon As Possible). Siap! 👍"
        }
        
        for name, original_text in scenarios.items():
            with self.subTest(name=name):
                # Pastikan file codebook ada sebelum menjalankan tes
                self.assertTrue(os.path.exists(self.theme_path), f"File codebook tidak ditemukan di {self.theme_path}")
                
                print(f"\nOriginal Test : '{original_text}'")
                encrypted_output = encrypt(original_text, self.key, self.theme_path)
                print(f"\nEncrypted Output : '{encrypted_output}'")
                decrypted_text = decrypt(encrypted_output, self.key, self.theme_path)
                print(f"\nDecrypted Output : '{decrypted_text}'")
                
                self.assertEqual(decrypted_text, original_text)

if __name__ == '__main__':
    unittest.main()