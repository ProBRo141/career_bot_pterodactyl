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
# Прокси для доступа к api.telegram.org (если заблокирован на хостинге)
# По умолчанию — публичный SOCKS5 (для РФ/заблокированных хостингов).
# Чтобы отключить: PROXY= в .env
_PROXY_ENV = os.getenv("PROXY", "").strip()
if _PROXY_ENV:
    PROXY = _PROXY_ENV
elif _PROXY_ENV == "" and "PROXY" in os.environ:
    PROXY = None  # явно отключено
else:
    PROXY = "socks5://116.202.8.27:1080"  # fallback для заблокированных хостингов
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or "https://ollama.com"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL") or "gpt-oss:20b"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE") or str(BASE / "credentials.json")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
