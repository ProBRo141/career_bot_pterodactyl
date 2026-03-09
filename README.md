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

4. Добавь Startup Variables:
   - `TELEGRAM_BOT_TOKEN` — токен от @BotFather
   - `GROQ_API_KEY` — ключ с console.groq.com
   - `GOOGLE_SHEET_ID` — ID таблицы (по желанию)
   - `GOOGLE_CREDENTIALS_FILE` — `credentials.json` (по желанию)

5. Если используешь Google Sheets — залей `credentials.json` через File Manager
6. Запусти сервер

## Вариант 2: Ручная загрузка файлов

1. В переменных сервера задай **User Uploaded Files** = `1`
2. Через File Manager залей все файлы в `/home/container`
3. Создай папку `.git` в контейнере (иначе при старте яйцо может склонировать дефолтный репо и затереть файлы)
4. Добавь Startup Variables (см. выше)
5. Установи **App py file** = `app.py`
6. При первом запуске панель выполнит `pip install -r requirements.txt`

## Переменные окружения (Startup Variables)

| Переменная | Обязательно | Описание |
|------------|-------------|----------|
| TELEGRAM_BOT_TOKEN | да | Токен от @BotFather |
| GROQ_API_KEY | да | API-ключ Groq |
| GOOGLE_SHEET_ID | нет | ID таблицы Sheets |
| GOOGLE_CREDENTIALS_FILE | нет | Путь к credentials.json (по умолчанию credentials.json) |

## Файлы

- `app.py` — точка входа (PY_FILE=app.py)
- `bot.py` — логика бота
- `requirements.txt` — зависимости
- `credentials.json` — Google API (загрузить вручную при использовании Sheets)
