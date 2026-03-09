import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import TELEGRAM_TOKEN, GROQ_API_KEY, GIGACHAT_CREDENTIALS, CREDENTIALS_FILE, SHEET_ID
from states import Form
from questions import QUESTIONS, QUESTION_ORDER
from keyboards import (
    education_kb, hours_kb, communication_kb, goal_kb, priority_kb,
    back_map, label_map,
)
from validation import is_too_short, get_clarify_message, validate_work_format, normalize_work_format
from llm_service import get_recommendations
from sheets import save_result as save_to_sheets
from results_store import save_result as save_to_store, get_last_result
from storage import JsonStorage

import os as _os
_log_path = "/home/container/bot.log" if _os.path.exists("/home/container") else "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_path, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=JsonStorage())

STATE_MAP = {
    "age": Form.age,
    "city": Form.city,
    "education": Form.education,
    "hours": Form.hours,
    "interests": Form.interests,
    "dislikes": Form.dislikes,
    "work_format": Form.work_format,
    "skills": Form.skills,
    "experience": Form.experience,
    "communication": Form.communication,
    "goal": Form.goal,
    "limits": Form.limits,
    "priority": Form.priority,
}

KEYBOARD_MAP = {
    "education": education_kb,
    "hours": hours_kb,
    "communication": communication_kb,
    "goal": goal_kb,
    "priority": priority_kb,
}


async def ask_question(chat_id: int, step: str, ctx: FSMContext):
    text, key, has_kb = QUESTIONS[step]
    kb = KEYBOARD_MAP.get(step)
    state = STATE_MAP.get(step)
    if state:
        await ctx.set_state(state)
    if kb:
        await bot.send_message(chat_id, text, reply_markup=kb(key))
    else:
        back_map_dict = back_map()
        prev = back_map_dict.get(step)
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← Назад", callback_data=f"back:{prev}")]
        ]) if prev else None
        await bot.send_message(chat_id, text, reply_markup=markup)


def format_result(rec: dict, answers: dict) -> str:
    labels = label_map()
    top = rec.get("top_directions", [])[:5]
    reasons = rec.get("reasons", {})
    risks = rec.get("risks", {})
    first = rec.get("first_step_24h", {})
    plan = rec.get("plan_14_days", [])

    parts = ["*РЕКОМЕНДАЦИИ*\n"]
    for i, d in enumerate(top, 1):
        parts.append(f"*{i}. {d}*")
        for r in reasons.get(d, [])[:3]:
            parts.append(f"  • {r}")
        for r in risks.get(d, [])[:2]:
            parts.append(f"  ⚠ {r}")
        fs = first.get(d, "")
        if fs:
            parts.append(f"  Первый шаг за 24ч: {fs}")
        parts.append("")

    parts.append("*ПЛАН НА 14 ДНЕЙ*\n")
    for p in plan[:14]:
        day = p.get("day", "?")
        task = p.get("task", "")
        check = p.get("check_result", "")
        parts.append(f"День {day}: {task}")
        if check:
            parts.append(f"  Проверка: {check}")
        parts.append("")

    return "\n".join(parts)


async def send_result_and_save(msg: Message, ctx: FSMContext, rec: dict):
    data = await ctx.get_data()
    answers = {k: v for k, v in data.items() if k in QUESTION_ORDER}
    labels = label_map()
    display = {}
    for k, v in answers.items():
        if k in labels and isinstance(v, str):
            display[k] = labels[k].get(v, v)
        else:
            display[k] = v

    reasons = rec.get("reasons", {})
    risks = rec.get("risks", {})
    first = rec.get("first_step_24h", {})
    top_lines = []
    for i, d in enumerate(rec.get("top_directions", [])[:5], 1):
        r = "; ".join(reasons.get(d, [])[:3])
        k = "; ".join(risks.get(d, [])[:2])
        fs = first.get(d, "")
        line = f"{i}. {d}"
        if r:
            line += f"\n   Причины: {r}"
        if k:
            line += f"\n   Риски: {k}"
        if fs:
            line += f"\n   Шаг 24ч: {fs}"
        top_lines.append(line)
    top_str = "\n\n".join(top_lines)

    plan_parts = []
    for p in rec.get("plan_14_days", [])[:14]:
        day = p.get("day", "?")
        task = p.get("task", "")
        check = p.get("check_result", "")
        s = f"День {day}: {task}"
        if check:
            s += f"\n   ✓ {check}"
        plan_parts.append(s)
    plan_str = "\n\n".join(plan_parts)

    ts = datetime.utcnow()
    ts_str = ts.strftime("%d.%m.%Y %H:%M")

    row = {
        "timestamp": ts_str,
        "telegram_username": f"@{msg.from_user.username}" if msg.from_user.username else str(msg.from_user.id),
        "telegram_id": msg.from_user.id,
        **{k: str(v) for k, v in display.items()},
        "top_directions": top_str,
        "plan_14_days": plan_str,
        "ready_for_consultation": "да",
    }

    if SHEET_ID and CREDENTIALS_FILE:
        try:
            save_to_sheets(SHEET_ID, CREDENTIALS_FILE, row)
        except Exception as e:
            logger.error("Sheets save: %s", e)

    result_for_store = {
        "answers": display,
        "recommendations": rec,
        "timestamp": datetime.utcnow().isoformat(),
    }
    save_to_store(msg.from_user.id, result_for_store)
    await ctx.set_state(Form.done)
    await ctx.clear()

    out = format_result(rec, answers)
    await msg.answer(out, parse_mode="Markdown")


@dp.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Привет! Я помогу с профориентацией. Пройди анкету — получишь рекомендации и план на 14 дней.\n\n"
        "Команды: /restart — заново, /help — помощь, /myresult — последний результат."
    )
    await ask_question(msg.chat.id, "age", state)


@dp.message(Command("restart"))
async def cmd_restart(msg: Message, state: FSMContext):
    await cmd_start(msg, state)


@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(
        "Бот проводит профориентационную диагностику.\n"
        "Отвечай на вопросы — в конце получишь 3-5 направлений, причины, риски, первый шаг и план на 14 дней.\n"
        "Можно нажать «Назад» чтобы вернуться на шаг.\n"
        "/start — начать\n"
        "/restart — начать заново\n"
        "/myresult — показать последний результат"
    )


@dp.message(Command("myresult"))
async def cmd_myresult(msg: Message):
    res = get_last_result(msg.from_user.id)
    if not res:
        await msg.answer("Результатов пока нет. Пройди анкету: /start")
        return
    rec = res.get("recommendations", {})
    answers = res.get("answers", {})
    out = format_result(rec, answers)
    await msg.answer(out, parse_mode="Markdown")


@dp.callback_query(F.data.startswith("back:"))
async def cb_back(cb: CallbackQuery, state: FSMContext):
    step = cb.data.split(":", 1)[1]
    if step not in QUESTION_ORDER:
        await cb.answer()
        return
    idx = QUESTION_ORDER.index(step)
    data = await state.get_data()
    for s in QUESTION_ORDER[idx:]:
        data.pop(s, None)
    await state.set_data(data)
    await ask_question(cb.message.chat.id, step, state)
    await cb.answer()


@dp.callback_query(F.data == "ans:priority:done")
async def cb_priority_done(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur = data.get("priority", "")
    if not cur:
        await cb.answer("Выбери хотя бы один приоритет")
        return
    await cb.message.answer("Генерирую рекомендации...")
    await cb.answer()
    rec = get_recommendations(data, GROQ_API_KEY, label_map(), GIGACHAT_CREDENTIALS)
    if rec:
        await send_result_and_save(cb.message, state, rec)
    else:
        await cb.message.answer("Ошибка генерации. Для РФ используй GIGACHAT_CREDENTIALS (developers.sber.ru). Groq блокирует РФ. /restart")


@dp.callback_query(F.data.startswith("ans:priority:"))
async def cb_priority(cb: CallbackQuery, state: FSMContext):
    val = cb.data.split(":", 2)[2]
    data = await state.get_data()
    cur = data.get("priority", "")
    if isinstance(cur, str) and cur:
        parts = [p.strip() for p in cur.split(",") if p.strip()]
    else:
        parts = []
    if val not in parts:
        parts.append(val)
    if len(parts) > 2:
        parts = parts[-2:]
    await state.update_data(priority=",".join(parts))
    labels = label_map()
    names = [labels.get("priority", {}).get(p, p) for p in parts]
    if len(parts) >= 2:
        await cb.message.answer("Генерирую рекомендации...")
        await cb.answer()
        data = await state.get_data()
        rec = get_recommendations(data, GROQ_API_KEY, label_map(), GIGACHAT_CREDENTIALS)
        if rec:
            await send_result_and_save(cb.message, state, rec)
        else:
            await cb.message.answer("Ошибка генерации. Для РФ: GIGACHAT_CREDENTIALS в .env (developers.sber.ru). Groq блокирует РФ. /restart")
    else:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        ready_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Готово", callback_data="ans:priority:done")]
        ])
        await cb.message.answer(f"Выбрано: {', '.join(names)}. Выбери второй или нажми Готово.", reply_markup=ready_kb)
        await cb.answer()


@dp.callback_query(F.data.startswith("ans:"))
async def cb_ans(cb: CallbackQuery, state: FSMContext):
    _, step, val = cb.data.split(":", 2)
    await state.update_data({step: val})
    idx = QUESTION_ORDER.index(step)
    if idx + 1 >= len(QUESTION_ORDER):
        await cb.message.answer("Генерирую рекомендации...")
        await cb.answer()
        data = await state.get_data()
        rec = get_recommendations(data, GROQ_API_KEY, label_map(), GIGACHAT_CREDENTIALS)
        if rec:
            await send_result_and_save(cb.message, state, rec)
        else:
            await cb.message.answer("Ошибка генерации. Для РФ: GIGACHAT_CREDENTIALS в .env (developers.sber.ru). Groq блокирует РФ. /restart")
        return
    next_step = QUESTION_ORDER[idx + 1]
    await ask_question(cb.message.chat.id, next_step, state)
    await cb.answer()


@dp.message(Form.age, F.text)
async def ans_age(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if not t.isdigit() or int(t) < 10 or int(t) > 100:
        await msg.answer("Формат: 25")
        return
    await state.update_data(age=t)
    await ask_question(msg.chat.id, "city", state)


@dp.message(Form.city, F.text)
async def ans_city(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("city", t):
        await msg.answer(get_clarify_message("city") or "Напиши город и часовой пояс")
        return
    await state.update_data(city=t)
    await ask_question(msg.chat.id, "education", state)


@dp.message(Form.interests, F.text)
async def ans_interests(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("interests", t):
        await msg.answer(get_clarify_message("interests"))
        return
    await state.update_data(interests=t)
    await ask_question(msg.chat.id, "dislikes", state)


@dp.message(Form.dislikes, F.text)
async def ans_dislikes(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("dislikes", t):
        await msg.answer(get_clarify_message("dislikes"))
        return
    await state.update_data(dislikes=t)
    await ask_question(msg.chat.id, "work_format", state)


@dp.message(Form.work_format, F.text)
async def ans_work_format(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if not validate_work_format(t):
        await msg.answer(get_clarify_message("work_format"))
        return
    await state.update_data(work_format=normalize_work_format(t))
    await ask_question(msg.chat.id, "skills", state)


@dp.message(Form.skills, F.text)
async def ans_skills(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("skills", t):
        await msg.answer(get_clarify_message("skills"))
        return
    await state.update_data(skills=t)
    await ask_question(msg.chat.id, "experience", state)


@dp.message(Form.experience, F.text)
async def ans_experience(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("experience", t):
        await msg.answer(get_clarify_message("experience"))
        return
    await state.update_data(experience=t)
    await ask_question(msg.chat.id, "communication", state)


@dp.message(Form.limits, F.text)
async def ans_limits(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if is_too_short("limits", t):
        await msg.answer(get_clarify_message("limits"))
        return
    await state.update_data(limits=t)
    await ask_question(msg.chat.id, "priority", state)


@dp.message(Form.goal, F.text)
async def ans_goal_text(msg: Message, state: FSMContext):
    await msg.answer("Выбери вариант кнопкой:", reply_markup=goal_kb("goal"))


@dp.message(Form.priority, F.text)
async def ans_priority_text(msg: Message, state: FSMContext):
    await msg.answer("Выбери 1-2 приоритета кнопками:", reply_markup=priority_kb("priority"))


async def main():
    if not TELEGRAM_TOKEN:
        logger.error("Set TELEGRAM_BOT_TOKEN in .env")
        return
    if not GIGACHAT_CREDENTIALS and not GROQ_API_KEY:
        logger.error("Set GIGACHAT_CREDENTIALS (для РФ) или GROQ_API_KEY в .env")
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Fatal: %s", e)
