from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()

api_key = os.getenv("OPENAI_API_KEY")

client.api_key = api_key

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant. that reads and organizes orders."},
                {"role": "assistant", "content": "Please organize the following orders and return them in a json format with the following structure: {'items': [{'item': 'item1', 'quantity': 1}, {'item': 'item2', 'quantity': 2}]}"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0
        )
    except Exception as e:
        return str(e)
    # Transformamos el json de objetos a un array de python
    return response.choices[0].message.content
