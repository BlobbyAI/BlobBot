import openai
from telegram import Update
from telegram.ext import filters, CommandHandler, MessageHandler

from blobby import blob_app, openai_profile
from blobby.constants import OPENAI_OPTS


async def start(update: Update, _) -> None:
    await update.message.reply_text("I'm a friendly blob and I respond to your text messages!")


async def blob(update: Update, _) -> None:
    generated_text = openai.Completion.create(
        model = openai_profile.model,
        prompt = update.message.text,
        user = str(update.message.from_user.id),
        **OPENAI_OPTS
    )

    await update.message.reply_text(generated_text)


if __name__ == '__main__':
    start_handler = CommandHandler("start", start)
    blob_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), blob)
    
    blob_app.add_handler(start_handler)
    blob_app.add_handler(blob_handler)

    blob_app.run_polling()
