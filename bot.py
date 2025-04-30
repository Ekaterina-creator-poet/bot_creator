from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

NAME, PHONE, COMMENT = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Оставить заявку 📝"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я DROP - бот компании DROPCOLOR. Я помогу вам записаться на мастер-класс по текстильному ручному окрашиванию!\n\nНажмите кнопку ниже или введите /start",
        reply_markup=reply_markup
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Очень приятно. Укажите контактный номер телефона, чтобы наш менеджер с Вами связался:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Когда Вы хотите прийти на мастер-класс и сколько вас будет человек?")
    return COMMENT

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['comment'] = update.message.text

    with open("zayavki.txt", "a", encoding="utf-8") as f:
        f.write(f"{context.user_data['name']} | {context.user_data['phone']} | {context.user_data['comment']}\n")

    await update.message.reply_text("Спасибо! Заявка принята 😊 Скоро с Вами свяжется наш менеджер.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ок, отмена заявки 🙌")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("8078902046:AAFs5MKcNtZLkrmJStv6sUTN7fBAhYw4fWM").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
