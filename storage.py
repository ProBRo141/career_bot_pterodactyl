import json
import logging
import os
from pathlib import Path
from typing import Any

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

logger = logging.getLogger(__name__)
BASE = Path("/home/container" if os.path.exists("/home/container") else ".")
FILE = BASE / "fsm_state.json"


class JsonStorage(BaseStorage):
    def __init__(self):
        self._data: dict = {}
        self._load()

    def _load(self):
        if FILE.exists():
            try:
                with open(FILE, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception as e:
                logger.warning("Storage load error: %s", e)

    def _save(self):
        try:
            with open(FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False)
        except Exception as e:
            logger.warning("Storage save error: %s", e)

    def _key(self, key: StorageKey) -> str:
        return f"{key.bot_id}:{key.chat_id}:{key.user_id}"

    async def set_state(self, key: StorageKey, state: StateType = None):
        k = self._key(key)
        if k not in self._data:
            self._data[k] = {}
        self._data[k]["state"] = state.state if state else None
        self._save()

    async def get_state(self, key: StorageKey) -> str | None:
        k = self._key(key)
        return self._data.get(k, {}).get("state")

    async def set_data(self, key: StorageKey, data: dict[str, Any]):
        k = self._key(key)
        if k not in self._data:
            self._data[k] = {}
        self._data[k]["data"] = {**self._data[k].get("data", {}), **data}
        self._save()

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        k = self._key(key)
        return self._data.get(k, {}).get("data", {})

    async def close(self):
        pass
