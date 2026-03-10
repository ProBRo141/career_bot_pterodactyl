from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from questions import EDUCATION, HOURS, COMMUNICATION, GOAL_3M, PRIORITY


def back_kb(step: str | None):
    if not step:
        return None
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад", callback_data=f"back:{step}")]
    ])


def education_kb(step: str):
    btns = [
        [InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")]
        for val, txt in EDUCATION
    ]
    bk = back_kb("city")
    if bk:
        btns.append(bk.inline_keyboard[0])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def hours_kb(step: str):
    btns = [
        [InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")]
        for val, txt in HOURS
    ]
    bk = back_kb("education")
    if bk:
        btns.append(bk.inline_keyboard[0])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def communication_kb(step: str):
    btns = [
        [InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")]
        for val, txt in COMMUNICATION
    ]
    bk = back_kb("experience")
    if bk:
        btns.append(bk.inline_keyboard[0])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def goal_kb(step: str):
    btns = [
        [InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")]
        for val, txt in GOAL_3M
    ]
    bk = back_kb("communication")
    if bk:
        btns.append(bk.inline_keyboard[0])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def priority_kb(step: str):
    btns = []
    for val, txt in PRIORITY:
        btns.append([InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")])
    bk = back_kb("limits")
    if bk:
        btns.append(bk.inline_keyboard[0])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def priority_with_done_kb(step: str):
    btns = []
    for val, txt in PRIORITY:
        btns.append([InlineKeyboardButton(text=txt, callback_data=f"ans:{step}:{val}")])
    btns.append([InlineKeyboardButton(text="Готово", callback_data="ans:priority:done")])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def consultation_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="ans:consultation:yes")],
        [InlineKeyboardButton(text="Нет", callback_data="ans:consultation:no")],
        [InlineKeyboardButton(text="← Назад", callback_data="back:consultation")],
    ])


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Старт"), KeyboardButton(text="🔄 Перезапуск")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="📋 Мой результат")],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def back_map():
    return {
        "city": "age",
        "education": "city",
        "consultation": "priority",
        "phone": "consultation",
        "hours": "education",
        "interests": "hours",
        "dislikes": "interests",
        "work_format": "dislikes",
        "skills": "work_format",
        "experience": "skills",
        "communication": "experience",
        "goal": "communication",
        "limits": "goal",
        "priority": "limits",
    }


def label_map():
    return {
        "education": dict(EDUCATION),
        "hours": dict(HOURS),
        "communication": dict(COMMUNICATION),
        "goal": dict(GOAL_3M),
        "priority": dict(PRIORITY),
    }
