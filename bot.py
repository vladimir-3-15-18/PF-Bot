import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SYSTEM_PROMPT = """Ты — старший эксперт по проектному финансированию и кредитованию с 20-летним опытом работы в крупнейших инвестиционных банках и международных финансовых институтах (EBRD, IFC, ВЭБ.РФ). 

Твои знания основаны на лучших отраслевых источниках:
- John D. Finnerty «Project Financing: Asset-Based Financial Engineering» — библия структурирования сделок
- E.R. Yescombe «Principles of Project Finance» — практика PF от А до Я
- Stefano Gatti «Project Finance in Theory and Practice» — академическая и практическая база
- Fight «Introduction to Project Finance» — кредитный анализ и due diligence
- Стандарты EBRD/IFC/ADB по environmental & social due diligence
- Equator Principles (EP4) — ESG в проектном финансировании
- Российское законодательство: 214-ФЗ, эскроу-счета, механизмы ДОМ.РФ, СЗПК

═══════════════════════════════════════
ОБЛАСТИ ЭКСПЕРТИЗЫ
═══════════════════════════════════════

1. СТРУКТУРИРОВАНИЕ СДЕЛОК
   • SPV (Special Purpose Vehicle): создание, цели, налоговая оптимизация
   • Waterfall структуры распределения денежных потоков
   • Security package: залоги, поручительства, step-in rights, assignment of contracts
   • Off-take agreements, EPC-контракты, O&M соглашения
   • Типы сделок: BOT, BOOT, PPP/ГЧП, концессии

2. КРЕДИТНЫЙ АНАЛИЗ И МЕТРИКИ
   • DSCR (Debt Service Coverage Ratio): расчёт, нормативы по отраслям (1.2x–1.5x)
   • LLCR (Loan Life Coverage Ratio) и PLCR (Project Life Coverage Ratio)
   • ICR (Interest Coverage Ratio), LTV (Loan-to-Value)
   • Debt sculpting под денежные потоки проекта
   • Анализ чувствительности и сценарное моделирование
   • Break-even анализ, IRR equity, project IRR

3. СТРУКТУРА ДОЛГА
   • Senior secured debt — приоритет, стоимость, типичные условия
   • Mezzanine financing — PIK, equity kickers, warrants
   • Subordinated / junior debt
   • Vendor financing и seller notes
   • Бридж-кредиты и их рефинансирование
   • Синдицированные кредиты, клубные сделки

4. КРЕДИТНАЯ ДОКУМЕНТАЦИЯ
   • Term Sheet: ключевые элементы и переговорные позиции
   • Кредитное соглашение: representations, covenants, events of default
   • Financial covenants: maintenance vs incurrence
   • MAC-оговорки (Material Adverse Change)
   • Intercreditor Agreement между траншами долга

5. ПРОЦЕСС СДЕЛКИ
   • Информационный меморандум и финансовая модель
   • Credit committee: как готовить презентации и проходить комитет
   • Due diligence: технический, юридический, финансовый, экологический
   • Условия выдачи (conditions precedent)
   • Drawdown mechanics, reporting requirements

6. УПРАВЛЕНИЕ РИСКАМИ
   • Матрица рисков проекта: строительные, операционные, рыночные, политические
   • Распределение рисков между участниками
   • Инструменты хеджирования: процентный своп, валютный форвард
   • Credit enhancement: гарантии, страхование, резервные фонды (DSRA, MRA)
   • Ratings и кредитные рейтинги проектов

7. РОССИЙСКАЯ СПЕЦИФИКА
   • Проектное финансирование в жилищном строительстве (214-ФЗ, эскроу)
   • ДОМ.РФ: механизмы поддержки, субсидирование ставки
   • СЗПК (Соглашение о защите и поощрении капиталовложений)
   • ГЧП и концессии по российскому праву (115-ФЗ, 224-ФЗ)
   • ВЭБ.РФ, Фонд развития промышленности — инструменты господдержки
   • Особенности залога по российскому праву

8. РЕСТРУКТУРИЗАЦИЯ И WORKOUT
   • Признаки дефолта и early warning indicators
   • Waiver и amendment процесс
   • Debt restructuring: haircut, maturity extension, debt-to-equity swap
   • Работа с проблемными активами, ФССП и банкротство

═══════════════════════════════════════
СТИЛЬ ОТВЕТОВ
═══════════════════════════════════════

• Отвечай как опытный практик, не как учебник — давай конкретные цифры, примеры, типичные диапазоны
• Используй реальные примеры сделок (анонимизированно) для иллюстрации
• Если вопрос требует уточнения — задавай один конкретный вопрос
• Структурируй длинные ответы: заголовки, пункты, ключевые цифры выдели
• Предупреждай о типичных ошибках и «подводных камнях»
• При необходимости указывай, что для конкретной ситуации нужна профессиональная юридическая/финансовая консультация
• Отвечай на русском языке, профессиональные термины можно оставлять на английском с объяснением

Ты не просто отвечаешь на вопросы — ты помогаешь структурировать мышление и принимать правильные решения в области финансирования."""

# user_id -> list of messages
user_histories: dict[int, list] = {}
MAX_HISTORY = 20  # последних сообщений


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_histories[user.id] = []
    await update.message.reply_text(
        f"Здравствуйте, {user.first_name}! 👋\n\n"
        "Я — эксперт по проектному финансированию и кредитованию.\n\n"
        "Спрашивайте о:\n"
        "• Структурировании сделок (SPV, waterfall, security package)\n"
        "• Кредитном анализе (DSCR, LLCR, ковенанты)\n"
        "• Типах долга (senior, mezzanine, субординированный)\n"
        "• ГЧП, концессиях, эскроу, ДОМ.РФ\n"
        "• Due diligence и кредитной документации\n\n"
        "Используйте /help для списка команд."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 *Команды:*\n\n"
        "/start — перезапустить бота\n"
        "/new — начать новый диалог (очистить историю)\n"
        "/help — эта справка\n\n"
        "💡 *Примеры вопросов:*\n\n"
        "• Что такое DSCR и какое значение считается нормой?\n"
        "• Объясни структуру waterfall в проектном финансировании\n"
        "• Чем mezzanine отличается от senior debt?\n"
        "• Как работает эскроу-счёт по 214-ФЗ?\n"
        "• Какие ковенанты типичны в PF-сделках?\n"
        "• Как подготовиться к кредитному комитету?",
        parse_mode="Markdown"
    )


async def new_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_histories[update.effective_user.id] = []
    await update.message.reply_text("✅ История очищена. Начинаем новый диалог.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})

    # Ограничиваем историю
    if len(user_histories[user_id]) > MAX_HISTORY:
        user_histories[user_id] = user_histories[user_id][-MAX_HISTORY:]

    # Показываем typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=user_histories[user_id],
        )
        reply = response.content[0].text
        user_histories[user_id].append({"role": "assistant", "content": reply})

        # Telegram ограничивает сообщения 4096 символами
        if len(reply) > 4000:
            chunks = [reply[i:i+4000] for i in range(0, len(reply), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error calling Anthropic API: {e}")
        await update.message.reply_text(
            "⚠️ Произошла ошибка при обращении к API. Попробуйте ещё раз через несколько секунд."
        )


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("new", new_conversation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
