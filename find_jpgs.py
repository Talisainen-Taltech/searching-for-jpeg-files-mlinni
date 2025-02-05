import os
import sys

folder = sys.argv[1]

for entry in os.scandir(folder):
    if entry.is_file():
        try:
            with open(entry.path, 'rb') as f:
                header = f.read(2)
                if header != b'\xff\xd8':
                    print(f"Kustuta mitte-JPG fail: {entry.path}")
                    os.remove(entry.path)
        except Exception as e:
            print(f"Viga {entry.path}: {e}")