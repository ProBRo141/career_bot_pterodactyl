# Профориентационный бот — полная инструкция по установке

Телеграм-бот для профориентации: проводит анкету, выдаёт конкретные профессии с рекомендациями, рисками, ссылками на обучение и планом на 14 дней. Использует **Ollama** (локальные LLM).

---

## Что нужно заранее

- **Аккаунт Telegram** — чтобы создать бота
- **Ollama** — установленная и запущенная (на том же сервере или удалённо)
- **Сервер** — VPS, хостинг или панель Pterodactyl (с доступом к Ollama)
- **Google аккаунт** — опционально, для сохранения в таблицу

---

## 1. Характеристики сервера

Для бота: минимум 512 МБ RAM, 1 ГБ диск.

Для **Ollama** (если крутится на том же сервере): нужно больше ресурсов. Рекомендуется:
- **CPU:** 2+ ядра
- **RAM:** 4–8 ГБ (для llama3.2 или gemma)
- **Диск:** 5–10 ГБ (модели 2–7 ГБ)

Если Ollama на другом сервере — укажи `OLLAMA_BASE_URL` в `.env`.

---

## 2. Создание бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram.
2. Команда `/newbot` → придумай имя и username (например `@MyCareerBot`).
3. Сохрани **токен** вида `7123456789:AAH...`.

---

## 3. Установка Ollama

### Локально (Windows / macOS / Linux)

1. Скачай [Ollama](https://ollama.com/download).
2. Установи и запусти.
3. Скачай модель: `ollama pull llama3.2` (или `gemma3`, `qwen2.5` и т.п.).

### На Linux-сервере

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve   # или как systemd-сервис
ollama pull llama3.2
```

Документация: [docs.ollama.com](https://docs.ollama.com).

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
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Если Ollama на другом хосте: `OLLAMA_BASE_URL=http://192.168.1.10:11434`.

**Шаг 5.** Запусти сервер. Убедись, что Ollama доступна по `OLLAMA_BASE_URL`.

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
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Запуск:

```bash
python app.py
```

Или через systemd — см. раздел «Автозапуск» в полной инструкции ниже.

---

### Вариант C: Локально (Windows / Linux)

1. Установи [Python 3.11+](https://www.python.org/downloads/) и [Ollama](https://ollama.com).
2. `ollama pull llama3.2`
3. Скачай проект, создай `.env` с `TELEGRAM_BOT_TOKEN` и `OLLAMA_BASE_URL=http://localhost:11434`.
4. `pip install -r requirements.txt` и `python app.py`.

---

## 5. Переменные окружения (.env)

| Переменная         | Обязательно | Описание                             |
|--------------------|-------------|--------------------------------------|
| TELEGRAM_BOT_TOKEN | Да          | Токен от @BotFather                  |
| OLLAMA_BASE_URL    | Нет         | URL Ollama (по умолчанию `http://localhost:11434`) |
| OLLAMA_MODEL       | Нет         | Модель (`llama3.2`, `gemma3`, `qwen2.5` и др.) |
| GOOGLE_SHEET_ID    | Нет         | ID таблицы Google Sheets             |
| GOOGLE_CREDENTIALS_FILE | Нет   | Путь к `credentials.json`            |

---

## 6. Ошибки и решения

### «Ошибка генерации»

- Ollama запущена? `curl http://localhost:11434/api/tags`
- Модель скачана? `ollama list`
- `OLLAMA_BASE_URL` и `OLLAMA_MODEL` заданы верно?

### Бот не стартует

- Проверь `TELEGRAM_BOT_TOKEN`.
- Логи: `bot.log` или вывод консоли.

---

## 7. Краткий чеклист

1. Установи Ollama, `ollama pull llama3.2`
2. Создай бота в BotFather → `TELEGRAM_BOT_TOKEN`
3. `.env`: `TELEGRAM_BOT_TOKEN`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
4. `pip install -r requirements.txt` и `python app.py`
5. Напиши боту в Telegram
