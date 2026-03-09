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
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL")  # Опционально: GigaChat, GigaChat-2, GigaChat-2-Pro
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE") or str(BASE / "credentials.json")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
