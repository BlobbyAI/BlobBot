import contextlib
from os import environ as env

import telegram

from blobby.config import from_toml


with contextlib.suppress(ImportError):
    import uvloop
    import asyncio
    from tornado.platform.asyncio import AsyncIOMainLoop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    AsyncIOMainLoop().install()

blob_bot = telegram.Bot(env.get("BOT_TOKEN"))
with open("blobby_config.toml", "rb") as f:
    openai_chat = from_toml(f)
