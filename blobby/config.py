from dataclasses import dataclass
import tomllib
from typing import BinaryIO


@dataclass(frozen=True, slots=True, eq=False)
class AIProfile:
    """
    Prompts:
    name: name of the bot, it may change how the bot percieves itself.
    prompt: describes how the bot should respond, it works best with a name. E.g 'marv is a really rude bot'.
    conversation_buffer_size: Buffer for the amount of conversations to be kept in memory.
    model: name of the model (see https://beta.openai.com/docs/models/gpt-3).

    Warning:
    keep the prompt short, as it counts towards every single API request.
    keep the context size small, it may increase the chargers.

    Example presets:
    marv_preset = {name: 'marv', model: 'text-davinci-002', context: 1, prompt: 'marv is quite rude'}
    blob_preset = {name: 'blob', model: 'text-davinci-002', context: 2, prompt: 'blob is really friendly and jokes a lot'}
    """

    name: str
    prompt: str
    model: str
    conversation_buffer_size: int


def from_toml(tomlfile: BinaryIO) -> AIProfile:
    toml = tomllib.load(tomlfile)
    return AIProfile(**toml["openai-profile"])
