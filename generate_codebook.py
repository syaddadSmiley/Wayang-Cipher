import json
import random
import os
import sys

def generate_final_codebook():
    """
    Menghasilkan codebook lengkap 676 bi-gram dengan metode pra-generasi
    untuk menjamin keunikan dan mencegah proses macet.
    """
    print("--- Memulai Proses Pembuatan Codebook (Versi Definitif) ---")
    
    vocabs = {
        'benda': {
            'an': ['udan', 'wulan', 'dalan', 'pangan', 'kancan', 'taman', 'papan', 'kahanan', 'tekanan', 'lamunan', 'katresnan'],
            'i': ['ati', 'bumi', 'wengi', 'geni', 'meri', 'janji', 'bukti', 'pati', 'sandhing', 'suci', 'sepi'],
            'o': ['roso', 'tresno', 'loro', 'dongo', 'songo', 'werno', 'asmoro', 'karyo', 'bodho', 'rekoso'],
            'u': ['banyu', 'watu', 'sliramu', 'nesu', 'turu', 'awakmu', 'wektumu', 'rasamu', 'pilu', 'rindu'],
            'ung': ['gunung', 'suwung', 'gandrung', 'wurung', 'agung', 'bingung', 'jantung', 'sarung'],
            'ing': ['wening', 'bening', 'sanding', 'kuning', 'pusing', 'miring', 'keping', 'garing']
        },
        'sifat': {
            'an': ['terang', 'tenan', 'nyaman', 'edan', 'kasmaran', 'tentrem', 'nelongso'],
            'i': ['wangi', 'pesti', 'gemati', 'lathi', 'prasetyaji', 'sepi', 'suci'],
            'o': ['ijo', 'tuwo', 'gelo', 'rumongso', 'prasojo', 'loro', 'bodho'],
            'u': ['ayu', 'kudu', 'bingung', 'pilu', 'kelu', 'saru', 'rindu'],
            'ar': ['anyar', 'sabar', 'kasar', 'bubar', 'jembar', 'sumebar'],
            'ur': ['luhur', 'akur', 'makmur', 'campur', 'mujur', 'hancur']
        },
        'kriya': {
            'an': ['kelingan', 'bebarengan', 'pamitan', 'perangan', 'goyangan'],
            'i': ['ngenteni', 'nggoleki', 'ngrasani', 'ngajeni', 'ngugemi', 'ngobati'],
            'o': ['lungo', 'moco', 'ngomong', 'kerjo', 'nrimo', 'nyoto'],
            'u': ['mlaku', 'ngguyu', 'sinau', 'nesu', 'nyawiji', 'ngganggu']
        }
    }
    templates = [
        "Rembulane katon {sifat}", "Kembang {benda} ing pinggir dalan", "Angin wengi nggowo {benda}",
        "Rasane {sifat} ing njero ati", "Urip iku kudu {sifat}", "Ojo seneng gawe {sifat}",
        "Yen {kriya} ojo lali wektu", "Isuk-isuk wes {kriya}", "Ngenteni tekane {benda}",
        "Sliramu katon luwih {sifat}", "Swara {benda} ing wayah wengi", "Ayo {kriya} kanthi temenan",
        "Langite katon {sifat}", "Tansah eling marang {benda}", "Golek {benda} tekan {benda}",
        "Ati {sifat} amergo {benda}", "Kudu {kriya} ben ora {sifat}"
    ]
    
    # 1. Pra-generasi semua kemungkinan frasa unik
    print("[INFO] Membuat semua kemungkinan kombinasi frasa...")
    unique_phrases = set()
    for template in templates:
        placeholders = [ph[1:-1] for ph in template.split() if ph.startswith('{') and ph.endswith('}')]
        
        # Ini adalah loop kombinatorial headerless untuk mengisi placeholder
        # Untuk 1 placeholder
        if len(placeholders) == 1:
            cat = placeholders[0]
            for rhyme_group in vocabs[cat].values():
                for word in rhyme_group:
                    unique_phrases.add(template.format(**{cat: word}))
        # Untuk 2 placeholder
        elif len(placeholders) == 2:
            cat1, cat2 = placeholders[0], placeholders[1]
            for rhyme_group1 in vocabs[cat1].values():
                for word1 in rhyme_group1:
                    for rhyme_group2 in vocabs[cat2].values():
                        for word2 in rhyme_group2:
                            if word1 != word2: # Pastikan kata tidak sama
                                unique_phrases.add(template.format(**{cat1: word1, cat2: word2}))

    print(f"[INFO] Ditemukan {len(unique_phrases)} total frasa unik yang bisa dibuat.")

    # 2. Periksa Kecukupan
    if len(unique_phrases) < 676:
        print(f"\n[ERROR] Kosakata tidak cukup! Hanya bisa membuat {len(unique_phrases)} frasa unik, butuh 676.")
        return

    # 3. Acak dan Tugaskan
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bigrams = [a + b for a in alphabet for b in alphabet]
    
    shuffled_phrases = list(unique_phrases)
    random.shuffle(shuffled_phrases)
    
    word_to_rhyme = {}
    for cat_data in vocabs.values():
        for rhyme, words in cat_data.items():
            for word in words:
                word_to_rhyme[word] = rhyme

    dictionary = {}
    for i, bigram in enumerate(bigrams):
        phrase = shuffled_phrases[i]
        last_word = phrase.split()[-1]
        rhyme_key = word_to_rhyme.get(last_word, "unk") # default 'unk' jika kata tidak ditemukan
        
        dictionary[bigram] = {"phrase": phrase, "rhyme_key": rhyme_key}

    print("[INFO] Berhasil menugaskan frasa unik ke 676 bigram.")

    # Simpan ke file
    codebook = {"metadata":{"name":"Parikan Jowo Final (Unik & Terjamin)","language":"Javanese","type":"parikan_4_baris","chunk_size":2},"dictionary":dictionary}
    output_filename = os.path.join("data", "parikan_jowo_final.json")

    print(f"[INFO] Menyimpan hasil ke file '{output_filename}'...")
    with open(output_filename, "w", encoding='utf-8') as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)
    
    print(f"\n--- ✅ SUKSES! File '{output_filename}' berhasil dibuat. ---")

if __name__ == '__main__':
    try:
        generate_final_codebook()
    except Exception as e:
        print(f"\n[FATAL ERROR] Terjadi kesalahan: {e}")