from os import environ as env
import textwrap

import openai

from .openai_completions import OpenAICompletions

if openai_key := env.get("OPENAI_API_KEY"):
    openai.api_key = openai_key
else:
    raise openai.error.AuthenticationError(textwrap.dedent("""\
            No API key provided. Set the environment variable OPENAI_API_KEY=<API-KEY>).
            You can generate API keys in the OpenAI web interface.
            See https://onboard.openai.com for details, or email support@openai.com if you have any questions.
        """))
