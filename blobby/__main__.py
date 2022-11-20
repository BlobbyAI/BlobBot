from telegram import Update
from telegram.ext import filters, CommandHandler, MessageHandler

from blobby.generate_text import generate_text
from blobby import blob_app


async def start(update: Update, _) -> None:
    await update.message.reply_text("I'm a friendly blob and I respond to your text messages!")


async def blob(update: Update, _) -> None:
    message = update.message
    input_text = message.text
    user = message.from_user
    chat = message.chat

    generated_text = generate_text(input_text, chat.id, user.id, user.username)
    await update.message.reply_text(generated_text)


if __name__ == '__main__':
    start_handler = CommandHandler("start", start)
    blob_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), blob)
    
    blob_app.add_handler(start_handler)
    blob_app.add_handler(blob_handler)

    blob_app.run_polling(allowed_updates=["message"], drop_pending_updates=True)
