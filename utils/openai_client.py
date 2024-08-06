from openai import OpenAI
import os
from typing import List, Dict

open_ai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

client.api_key = open_ai_key

def select_client(message: str, clients: List[Dict]) -> Dict:
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. that helps to select a client based on the information provided that is a list and a message with the client information, and you will select the most likely client from the list based on the message and return it as a json object" },
                    {"role": "assistant", "content": "I can help you find a client based on the information you provide me."},
                    {"role": "user", "content": f"Select the most likely client from the following list based on this message: {message}\n\nClients: {clients}"},
                ],
                temperature=0.0
            )
        except Exception as e:
            return str(e)
        return response.choices[0].message.content

def select_products(message: str, products: List[Dict]) -> List[Dict]:
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. that helps to select a product based on the information provided that is a list and a message with the product information. and you will return a list of products named selected_products in a json object."},
                    {"role": "assistant", "content": "I can help you find a product based on the information you provide me."},
                    {"role": "user", "content": f"Select the most likely product from the following list based on this message, also add the quntity that is on the message: {message}\n\nProducts: {products}"},
                ],
                temperature=0.0
            )
        except Exception as e:
                return str(e)
        return response.choices[0].message.content

def extract_date_time(message: str) -> Dict:
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts date and time from a given message and returns it as a json object. you should extract the date and time from the message provided, return both as delivery_time and delivery_date in a json object."},
                    {"role": "assistant", "content": "I can help you extract the date and time from the information you provide me."},
                    {"role": "user", "content": f"Extract the date and time from the following message: {message}"},
                ],
                temperature=0.0
            )
        except Exception as e:
            return str(e)

        return response.choices[0].message.content
