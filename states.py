from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    age = State()
    city = State()
    education = State()
    hours = State()
    interests = State()
    dislikes = State()
    work_format = State()
    skills = State()
    experience = State()
    communication = State()
    goal = State()
    limits = State()
    priority = State()
    consultation_ready = State()
    phone = State()
    done = State()
