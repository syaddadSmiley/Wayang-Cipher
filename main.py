# main.py

import argparse
import sys
import subprocess
from src.core.engine import encrypt, decrypt, encrypt_headerless, decrypt_headerless, encrypt_steganography, decrypt_steganography

DEFAULT_THEME_PATH = "data/parikan_jowo_final.json"

def handle_encrypt(args):
    try:
        if args.steganography:
            target_func = encrypt_steganography
            mode_str = "(Mode Steganografi: Output Puisi Bersih & Akurat)"
        elif args.headerless:
            target_func = encrypt_headerless
            mode_str = "(Mode Headerless: Hanya Puisi)"
        else:
            target_func = encrypt
            mode_str = "(Mode Standar: Dengan Header)"
        
        try:
            with open(args.plaintext, 'r', encoding='utf-8') as f:
                plaintext = f.read()
            print(f"Mengenkripsi konten dari file: {args.plaintext}")
        except (FileNotFoundError, TypeError, OSError):
            plaintext = args.plaintext
            print("Mengenkripsi teks dari argumen langsung.")

        encrypted_result = target_func(plaintext, args.key, args.theme)
        
        print("\n--- Hasil Enkripsi ---")
        print(mode_str)
        print(encrypted_result)
        
        # --- LOGIKA BARU UNTUK MENYIMPAN KE FILE ---
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(encrypted_result)
                print(f"\n[SUKSES] Hasil enkripsi telah disimpan ke file: {args.output}")
            except Exception as e:
                print(f"\n[ERROR] Gagal menyimpan file: {e}")
        
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

def handle_decrypt(args):
    try:
        if args.steganography:
            target_func = decrypt_steganography
            mode_str = "(Mode Steganografi)"
        elif args.headerless:
            target_func = decrypt_headerless
            mode_str = "(Mode Headerless)"
        else:
            target_func = decrypt
            mode_str = "(Mode Standar)"
            
        try:
            with open(args.ciphertext, 'r', encoding='utf-8') as f:
                ciphertext = f.read()
            print(f"Mendekripsi konten dari file: {args.ciphertext}")
        except (FileNotFoundError, TypeError, OSError):
            ciphertext = args.ciphertext
            print("Mendekripsi teks dari argumen langsung.")

        decrypted_result = target_func(ciphertext, args.key, args.theme)
        
        print("\n--- Hasil Dekripsi ---")
        print(mode_str)
        print(decrypted_result)
        
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

def handle_test():
    print("--- Menjalankan Unit Tests ---")
    command = [sys.executable, '-m', 'unittest', 'discover', 'tests']
    try:
        subprocess.run(command, check=True)
        print("\n[SUKSES] Semua tes berhasil.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n[GAGAL] Terjadi kesalahan saat menjalankan tes.")

def main():
    parser = argparse.ArgumentParser(
        description="Aplikasi Enkripsi Puitis.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.epilog = (
        "Contoh Penggunaan:\n"
        "  Enkripsi ke file : python main.py encrypt \"Teks ini!\" -k KUNCI -t data/file.json --steganography -o chipertext.txt\n"
        "  Dekripsi dari file : python main.py decrypt chipertext.txt -k KUNCI -t data/file.json --steganography"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_encrypt = subparsers.add_parser('encrypt', help='Enkripsi plaintext.')
    parser_encrypt.add_argument('plaintext', type=str, help='Teks asli atau path ke file teks asli.')
    parser_encrypt.add_argument('-k', '--key', type=str, required=True, help='Kunci enkripsi.')
    parser_encrypt.add_argument('-t', '--theme', type=str, default=DEFAULT_THEME_PATH, help=f'Path ke file tema (default: {DEFAULT_THEME_PATH}')
    parser_encrypt.add_argument('-o', '--output', type=str, help='(Opsional) Simpan hasil enkripsi ke file.') # OPSI BARU
    mode_group_enc = parser_encrypt.add_mutually_exclusive_group()
    mode_group_enc.add_argument('--headerless', action='store_true', help='Gunakan mode headerless (tanpa header).')
    mode_group_enc.add_argument('--steganography', action='store_true', help='Gunakan mode steganografi (tanpa header, akurat).')

    parser_decrypt = subparsers.add_parser('decrypt', help='Dekripsi ciphertext.')
    parser_decrypt.add_argument('ciphertext', type=str, help='Teks sandi atau path ke file teks sandi.')
    parser_decrypt.add_argument('-k', '--key', type=str, required=True, help='Kunci dekripsi.')
    parser_decrypt.add_argument('-t', '--theme', type=str, default=DEFAULT_THEME_PATH, help=f'Path ke file tema (default: {DEFAULT_THEME_PATH}')
    mode_group_dec = parser_decrypt.add_mutually_exclusive_group()
    mode_group_dec.add_argument('--headerless', action='store_true', help='Gunakan mode headerless (tanpa header).')
    mode_group_dec.add_argument('--steganography', action='store_true', help='Gunakan mode steganografi (tanpa header, akurat).')

    subparsers.add_parser('test', help='Jalankan semua unit test.')
    args = parser.parse_args()

    if args.command == 'encrypt':
        handle_encrypt(args)
    elif args.command == 'decrypt':
        handle_decrypt(args)
    elif args.command == 'test':
        handle_test()

if __name__ == '__main__':
    main()