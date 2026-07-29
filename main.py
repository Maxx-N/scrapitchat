"""
An application where the user gives a web URL to an LLM, which then acts as a
salesperson in a conversation with the customer to sell the product, service,
brand or person's skill featured on the web page. The conversation is between
the LLM (as the salesperson) and the user (as the customer or prospect).
"""

from helpers.chat import chat_with_gradio

chat_with_gradio()
