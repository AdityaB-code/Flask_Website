import os
import zipfile
import requests
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Config ===
SOURCE_FOLDER = Path(r"E:")
UPLOAD_URL = "http://192.168.231.21:5000/upload_zip"
BATCH_SIZE = 20

# === Find all image files ===
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"]

def find_images(source_folder):
    return [f for f in source_folder.rglob("*") if f.suffix.lower() in IMAGE_EXTS]

# === Zip and upload ===
def zip_and_upload(batch, batch_index):
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=f"_batch_{batch_index}.zip")
    zip_path = temp_zip.name
    temp_zip.close()

    try:
        # Create zip
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in batch:
                arcname = file.relative_to(SOURCE_FOLDER)
                zipf.write(file, arcname)

        # Upload
        with open(zip_path, 'rb') as f:
            files = {'file': (os.path.basename(zip_path), f)}
            requests.post(UPLOAD_URL, files=files)

    except Exception:
        pass  # Silently ignore errors

    finally:
        os.remove(zip_path)

# === Main logic ===
def main():
    images = find_images(SOURCE_FOLDER)
    batches = [images[i:i+BATCH_SIZE] for i in range(0, len(images), BATCH_SIZE)]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(zip_and_upload, batch, idx) for idx, batch in enumerate(batches)]
        for _ in as_completed(futures):
            pass

if __name__ == "__main__":
    main()
