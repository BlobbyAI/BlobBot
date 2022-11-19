import contextlib
from os import environ as env
import logging

from telegram.ext import ApplicationBuilder

from blobby.config import from_toml


try:
    import uvloop
    import asyncio
    from tornado.platform.asyncio import AsyncIOMainLoop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    AsyncIOMainLoop().install()
except ImportError as e:
    logging.warn(
        f"ImportError: {e.name}"
        + "\ninstall blobby[speedups] for better performance"
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

blob_app = ApplicationBuilder() \
        .token(env.get("BOT_TOKEN")) \
        .build()

with open("blobby_config.toml", "rb") as f:
    openai_chat = from_toml(f)
