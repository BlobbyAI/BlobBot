from collections import deque
from datetime import datetime, timedelta
from typing import NamedTuple, Optional, Self

from cachetools import TTLCache

from blobby.openai_completions.constants import CONVERSATION_CACHE_TTL_HOURS


class Conversation(NamedTuple):
    """
    Basic layout of a conversation with,
    sanitized string representation to replace the new lines,
    with spaces, to avoid impersonation attempts.
    """

    username: str
    text: str

    def __str__(self: Self):
        text = self.text.replace("\n", " ")
        return f"{self.username}: {text}"


class CachedConversation:
    """
    Cached Conversation caches x amount of messages from y amount of chats
    chat_buffer_size must be greater than or equal to 1
    conversation_buffer_size must be greater than or equal to 4
    """

    def __init__(self: Self, chat_buffer_size: int, conversation_buffer_size: int) -> Self:
        self._conversation_buffer_size = conversation_buffer_size
        self.cached_chat = TTLCache(
            maxsize=chat_buffer_size,
            ttl=timedelta(hours=CONVERSATION_CACHE_TTL_HOURS),
            timer=datetime.now,
        )


    def get_conversation(self: Self, chat_id: int) -> Optional[deque[Conversation]]:
        return self.cached_chat.get(chat_id)


    def add_conversation(self: Self, chat_id: int, conversation = Conversation) -> None:
        cached_conversation = self.cached_chat.get(chat_id)
        if cached_conversation is None:
            cached_conversation = deque(maxlen=self._conversation_buffer_size)

        cached_conversation.append(conversation)
        self.cached_chat.update({chat_id: cached_conversation})
