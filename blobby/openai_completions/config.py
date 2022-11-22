import argparse
from dataclasses import dataclass
import tomllib
from typing import BinaryIO

import attrs


@attrs.define(frozen=True)
class AIProfile:
    """
    Prompts:
        name: name of the bot, it may change how the bot perceives itself.
        description: the way the bot should perceive itself.
        model: name of the model (see https://beta.openai.com/docs/models/gpt-3).
        chat_buffer_size: Buffer for the amount of chats to be kept in memory.
        conversation_buffer_size: Buffer for the amount of conversations of chats to be kept in memory.
        retry_on_fail: retry if it fails to generate text

    Conversation Caching:
        caches x amount of messages from y amount of chats
        chat_buffer_size must be greater than or equal to 1
        conversation_buffer_size must be greater than or equal to 3

    Warning:
        keep the description and the buffer sizes short,
        as it counts towards every single API request.

    Example presets:
        marv_preset = {
            name: 'Marv',
            description: 'really rude.',
            model: 'text-davinci-002',
            chat_buffer_size: 2,
            conversation_buffer_size: 3,
        }
        blob_preset = {
            name: 'Blob',
            description: 'really friendly and jokes a lot.',
            model: 'text-davinci-002',
            chat_buffer_size: 5,
            conversation_buffer_size: 5,
        }
    """

    name: str
    description: str
    model: str
    chat_buffer_size: int = attrs.field(validator = attrs.validators.ge(1))
    conversation_buffer_size: int = attrs.field(validator = attrs.validators.ge(3))


def from_toml(tomlfile: BinaryIO) -> AIProfile:
    toml = tomllib.load(tomlfile)
    return AIProfile(**toml["openai-profile"])


def config_argparse() -> AIProfile:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help = "path to the config.toml file",
        type = argparse.FileType("rb"),
        required = True,
    )
    args = parser.parse_args()

    return from_toml(args.config)
