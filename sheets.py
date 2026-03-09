import logging
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


def get_client(creds_path: str):
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    return gspread.authorize(creds)


def ensure_headers(sh, sheet_name="Лист1"):
    try:
        ws = sh.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(sheet_name, 1, 20)
    row1 = ws.row_values(1)
    if not row1 or row1[0] != "timestamp":
        headers = [
            "timestamp", "telegram_username", "telegram_id", "age", "city", "education",
            "hours", "interests", "dislikes", "work_format", "skills", "experience",
            "communication", "goal", "limits", "priority", "top_directions", "plan_14_days",
            "ready_for_consultation"
        ]
        ws.update("A1:S1", [headers])
    return ws


def save_result(sheet_id: str, creds_path: str, data: dict):
    try:
        gc = get_client(creds_path)
        sh = gc.open_by_key(sheet_id)
        ws = ensure_headers(sh)
        row = [
            data.get("timestamp", datetime.utcnow().isoformat()),
            data.get("telegram_username", ""),
            data.get("telegram_id", ""),
            data.get("age", ""),
            data.get("city", ""),
            data.get("education", ""),
            data.get("hours", ""),
            data.get("interests", ""),
            data.get("dislikes", ""),
            data.get("work_format", ""),
            data.get("skills", ""),
            data.get("experience", ""),
            data.get("communication", ""),
            data.get("goal", ""),
            data.get("limits", ""),
            data.get("priority", ""),
            data.get("top_directions", ""),
            data.get("plan_14_days", ""),
            data.get("ready_for_consultation", "нет"),
        ]
        ws.append_row(row)
        return True
    except Exception as e:
        logger.exception("Sheets save error: %s", e)
        return False
