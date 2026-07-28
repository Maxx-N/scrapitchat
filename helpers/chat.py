import os
from typing import Literal

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict

from helpers.scraper import fetch_website_contents


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


def chat(message, history, model_type: Literal["gpt", "claude", "llama"], state):
    if state is None:
        state = {"url_loaded": False, "system_prompt": "You are a helpful assistant"}
    if not state["url_loaded"]:
        try:
            website_contents = fetch_website_contents(message)
        except Exception as e:
            print(e)
            return (
                f'I couldn\'t fetch that URL: "{message}".\nPlease send a valid website URL (including https://).',
                state,
            )
        state = {**state, "url_loaded": True}
        return (
            f"Got it — I've loaded {message}. What would you like to know about it?",
            state,
        )

    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = (
        [{"role": "system", "content": state["system_prompt"]}]
        + history
        + [{"role": "user", "content": message}]
    )
    model, provider = define_model_and_provider(model_type=model_type)
    result = provider.chat.completions.create(model=model, messages=messages)
    return (result.choices[0].message.content, state)


def chat_with_gradio():
    dropdown = gr.Dropdown(
        choices=["gpt", "claude", "llama"], value="gpt", label="Model"
    )
    state = gr.State(None)
    chatbot = gr.Chatbot(
        value=[
            {
                "role": "assistant",
                "content": "Hi! Send me a website URL (including https://) and I'll answer questions about it.",
            }
        ]
    )
    gr.ChatInterface(
        fn=chat,
        chatbot=chatbot,
        additional_inputs=[dropdown, state],
        additional_outputs=[state],
    ).launch(inbrowser=True)
