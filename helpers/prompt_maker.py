from helpers.scraper import fetch_website_links


def get_links_system_prompt():
    return """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to navigate to for a salesperson
who must sell the product, service, brand or person's skill featured on the web page 
in a conversation with a customer who will ask questions.
E. g., links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
 
"""


def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url}.
Please decide which of these are relevant web links to navigate to for a salesperson
who must sell the product, service, brand or person's skill featured on the web page 
in a conversation with a customer who will ask questions.
Respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

    """
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt
