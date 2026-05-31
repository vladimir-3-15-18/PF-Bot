# 🏦 Бот-эксперт по проектному финансированию

Telegram-бот на базе Claude, обученный на лучших практиках проектного финансирования и кредитования.

---

## 🚀 Деплой на Railway (рекомендуется, бесплатно)

### Шаг 1 — Создать Telegram-бота

1. Откройте Telegram, найдите **@BotFather**
2. Отправьте `/newbot`
3. Придумайте имя и username (например `pf_expert_bot`)
4. Скопируйте токен — он выглядит так: `7123456789:AAHdqTg...`

### Шаг 2 — Загрузить код на GitHub

1. Создайте новый репозиторий на [github.com](https://github.com)
2. Загрузите все файлы из этой папки:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `README.md`

### Шаг 3 — Деплой на Railway

1. Зайдите на [railway.app](https://railway.app) → войдите через GitHub
2. Нажмите **New Project** → **Deploy from GitHub repo**
3. Выберите ваш репозиторий
4. Перейдите в **Variables** и добавьте две переменные:

```
ANTHROPIC_API_KEY=sk-ant-...ваш ключ от Anthropic...
TELEGRAM_BOT_TOKEN=7123456789:AAH...ваш токен от BotFather...
```

5. Нажмите **Deploy** — Railway сам установит зависимости и запустит бота

### Где взять ANTHROPIC_API_KEY?

Зайдите на [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key

---

## 🔄 Альтернатива — Render.com

1. Зайдите на [render.com](https://render.com) → New → **Web Service**
2. Подключите GitHub репозиторий
3. Настройки:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
4. В разделе **Environment** добавьте те же две переменные

---

## 💬 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Запустить бота |
| `/new` | Очистить историю диалога |
| `/help` | Примеры вопросов |

---

## 📚 База знаний агента

Системный промпт составлен на основе:

- **Finnerty** «Project Financing: Asset-Based Financial Engineering»
- **Yescombe** «Principles of Project Finance»
- **Gatti** «Project Finance in Theory and Practice»
- Стандартов **EBRD / IFC / ADB**
- **Equator Principles EP4**
- Российского законодательства: 214-ФЗ, 115-ФЗ, 224-ФЗ, механизмов ДОМ.РФ и СЗПК

Агент знает: структурирование сделок (SPV, waterfall, security package), кредитный анализ (DSCR, LLCR, ICR), типы долга (senior, mezzanine, subordinated), кредитную документацию, ГЧП/концессии, эскроу, реструктуризацию и workout.

---

## ✏️ Как улучшить бота

Откройте `bot.py` и найдите переменную `SYSTEM_PROMPT`. Можете добавить туда:
- Специфику конкретных отраслей (энергетика, инфраструктура, недвижимость)
- Примеры реальных сделок вашей компании
- Внутренние методологии и критерии кредитования

---

## ⚠️ Стоимость

- **Railway / Render**: бесплатный план покрывает небольшой трафик
- **Anthropic API**: ~$0.003 за 1000 токенов (claude-opus-4-5). При 100 вопросах в день — около $1-3/месяц
