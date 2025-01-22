from openai import OpenAI
import os

opnai_key = os.getenv('OPENAI_API_KEY')
if opnai_key is None:
    message = f"Cannot get env. var '{'OPENAI_API_KEY'}'. Perhaps is not set?"
    raise ValueError(message)

client = OpenAI(api_key=opnai_key)


def get_floor_area(text: str) -> str:
    response = client.chat.completions.create(
        model= "gpt-4o-mini",
        max_tokens= 300,
        temperature= 0.0,
        messages= [
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": 
                    """Based on this text what is the area of the house in square meters? how many rooms are there in this house?"""
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"{text}"
                }
            ]
            }
        ]
        )
    return response.choices[0].message.content