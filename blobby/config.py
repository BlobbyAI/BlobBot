from enum import auto, IntEnum
import tomllib
import typing

import attrs

class AIStrength(IntEnum):
    text_ada_001 = 0
    text_babbage_001 = auto()
    text_curie_001 = auto()
    text_davinci_002 = auto()


@attrs.define(frozen=True)
class AIProfile:
    """
    Prompts:
    name: name of the bot, it may change how the bot percieves itself.
    prompt: describes how the bot should respond, it works best with a name. E.g 'marv is a really rude bot'.
    context: Buffer for the amount of conversations to be kept in memory.
    model: 0-3: strength of AI (see https://openai.com/api/pricing for pricing).

    Warning:
    keep the prompt short, as it counts towards every single API request.
    keep the context size small, it may increase the chargers.

    Example presets:
    marv_preset = {name: 'marv', model: 3, context: 1, prompt: 'marv is quite rude'}
	blob_preset = {name: 'blob', model: 3, context: 2, prompt: 'blob is really friendly and jokes a lot'}
    """

    name: str
    prompt: str
    context: int = attrs.field(validator=attrs.validators.instance_of(int))
    model: AIStrength = attrs.field(
        validator = attrs.validators.instance_of(int),
        converter = AIStrength,
    )


def from_toml(tomlfile: typing.BinaryIO) -> AIProfile:
    toml = tomllib.load(tomlfile)
    return AIProfile(**toml["openai-chat"])
