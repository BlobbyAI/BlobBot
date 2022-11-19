import asyncio

from tornado.platform.asyncio import AsyncIOMainLoop
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
AsyncIOMainLoop().install()
