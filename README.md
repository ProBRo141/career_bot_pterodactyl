# Профориентационный бот (Pterodactyl)

Запуск в Pterodactyl Panel на яйце "Python Generic".

## Вариант 1: Git-репозиторий

1. Залей проект в GitHub/GitLab
2. В панели создай сервер на яйце "python generic"
3. В переменных сервера задай:
   - **Git Repo Address** — `https://github.com/твой_юзер/career_bot_pterodactyl`
   - **User Uploaded Files** — `0`
   - **App py file** — `app.py`
   - **Requirements file** — `requirements.txt`

4. Создай `.env` в корне (File Manager):
   - `TELEGRAM_BOT_TOKEN` — @BotFather
   - `GIGACHAT_CREDENTIALS` — ключ с developers.sber.ru (для РФ, бесплатно)
   - или `GROQ_API_KEY` — если сервер не в РФ
   - `GOOGLE_SHEET_ID` — опционально

5. GigaChat: developers.sber.ru → GigaChat API → Получить ключ

6. Google Sheets — залей `credentials.json` в корень. Запусти сервер

## Вариант 2: Ручная загрузка файлов

1. В переменных сервера задай **User Uploaded Files** = `1`
2. Через File Manager залей все файлы в `/home/container`
3. Создай папку `.git` в контейнере (иначе при старте яйцо может склонировать дефолтный репо и затереть файлы)
4. Добавь Startup Variables (см. выше)
5. Установи **App py file** = `app.py`
6. При первом запуске панель выполнит `pip install -r requirements.txt`

## Переменные (.env)

| Переменная | Описание |
|------------|----------|
| TELEGRAM_BOT_TOKEN | @BotFather (обязательно) |
| GIGACHAT_CREDENTIALS | Ключ GigaChat, developers.sber.ru — для РФ |
| GROQ_API_KEY | Groq (блокирует РФ) |
| GOOGLE_SHEET_ID | ID таблицы |

## Файлы

- `app.py` — точка входа (PY_FILE=app.py)
- `bot.py` — логика бота
- `requirements.txt` — зависимости
- `credentials.json` — Google API (загрузить вручную при использовании Sheets)
