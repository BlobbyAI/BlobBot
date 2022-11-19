from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from blobby import openai_chat, blob_app


async def blob(update: Update, _):
    await update.message.reply_text("I'm a blob")


if __name__ == '__main__':
    blob_handler = CommandHandler("blob", blob)
    blob_app.add_handler(blob_handler)
    
    blob_app.run_polling()
