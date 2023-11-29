import pyzipper
from tqdm import tqdm
import zipfile

wordlist_path = input("Masukkan Direktori Password: ")
zip_file_path = input("Masukkan Direktori File Zip: ")

# Buka file Zip dengan enkripsi AES
with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
    # Hitung total kata sandi pada wordlist
    n_words = len(list(open(wordlist_path, "rb")))
    print("Total passwords to test: ", n_words)

    # Baca wordlist dan coba setiap kata sandi
    with open(wordlist_path, "rb") as wordlist:
        for word in tqdm(wordlist, total=n_words, unit="word", desc="Testing Passwords"):
            password = word.strip()
            try:
                # Coba ekstraksi file Zip dengan kata sandi
                zip_file.extractall(pwd=password)
            except (zipfile.BadZipFile, RuntimeError) as e:
                if "password required" in str(e).lower():
                    tqdm.write(f"[-] Kata sandi salah: {password.decode()}")
                else:
                    tqdm.write(f"[-] Kesalahan ekstraksi: {e}")
            except Exception as e:
                tqdm.write(f"[-] Kesalahan: {e}")
            else:
                tqdm.write(f"[+] Kata sandi ditemukan: {password.decode()}")
                exit(0)

print("[!] Kata sandi tidak ditemukan. Coba wordlist lainnya.")
