import os
from typing import Literal

from pydantic import BaseModel, ConfigDict
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
        # model = "gpt-5.6-luna"
        model = "gpt-4.1-mini"
        provider = openai
    elif model_type.lower() == "claude":
        # model = "claude-sonnet-5"
        model = "claude-sonnet-4-5-20250929"
        provider = anthropic
    else:
        model = "llama3.2"
        provider = ollama
    return model, provider


class Link(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    url: str


class RelevantLinks(BaseModel):
    model_config = ConfigDict(extra="forbid")
    links: list[Link]


LINKS_JSON_SCHEMA = {
    "name": "relevant_links",
    "strict": True,
    "schema": RelevantLinks.model_json_schema(),
}


def message_llm(
    system_prompt: str,
    user_prompt: str,
    model_type: Literal["gpt", "claude", "llama"] = "gpt",
    json=False,
) -> str:
    model, provider = define_model_and_provider(model_type)
    if json is True:
        json_response_format = (
            {"type": "json_schema", "json_schema": LINKS_JSON_SCHEMA}
            if model_type == "claude"
            else {"type": "json_object"}
        )
    else:
        json_response_format = {"type": "text"}
    response = provider.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=json_response_format,
    )
    result = response.choices[0].message.content or ""
    return result
