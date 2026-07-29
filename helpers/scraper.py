import json
from typing import Literal

# import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from helpers.prompt_maker import get_links_system_prompt, get_links_user_prompt

# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_soup(url: str):
    # response = requests.get(url, headers=headers)
    # return BeautifulSoup(response.content, "html.parser")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=headers["User-Agent"])
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        html = page.content()
        browser.close()
    return BeautifulSoup(html, "html.parser")


def fetch_website_contents(soup):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return f"{title}\n\n{text}"[:2000]


def fetch_website_links(soup) -> list[str]:
    """
    Return the links on the webiste at the given url
    """
    links = [link.get("href") for link in soup.find_all("a")]
    return [str(link) for link in links if link]


def select_relevant_links(
    url: str, links: list[str], model_type: Literal["gpt", "claude", "llama"]
):
    from helpers.chat import message_llm

    system_prompt = get_links_system_prompt()
    user_prompt = get_links_user_prompt(url, links)
    result = message_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_type=model_type,
        json=True,
    )
    links = json.loads(result)
    return links


def fetch_page_and_all_relevant_links(contents: str, relevant_links):
    result = f"## Landing Page:\n\n{contents}\n\nRelevant Links:"
    for link in relevant_links["links"]:
        try:
            soup = fetch_website_soup(link["url"])
        except PlaywrightError as e:
            print(f"Skipping {link['url']}: {e}")
            continue
        link_contents = fetch_website_contents(soup)
        result += f"\n\n###Link: {link['type']}\n"
        result += link_contents
    return result
