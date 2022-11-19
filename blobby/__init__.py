import contextlib

with contextlib.suppress(ImportError):
    import uvloop
    import asyncio
    from tornado.platform.asyncio import AsyncIOMainLoop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    AsyncIOMainLoop().install()
