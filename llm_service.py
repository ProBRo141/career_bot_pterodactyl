import json
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты профориентационный аналитик. Анализируешь ответы анкеты и выдаёшь результат СТРОГО в JSON.
Формат ответа - только валидный JSON, без markdown и пояснений:
{
  "top_directions": ["направление1", "направление2", "направление3", "направление4", "направление5"],
  "reasons": {
    "направление1": ["причина1", "причина2", "причина3"],
    "направление2": ["причина1", "причина2", "причина3"],
    ...
  },
  "risks": {
    "направление1": ["риск1", "риск2"],
    ...
  },
  "first_step_24h": {
    "направление1": "конкретный шаг",
    ...
  },
  "plan_14_days": [
    {"day": 1, "task": "описание задачи", "check_result": "как проверить"},
    {"day": 2, "task": "...", "check_result": "..."},
    ...
  ]
}
План: 14 задач по 20-60 мин. Типы: мини-тест, лекция 20 мин + 3 вопроса, микро-портфолио, 3 вакансии с требованиями, короткий проект 1-2ч.
Задачи конкретные и проверяемые."""


LABELS = {
    "age": "Возраст",
    "city": "Город",
    "education": "Образование",
    "hours": "Часов в неделю",
    "interests": "Интересы",
    "dislikes": "Что не нравится",
    "work_format": "Формат работы",
    "skills": "Навыки",
    "experience": "Опыт",
    "communication": "Коммуникация",
    "goal": "Цель на 3 мес",
    "limits": "Ограничения",
    "priority": "Приоритет",
}


def build_context(answers: dict, value_labels: dict = None) -> str:
    parts = []
    for k, v in answers.items():
        if v:
            key_label = LABELS.get(k, k)
            if isinstance(v, str) and value_labels and k in value_labels:
                labels = value_labels[k]
                if "," in v:
                    v = ", ".join(labels.get(p.strip(), p.strip()) for p in v.split(","))
                else:
                    v = labels.get(v, v)
            parts.append(f"{key_label}: {v}")
    return "\n".join(parts)


def parse_llm_response(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        filtered = []
        for line in lines:
            if line.strip() in ("```json", "```"):
                continue
            filtered.append(line)
        text = "\n".join(filtered)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _call_gigachat(credentials: str, user_msg: str) -> dict | None:
    import time
    from gigachat import GigaChat
    from gigachat.models import Chat, Messages, MessagesRole
    from gigachat.exceptions import ServerError

    full_prompt = f"{SYSTEM_PROMPT}\n\n{user_msg}"
    for attempt in range(3):
        try:
            with GigaChat(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS", timeout=90) as client:
                chat = Chat(
                    messages=[Messages(role=MessagesRole.USER, content=full_prompt)],
                    model="GigaChat-2",
                    max_tokens=3000,
                )
                resp = client.chat(chat)
                content = resp.choices[0].message.content
                return parse_llm_response(content)
        except ServerError as e:
            if e.status_code == 500 and attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise


def _call_groq(api_key: str, user_msg: str) -> dict | None:
    from groq import Groq

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.5,
        max_tokens=4000,
    )
    content = resp.choices[0].message.content
    return parse_llm_response(content)


def get_recommendations(answers: dict, api_key: str, value_labels: dict = None, gigachat_creds: str = None) -> dict | None:
    ctx = build_context(answers, value_labels)
    user_msg = f"Ответы анкеты:\n{ctx}\n\nСформируй рекомендации в JSON."
    try:
        if gigachat_creds:
            return _call_gigachat(gigachat_creds, user_msg)
        if api_key:
            return _call_groq(api_key, user_msg)
        logger.error("No LLM credentials: set GIGACHAT_CREDENTIALS or GROQ_API_KEY")
        return None
    except Exception as e:
        logger.exception("LLM error: %s", e)
        return None
