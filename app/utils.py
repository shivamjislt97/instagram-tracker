import hashlib
import requests
from pathlib import Path

def text_hash(text: str):
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def image_hash(image_bytes: bytes):
    return hashlib.sha256(image_bytes).hexdigest()

def download_image(url, save_path):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(r.content)
    return r.content
