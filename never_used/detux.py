"""Don't ever user this code, we're not Santa."""
import logging
import os
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KEY_FILE = os.getenv("KEY_FILE", "/keys/aes_key_client.key")
TARGET_DIR = os.getenv("TARGET_DIR", "/data")

def load_key(path: str) -> bytes:
    """Load the AES key from a file."""
    with Path(path).open("rb") as f:
        return f.read()

def decrypt_file(path: Path, aesgcm) -> None:
    """Decrypt a file using AES-GCM."""
    try:
        if path.name in EXCLUDED_FILES:
            logger.info("Fichier exclu : %s", path)
            return
        with path.open("rb") as f:
            data = f.read()
        min_size = 12
        if len(data) < min_size:
            logger.warning("File too short, ignored: %s", path)
            return
        nonce = data[:12]
        ct = data[12:]
        decrypted = aesgcm.decrypt(nonce, ct, None)
        with path.open("wb") as f:
            f.write(decrypted)
        logger.info("Decrypted %s", path)
    except InvalidTag:
        logger.exception("Incorrect key for %s", path)
    except Exception:
        logger.exception("Unexpected error for %s.", path)

EXCLUDED_FILES = {"tux_msg.png"}

def main() -> None:
    """Launch the decryption process."""
    key = load_key(KEY_FILE)
    aesgcm = AESGCM(key)
    files = [f for f in Path(TARGET_DIR).rglob("*") if f.is_file()]
    for f in files:
        if f.name in EXCLUDED_FILES:
            logger.info("Fichier exclu : %s", f)
            continue
        decrypt_file(f, aesgcm)

if __name__ == "__main__":
    main()
