"""
An application where the user gives a web URL to an LLM, which then acts as a
salesperson in a conversation with the customer to sell the product, service,
brand or person's skill featured on the web page. The conversation is between
the LLM (as the salesperson) and the user (as the customer or prospect).
"""

import json
from typing import Literal

from helpers.chat import chat
from helpers.prompt_maker import get_links_system_prompt, get_links_user_prompt


def select_relevant_links(url: str, model_type: Literal["gpt", "claude", "llama"]):
    system_prompt = get_links_system_prompt()
    user_prompt = get_links_user_prompt(url)
    result = chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_type=model_type,
        json=True,
    )
    links = json.loads(result)
    return links


print(select_relevant_links("https://www.anthropic.com/", "llama"))
