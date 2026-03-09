MIN_LENGTH = 10
CLARIFY_TEMPLATES = {
    "interests": "Слишком коротко. Напиши 3-5 конкретных тем, что интересны (например: программирование, психология, маркетинг).",
    "dislikes": "Нужно минимум 3 пункта. Что точно не нравится?",
    "skills": "Нужно 5 навыков. Перечисли что уже умеешь.",
    "experience": "Опиши подробнее: какие профессии, подработки или проекты пробовал.",
    "limits": "Опиши ограничения: что мешает по деньгам, времени, семье, здоровью?",
    "work_format": "Напиши 5 цифр через пробел или запятую — порядок для: люди, данные, техника, творчество, управление. 1 = самый желанный.\nПример: 3 5 4 1 2",
    "city": "Напиши город и часовой пояс (например: Санкт-Петербург UTC+3).",
}


def is_too_short(key: str, text: str) -> bool:
    if key in ("age", "education", "hours", "communication", "goal", "priority"):
        return False
    if key == "city":
        return len(text.strip()) < 3
    return len(text.strip()) < MIN_LENGTH


def validate_work_format(text: str) -> bool:
    import re
    nums = [int(m) for m in re.findall(r"\b([1-5])\b", text)]
    return len(nums) == 5 and set(nums) == {1, 2, 3, 4, 5}


def normalize_work_format(text: str) -> str:
    import re
    nums = [int(m) for m in re.findall(r"\b([1-5])\b", text)]
    if len(nums) != 5 or set(nums) != {1, 2, 3, 4, 5}:
        return text
    order = ["люди", "данные", "техника", "творчество", "управление"]
    return " ".join(f"{k}:{n}" for k, n in zip(order, nums))


def get_clarify_message(key: str) -> str | None:
    return CLARIFY_TEMPLATES.get(key)
