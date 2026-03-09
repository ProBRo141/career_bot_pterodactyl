MIN_LENGTH = 10
CLARIFY_TEMPLATES = {
    "age": "Напиши только число. Ответь так: 25",
    "city": "Ответь так: Москва UTC+3",
    "interests": "Ответь так: программирование, психология, маркетинг",
    "dislikes": "Ответь так: бухгалтерия, холодные звонки, рутина",
    "skills": "Ответь так: Python, Excel, презентации, работа в команде, аналитика",
    "experience": "Ответь так: продажи в магазине, вожатый в лагере, курсовой проект",
    "limits": "Ответь так: мало времени, нужен доход, помогаю семье",
    "work_format": "Ответь так: 3 5 4 1 2",
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
