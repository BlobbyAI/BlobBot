from dataclasses import dataclass
import tomllib
from typing import BinaryIO


@dataclass(frozen=True, slots=True, eq=False)
class AIProfile:
    """
    Prompts:
    conv_buf_size: Buffer for the amount of conversations to be kept in memory.
    model: name of the model (see https://beta.openai.com/docs/models/gpt-3).

    Warning:
    keep the prompt short, as it counts towards every single API request.
    keep the conv_buf_size small, as it may increase the charges.

    Example profiles:
    marv_preset = {model: 'text-davinci-002', conv_buf_size: 1}
    blob_preset = {model: 'text-davinci-002', conv_buf_size: 2}
    """

    model: str
    conv_buf_size: int


def from_toml(tomlfile: BinaryIO) -> AIProfile:
    toml = tomllib.load(tomlfile)
    return AIProfile(**toml["openai-profile"])
