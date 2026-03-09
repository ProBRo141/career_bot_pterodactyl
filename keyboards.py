from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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


def back_map():
    return {
        "city": "age",
        "education": "city",
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
