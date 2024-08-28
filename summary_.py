from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def generate_summary(text, max_token_limit, language):
    # Adjust max token limit for non-English language
    if language != "English":
        max_token_limit = int(max_token_limit * 3)

    prompt = f"give me a comnbined summary of these articles in {language} in a readable text format:\n" + text

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_token_limit,
    )

    return completion.choices[0].message.content
