from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, NamedTuple, Optional, Self

from cachetools import TTLCache
import openai

from blobby import openai_profile as profile
from blobby.constants import OPENAI_OPTS, CONVERSATION_CACHE_TTL_HOURS


class _Conversation(NamedTuple):
    username: str
    text: str

    def __str__(self):
        return f"{self.username}: {self.text}"


class _CachedConversation:
    """
    Cached Conversation caches x amount of messages from y amount of chats
    chat_buffer_size must be greater or equal to 1
    conversation_buffer_size must be greater than 4 and it must be divisible by 2
    """
    def __init__(self, chat_buffer_size: int, conversation_buffer_size: int) -> Self:
        self._conversation_buffer_size = conversation_buffer_size
        self.cached_chat = TTLCache(
            maxsize=chat_buffer_size,
            ttl=timedelta(hours=CONVERSATION_CACHE_TTL_HOURS),
            timer=datetime.now,
        )


    def get_conversation(self, chat_id: int) -> Optional[_Conversation] | list[_Conversation]:
        return self.cached_chat.get(chat_id)


    def add_conversation(self, chat_id: int, conversation = _Conversation) -> None:
        cached_conversation = self.cached_chat.get(chat_id)
        if cached_conversation is None:
            cached_conversation = deque(maxlen=self._conversation_buffer_size)

        cached_conversation.append(conversation)
        self.cached_chat.update({chat_id: cached_conversation})


_conversation_cacher = _CachedConversation(profile.chat_buffer_size, profile.conversation_buffer_size)


def _generate_prompt(profile_text: str, conversation: Iterable[_Conversation]) -> str:
    prompt = f"{profile_text}\n\n"
    prompt += '\n'.join(str(user) for user in conversation)
    return prompt


def generate_text(input_text: str, chat_id: int, user_id: int, username: str) -> str:
    input_conversation = _Conversation(username, input_text)
    _conversation_cacher.add_conversation(chat_id, input_conversation)
    prompt = _generate_prompt(profile.prompt, _conversation_cacher.get_conversation(chat_id))

    generated_text = openai.Completion.create(
        model = profile.model,
        prompt = prompt,
        suffix = f"\n{profile.name}:",
        user = str(user_id),
        **OPENAI_OPTS
    )
    # n = choices = 1
    generated_text = generated_text["choices"][0]["text"]
    
    generated_conversation = _generate_prompt(profile.prompt, _Conversation(profile.name, generated_text))
    _conversation_cacher.add_conversation(chat_id, generated_conversation)

    return generated_text
