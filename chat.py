import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

anthropic_url = "https://api.anthropic.com/v1"

openai = OpenAI(api_key=openai_api_key)
anthropic = OpenAI(base_url=anthropic_url, api_key=anthropic_api_key)


def define_model_and_provider(
    model_type: Literal["gpt", "claude"],
) -> tuple[str, OpenAI]:
    if model_type.lower() == "gpt":
        model = "gpt-5.6-luna"
        provider = openai
    else:
        model = "claude-sonnet-5"
        provider = anthropic
    return model, provider


def chat(
    system_prompt: str,
    user_prompt: str,
    model_type: Literal["gpt", "claude"] = "gpt",
) -> str:
    model, provider = define_model_and_provider(model_type)
    response = provider.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    result = response.choices[0].message.content
    return f"{model_type.upper()} says:\n {result}\n"
