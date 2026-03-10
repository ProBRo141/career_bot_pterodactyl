# Профориентационный бот — полная инструкция по установке

Телеграм-бот для профориентации: проводит анкету, выдаёт конкретные профессии с рекомендациями, рисками, ссылками на обучение и планом на 14 дней. Использует **Ollama** (локальные LLM).

---

## Что нужно заранее

- **Аккаунт Telegram** — чтобы создать бота
- **Ollama Cloud** — API-ключ с [ollama.com/settings/keys](https://ollama.com/settings/keys) (не нужна установка)
- **Сервер** — любой VPS или Pterodactyl
- **Google аккаунт** — опционально, для таблицы

---

## 1. Характеристики сервера

Бот использует **Ollama Cloud API** — установка Ollama не нужна. Достаточно:
- **CPU:** 1 ядро
- **RAM:** 512 МБ
- **Диск:** 2 ГБ

---

## 2. Создание бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram.
2. Команда `/newbot` → придумай имя и username (например `@MyCareerBot`).
3. Сохрани **токен** вида `7123456789:AAH...`.

---

## 3. Ключ Ollama Cloud API

1. Зайди на [ollama.com](https://ollama.com) и создай аккаунт.
2. Открой [ollama.com/settings/keys](https://ollama.com/settings/keys).
3. Создай API-ключ и скопируй его.
4. Укажи в `.env`: `OLLAMA_API_KEY=твой_ключ`.

Установка Ollama **не требуется** — используются облачные модели.

---

## 4. Варианты установки бота

### Вариант A: Pterodactyl Panel

**Шаг 1.** Залей проект на GitHub (форк [репозитория](https://github.com/ProBRo141/career_bot_pterodactyl)).

**Шаг 2.** Создай сервер на яйце Python Generic.

**Шаг 3.** Переменные:
- Git Repo Address — URL репо
- App py file — `app.py`
- Requirements file — `requirements.txt`

**Шаг 4.** Файл `.env`:

```
TELEGRAM_BOT_TOKEN=твой_токен
OLLAMA_API_KEY=твой_ключ_с_ollama.com
```

По умолчанию: `OLLAMA_BASE_URL=https://ollama.com`, `OLLAMA_MODEL=gpt-oss:20b`.

**Шаг 5.** Запусти сервер.

---

### Вариант B: Свой VPS (Linux)

```bash
apt update && apt install -y python3 python3-pip python3-venv git
cd /opt
git clone https://github.com/ProBRo141/career_bot_pterodactyl.git
cd career_bot_pterodactyl
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создай `.env`:

```
TELEGRAM_BOT_TOKEN=твой_токен
OLLAMA_API_KEY=ключ_с_ollama.com/settings/keys
```

Запуск:

```bash
python app.py
```

Или через systemd — см. раздел «Автозапуск» в полной инструкции ниже.

---

### Вариант C: Локально (Windows / Linux)

1. Установи [Python 3.11+](https://www.python.org/downloads/).
2. Скачай проект, создай `.env` с `TELEGRAM_BOT_TOKEN` и `OLLAMA_API_KEY`.
3. `pip install -r requirements.txt` и `python app.py`.

---

## 5. Переменные окружения (.env)

| Переменная         | Обязательно | Описание                             |
|--------------------|-------------|--------------------------------------|
| TELEGRAM_BOT_TOKEN | Да          | Токен от @BotFather                  |
| OLLAMA_API_KEY     | Да (облако) | Ключ с [ollama.com/settings/keys](https://ollama.com/settings/keys) |
| OLLAMA_BASE_URL    | Нет         | Облако: `https://ollama.com`. Локально: `http://localhost:11434` |
| OLLAMA_MODEL       | Нет         | Облако: `gpt-oss:20b`, `gpt-oss:120b`. Локально: `llama3.2` и др. |
| GOOGLE_SHEET_ID    | Нет         | ID таблицы Google Sheets             |
| GOOGLE_CREDENTIALS_FILE | Нет   | Путь к `credentials.json`            |

---

## 6. Ошибки и решения

### «Ошибка генерации»

- `OLLAMA_API_KEY` задан и верен (ключ с ollama.com/settings/keys)
- Проверь доступ: `curl -H "Authorization: Bearer $OLLAMA_API_KEY" https://ollama.com/api/tags`

### Бот не стартует

- Проверь `TELEGRAM_BOT_TOKEN`.
- Логи: `bot.log` или вывод консоли.

---

## 7. Краткий чеклист

1. Создай аккаунт на ollama.com → API-ключ в настройках
2. Создай бота в BotFather → `TELEGRAM_BOT_TOKEN`
3. `.env`: `TELEGRAM_BOT_TOKEN`, `OLLAMA_API_KEY`
4. `pip install -r requirements.txt` и `python app.py`
5. Напиши боту в Telegram
