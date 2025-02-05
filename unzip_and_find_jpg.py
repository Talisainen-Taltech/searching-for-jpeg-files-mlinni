import os
import zipfile
import sys
import time
import shutil

# Define paths
zip_path = r"folder\path"
extract_folder = r"folder\path"


# Step 1: Unzip the archive
def unzip_file(zip_path, extract_folder):
    if not os.path.exists(extract_folder):  # Create the folder if it doesn't exist
        os.makedirs(extract_folder)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"✅ ZIP fail on lahti pakitud: {extract_folder}")


# Step 2: Find and delete non-JPG files
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


# Step 3: Execute the functions
if __name__ == "__main__":
    if os.path.exists(zip_path):
        unzip_file(zip_path, extract_folder)
        clean_non_jpg(extract_folder)
    else:
        print(f"❌ ZIP faili ei leitud: {zip_path}")