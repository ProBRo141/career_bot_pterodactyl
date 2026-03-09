MIN_LENGTH = 10
CLARIFY_TEMPLATES = {
    "interests": "Слишком коротко. Напиши 3-5 конкретных тем, что интересны (например: программирование, психология, маркетинг).",
    "dislikes": "Нужно минимум 3 пункта. Что точно не нравится?",
    "skills": "Нужно 5 навыков. Перечисли что уже умеешь.",
    "experience": "Опиши подробнее: какие профессии, подработки или проекты пробовал.",
    "limits": "Опиши ограничения: что мешает по деньгам, времени, семье, здоровью?",
    "work_format": "Формат: люди:1 данные:2 техника:3 творчество:4 управление:5 (цифры от 1 до 5, каждое по разу).",
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
    keywords = ["люди", "данные", "техника", "творчество", "управление"]
    t = text.lower()
    if not all(kw in t for kw in keywords):
        return False
    nums = [int(m) for m in re.findall(r"\b([1-5])\b", t)]
    return len(nums) == 5 and set(nums) == {1, 2, 3, 4, 5}


def get_clarify_message(key: str) -> str | None:
    return CLARIFY_TEMPLATES.get(key)
