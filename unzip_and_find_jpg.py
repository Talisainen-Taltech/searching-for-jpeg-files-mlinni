import os
import zipfile
import requests
import time
import shutil

# Define URLs and paths
url = "https://upload.itcollege.ee/~aleksei/random_files_without_extension.zip"
download_path = r"C:\Users\marko\Downloads\random_files_without_extension.zip"
extract_folder = r"C:\Users\marko\Downloads\random_files_without_extension"


# Step 1: Download the ZIP file
def download_zip(url, save_path):
    print(f"📥 Laen alla ZIP faili: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"✅ ZIP fail alla laetud: {save_path}")
    else:
        print(f"❌ Viga allalaadimisel: {response.status_code}")


# Step 2: Extract the ZIP file
def unzip_file(zip_path, extract_folder):
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"✅ ZIP fail lahti pakitud: {extract_folder}")


# Step 3: Find and delete non-JPG files
def clean_non_jpg(folder):
    for entry in os.scandir(folder):
        if entry.is_file():
            try:
                with open(entry.path, 'rb') as f:
                    header = f.read(2)
                    if header != b'\xff\xd8':  # JPG header check
                        print(f"❌ Kustutan mitte-JPG faili: {entry.path}")
                        try:
                            os.remove(entry.path)
                        except PermissionError:
                            print(f"⚠ Fail on lukustatud, ootan 5 sekundit: {entry.path}")
                            time.sleep(5)
                            try:
                                os.remove(entry.path)
                            except Exception as e:
                                print(f"🚫 Ei saanud kustutada {entry.path}: {e}")
            except PermissionError:
                print(f"⚠ Ei saa lugeda faili, see on kasutuses: {entry.path}")
            except Exception as e:
                print(f"❗ Viga {entry.path}: {e}")


# Step 4: Execute the script
if __name__ == "__main__":
    download_zip(url, download_path)
    unzip_file(download_path, extract_folder)
    clean_non_jpg(extract_folder)
