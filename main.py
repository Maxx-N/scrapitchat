"""
An application where the user gives a web URL to an LLM, which then acts as a
salesperson in a conversation with the customer to sell the product, service,
brand or person's skill featured on the web page. The conversation is between
the LLM (as the salesperson) and the user (as the customer or prospect).
"""

import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

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


def create_messages() -> list[ChatCompletionMessageParam]:
    system_prompt = "You are a helpful assistant."
    user_prompt = "Who are you?"
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def test_api(model_type: Literal["gpt", "claude"]) -> str:
    model, provider = define_model_and_provider(model_type)
    messages = create_messages()
    response = provider.chat.completions.create(model=model, messages=messages)
    result = response.choices[0].message.content
    return f"{model_type.upper()} says:\n {result}\n"


print(test_api("gpt"))
print(test_api("claude"))
