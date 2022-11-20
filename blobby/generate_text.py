from collections.abc import Iterable
from typing import Optional

import openai

from blobby import openai_profile as profile
from blobby.cache_conversation import CachedConversation, Conversation
from blobby.constants import GENERATION_RETRY_LIMIT, OPENAI_OPTS


_conversation_cacher = CachedConversation(profile.chat_buffer_size, profile.conversation_buffer_size)


def _generate_prompt(profile_text: str, conversation: Iterable[Conversation]) -> str:
    prompt = f"{profile_text}\n\n"
    prompt += '\n'.join(str(user) for user in conversation)
    return prompt


def _create_text(model: str, prompt: str, name: str, user_id: int) -> Optional[str]:
    generated_text = openai.Completion.create(
        model = model,
        prompt = prompt,
        suffix = f"\n{name}: ",
        user = str(user_id),
        **OPENAI_OPTS,
    )
    # n = choices = 1
    generated_text = generated_text["choices"][0]["text"]
    return generated_text.strip()


def generate_text(input_text: str, chat_id: int, user_id: int, username: str) -> str:
    input_conversation = Conversation(username, input_text)
    _conversation_cacher.add_conversation(chat_id, input_conversation)
    prompt = _generate_prompt(profile.prompt, _conversation_cacher.get_conversation(chat_id))

    generated_text = _create_text(profile.model, prompt, profile.name, user_id)

    if profile.retry_on_fail and not generated_text:
        for _ in range(GENERATION_RETRY_LIMIT):
            if generated_text := _create_text(profile.model, prompt, profile.name, user_id):
                break

        else:
            return "[ERR]: retry limit reached."

    generated_conversation = _generate_prompt(profile.prompt, Conversation(profile.name, generated_text))
    _conversation_cacher.add_conversation(chat_id, generated_conversation)

    return generated_text
