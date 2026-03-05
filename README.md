# 🌸 8 Марта Бот — ДУМД

Telegram бот с поздравлением, викториной и красивым Mini App пригласительным.

---

## 📁 Структура проекта

```
march8bot/
├── bot.py              # основной код бота
├── requirements.txt    # зависимости
├── .env.example        # шаблон переменных окружения
├── .env                # твои токены (не коммитить!)
└── webapp/
    └── index.html      # Mini App пригласительное (выложить на GitHub Pages)
```

---

## 🚀 Быстрый старт

### Шаг 1 — Создай бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot`
3. Задай имя и username
4. Скопируй токен

---

### Шаг 2 — Выложи Mini App на GitHub Pages

1. Создай новый репозиторий на [github.com](https://github.com), например `march8-invite`
2. Загрузи файл `webapp/index.html` как `index.html`
3. Перейди: **Settings → Pages → Source: Deploy from branch → Branch: main → Save**
4. Подожди 1-2 минуты, получишь ссылку:
   ```
   https://ТВО_ЛОГИН.github.io/march8-invite/
   ```

---

### Шаг 3 — Настрой переменные окружения

```bash
cp .env.example .env
```

Открой `.env` и заполни:
```
BOT_TOKEN=123456789:ABCdef...    ← токен от BotFather
WEBAPP_URL=https://твой-логин.github.io/march8-invite/
```

---

### Шаг 4 — Установи зависимости и запусти

```bash
# Создай виртуальное окружение (рекомендуется)
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Установи зависимости
pip install -r requirements.txt

# Запусти бота
python bot.py
```

---

## 🌐 Деплой на Railway (постоянная работа)

1. Зайди на [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Выбери репозиторий с `bot.py`
3. В разделе **Variables** добавь:
   - `BOT_TOKEN` = твой токен
   - `WEBAPP_URL` = ссылка на GitHub Pages
4. Deploy → готово!

---

## 🎯 Что умеет бот

| Шаг | Что происходит |
|-----|----------------|
| `/start` | Выбор языка 🇷🇺 / 🇰🇿 |
| После выбора | Красивое поздравление ДУМД |
| Кнопка "Начать викторину" | 5 вопросов про весну и настроение |
| После 5 вопросов | Персональный результат + кнопка приза |
| Кнопка приза | Открывается Mini App пригласительное |

---

## ✏️ Как поменять детали мероприятия

В файле `webapp/index.html` найди блоки `info-block` и поменяй:
- `17:00 — ...∞` → твоё время
- `Переговорная «Весна»` → твоё место

В файле `bot.py` можно поменять:
- Вопросы викторины → `QUIZ_QUESTIONS`
- Тексты поздравлений → `TEXTS`
