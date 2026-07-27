import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

anthropic_url = "https://api.anthropic.com/v1"
ollama_url = "http://localhost:11434/v1"

openai = OpenAI(api_key=openai_api_key)
anthropic = OpenAI(base_url=anthropic_url, api_key=anthropic_api_key)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)


def define_model_and_provider(
    model_type: Literal["gpt", "claude", "llama"],
) -> tuple[str, OpenAI]:
    if model_type.lower() == "gpt":
        model = "gpt-5.6-luna"
        provider = openai
    elif model_type.lower() == "claude":
        model = "claude-sonnet-5"
        provider = anthropic
    else:
        model = "llama3.2"
        provider = ollama
    return model, provider


def chat(
    system_prompt: str,
    user_prompt: str,
    model_type: Literal["gpt", "claude", "llama"] = "gpt",
    json=False,
) -> str:
    model, provider = define_model_and_provider(model_type)
    response = provider.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"} if json else {"type": "text"},
    )
    result = response.choices[0].message.content or ""
    return result
