"""Penguinet is the server handling file uploads and key storage."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from flask import Flask, request

app = Flask(__name__)

UPLOAD_FOLDER = Path("/data/uploads")
KEY_FOLDER = Path("/data/keys")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
KEY_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file() -> tuple[Literal["No file"], Literal[400]] | tuple[str, Literal[200]]:
    """Handle file uploads."""
    file = request.files.get("file")
    if not file:
        return "No file", 400
    filename = file.filename
    path = UPLOAD_FOLDER / filename
    file.save(path)
    return f"Received {filename}", 200

@app.route("/key", methods=["POST"])
def receive_key() -> tuple[str, Literal[200]]:
    """Receive and store a key."""
    content = request.get_data()
    client_id = request.headers.get("Client-ID", "unknown")
    path = KEY_FOLDER / f"{client_id}.key"
    with Path(path).open("wb") as f:
        f.write(content)
    return f"Key stored for {client_id}", 200

app.run(host="0.0.0.0", port=5000) #noqa: S104
