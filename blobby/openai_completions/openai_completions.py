from collections.abc import Iterable
import textwrap
from typing import Optional, Self

import openai

from blobby.openai_completions.config import AIProfile
from blobby.openai_completions.cache_conversation import CachedConversation, Conversation
from blobby.openai_completions.constants import CREATION_RETRY_LIMIT, OPENAI_OPTS


class OpenAICompletions:
    def __init__(self: Self, profile: AIProfile) -> Self:
        self.profile = profile
        self.conversation_cacher = CachedConversation(
            profile.chat_buffer_size,
            profile.conversation_buffer_size,
        )


    @staticmethod
    def _generate_prompt(name: str, description: str, conversation: Iterable[Conversation]) -> str:
        prompt = textwrap.dedent(f"""\
            The following is an informal conversation with {name}.
            {name} is {description}

        """)

        prompt += '\n'.join(str(conv) for conv in conversation)
        prompt += f"\n{name}:"

        return prompt


    @staticmethod
    def _create_text(model: str, prompt: str, username: str, user_id: int) -> Optional[str]:
        created_text = openai.Completion.create(
            model = model,
            prompt = prompt,
            stop = f"{username}:",
            user = str(user_id),
            **OPENAI_OPTS,
        )
        # n = choices = 1
        created_text = created_text["choices"][0]["text"]

        return created_text.strip()


    def create_text(self: Self, input_text: str, chat_id: int, user_id: int, username: str) -> Optional[str]:
        input_conversation = Conversation(username, input_text)
        self.conversation_cacher.add_conversation(chat_id, input_conversation)

        prompt = self._generate_prompt(
            self.profile.name,
            self.profile.description,
            self.conversation_cacher.get_conversation(chat_id),
        )

        created_text = self._create_text(self.profile.model, prompt, username, user_id)

        if not created_text:
            return

        created_conversation = Conversation(self.profile.name, created_text)
        self.conversation_cacher.add_conversation(chat_id, created_conversation)

        return created_text
