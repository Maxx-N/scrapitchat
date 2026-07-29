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


def get_links_user_prompt(url, links):
    user_prompt = f"""
Here is the list of links on the website {url}.
Please decide which of these are relevant web links to navigate to for a salesperson
who must sell the product, service, brand or person's skill featured on the web page 
in a conversation with a customer who will ask questions.
Respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

    """
    user_prompt += "\n".join(links)
    return user_prompt


def get_sales_representative_system_prompt(website_contents: str):
    system_promt = """You are a sales representative in a conversation with a customer.
Your job is to answer their questions about a product, service, brand, or a person’s skills, with the goal of selling that item to them.
To do this, you have access to content from several relevant web pages, which you must always use. 
Be extremely persuasive and enthusiastic about what you’re selling, presenting the facts in the best possible light.
Here are the contents of the landing page and other relevant pages to use:\n\n"""
    system_promt += website_contents
    system_promt = system_promt[:5_000]
    return system_promt
