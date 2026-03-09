# Профориентационный бот — полная инструкция по установке

Телеграм-бот для профориентации: проводит анкету из 13 вопросов, выдаёт 3–5 направлений с рекомендациями, рисками и планом на 14 дней. Использует GigaChat API.

---

## Что нужно заранее

- **Аккаунт Telegram** — чтобы создать бота
- **GigaChat** — бесплатный ключ с developers.sber.ru (для России)
- **Сервер** — VPS, хостинг или панель Pterodactyl
- **Google аккаунт** — опционально, для сохранения в таблицу

---

## 1. Характеристики сервера

Бот лёгкий. Минимум:

- **CPU:** 1 ядро
- **RAM:** 512 МБ (лучше 1 ГБ)
- **Диск:** 2–3 ГБ
- **ОС:** Linux (Ubuntu 20.04/22.04, Debian 11+)

Для Pterodactyl обычно хватает выделения 512 МБ RAM и 1 ГБ места. Для VPS — минимальный тариф ($3–5/мес).

---

## 2. Создание бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram.
2. Команда `/newbot` → придумай имя и username (например `@MyCareerBot`).
3. Сохрани **токен** вида `7123456789:AAH...`.

---

## 3. Получение ключа GigaChat

1. Зайди на [developers.sber.ru](https://developers.sber.ru/).
2. Войди через Сбер ID (или создай).
3. **Продукты** → **GigaChat API** → **Получить API-ключ**.
4. Согласись с условиями и скопируй ключ (длинная строка).

GigaChat даёт бесплатные запросы для разработки. Ограничения смотри в личном кабинете.

---

## 4. Варианты установки

### Вариант A: Pterodactyl Panel (готовое хостинг-решение)

Подходит, если бот крутится на панели с яйцом Python (например Nitrado, FreeHost, свои панели).

**Шаг 1.** Залей проект на GitHub:

- Сделай форк [репозитория](https://github.com/ProBRo141/career_bot_pterodactyl) или загрузи файлы в свой репозиторий.

**Шаг 2.** Создай сервер в панели:

- Яйцо: **Python Generic** (или аналог для Python).
- Версия Python: **3.11** или **3.12**.

**Шаг 3.** Переменные окружения сервера:

| Переменная           | Значение                            |
|----------------------|-------------------------------------|
| Git Repo Address     | `https://github.com/твой_юзер/career_bot_pterodactyl` |
| User Uploaded Files  | `0`                                 |
| App py file          | `app.py`                            |
| Requirements file    | `requirements.txt`                  |

**Шаг 4.** Файл `.env` (File Manager → New File):

```
TELEGRAM_BOT_TOKEN=твой_токен_от_BotFather
GIGACHAT_CREDENTIALS=твой_ключ_GigaChat
```

Опционально, если часто бывают 500 от GigaChat:

```
GIGACHAT_MODEL=GigaChat
```

Сохрани `.env` в корень контейнера (рядом с `app.py`).

**Шаг 5.** Запусти сервер. Панель сама выполнит `pip install -r requirements.txt` и запустит `app.py`.

---

### Вариант B: Свой VPS (Linux)

Полный контроль. Сервер в DigitalOcean, Timeweb, Reg.ru и т.п.

**Шаг 1.** Подключись по SSH:

```bash
ssh root@твой_ip
```

**Шаг 2.** Установи Python и зависимости:

```bash
apt update
apt install -y python3 python3-pip python3-venv git
```

**Шаг 3.** Клонируй проект:

```bash
cd /opt
git clone https://github.com/ProBRo141/career_bot_pterodactyl.git
cd career_bot_pterodactyl
```

**Шаг 4.** Создай виртуальное окружение и установи зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Шаг 5.** Создай `.env`:

```bash
nano .env
```

Вставь:

```
TELEGRAM_BOT_TOKEN=твой_токен
GIGACHAT_CREDENTIALS=твой_ключ_gigachat
```

Сохрани (Ctrl+O, Enter, Ctrl+X).

**Шаг 6.** Запуск (для проверки):

```bash
python app.py
```

Если всё ок — останови (Ctrl+C) и настрой автозапуск через systemd.

**Шаг 7.** Создай службу:

```bash
nano /etc/systemd/system/career_bot.service
```

Содержимое:

```ini
[Unit]
Description=Career Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/career_bot_pterodactyl
ExecStart=/opt/career_bot_pterodactyl/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Включи и запусти:

```bash
systemctl daemon-reload
systemctl enable career_bot
systemctl start career_bot
systemctl status career_bot
```

Логи:

```bash
journalctl -u career_bot -f
```

---

### Вариант C: Локально (Windows / Linux для теста)

1. Установи [Python 3.11+](https://www.python.org/downloads/).
2. Скачай проект (ZIP или `git clone`).
3. В папке проекта открой терминал:

```bash
pip install -r requirements.txt
```

4. Создай файл `.env` с `TELEGRAM_BOT_TOKEN` и `GIGACHAT_CREDENTIALS`.
5. Запуск:

```bash
python app.py
```

Пока терминал открыт, бот работает.

---

## 5. Google Sheets (опционально)

Чтобы сохранять результаты в таблицу:

1. Создай проект в [Google Cloud Console](https://console.cloud.google.com/).
2. Включи **Google Sheets API**.
3. Создай **Service Account** → Credentials → Create Service Account.
4. Скачай JSON-ключ и переименуй в `credentials.json`.
5. Положи `credentials.json` в корень проекта.
6. Создай таблицу Google Sheets и скопируй ID из URL (длинная строка между `/d/` и `/edit`).
7. В `.env` добавь:

```
GOOGLE_SHEET_ID=id_таблицы
```

Или укажи путь к ключу:

```
GOOGLE_CREDENTIALS_FILE=credentials.json
```

7. Выдай доступ: открой таблицу → Поделиться → вставь email из `credentials.json` (Client email) с правами «Редактор».

---

## 6. Переменные окружения (.env)

| Переменная            | Обязательно | Описание                                  |
|-----------------------|-------------|-------------------------------------------|
| TELEGRAM_BOT_TOKEN    | Да          | Токен от @BotFather                       |
| GIGACHAT_CREDENTIALS  | Да (для РФ) | Ключ GigaChat с developers.sber.ru        |
| GIGACHAT_MODEL        | Нет         | Модель: `GigaChat`, `GigaChat-2`, `GigaChat-2-Pro` |
| GOOGLE_SHEET_ID       | Нет         | ID таблицы Google Sheets                  |
| GOOGLE_CREDENTIALS_FILE | Нет      | Путь к `credentials.json` (по умолчанию в корне) |

---

## 7. Ошибки и решения

### GigaChat возвращает 500 (Internal Server Error)

Это ошибка на стороне сервера GigaChat.

Что можно сделать:

- Подождать и повторить запрос.
- В `.env` указать модель вручную: `GIGACHAT_MODEL=GigaChat` (часто стабильнее).
- Проверить статус на [developers.sber.ru](https://developers.sber.ru/).

### Бот «отвечает через раз»

GigaChat бывает перегружен. Бот уже пробует несколько моделей: GigaChat-2 → GigaChat-2-Pro → GigaChat. Если зафиксировать `GIGACHAT_MODEL=GigaChat`, запросы пойдут только к одной модели — иногда это помогает.

### «Ошибка генерации»

Проверь:

- Токен бота в `TELEGRAM_BOT_TOKEN`.
- Ключ GigaChat в `GIGACHAT_CREDENTIALS`.
- Убедись, что ключ GigaChat действителен.

### Бот не стартует

- Проверь логи (в Pterodactyl — консоль; на VPS — `journalctl -u career_bot -f`).
- Убедись, что `.env` в той же папке, что и `app.py`.
- Проверь версию Python: `python --version` (3.11+).

---

## 8. Файлы проекта

| Файл              | Назначение                              |
|-------------------|-----------------------------------------|
| `app.py`          | Точка входа, запуск бота                |
| `bot.py`          | Логика бота, команды, анкета            |
| `keyboards.py`    | Кнопки и меню                           |
| `llm_service.py`  | Работа с GigaChat API                   |
| `questions.py`    | Тексты и варианты вопросов              |
| `validation.py`   | Проверка введённых ответов              |
| `sheets.py`       | Запись в Google Sheets                  |
| `requirements.txt`| Python-зависимости                      |

---

## Краткий чеклист для быстрого старта

1. Токен бота → `TELEGRAM_BOT_TOKEN`
2. Ключ GigaChat → `GIGACHAT_CREDENTIALS`
3. Создать `.env` с этими переменными
4. Запустить `python app.py` или поднять через Pterodactyl / systemd
5. Написать боту в Telegram — проверить работу

Если при установке возникнут вопросы — посмотри логи и раздел «Ошибки и решения» выше.
