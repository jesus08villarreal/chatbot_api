import openai
import os
from typing import List, Dict

openai.api_key = os.getenv("OPENAI_API_KEY")

def select_client(message: str, clients: List[Dict]) -> Dict:
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Select the most likely client from the following list based on this message: {message}\n\nClients: {clients}",
        max_tokens=50
    )
    result = response.choices[0].text.strip()
    return eval(result)

def select_products(message: str, products: List[Dict]) -> List[Dict]:
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Select the products from the following list based on this message: {message}\n\nProducts: {products}",
        max_tokens=150
    )
    result = response.choices[0].text.strip()
    return eval(result)
