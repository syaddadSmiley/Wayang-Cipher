# src/core/engine.py

import json
import base64
import os

BOUNDARY = "\n---POE-BOUNDARY---\n"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PADDING_CHAR = 'X'

# --- KARAKTER STEGANOGRAFI (TAK KASAT MATA) ---
ZERO_WIDTH_SPACE = '\u200b'  # Mewakili bit '0'
ZERO_WIDTH_NON_JOINER = '\u200c' # Mewakili bit '1'

# --- FUNGSI INTI ---
def vigenere_process(text_upper, key_upper, mode):
    result = []
    key_len = len(key_upper)
    for i, char in enumerate(text_upper):
        text_num = ALPHABET.find(char)
        key_num = ALPHABET.find(key_upper[i % key_len])
        if mode == 'encrypt':
            result_num = (text_num + key_num) % 26
        else: # decrypt
            result_num = (text_num - key_num + 26) % 26
        result.append(ALPHABET[result_num])
    return "".join(result)

def core_encrypt(plaintext, key, dictionary):
    alpha_chars = [char for char in plaintext if char.isalpha()]
    alpha_text_upper = "".join(alpha_chars).upper()
    
    non_alpha_map = {i: char for i, char in enumerate(plaintext) if not char.isalpha()}
    uppercase_indices = {i for i, char in enumerate(alpha_chars) if char.isupper()}

    vigenere_ciphertext = vigenere_process(alpha_text_upper, key.upper(), 'encrypt')
    
    padded = False
    if len(vigenere_ciphertext) % 2 != 0:
        vigenere_ciphertext += PADDING_CHAR
        padded = True

    bigrams = [vigenere_ciphertext[i:i+2] for i in range(0, len(vigenere_ciphertext), 2)]
    
    poetic_lines = [dictionary.get(bg, {}).get('phrase', f"({bg})") for bg in bigrams]
    
    poetic_output = ""
    for i in range(0, len(poetic_lines), 4):
        chunk = poetic_lines[i:i+4]
        bait = "\n".join(chunk)
        poetic_output += bait + "\n\n"
    poetic_output = poetic_output.strip()
        
    header_obj = {"non_alpha": non_alpha_map, "uppercase": list(uppercase_indices), "padded": padded}
    
    # --- PERUBAHAN KRUSIAL 1 ---
    # Sekarang mengembalikan 2 nilai: puisi dan objek header mentah
    return poetic_output, header_obj

def core_decrypt(poetic_body, key, inverse_map, header_obj):
    lines = [line for line in poetic_body.strip().split('\n') if line]
    vigenere_ciphertext = "".join([inverse_map.get(line, "") for line in lines])
    padded = header_obj["padded"]
    if padded:
        vigenere_ciphertext = vigenere_ciphertext[:-1]
    decrypted_upper = vigenere_process(vigenere_ciphertext, key.upper(), 'decrypt')
    uppercase_indices = set(header_obj["uppercase"])
    non_alpha_map = {int(k): v for k, v in header_obj["non_alpha"].items()}
    decrypted_cased_chars = [
        char.upper() if i in uppercase_indices else char.lower()
        for i, char in enumerate(decrypted_upper)
    ]
    result_chars = []
    alpha_idx = 0
    total_len = len(decrypted_cased_chars) + len(non_alpha_map)
    for i in range(total_len):
        if i in non_alpha_map:
            result_chars.append(non_alpha_map[i])
        else:
            if alpha_idx < len(decrypted_cased_chars):
                result_chars.append(decrypted_cased_chars[alpha_idx])
                alpha_idx += 1
    return "".join(result_chars)

# --- FUNGSI WRAPPER ---
def encrypt(plaintext, key, theme_path):
    """Fungsi wrapper untuk mode standar (dengan header)."""
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f).get('dictionary', {})
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
    
    # --- PERUBAHAN KRUSIAL 2 ---
    # Menangkap 2 nilai dari core_encrypt
    poetic_output, header_obj = core_encrypt(plaintext, key, dictionary)
    
    # Memformat header menjadi string di sini
    header_data = json.dumps(header_obj, sort_keys=True).encode('utf-8')
    encoded_header = base64.b64encode(header_data).decode('utf-8')
    return f"{encoded_header}{BOUNDARY}{poetic_output}"

def decrypt(ciphertext, key, theme_path):
    """Fungsi wrapper untuk mode standar."""
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            inverse_map = {v['phrase']: k for k, v in json.load(f).get('dictionary', {}).items()}
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
    try:
        encoded_header, poetic_body = ciphertext.split(BOUNDARY, 1)
        header_data = base64.b64decode(encoded_header)
        header_obj = json.loads(header_data)
    except Exception:
        raise ValueError("Invalid ciphertext format or corrupt header.")
    return core_decrypt(poetic_body, key, inverse_map, header_obj)
    
def encrypt_headerless(plaintext, key, theme_path):
    """Fungsi wrapper untuk mode headerless."""
    alpha_text = "".join([c for c in plaintext if c.isalpha()]).upper()
    if len(alpha_text) % 2 != 0:
        raise ValueError("Untuk mode headerless, jumlah huruf dalam plaintext harus genap.")
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f).get('dictionary', {})
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
    
    # Fungsi ini sudah benar karena hanya mengambil nilai pertama (puisi)
    poetic_output, _ = core_encrypt(alpha_text, key, dictionary)
    return poetic_output

def decrypt_headerless(poetic_ciphertext, key, theme_path):
    # ... (Fungsi ini tidak berubah)
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            inverse_map = {v['phrase']: k for k, v in json.load(f).get('dictionary', {}).items()}
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
    lines = [line for line in poetic_ciphertext.strip().split('\n') if line]
    vigenere_ciphertext = "".join([inverse_map.get(line, "") for line in lines])
    return vigenere_process(vigenere_ciphertext, key.upper(), 'decrypt')

# --- FUNGSI STEGANOGRAFI (Tidak berubah, sekarang akan bekerja) ---
def _header_to_zero_width(header_obj):
    json_str = json.dumps(header_obj, sort_keys=True)
    binary_str = ''.join(format(byte, '08b') for byte in json_str.encode('utf-8'))
    return binary_str.replace('0', ZERO_WIDTH_SPACE).replace('1', ZERO_WIDTH_NON_JOINER)

def _zero_width_to_header(text):
    binary_str = ""
    for char in text:
        if char == ZERO_WIDTH_SPACE:
            binary_str += '0'
        elif char == ZERO_WIDTH_NON_JOINER:
            binary_str += '1'
    if not binary_str:
        raise ValueError("Tidak ada data steganografi yang ditemukan dalam ciphertext.")
    byte_array = bytearray(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
    json_str = byte_array.decode('utf-8')
    return json.loads(json_str)

def encrypt_steganography(plaintext, key, theme_path):
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f).get('dictionary', {})
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
    
    # Fungsi ini sekarang akan menerima 2 nilai dengan benar
    poetic_output, header_obj = core_encrypt(plaintext, key, dictionary)
    stego_payload = _header_to_zero_width(header_obj)
    
    return poetic_output + stego_payload

def decrypt_steganography(poetic_ciphertext, key, theme_path):
    try:
        with open(theme_path, 'r', encoding='utf-8') as f:
            inverse_map = {v['phrase']: k for k, v in json.load(f).get('dictionary', {}).items()}
    except FileNotFoundError:
        raise ValueError(f"Error: File tema tidak ditemukan di '{theme_path}'")
        
    header_obj = _zero_width_to_header(poetic_ciphertext)
    visible_poetic_body = poetic_ciphertext.replace(ZERO_WIDTH_SPACE, "").replace(ZERO_WIDTH_NON_JOINER, "")
    
    return core_decrypt(visible_poetic_body, key, inverse_map, header_obj)