import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(
        api_key=api_key
    )


def generate_response(prompt: str) -> str:

    client = get_client()

    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content