import pyzipper
from tqdm import tqdm
import zipfile
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures



def try_password(password, zip_file):
    try:
        zip_file.extractall(pwd=password)
        return password
    except (zipfile.BadZipFile, RuntimeError) as e:
        if "password required" in str(e).lower():
            tqdm.write(f"[-] Kata sandi salah: {password.decode()}")
        else:
            tqdm.write(f"[-] Kesalahan ekstraksi: {e}")
    except Exception as e:
        tqdm.write(f"[-] Kesalahan: {e}")
    return None

def main():
    wordlist_path = input("Masukkan Direktori Password: ")
    zip_file_path = input("Masukkan Direktori File Zip: ")

    with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
        n_words = len(list(open(wordlist_path, "rb")))
        print("Total passwords to test: ", n_words)

        with open(wordlist_path, "rb") as wordlist:
            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor() as executor:
                # Submit tasks for each password
                futures = [executor.submit(try_password, word.strip(), zip_file) for word in wordlist]

                # Iterate over completed tasks
                for future in tqdm(concurrent.futures.as_completed(futures), total=n_words, unit="word", desc="Testing Passwords"):
                    result = future.result()
                    if result:
                        tqdm.write(f"[+] Kata sandi ditemukan: {result.decode()}")
                        exit(0)

    print("[!] Kata sandi tidak ditemukan. Coba wordlist lainnya.")

if __name__ == "__main__":
    main()
