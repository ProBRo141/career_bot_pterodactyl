import os
from pathlib import Path

from dotenv import load_dotenv

BASE = Path("/home/container" if os.path.exists("/home/container") else ".")
for p in [BASE / ".env", Path(".env")]:
    if p.exists():
        load_dotenv(p)
        break
else:
    load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL") or "llama3.2"
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE") or str(BASE / "credentials.json")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
