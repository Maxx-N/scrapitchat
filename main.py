"""
An application where the user gives a web URL to an LLM, which then acts as a
salesperson in a conversation with the customer to sell the product, service,
brand or person's skill featured on the web page. The conversation is between
the LLM (as the salesperson) and the user (as the customer or prospect).
"""

import json
from typing import Literal

from helpers.chat import chat_with_gradio, message_llm
from helpers.prompt_maker import get_links_system_prompt, get_links_user_prompt
from helpers.scraper import fetch_website_contents


def select_relevant_links(url: str, model_type: Literal["gpt", "claude", "llama"]):
    system_prompt = get_links_system_prompt()
    user_prompt = get_links_user_prompt(url)
    result = message_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_type=model_type,
        json=True,
    )
    links = json.loads(result)
    return links


def fetch_page_and_all_relevant_links(
    url: str, model_type: Literal["gpt", "claude", "llama"]
):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url=url, model_type=model_type)
    result = f"## Landing Page:\n\n{contents}\n\nRelevant Links:"
    for link in relevant_links["links"]:
        result += f"\n\n###Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result


chat_with_gradio(model_type="llama")
