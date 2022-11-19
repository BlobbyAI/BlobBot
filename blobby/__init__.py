import contextlib
from os import environ as env
import logging

import openai
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

with open("blobby_config.toml", "rb") as f:
    openai_profile = from_toml(f)

blob_app = ApplicationBuilder() \
    .token(env.get("BOT_TOKEN")) \
    .build()

if openai_key := env.get("OPENAI_API_KEY"):
    openai.api_key = openai_key
else:
    raise openai.error.AuthenticationError(
        "No OPENAI API key provided. You can generate API keys in the OpenAI web interface."
        + "\nSee https://onboard.openai.com for details."
    )
