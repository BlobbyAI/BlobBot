from dataclasses import dataclass
import tomllib
from typing import BinaryIO

import attrs


@attrs.define(frozen=True)
class AIProfile:
    """
    Prompts:
        name: name of the bot, it may change how the bot percieves itself.
        prompt: describes how the bot should respond, it works best with a name. E.g 'marv is a really rude bot'.
        model: name of the model (see https://beta.openai.com/docs/models/gpt-3).
        chat_buffer_size: Buffer for the amount of chats to be kept in memory.
        conversation_buffer_size: Buffer for the amount of conversations of chats to be kept in memory.
        retry_on_fail: retry if it fails to generate text

    Warning:
        keep the prompt short, as it counts towards every single API request.
        keep the context size small, it may increase the chargers.

    Example presets:
        marv_preset = {
            name: 'marv',
            prompt: 'marv is quite rude',
            model: 'text-davinci-002',
            chat_buffer_size: 2,
            conversation_buffer_size: 4,
            retry_on_fail: True,
        }
        blob_preset = {
            name: 'blob',
            prompt: 'blob is really friendly and jokes a lot',
            model: 'text-davinci-002',
            chat_buffer_size: 5,
            conversation_buffer_size: 6,
            retry_on_fail: True,
        }
    """

    name: str
    prompt: str
    model: str
    chat_buffer_size: int = attrs.field(validator = attrs.validators.ge(1))
    conversation_buffer_size: int = attrs.field(validator = attrs.validators.ge(4))
    retry_on_fail: bool


def from_toml(tomlfile: BinaryIO) -> AIProfile:
    toml = tomllib.load(tomlfile)
    return AIProfile(**toml["openai-profile"])
