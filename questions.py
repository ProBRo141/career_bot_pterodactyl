EDUCATION = [
    ("school", "Школа"),
    ("college", "СПО/колледж"),
    ("uni", "Вуз"),
    ("after", "После вуза"),
]

HOURS = [
    ("2", "2 часа"),
    ("5", "5 часов"),
    ("10", "10+ часов"),
]

WORK_FORMAT = ["люди", "данные", "техника", "творчество", "управление"]

COMMUNICATION = [
    ("low", "Низкий"),
    ("mid", "Средний"),
    ("high", "Высокий"),
]

GOAL_3M = [
    ("job", "Работа"),
    ("intern", "Стажировка"),
    ("project", "Проект"),
    ("choice", "Выбор направления"),
]

PRIORITY = [
    ("money", "Деньги"),
    ("interest", "Интерес"),
    ("stability", "Стабильность"),
    ("growth", "Рост"),
    ("freedom", "Свобода"),
]

QUESTIONS = {
    "age": ("Сколько тебе лет? Напиши число.", "age", False),
    "city": ("Город и часовой пояс (например: Москва UTC+3)", "city", False),
    "education": ("Уровень образования", "education", True),
    "hours": ("Сколько часов в неделю готов уделять?", "hours", True),
    "interests": ("Какие темы реально интересуют? Напиши 3-5 пунктов.", "interests", False),
    "dislikes": ("Что точно НЕ нравится? Напиши 3 пункта.", "dislikes", False),
    "work_format": ("Ранжируй от 1 до 5 (1 — самый желанный): люди, данные, техника, творчество, управление.\nНапиши 5 цифр через пробел: 3 5 4 1 2", "work_format", False),
    "skills": ("Что уже умеешь? Напиши 5 навыков.", "skills", False),
    "experience": ("Что пробовал из профессий/подработок/проектов?", "experience", False),
    "communication": ("Уровень коммуникации", "communication", True),
    "goal": ("Цель на 3 месяца", "goal", True),
    "limits": ("Ограничения: деньги, время, семья, здоровье — напиши свободно", "limits", False),
    "priority": ("Приоритет (выбери 1-2)", "priority", True),
}

QUESTION_ORDER = [
    "age", "city", "education", "hours", "interests", "dislikes",
    "work_format", "skills", "experience", "communication",
    "goal", "limits", "priority"
]
